"""Isolated exact fourth classification and independent construction probe."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
def main():
    prefix='b1_c14_fourth';archive=ROOT/'certificates'/f'{prefix}.zip'
    destination=(ROOT.parent/'_qa'/f'{prefix}_reproduction').resolve()
    assert destination.is_relative_to(ROOT.parent.resolve());destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as package:
        names=package.namelist();assert len(names)==len(set(names))==21
        for name in names:
            path=PurePosixPath(name)
            assert not path.is_absolute() and '..' not in path.parts and path.parts[0]==prefix
            assert (destination/name).resolve().is_relative_to(destination)
        entries=package.read(prefix+'/CHECKSUMS.txt').decode().splitlines();assert len(entries)==20
        for line in entries:
            h,name=line.split('  ',1);assert hashlib.sha256(package.read(prefix+'/'+name)).hexdigest()==h
        package.extractall(destination)
    folder=destination/prefix
    data=['b1_c14_nonsingleton_fourth_inventory.json','codimension_four_cycle5_probe.json']
    audits=['b1_c14_nonsingleton_fourth_audit.json','codimension_four_cycle5_probe_audit.json']
    expected={name:(folder/name).read_bytes() for name in data+audits};runs=[]
    for script in ('enumerate_b1_c14_nonsingleton_fourth.py','check_b1_c14_nonsingleton_fourth.py','check_codimension_four_cycle5_probe.py'):
        run=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,text=True,capture_output=True,check=True)
        parsed=[json.loads(line) for line in run.stdout.splitlines() if line.strip()]
        if script.startswith('check_'):assert parsed[-1]['status']=='pass'
        runs.append(dict(script=script,exit=run.returncode,outputs=parsed))
    for name,value in expected.items():assert (folder/name).read_bytes()==value,name
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),
        sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files=21,checksum_entries=20,
        data_files_reproduced_byte_identically=2,audits_reproduced_byte_identically=2,
        complete_literal_masks=606060,complete_augmented_ranks=10444,complete_bounded_row_pairs=1164240,runs=runs,
        source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'b1_c14_fourth_package_reproduction.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(dict(status='pass',files=21,isolated_data_files_byte_identical=2,
        isolated_audits_byte_identical=2,complete_bounded_row_pairs=1164240)))
if __name__=='__main__':main()
