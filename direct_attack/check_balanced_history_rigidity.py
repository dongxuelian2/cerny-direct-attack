"""Independent four-bit direct equation and disjoint-zero-set cover audit."""
import argparse,copy,json
from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path

def digest(z):return sha256(json.dumps(z,separators=(',',':')).encode()).hexdigest()

def audit(z):
    n=z['n'];assert 5<=n<=8 and z['coefficient_grid']==[-1,0,1] and z['canonical_first_coefficient']==0
    vertices=[v for v in range(1<<n) if (v&1)+(v>>1&1)==(v>>2&1)+(v>>3&1)]
    assert len(vertices)==z['boolean_vertices']==6*2**(n-4) and digest(vertices)==z['vertices_sha256']
    forms=[]
    for tail in product((-1,0,1),repeat=n-1):
        if any(tail) and not sum(tail):forms.append((0,)+tail)
    assert len(forms)==z['zero_sum_nonzero_forms'] and len(forms)**2==z['ordered_form_pairs']
    nonzeros=[];classes=[]
    for F in forms:
        nonzeros.append({v for v in vertices if sum(a for q,a in enumerate(F) if v>>q&1)})
        assert nonzeros[-1] and sum(F)==0
        # Identify annihilated core pair directions, independently of the generator coefficient test.
        if any(F[q] for q in range(4,n)):classes.append(None)
        else:
            vanish=[pair for pair in ((0,2),(0,3)) if sum(F[q] for q in pair)==0]
            assert len(vanish)<=1;classes.append(vanish[0] if vanish else None)
    covered=0;hist=Counter();stream=sha256();free_controls=0
    for i,F in enumerate(forms):
        for j,G in enumerate(forms):
            intersection=nonzeros[i]&nonzeros[j];actual=not intersection
            predicted=classes[i] is not None and classes[j] is not None and classes[i]!=classes[j]
            assert actual==predicted;covered+=actual;hist[len(intersection)]+=1
            stream.update(json.dumps([i,j,actual],separators=(',',':')).encode()+b'\n')
            # The free-cube product can only vanish if one whole free restriction is zero.
            if all(F[p]*G[p]==0 for p in range(4,n)) and all((F[p]+F[q])*(G[p]+G[q])==0 for p in range(4,n) for q in range(p+1,n)):
                assert not any(F[4:]) or not any(G[4:])
            free_controls+=1
    assert covered==z['covering_pairs'] and z['uncovered_vertex_histogram']=={str(k):hist[k] for k in sorted(hist)} and z['semantic_sha256']==stream.hexdigest()
    return free_controls

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,default=Path('direct_attack/data/balanced_history_rigidity.json'));ap.add_argument('--out',type=Path,default=Path('direct_attack/data/balanced_history_rigidity_checks.json'));args=ap.parse_args()
    data=json.loads(args.data.read_text(encoding='utf-8'));assert [z['n'] for z in data['records']]==list(range(5,9));free=sum(audit(z) for z in data['records']);corruptions=[]
    for field,value in [('zero_sum_nonzero_forms',0),('covering_pairs',0),('vertices_sha256','0'*64),('semantic_sha256','0'*64),('ordered_form_pairs',0),('boolean_vertices',0)]:
        z=copy.deepcopy(data['records'][0]);z[field]=value
        try:audit(z)
        except AssertionError:corruptions.append(field)
        else:raise AssertionError('accepted '+field)
    out=dict(verified=True,scopes=4,ordered_form_pairs=sum(z['ordered_form_pairs'] for z in data['records']),
             boolean_vertex_product_controls=sum(z['ordered_form_pairs']*z['boolean_vertices'] for z in data['records']),
             free_restriction_pair_controls=free,covering_pairs=sum(z['covering_pairs'] for z in data['records']),corruptions_rejected=corruptions,
             boundary='independent exact finite integer-form Boolean covering controls only; the arbitrary-real classification and saturated-history implication are paper proofs, not formal or all-DFA verification. General Cerny and unrestricted cost/rank OPEN; separate negative pressure not part of this checker.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
