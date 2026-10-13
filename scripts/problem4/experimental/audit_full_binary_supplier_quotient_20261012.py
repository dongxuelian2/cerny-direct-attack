"""Gated complete binary native geometry; never an unrestricted exclusion."""
from collections import Counter
from hashlib import sha256
from pathlib import Path,PurePosixPath
import json,sys,zipfile
HERE=Path(__file__).resolve().parent;PAPER=HERE.parent;ROOT=PAPER
def digest(p):
    h=sha256()
    with p.open('rb') as f:
        while data:=f.read(8<<20):h.update(data)
    return h.hexdigest()
def read(p):return json.loads(p.read_text())
def verify_scope(scope,transport,full):
    assert scope['id']==transport['id']==full['id']
    assert scope['parameter']==full['parameter']==[13,9,1] and scope['target_ac']==full['target_ac']==12
    assert full['status']=='complete_independently_checked_QA_only' and full['complete_scope'] is True
    assert full['binary_only'] is True and full['unrestricted_exclusion'] is False
    assert full['alphabet_scope']=='at most two literal letters'
    assert full['candidate'] is None and full['range_start']==0 and full['complete_range'] is True
    count=transport['counts']['canonical_prefixes'];assert len(scope['prefixes'])==len(full['prefixes'])==count
    assert full['total_native_prefixes']==full['counts']['prefixes']==count
    assert [r['index'] for r in full['prefixes']]==list(range(count))
    for r,z in zip(full['prefixes'],scope['prefixes']):
        assert r['P1_mask']==z['P1_mask'] and r['basis']==z['basis'] and r['multiplicity']==z['multiplicity']

def main():
    name=sys.argv[1];dest=ROOT/(name+'_binary_supplier_full_audit.json');assert not dest.exists()
    names=[name+'_graph_quotient_scope.json',name+'_graph_quotient_transport_audit.json',name+'_graph_transport_protection_audit.json',
           name+'_binary_supplier_from0_v1_probe.json',name+'_binary_supplier_quotient_reproduction.json',
           'binary_supplier_cover_audit_20261012.json','supplier_image_controls_audit_20261011.json','supplier_image_horizon_audit_20261011.json']
    objects={n:read(HERE/n) for n in names};sources={}
    for n,d in objects.items():
        sources['../_qa/'+n]=digest(HERE/n)
        for key,base in [('source_sha256',HERE),('root_source_sha256',ROOT)]:
            for f,h in d.get(key,{}).items():
                p=(base/f).resolve();assert p.is_relative_to(PAPER.resolve()) and digest(p)==h,(n,f)
                rel=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT.resolve()) else '../'+p.relative_to(PAPER).as_posix()
                sources[rel]=h
    scope,transport,protection,full,replay=[objects[n] for n in names[:5]]
    controls,image,horizon=[objects[n] for n in names[5:]]
    assert transport['status']==protection['status']==replay['status']==controls['status']==image['status']==horizon['status']=='pass'
    assert scope['id']==full['id']==name and protection['id']==name
    verify_scope(scope,transport,full)
    assert transport['rejected_invalid_metadata']==12 and len(protection['rejected_bijective_graph_preserving_corruptions'])==2
    assert controls['complete_small_families']==87947 and len(controls['corruptions_rejected'])==8
    assert image['adversarial_corruptions_rejected']==9 and horizon['valid_depth_premise_at_horizon_rejected'] and horizon['empty_required_group_rejected']
    rejected=[]
    def reject(label,mutate):
        d=dict(full);mutate(d)
        try:verify_scope(scope,transport,d)
        except AssertionError:rejected.append(label);return
        raise AssertionError('Accepted an invalid binary certificate scope: '+label)
    reject('wrong alphabet scope',lambda d:d.__setitem__('alphabet_scope','arbitrary finite'))
    reject('missing binary limitation',lambda d:d.__setitem__('binary_only',False))
    reject('promoted unrestricted exclusion',lambda d:d.__setitem__('unrestricted_exclusion',True))
    reject('wrong parameter',lambda d:d.__setitem__('parameter',[14,10,1]))
    reject('wrong target',lambda d:d.__setitem__('target_ac',11))
    reject('incomplete domain',lambda d:d.__setitem__('complete_scope',False))
    reject('omitted initial range',lambda d:d.__setitem__('range_start',1))
    reject('surviving candidate',lambda d:d.__setitem__('candidate',{}))
    reject('missing prefix',lambda d:d.__setitem__('prefixes',d['prefixes'][:-1]))
    reject('duplicate prefix',lambda d:d.__setitem__('prefixes',[d['prefixes'][0],*d['prefixes'][1:-1],d['prefixes'][0]]))
    def bad_basis(d):
        records=list(d['prefixes']);records[0]=dict(records[0],basis=[0,1]);d['prefixes']=records
    reject('wrong prefix basis',bad_basis)
    totals=Counter();maximum=0
    for r in full['prefixes']:
        totals.update(r['tree_stats']);totals['prefixes']+=1;totals['literal_letters']+=r['letter_count']
        maximum=max(maximum,max(int(k[6:]) for k,v in r['tree_stats'].items() if k.startswith('depth_') and v))
    assert dict(totals)==full['counts'] and totals['binary_supplier_cover']>0
    commands=[('audit_binary_supplier_cover_20261012.py',[]),('audit_supplier_image_controls.py',[]),
              ('audit_supplier_image_horizon.py',[]),('compile_native_graph_quotient.py',[name]),
              ('check_native_graph_quotient.py',[name]),('check_native_graph_protection.py',[name]),('probe_binary_supplier_range_v1.py',[name,'0'])]
    assert replay['binary_only'] is True and replay['unrestricted_exclusion'] is False and replay['complete_conditional_flag_tree_certificate']
    assert replay['byte_identical_scope_and_audit_reports']==len(replay['runs'])==7
    assert [(r['script'],r['arguments']) for r in replay['runs']]==commands and all(r['exit']==0 for r in replay['runs'])
    archive=(HERE/replay['archive']).resolve();assert digest(archive)==replay['sha256'];sources['../_qa/'+replay['archive']]=replay['sha256']
    prefix=name+'_binary_supplier_flags';isolated=HERE/(prefix+'_reproduction')/prefix/'_qa'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==replay['files']
        for n in z.namelist():
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]==prefix
        lines=z.read(prefix+'/CHECKSUMS.txt').decode().splitlines();assert len(lines)==replay['checksum_entries']==len(z.namelist())-1
        for line in lines:
            h,n=line.split('  ',1);assert sha256(z.read(prefix+'/'+n)).hexdigest()==h
        for n in names[:4]+names[5:]:assert z.read(prefix+'/_qa/'+n)==(HERE/n).read_bytes()==(isolated/n).read_bytes(),n
    sources['../_qa/'+Path(__file__).name]=digest(Path(__file__))
    out=dict(status='pass',id=name,parameter=[13,9,1],target_ac=12,
             complete_conditional_binary_geometry_exclusion=True,binary_only=True,unrestricted_exclusion=False,
             raw_graph_classes=transport['counts']['raw_graph_classes'],canonical_graph_classes=transport['counts']['canonical_graph_classes'],
             labelled_first_pairs=transport['counts']['labelled_ordered_pairs'],canonical_prefixes=len(scope['prefixes']),checked_prefixes=len(full['prefixes']),
             tree_counts=dict(totals),maximum_basis_depth=maximum,metadata_corruptions_rejected=14,
             binary_scope_corruptions_rejected=rejected,binary_rule_corruptions_rejected=8,supplier_image_rule_corruptions_rejected=11,
             new_excluded_binary_third_ids=[name],new_excluded_unrestricted_third_ids=[],byte_identical_scope_and_audit_reports=7,
             archive='../_qa/'+replay['archive'],interval=[11,12],no_new_numerical_extremum=True,
             scope='Complete conditional binary-only exclusion of this native geometry at (13,9,1),target12. No unrestricted exclusion, new F value or alphabet separation.',
             source_sha256=sources)
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
