"""Isolated byte-identical reproduction of common-E and binary cuts."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent

def main():
    prefix='b1_partial_cover_fourth';archive=ROOT/'certificates'/f'{prefix}.zip'
    destination=(ROOT.parent/'_qa'/f'{prefix}_reproduction').resolve()
    assert destination.is_relative_to(ROOT.parent.resolve());destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as package:
        names=package.namelist();assert len(names)==len(set(names))==20
        for name in names:
            path=PurePosixPath(name)
            assert not path.is_absolute() and '..' not in path.parts and path.parts[0]==prefix
            assert (destination/name).resolve().is_relative_to(destination)
        entries=package.read(prefix+'/CHECKSUMS.txt').decode('utf-8').splitlines();assert len(entries)==19
        for line in entries:
            digest,name=line.split('  ',1);assert hashlib.sha256(package.read(prefix+'/'+name)).hexdigest()==digest
        package.extractall(destination)
    folder=destination/prefix
    files=['b1_partial_cover_inventory.json','b1_partial_cover_fourth_inventory.json',
        'b1_partial_cover_fourth_audit.json','b1_partial_cover_fourth_pair_exclusion_audit.json']
    expected={name:(folder/name).read_bytes() for name in files};runs=[]
    for script in ('enumerate_b1_partial_cover.py','enumerate_b1_partial_cover_fourth.py',
                   'check_b1_partial_cover_fourth.py','check_b1_partial_cover_fourth_pair_exclusions.py'):
        run=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,
            text=True,capture_output=True,check=True,timeout=30)
        runs.append(dict(script=script,exit=run.returncode,outputs=[json.loads(line) for line in run.stdout.splitlines() if line.strip()]))
    for name,value in expected.items():assert (folder/name).read_bytes()==value,name
    assert runs[2]['outputs'][-1]['status']=='pass' and runs[3]['outputs'][-1]['status']=='pass'
    assert runs[3]['outputs'][-1]['remaining_field_pairs']==94
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),
        sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files=20,checksum_entries=19,
        inventories_reproduced_byte_identically=2,audits_reproduced_byte_identically=2,runs=runs,
        source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'b1_partial_cover_fourth_package_reproduction.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',files=20,isolated_inventories_byte_identical=2,isolated_audits_byte_identical=2)))

if __name__=='__main__':main()
