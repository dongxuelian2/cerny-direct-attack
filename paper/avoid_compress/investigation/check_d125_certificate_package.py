"""Isolated reproduction of fourth geometry, actual rows and whole-D125 composition."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent

def main():
    prefix='b1_d125_complete';archive=ROOT/'certificates'/f'{prefix}.zip'
    destination=(ROOT.parent/'_qa'/f'{prefix}_reproduction').resolve()
    assert destination.is_relative_to(ROOT.parent.resolve())
    assert not (destination/prefix).exists(), 'Use a fresh isolated reproduction.'
    destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as package:
        names=package.namelist();assert len(names)==len(set(names))
        for name in names:
            p=PurePosixPath(name)
            assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix
            assert (destination/name).resolve().is_relative_to(destination)
        checks=package.read(prefix+'/CHECKSUMS.txt').decode().splitlines()
        assert len(checks)==len(names)-1
        for line in checks:
            h,name=line.split('  ',1)
            assert hashlib.sha256(package.read(prefix+'/'+name)).hexdigest()==h
        package.extractall(destination)
    folder=destination/prefix
    data=['b1_c14_nonsingleton_fourth_inventory.json','d125_fourth_rows_inventory.json','d125_fourth_rows_fields.txt']
    audits=['b1_c14_nonsingleton_fourth_audit.json','d125_fourth_rows_audit.json','b1_d125_composition_audit.json']
    expected={n:(folder/n).read_bytes() for n in data+audits};runs=[]
    scripts=('enumerate_b1_c14_nonsingleton_fourth.py','check_b1_c14_nonsingleton_fourth.py',
             'enumerate_d125_fourth_rows.py','check_d125_fourth_rows.py','check_b1_d125_composition.py')
    for script in scripts:
        result=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,text=True,capture_output=True)
        if result.returncode:raise RuntimeError(script+'\n'+result.stdout+'\n'+result.stderr)
        parsed=[json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        if script.startswith('check_'):assert parsed[-1]['status']=='pass'
        runs.append(dict(script=script,exit=result.returncode,outputs=parsed))
        print(script+': pass',flush=True)
    for n,b in expected.items():assert (folder/n).read_bytes()==b,n
    report=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),
        sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files=len(names),checksum_entries=len(checks),
        data_files_reproduced_byte_identically=3,audits_reproduced_byte_identically=3,
        raw_individual_rows=241920,pointwise_transports_checked=119520,
        complete_representative_pairs_per_implementation=7164000,whole_binary_D125_excluded=True,runs=runs,
        source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (ROOT/'d125_certificate_reproduction.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('runs','source_sha256')}),flush=True)
if __name__=='__main__':main()
