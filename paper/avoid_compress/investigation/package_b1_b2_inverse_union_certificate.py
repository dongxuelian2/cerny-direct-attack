"""Immutable fixed-parameter archive and isolated byte-identical regeneration."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,subprocess,sys
ROOT=Path(__file__).resolve().parent;PREFIX='b1_b2_inverse_union'
AUDITS=['b1_b2_inverse_union_controls_audit.json','b1_b2_inverse_union_audit.json']
DATA=['b1_b2_inverse_union_inventory.json']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    archive=ROOT/'certificates'/f'{PREFIX}.zip'
    if '--check-package' not in sys.argv:
        names={'B1_B2_INVERSE_UNION_CERTIFICATE_README.md'}
        for n in AUDITS+DATA+['b1_b2_inverse_union_scope.json']:
            obj=json.loads((ROOT/n).read_text());names.add(n)
            for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,f;names.add(f)
        contents={('README.md' if n=='B1_B2_INVERSE_UNION_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
        contents['CHECKSUMS.txt']=''.join(f'{hashlib.sha256(b).hexdigest()}  {n}\n' for n,b in sorted(contents.items())).encode()
        assert not archive.exists()
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
            for n,b in sorted(contents.items()):
                info=zipfile.ZipInfo(PREFIX+'/'+n,date_time=(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
        print(json.dumps(dict(status='created',files=len(contents),checksum_entries=len(contents)-1,sha256=sha(archive))),flush=True);return
    dest=(ROOT.parent/'_qa'/f'{PREFIX}_reproduction').resolve()
    assert dest.is_relative_to(ROOT.parent.resolve()) and not (dest/PREFIX).exists();dest.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
        for n in names:
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==PREFIX and (dest/n).resolve().is_relative_to(dest)
        checks=z.read(PREFIX+'/CHECKSUMS.txt').decode().splitlines();assert len(checks)==len(names)-1
        for line in checks:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read(PREFIX+'/'+n)).hexdigest()==h
        z.extractall(dest)
    folder=dest/PREFIX;expected={n:(folder/n).read_bytes() for n in AUDITS+DATA};runs=[]
    for script in ['enumerate_b1_b2_inverse_union.py','check_b1_b2_inverse_union_controls.py','check_b1_b2_inverse_union.py']:
        proc=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(script+'\n'+proc.stdout+'\n'+proc.stderr)
        result=json.loads(proc.stdout.splitlines()[-1]);assert result['status'] in ('pass','complete_necessary_exclusion_inventory')
        runs.append(dict(script=script,exit=0,output=result));print(script+': pass',flush=True)
    for n,b in expected.items():
        assert (folder/n).read_bytes()==b,n
        for f,h in json.loads(b)['source_sha256'].items():assert sha(folder/f)==h,f
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),sha256=sha(archive),files=len(names),checksum_entries=len(checks),audits_reproduced_byte_identically=2,data_files_reproduced_byte_identically=1,runs=runs,source_sha256={Path(__file__).name:sha(Path(__file__))})
    (ROOT/'b1_b2_inverse_union_certificate_reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('runs','source_sha256')}),flush=True)
if __name__=='__main__':main()
