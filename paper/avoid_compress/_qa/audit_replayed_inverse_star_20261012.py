"""Read-only full certificate gate before adopting one native geometry."""
import json,zipfile
from hashlib import sha256
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'investigation';NAME='b2_mixed_c4_third7'

def read(p):return json.loads(p.read_text())
def digest(p):
    h=sha256()
    with p.open('rb') as f:
        while b:=f.read(8<<20):h.update(b)
    return h.hexdigest()

def main():
    dest=ROOT/(NAME+'_inverse_native_full_audit.json');assert not dest.exists()
    rn=NAME+'_inverse_native_reproduction_20261012.json';r=read(HERE/rn)
    assert r['status']=='pass' and r['id']==NAME and r['complete_conditional_native_geometry_exclusion']
    assert r['byte_identical_generator_and_audit_reports']==len(r['runs'])==2
    assert all(run['exit']==0 for run in r['runs']) and r['corruptions_rejected']==9 and r['union_closure_controls']==7
    archive=(HERE/r['archive']).resolve();assert archive.is_relative_to(HERE.resolve()) and digest(archive)==r['sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==r['files']==50
        prefix=z.namelist()[0].split('/')[0]
        for n in z.namelist():
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix
        lines=z.read(prefix+'/CHECKSUMS.txt').decode().splitlines();assert len(lines)==r['checksum_entries']==49
        for line in lines:
            h,n=line.split('  ',1);actual=sha256()
            with z.open(prefix+'/'+n) as f:
                while b:=f.read(8<<20):actual.update(b)
            assert actual.hexdigest()==h,n
    sources={Path(__file__).resolve(),HERE/rn,archive}
    for n,h in r['source_sha256'].items():assert digest(HERE/n)==h;sources.add(HERE/n)
    local=HERE/(prefix+'_reproduction')/prefix/'_qa'
    for run in r['runs']:
        n=run['report'];assert digest(local/n)==digest(HERE/n)==r['source_sha256'][n]
    filename=NAME+'_inverse_native_audit_20261012.json';audit=read(HERE/filename)
    assert audit['status']=='pass' and audit['complete_conditional_native_geometry_exclusion']
    assert len(audit['corruptions_rejected'])==9 and audit['union_closure_controls']==7
    assert audit['retained_positive_control']['counts']['retained_overapproximation']==4
    for key,base in [('source_sha256',HERE),('root_source_sha256',ROOT)]:
        for n,h in audit[key].items():assert digest(base/n)==h;sources.add(base/n)
    domain=audit['independent_domain'];assert domain==r['independent_domain']
    assert domain['global_classes']==18277 and sum(domain['counts'].values())==18277
    assert domain['counts']==dict(preliminary_missing_supplier=15483,missing_supplier=1722,maximal_graph_not_SC=1072)
    assert domain['labelled_D_transports']==1 and domain['closed_set_transports']==1072
    out=dict(status='pass',id=NAME,parameter=[13,9,1],target_ac=12,interval=[11,12],
        complete_conditional_native_geometry_exclusion=True,new_excluded_third_ids=[NAME],arbitrary_finite_alphabet=True,
        domain=domain,corruptions_rejected=9,union_closure_controls=7,byte_identical_generator_and_audit_reports=2,
        archive='../_qa/'+r['archive'],archive_sha256=r['sha256'],archive_files=50,reproduction='../_qa/'+rn,
        no_new_numerical_extremum=True,alphabet_separation_established=False,
        scope='Complete conditional inverse-domain exclusion of b2_mixed_c4_third7 at(13,9,1),target12, for arbitrary finite alphabets. Existing native-field and P1<=4 premises only. No numerical F value, alphabet separation or full folded-profile transport.',
        source_sha256={(p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('..')/p.relative_to(ROOT.parent)).as_posix():digest(p) for p in sorted(sources)})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)

if __name__=='__main__':main()
