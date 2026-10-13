"""Positive records and deliberately corrupted local negative certificates."""
from pathlib import Path
import copy,json,hashlib
import check_b1_b2_inverse_union as independent
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    data=read('b1_b2_inverse_union_inventory.json');scope=read('b1_b2_inverse_union_scope.json')
    zmap={z['id']:z for z in read('small_first_third_inventory.json')['records']};nmap={z['id']:z for z in read('three_cover_atom_kernel_inventory.json')['records']}
    name='b2_mixed_c12_third7';original=next(z for z in data['records'] if z['id']==name)
    positive=next(z for z in data['records'] if z['id']==scope['retained_control'])
    for record in (original,positive):independent.verify_geometry(record,zmap[record['id']],nmap[record['id']])
    cases=[]
    def altered(label,fn,base=original):
        x=copy.deepcopy(base);fn(x);cases.append((label,x))
    altered('missing_global_graph',lambda x:x['records'].pop())
    altered('duplicate_global_graph',lambda x:x['records'].append(copy.deepcopy(x['records'][0])))
    altered('invented_supplier',lambda x:next(c for c in x['records'] if c['reason']=='preliminary_missing_supplier')['supplier_options'].__setitem__(0,not next(c for c in x['records'] if c['reason']=='preliminary_missing_supplier')['supplier_options'][0]))
    altered('altered_arrows',lambda x:next(c for c in x['records'] if c['reason']=='maximal_graph_not_SC')['maximal_arrows'][0].append(12))
    altered('improper_closed_set',lambda x:next(c for c in x['records'] if c['reason']=='maximal_graph_not_SC').__setitem__('closed_set',list(range(13))))
    altered('wrong_mandatory_core',lambda x:x['mandatory'].append(0))
    altered('omitted_native_kernel',lambda x:next(f for f in x['fields'] if f['compatible_kernel_masks'])['compatible_kernel_masks'].pop())
    altered('changed_field',lambda x:x['fields'][0].__setitem__('preA',[12]))
    altered('false_retained_rejection',lambda x:next(c for c in x['records'] if c['reason']=='retained_overapproximation').__setitem__('reason','missing_supplier'),positive)
    rejected=[]
    for label,x in cases:
        try:independent.verify_geometry(x,zmap[x['id']],nmap[x['id']])
        except AssertionError:rejected.append(label)
        else:raise AssertionError('Accepted corruption: '+label)
    assert len(rejected)==9
    # Independent union-closure controls include the empty native kernel,
    # repeated kernels, disconnected pairs, triples, and a capped union.
    graph_controls=0
    for family in [[],[0],[0,1],[1,2,3],[1,2,4,8,16],[3,5,6],[1,1,2,0]]:
        actual={0}
        for m in family:actual|={m|u for u in actual if (m|u).bit_count()<=4}
        actual.discard(0);assert sorted(actual)==independent.graphs(family);graph_controls+=1
    sources=[Path(__file__).name,'check_b1_b2_inverse_union.py','b1_b2_inverse_union_inventory.json','b1_b2_inverse_union_scope.json','small_first_third_inventory.json','three_cover_atom_kernel_inventory.json']
    result=dict(status='pass',positive_geometry_controls=2,union_closure_controls=graph_controls,adversarial_controls_rejected=len(rejected),rejected=rejected,source_sha256={n:sha(ROOT/n) for n in sources},scope='Local controls of exact certificate verification; no F theorem.')
    (ROOT/'b1_b2_inverse_union_controls_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}))
if __name__=='__main__':main()
