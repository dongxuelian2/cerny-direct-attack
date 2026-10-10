"""Build and independently execute the minimal diagnostic package."""
import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PRIMARY=ROOT.parent

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_manifest(root,manifest):
    for line in manifest.read_text(encoding='utf-8').splitlines():
        expected,name=line.split('  ',1)
        assert digest(root/name)==expected,(name,expected,digest(root/name))

def main():
    # Ensure none of the paper's released files changed during the investigation.
    verify_manifest(PRIMARY,PRIMARY/'SHA256SUMS.txt')
    verify_manifest(PRIMARY/'release',PRIMARY/'release'/'ARCHIVE_SHA256SUMS.txt')
    shutil.copyfile(PRIMARY/'reproducibility'/'LICENSE',ROOT/'LICENSE')
    files=['README.md','FORMULA_AUDIT.md','verify_certificates.py','formula_certificates.json',
           'exhaust_binary.cpp','audit_small.py','small_case_audit.json','extension_audit.json',
           'unresolved_intervals.json','LICENSE']+[f'binary_n{n}.json' for n in range(2,8)]
    files+=['COFINAL_PROOF.md','DEFECT_TWO_PROOF.md','cofinal_family.py','defect_two.py',
            'check_cofinal.py','check_boundary.py','check_defect_two.py','cofinal_audit.json',
            'boundary_audit.json','defect_two_audit.json','defect_one_audit.json']
    (ROOT/'SHA256SUMS.txt').write_text(''.join(digest(ROOT/name)+'  '+name+'\n' for name in sorted(files)),encoding='utf-8')
    files.append('SHA256SUMS.txt')
    archive=ROOT/'reproducibility.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as out:
        for name in sorted(files):
            entry=zipfile.ZipInfo(name,(2026,10,8,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED
            entry.external_attr=0o100644<<16
            out.writestr(entry,(ROOT/name).read_bytes(),compresslevel=9)
    with zipfile.ZipFile(archive) as out:
        assert out.testzip() is None and sorted(out.namelist())==sorted(files)
        for name in files:assert out.read(name)==(ROOT/name).read_bytes()
        check=ROOT/'_archive_check'
        assert not check.exists()
        check.mkdir()
        out.extractall(check)
    verify_manifest(check,check/'SHA256SUMS.txt')
    subprocess.run([sys.executable,'-B',str(check/'verify_certificates.py')],cwd=check,check=True)
    subprocess.run([sys.executable,'-B',str(check/'audit_small.py')],cwd=check,check=True)
    for script,reports in [('check_cofinal.py',['cofinal_audit.json']),('check_boundary.py',['boundary_audit.json']),
                          ('check_defect_two.py',['defect_two_audit.json','defect_one_audit.json'])]:
        subprocess.run([sys.executable,'-B',str(check/script)],cwd=check,check=True)
        for name in reports:assert (check/name).read_bytes()==(ROOT/name).read_bytes(),name
    assert (check/'small_case_audit.json').read_bytes()==(ROOT/'small_case_audit.json').read_bytes()
    # Verified exact scratch directory; delete only the extractor created here.
    assert check.resolve()==ROOT.resolve()/'_archive_check'
    shutil.rmtree(check)
    (ROOT/'ARCHIVE_SHA256SUMS.txt').write_text(digest(archive)+'  reproducibility.zip\n',encoding='utf-8')
    print(f'Packaged {len(files)} files; isolated checks passed; original paper/release hashes unchanged.')

if __name__=='__main__':main()
