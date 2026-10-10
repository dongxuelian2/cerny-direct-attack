"""Isolated full regeneration of the direct fourth/branch/composition package."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
def main():
    prefix='singleton_c_d125_unrestricted_complete';archive=ROOT/'certificates'/f'{prefix}.zip'
    dest=(ROOT.parent/'_qa'/f'{prefix}_reproduction').resolve()
    assert dest.is_relative_to(ROOT.parent.resolve()) and not (dest/prefix).exists()
    dest.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names))
        for n in names:
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix
            assert (dest/n).resolve().is_relative_to(dest)
        checks=z.read(prefix+'/CHECKSUMS.txt').decode().splitlines();assert len(checks)==len(names)-1
        for line in checks:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read(prefix+'/'+n)).hexdigest()==h
        z.extractall(dest)
    folder=dest/prefix
    data=['b1_c4_fourth_inventory.json','c4_d125_e6_individual_controls.json','c4_d125_e6_unrestricted_samples.json',
        'c4_d125_guarded_individual_controls.json','c4_d125_guarded_unrestricted_samples.json']
    audits=['b1_c4_fourth_audit.json','c4_d125_e6_unrestricted_audit.json',
        'c4_d125_guarded_unrestricted_audit.json','singleton_c_d125_unrestricted_composition_audit.json']
    expected={n:(folder/n).read_bytes() for n in data+audits};runs=[]
    scripts=['enumerate_b1_c4_fourth.py','check_b1_c4_fourth.py',
        'enumerate_c4_d125_e6_unrestricted.py','check_c4_d125_e6_unrestricted.py',
        'enumerate_c4_d125_guarded_unrestricted.py','check_c4_d125_guarded_unrestricted.py',
        'check_singleton_c_d125_unrestricted_composition.py']
    for script in scripts:
        r=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,capture_output=True,text=True)
        if r.returncode:raise RuntimeError(script+'\n'+r.stdout+'\n'+r.stderr)
        parsed=[json.loads(line) for line in r.stdout.splitlines() if line.strip().startswith('{')]
        if script.startswith('check_'):assert parsed[-1]['status']=='pass'
        runs.append(dict(script=script,exit=r.returncode,outputs=parsed));print(script+': pass',flush=True)
    for n,b in expected.items():assert (folder/n).read_bytes()==b,n
    for n in audits:
        report=json.loads((folder/n).read_text())
        for f,h in report['source_sha256'].items():assert hashlib.sha256((folder/f).read_bytes()).hexdigest()==h,f
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),
        sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files=len(names),checksum_entries=len(checks),
        data_files_reproduced_byte_identically=5,audits_reproduced_byte_identically=4,
        complete_individual_rows=5904,complete_binary_ordered_controls=207360,seeded_alphabet_controls=54000,
        whole_unrestricted_third_exclusions=2,additional_binary_remaining_pairs_excluded=9,
        runs=runs,source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'singleton_c_d125_certificate_reproduction.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('runs','source_sha256')}),flush=True)
if __name__=='__main__':main()
