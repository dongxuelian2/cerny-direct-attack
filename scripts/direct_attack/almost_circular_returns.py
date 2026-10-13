"""Complete finite normal-form controls and paid return Bellman certificates."""
import heapq,json
from itertools import permutations
from pathlib import Path

def act(rows,w,domain=None):
    f=list(range(len(rows[0]))) if domain is None else list(domain)
    for letter in w:f=[rows[letter][q] for q in f]
    return f

def image(S,f):return sum(1<<p for p in {f[q] for q in range(len(f)) if S>>q&1})

def distances(rows,costs):
    n=len(rows[0]);reverse=[[] for _ in range(1<<n)]
    for S in range(1<<n):
        for f,cost in zip(rows,costs):reverse[image(S,f)].append((S,cost))
    d=[None]*(1<<n);heap=[]
    for S in range(1<<n):
        if S.bit_count()<=1:d[S]=0;heap.append((0,S))
    heapq.heapify(heap)
    while heap:
        value,T=heapq.heappop(heap)
        if value!=d[T]:continue
        for S,cost in reverse[T]:
            x=value+cost
            if d[S] is None or x<d[S]:d[S]=x;heapq.heappush(heap,(x,S))
    return d

def witness(rows,costs,d):
    S=(1<<len(rows[0]))-1;word=[]
    if d[S] is None:return None
    while S.bit_count()>1:
        for i,(f,cost) in enumerate(zip(rows,costs)):
            T=image(S,f)
            if d[T] is not None and d[S]==cost+d[T]:word.append(i);S=T;break
        else:raise AssertionError('missing shortest edge')
    return word

def record(A):
    M=len(A);n=M+1;abar=[0]+list(A);inv=[abar.index(q) for q in range(n)]
    a=[A[0]]+list(A);b=[(inv[q]+1)%n for q in range(n)];rows=[a,b]
    ret=[[q-1 for q in act(rows,w,range(1,n))] for w in ([1,0],[1,1,0])]
    original=distances(rows,[1,1]);returned=distances(ret,[2,3]);assert (original[-1] is None)==(returned[-1] is None)
    return dict(n=n,A=list(A),rows=rows,return_rows=ret,original_costs=original,return_costs=returned,
                return_word=witness(ret,[2,3],returned))

def main():
    records=[record(A) for n in range(3,8) for A in permutations(range(1,n))]
    fs=[[0,1,2,4,3,3],[1,3,5,0,2,4]];S=list(range(5))
    returned=[act(fs,w,S) for w in ([1,0],[1,1,0])];extra=[act(fs,[0],S)]+returned
    dc=distances(returned,[2,3]);de=distances(extra,[1,2,3]);do=distances(fs,[1,1])
    assert (do[-1],dc[-1],de[-1])==(25,25,24)
    counter=dict(rows=fs,entered_set=S,return_rows=returned,extra_rows=extra,original_costs=do,return_costs=dc,extra_costs=de,
                 return_word=witness(returned,[2,3],dc),extra_word=witness(extra,[1,2,3],de))
    out=dict(records=records,counter=counter,boundary='All872 finite normal-form permutations n3..7 and one retained paid n6 obstruction. Paper all-n c/f synchronization equivalence PROVED separately; c/f-only entered cost26 exceeds square25, adding A enters at25. No general paid square theorem or formal proof; Cerny OPEN.')
    Path('scripts/direct_attack/data/almost_circular_returns.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),sync=sum(z['original_costs'][-1] is not None for z in records),cf_only_square_failures=sum(z['return_costs'][-1] is not None and z['return_costs'][-1]+1>(z['n']-1)**2 for z in records),counter_costs=[do[-1],dc[-1],de[-1]],boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
