"""Check source-backed theorem inventory and existing evidence packages."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FORMAL = [
    'lean/CertificateCore.lean',
    'post_baseline/lean_sprint/ResearchCore.lean',
    'post_baseline/lean_sprint/AnchorPotentials.lean',
    'post_baseline/lean_sprint/ThreeAnchorGraph.lean',
    'post_baseline/lean_sprint/Cerny3Checked.lean',
    'post_baseline/lean_sprint/Cerny4Checked.lean',
    'direct_attack/LayeredPairBarrier.lean',
    'direct_attack/KariInverseShrink.lean',
    'direct_attack/KariShrinkProducts.lean',
    'direct_attack/ReflectionCoreCut.lean',
]
ARCHIVAL = ['lean/Cerny3.lean', 'lean/Cerny4.lean']
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_comments(source):
    """Preserve line locations, including nested Lean block comments."""
    result = []
    i = depth = 0
    while i < len(source):
        if source.startswith('/-', i):
            depth += 1
            result.extend('  ')
            i += 2
        elif depth and source.startswith('-/', i):
            depth -= 1
            result.extend('  ')
            i += 2
        elif depth:
            result.append('\n' if source[i] == '\n' else ' ')
            i += 1
        elif source.startswith('--', i):
            end = source.find('\n', i)
            if end < 0:
                end = len(source)
            result.extend(' ' * (end-i))
            i = end
        else:
            result.append(source[i])
            i += 1
    assert depth == 0, 'Unclosed Lean comment'
    return ''.join(result)


def declarations(code):
    tokens = list(re.finditer(r'(?m)^namespace\s+([\w.]+)|^end(?:\s+[\w.]+)?\s*$', code))
    theorems = []
    for match in re.finditer(r'(?ms)^theorem\s+(\w+)\b(.*?)\s*:=\s*by\b', code):
        namespaces = []
        for token in tokens:
            if token.start() >= match.start():
                break
            if token.group(1):
                namespaces.append(token.group(1))
            else:
                assert namespaces
                namespaces.pop()
        theorems.append(dict(name='.'.join(namespaces + [match.group(1)]),
                             line=code[:match.start()].count('\n')+1,
                             statement=('theorem '+match.group(1)+match.group(2)).rstrip()))
    return theorems


def formal_check(lean, env, rows, output, run):
    if not lean:
        sys.path.insert(0, str(ROOT))
        from direct_attack.submission_runtime import lean_compiler
        lean = str(lean_compiler())
    version = run([lean, '--version'], ROOT, env, rows).stdout
    assert re.search(r'\bversion 4\.19\.0(?:,|\s)', version), version
    folder = output / 'formal'
    folder.mkdir(exist_ok=True)
    local_env = dict(env, LEAN_PATH=str(folder))
    inventory = dict(compiler_version=version.strip(), compiler_sha256=sha(Path(lean)),
                     allowed_axioms=sorted(ALLOWED_AXIOMS), modules=[], archival=[])
    files = subprocess.check_output(['git', 'ls-files', '-z', '*.lean'], cwd=ROOT, env=env).decode().split('\0')
    assert set(filter(None, files)) == set(FORMAL + ARCHIVAL), 'Unclassified tracked Lean source'
    for rel in FORMAL + ARCHIVAL:
        source = (ROOT/rel).read_text(encoding='utf-8')
        code = strip_comments(source)
        # These sources contain no string literals. Scan actual code, not prose.
        assert '"' not in code, 'Extend scanner for strings before accepting new code'
        forbidden = re.findall(r'\b(?:sorry|admit|axiom|native_decide|unsafe|implemented_by|extern)\b', code)
        assert not forbidden, (rel, forbidden)
        assert not re.search(r'\b(?:opaque|partial)\b', code), rel
        imports = re.findall(r'(?m)^import\s+(.+)$', code)
        assert all(m in ('Std', 'ResearchCore', 'AnchorPotentials') for m in imports), (rel, imports)
        entry = dict(source=rel, source_sha256=sha(ROOT/rel), imports=imports, theorems=declarations(code))
        if rel in ARCHIVAL:
            # Audit failures explicitly; a failing draft is never a formal result.
            result = subprocess.run([lean, rel], cwd=ROOT, env=local_env, capture_output=True,
                                    text=True, encoding='utf-8', errors='replace')
            rows.append(dict(argv=[lean, rel], cwd=str(ROOT), returncode=result.returncode,
                             stdout=result.stdout, stderr=result.stderr, expected_failure=True))
            assert result.returncode != 0 and 'failed to synthesize' in result.stdout and 'sorryAx' in result.stdout
            entry.update(status='EXCLUDED: frozen noncompiling draft', returncode=result.returncode)
            inventory['archival'].append(entry)
            print('EXPECTED ARCHIVAL FAILURE ' + rel, flush=True)
            continue
        result = run([lean, '-o', folder/(Path(rel).stem+'.olean'), rel], ROOT, local_env, rows)
        assert not re.search(r'sorryAx|\b(?:error|failed)\b', result.stdout+result.stderr), rel
        # Print every source theorem, in its own compilation unit; duplicate
        # namespaces in the historical standalone files cannot be co-imported.
        probe = folder / (Path(rel).stem + 'Audit.lean')
        probe.write_text(source+'\n'+''.join('\n#print '+t['name']+'\n#print axioms '+t['name']+'\n'
                                           for t in entry['theorems']), encoding='utf-8')
        printed = run([lean, str(probe)], ROOT, local_env, rows).stdout
        assert 'sorryAx' not in printed
        for theorem in entry['theorems']:
            name = re.escape(theorem['name'])
            found = re.search("'"+name+"' depends on axioms: \\[([^\\]]*)\\]", printed)
            if found:
                axioms = found.group(1).split(', ') if found.group(1) else []
            else:
                assert "'"+theorem['name']+"' does not depend on any axioms" in printed, theorem
                axioms = []
            assert set(axioms) <= ALLOWED_AXIOMS, (theorem, axioms)
            theorem['axioms'] = axioms
        entry['status'] = 'FORMALLY VERIFIED'
        inventory['modules'].append(entry)
    (output/'theorems.json').write_text(json.dumps(inventory, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    parts = ['# Exact Lean theorem inventory\n\nGenerated from actual source declarations by `submission/check.py --suite formal`.',
             '\nOnly the ten authoritative modules below are FORMALLY VERIFIED. All hypotheses are part of each statement.\n']
    for entry in inventory['modules']:
        parts.append('\n## '+entry['source']+'\n\nSHA-256: `'+entry['source_sha256']+'`\n')
        for theorem in entry['theorems']:
            parts.append('\n`'+theorem['name']+'`, source line '+str(theorem['line'])+
                         ', axioms: '+(', '.join(theorem['axioms']) or 'none')+'.\n\n```lean\n'+theorem['statement']+'\n```\n')
    parts.append('\n## Excluded archival drafts\n\n`lean/Cerny3.lean` and `lean/Cerny4.lean` fail elaboration and produce `sorryAx` in error recovery. Their proved replacements are the checked copies above. No theorem in either draft is submitted as verified.\n')
    (output/'THEOREMS.md').write_text('\n'.join(parts), encoding='utf-8')


def baseline_check(env, rows, output, run):
    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], ROOT, env, rows)
    certificates = sorted((ROOT/'reference_results').rglob('*.json'))
    count = 0
    for path in certificates:
        data = json.loads(path.read_text(encoding='utf-8'))
        if isinstance(data, dict) and 'kind' in data and 'automaton' in data:
            run([sys.executable, 'src/check_certificate.py', str(path)], ROOT, env, rows)
            count += 1
    assert count == 83, count
    for argv in [['demo'], ['compare', '--n', '8'], ['landmarks', '--n', '8'],
                 ['mutate', '--n', '6']]:
        run([sys.executable, 'run.py']+argv+['--out', str(output/('baseline-'+argv[0]))], ROOT, env, rows)
    sys.path.insert(0, str(ROOT))
    from direct_attack.submission_runtime import lean_compiler
    compiler = env.get('ORION_LEAN') or str(lean_compiler())
    for n in range(2, 6):
        generated = output / ('ExportC'+str(n)+'.lean')
        run([sys.executable, 'run.py', 'export-lean', 'reference_results/demo/C'+str(n)+'.json',
             '--out', str(generated)], ROOT, env, rows)
        checked = run([compiler, str(generated)], ROOT, env, rows)
        assert 'sorryAx' not in checked.stdout+checked.stderr
        rows.append(dict(check='generated_export', n=n, source_sha256=sha(generated), returncode=0))


def post_check(env, rows, output, run):
    checks = ['check_uniform', 'layout_experiments', 'endpoint_layout', 'check_normal_form',
              'optimal_language', 'check_language_stabilization', 'check_sharp_language',
              'check_language_counts', 'check_manuscript_source', 'check_affine_certificates']
    for name in checks:
        run([sys.executable, 'post_baseline/'+name+'.py'], ROOT, env, rows)


def integrity_check(env, rows, output, run):
    run(['git', 'diff', '--check'], ROOT, env, rows)
    run(['git', 'fsck', '--full'], ROOT, env, rows)
    run([sys.executable, 'post_baseline/audit/verify_manifest.py'], ROOT, env, rows)
    manifest = json.loads((ROOT/'direct_attack/data/sha256_manifest.json').read_text(encoding='utf-8'))
    # This is historical evidence. Current overrides are separately sealed by
    # submission/SHA256.json; never relabel old captures as fresh executions.
    allowed = {'direct_attack/RESULTS.md', 'direct_attack/README.md',
               'direct_attack/check_layered_pair_barrier_lean.py', 'direct_attack/check_kari_inverse_shrink.py',
               'direct_attack/check_kari_shrink_products.py', 'direct_attack/check_reflection_core_tradeoff.py',
               'direct_attack/weighted_class_reset_native.py', 'direct_attack/KARI_INVERSE_SHRINK_OBSTRUCTION.md',
               'direct_attack/REFLECTION_CORE_TRADEOFF.md', 'direct_attack/LITERATURE_AND_BOTTLENECKS.md',
               # Packaging correction: render [C](P_f-I) as literal mathematics,
               # rather than an accidental link to a nonexistent file.
               'direct_attack/ONE_CLUSTER_UPPER_PROOF_AUDIT.md'}
    changed = []
    restored_eol = []
    recipes = json.loads((ROOT/'submission/HISTORICAL_EOL.json').read_text(encoding='utf-8'))
    frozen = 'f30afd64643d785dff7ec5d44c730cb36a80dce6'
    process = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT, env=env,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for rel, expected in manifest.items():
            process.stdin.write((frozen+':'+rel+'\n').encode('utf-8'))
            process.stdin.flush()
            header = process.stdout.readline().split()
            assert len(header) == 3 and header[1] == b'blob', (rel, header)
            original = process.stdout.read(int(header[2]))
            assert process.stdout.read(1) == b'\n'
            if hashlib.sha256(original).hexdigest() != expected:
                lf = original.replace(b'\r\n', b'\n')
                uniform = {hashlib.sha256(lf).hexdigest(), hashlib.sha256(lf.replace(b'\n', b'\r\n')).hexdigest()}
                if expected not in uniform:
                    recipe = recipes[rel]
                    assert recipe['raw_sha256'] == expected and recipe['lf_sha256'] == hashlib.sha256(lf).hexdigest()
                    lines = lf.split(b'\n')
                    indices = set(recipe['crlf_lines'])
                    assert len(indices) == len(recipe['crlf_lines']) and all(0 <= i < len(lines)-1 for i in indices)
                    restored = b'\n'.join(line+b'\r' if i in indices else line for i,line in enumerate(lines))
                    assert hashlib.sha256(restored).hexdigest() == expected, rel
                restored_eol.append(rel)
            if (ROOT/rel).read_bytes().replace(b'\r\n', b'\n') != original.replace(b'\r\n', b'\n'):
                assert rel in allowed, 'Undocumented historical input change: '+rel
                if rel == 'direct_attack/ONE_CLUSTER_UPPER_PROOF_AUDIT.md':
                    assert (ROOT/rel).read_bytes().replace(b'\r\n', b'\n') == original.replace(
                        b'\r\n', b'\n').replace(b'u_f=[C](P_f-I)', b'`u_f=[C](P_f-I)`'), rel
                changed.append(rel)
    finally:
        process.stdin.close()
        assert process.wait() == 0
    rows.append(dict(check='historical_direct_manifest', entries=len(manifest),
                     immutable_revision=frozen, exact_hash_eol_reconstruction=restored_eol,
                     documented_preparation_overrides=changed, returncode=0))
    current = ROOT/'submission/SHA256.json'
    if current.is_file():
        sealed = json.loads(current.read_text(encoding='utf-8'))
        run([sys.executable, 'submission/seal.py'], ROOT, env, rows)
        rows.append(dict(check='submission_sha256', entries=len(sealed), returncode=0))
    inventory = output/'theorems.json'
    document = ROOT/'OPENMATH_SUBMISSION.md'
    if inventory.is_file() and document.is_file():
        data = json.loads(inventory.read_text(encoding='utf-8'))
        names = {t['name'] for m in data['modules'] for t in m['theorems']}
        cited = set(re.findall(r'`([A-Z]\w*(?:\.\w+)+)`', document.read_text(encoding='utf-8')))
        cited -= {'Classical.choice', 'Quot.sound', 'MANIFEST.sha256', 'STATUS.json'}
        cited = {name for name in cited if not name.endswith(('.md','.json','.lean','.py','.ps1'))}
        assert cited <= names, 'Cited theorem missing from checked source: '+str(cited-names)
        assert all(sha(ROOT/m['source']) == m['source_sha256'] for m in data['modules'])
        rows.append(dict(check='submission_theorem_citations', cited=len(cited), returncode=0))


def native_check(env, rows, output, run):
    compiler = env.get('CXX') or shutil.which('g++', path=env.get('PATH'))
    assert compiler, 'Set CXX or --cxx to an installed g++'
    run([compiler, '--version'], ROOT, env, rows)
    folder = output/'native'
    folder.mkdir(exist_ok=True)
    sources = sorted((ROOT/'direct_attack').glob('*.cpp'))
    assert len(sources) == 8
    for source in sources:
        run([compiler, '-O3', '-std=c++11', '-static-libgcc', '-static-libstdc++',
             source, '-o', folder/(source.stem+'.exe')], ROOT, env, rows)


def check_suite(suite, lean, env, rows, output, run):
    if suite in ('formal', 'all'):
        formal_check(lean, env, rows, output, run)
    if suite in ('baseline', 'all'):
        baseline_check(env, rows, output, run)
    if suite in ('post', 'all'):
        post_check(env, rows, output, run)
    if suite in ('native', 'all'):
        native_check(env, rows, output, run)
    if suite in ('integrity', 'all'):
        integrity_check(env, rows, output, run)
