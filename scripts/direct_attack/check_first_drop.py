"""Independent all-source ordinary-set audit of rank-boundary and singleton formulas."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path
import random
import time
from direct_attack.mine import inputs,maps
from direct_attack.native_sparse_policy import profile


def verify(rows,p):
    n=len(rows[0]);Q=frozenset(range(n));R=[Q];index={Q:0};edges=[]
    for T in R:
        children=[]
        for row in rows:
            U=frozenset(row[q] for q in T)
            if U not in index:index[U]=len(R);R.append(U)
            children.append(index[U])
        edges.append(children)
    distances=[]
    for i in range(len(R)):
        d=[-1]*len(R);d[i]=0;queue=deque([i])
        while queue:
            j=queue.popleft()
            for t in edges[j]:
                if d[t]<0:d[t]=d[j]+1;queue.append(t)
        distances.append(d)
    e={};G={0:0};W={0:0};first_letters=0;winning_sources=0
    for si in sorted(range(1,len(R)),key=lambda i:len(R[i]),reverse=True):
        S=R[si];k=len(S);contained=[i for i,U in enumerate(R) if U<=S]
        into=[min((d[j] for j in contained if d[j]>=0),default=10**9) for d in distances]
        ecost=min(into[i] for i,T in enumerate(R) if len(T)>k)
        winners={i for i,T in enumerate(R) if len(T)>k and into[i]==ecost}
        boundary={}
        for i,T in enumerate(R):
            if len(T)<=k:continue
            for j in edges[i]:
                if len(R[j])<=k:boundary.setdefault(j,set()).add(i)
        assert ecost==1+min(into[j] for j in boundary)
        boundary_winners=set().union(*(parents for j,parents in boundary.items() if into[j]==ecost-1))
        assert boundary_winners==winners
        for i in winners:
            for j in edges[i]:
                if into[j]==ecost-1:assert len(R[j])<=k;first_letters+=1
        winning_sources+=len(winners);e[si]=ecost;G[si]=ecost+min(G[i] for i in winners);W[si]=ecost+max(W[i] for i in winners)
    mask=lambda T:sum(1<<q for q in T)
    assert p['extension']=={mask(R[i]):v for i,v in e.items()}
    assert p['best']=={mask(R[i]):v for i,v in G.items()} and p['worst']=={mask(R[i]):v for i,v in W.items()}
    merged={i for i,T in enumerate(R) if len(T)>1 and any(len(R[j])==1 for j in edges[i])}
    H={next(iter(R[j])) for i in merged for j in edges[i] if len(R[j])==1};assert H
    state_dist=[]
    for q in range(n):
        d={q:0};queue=deque([q])
        while queue:
            r=queue.popleft()
            for row in rows:
                if row[r] not in d:d[row[r]]=d[r]+1;queue.append(row[r])
        assert len(d)==n;state_dist.append(d)
    for q in range(n):
        d=min(state_dist[h][q] for h in H);nearest=[h for h in H if state_dist[h][q]==d];qi=index[frozenset([q])]
        assert e[qi]==1+d
        assert G[qi]==d+min(G[index[frozenset([h])]] for h in nearest)
        assert W[qi]==d+max(W[index[frozenset([h])]] for h in nearest)
    kappa=max(len(R[i]) for i in merged);metrics=dict(kappa=kappa,seed_best=1+min(G[i] for i in merged),
        anchor_best=1+min(G[i] for i in merged if len(R[i])==kappa),anchor_worst=1+max(W[i] for i in merged if len(R[i])==kappa))
    assert metrics['seed_best']==min(G[index[frozenset([q])]] for q in range(n))==p['best_policy']
    L=min(distances[0][index[frozenset([q])]] for q in range(n));assert L==p['rt']
    r=max(len(T) for T in R if T!=Q)
    bound=1+sum(L+n-k for k in range(2,r+1))
    for si,cost in e.items():assert cost<=L+n-len(R[si])
    # Select a shortest reset path with a small rank area on its BFS level DAG.
    areas={0:0};pred={}
    for i in sorted(range(len(R)),key=lambda i:distances[0][i]):
        if i not in areas or distances[0][i]>=L:continue
        for x,j in enumerate(edges[i]):
            if distances[0][j]!=distances[0][i]+1:continue
            v=areas[i]+max(0,r-max(2,len(R[j]))+1)
            if j not in areas or v<areas[j]:areas[j]=v;pred[j]=(i,x)
    goal=min((i for i,T in enumerate(R) if len(T)==1 and distances[0][i]==L),key=lambda i:(areas[i],i))
    word=[];i=goal
    while i:i,x=pred[i];word.append(x)
    word.reverse();assert len(word)==L
    image=0;ranks=[n]
    for x in word:image=edges[image][x];ranks.append(len(R[image]))
    assert image==goal and ranks[-1]==1
    tails={k:L-max(t for t,v in enumerate(ranks) if v>k) for k in range(1,r+1)}
    rank_bound=1+sum(tails[k]+n-k for k in range(2,r+1))
    area=sum(max(0,r-max(2,v)+1) for v in ranks[1:])
    assert area==areas[goal]==sum(tails[k] for k in range(2,r+1))
    assert rank_bound==2+(r-1)*n-r*(r+1)//2+area and rank_bound<=bound
    for si,cost in e.items():assert cost<=tails[len(R[si])]+n-len(R[si])
    for h in H:
        assert W[index[frozenset([h])]]<=bound
        assert W[index[frozenset([h])]]<=rank_bound
        if 2*L<=n+1:assert W[index[frozenset([h])]]<=(n-1)**2
        if rank_bound<=(n-1)**2:assert W[index[frozenset([h])]]<=(n-1)**2
    m=profile(rows,seed_budget=True);assert m is not None and not m['truncated']
    for key,v in metrics.items():assert m[key]==v
    for key,budget in [('seed_image','seed_best'),('anchor_image','anchor_best')]:
        i=index[frozenset(q for q in range(n) if m[key]>>q&1)];assert i in merged and G[i]+1==m[budget]
        if key=='anchor_image':assert len(R[i])==kappa
    return dict(images=len(R),proper_images=len(e),winning_sources=winning_sources,shortest_first_letters=first_letters,
                budget_seed_targets=len(H),short_reset_budget_cases=int(2*L<=n+1),
                rank_profile_square_cases=int(rank_bound<=(n-1)**2),
                rank_profile_extra_square_cases=int(2*L>n+1 and rank_bound<=(n-1)**2),
                rank_profile_improved_bounds=int(rank_bound<bound),
                rank_profile_new_vs_rank_budget=int(rank_bound<=(n-1)**2<bound),
                rank_profile_witness=dict(rows=rows,n=n,rt=L,r=r,word=word,ranks=ranks,tails=tails,area=area,
                                          bound=rank_bound,old_rank_bound=bound,max_seed_worst=max(W[index[frozenset([h])]] for h in H)),**metrics)


def main():
    started=time.monotonic();counts=dict(tested=0,accepted=0,rejected=0,proper_images=0,winning_sources=0,shortest_first_letters=0,
                                        budget_seed_targets=0,short_reset_budget_cases=0,rank_profile_square_cases=0,
                                        rank_profile_extra_square_cases=0,rank_profile_improved_bounds=0,
                                        rank_profile_new_vs_rank_budget=0);seen=set();extra=[]
    def check(rows):
        key=tuple(map(tuple,rows))
        if key in seen:return
        seen.add(key);counts['tested']+=1;p=profile(rows,True)
        if p is None:assert profile(rows,seed_budget=True) is None;counts['rejected']+=1;return
        assert not p['truncated'];r=verify(rows,p);counts['accepted']+=1
        for k in ['proper_images','winning_sources','shortest_first_letters','budget_seed_targets','short_reset_budget_cases',
                  'rank_profile_square_cases','rank_profile_extra_square_cases','rank_profile_improved_bounds',
                  'rank_profile_new_vs_rank_budget']:counts[k]+=r[k]
        if r['rank_profile_new_vs_rank_budget'] and len(extra)<12:extra.append(r['rank_profile_witness'])
    for n in [2,3,4]:
        for rows in inputs(n,'first-map-orbits',0,0,2):check(rows)
    for rows in combinations(maps(3),3):check(rows)
    for path in sorted(Path('scripts/direct_attack/data').rglob('*.json')):
        c=json.loads(path.read_text(encoding='utf-8'));rows=c.get('rows') if isinstance(c,dict) else None
        if not rows or not all(isinstance(row,list) and row and all(type(q)==int for q in row) for row in rows):continue
        if 2<=len(rows[0])<=8 and all(len(row)==len(rows[0]) for row in rows):check(rows)
    rng=random.Random(20261021)
    for n in [6,8,10,12]:
        for _ in range(20):check([[rng.randrange(n) for q in range(n)] for a in range(3)])
    assert profile([[0,1,2,0],[1,2,3,0]],seed_budget=True,limit=2)['truncated']
    assert profile([[0,1,2,0],[1,2,3,0]],seed_budget=True)['seed_best']==9
    report=dict(verified=True,counts=counts,seconds=time.monotonic()-started,protocol_limit_recovery=True,
                boundary='Each accepted case independently recomputes every e/G/W entry, exact rt and every winning source with ordinary ALL-SOURCE distances; first-letter condition, complete boundary-parent equality, singleton formulas, reset-length-dependent and reset-rank-profile-dependent all-seed budgets checked. Each rank budget uses an explicitly reconstructed shortest reset word. Computational scope is finite; universal results are paper proofs.')
    Path('scripts/direct_attack/data/rank_profile_budget_cases.json').write_text(json.dumps(dict(verified=True,counts=counts,witnesses=extra),indent=2)+'\n',encoding='utf-8')
    Path('scripts/direct_attack/data/first_drop_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':main()
