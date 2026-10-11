"""Immutable full certificate and byte-exact isolated regeneration."""
from pathlib import Path,PurePosixPath
import ast,hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PREFIX='b2_column_first_pair'
IDS=['b2_in_c3_third5','b2_in_c3_third4','b2_mixed_c3_third4','b2_mixed_c3_third7','b2_in_c6_third6']
AUDITS=['basis_column_reaching_audit.json','basis_column_controls_audit.json']+[n+'_column_audit.json' for n in IDS]+['b2_column_composition_audit.json']
DATA=[n+'_column_inventory.json' for n in IDS]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    archive=ROOT/'certificates'/f'{PREFIX}.zip'
    if '--check-package' not in sys.argv:
        names={'B2_COLUMN_CERTIFICATE_README.md','B2_COLUMN_FIRST_PAIR_EXCLUSION.md',Path(__file__).name,
               'THREE_COVER_ATOM_KERNEL_COMPATIBILITY.md','B1_B2_INVERSE_UNION_EXCLUSION.md',
               'B2_C5_FIRST_PAIR_STAIRCASE_EXCLUSION.md'}
        for n in AUDITS+DATA+['b2_column_scope.json']:
            obj=json.loads((ROOT/n).read_text());names.add(n)
            for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,f;names.add(f)
        names.update(json.loads((ROOT/'b2_column_parent_domains.json').read_text())['historical_source_bindings'])
        # Bind all local Python imports, including reusable helper imports.
        queue=list(names);visited=set()
        while queue:
            name=queue.pop()
            if name in visited or not name.endswith('.py'):continue
            visited.add(name)
            for node in ast.walk(ast.parse((ROOT/name).read_text())):
                modules=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
                for module in modules:
                    candidate=module.split('.')[0]+'.py'
                    if (ROOT/candidate).is_file() and candidate not in names:names.add(candidate);queue.append(candidate)
        contents={('README.md' if n=='B2_COLUMN_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
        contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(b).hexdigest()}  {n}\n' for n,b in sorted(contents.items())).encode()
        assert not archive.exists()
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
            for n,b in sorted(contents.items()):
                info=zipfile.ZipInfo(PREFIX+'/'+n,date_time=(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
        print(json.dumps(dict(status='created',files=len(contents),checksum_entries=len(contents)-1,sha256=sha(archive))),flush=True);return
    dest=(ROOT.parent/'_qa'/f'{PREFIX}_reproduction').resolve()
    assert dest.is_relative_to(ROOT.parent.resolve()) and not (dest/PREFIX).exists();dest.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
        for n in names:
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==PREFIX and (dest/n).resolve().is_relative_to(dest)
        checks=z.read(PREFIX+'/CHECKSUMS.txt').decode().splitlines();assert len(checks)==len(names)-1
        for line in checks:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read(PREFIX+'/'+n)).hexdigest()==h
        z.extractall(dest)
    folder=dest/PREFIX;expected={n:(folder/n).read_bytes() for n in AUDITS+DATA}
    # Only the exact named generated outputs in this verified extraction.
    for n in AUDITS+DATA:
        path=(folder/n).resolve();assert path.parent==folder.resolve();path.unlink()
    commands=[['check_basis_column_reaching.py']]+[['enumerate_b2_column_case.py',n] for n in IDS]+[
              ['check_basis_column_controls.py']]+[['check_b2_column_case.py',n] for n in IDS]+[['check_b2_column_composition.py']]
    runs=[]
    for command in commands:
        proc=subprocess.run([sys.executable,'-B',*command],cwd=folder,capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(str(command)+'\n'+proc.stdout+'\n'+proc.stderr)
        result=json.loads(proc.stdout.splitlines()[-1]);assert result['status'] in ('pass','complete_necessary_exclusion_inventory')
        runs.append(dict(command=command,exit=0));print(' '.join(command)+': pass',flush=True)
    for n,b in expected.items():
        assert (folder/n).read_bytes()==b,n
        for f,h in json.loads(b)['source_sha256'].items():assert sha(folder/f)==h,f
    report=dict(status='pass',archive=archive.relative_to(ROOT).as_posix(),sha256=sha(archive),files=len(names),
                checksum_entries=len(checks),audits_reproduced_byte_identically=len(AUDITS),
                data_files_reproduced_byte_identically=len(DATA),runs=runs,
                source_sha256={Path(__file__).name:sha(Path(__file__))})
    (ROOT/'b2_column_certificate_reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('runs','source_sha256')}),flush=True)

if __name__=='__main__':main()
