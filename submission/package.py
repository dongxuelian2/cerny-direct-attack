"""Packaging-only checks and sealed release generation; standard library only.

No Lean builds, mathematical searches or experiment replays are run here.
The full ZIP checksum is detached to avoid a self-referential checksum.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MATH = 'f30afd64643d785dff7ec5d44c730cb36a80dce6'
VALIDATED = 'b8d7362e3466d17b1dc611a7ef1bead90c878074'
RECEIPTS = ('submission/COMPLETION.md', 'submission/COMPLETION.json')
MARKER = b'$Format:%H$'
PACKAGING = {
    '.gitattributes', 'STATUS.json', 'README.md', 'START_HERE.md',
    'REPRODUCIBILITY.md', 'OPENMATH_SUBMISSION.md',
    'POST_BASELINE_RESEARCH_LEDGER.md', 'submission/VALIDATION.md',
    'submission/SHA256.json', 'submission/PATH_MIGRATIONS.json',
    'submission/package.py', 'post_baseline/audit/verify_manifest.py',
    'submission/audit.py', 'direct_attack/ONE_CLUSTER_UPPER_PROOF_AUDIT.md',
    *RECEIPTS,
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def environment():
    env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
    n = int(env.get('GIT_CONFIG_COUNT', '0'))
    env.update({'GIT_CONFIG_COUNT': str(n+1), 'GIT_CONFIG_KEY_'+str(n): 'safe.directory',
                'GIT_CONFIG_VALUE_'+str(n): ROOT.as_posix()})
    return env


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, env=environment())


def markdown_links(source):
    # Ignore fenced/inline code; read inline links, images and reference targets.
    source = re.sub(r'(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', source)
    source = re.sub(r'(?m)^ {4}[^\n]*$', '', source)
    source = re.sub(r'`+[^`\n]*`+', '', source)
    target = r'(<[^>\n]+>|(?:\\.|[^\s()])+)(?:\s+["\'][^\n]*?["\'])?'
    for match in re.finditer(r'!?\[[^\]\n]*\]\(\s*'+target+r'\s*\)', source):
        yield match.group(1).strip('<>')
    definitions = {}
    for match in re.finditer(r'(?m)^\s*\[([^\]]+)\]:\s*'+target, source):
        definitions[match.group(1).casefold()] = match.group(2).strip('<>')
        yield match.group(2).strip('<>')
    # Undefined bracket pairs (e.g. A[p][q]) are ordinary text, not links.
    # Every defined reference target is checked above, including shortcut links.


def check_paths(root, paths):
    known = set(paths)
    failures = []
    count = 0
    for rel in sorted(known):
        assert rel.isascii(), 'Non-ASCII archive path: '+rel
        assert (root/rel).is_file(), 'Missing package file: '+rel
        if not rel.endswith('.md'):
            continue
        for url in markdown_links((root/rel).read_text(encoding='utf-8')):
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            path = unquote(parsed.path).replace('\\', '/')
            destination = posixpath.normpath(posixpath.join(posixpath.dirname(rel), path)) if path else rel
            count += 1
            if destination.startswith('../') or destination.startswith('/') or not (
                    destination in known or any(p.startswith(destination.rstrip('/')+'/') for p in known)):
                failures.append((rel, url, destination))
    assert not failures, 'Broken relative Markdown links: '+json.dumps(failures, ensure_ascii=False)
    status = json.loads((root/'STATUS.json').read_text(encoding='utf-8'))['final_submission']
    inventory = json.loads((root/'submission/theorems.json').read_text(encoding='utf-8'))
    assert status['authoritative_lean_modules'] == [m['source'] for m in inventory['modules']]
    assert len(inventory['modules']) == 10
    assert sum(len(m['theorems']) for m in inventory['modules']) == 100
    assert status['excluded_frozen_drafts'] == ['lean/Cerny3.lean', 'lean/Cerny4.lean']
    for field in ('authoritative_lean_modules', 'excluded_frozen_drafts'):
        assert all(p in known for p in status[field])
    for field in ('validation_receipt', 'formal_execution_receipt', 'completion_receipt',
                  'machine_completion_receipt'):
        assert status[field] in known, (field, status[field])
    for suite in ('formal', 'baseline', 'post', 'native', 'direct', 'integrity_preseal'):
        receipt = root/('submission/validation_'+suite+'.json')
        assert receipt.is_file() and json.loads(receipt.read_text(encoding='utf-8'))['all_passed']
    migrations = json.loads((root/'submission/PATH_MIGRATIONS.json').read_text(encoding='utf-8'))
    references = 0
    manifests = [p for p in known if p.endswith('sha256_manifest.json')]
    manifests += ['submission/validation_direct.json', 'submission/HISTORICAL_EOL.json']
    for rel in manifests:
        data = json.loads((root/rel).read_text(encoding='utf-8'))
        if rel == 'submission/validation_direct.json':
            data = data['input_sha256']
        for old in data:
            assert migrations.get(old, old) in known, 'Unresolved preserved manifest path: '+rel+':'+old
            references += 1
    for line in (root/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        if line.strip():
            _, old = line.split('  ', 1)
            assert migrations.get(old, old) in known, 'Unresolved baseline path: '+old
            references += 1
    print('ARCHIVED_PATHS='+str(len(known))+' RELATIVE_MARKDOWN_LINKS='+str(count)+' PASS')
    print('PRESERVED_MANIFEST_PATH_REFERENCES='+str(references)+' PASS')
    return dict(relative_markdown_links=count, referenced_manifest_paths=references)


def source_check():
    paths = list(filter(None, git('ls-files', '-z').decode('utf-8').split('\0')))
    migrations = json.loads((ROOT/'submission/PATH_MIGRATIONS.json').read_text(encoding='utf-8'))
    allowed = PACKAGING | set(migrations) | set(migrations.values())
    changed = set(filter(None, git('diff', '--name-only', '-z', '--no-renames', VALIDATED).decode('utf-8').split('\0')))
    assert changed <= allowed, 'Changes outside packaging scope: '+str(changed-allowed)
    lean_paths = list(filter(None, git('ls-files', '-z', '*.lean').decode('utf-8').split('\0')))
    assert len(lean_paths) == 12
    for rel in lean_paths:
        assert git('rev-parse', MATH+':'+rel) == git('rev-parse', ':'+rel), rel
        assert (ROOT/rel).read_bytes().replace(b'\r\n', b'\n') == git('show', MATH+':'+rel).replace(b'\r\n', b'\n'), rel
    for old, new in migrations.items():
        assert (ROOT/new).read_bytes() == git('show', VALIDATED+':'+old), new
    status = json.loads((ROOT/'STATUS.json').read_text(encoding='utf-8'))
    assert status['historical_baseline']['original_status'] == json.loads(git('show', VALIDATED+':STATUS.json'))
    subprocess.run([sys.executable, 'submission/seal.py'], cwd=ROOT, env=environment(), check=True)
    references = check_paths(ROOT, paths)
    print('UNCHANGED_MATH_INPUT='+MATH+' LEAN_SOURCES=12 PACKAGING_SCOPE PASS')
    return dict(mathematical_input_identity='PASS', lean_sources_unchanged=12,
                packaging_scope='PASS', canonical_seal='PASS', **references,
                ascii_paths='PASS', byte_identical_manual_renames='PASS')


def extracted_check(root, expected_commit=None):
    receipt = json.loads((root/'submission/COMPLETION.json').read_text(encoding='utf-8'))
    commit = receipt['final_commit']
    assert re.fullmatch(r'[0-9a-f]{40}', commit), 'Unexpanded archive commit identity'
    if expected_commit:
        assert commit == expected_commit
    assert receipt['mathematical_input_revision'] == MATH
    sealed = json.loads((root/'submission/SHA256.json').read_text(encoding='utf-8'))
    for rel, expected in sealed.items():
        data = (root/rel).read_bytes()
        if rel in RECEIPTS:
            assert data.count(commit.encode('ascii')) == 1, rel
            data = data.replace(commit.encode('ascii'), MARKER)
        assert sha(data) == expected, 'Archived canonical hash mismatch: '+rel
    paths = set(sealed) | {'submission/SHA256.json'}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual == paths, 'Archive file inventory mismatch: '+str(actual ^ paths)
    references = check_paths(root, paths)
    print('EXTRACTED_CANONICAL_SEAL='+str(len(sealed))+' COMMIT='+commit+' PASS')
    return dict(final_commit=commit, extracted_canonical_seal='PASS', archive_files=len(paths),
                **references, archive_path_inventory='PASS')


def verify_zip(path, expected_commit=None):
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None, 'ZIP CRC failure'
        commit = archive.comment.decode('ascii')
        assert re.fullmatch(r'[0-9a-f]{40}', commit), 'Missing Git archive commit comment'
        if expected_commit:
            assert commit == expected_commit
        names = archive.namelist()
        assert len(names) == len(set(names)) == len({p.casefold() for p in names})
        for name in names:
            parts = PurePosixPath(name).parts
            assert name.isascii() and not name.startswith('/') and '\\' not in name and '..' not in parts, name
            assert all(not re.match(r'(?i)^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)', p)
                       and not p.endswith((' ', '.')) and ':' not in p for p in parts), name
        with tempfile.TemporaryDirectory(prefix='zip-check-', dir=path.parent) as temporary:
            root = Path(temporary)
            archive.extractall(root)
            result = extracted_check(root, commit)
    result.update(zip_crc='PASS', safe_portable_zip_paths='PASS', extraction='PASS',
                  archive_sha256=sha(path.read_bytes()), archive_bytes=path.stat().st_size)
    return result


def release():
    assert not git('status', '--porcelain=v1'), 'Release requires clean committed worktree'
    commit = git('rev-parse', 'HEAD').decode().strip()
    checks = source_check()
    for argv in ([sys.executable, 'submission/check.py', '--suite', 'integrity'],
                 ['git', 'diff', '--check'], ['git', 'fsck', '--full']):
        subprocess.run(argv, cwd=ROOT, env=environment(), check=True)
    output = ROOT/'results/openmath'
    output.mkdir(parents=True, exist_ok=True)
    path = output/'openmath-final.zip'
    # Git archive applies checkout conversion by default on Windows. Disable it
    # for this command so the ZIP preserves the canonical bytes sealed above.
    subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf',
                    'archive', '--format=zip', '--output='+str(path), commit],
                   cwd=ROOT, env=environment(), check=True)
    checks.update(verify_zip(path, commit))
    assert not git('status', '--porcelain=v1'), 'Worktree changed during packaging'
    assert git('rev-parse', 'HEAD').decode().strip() == commit
    receipt = dict(final_commit=commit, tree=git('rev-parse', 'HEAD^{tree}').decode().strip(),
                   mathematical_input_revision=MATH, validated_submission_revision=VALIDATED,
                   mathematical_sources_unchanged=True, archive_filename=path.name,
                   archive_sha256=checks['archive_sha256'], archive_bytes=checks['archive_bytes'],
                   validated_utc=datetime.now(timezone.utc).isoformat(), all_passed=True,
                   clean_worktree=True, seal_status='PASS', checks=checks,
                   integrity_execution_receipt='integrity.json',
                   included_completion_receipt='submission/COMPLETION.md',
                   checksum_boundary='Full ZIP SHA-256 is detached; in-archive receipt is commit-bound metadata.')
    (output/'openmath-final.COMPLETION.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    (output/'openmath-final.zip.sha256').write_text(receipt['archive_sha256']+'  '+path.name+'\n', encoding='ascii')
    print(json.dumps(receipt, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--check', action='store_true')
    modes.add_argument('--check-extracted', action='store_true')
    modes.add_argument('--release', action='store_true')
    modes.add_argument('--verify-zip', type=Path)
    args = parser.parse_args()
    if args.check:
        source_check()
    elif args.check_extracted:
        extracted_check(ROOT)
    elif args.verify_zip:
        print(json.dumps(verify_zip(args.verify_zip.resolve()), indent=2))
    else:
        release()


if __name__ == '__main__':
    main()
