"""Finite optimal endpoint-history audit via inverse BFS and rational rank."""
import argparse
from collections import Counter,deque
from fractions import Fraction
import json
from pathlib import Path


def generate():
    n=7; d=3; Q=(1<<n)-1
    blocks=[list(range(2**i-1,2**(i+1)-1)) for i in range(d)]
    def mask(k): return sum(1<<q for i,B in enumerate(blocks) if k>>i&1 for q in B)
    original=[]
    for j in range(n-1):
        row=list(range(n));row[j],row[j+1]=row[j+1],row[j];original.append(row)
    for k in range(2,n):
        i=next(i for i in range(1,d) if (k+1)>>i&1)
        s=blocks[i][0];X=mask(k+1)&~(1<<s)
        before=[q for q in range(n) if X>>q&1]+[q for q in range(n) if not (X>>q&1)]
        after=[q for q in range(n) if mask(k)>>q&1]+[q for q in range(n) if not (mask(k)>>q&1)]
        row=[None]*n
        for a,b in zip(before,after):row[a]=b
        original.append(row)
    for B in blocks[1:]:
        for s,t in ((B[0],B[1]),(B[1],B[0])):
            row=list(range(n));row[s]=t;original.append(row)
    rows=[list(row) for row in sorted(set(map(tuple,original)))]
    def pre(S,row): return sum(1<<q for q in range(n) if S>>row[q]&1)
    edges={S:sorted({pre(S,row) for row in rows}) for S in range(1,1<<n)}
    e={};parents={};G={Q:0};W={Q:0}
    inverse_vertices=0
    for S in sorted(range(1,Q),key=int.bit_count,reverse=True):
        dist={S:0};queue=deque([S]);goals=set();best=None
        while queue:
            T=queue.popleft()
            if best is not None and dist[T]>=best:continue
            for U in edges[T]:
                if U in dist:continue
                dist[U]=dist[T]+1
                if U.bit_count()>S.bit_count():
                    assert U.bit_count()==S.bit_count()+1
                    best=dist[U] if best is None else best
                    if dist[U]==best:goals.add(U)
                elif U:queue.append(U)
        assert goals and best
        inverse_vertices+=len(dist)
        e[S]=best;parents[S]=sorted(goals)
        G[S]=best+min(G[T] for T in goals)
        W[S]=best+max(W[T] for T in goals)
    P=min(G[1<<q] for q in range(n));assert P==9
    def rank(sets):
        basis={}
        for S in sets:
            row=[Fraction(int(S>>q&1)) for q in range(n)]
            for pivot,base in sorted(basis.items()):
                if row[pivot]:
                    x=row[pivot];row=[a-x*b for a,b in zip(row,base)]
            p=next((p for p,x in enumerate(row) if x),None)
            if p is not None:
                x=row[p];basis[p]=[a/x for a in row]
        return len(basis)
    hist=Counter();chains=[]
    def visit(S,trace):
        if S==Q:
            proper=[T for T in trace if 1<T.bit_count()<n]
            value=rank(proper+[Q])-1
            hist[value]+=1
            chains.append(dict(sets=trace[:],phase_costs=[e[T] for T in trace[:-1]],
                               normalized_dimension=value,proper_stages=len(proper)))
            return
        for T in parents[S]:
            if e[S]+G[T]==G[S]:visit(T,trace+[T])
    for q in range(n):
        if G[1<<q]==P:visit(1<<q,[1<<q])
    return dict(status='COMPUTATIONAL finite certificate; independent forward/minor checker required',
                source='MAXIMAL_JUMP_LOG_HISTORY.md, d3 ONLY',n=n,d=d,
                original_labeled_rows=original,unique_induced_rows=rows,
                P=P,singleton_G=[G[1<<q] for q in range(n)],
                optimal_endpoint_histories=len(chains),normalized_dimension_histogram=dict(hist),
                minimum_normalized_dimension=min(hist),maximum_normalized_dimension=max(hist),
                optimal_chains=chains,inverse_vertices=inverse_vertices,
                extension=e,best=G,worst=W,parents=parents,
                boundary='endpoint chains, not all original word-label paths; finite only; no all-n dimension bound')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='direct_attack/data/optimal_log_history_n7.json')
    args=ap.parse_args()
    out=generate()
    Path(args.out).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:out[k] for k in ('n','P','optimal_endpoint_histories',
          'normalized_dimension_histogram','minimum_normalized_dimension','maximum_normalized_dimension')}))


if __name__=='__main__':main()
