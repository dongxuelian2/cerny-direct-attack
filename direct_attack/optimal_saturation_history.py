"""Exact inverse rank-growth DAGs for fixed d3/d4 inputs; no all-d claim."""
import argparse
from collections import deque
from fractions import Fraction
import json
from pathlib import Path


def rank(sets,n):
    basis={}
    for S in sets:
        v=[Fraction(int(S>>q&1)) for q in range(n)]
        for j,b in sorted(basis.items()):
            if v[j]:
                x=v[j];v=[a-x*c for a,c in zip(v,b)]
        p=next((j for j,x in enumerate(v) if x),None)
        if p is not None:
            x=v[p];basis[p]=[a/x for a in v]
    return len(basis)


def profile(source):
    d,n,rows=(source[k] for k in ('d','n','rows'));Q=(1<<n)-1
    assert n==2**d-1 and all(len(set(r))==n-1 for r in rows)
    pop=[S.bit_count() for S in range(Q+1)];inverse=[]
    for row in rows:
        fibers=[0]*n
        for q,t in enumerate(row):fibers[t]|=1<<q
        table=[0]*(Q+1)
        for S in range(1,Q+1):
            b=S&-S;table[S]=table[S^b]|fibers[b.bit_length()-1]
        inverse.append(table)
    order=sorted(range(1,Q+1),key=lambda S:(-pop[S],S))
    good=[False]*(Q+1);good[Q]=True
    for S in order:
        if S!=Q:good[S]=any(pop[t[S]]==pop[S]+1 and good[t[S]] for t in inverse)
    roots=[1<<q for q in range(n) if good[1<<q]];assert roots
    reached=set(roots);queue=deque(roots)
    while queue:
        S=queue.popleft()
        for t in inverse:
            T=t[S]
            if pop[T]==pop[S]+1 and good[T] and T not in reached:reached.add(T);queue.append(T)
    blocks=[sum(1<<q for q in range(2**i-1,2**(i+1)-1)) for i in range(d)]
    selected=lambda k:sum(B for i,B in enumerate(blocks) if k>>i&1)
    proper=[selected(k) for k in range(2,n)]
    assert reached==set(roots+proper+[Q])
    assert rank(proper+[Q],n)==d
    words=[]
    def visit(S,reverse,trace):
        if S==Q:
            word=list(reversed(reverse));words.append(dict(original_indices=word,endpoint=trace[0],
                    inverse_sets=trace[:],full_inverse_raw_rank=rank(trace,n)))
            return
        for a,t in enumerate(inverse):
            T=t[S]
            if pop[T]==pop[S]+1 and good[T]:visit(T,reverse+[a],trace+[T])
    for root in roots:visit(root,[],[root])
    words.sort(key=lambda w:(w['endpoint'],w['original_indices']))
    assert all(w['inverse_sets'][1:-1]==proper for w in words)
    added=[]
    for q in range(n-1):
        row=list(range(n));row[q],row[q+1]=row[q+1],row[q];added.append(row)
    return dict(d=d,n=n,base_original_rows=rows,added_original_permutations=added,
                original_letter_ranks=[n-1]*len(rows),rt=n-1,P=n-1,
                optimal_inverse_roots=roots,all_optimal_growth_masks=sorted(reached),
                canonical_proper_masks=proper,proper_stage_count=n-2,
                raw_proper_plus_Q_rank=d,normalized_proper_rank=d-1,
                all_shortest_original_words=words,shortest_original_word_count=len(words),
                optimal_endpoint_chain_count=len(roots),
                inverse_all_subset_vertices=Q,inverse_label_edges=Q*len(rows),
                augmented_completely_reachable_count=Q,
                augmentation_boundary='only permutations added; rank-loss saturation excludes every added letter from all shortest words',
                scope='finite d'+str(d)+' ONLY; no all-d construction')


def generate():
    inputs=json.loads(Path('direct_attack/data/optimal_saturation_inputs.json').read_text())
    assert [r['d'] for r in inputs['records']]==[3,4]
    return dict(status='finite inverse DAG certificate; independent forward DAG checker required',
                records=[profile(r) for r in inputs['records']],
                boundary='paper permutation-augmentation theorem general; low logarithmic optimal geometry verified at n7/15 ONLY; general positive-fraction bound and Cerny OPEN')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='direct_attack/data/optimal_saturation_history.json')
    args=ap.parse_args();z=generate()
    Path(args.out).write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ('d','n','rt','P','proper_stage_count','normalized_proper_rank',
          'shortest_original_word_count','optimal_endpoint_chain_count')} for r in z['records']]))


if __name__=='__main__':main()
