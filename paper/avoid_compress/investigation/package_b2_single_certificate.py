"""Freeze and regenerate the complete five-case single-class certificate."""
from pathlib import Path,PurePosixPath
import ast,hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PREFIX='b2_single_first_pair'
IDS=['b2_mixed_c12_third4','b2_in_c1_third6','b2_mixed_c1_third11','b2_mixed_c1_third9','b2_mixed_c1_third10']
AUDITS=['basis_column_reaching_audit.json']+[n+'_single_audit.json' for n in IDS]+['b2_single_composition_audit.json']
DATA=[n+'_single_inventory.json' for n in IDS]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    archive=ROOT/'certificates'/f'{PREFIX}.zip'
    if '--check-package' not in sys.argv:
        names={'B2_SINGLE_CERTIFICATE_README.md','B2_SINGLE_CLASS_FIRST_PAIR_EXCLUSION.md',Path(__file__).name,
               'B2_COLUMN_FIRST_PAIR_EXCLUSION.md','THREE_COVER_ATOM_KERNEL_COMPATIBILITY.md',
               'B1_B2_INVERSE_UNION_EXCLUSION.md','B2_C5_FIRST_PAIR_STAIRCASE_EXCLUSION.md'}
        for n in AUDITS+DATA+['b2_single_scope.json']:
            obj=json.loads((ROOT/n).read_text());names.add(n)
            for f,h in obj['source_sha256'].items():assert digest(ROOT/f)==h,f;names.add(f)
        names.update(json.loads((ROOT/'b2_single_parent_domains.json').read_text())['historical_source_bindings'])
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
        contents={('README.md' if n=='B2_SINGLE_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
        contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(b).hexdigest()}  {n}\n' for n,b in sorted(contents.items())).encode()
        assert not archive.exists()
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
            for n,b in sorted(contents.items()):
                info=zipfile.ZipInfo(PREFIX+'/'+n,date_time=(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
        print(json.dumps(dict(status='created',files=len(contents),checksum_entries=len(contents)-1,sha256=digest(archive))),flush=True);return
    dest=(ROOT.parent/'_qa'/f'{PREFIX}_reproduction').resolve()
    assert dest.is_relative_to(ROOT.parent.resolve()) and not (dest/PREFIX).exists();dest.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
        for n in names:
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==PREFIX and (dest/n).resolve().is_relative_to(dest)
        lines=z.read(PREFIX+'/CHECKSUMS.txt').decode().splitlines();assert len(lines)==len(names)-1
        for line in lines:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read(PREFIX+'/'+n)).hexdigest()==h
        z.extractall(dest)
    folder=dest/PREFIX;expected={n:(folder/n).read_bytes() for n in AUDITS+DATA}
    for n in AUDITS+DATA:
        p=(folder/n).resolve();assert p.parent==folder.resolve();p.unlink()
    commands=[['check_basis_column_reaching.py']]+[['enumerate_b2_single_case.py',n] for n in IDS]+[['check_b2_single_case.py',n] for n in IDS]+[['check_b2_single_composition.py']]
    runs=[]
    for command in commands:
        proc=subprocess.run([sys.executable,'-B',*command],cwd=folder,capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(str(command)+'\n'+proc.stdout+'\n'+proc.stderr)
        result=json.loads(proc.stdout.splitlines()[-1]);assert result['status'] in ('pass','complete_necessary_exclusion_inventory')
        runs.append(dict(command=command,exit=0));print(' '.join(command)+': pass',flush=True)
    for n,b in expected.items():
        assert (folder/n).read_bytes()==b,n
        for f,h in json.loads(b)['source_sha256'].items():assert digest(folder/f)==h,f
    result=dict(status='pass',archive=archive.relative_to(ROOT).as_posix(),sha256=digest(archive),files=len(names),
                checksum_entries=len(lines),audits_reproduced_byte_identically=len(AUDITS),data_files_reproduced_byte_identically=len(DATA),
                runs=runs,source_sha256={Path(__file__).name:digest(Path(__file__))})
    output=ROOT/'b2_single_certificate_reproduction.json';assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('runs','source_sha256')}),flush=True)
if __name__=='__main__':main()
