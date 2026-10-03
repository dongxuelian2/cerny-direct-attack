"""All-length monotone inverse cut and lexicographic shrink-count certificate."""
from collections import deque
from heapq import heappop,heappush
import json
from pathlib import Path
from direct_attack.almost_circular_returns import distances

ROWS=[[4,4,2,3,1,5],[1,5,3,4,2,0]]

def pred(S,f):return sum(1<<q for q in range(6) if S>>f[q]&1)

def main():
    R={1<<q:dict(q=q,word=[]) for q in range(6)};queue=deque(R)
    while queue:
        S=queue.popleft()
        for i,f in enumerate(ROWS):
            T=pred(S,f)
            if T.bit_count()>=S.bit_count() and T not in R:
                R[T]=dict(q=R[S]['q'],word=[i]+R[S]['word']);queue.append(T)
    assert len(R)==35 and 63 not in R
    reverse=[[] for _ in range(64)]
    for S in range(64):
        for i,f in enumerate(ROWS):
            T=pred(S,f);reverse[T].append((S,i,int(T.bit_count()<S.bit_count())))
    d=[None]*64;d[63]=(0,0);heap=[(0,0,63)]
    while heap:
        shrink,cost,T=heappop(heap)
        if d[T]!=(shrink,cost):continue
        for S,i,c in reverse[T]:
            z=(shrink+c,cost+1)
            if d[S] is None or z<d[S]:d[S]=z;heappush(heap,(*z,S))
    value,q=min((d[1<<q],q) for q in range(6));S=1<<q;word=[]
    while S!=63:
        for i,f in enumerate(ROWS):
            T=pred(S,f);c=int(T.bit_count()<S.bit_count())
            if d[T] is not None and d[S]==(d[T][0]+c,d[T][1]+1):word=[i]+word;S=T;break
    assert value==(1,25) and q==4
    out=dict(rows=ROWS,cut=sorted(R),reach_witnesses=[dict(S=S,**R[S]) for S in sorted(R)],
             lex_distances=d,target=q,word=word,original_distances=distances(ROWS,[1,1]),
             boundary='Retained literal Kari n6. Every original reset needs an inverse cardinality decrease at some intermediate letter; no monotone inverse reset exists at ANY length. Minimum shrink count1 is attained by an optimal original cost25 reset. Exact finite graph certificates and a separate Lean all-word cut proof; no general Cerny proof or novelty claim.')
    Path('direct_attack/data/kari_inverse_shrink.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cut=sorted(R),reachable=len(R),max_monotone_size=max(S.bit_count() for S in R),singleton_lex=[d[1<<q] for q in range(6)],target=q,word=word,inverse_processing=list(reversed(word)),boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
