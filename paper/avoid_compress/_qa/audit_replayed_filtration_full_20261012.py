"""Full native-domain gate for the generic independently checked v12 engine."""
from collections import Counter
from hashlib import sha256
import json,sys,zipfile
from pathlib import Path,PurePosixPath
from package_quotient_flags_20261012_v2 import metadata
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'investigation'

def read(p):return json.loads(p.read_text())
def digest(p):
    h=sha256()
    with p.open('rb') as f:
        while b:=f.read(8<<20):h.update(b)
    return h.hexdigest()

def main():
    name=sys.argv[1];assert name.replace('_','').isalnum()
    dest=ROOT/(name+'_filtration_full_audit.json');assert not dest.exists()
    rn=name+'_filtration_full_reproduction_20261012_v8.json';r=read(HERE/rn)
    assert r['status']=='pass' and r['id']==name and r['complete_conditional_flag_tree_certificate']
    assert r['byte_identical_scope_and_audit_reports']==len(r['runs'])==18 and all(x['exit']==0 for x in r['runs'])
    archive=(HERE/r['archive']).resolve();assert archive.is_relative_to(HERE.resolve()) and digest(archive)==r['sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==r['files']
        prefix=z.namelist()[0].split('/')[0]
        for n in z.namelist():
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix
        lines=z.read(prefix+'/CHECKSUMS.txt').decode().splitlines();assert len(lines)==r['checksum_entries']==r['files']-1
        for line in lines:
            h,n=line.split('  ',1);actual=sha256()
            with z.open(prefix+'/'+n) as f:
                while b:=f.read(8<<20):actual.update(b)
            assert actual.hexdigest()==h,n
    sources={Path(__file__).resolve(),HERE/rn,archive,HERE/'package_quotient_flags_20261012_v2.py'}
    local=HERE/(prefix+'_reproduction')/prefix/'_qa'
    for n,h in r['source_sha256'].items():assert digest(HERE/n)==h;sources.add(HERE/n)
    for run in r['runs']:
        n=run['report'];assert digest(local/n)==digest(HERE/n)==r['source_sha256'][n]
        d=metadata(HERE/n)
        for key,base in [('source_sha256',HERE),('root_source_sha256',ROOT)]:
            for f,h in d.get(key,{}).items():assert digest(base/f)==h;sources.add(base/f)
    scope=read(HERE/(name+'_graph_quotient_scope.json'))
    transport=read(HERE/(name+'_graph_quotient_transport_audit.json'))
    protection=read(HERE/(name+'_graph_transport_protection_audit.json'))
    assert transport['status']==protection['status']=='pass' and transport['rejected_invalid_metadata']==12
    assert len(protection['rejected_bijective_graph_preserving_corruptions'])==2
    full=metadata(HERE/(name+'_product_supplier_from0_v12_probe.json'))
    assert full['id']==name and full['parameter']==[13,9,1] and full['target_ac']==12
    assert full['complete_scope'] and full['complete_range'] and full['range_start']==0 and full['candidate'] is None
    n=len(scope['prefixes']);assert n>0 and full['total_native_prefixes']==full['counts']['prefixes']==transport['counts']['canonical_prefixes']==n
    # Read the native arrays to check every negative prefix, never just header counts.
    data=read(HERE/(name+'_product_supplier_from0_v12_probe.json'))
    assert [x['index'] for x in data['prefixes']]==list(range(n));counts=Counter()
    for x,p in zip(data['prefixes'],scope['prefixes']):
        assert all(x.get(f)==v for f,v in p.items())
        counts.update(x['tree_stats']);counts['prefixes']+=1;counts['literal_letters']+=x['letter_count']
    assert dict(counts)==full['counts']
    depths=[int(k.split('_')[1]) for k,v in counts.items() if k.startswith('depth_') and v]
    assert max(depths)<=11
    c=transport['counts']
    out=dict(status='pass',id=name,parameter=[13,9,1],target_ac=12,interval=[11,12],
        complete_conditional_geometry_exclusion=True,new_excluded_third_ids=[name],
        checked_prefixes=n,canonical_prefixes=n,raw_graph_classes=c['raw_graph_classes'],canonical_graph_classes=c['canonical_graph_classes'],
        labelled_first_pairs=c['labelled_ordered_pairs'],metadata_corruptions_rejected=14,
        tree_counts=dict(counts),maximum_basis_depth=max(depths),byte_identical_scope_and_audit_reports=18,
        archive='../_qa/'+r['archive'],archive_sha256=r['sha256'],archive_files=r['files'],reproduction='../_qa/'+rn,
        no_new_numerical_extremum=True,alphabet_separation_established=False,
        scope='Complete conditional arbitrary finite alphabet exclusion of one native geometry at(13,9,1),target12. Every native prefix has an independently checked literal/rational tree and isolated byte-identical regeneration. No numerical F value, separation or full folded-profile transport.',
        source_sha256={(p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('..')/p.relative_to(ROOT.parent)).as_posix():digest(p) for p in sorted(sources)})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)

if __name__=='__main__':main()
