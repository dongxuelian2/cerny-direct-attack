"""Isolated exact reproduction of the complete auxiliary B3 geometry cut."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent

def main():
    prefix='b3_third_cover';archive=ROOT/'certificates'/f'{prefix}.zip'
    destination=(ROOT.parent/'_qa'/f'{prefix}_reproduction').resolve()
    assert destination.is_relative_to(ROOT.parent.resolve());destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as package:
        names=package.namelist();assert len(names)==len(set(names))==18
        for name in names:
            path=PurePosixPath(name)
            assert not path.is_absolute() and '..' not in path.parts and path.parts[0]==prefix
            assert (destination/name).resolve().is_relative_to(destination)
        entries=package.read(prefix+'/CHECKSUMS.txt').decode('utf-8').splitlines();assert len(entries)==17
        for line in entries:
            digest,name=line.split('  ',1)
            assert hashlib.sha256(package.read(prefix+'/'+name)).hexdigest()==digest
        package.extractall(destination)
    folder=destination/prefix;report='b3_third_cover_audit.json';inventory='b3_third_cover_inventory.json'
    expected_report=(folder/report).read_bytes();expected_inventory=(folder/inventory).read_bytes()
    runs=[]
    for script in ('enumerate_b3_third_cover.py','check_b3_third_cover.py'):
        run=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,
            text=True,capture_output=True,check=True,timeout=30)
        runs.append(dict(script=script,exit=run.returncode,output=json.loads(run.stdout)))
    assert (folder/report).read_bytes()==expected_report
    assert (folder/inventory).read_bytes()==expected_inventory
    assert runs[1]['output']['status']=='pass' and runs[1]['output']['complete_labelled_D_choices']==827
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),
        sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files=18,checksum_entries=17,
        reproduced_audit_byte_identical=True,reproduced_inventory_byte_identical=True,runs=runs,
        source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'b3_third_cover_package_reproduction.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',files=18,isolated_checker_byte_identical=True,isolated_generator_byte_identical=True)))

if __name__=='__main__':main()
