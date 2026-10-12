"""Immutable, isolated replay of scope assembly; not a tree proof/adoption."""
from hashlib import sha256
import json,shutil,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
PREFIX='composite_filtration_scope_20261012'
NAME='b2_mixed_c4_third2'

def digest(p):
    h=sha256()
    with p.open('rb') as f:
        while b:=f.read(8<<20):h.update(b)
    return h.hexdigest()

def main():
    report=NAME+'_composite_filtration_scope_audit_20261012.json'
    receipt=HERE/(NAME+'_composite_filtration_scope_reproduction_20261012.json')
    assert not receipt.exists()
    audit=json.loads((HERE/report).read_text());assert audit['status']=='pass'
    files={n:HERE/n for n in [Path(__file__).name,report,*audit['source_sha256']]}
    for n,h in audit['source_sha256'].items():assert digest(files[n])==h
    extra={'README.md':(
        '# Composite native-prefix scope audit\n\n'
        'Python >=3.10, standard library. Run in this directory.\n'
        'The two stored negative arrays cover exactly0..966 and967..1638.\n'
        'Candidate967 in the first report is not counted as a negative.\n'
        'This package checks assembly, all native prefix metadata and aggregate counts.\n'
        'It is not a replay of the individual proof trees. Separate immutable packages\n'
        'must replay both drivers and all independent literal/rational tree checks\n'
        'before any authoritative exclusion. No F value or alphabet separation follows.\n'
        'Move aside '+report+' and run:\n'
        'python -B audit_composite_filtration_scope_20261012.py\n'
        'The recreated report must have the stored SHA256.\n').encode()}
    hashes={n:digest(p) for n,p in files.items()};hashes.update({n:sha256(b).hexdigest() for n,b in extra.items()})
    extra['CHECKSUMS.txt']=''.join(h+'  '+n+'\n' for n,h in sorted(hashes.items())).encode()
    archive=HERE/'certificates'/(NAME+'_'+PREFIX+'.zip');assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,allowZip64=True) as z:
        for n in sorted(set(files)|set(extra)):
            info=zipfile.ZipInfo(PREFIX+'/'+n,date_time=(2026,10,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            if n in extra:z.writestr(info,extra[n])
            else:
                with files[n].open('rb') as src,z.open(info,'w',force_zip64=True) as dst:shutil.copyfileobj(src,dst,8<<20)
    dest=(HERE/(PREFIX+'_reproduction')).resolve();assert not dest.exists() and dest.is_relative_to(HERE.resolve());dest.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(hashes)+1
        for n in z.namelist():
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==PREFIX
            assert (dest/n).resolve().is_relative_to(dest)
        z.extractall(dest)
    local=dest/PREFIX
    for n,h in hashes.items():assert digest(local/n)==h,n
    p=local/report;assert p.resolve().parent==local;p.unlink()
    proc=subprocess.run([sys.executable,'-B','audit_composite_filtration_scope_20261012.py'],cwd=local,capture_output=True,text=True)
    assert proc.returncode==0,(proc.stdout,proc.stderr)
    assert digest(local/report)==hashes[report]
    out=dict(status='pass',archive=archive.relative_to(HERE).as_posix(),sha256=digest(archive),
        files=len(hashes)+1,checksum_entries=len(hashes),byte_identical_scope_reports=1,
        native_prefixes=1639,negative_ranges=[[0,966],[967,1638]],scope_controls_rejected=10,
        proof_tree_replays_still_required=True,no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        source_sha256={n:digest(p) for n,p in files.items()})
    receipt.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)

if __name__=='__main__':main()
