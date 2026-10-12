"""Full independent native kernel, literal quota and closed-set verification."""
from copy import deepcopy
from hashlib import sha256
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'investigation';sys.path.insert(0,str(ROOT))
import check_b1_b2_inverse_union as independent
NAME='b2_mixed_c4_third7'

def read(p):return json.loads(p.read_text())
def digest(p):return sha256(p.read_bytes()).hexdigest()

def main():
    filename=NAME+'_inverse_native_inventory_20261012.json'
    dest=HERE/(NAME+'_inverse_native_audit_20261012.json');assert not dest.exists()
    data=read(HERE/filename)
    assert data['status']=='complete_necessary_native_inventory_QA_only' and data['parameter']==[13,9,1]
    for n,h in data['source_sha256'].items():
        p=ROOT/('b1_b2_inverse_union_baseline_state.json' if n=='active_research.json' else n)
        assert digest(p)==h,n
    for n,h in data['qa_source_sha256'].items():assert digest(HERE/n)==h,n
    zmap={z['id']:z for z in read(ROOT/'small_first_third_inventory.json')['records']}
    nmap={z['id']:z for z in read(ROOT/'three_cover_atom_kernel_inventory.json')['records']}
    checked=independent.verify_geometry(data,zmap[NAME],nmap[NAME])
    assert checked['global_classes']==18277 and checked['counts']==dict(preliminary_missing_supplier=15483,missing_supplier=1722,maximal_graph_not_SC=1072)
    assert not checked['counts'].get('retained_overapproximation',0)
    control_name='b2_mixed_c5_third3'
    positive=next(z for z in read(ROOT/'b1_b2_inverse_union_inventory.json')['records'] if z['id']==control_name)
    positive_checked=independent.verify_geometry(positive,zmap[control_name],nmap[control_name])
    assert positive_checked['counts']['retained_overapproximation']>0
    rejected=[]
    def bad(label,fn,original=data):
        d=deepcopy(original);fn(d)
        try:independent.verify_geometry(d,zmap[d['id']],nmap[d['id']])
        except AssertionError:rejected.append(label)
        else:raise AssertionError('Accepted native corruption: '+label)
    bad('missing immediate graph',lambda d:d['records'].pop())
    bad('duplicate immediate graph',lambda d:d['records'].append(deepcopy(d['records'][0])))
    bad('wrong mandatory set',lambda d:d['mandatory'].append(0))
    bad('wrong preimage field',lambda d:d['fields'][0].update(preA=[12]))
    bad('omitted native kernel',lambda d:next(f for f in d['fields'] if f['compatible_kernel_masks'])['compatible_kernel_masks'].pop())
    bad('invented preliminary supplier',lambda d:next(c for c in d['records'] if c['reason']=='preliminary_missing_supplier')['supplier_options'].__setitem__(0,not next(c for c in d['records'] if c['reason']=='preliminary_missing_supplier')['supplier_options'][0]))
    bad('improper closed set',lambda d:next(c for c in d['records'] if c['reason']=='maximal_graph_not_SC').update(closed_set=list(range(13))))
    bad('omitted allowed arrow',lambda d:next(c for c in d['records'] if c['reason']=='maximal_graph_not_SC')['maximal_arrows'][0].append(12))
    bad('false rejection of retained control',lambda d:next(c for c in d['records'] if c['reason']=='retained_overapproximation').update(reason='missing_supplier'),positive)
    assert len(rejected)==9
    closure_controls=0
    for family in [[],[0],[0,1],[1,2,3],[1,2,4,8,16],[3,5,6],[1,1,2,0]]:
        actual={0}
        for m in family:actual|={m|u for u in actual if (m|u).bit_count()<=4}
        actual.discard(0);assert sorted(actual)==independent.graphs(family);closure_controls+=1
    premises=['three_cover_atom_kernel_audit.json','small_first_third_audit.json','mandatory_core_isolation_audit.json','inverse_clique_letter_controls_audit.json']
    rootfiles={'check_b1_b2_inverse_union.py','small_first_third_inventory.json','three_cover_atom_kernel_inventory.json',
        'b1_b2_inverse_union_inventory.json','b1_b2_inverse_union_baseline_state.json','B1_B2_INVERSE_UNION_EXCLUSION.md',*premises}
    for n in premises:
        d=read(ROOT/n);assert d['status']=='pass'
        for f,h in d['source_sha256'].items():assert digest(ROOT/f)==h;rootfiles.add(f)
    out=dict(status='pass',id=NAME,parameter=[13,9,1],target_ac=12,complete_conditional_native_geometry_exclusion=True,
        independent_domain=checked,retained_positive_control=positive_checked,
        corruptions_rejected=rejected,union_closure_controls=closure_controls,no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        scope='Complete arbitrary finite alphabet native inverse-domain exclusion of one geometry only. No new F value or alphabet separation; isolated replay and gated adoption still required.',
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,filename,*data['qa_source_sha256']]},
        root_source_sha256={n:digest(ROOT/n) for n in sorted(rootfiles)})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','root_source_sha256')}),flush=True)

if __name__=='__main__':main()
