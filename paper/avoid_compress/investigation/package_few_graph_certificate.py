"""Scope-specific immutable packaging and complete isolated regeneration."""
from pathlib import Path,PurePosixPath
import argparse,ast,hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scope',required=True);ap.add_argument('--check-package',action='store_true');args=ap.parse_args()
    scope=read(args.scope);tag=scope['output_tag'];prefix=tag+'_first_pair';ids=scope['selected']
    assert tag.replace('_','').isalnum() and Path(args.scope).name==args.scope
    audits=['basis_column_reaching_audit.json']+[n+'_'+tag+'_audit.json' for n in ids]+[tag+'_controls_audit.json',tag+'_composition_audit.json']
    data=[n+'_'+tag+'_inventory.json' for n in ids];archive=ROOT/'certificates'/(prefix+'.zip')
    if not args.check_package:
        names={Path(__file__).name,'FEW_GRAPH_CERTIFICATE_README.md','FEW_GRAPH_FIRST_PAIR_CERTIFICATES.md',
               'B2_COLUMN_FIRST_PAIR_EXCLUSION.md','B1_B2_INVERSE_UNION_EXCLUSION.md',
               'B2_C5_FIRST_PAIR_STAIRCASE_EXCLUSION.md','THREE_COVER_ATOM_KERNEL_COMPATIBILITY.md'}
        for n in audits+data+[args.scope]:
            obj=read(n);names.add(n)
            for f,h in obj['source_sha256'].items():assert digest(ROOT/f)==h,f;names.add(f)
        names.update(read(scope['parent_domains'])['historical_source_bindings'])
        queue=list(names);visited=set()
        while queue:
            n=queue.pop()
            if n in visited or not n.endswith('.py'):continue
            visited.add(n)
            for node in ast.walk(ast.parse((ROOT/n).read_text())):
                modules=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
                for module in modules:
                    f=module.split('.')[0]+'.py'
                    if (ROOT/f).is_file() and f not in names:names.add(f);queue.append(f)
        contents={('README.md' if n=='FEW_GRAPH_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
        contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(b).hexdigest()}  {n}\n' for n,b in sorted(contents.items())).encode()
        assert not archive.exists()
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
            for n,b in sorted(contents.items()):
                info=zipfile.ZipInfo(prefix+'/'+n,date_time=(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
        print(json.dumps(dict(status='created',files=len(contents),checksum_entries=len(contents)-1,sha256=digest(archive))),flush=True);return
    dest=(ROOT.parent/'_qa'/(prefix+'_reproduction')).resolve()
    assert dest.is_relative_to(ROOT.parent.resolve()) and not (dest/prefix).exists();dest.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
        for n in names:
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix and (dest/n).resolve().is_relative_to(dest)
        lines=z.read(prefix+'/CHECKSUMS.txt').decode().splitlines();assert len(lines)==len(names)-1
        for line in lines:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read(prefix+'/'+n)).hexdigest()==h
        z.extractall(dest)
    folder=dest/prefix;expected={n:(folder/n).read_bytes() for n in audits+data}
    for n in audits+data:
        p=(folder/n).resolve();assert p.parent==folder.resolve();p.unlink()
    commands=[['check_basis_column_reaching.py']]+[['enumerate_few_graph_case.py',n,'--scope',args.scope] for n in ids]+[
        ['check_few_graph_case.py',n,'--scope',args.scope] for n in ids]+[
        ['check_few_graph_controls.py','--scope',args.scope],['check_few_graph_composition.py','--scope',args.scope]]
    runs=[]
    for command in commands:
        proc=subprocess.run([sys.executable,'-B',*command],cwd=folder,capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(str(command)+'\n'+proc.stdout+'\n'+proc.stderr)
        obj=json.loads(proc.stdout.splitlines()[-1]);assert obj['status'] in ('pass','complete_necessary_exclusion_inventory')
        runs.append(dict(command=command,exit=0));print(' '.join(command)+': pass',flush=True)
    for n,b in expected.items():
        assert (folder/n).read_bytes()==b,n
        for f,h in json.loads(b)['source_sha256'].items():assert digest(folder/f)==h,f
    out=dict(status='pass',archive=archive.relative_to(ROOT).as_posix(),sha256=digest(archive),files=len(names),checksum_entries=len(lines),
             audits_reproduced_byte_identically=len(audits),data_files_reproduced_byte_identically=len(data),runs=runs,
             source_sha256={Path(__file__).name:digest(Path(__file__)),args.scope:digest(ROOT/args.scope)})
    output=ROOT/(tag+'_certificate_reproduction.json');assert not output.exists()
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('runs','source_sha256')}),flush=True)
if __name__=='__main__':main()
