"""Reproduce the third-entrance certificate from its standalone archive."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent

def main():
 archive=ROOT/'certificates/third_entrance.zip'
 destination=(ROOT.parent/'_qa/third_entrance_reproduction').resolve()
 assert destination.is_relative_to(ROOT.parent.resolve())
 destination.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(archive) as package:
  names=package.namelist();assert len(names)==len(set(names))==22
  for name in names:
   parts=PurePosixPath(name);assert not parts.is_absolute() and '..' not in parts.parts
   assert parts.parts[0]=='third_entrance'
   assert (destination/name).resolve().is_relative_to(destination)
  entries=package.read('third_entrance/CHECKSUMS.txt').decode('utf-8').splitlines()
  assert len(entries)==21
  for line in entries:
   digest,name=line.split('  ',1)
   assert hashlib.sha256(package.read('third_entrance/'+name)).hexdigest()==digest
  package.extractall(destination)
 folder=destination/'third_entrance'
 inventory=folder/'third_entrance_inventory.json';audit=folder/'third_entrance_audit.json'
 distributed_inventory=inventory.read_bytes();distributed_audit=audit.read_bytes()
 generated=subprocess.run([sys.executable,str(folder/'enumerate_third_entrance.py')],cwd=folder,
  text=True,capture_output=True,check=True,timeout=60)
 assert inventory.read_bytes()==distributed_inventory
 checked=subprocess.run([sys.executable,str(folder/'check_third_entrance.py')],cwd=folder,
  text=True,capture_output=True,check=True,timeout=60)
 assert audit.read_bytes()==distributed_audit
 result=dict(status='pass',archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
  archive_files=len(names),checksum_entries=len(entries),isolated_generator_exit=generated.returncode,
  isolated_checker_exit=checked.returncode,reproduced_inventory_byte_identical=True,
  reproduced_audit_byte_identical=True,generator_output=generated.stdout.strip(),
  checker_output=checked.stdout.strip(),
  source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
 (ROOT/'third_entrance_package_reproduction.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key not in ('source_sha256','generator_output','checker_output')}))

if __name__=='__main__':main()
