"""Package and isolate direct dependencies of the complete atom/kernel audit."""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,subprocess,sys
ROOT=Path(__file__).resolve().parent;PREFIX='three_cover_atom'
NEW=['general_atom_kernel_controls_audit.json','three_cover_atom_kernel_audit.json']
DATA=['three_cover_atom_kernel_inventory.json','three_cover_atom_frontier_input.json']
OLD=['small_first_third_audit.json','b3_third_cover_audit.json','mandatory_core_isolation_audit.json']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    archive=ROOT/'certificates'/f'{PREFIX}.zip'
    if '--check-package' not in sys.argv:
        names={'THREE_COVER_ATOM_CERTIFICATE_README.md'}
        for n in NEW+DATA+OLD:
            z=json.loads((ROOT/n).read_text());names.add(n)
            if n in NEW+OLD:assert z['status']=='pass'
            for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f;names.add(f)
        contents={('README.md' if n=='THREE_COVER_ATOM_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
        contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(b).hexdigest()}  {n}\n' for n,b in sorted(contents.items())).encode()
        assert not archive.exists()
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
            for n,b in sorted(contents.items()):
                info=zipfile.ZipInfo(PREFIX+'/'+n,date_time=(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
        print(json.dumps(dict(files=len(contents),checksum_entries=len(contents)-1,sha256=sha(archive))),flush=True);return
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
    folder=dest/PREFIX;expected={n:(folder/n).read_bytes() for n in NEW+[DATA[0]]};runs=[]
    for script in ['check_general_atom_kernel_controls.py','enumerate_three_cover_atom_kernels.py','check_three_cover_atom_kernels.py']:
        r=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,capture_output=True,text=True)
        if r.returncode:raise RuntimeError(script+'\n'+r.stdout+'\n'+r.stderr)
        parsed=json.loads(r.stdout.splitlines()[-1]);assert parsed['status'] in ('pass','generated')
        runs.append(dict(script=script,exit=0,output=parsed));print(script+': pass',flush=True)
    for n,b in expected.items():
        assert (folder/n).read_bytes()==b,n
        for f,h in json.loads(b)['source_sha256'].items():assert sha(folder/f)==h,f
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),sha256=sha(archive),files=len(names),
        checksum_entries=len(checks),audits_reproduced_byte_identically=2,data_files_reproduced_byte_identically=1,runs=runs,
        source_sha256={Path(__file__).name:sha(Path(__file__))})
    (ROOT/'three_cover_atom_certificate_reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('runs','source_sha256')}),flush=True)
if __name__=='__main__':main()
