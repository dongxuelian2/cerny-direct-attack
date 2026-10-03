"""Public reproduction entry point. Historical scientific inputs remain read-only."""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT/'.reproduction'
sys.path.insert(0, str(ROOT))


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canonical_digest(p):
    data=p.read_bytes()
    if p.suffix.lower() not in ('.pdf','.docx','.png','.jpg'):
        data=data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def run(argv, cwd, env, rows):
    tick = time.monotonic()
    result = subprocess.run(list(map(str, argv)), cwd=cwd, env=env,
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
    # A public receipt uses relative checkout/command names, not local paths.
    def portable(s):
        s = s.replace(str(ROOT), '<CHECKOUT>').replace(ROOT.as_posix(), '<CHECKOUT>')
        s = s.replace(sys.executable, '<PYTHON>')
        s = re.sub(r'[A-Z]:[/\\]+[^\s\n\r"\'`<>]*', '<LOCAL_PATH>', s)
        s = re.sub(r'/(?:home|Users|tmp|mnt)/[^\s\n\r"\'`<>]*', '<LOCAL_PATH>', s)
        return s
    rows.append(dict(argv=[portable(str(a)) for a in argv], cwd=portable(str(cwd)),
                     seconds=round(time.monotonic()-tick, 3), returncode=result.returncode,
                     stdout=portable(result.stdout), stderr=portable(result.stderr)))
    print(('PASS ' if result.returncode == 0 else 'FAIL ') + portable(str(argv[1:])), flush=True)
    if result.returncode:
        print(portable(result.stdout+result.stderr), flush=True)
        raise RuntimeError('Check failed; see .reproduction receipt')
    return result


def inventory():
    return json.loads((ROOT/'formal/modules.json').read_text(encoding='utf-8'))


def formal(lean, env, rows):
    from submission.audit import strip_comments, declarations
    selected = lean or env.get('ORION_LEAN') or shutil.which('lean')
    if not selected:
        raise RuntimeError('Lean 4.19.0 required: use --lean or ORION_LEAN')
    version = run([selected, '--version'], ROOT, env, rows).stdout
    if not re.search(r'\bversion 4\.19\.0(?:,|\s)', version):
        raise RuntimeError('Expected exact Lean 4.19.0: '+version)
    inv = inventory()
    accepted = {m['source'] for m in inv['accepted']}
    sources = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*.lean')
               if not any(part in ('.reproduction', '.git', '.lake') for part in p.parts)}
    if sources != accepted | set(inv['excluded']):
        raise RuntimeError('Unclassified Lean sources: '+str(sources ^ (accepted | set(inv['excluded']))))
    folder = OUTPUT/'formal'
    folder.mkdir(parents=True, exist_ok=True)
    local_env = dict(env, LEAN_PATH=str(folder))
    verified = []
    frozen = json.loads((ROOT/'submission/theorems.json').read_text(encoding='utf-8'))
    by_source = {m['source']:m for m in frozen['modules']}
    for module in inv['accepted']:
        path = ROOT/module['source']
        source = path.read_text(encoding='utf-8')
        if canonical_digest(path) != module['source_sha256']:
            raise RuntimeError('Accepted source hash changed; review inventory: '+module['source'])
        code = strip_comments(source)
        if '"' in code or re.search(r'\b(?:sorry|admit|axiom|native_decide|unsafe|implemented_by|extern|opaque|partial)\b', code):
            raise RuntimeError('Forbidden proof shortcut or unclassified string: '+module['source'])
        decls = declarations(code)
        if module['source'] in by_source:
            expected = by_source[module['source']]['theorems']
            if [(d['name'], d['statement']) for d in decls] != [(d['name'], d['statement']) for d in expected]:
                raise RuntimeError('Frozen declaration inventory mismatch: '+module['source'])
        stem = path.stem
        run([selected, '-o', folder/(stem+'.olean'), module['source']], ROOT, local_env, rows)
        probe = folder/(stem+'Probe.lean')
        probe.write_text('import '+stem+'\n'+''.join('#check '+d['name']+'\n#print axioms '+d['name']+'\n' for d in decls), encoding='utf-8')
        result = run([selected, probe], ROOT, local_env, rows)
        if 'sorryAx' in result.stdout:
            raise RuntimeError('sorryAx in accepted theorem')
        axiom_lines = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", result.stdout)
        zero = re.findall(r"'([^']+)' does not depend on any axioms", result.stdout)
        deps = {name:[a.strip() for a in values.split(',') if a.strip()] for name,values in axiom_lines}
        deps.update({name:[] for name in zero})
        if set(deps) != {d['name'] for d in decls}:
            raise RuntimeError('Incomplete printed axiom inventory: '+module['source'])
        for d in decls:
            d['axioms'] = deps[d['name']]
            if not set(d['axioms']) <= set(inv['allowed_axioms']):
                raise RuntimeError('Unexpected axiom dependencies: '+d['name'])
        verified.append(dict(source=module['source'], stage=module['stage'],
                             status='FORMALLY VERIFIED', theorems=decls, source_sha256=module['source_sha256']))
    (folder/'inventory.json').write_text(json.dumps(dict(version=version.strip(), modules=verified), indent=2)+'\n', encoding='utf-8')
    total = sum(len(m['theorems']) for m in verified)
    print('PASS: '+str(len(verified))+' accepted modules, '+str(total)+' declarations; frozen core remains 100', flush=True)
    return {'accepted_modules':len(verified), 'declarations':total, 'frozen_core_declarations':100}


def certificates():
    from src.check_certificate import check
    counts = {}
    for p in sorted((ROOT/'reference_results').rglob('*.json')):
        obj = json.loads(p.read_text(encoding='utf-8'))
        if isinstance(obj, dict) and obj.get('schema') == 'orion.sync-certificate.v1':
            result = check(obj)
            counts[result['kind']] = counts.get(result['kind'], 0)+1
    if sum(counts.values()) != 83:
        raise RuntimeError('Expected all 83 baseline certificates')
    print('PASS: 83 baseline certificates '+str(counts), flush=True)
    return counts


def integrity():
    manifest = json.loads((ROOT/'archive/source_manifest.json').read_text(encoding='utf-8'))
    errors = []
    for e in manifest['entries']:
        p = ROOT/e['public_path']
        if e['storage'] == 'release-asset' and not p.exists():
            continue
        if not p.exists():
            errors.append('Missing preserved source: '+e['public_path'])
        else:
            if canonical_digest(p) != e['public_sha256']:
                errors.append('Source hash mismatch: '+e['public_path'])
    assets = json.loads((ROOT/'archive/assets.json').read_text(encoding='utf-8'))
    allowed_missing = set(assets['scientific_files'])
    doc_count = link_count = python_count = 0
    tracked = subprocess.check_output(['git','ls-files','-z'], cwd=ROOT).decode('utf-8').split('\0')
    paths = [ROOT/p for p in filter(None, tracked)]
    if not paths:
        paths = [p for p in ROOT.rglob('*') if p.is_file() and '.reproduction' not in p.parts and '.git' not in p.parts]
    for p in paths:
        rel = p.relative_to(ROOT).as_posix()
        if p.suffix == '.py':
            ast.parse(p.read_text(encoding='utf-8'), filename=rel); python_count += 1
        if p.suffix == '.json':
            json.loads(p.read_text(encoding='utf-8'))
        if p.suffix == '.md':
            doc_count += 1
            s = p.read_text(encoding='utf-8')
            # Fenced examples are not active Markdown links.
            s = re.sub(r'```.*?```', '', s, flags=re.S)
            s = re.sub(r'(?m)^ {4}.*$', '', s)
            s = re.sub(r'`[^`\n]+`', '', s)
            links = re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', s)
            links += re.findall(r'^\[[^\]]+\]:\s*(\S+)', s, flags=re.M)
            for link in links:
                link = link.strip('<>')
                if urlsplit(link).scheme or link.startswith('#'):
                    continue
                target = (p.parent/unquote(link.split('#')[0])).resolve()
                if not target.exists():
                    try: name = target.relative_to(ROOT.resolve()).as_posix()
                    except ValueError: name = ''
                    if name not in allowed_missing:
                        errors.append(rel+': broken link '+link)
                link_count += 1
        if p.suffix.lower() not in ('.pdf','.docx','.png','.jpg'):
            s = p.read_text(encoding='utf-8', errors='replace')
            if re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}', s):
                errors.append('Potential secret: '+rel)
            if re.search(r'(?:[A-Z]:[/\\]+(?:Users|cerny|tool)|/(?:home|Users)/[^\s])', s):
                errors.append('Private absolute path: '+rel)
            if '@' in s:
                for line in s.splitlines():
                    if '@' in line and re.search(r'[\w.%+-]{1,64}@[\w.-]+\.[A-Za-z]{2,}', line):
                        errors.append('Email needs publication review: '+rel)
    public_seal = ROOT/'archive/public_manifest.json'
    if public_seal.exists():
        for rel, expected in json.loads(public_seal.read_text(encoding='utf-8')).items():
            if canonical_digest(ROOT/rel) != expected:
                errors.append('Publication seal mismatch: '+rel)
    if errors:
        raise RuntimeError('\n'.join(errors))
    print(f'PASS: source provenance, {python_count} Python sources, {doc_count} Markdown documents/{link_count} links, privacy scan', flush=True)
    return dict(python_sources=python_count, markdown_documents=doc_count, internal_links=link_count)


def scratch():
    files = subprocess.check_output(['git','ls-files','-z'], cwd=ROOT).decode('utf-8').split('\0')
    out = Path(tempfile.mkdtemp(prefix='audit-', dir=OUTPUT))
    for rel in filter(None, files):
        source = ROOT/rel
        target = out/rel;target.parent.mkdir(parents=True, exist_ok=True);shutil.copyfile(source,target)
    asset = json.loads((ROOT/'archive/assets.json').read_text(encoding='utf-8'))
    for rel in asset['scientific_files']:
        source = ROOT/rel
        if not source.exists():
            raise RuntimeError('Hydrate release data first: python scripts/hydrate_data.py')
        target = out/rel;target.parent.mkdir(parents=True, exist_ok=True);shutil.copyfile(source,target)
    # Explicit metadata migration for the derived public tree. Certificates and
    # Lean statements are not altered; expected historical file digests change.
    source_manifest = json.loads((ROOT/'archive/source_manifest.json').read_text(encoding='utf-8'))
    originals={e['source_sha256']:e['public_path'] for e in source_manifest['entries']
               if (out/e['public_path']).exists()}
    pattern=re.compile(r'\b[0-9a-f]{64}\b')
    nodes={}
    for folder in ('direct_attack','post_baseline','submission','src'):
        for p in (out/folder).rglob('*'):
            if p.suffix not in ('.py','.json'): continue
            content=p.read_text(encoding='utf-8')
            if any(m[0] in originals for m in pattern.finditer(content)):
                nodes[p]=content
    # Source summaries can depend on other path-redacted summaries. Propagate
    # hashes through that metadata dependency graph, not just one replacement.
    for iteration in range(20):
        translation={old:digest(out/rel) for old,rel in originals.items()}
        changed=False
        for p,base in nodes.items():
            content=pattern.sub(lambda m:translation.get(m[0],m[0]),base)
            if content!=p.read_text(encoding='utf-8'):
                p.write_text(content,encoding='utf-8',newline='\n');changed=True
        if not changed:break
    else:raise RuntimeError('Historical hash migration did not converge; inspect metadata dependencies')
    (out/'direct_attack/native_build').mkdir(exist_ok=True)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', choices=['core','formal','certificates','focused','post','audit','native','all'], default='all')
    parser.add_argument('--lean')
    parser.add_argument('--cxx')
    args = parser.parse_args()
    OUTPUT.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
    if args.lean: env['ORION_LEAN'] = str(Path(args.lean).resolve()) if Path(args.lean).exists() else args.lean
    if args.cxx: env['CXX'] = args.cxx
    rows=[]
    report=dict(suite=args.suite, date_utc=datetime.now(timezone.utc).isoformat(), python=sys.version,
                status='FAIL', runs=rows)
    try:
        if args.suite in ('core','all'):
            run([sys.executable,'-m','unittest','discover','-s','tests','-v'],ROOT,env,rows)
            report['certificates'] = certificates()
            report['integrity'] = integrity()
            run(['git','diff','--check'],ROOT,env,rows)
        if args.suite=='certificates': report['certificates']=certificates()
        if args.suite in ('formal','all'): report['formal']=formal(args.lean,env,rows)
        if args.suite in ('focused','post','audit'):
            out=scratch()
            if args.suite=='focused':
                checks=['check_transposition_fold_obstruction','check_direct_binary_image_obstruction',
                        'check_avoid_compress_sharp_faces','check_avoid_compress_all_gaps',
                        'check_rank_two_permutation_alphabet','check_rank_two_only_nonperm',
                        'check_class_compression_pressure','check_order_two_three_a_barrier',
                        'check_opposite_kernel_primitive_square']
                for name in checks:
                    argv=[sys.executable,'-m','direct_attack.'+name]
                    if name in ('check_rank_two_permutation_alphabet','check_rank_two_only_nonperm'):
                        argv+=['--out','direct_attack/data/public_'+name+'.json']
                    run(argv,out,env,rows)
                report['focused_checks']=len(checks)
            elif args.suite=='audit':
                run([sys.executable,'-m','direct_attack.reproduce'],out,env,rows)
                result=json.loads((out/'direct_attack/data/audit_run.json').read_text(encoding='utf-8'))
                if not result['all_passed'] or len(result['runs'])!=146:raise RuntimeError('Registry audit incomplete')
                report['registered_checks']=146
            else:
                checks=['check_uniform','layout_experiments','endpoint_layout','check_normal_form','optimal_language',
                        'check_language_stabilization','check_sharp_language','check_language_counts','check_manuscript_source','check_affine_certificates']
                for name in checks:run([sys.executable,'post_baseline/'+name+'.py'],out,env,rows)
        if args.suite=='native':
            compiler=args.cxx or env.get('CXX') or shutil.which('g++')
            if not compiler:raise RuntimeError('C++11 compiler required; pass --cxx')
            folder=OUTPUT/'native';folder.mkdir(exist_ok=True)
            sources=sorted((ROOT/'direct_attack').glob('*.cpp'))
            run([compiler,'--version'],ROOT,env,rows)
            for p in sources:run([compiler,'-std=c++11','-O2',p,'-o',folder/(p.stem+'.exe')],ROOT,env,rows)
            report['native_sources_built']=len(sources)
        report['status']='PASS'
    except Exception as exc:
        report['error']=str(exc)
        raise
    finally:
        (OUTPUT/(args.suite+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('Receipt: .reproduction/'+args.suite+'.json',flush=True)


if __name__=='__main__':
    main()
