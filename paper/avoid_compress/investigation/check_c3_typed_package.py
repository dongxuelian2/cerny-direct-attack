"""Isolated reproduction of the typed c3 certificate."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent

def main():
 archive=ROOT/'certificates/c3_typed_third.zip'
 destination=(ROOT.parent/'_qa/c3_typed_third_reproduction').resolve()
 assert destination.is_relative_to(ROOT.parent.resolve())
 destination.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(archive) as package:
  names=package.namelist();assert len(names)==len(set(names))==14
  for name in names:
   parts=PurePosixPath(name);assert not parts.is_absolute() and '..' not in parts.parts
   assert parts.parts[0]=='c3_typed_third'
   assert (destination/name).resolve().is_relative_to(destination)
  entries=package.read('c3_typed_third/CHECKSUMS.txt').decode('utf-8').splitlines()
  assert len(entries)==13
  for line in entries:
   digest,name=line.split('  ',1)
   assert hashlib.sha256(package.read('c3_typed_third/'+name)).hexdigest()==digest
  package.extractall(destination)
 folder=destination/'c3_typed_third';audit=folder/'c3_typed_third_audit.json'
 distributed=audit.read_bytes()
 run=subprocess.run([sys.executable,str(folder/'check_c3_typed_third.py')],cwd=folder,
  text=True,capture_output=True,check=True,timeout=60)
 assert audit.read_bytes()==distributed
 result=dict(status='pass',archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
  archive_files=len(names),checksum_entries=len(entries),isolated_checker_exit=run.returncode,
  reproduced_audit_byte_identical=True,checker_output=json.loads(run.stdout),
  source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
 (ROOT/'c3_typed_package_reproduction.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key not in ('source_sha256','checker_output')}))

if __name__=='__main__':main()
