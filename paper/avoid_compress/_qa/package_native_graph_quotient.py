"""Immutable full graph/first-pair/flag package and isolated replay."""
import ast
from hashlib import sha256
import json
from pathlib import Path,PurePosixPath
import subprocess,sys,zipfile
HERE=Path(__file__).resolve().parent;PAPER=HERE.parent;ROOT=PAPER/'investigation'
NAME=sys.argv[1]
REPORTS=[NAME+'_graph_quotient_scope.json',NAME+'_graph_quotient_transport_audit.json',NAME+'_graph_transport_protection_audit.json',NAME+'_graph_quotient_full_probe.json']
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    output=HERE/(NAME+'_full_quotient_reproduction.json');assert not output.exists()
    files={Path(__file__).resolve()};expected={}
    for name in REPORTS:
        p=HERE/name;d=json.loads(p.read_text());assert d['status'] in ('pass','complete_transport_scope_only','complete_independently_checked_QA_only')
        files.add(p);expected[name]=p.read_bytes()
        for category,base in (('source_sha256',HERE),('root_source_sha256',ROOT)):
            for f,h in d[category].items():
                p=(base/f).resolve();assert p.is_relative_to(PAPER.resolve()) and digest(p)==h,(name,f);files.add(p)
    parent=json.loads((HERE/(NAME+'_inverse_probe.json')).read_text())
    for f,h in parent['source_sha256'].items():
        n='b1_b2_inverse_union_baseline_state.json' if f=='active_research.json' else f
        p=ROOT/n;assert digest(p)==h;files.add(p)
    for name in ['B2_COLUMN_FIRST_PAIR_EXCLUSION.md','B1_B2_INVERSE_UNION_EXCLUSION.md',
                 'THREE_COVER_ATOM_KERNEL_COMPATIBILITY.md','ENTRY_FIBER_FLAG.md',
                 'SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md']:
        files.add(ROOT/name)
    queue=list(files);visited=set()
    while queue:
        p=queue.pop()
        if p.suffix!='.py' or p in visited:continue
        visited.add(p)
        for node in ast.walk(ast.parse(p.read_text())):
            modules=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
            for module in modules:
                name=module.split('.')[0]+'.py'
                for base in (p.parent,HERE,ROOT):
                    q=base/name
                    if q.is_file():
                        if q not in files:files.add(q);queue.append(q)
                        break
    prefix=NAME+'_full_flags';content={p.relative_to(PAPER).as_posix():p.read_bytes() for p in sorted(files)}
    commands=['compile_native_graph_quotient.py','check_native_graph_quotient.py','check_native_graph_protection.py','probe_native_graph_quotient.py']
    content['README.md']=(
        '# Complete graph-first flag certificate for one native geometry\n\nPython >=3.10; standard library only.\n'
        'Geometry: '+NAME+'\n\nFrom _qa, move aside the four stored JSON reports named in REPORTS of\n'
        'package_native_graph_quotient.py, then run in order:\n'+
        ''.join('python -B '+script+' '+NAME+'\n' for script in commands)+'\n'+
        'All four reports regenerate byte identically. The last command can take substantial time.\n'
        'The scope is this enumerated native geometry at (13,9,1), target ac=12,\n'
        'including every retained P1 graph and ordered initial pair. It uses the\n'
        'existing literal/rational flag engine; a depth11 survivor aborts the exclusion.\n'
        'The certificate supplies no new numerical F value or alphabet separation.\n').encode()
    content['CHECKSUMS.txt']=''.join(f'{sha256(b).hexdigest()}  {n}\n' for n,b in sorted(content.items())).encode()
    archive=HERE/'certificates'/(prefix+'.zip');assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in sorted(content.items()):
            info=zipfile.ZipInfo(prefix+'/'+n,date_time=(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
    dest=(HERE/(prefix+'_reproduction')).resolve();assert dest.is_relative_to(HERE.resolve()) and not dest.exists();dest.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(content)
        for n in z.namelist():
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix
            assert (dest/n).resolve().is_relative_to(dest)
        for line in z.read(prefix+'/CHECKSUMS.txt').decode().splitlines():
            h,n=line.split('  ',1);assert sha256(z.read(prefix+'/'+n)).hexdigest()==h
        z.extractall(dest)
    local=dest/prefix/'_qa'
    for name,b in expected.items():
        p=(local/name).resolve();assert p.parent==local.resolve() and p.read_bytes()==b;p.unlink()
    runs=[]
    for script in ('compile_native_graph_quotient.py','check_native_graph_quotient.py','check_native_graph_protection.py','probe_native_graph_quotient.py'):
        proc=subprocess.run([sys.executable,'-B',script,NAME],cwd=local,capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(script+'\n'+proc.stdout+'\n'+proc.stderr)
        assert json.loads(proc.stdout.splitlines()[-1])['status'] in ('pass','complete_transport_scope_only','complete_independently_checked_QA_only')
        runs.append(dict(script=script,arguments=[NAME],exit=0));print(script+': pass',flush=True)
    for name,b in expected.items():assert (local/name).read_bytes()==b,name
    out=dict(status='pass',archive=archive.relative_to(HERE).as_posix(),sha256=digest(archive),files=len(content),
        checksum_entries=len(content)-1,byte_identical_scope_and_audit_reports=4,runs=runs,
        no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        complete_conditional_flag_tree_certificate=True,
        scope='Isolated full native graph/first-pair and flag-tree replay for this geometry only; no new numerical F value.',
        source_sha256={Path(__file__).name:digest(Path(__file__)),**{name:digest(HERE/name) for name in REPORTS}})
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
