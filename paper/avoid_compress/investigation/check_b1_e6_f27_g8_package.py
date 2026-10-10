"""Isolated complete new F27/G8 reductions and complete binary sixth exclusion."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent

def main():
    prefix='b1_e6_f27_g8';archive=ROOT/'certificates'/f'{prefix}.zip'
    destination=(ROOT.parent/'_qa'/f'{prefix}_reproduction').resolve()
    assert destination.is_relative_to(ROOT.parent.resolve());destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as package:
        names=package.namelist();assert len(names)==len(set(names))==23
        for name in names:
            path=PurePosixPath(name)
            assert not path.is_absolute() and '..' not in path.parts and path.parts[0]==prefix
            assert (destination/name).resolve().is_relative_to(destination)
        entries=package.read(prefix+'/CHECKSUMS.txt').decode('utf-8').splitlines();assert len(entries)==22
        for line in entries:
            digest,name=line.split('  ',1)
            assert hashlib.sha256(package.read(prefix+'/'+name)).hexdigest()==digest
        package.extractall(destination)
    folder=destination/prefix
    data=['b1_f27_g8_seventh_inventory.json','b1_f27_g8_rows_inventory.json','b1_f27_g8_rows_fields.txt']
    audits=['b1_f27_g8_seventh_audit.json','b1_f27_g8_rows_audit.json']
    expected={name:(folder/name).read_bytes() for name in data+audits};runs=[]
    for script in ('enumerate_b1_f27_g8_seventh.py','check_b1_f27_g8_seventh.py',
        'enumerate_b1_f27_g8_rows.py','check_b1_f27_g8_rows.py'):
        run=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,
            text=True,capture_output=True,check=True)
        parsed=[json.loads(line) for line in run.stdout.splitlines() if line.strip()]
        if script.startswith('check_'):assert parsed[-1]['status']=='pass'
        runs.append(dict(script=script,exit=run.returncode,outputs=parsed))
    for name,value in expected.items():assert (folder/name).read_bytes()==value,name
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),
        sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files=23,checksum_entries=22,
        data_files_reproduced_byte_identically=3,audits_reproduced_byte_identically=2,
        full_H19_literal_row_pairs=737280,complete_coupled_pairs_per_implementation=6100992,runs=runs,
        source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'b1_e6_f27_g8_package_reproduction.json').write_bytes((json.dumps(result,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(dict(status='pass',files=23,isolated_data_files_byte_identical=3,
        isolated_audits_byte_identical=2,complete_coupled_pairs_per_implementation=6100992)))
if __name__=='__main__':main()
