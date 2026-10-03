"""Finite integer-functional controls of the arbitrary-real covering proof."""
import argparse,json
from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path

def digest(z):return sha256(json.dumps(z,separators=(',',':')).encode()).hexdigest()

def direction(beta):
    if any(beta[4:]):return None
    if beta[2]==0 and beta[1]==-beta[3]!=0:return '02'
    if beta[3]==0 and beta[1]==-beta[2]!=0:return '03'
    return None

def scope(n):
    core=[0,15,5,9,6,10];vertices=sorted(z+16*free for z in core for free in range(1<<(n-4)))
    forms=[[0]+list(tail) for tail in product((-1,0,1),repeat=n-1) if any(tail) and sum(tail)==0]
    values=[[sum(a*(S>>q&1) for q,a in enumerate(beta)) for S in vertices] for beta in forms]
    stream=sha256();covered=0;hist=Counter()
    for i,F in enumerate(forms):
        for j,G in enumerate(forms):
            actual=all(x*y==0 for x,y in zip(values[i],values[j]));predicted=direction(F) is not None and direction(G) is not None and direction(F)!=direction(G)
            assert actual==predicted;covered+=actual;hist[sum(x*y!=0 for x,y in zip(values[i],values[j]))]+=1
            stream.update(json.dumps([i,j,actual],separators=(',',':')).encode()+b'\n')
    return dict(n=n,coefficient_grid=[-1,0,1],canonical_first_coefficient=0,zero_sum_nonzero_forms=len(forms),ordered_form_pairs=len(forms)**2,
                boolean_vertices=len(vertices),vertices_sha256=digest(vertices),covering_pairs=covered,uncovered_vertex_histogram={str(k):hist[k] for k in sorted(hist)},semantic_sha256=stream.hexdigest())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('direct_attack/data/balanced_history_rigidity.json'));args=ap.parse_args()
    records=[scope(n) for n in range(5,9)]
    out=dict(records=records,boundary='PROVED paper exact REAL-space binary hyperplane-covering classification and necessary saturated-shortest-history guards, ANY n>=5. Integer finite controls only, not all real forms or DFAs. General Cerny and ALL/SOME history cost/rank OPEN; no formal verification.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(scopes=len(records),ordered_pairs=sum(z['ordered_form_pairs'] for z in records),boolean_vertex_product_controls=sum(z['ordered_form_pairs']*z['boolean_vertices'] for z in records),covering_pairs=sum(z['covering_pairs'] for z in records))),flush=True)

if __name__=='__main__':main()
