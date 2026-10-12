"""Adversarial bijective graph-preserving tests of the actual native checker."""
import copy
from hashlib import sha256
import json
from pathlib import Path
import sys
from check_native_graph_quotient import verify,move_edges,ROOT,PAIRS
HERE=Path(__file__).resolve().parent

def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())

def main():
    name=sys.argv[1];file=name+'_graph_quotient_scope.json';scope=read(HERE/file)
    parent=read(HERE/(name+'_inverse_probe.json'))
    z=next(z for z in read(ROOT/'small_first_third_inventory.json')['records'] if z['id']==name)
    controls=[{0,1,2},{3},set(z['B']),set(z['C']),set(z['D']),set(parent['mandatory'])]
    for f in parent['fields']:controls.extend(set(f[k]) for k in ('preA','preB','preC'))
    tests=[]
    # Pick transpositions of isolated target vertices with different control cells.
    # Every mutation is a bijection and literally preserves the target P1 graph.
    for index,r in enumerate(scope['raw_classes']):
        fixed={q for i,e in enumerate(PAIRS) if r['target_P1']>>i&1 for q in e}
        free=sorted(set(range(13))-fixed)
        for u in free:
            for v in free:
                if u>=v or all((u in X)==(v in X) for X in controls):continue
                d=copy.deepcopy(scope);p=d['raw_classes'][index]['permutation']
                i,j=p.index(u),p.index(v);p[i],p[j]=p[j],p[i]
                assert set(p)==set(range(13)) and move_edges(r['P1_mask'],p)==r['target_P1']
                try:verify(d,parent,z)
                except AssertionError:
                    tests.append(dict(raw_index=index,swapped_target_vertices=[u,v]))
                    if len(tests)>=2:break
                    continue
                raise AssertionError('Accepted a bijective graph-preserving control violation')
            if len(tests)>=2:break
        if len(tests)>=2:break
    assert len(tests)>=2
    out=dict(status='pass',id=name,rejected_bijective_graph_preserving_corruptions=tests,
        no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        scope='Adversarial protection tests only; each mutation preserves bijectivity and the P1 graph.',
        source_sha256={Path(__file__).name:digest(Path(__file__)),'check_native_graph_quotient.py':digest(HERE/'check_native_graph_quotient.py'),
            file:digest(HERE/file),name+'_inverse_probe.json':digest(HERE/(name+'_inverse_probe.json'))},
        root_source_sha256={'small_first_third_inventory.json':digest(ROOT/'small_first_third_inventory.json')})
    dest=HERE/(name+'_graph_transport_protection_audit.json');assert not dest.exists()
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','root_source_sha256')}),flush=True)
if __name__=='__main__':main()
