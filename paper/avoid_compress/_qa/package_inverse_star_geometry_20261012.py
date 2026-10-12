"""Immutable deterministic full inverse-domain generator/checker replay."""
import ast,json,shutil,subprocess,sys,zipfile
from hashlib import sha256
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent;PAPER=HERE.parent;ROOT=PAPER/'investigation'
NAME='b2_mixed_c4_third7';PREFIX='inverse_star_geometry_20261012'

def digest(p):
    h=sha256()
    with p.open('rb') as f:
        while b:=f.read(8<<20):h.update(b)
    return h.hexdigest()

def main():
    output=HERE/(NAME+'_inverse_native_reproduction_20261012.json');assert not output.exists()
    commands=[('enumerate_inverse_star_geometry_20261012.py',NAME+'_inverse_native_inventory_20261012.json'),
              ('check_inverse_star_geometry_20261012.py',NAME+'_inverse_native_audit_20261012.json')]
    files={Path(__file__).resolve()};expected={}
    for script,report in commands:
        files.add(HERE/script);p=HERE/report;d=json.loads(p.read_text())
        assert d['status'] in ('pass','complete_necessary_native_inventory_QA_only')
        files.add(p);expected[report]=digest(p)
        source_bases=[('source_sha256',ROOT if 'qa_source_sha256' in d else HERE),('qa_source_sha256',HERE),('root_source_sha256',ROOT)]
        for key,base in source_bases:
            for n,h in d.get(key,{}).items():
                f='b1_b2_inverse_union_baseline_state.json' if n=='active_research.json' and base==ROOT else n
                q=(base/f).resolve();assert q.is_relative_to(PAPER.resolve()) and digest(q)==h,(report,n);files.add(q)
    queue=list(files);seen=set()
    while queue:
        p=queue.pop()
        if p.suffix!='.py' or p in seen:continue
        seen.add(p)
        for node in ast.walk(ast.parse(p.read_text())):
            modules=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
            for m in modules:
                for b in (p.parent,HERE,ROOT):
                    q=b/(m.split('.')[0]+'.py')
                    if q.is_file():
                        if q not in files:files.add(q);queue.append(q)
                        break
    content={p.relative_to(PAPER).as_posix():p for p in sorted(files)}
    extra={'README.md':(
        '# Complete conditional native inverse-domain certificate\n\n'
        'Python >=3.10, standard library. Parameter(13,9,1),target12.\n'
        'B={0,4},C={1,4},D={2,4},H={0,1,2},protected state3.\n'
        'The existing necessary entrance-fibre, mandatory-state and P1<=4 premises\n'
        'are documented in investigation/B1_B2_INVERSE_UNION_EXCLUSION.md.\n'
        'All18277 possible immediate graphs are covered, for arbitrary finite alphabets.\n'
        'The independent checker uses literal independent sets, clique-union kernels\n'
        'and full output quotas; no colouring-generator import is used by it.\n'
        'It checks a retained positive control, rejects9 corruptions and checks7 union controls.\n'
        'This excludes only the named native geometry, not all equality configurations.\n'
        'No numerical F value, alphabet separation or folded-profile transport is asserted.\n'
        'The historical baseline is opaque bound input, not current authoritative state.\n'
        'Move aside the following two reports from _qa, then run there in order:\n'+
        ''.join(report+'\n' for script,report in commands)+'\n'+
        ''.join('python -B '+script+'\n' for script,report in commands)+
        'Both recreated reports must match their stored SHA256.\n'
        'Separate gated adoption is required before changing the authoritative frontier.\n').encode()}
    hashes={n:digest(p) for n,p in content.items()};hashes.update({n:sha256(b).hexdigest() for n,b in extra.items()})
    extra['CHECKSUMS.txt']=''.join(h+'  '+n+'\n' for n,h in sorted(hashes.items())).encode()
    archive=HERE/'certificates'/(NAME+'_'+PREFIX+'.zip');assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,allowZip64=True) as z:
        for n in sorted(set(content)|set(extra)):
            info=zipfile.ZipInfo(PREFIX+'/'+n,date_time=(2026,10,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            if n in extra:z.writestr(info,extra[n])
            else:
                with content[n].open('rb') as src,z.open(info,'w',force_zip64=True) as dst:shutil.copyfileobj(src,dst,8<<20)
    dest=(HERE/(PREFIX+'_reproduction')).resolve();assert not dest.exists() and dest.is_relative_to(HERE.resolve());dest.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(hashes)+1
        for n in z.namelist():
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==PREFIX
            assert (dest/n).resolve().is_relative_to(dest)
        z.extractall(dest)
    for n,h in hashes.items():assert digest(dest/PREFIX/n)==h,n
    local=dest/PREFIX/'_qa'
    for script,report in commands:
        p=local/report;assert p.resolve().parent==local.resolve() and digest(p)==expected[report];p.unlink()
    runs=[]
    for script,report in commands:
        proc=subprocess.run([sys.executable,'-B',script],cwd=local,capture_output=True,text=True)
        assert proc.returncode==0,(proc.stdout,proc.stderr)
        assert digest(local/report)==expected[report],report
        runs.append(dict(script=script,exit=0,report=report));print(script+': byte-identical',flush=True)
    audit=json.loads((HERE/commands[1][1]).read_text())
    out=dict(status='pass',id=NAME,archive=archive.relative_to(HERE).as_posix(),sha256=digest(archive),files=len(hashes)+1,
        checksum_entries=len(hashes),byte_identical_generator_and_audit_reports=2,complete_conditional_native_geometry_exclusion=True,
        independent_domain=audit['independent_domain'],corruptions_rejected=9,union_closure_controls=7,
        no_authoritative_exclusion=True,no_new_numerical_extremum=True,runs=runs,
        source_sha256={Path(__file__).name:digest(Path(__file__)),**expected})
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','runs')}),flush=True)

if __name__=='__main__':main()
