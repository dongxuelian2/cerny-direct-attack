"""Streaming immutable package and isolated replay of the flag quotient.

CLI: GEOMETRY full, or GEOMETRY selected INDEX [INDEX ...].
Selected prefixes never become a whole-geometry certificate.
"""
import ast
from hashlib import sha256
import json,mmap,shutil,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent;PAPER=HERE.parent;ROOT=PAPER/'investigation'

def digest(p):
    h=sha256()
    with p.open('rb') as f:
        while b:=f.read(8<<20):h.update(b)
    return h.hexdigest()

def stream_digest(f):
    h=sha256()
    while b:=f.read(8<<20):h.update(b)
    return h.hexdigest()

def metadata(p):
    with p.open('rb') as f:
        with mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as m:
            pos=m.find(b'"prefixes":[')
            if pos<0:pos=m.find(b'"prefixes": [')
            if pos<0:return json.loads(m[:])
            head=json.loads(m[:pos].rstrip().rstrip(b',')+b'}')
            start=m.rfind(b'"candidate":')
            if start<0:return json.loads(m[:])
            assert start>pos
            return dict(head,**json.loads(b'{'+m[start:]))

def main():
    name,mode=sys.argv[1:3];assert mode in ('full','selected')
    indices=list(map(int,sys.argv[3:]))
    if mode=='selected':assert indices and indices==sorted(set(indices)) and min(indices)>=0
    else:assert not indices
    tag='_'.join(map(str,indices)) if mode=='selected' else 'full'
    prefix='quotient_'+tag+'_20261012_v2'
    final=name+('_quotient_flags_selected_'+tag+'_probe.json' if mode=='selected' else '_product_supplier_from0_v8_probe.json')
    output=HERE/(name+'_quotient_'+tag+'_reproduction_20261012_v2.json');assert not output.exists()
    commands=[
        ('audit_supplier_image_controls.py',[],'supplier_image_controls_audit_20261011.json'),
        ('audit_supplier_image_horizon.py',[],'supplier_image_horizon_audit_20261011.json'),
        ('audit_supplier_products.py',[],'supplier_products_audit_20261012.json'),
        ('audit_supplier_product_extensions.py',[],'supplier_product_extensions_audit_20261012.json'),
        ('audit_supplier_triples_v2.py',[],'supplier_triples_v2_audit_20261012.json'),
        ('audit_supplier_triples_v3.py',[],'supplier_triples_v3_audit_20261012.json'),
        ('audit_obligatory_supplier_split_20261012.py',[],'obligatory_supplier_split_audit_20261012.json'),
        ('audit_obligatory_supplier_split_extended_20261012.py',[],'obligatory_supplier_split_extended_audit_20261012.json'),
        ('compile_native_graph_quotient.py',[name],name+'_graph_quotient_scope.json'),
        ('audit_flag_stabilizer_quotient_20261012.py',[],'flag_stabilizer_quotient_audit_20261012.json'),
        ('check_native_graph_quotient.py',[name],name+'_graph_quotient_transport_audit.json'),
        ('check_native_graph_protection.py',[name],name+'_graph_transport_protection_audit.json'),
        (('probe_quotient_flags_selected_20261012.py' if mode=='selected' else 'probe_quotient_flags_range_v8.py'),
         [name,*map(str,indices)] if mode=='selected' else [name,'0'],final)]
    assert len(commands)==13
    files={Path(__file__).resolve()};expected={}
    for script,args,report in commands:
        files.add(HERE/script);p=HERE/report;d=metadata(p)
        assert d['status'] in ('pass','complete_transport_scope_only','complete_selected_quotient_flags_QA_only','complete_independently_checked_QA_only')
        files.add(p);expected[report]=digest(p)
        for key,base in [('source_sha256',HERE),('root_source_sha256',ROOT)]:
            for f,h in d.get(key,{}).items():
                q=(base/f).resolve();assert q.is_relative_to(PAPER.resolve()) and digest(q)==h,(report,f)
                files.add(q)
    full=metadata(HERE/final)
    assert full['id']==name and full['parameter']==[13,9,1] and full['target_ac']==12 and full['candidate'] is None
    if mode=='selected':
        assert full['complete_selected'] is True and full['complete_scope'] is False and full['selected_prefixes']==indices
        assert full['counts']['prefixes']==len(indices)
    else:
        assert full['complete_scope'] is True and full['complete_range'] is True and full['range_start']==0
        assert full['counts']['prefixes']==full['total_native_prefixes']
    parent=json.loads((HERE/(name+'_inverse_probe.json')).read_text())
    for f,h in parent['source_sha256'].items():
        f='b1_b2_inverse_union_baseline_state.json' if f=='active_research.json' else f
        p=ROOT/f;assert digest(p)==h;files.add(p)
    for f in ['B2_COLUMN_FIRST_PAIR_EXCLUSION.md','B1_B2_INVERSE_UNION_EXCLUSION.md',
              'THREE_COVER_ATOM_KERNEL_COMPATIBILITY.md','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md']:
        files.add(ROOT/f)
    queue=list(files);visited=set()
    while queue:
        p=queue.pop()
        if p.suffix!='.py' or p in visited:continue
        visited.add(p)
        for node in ast.walk(ast.parse(p.read_text())):
            modules=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
            for module in modules:
                f=module.split('.')[0]+'.py'
                for base in (p.parent,HERE,ROOT):
                    q=base/f
                    if q.is_file():
                        if q not in files:files.add(q);queue.append(q)
                        break
    content={p.relative_to(PAPER).as_posix():p for p in sorted(files)}
    extra={'README.md':(
        '# Independently checked flag-stabilizer quotient\n\n'
        'Python >=3.10; standard library only. Geometry: '+name+'\n'
        'Scope: '+('selected prefixes '+tag if mode=='selected' else 'all native first-pair prefixes')+'.\n'
        'Every quotient conjugates the whole alphabet by one common state permutation.\n'
        'No independent relabelling of letters and no depth12 safety premise is used.\n'
        'The checker reconstructs each literal-row transport and every omitted child.\n'
        'From _qa move aside exactly the following thirteen stored reports:\n'+
        ''.join(report+'\n' for _,_,report in commands)+'\nThen run in order:\n'+
        ''.join('python -B '+s+' '+' '.join(a)+'\n' for s,a,_ in commands)+'\n'
        'All thirteen reports must match their stored SHA256, including the complete flag tree.\n'
        'The observed replay is on Windows; other platforms may need newline normalization.\n'
        'Selected-prefix success is not a whole-geometry exclusion. Full success is a\n'
        'conditional geometry certificate and still requires a separate adoption audit.\n'
        'Neither mode establishes a new numerical extremum, alphabet separation or a\n'
        'complete answer to Open Problem4. The accepted publication is unchanged.\n').encode()}
    hashes={n:digest(p) for n,p in content.items()}
    hashes.update({n:sha256(b).hexdigest() for n,b in extra.items()})
    extra['CHECKSUMS.txt']=''.join(h+'  '+n+'\n' for n,h in sorted(hashes.items())).encode()
    archive=HERE/'certificates'/(name+'_'+prefix+'.zip');assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,allowZip64=True) as z:
        for n in sorted(set(content)|set(extra)):
            info=zipfile.ZipInfo(prefix+'/'+n,date_time=(2026,10,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            if n in extra:z.writestr(info,extra[n])
            else:
                with content[n].open('rb') as src,z.open(info,'w',force_zip64=True) as dest:shutil.copyfileobj(src,dest,8<<20)
    dest=(HERE/(prefix+'_reproduction')).resolve();assert dest.is_relative_to(HERE.resolve()) and not dest.exists();dest.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(hashes)+1
        for n in z.namelist():
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix
            assert (dest/n).resolve().is_relative_to(dest)
        for n,h in hashes.items():
            with z.open(prefix+'/'+n) as f:assert stream_digest(f)==h,n
        z.extractall(dest)
    local=dest/prefix/'_qa'
    for report,h in expected.items():
        p=(local/report).resolve();assert p.parent==local.resolve() and digest(p)==h;p.unlink()
    runs=[]
    for script,args,report in commands:
        proc=subprocess.run([sys.executable,'-B',script,*args],cwd=local,capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(script+'\n'+proc.stdout+'\n'+proc.stderr)
        assert digest(local/report)==expected[report],report
        runs.append(dict(script=script,arguments=args,exit=0,report=report))
        print(script+' '+' '.join(args)+': byte-identical',flush=True)
    out=dict(status='pass',id=name,archive=archive.relative_to(HERE).as_posix(),sha256=digest(archive),
        files=len(hashes)+1,checksum_entries=len(hashes),byte_identical_scope_and_audit_reports=13,
        complete_selected_prefix_certificate=mode=='selected',complete_conditional_flag_tree_certificate=mode=='full',
        selected_prefixes=indices,no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        scope='Isolated replay only; selection never excludes the full native geometry.',runs=runs,
        source_sha256={Path(__file__).name:digest(Path(__file__)),**expected})
    output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','runs')}),flush=True)
if __name__=='__main__':main()
