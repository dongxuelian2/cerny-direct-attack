"""Independent complete native-domain transports and adversarial metadata audit."""
from collections import Counter
import copy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'investigation';sys.path.insert(0,str(ROOT))
from check_b1_b2_inverse_union import verify_geometry
PAIRS=list(combinations(range(13),2));INDEX={e:i for i,e in enumerate(PAIRS)}
def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def move_edges(mask,perm):return sum(1<<INDEX[tuple(sorted(perm[q] for q in e))] for i,e in enumerate(PAIRS) if mask>>i&1)
def mset(mask):return {p for p in range(13) if mask>>p&1}
def mask(X):return sum(1<<p for p in X)

def verify(scope,parent,z):
    assert scope['status']=='complete_transport_scope_only' and scope['parameter']==[13,9,1] and scope['target_ac']==12
    B,C,D=map(set,(z['B'],z['C'],z['D']));controls=[{0,1,2},{3},B,C,D,set(parent['mandatory'])]
    for f in parent['fields']:controls.extend(set(f[k]) for k in ('preA','preB','preC'))
    atoms={}
    for p in range(13):atoms.setdefault(tuple(p in X for X in controls),[]).append(p)
    cells=list(atoms.values());assert {tuple(c) for c in scope['cells']}=={tuple(c) for c in cells}
    keep={r['P1_mask']:r for r in parent['records'] if r['reason']=='retained_overapproximation'}
    assert [r['P1_mask'] for r in scope['raw_classes']]==sorted(keep)
    allframes=[set(S) for S in combinations(range(13),9) if 3 in S and all(len(set(S)&X)==1 for X in (B,C,D))]
    expected=Counter();labelled=0;checked_targets=set()
    for r in scope['raw_classes']:
        graph=r['P1_mask'];target=r['target_P1'];p=r['permutation'];old=keep[graph]
        assert len(p)==13 and set(p)==set(range(13)) and target in keep and move_edges(graph,p)==target
        new=keep[target];assert all({p[q] for q in X}==X for X in controls)
        assert {tuple(sorted(p[q] for q in e)) for e in old['G']}==set(map(tuple,new['G']))
        for f in parent['fields']:
            assert sorted(move_edges(m,p) for m in f['compatible_kernel_masks'])==f['compatible_kernel_masks']
        for a,b in zip(old['field_kernel_masks'],new['field_kernel_masks']):assert sorted(move_edges(m,p) for m in a)==b
        G=list(map(set,old['G']));frames=[S for S in allframes if not any(e<=S for e in G)]
        assert r['frames']==[mask(S) for S in frames]
        fixed={q for i,e in enumerate(PAIRS) if target>>i&1 for q in e};free=[sorted(set(c)-fixed) for c in cells if set(c)-fixed]
        if target not in checked_targets:
            # Adjacent transpositions generate every second-stage cell permutation.
            for cell in free:
                for u,v in zip(cell,cell[1:]):
                    t=list(range(13));t[u],t[v]=v,u
                    assert move_edges(target,t)==target and all({t[q] for q in X}==X for X in controls)
                    assert {tuple(sorted(t[q] for q in e)) for e in new['G']}==set(map(tuple,new['G']))
                    for f in parent['fields']:assert sorted(move_edges(m,t) for m in f['compatible_kernel_masks'])==f['compatible_kernel_masks']
                    for kernels in new['field_kernel_masks']:assert sorted(move_edges(m,t) for m in kernels)==kernels
            checked_targets.add(target)
        for S in frames:
            U={p[q] for q in S}
            for T in frames:
                if S==T:continue
                V={p[q] for q in T};t=list(range(13))
                for cell in free:
                    ordered=[]
                    for a,b in ((False,False),(False,True),(True,False),(True,True)):
                        ordered.extend(q for q in cell if (q in U)==a and (q in V)==b)
                    for oldq,newq in zip(ordered,cell):t[oldq]=newq
                expected[target,(mask(t[q] for q in U),mask(t[q] for q in V))]+=1;labelled+=1
    saved={(r['P1_mask'],tuple(r['basis'])):r['multiplicity'] for r in scope['prefixes']}
    assert len(saved)==len(scope['prefixes']) and saved==expected and labelled==scope['labelled_ordered_pairs']
    assert scope['canonical_graph_classes']==len(checked_targets)
    return dict(raw_graph_classes=len(keep),canonical_graph_classes=len(checked_targets),
        labelled_ordered_pairs=labelled,canonical_prefixes=len(expected))

def main():
    name=sys.argv[1];file=name+'_graph_quotient_scope.json';scope=read(HERE/file);parent=read(HERE/(name+'_inverse_probe.json'))
    for n,h in scope['source_sha256'].items():assert digest(HERE/n)==h,n
    for n,h in scope['root_source_sha256'].items():assert digest(ROOT/n)==h,n
    z=next(z for z in read(ROOT/'small_first_third_inventory.json')['records'] if z['id']==name)
    native=next(z for z in read(ROOT/'three_cover_atom_kernel_inventory.json')['records'] if z['id']==name)
    assert verify_geometry(parent,z,native)==scope['parent_domain'];positive=verify(scope,parent,z)
    rejected=[]
    def test(label,mutate):
        d=copy.deepcopy(scope);mutate(d)
        try:verify(d,parent,z)
        except AssertionError:rejected.append(label);return
        raise AssertionError('Accepted corrupted metadata: '+label)
    test('missing raw graph',lambda d:d['raw_classes'].pop())
    test('duplicate raw graph',lambda d:d['raw_classes'].append(d['raw_classes'][0]))
    test('missing frame',lambda d:d['raw_classes'][0]['frames'].pop())
    test('wrong frame',lambda d:d['raw_classes'][0]['frames'].__setitem__(0,0))
    test('nonbijective first transport',lambda d:d['raw_classes'][0]['permutation'].__setitem__(0,d['raw_classes'][0]['permutation'][1]))
    test('wrong target graph',lambda d:d['raw_classes'][0].__setitem__('target_P1',0))
    test('unprotected first transport',lambda d:d['raw_classes'][0]['permutation'].__setitem__(3,0))
    test('missing prefix',lambda d:d['prefixes'].pop())
    test('duplicate prefix',lambda d:d['prefixes'].append(d['prefixes'][0]))
    test('wrong multiplicity',lambda d:d['prefixes'][0].__setitem__('multiplicity',0))
    test('wrong parameter',lambda d:d.__setitem__('parameter',[13,8,1]))
    test('wrong target length',lambda d:d.__setitem__('target_ac',13))
    out=dict(status='pass',id=name,counts=positive,rejected_invalid_metadata=len(rejected),rejected_records=rejected,
        no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        scope='Complete native graph/first-pair transport audit only; no flag-tree exclusion.',
        source_sha256={Path(__file__).name:digest(Path(__file__)),file:digest(HERE/file),
            name+'_inverse_probe.json':digest(HERE/(name+'_inverse_probe.json')),
            'GRAPH_FIRST_TRANSPORTS.md':digest(HERE/'GRAPH_FIRST_TRANSPORTS.md')},
        root_source_sha256={n:digest(ROOT/n) for n in ['check_b1_b2_inverse_union.py','small_first_third_inventory.json',
            'three_cover_atom_kernel_inventory.json','FEW_GRAPH_FIRST_PAIR_CERTIFICATES.md']})
    dest=HERE/(name+'_graph_quotient_transport_audit.json');assert not dest.exists()
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','root_source_sha256')}),flush=True)
if __name__=='__main__':main()
