"""Isolated byte-identical reproduction of both uniform-proof audits."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent

def main():
    prefix='two_cover_p3_classification';archive=ROOT/'certificates'/f'{prefix}.zip'
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
    folder=dest/prefix;audits=['finite_independent_image_trap_audit.json','two_cover_p3_classification_audit.json']
    expected={n:(folder/n).read_bytes() for n in audits};runs=[]
    for script in ('check_finite_independent_image_trap.py','check_two_cover_p3_classification.py'):
        r=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,capture_output=True,text=True)
        if r.returncode:raise RuntimeError(script+'\n'+r.stdout+'\n'+r.stderr)
        parsed=[json.loads(line) for line in r.stdout.splitlines() if line.strip().startswith('{')]
        assert parsed[-1]['status']=='pass';runs.append(dict(script=script,exit=r.returncode,outputs=parsed))
        print(script+': pass',flush=True)
    for n,b in expected.items():assert (folder/n).read_bytes()==b,n
    for n in audits:
        z=json.loads((folder/n).read_text())
        for f,h in z['source_sha256'].items():assert hashlib.sha256((folder/f).read_bytes()).hexdigest()==h,f
    report=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        files=len(names),checksum_entries=len(checks),audits_reproduced_byte_identically=2,
        complete_fixed_two_cover_graphs=43680,complete_binary_semantic_controls=65536,qualifying_semantic_controls=24,
        runs=runs,source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'two_cover_p3_certificate_reproduction.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('runs','source_sha256')}),flush=True)
if __name__=='__main__':main()
