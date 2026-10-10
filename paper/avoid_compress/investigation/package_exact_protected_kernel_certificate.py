"""Direct-premise exact/protected-kernel package and isolated audit regeneration."""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,subprocess,sys
ROOT=Path(__file__).resolve().parent;PREFIX='exact_protected_kernel'
NEW=['exact_atom_kernel_compatibility_audit.json','two_cover_third_exact_kernel_audit.json',
     'two_cover_protected_kernel_graph_audit.json','two_cover_protected_kernel_application_audit.json',
     'singleton_c_d5_e16_transport_audit.json']
OLD=['letter_image_short_pair_cover_audit.json','two_cover_third_unique_kernel_audit.json',
     'small_first_third_audit.json','two_cover_unique_immediate_pair_audit.json','mandatory_core_isolation_audit.json',
     'two_cover_p3_classification_audit.json','finite_independent_image_trap_audit.json','b1_c4_fourth_audit.json']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    archive=ROOT/'certificates'/f'{PREFIX}.zip'
    if '--check-package' not in sys.argv:
        names={'EXACT_PROTECTED_KERNEL_CERTIFICATE_README.md'}
        for n in NEW+OLD:
            z=json.loads((ROOT/n).read_text());assert z['status']=='pass';names.add(n)
            for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f
            names.update(z['source_sha256'])
        contents={('README.md' if n=='EXACT_PROTECTED_KERNEL_CERTIFICATE_README.md' else n):(ROOT/n).read_bytes() for n in sorted(names)}
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
    folder=dest/PREFIX;expected={n:(folder/n).read_bytes() for n in NEW};runs=[]
    scripts=['check_exact_atom_kernel_compatibility.py','check_two_cover_third_exact_kernel.py',
             'check_two_cover_protected_kernel_graph.py','check_two_cover_protected_kernel_application.py',
             'check_singleton_c_d5_e16_transport.py']
    for script in scripts:
        r=subprocess.run([sys.executable,'-B',str(folder/script)],cwd=folder,capture_output=True,text=True)
        if r.returncode:raise RuntimeError(script+'\n'+r.stdout+'\n'+r.stderr)
        parsed=json.loads(r.stdout.splitlines()[-1]);assert parsed['status']=='pass'
        runs.append(dict(script=script,exit=r.returncode,output=parsed));print(script+': pass',flush=True)
    for n,b in expected.items():
        assert (folder/n).read_bytes()==b,n
        for f,h in json.loads(b)['source_sha256'].items():assert sha(folder/f)==h,f
    result=dict(status='pass',archive=str(archive.relative_to(ROOT)).replace('\\','/'),sha256=sha(archive),files=len(names),
                checksum_entries=len(checks),audits_reproduced_byte_identically=5,runs=runs,
                source_sha256={Path(__file__).name:sha(Path(__file__))})
    (ROOT/'exact_protected_kernel_certificate_reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('runs','source_sha256')}),flush=True)
if __name__=='__main__':main()
