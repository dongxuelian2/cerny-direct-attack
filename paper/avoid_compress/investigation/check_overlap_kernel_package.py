"""Isolated reproduction of the new auxiliary overlap certificate."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent

def main():
 archive=ROOT/'certificates/overlap_three_kernel.zip'
 destination=(ROOT.parent/'_qa/overlap_three_kernel_reproduction').resolve()
 destination.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(archive) as package:
  names=package.namelist();assert len(names)==len(set(names))==47
  for name in names:
   parts=PurePosixPath(name);assert not parts.is_absolute() and '..' not in parts.parts
   assert parts.parts[0]=='overlap_three_kernel'
   assert (destination/name).resolve().is_relative_to(destination)
  table=package.read('overlap_three_kernel/CHECKSUMS.txt').decode('utf-8');entries=table.splitlines()
  assert len(entries)==46
  for line in entries:
   digest,name=line.split('  ',1)
   assert hashlib.sha256(package.read('overlap_three_kernel/'+name)).hexdigest()==digest
  package.extractall(destination)
 folder=destination/'overlap_three_kernel';audit=folder/'overlap_three_kernel_audit.json'
 distributed=audit.read_bytes()
 run=subprocess.run([sys.executable,str(folder/'check_overlap_three_kernel.py')],cwd=folder,
  text=True,capture_output=True,check=True,timeout=60)
 assert audit.read_bytes()==distributed
 result=dict(status='pass',archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
  archive_files=len(names),checksum_entries=len(entries),isolated_checker_exit=run.returncode,
  reproduced_audit_byte_identical=True,checker_output=json.loads(run.stdout),
  source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
 (ROOT/'overlap_kernel_package_reproduction.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key not in ('source_sha256','checker_output')}))

if __name__=='__main__':main()
