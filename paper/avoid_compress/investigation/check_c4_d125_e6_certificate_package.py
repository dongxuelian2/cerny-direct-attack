"""Isolated regeneration of the unrestricted E6 direct proof controls."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent

def main():
    prefix='c4_d125_e6_unrestricted';archive=ROOT/'certificates'/f'{prefix}.zip'
    dest=(ROOT.parent/'_qa'/f'{prefix}_reproduction').resolve()
    assert dest.is_relative_to(ROOT.parent.resolve()) and not (dest/prefix).exists()
    dest.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names))
        for n in names:
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix
            assert (dest/n).resolve().is_relative_to(dest)
        checks=z.read(prefix+'/CHECKSUMS.txt').decode().splitlines();assert len(checks)==len(names)-1
        for line in checks:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read(prefix+'/'+n)).hexdigest()==h
        z.extractall(dest)
    folder=dest/prefix
    data=['c4_d125_e6_individual_controls.json','c4_d125_e6_unrestricted_samples.json']
    audit='c4_d125_e6_unrestricted_audit.json'
    expected={n:(folder/n).read_bytes() for n in data+[audit]};runs=[]
    for script in ['enumerate_c4_d125_e6_unrestricted.py','check_c4_d125_e6_unrestricted.py']:
        r=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,capture_output=True,text=True)
        if r.returncode:raise RuntimeError(script+'\n'+r.stdout+'\n'+r.stderr)
        parsed=[json.loads(line) for line in r.stdout.splitlines() if line.strip().startswith('{')]
        if script.startswith('check_'):assert parsed[-1]['status']=='pass'
        runs.append(dict(script=script,exit=r.returncode,outputs=parsed));print(script+': pass',flush=True)
    for n,b in expected.items():assert (folder/n).read_bytes()==b,n
    report=json.loads((folder/audit).read_text())
    for n,h in report['source_sha256'].items():assert hashlib.sha256((folder/n).read_bytes()).hexdigest()==h,n
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),
        sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files=len(names),checksum_entries=len(checks),
        data_files_reproduced_byte_identically=2,audits_reproduced_byte_identically=1,
        complete_individual_rows=1944,seeded_alphabets=18000,unrestricted_E6_paper_excluded=True,
        runs=runs,source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'c4_d125_e6_certificate_reproduction.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('runs','source_sha256')}),flush=True)
if __name__=='__main__':main()
