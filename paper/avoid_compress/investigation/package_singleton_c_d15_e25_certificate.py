"""Deterministic direct-premise package for two E25 fourth cuts."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
def main():
    reports=['saturated_two_guard_trap_audit.json','singleton_c_d15_e25_transport_audit.json','c4_d15_e25_unrestricted_audit.json','b1_c4_fourth_audit.json']
    names=set(reports)|{'SINGLETON_C_D15_E25_CERTIFICATE_README.md'}
    for n in reports:
        z=json.loads((ROOT/n).read_text());assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
        names.update(z['source_sha256'])
    prefix='singleton_c_d15_e25_unrestricted'
    contents={('README.md' if n=='SINGLETON_C_D15_E25_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
    contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(data).hexdigest()}  {n}\n' for n,data in sorted(contents.items())).encode()
    archive=ROOT/'certificates'/f'{prefix}.zip';assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for n,data in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+n,date_time=(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    print(json.dumps(dict(files=len(contents),checksum_entries=len(contents)-1,sha256=hashlib.sha256(archive.read_bytes()).hexdigest())))
if __name__=='__main__':main()
