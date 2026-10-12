"""Gate a complete conditional thirteen-state geometry after three replays.

This is a native-domain cut, not a new numerical upper bound or a fold lift.
"""
from hashlib import sha256
import json,sys,zipfile
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'investigation'
NAME='b2_mixed_c4_third2'

def digest(p):
    h=sha256()
    with p.open('rb') as f:
        while b:=f.read(8<<20):h.update(b)
    return h.hexdigest()

def read(p):return json.loads(p.read_text())

def archive_check(d):
    archive=(HERE/d['archive']).resolve();assert archive.is_relative_to(HERE.resolve())
    assert digest(archive)==d['sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==d['files']
        prefix=z.namelist()[0].split('/')[0]
        for n in z.namelist():
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix
        lines=z.read(prefix+'/CHECKSUMS.txt').decode().splitlines()
        assert len(lines)==d['checksum_entries']==d['files']-1
        for line in lines:
            h,n=line.split('  ',1);actual=sha256()
            with z.open(prefix+'/'+n) as f:
                while b:=f.read(8<<20):actual.update(b)
            assert actual.hexdigest()==h,n
    return prefix

def main():
    dest=ROOT/(NAME+'_composite_filtration_full_audit.json');assert not dest.exists()
    sources={Path(__file__).name:Path(__file__)}
    receipts=[(NAME+'_quotient_partial_0_966_reproduction_20261012_v6.json',13,[0,966]),
              (NAME+'_filtration_range_967_1638_reproduction_20261012_v7.json',18,[967,1638])]
    replay_summaries=[];reproduced=0
    for n,expected,extent in receipts:
        d=read(HERE/n);assert d['status']=='pass' and d['id']==NAME
        assert d['prefix_range']==extent and d['no_authoritative_exclusion'] and d['no_new_numerical_extremum']
        assert d['complete_selected_prefix_certificate'] and not d['complete_conditional_flag_tree_certificate']
        assert d['byte_identical_scope_and_audit_reports']==len(d['runs'])==expected
        if extent[0]==0:assert d['candidate_prefix_not_excluded']==967
        prefix=archive_check(d);local=HERE/(prefix+'_reproduction')/prefix/'_qa'
        sources[n]=HERE/n;sources[d['archive']]=HERE/d['archive']
        for f,h in d['source_sha256'].items():assert digest(HERE/f)==h; sources[f]=HERE/f
        for run in d['runs']:
            assert run['exit']==0;f=run['report'];assert digest(local/f)==digest(HERE/f)==d['source_sha256'][f]
            obj=read(HERE/f) if (HERE/f).stat().st_size<10_000_000 else None
            if obj:
                for key,base in [('source_sha256',HERE),('root_source_sha256',ROOT)]:
                    for q,h in obj.get(key,{}).items():
                        p=base/q;assert digest(p)==h;sources[p.relative_to(HERE.parent).as_posix()]=p
        replay_summaries.append(dict(receipt=n,archive=d['archive'],sha256=d['sha256'],reports=expected,prefix_range=extent))
        reproduced+=expected
    assembly_name=NAME+'_composite_filtration_scope_reproduction_20261012.json'
    assembly=read(HERE/assembly_name);assert assembly['status']=='pass'
    assert assembly['native_prefixes']==1639 and assembly['negative_ranges']==[[0,966],[967,1638]]
    assert assembly['byte_identical_scope_reports']==1 and assembly['scope_controls_rejected']==10
    prefix=archive_check(assembly)
    auditfile=NAME+'_composite_filtration_scope_audit_20261012.json';scope_audit=read(HERE/auditfile)
    assert scope_audit['status']=='pass' and scope_audit['exact_native_prefix_coverage']==1639
    assert scope_audit['counts']['prefixes']==1639 and scope_audit['counts']['literal_letters']==63698784
    assert len(scope_audit['rejected_invalid_scope_controls'])==10 and not scope_audit['original_candidate_counted_as_negative']
    assert digest(HERE/(prefix+'_reproduction')/prefix/auditfile)==digest(HERE/auditfile)
    for f,h in assembly['source_sha256'].items():assert digest(HERE/f)==h;sources[f]=HERE/f
    sources[assembly_name]=HERE/assembly_name;sources[assembly['archive']]=HERE/assembly['archive']
    reports=[NAME+'_graph_quotient_scope.json',NAME+'_graph_quotient_transport_audit.json',NAME+'_graph_transport_protection_audit.json']
    scope,transport,protection=map(lambda n:read(HERE/n),reports)
    assert scope['status']=='complete_transport_scope_only' and transport['status']==protection['status']=='pass'
    assert transport['rejected_invalid_metadata']==12
    assert len(protection['rejected_bijective_graph_preserving_corruptions'])==2
    assert transport['counts']['canonical_prefixes']==len(scope['prefixes'])==1639
    assert len(scope['raw_classes'])==598
    assert transport['counts']==dict(raw_graph_classes=598,canonical_graph_classes=29,labelled_ordered_pairs=429016,canonical_prefixes=1639)
    for n in reports:sources[n]=HERE/n
    # This report describes only the native case, with actual inherited premises.
    out=dict(status='pass',parameter=[13,9,1],target_ac=12,interval=[11,12],
        complete_conditional_geometry_exclusion=True,new_excluded_third_ids=[NAME],
        unrestricted_alphabet=True,binary_case_already_excluded=True,
        checked_prefixes=1639,canonical_prefixes=1639,raw_graph_classes=598,canonical_graph_classes=29,
        labelled_first_pairs=429016,metadata_corruptions_rejected=14,assembly_corruptions_rejected=10,
        tree_counts=scope_audit['counts'],maximum_basis_depth=11,
        byte_identical_scope_and_audit_reports=reproduced+1,replays=replay_summaries,
        assembly_replay=dict(receipt=assembly_name,archive=assembly['archive'],sha256=assembly['sha256'],reports=1),
        no_new_numerical_extremum=True,alphabet_separation_established=False,
        scope='Complete conditional exclusion of one native geometry at (13,9,1),target12, for finite arbitrary alphabets. All 1639 prefixes covered by two independently checked and isolated byte-identical tree ranges. Does not establish a new F value, alphabet separation or full folded-profile transport.',
        source_sha256={(p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('..')/p.relative_to(ROOT.parent)).as_posix():digest(p) for p in sorted(set(sources.values()))})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)

if __name__=='__main__':main()
