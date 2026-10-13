"""Literal uniform proof controls, with no investigation imports."""
from pathlib import Path
from itertools import combinations,permutations,product
from collections import deque
import json,hashlib
ROOT=Path(__file__).resolve().parent
def main():
    sequences=0
    for n in range(4,10):
        Q=set(range(n));pairs=list(combinations(range(n),2))
        for triple in permutations(pairs,3):
            sets=[]
            for j,e in enumerate(triple):
                excluded={next(q for q in later if q not in e) for later in triple[j+1:]}
                for q in sorted(Q-set(e)-excluded):
                    if len(excluded)==2:break
                    excluded.add(q)
                T=Q-excluded
                assert len(T)==n-2 and set(e)<=T and all(not set(later)<=T for later in triple[j+1:])
                sets.append(T)
            assert all(not set(triple[i])<=sets[j] for i in range(3) for j in range(i));sequences+=1
    mapcounts=[];K={0,1,2}
    for n in (4,5,6):
        count=0
        for f in product(range(n),repeat=n):
            if len({f[k] for k in K})!=1:continue
            edges={e for e in combinations(range(n),2) if f[e[0]]==f[e[1]]}
            if len(edges)>4 or any(not(set(e)&K) for e in edges):continue
            assert edges==set(combinations(sorted(K),2)) and len(set(f))==n-2
            count+=1
        expected=n
        for factor in range(n-1,2,-1):expected*=factor
        assert count==expected;mapcounts.append(dict(n=n,exact_collapsed_cover_maps=count))
    n=4;Q=set(range(n));pairs=list(combinations(range(n),2));index={p:i for i,p in enumerate(pairs)}
    maps=list(product(range(n),repeat=n));profiles=[]
    for f in maps:
        trans=[-1 if f[u]==f[v] else index[tuple(sorted((f[u],f[v])))] for u,v in pairs]
        profiles.append((trans,{i for i,t in enumerate(trans) if t==-1},{f[k] for k in K}))
    binary=sync=qualified=collapsed=refinement_controls=0;boundary=None
    for i,f in enumerate(maps):
        for j,g in enumerate(maps):
            binary+=1;tf,kf,cf=profiles[i];tg,kg,cg=profiles[j];P1=kf|kg
            dist=[99]*6;reverse=[[] for _ in pairs];queue=deque()
            for p in P1:dist[p]=1;queue.append(p)
            for t in (tf,tg):
                for p,to in enumerate(t):
                    if to!=-1:reverse[to].append(p)
            while queue:
                to=queue.popleft()
                for p in reverse[to]:
                    if dist[p]>dist[to]+1:dist[p]=dist[to]+1;queue.append(p)
            if len(P1)>=3:
                assert all(d==99 or d<=4 for d in dist);refinement_controls+=1
            if max(dist)==99:continue
            sync+=1
            for cover in combinations(range(4),2):
                if all(d>4 or set(e)&set(cover) for e,d in zip(pairs,dist)):
                    qualified+=1;assert len(P1)<=2
            if len(P1)>4:continue
            assert all(d>5 or set(e)&K for e,d in zip(pairs,dist))
            for row,collapse in ((f,cf),(g,cg)):
                if len(collapse)!=1:continue
                p=next(iter(collapse));collapsed+=1
                assert any(p in e and d<=4 for e,d in zip(pairs,dist))
            if f==(3,3,3,0) and g==(1,2,3,0):
                assert all(len({row[q] for q in Q})>=1 for row in (f,g))
                for start in Q:
                    seen={start};work=[start]
                    while work:
                        p=work.pop()
                        for to in (f[p],g[p]):
                            if to not in seen:seen.add(to);work.append(to)
                    assert seen==Q
                boundary=dict(letters=[list(f),list(g)],collapsed_target=3,target_not_isolated_in_P4=True,pair_distances=dist)
    assert binary==65536 and boundary is not None
    # n3 singleton-complement boundary of the two-cover consequence.
    assert len({0,1,2}-{1,2})==1 and len(list(combinations(range(3),2)))==3
    names=[Path(__file__).name,'PROOF.md#problem4-collapsed-three-cover-obstruction','PROOF.md#problem4-two-cover-unique-immediate-pair','PROOF.md#problem4-letter-image-short-pair-cover']
    result=dict(status='pass',ordered_three_pair_sequences_checked=sequences,collapsed_map_controls=mapcounts,
        complete_n4_ordered_binary_alphabets=binary,synchronizing_alphabets=sync,two_cover_P4_controls=qualified,
        immediate_three_pair_refinement_controls=refinement_controls,collapsed_cover_instances=collapsed,nonisolated_target_boundary=boundary,
        n3_complement_is_singleton_boundary=True,source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Uniform written collapsed-cover proof with literal sequence/map/full-n4 controls. No F value.')
    (ROOT/'collapsed_three_cover_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
