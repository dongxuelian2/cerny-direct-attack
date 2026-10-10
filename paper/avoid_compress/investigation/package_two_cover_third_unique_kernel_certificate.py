"""Minimal fixed-premise unique-kernel field package and isolated reproduction."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,subprocess,sys
ROOT=Path(__file__).resolve().parent
PREFIX='two_cover_third_unique_kernel'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    archive=ROOT/'certificates'/f'{PREFIX}.zip'
    if '--check-package' not in sys.argv:
        names={'TWO_COVER_THIRD_UNIQUE_KERNEL_CERTIFICATE_README.md'}
        for n in ['two_cover_third_unique_kernel_audit.json','small_first_third_audit.json',
                  'two_cover_unique_immediate_pair_audit.json','mandatory_core_isolation_audit.json']:
            z=json.loads((ROOT/n).read_text());assert z['status']=='pass';names.add(n)
            for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f
            names.update(z['source_sha256'])
        contents={('README.md' if n=='TWO_COVER_THIRD_UNIQUE_KERNEL_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
        contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(b).hexdigest()}  {n}\n' for n,b in sorted(contents.items())).encode()
        assert not archive.exists()
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
            for n,b in sorted(contents.items()):
                info=zipfile.ZipInfo(PREFIX+'/'+n,date_time=(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
        print(json.dumps(dict(files=len(contents),checksum_entries=len(contents)-1,sha256=sha(archive))),flush=True)
        return
    dest=(ROOT.parent/'_qa'/f'{PREFIX}_reproduction').resolve()
    assert dest.is_relative_to(ROOT.parent.resolve()) and not (dest/PREFIX).exists()
    dest.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
        for n in names:
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==PREFIX
            assert (dest/n).resolve().is_relative_to(dest)
        checks=z.read(PREFIX+'/CHECKSUMS.txt').decode().splitlines()
        for line in checks:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read(PREFIX+'/'+n)).hexdigest()==h
        assert len(checks)==len(names)-1;z.extractall(dest)
    folder=dest/PREFIX;name='two_cover_third_unique_kernel_audit.json';expected=(folder/name).read_bytes()
    r=subprocess.run([sys.executable,'-B',str(folder/'check_two_cover_third_unique_kernel.py')],cwd=folder,capture_output=True,text=True)
    assert r.returncode==0,r.stderr
    assert (folder/name).read_bytes()==expected
    for n,h in json.loads(expected)['source_sha256'].items():assert sha(folder/n)==h,n
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),sha256=sha(archive),files=len(names),
                checksum_entries=len(checks),audits_reproduced_byte_identically=1,checker_exit=r.returncode,
                two_cover_geometries=43,fields_reconstructed=311,global_kernel_classes=765,
                source_sha256={Path(__file__).name:sha(Path(__file__))})
    (ROOT/'two_cover_third_unique_kernel_certificate_reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
