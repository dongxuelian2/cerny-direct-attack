"""Isolated byte-identical reproduction of the fourth-entrance certificate."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent

def main():
    prefix='b1_mixed_c3_fourth';archive=ROOT/'certificates'/f'{prefix}.zip'
    destination=(ROOT.parent/'_qa'/f'{prefix}_reproduction').resolve()
    assert destination.is_relative_to(ROOT.parent.resolve());destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as package:
        names=package.namelist();assert len(names)==len(set(names))==14
        for name in names:
            path=PurePosixPath(name);assert not path.is_absolute() and '..' not in path.parts
            assert path.parts[0]==prefix and (destination/name).resolve().is_relative_to(destination)
        entries=package.read(prefix+'/CHECKSUMS.txt').decode('utf-8').splitlines();assert len(entries)==13
        for line in entries:
            digest,name=line.split('  ',1)
            assert hashlib.sha256(package.read(prefix+'/'+name)).hexdigest()==digest
        package.extractall(destination)
    folder=destination/prefix;audit=prefix+'_audit.json';distributed=(folder/audit).read_bytes()
    inventory=prefix+'_inventory.json';expected=(folder/inventory).read_bytes()
    generator=subprocess.run([sys.executable,str(folder/'enumerate_b1_mixed_c3_fourth.py')],cwd=folder,
        text=True,capture_output=True,check=True,timeout=30)
    assert (folder/inventory).read_bytes()==expected
    run=subprocess.run([sys.executable,str(folder/'check_b1_mixed_c3_fourth.py')],cwd=folder,
        text=True,capture_output=True,check=True,timeout=60)
    assert (folder/audit).read_bytes()==distributed
    lines=[json.loads(v) for v in run.stdout.splitlines() if v.strip()]
    assert [z['row_assignments'] for z in lines[:-1]]==[12744,53568] and lines[-1]['status']=='pass'
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),
        sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files=14,checksum_entries=13,
        isolated_checker_exit=run.returncode,reproduced_audit_byte_identical=True,
        isolated_generator_exit=generator.returncode,reproduced_inventory_byte_identical=True,checker_output=lines,
        source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'b1_mixed_c3_fourth_package_reproduction.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',files=14,isolated_checker_byte_identical=True,isolated_generator_byte_identical=True)))

if __name__=='__main__':main()
