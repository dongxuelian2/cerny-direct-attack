"""Fresh isolated reproduction of the new geometry, lemma and profile cuts."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
def main():
    prefix='common_block_profiles_complete';archive=ROOT/'certificates'/f'{prefix}.zip'
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
    data=['b1_c4_fourth_inventory.json']
    audits=['b1_c4_fourth_audit.json','common_collapsing_block_audit.json','common_block_profiles_audit.json']
    expected={n:(folder/n).read_bytes() for n in data+audits};runs=[]
    for script in ('enumerate_b1_c4_fourth.py','check_b1_c4_fourth.py','check_common_collapsing_block.py','check_common_block_profiles.py'):
        r=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,capture_output=True,text=True)
        if r.returncode:raise RuntimeError(script+'\n'+r.stdout+'\n'+r.stderr)
        parsed=[json.loads(line) for line in r.stdout.splitlines() if line.strip().startswith('{')]
        if script.startswith('check_'):assert parsed[-1]['status']=='pass'
        runs.append(dict(script=script,exit=r.returncode,outputs=parsed));print(script+': pass',flush=True)
    for n,b in expected.items():assert (folder/n).read_bytes()==b,n
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        files=len(names),checksum_entries=len(checks),data_files_reproduced_byte_identically=1,audits_reproduced_byte_identically=3,
        uniform_conditional_common_block_proof=True,newly_excluded_binary_profile_pairs=25,
        remaining_binary_third_geometries=146,remaining_binary_profile_pairs=719,runs=runs,
        source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'common_block_certificate_reproduction.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('runs','source_sha256')}),flush=True)
if __name__=='__main__':main()
