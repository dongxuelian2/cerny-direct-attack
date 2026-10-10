"""Isolated byte-identical reproduction of both current B1/C3 certificates."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent

def main():
    reports=[]
    for prefix,checker,audit in [('b1_mixed_c3_new2','check_b1_mixed_c3_new2.py','b1_mixed_c3_new2_audit.json'),
            ('b1_mixed_c3_singleton','check_b1_mixed_c3_singleton.py','b1_mixed_c3_singleton_audit.json')]:
        archive=ROOT/'certificates'/f'{prefix}.zip'
        destination=(ROOT.parent/'_qa'/f'{prefix}_reproduction').resolve()
        assert destination.is_relative_to(ROOT.parent.resolve());destination.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(archive) as package:
            names=package.namelist();assert len(names)==len(set(names))==15
            for name in names:
                path=PurePosixPath(name);assert not path.is_absolute() and '..' not in path.parts
                assert path.parts[0]==prefix and (destination/name).resolve().is_relative_to(destination)
            entries=package.read(prefix+'/CHECKSUMS.txt').decode('utf-8').splitlines();assert len(entries)==14
            for line in entries:
                digest,name=line.split('  ',1)
                assert hashlib.sha256(package.read(prefix+'/'+name)).hexdigest()==digest
            package.extractall(destination)
        folder=destination/prefix;distributed=(folder/audit).read_bytes()
        run=subprocess.run([sys.executable,str(folder/checker)],cwd=folder,text=True,capture_output=True,check=True,timeout=60)
        assert (folder/audit).read_bytes()==distributed
        reports.append(dict(archive=str(archive.relative_to(ROOT)).replace('\\','/'),
            sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files=15,checksum_entries=14,
            isolated_checker_exit=run.returncode,reproduced_audit_byte_identical=True,checker_output=json.loads(run.stdout)))
    result=dict(status='pass',packages=reports,source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'b1_mixed_c3_packages_reproduction.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',packages=2,files=[v['files'] for v in reports],isolated_byte_identical=True)))

if __name__=='__main__':main()
