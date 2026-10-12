"""Check the complete replayed quotient certificate before authoritative adoption."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path,PurePosixPath
import zipfile,sys
HERE=Path(__file__).resolve().parent;PAPER=HERE.parent;ROOT=PAPER/'investigation';NAME=sys.argv[1]
def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    output=ROOT/(NAME+'_graph_quotient_full_audit.json');assert not output.exists()
    names=[NAME+'_graph_quotient_scope.json',NAME+'_graph_quotient_transport_audit.json',
        NAME+'_graph_transport_protection_audit.json',NAME+'_graph_quotient_full_probe.json',
        NAME+'_full_quotient_reproduction.json']
    objects={name:read(HERE/name) for name in names};sources={}
    for name,d in objects.items():
        sources['../_qa/'+name]=digest(HERE/name)
        for category,base in (('source_sha256',HERE),('root_source_sha256',ROOT)):
            for f,h in d.get(category,{}).items():
                p=(base/f).resolve();assert p.is_relative_to(PAPER.resolve()) and digest(p)==h,(name,f)
                rel=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT.resolve()) else '../'+p.relative_to(PAPER).as_posix()
                sources[rel]=h
    scope,transport,protection,full,replay=[objects[n] for n in names]
    assert scope['id']==full['id']==transport['id']==protection['id']==NAME
    assert scope['parameter']==full['parameter']==[13,9,1] and scope['target_ac']==full['target_ac']==12
    assert transport['status']==protection['status']==replay['status']=='pass'
    assert full['status']=='complete_independently_checked_QA_only' and full['complete_scope'] and full['candidate'] is None
    raw_count=transport['counts']['raw_graph_classes'];graph_count=transport['counts']['canonical_graph_classes'];labelled_count=transport['counts']['labelled_ordered_pairs'];prefix_count=transport['counts']['canonical_prefixes']
    assert raw_count==len(scope['raw_classes'])>0
    assert graph_count==scope['canonical_graph_classes']>0
    assert labelled_count==scope['labelled_ordered_pairs']>0
    assert prefix_count==len(scope['prefixes'])==len(full['prefixes'])>0
    assert transport['rejected_invalid_metadata']==12
    assert len(protection['rejected_bijective_graph_preserving_corruptions'])==2
    totals=Counter();maximum=0
    for index,(prefix,saved) in enumerate(zip(scope['prefixes'],full['prefixes'])):
        assert saved['index']==index
        for key in ('P1_mask','basis','multiplicity'):assert saved[key]==prefix[key]
        assert saved['tree']['basis']==saved['basis'] and saved['tree']['depth']==1
        assert len(saved['rows_sha256'])==len(saved['flags_sha256'])==64 and saved['letter_count']>=0
        totals.update(saved['tree_stats']);totals['prefixes']+=1;totals['literal_letters']+=saved['letter_count']
        maximum=max(maximum,max(int(k[6:]) for k,v in saved['tree_stats'].items() if k.startswith('depth_') and v))
    assert dict(totals)==full['counts'] and maximum<=11
    assert sum(totals[k] for k in ('maximal_graph_not_SC','missing_required_group','internal_nodes',
        'zero_prefix_column','forced_short_word','no_growth'))==totals['nodes']
    assert replay['byte_identical_scope_and_audit_reports']==4 and len(replay['runs'])==4
    assert [r['script'] for r in replay['runs']]==['compile_native_graph_quotient.py','check_native_graph_quotient.py',
        'check_native_graph_protection.py','probe_native_graph_quotient.py']
    assert all(r['arguments']==[NAME] for r in replay['runs'])
    assert all(r['exit']==0 for r in replay['runs']) and replay['complete_conditional_flag_tree_certificate']
    archive=HERE/replay['archive'];assert digest(archive)==replay['sha256'];sources['../_qa/'+replay['archive']]=replay['sha256']
    prefix=NAME+'_full_flags';isolated=HERE/(prefix+'_reproduction')/prefix/'_qa'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==replay['files']
        for n in z.namelist():
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix
        lines=z.read(prefix+'/CHECKSUMS.txt').decode().splitlines();assert len(lines)==replay['checksum_entries']==len(z.namelist())-1
        for line in lines:
            h,n=line.split('  ',1);assert sha256(z.read(prefix+'/'+n)).hexdigest()==h
        for name in names[:4]:
            assert z.read(prefix+'/_qa/'+name)==(HERE/name).read_bytes()==(isolated/name).read_bytes(),name
    sources['../_qa/'+Path(__file__).name]=digest(Path(__file__))
    out=dict(status='pass',id=NAME,parameter=[13,9,1],target_ac=12,raw_graph_classes=raw_count,
        canonical_graph_classes=graph_count,labelled_first_pairs=labelled_count,canonical_prefixes=prefix_count,checked_prefixes=prefix_count,
        tree_counts=dict(totals),maximum_basis_depth=maximum,metadata_corruptions_rejected=14,
        complete_conditional_geometry_exclusion=True,new_excluded_third_ids=[NAME],
        byte_identical_scope_and_audit_reports=4,archive='../_qa/'+replay['archive'],
        no_new_numerical_extremum=True,interval=[11,12],
        scope='Complete conditional exclusion of this native geometry at (13,9,1),target12, for arbitrary finite alphabets. No F value or alphabet separation.',
        source_sha256=sources)
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
