"""Immutable full graph/first-pair/flag package and isolated replay."""
import ast
from hashlib import sha256
import json
from pathlib import Path,PurePosixPath
import subprocess,sys,zipfile
HERE=Path(__file__).resolve().parent;PAPER=HERE.parent;ROOT=PAPER/'investigation'
NAME=sys.argv[1]
REPORTS=['binary_supplier_cover_audit_20261012.json','supplier_image_controls_audit_20261011.json','supplier_image_horizon_audit_20261011.json',NAME+'_graph_quotient_scope.json',NAME+'_graph_quotient_transport_audit.json',NAME+'_graph_transport_protection_audit.json',NAME+'_binary_supplier_from0_v1_probe.json']

def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    output=HERE/(NAME+'_binary_supplier_quotient_reproduction.json');assert not output.exists()
    files={Path(__file__).resolve()};expected={}
    for name in REPORTS:
        p=HERE/name;d=json.loads(p.read_text());assert d['status'] in ('pass','complete_transport_scope_only','complete_independently_checked_QA_only')
        files.add(p);expected[name]=p.read_bytes()
        for category,base in (('source_sha256',HERE),('root_source_sha256',ROOT)):
            for f,h in d.get(category,{}).items():
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
    prefix=NAME+'_binary_supplier_flags';content={p.relative_to(PAPER).as_posix():p.read_bytes() for p in sorted(files)}
    full=json.loads((HERE/(NAME+'_binary_supplier_from0_v1_probe.json')).read_text())
    assert full['complete_scope'] and full['candidate'] is None and full['binary_only'] is True
    assert full['unrestricted_exclusion'] is False and full['range_start']==0
    commands=[('audit_binary_supplier_cover_20261012.py',[]),('audit_supplier_image_controls.py',[]),
              ('audit_supplier_image_horizon.py',[]),('compile_native_graph_quotient.py',[NAME]),
              ('check_native_graph_quotient.py',[NAME]),('check_native_graph_protection.py',[NAME]),
              ('probe_binary_supplier_range_v1.py',[NAME,'0'])]
    content['README.md']=(
        '# Complete conditional binary native-geometry certificate\n\n'
        'Python >=3.10; standard library only. Geometry: '+NAME+'\n'
        'From _qa move aside the seven stored reports listed in REPORTS, then run:\n'+
        ''.join('python -B '+script+' '+' '.join(args)+'\n' for script,args in commands)+'\n'+
        'The isolated replay regenerates all seven reports byte-identically.\n'
        'Every transported first pair and every binary flag child is checked.\n'
        'The supplier-coverage rule applies only to alphabets of at most two\n'
        'literal letters. It does not exclude arbitrary finite alphabets.\n'
        'Each literal pool and tree has an independent literal/rational checker.\n'
        'The image-propagation rule and binary coverage rule have independently\n'
        'replayed controls. No depth12 safety premise is used.\n'
        'This excludes the stated geometry conditionally at (13,9,1),target12,\n'
        'for binary automata only. It establishes no new F value or separation.\n').encode()
    content['CHECKSUMS.txt']=''.join(f'{sha256(b).hexdigest()}  {n}\n' for n,b in sorted(content.items())).encode()
    archive=HERE/'certificates'/(prefix+'.zip');assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in sorted(content.items()):
            info=zipfile.ZipInfo(prefix+'/'+n,date_time=(2026,10,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
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
    for script,args in commands:
        proc=subprocess.run([sys.executable,'-B',script,*args],cwd=local,capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(script+'\n'+proc.stdout+'\n'+proc.stderr)
        assert json.loads(proc.stdout.splitlines()[-1])['status'] in ('pass','complete_transport_scope_only','complete_independently_checked_QA_only')
        runs.append(dict(script=script,arguments=args,exit=0));print(script+' '+' '.join(args)+': pass',flush=True)
    for name,b in expected.items():assert (local/name).read_bytes()==b,name
    out=dict(status='pass',archive=archive.relative_to(HERE).as_posix(),sha256=digest(archive),files=len(content),
        checksum_entries=len(content)-1,byte_identical_scope_and_audit_reports=7,runs=runs,
        no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        complete_conditional_flag_tree_certificate=True,binary_only=True,unrestricted_exclusion=False,
        scope='Complete native graph/first-pair and binary flag-tree replay only; no unrestricted-alphabet exclusion or numerical F value.',
        source_sha256={Path(__file__).name:digest(Path(__file__)),**{name:digest(HERE/name) for name in REPORTS}})
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
