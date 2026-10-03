"""Exact minimum rank-area over ALL reset words, with Bellman/word certificates."""
from heapq import heappop,heappush
import json
from pathlib import Path
from direct_attack.core import graph


def certificate(rows):
    n=len(rows[0]);Q=(1<<n)-1;g=graph(rows);R=[Q];seen={Q}
    for S in R:
        for T in g[S]:
            if T not in seen:seen.add(T);R.append(T)
    r=max(S.bit_count() for S in R if S!=Q)
    weight=lambda S:max(0,r-max(2,S.bit_count())+1)
    d={Q:(0,0)};parent={};heap=[(0,0,Q)]
    while heap:
        area,ell,S=heappop(heap)
        if d[S]!=(area,ell):continue
        for x,T in enumerate(g[S]):
            v=(area+weight(T),ell+1)
            if T not in d or v<d[T]:d[T]=v;parent[T]=(S,x);heappush(heap,(*v,T))
    goals=[S for S in R if S.bit_count()==1];assert goals
    goal=min(goals,key=lambda S:(*d[S],S));word=[];S=goal
    while S!=Q:S,x=parent[S];word.append(x)
    word.reverse()
    base=2+(r-1)*n-r*(r+1)//2
    return dict(n=n,rows=rows,r=r,reachable=len(R),area=d[goal][0],length=d[goal][1],word=word,
                budget=base+d[goal][0],nodes={S:dict(area=d[S][0],length=d[S][1],parent=parent.get(S)) for S in sorted(R)})


def main():
    root=Path('direct_attack/data/circular_rank_area');root.mkdir(exist_ok=True);records=[]
    for n in range(2,15):
        a=[(q+1)%n for q in range(n)];b=list(range(n));b[-1]=0;c=certificate([a,b])
        c.update(formula_status='Exact minimum-area formula is COMPUTATIONALLY VERIFIED only; paper proves matching cubic leading term and failure of every trajectory budget for all n>=3.')
        assert c['area']==(n-2)*(n*(n-1)//2+1) and c['length']==(n-1)**2
        name=f'n{n}.json';(root/name).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
        records.append(dict(file=name,n=n,area=c['area'],budget=c['budget'],length=c['length'],R=c['reachable']))
    (root/'summary.json').write_text(json.dumps(dict(records=records),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),vertices=sum(x['R'] for x in records),records=records)),flush=True)


if __name__=='__main__':main()
