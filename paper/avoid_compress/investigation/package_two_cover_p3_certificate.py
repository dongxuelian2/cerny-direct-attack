"""Deterministic minimal uniform two-cover classification package."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent

def main():
    reports=['finite_independent_image_trap_audit.json','two_cover_p3_classification_audit.json']
    names=set(reports)|{'TWO_COVER_P3_CERTIFICATE_README.md'}
    for n in reports:
        z=json.loads((ROOT/n).read_text());assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
        names.update(z['source_sha256'])
    prefix='two_cover_p3_classification'
    contents={('README.md' if n=='TWO_COVER_P3_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
    contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(b).hexdigest()}  {n}\n' for n,b in sorted(contents.items())).encode()
    archive=ROOT/'certificates'/f'{prefix}.zip';assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+n,date_time=(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    print(json.dumps(dict(files=len(contents),checksum_entries=len(contents)-1,sha256=hashlib.sha256(archive.read_bytes()).hexdigest())))
if __name__=='__main__':main()
