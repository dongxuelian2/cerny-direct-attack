"""Minimal deterministic package of the C4/D125 proof and direct controls."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
def main():
    reports=['c4_d125_composition_audit.json','c4_d125_fourth_rows_audit.json','c4_d125_fourth_rows_inventory.json',
        'b1_c4_fourth_audit.json','b1_c4_fourth_inventory.json','closed_merging_block_audit.json',
        'common_block_profiles_audit.json','common_collapsing_block_audit.json']
    names=set(reports)|{'C4_D125_CERTIFICATE_README.md'}
    for n in reports:names.update(json.loads((ROOT/n).read_text())['source_sha256'])
    prefix='c4_d125_complete'
    contents={('README.md' if n=='C4_D125_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
    contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(data).hexdigest()}  {n}\n' for n,data in sorted(contents.items())).encode()
    archive=ROOT/'certificates'/f'{prefix}.zip';assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for n,data in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+n,date_time=(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    print(json.dumps(dict(files=len(contents),checksum_entries=len(contents)-1,sha256=hashlib.sha256(archive.read_bytes()).hexdigest())))
if __name__=='__main__':main()
