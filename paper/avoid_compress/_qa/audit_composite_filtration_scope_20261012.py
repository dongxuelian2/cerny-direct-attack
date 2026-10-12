"""Independent assembly audit, never an F-value or an adoption recorder.

Every tree still requires its own independent literal checker and isolated replay.
This audit checks that two disjoint negative arrays cover the exact native domain.
"""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import gc,json
from pathlib import Path

HERE=Path(__file__).resolve().parent
NAME='b2_mixed_c4_third2'
FILES=[NAME+'_product_supplier_from0_v8_probe.json',
       NAME+'_product_supplier_from967_v12_probe.json']

def digest(p):
    h=sha256()
    with p.open('rb') as f:
        while b:=f.read(8<<20):h.update(b)
    return h.hexdigest()

def read(p):
    with p.open() as f:return json.load(f)

def validate(scope,parts):
    expected=scope['prefixes'];assert len(expected)==1639
    assert len(parts)==2
    joined=[];total=Counter()
    for k,d in enumerate(parts):
        assert d['id']==NAME and d['parameter']==[13,9,1] and d['target_ac']==12
        assert d['total_native_prefixes']==len(expected) and not d['complete_scope']
        a,b=(0,967) if k==0 else (967,1639)
        assert d['range_start']==a
        if k==0:
            assert d['status']=='depth11_candidate_not_exclusion' and not d['complete_range']
            assert d['candidate'] is not None and d['candidate']['prefix']==967
        else:
            assert d['status']=='complete_range_independently_checked_QA_only'
            assert d['complete_range'] and d['candidate'] is None
        records=d['prefixes'];assert [r['index'] for r in records]==list(range(a,b))
        sums=Counter()
        for r in records:
            p=expected[r['index']]
            assert all(r.get(f)==v for f,v in p.items())
            assert isinstance(r['letter_count'],int) and r['letter_count']>0
            assert isinstance(r['tree'],dict) and isinstance(r['tree_stats'],dict)
            for f in ('rows_sha256','flags_sha256'):
                h=r[f];assert isinstance(h,str) and len(h)==64 and all(c in '0123456789abcdef' for c in h)
            sums.update(r['tree_stats']);sums['prefixes']+=1;sums['literal_letters']+=r['letter_count']
        assert dict(sums)==d['counts'];total.update(sums);joined.extend(r['index'] for r in records)
    assert joined==list(range(1639))
    return dict(total)

def compact(d):
    # Keep all independently audited per-prefix metadata; avoid copying large trees.
    out={k:v for k,v in d.items() if k not in ('prefixes','candidate')}
    out['candidate']=None if d['candidate'] is None else {'prefix':d['candidate']['prefix']}
    out['prefixes']=[{k:v for k,v in r.items() if k!='tree'}|{'tree':{}} for r in d['prefixes']]
    return out

def main():
    dest=HERE/(NAME+'_composite_filtration_scope_audit_20261012.json');assert not dest.exists()
    scopefile=NAME+'_graph_quotient_scope.json';scope=read(HERE/scopefile)
    assert scope['status']=='complete_transport_scope_only'
    parts=[]
    for n in FILES:
        d=read(HERE/n);parts.append(compact(d));del d;gc.collect()
    counts=validate(scope,parts);rejected=[]
    def bad(label,fn):
        p=deepcopy(parts);fn(p)
        try:validate(scope,p)
        except (AssertionError,KeyError,TypeError,IndexError):rejected.append(label)
        else:raise AssertionError('Accepted invalid composite scope: '+label)
    bad('missing last prefix',lambda p:p[1]['prefixes'].pop())
    bad('duplicate native prefix',lambda p:p[1]['prefixes'][1].update(index=967))
    bad('candidate counted as negative',lambda p:p[0]['prefixes'].append(deepcopy(p[1]['prefixes'][0])))
    bad('wrong range boundary',lambda p:p[1].update(range_start=966))
    bad('wrong original candidate',lambda p:p[0]['candidate'].update(prefix=968))
    bad('unexcluded second candidate',lambda p:p[1].update(candidate={'prefix':1638}))
    bad('wrong initial characteristic rows',lambda p:p[1]['prefixes'][0].update(basis=[0,0]))
    bad('wrong first-pair graph',lambda p:p[1]['prefixes'][0].update(P1_mask=-1))
    bad('wrong aggregate literal count',lambda p:p[1]['counts'].update(literal_letters=0))
    bad('full scope claimed by partial',lambda p:p[0].update(complete_scope=True))
    assert len(rejected)==10
    out=dict(status='pass',id=NAME,parameter=[13,9,1],target_ac=12,
        exact_native_prefix_coverage=1639,negative_ranges=[[0,966],[967,1638]],counts=counts,
        rejected_invalid_scope_controls=rejected,complete_assembly_scope_only=True,
        original_candidate_counted_as_negative=False,independent_tree_replays_still_required=True,
        no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,scopefile,*FILES]})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)

if __name__=='__main__':main()
