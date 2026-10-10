"""Package the directly relevant D15/D25 proofs, row scans and fixed premises."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
def main():
    names={'D15_D25_CERTIFICATE_README.md','b1_d15_d25_composition_audit.json',
           'd15_d25_fourth_rows_audit.json','b1_c14_nonsingleton_fourth_audit.json'}
    for report in ('b1_d15_d25_composition_audit.json','d15_d25_fourth_rows_audit.json',
                   'b1_c14_nonsingleton_fourth_audit.json','b1_c14_nonsingleton_fourth_inventory.json'):
        names.update(json.loads((ROOT/report).read_text())['source_sha256'])
    prefix='b1_d15_d25_complete'
    contents={('README.md' if n=='D15_D25_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
    contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(data).hexdigest()}  {n}\n' for n,data in sorted(contents.items())).encode()
    archive=ROOT/'certificates'/f'{prefix}.zip';assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+name,date_time=(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    print(json.dumps(dict(files=len(contents),checksum_entries=len(contents)-1,sha256=hashlib.sha256(archive.read_bytes()).hexdigest())))
if __name__=='__main__':main()
