"""Deterministic direct-premise package of the unrestricted E6 proof."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent

def main():
    report=json.loads((ROOT/'c4_d125_e6_unrestricted_audit.json').read_text())
    assert report['status']=='pass' and report['unrestricted_E6_paper_excluded']
    names=set(report['source_sha256'])|{'c4_d125_e6_unrestricted_audit.json','C4_D125_E6_CERTIFICATE_README.md'}
    for n,h in report['source_sha256'].items():
        assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
    prefix='c4_d125_e6_unrestricted'
    contents={('README.md' if n=='C4_D125_E6_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
    contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(data).hexdigest()}  {n}\n' for n,data in sorted(contents.items())).encode()
    archive=ROOT/'certificates'/f'{prefix}.zip';assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for n,data in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+n,date_time=(2026,10,10,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    print(json.dumps(dict(files=len(contents),checksum_entries=len(contents)-1,sha256=hashlib.sha256(archive.read_bytes()).hexdigest())))
if __name__=='__main__':main()
