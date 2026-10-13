"""Independent literal rows, weighted preimages, image BFS and routing audit.

No obstruction generator or earlier solver is imported.
"""
from collections import deque
from copy import deepcopy
from itertools import product
from pathlib import Path
import json


def swap_row(n,x,y):
    row=list(range(n));row[x],row[y]=row[y],row[x]
    return row


def literal(rows,word):
    values=list(range(len(rows[0])))
    for a in word:values=[rows[a][q] for q in values]
    return values


def interval_permutation(n,lo,hi):
    # Evaluate EACH original transposition, tracking inverse positions.
    row=list(range(n));inv=list(range(n));charged=0
    for i in range(lo,hi):
        x,y=inv[i],inv[i+1]
        row[x],row[y]=row[y],row[x]
        inv[i],inv[i+1]=y,x
        charged+=1
    assert all(row[inv[q]]==q for q in range(n))
    return row,charged


def check_record(z):
    r,n=z['r'],z['n'];assert r>=1 and n==2*r
    fold=[q if q<r else q-r for q in range(n)]
    edges=[[q,q+1] for q in range(n-1)]
    assert z['fold_row']==fold and z['transposition_edges']==edges
    assert z['target']==list(range(r,n)) and z['source']==list(range(n))
    assert z['only_larger_actual_image_is_Q'] is True and len(set(fold))==r
    weights=z['inverse_potential_weights']
    assert weights==[max(r+1-q,0) for q in range(n)]
    # For EVERY subset, each inverse step increases the potential by <=1.
    assert max(abs(weights[i]-weights[i+1]) for i in range(n-1))<=1
    pull=[0]*n
    for q in range(n):pull[fold[q]]+=weights[q]
    delta=[pull[q]-weights[q] for q in range(n)]
    assert delta==[int(q==0)-int(q==r) for q in range(n)]
    assert sum(max(x,0) for x in delta)==1
    full=sum(weights);target=sum(weights[q] for q in z['target'])
    assert full-max(weights)==z['rt']==r*(r+1)//2
    assert full-target==z['image_extension']==r*(r+3)//2
    # Whole common-word evaluation, via efficient exact rows for the blocks.
    S=set(fold);stages=[len(S)];word_cost,b_count,swap_cost=1,1,0
    for j in range(r-1,0,-1):
        row,cost=interval_permutation(n,j,r)
        S={fold[row[q]] for q in S}
        stages.append(len(S));word_cost+=cost+1;b_count+=1;swap_cost+=cost
    assert S=={z['reset_endpoint']}=={0}
    assert stages==z['reset_stage_ranks']==list(range(r,0,-1))
    assert b_count==z['reset_b_count']==r and swap_cost==z['reset_swap_count']==r*(r-1)//2
    assert word_cost==z['rt']
    row,cost=interval_permutation(n,0,r)
    assert {row[q] for q in S}=={z['entering_endpoint']}=={r}
    assert word_cost+cost==z['image_extension']
    # The alleged target really is an ACTUAL Q-image; count all r^2 swaps.
    S=set(fold);target_cost=1
    for j in range(r-1,-1,-1):
        row,cost=interval_permutation(n,j,j+r)
        S={row[q] for q in S};target_cost+=cost
    assert S==set(z['target']) and target_cost==z['reachable_target_word_length']==r*r+1
    if r<=24:
        rows=[swap_row(n,i,i+1) for i in range(n-1)]+[fold]
        w=z['literal_reset_word'];v=z['literal_entering_word'];t=z['literal_reachable_target_word']
        assert len(w)==word_cost and set(literal(rows,w))=={0}
        assert len(v)==z['image_extension'] and set(literal(rows,v))=={r}
        assert len(t)==target_cost and set(literal(rows,t))==set(z['target'])
    return dict(r=r,n=n,reset=word_cost,image_extension=z['image_extension'],potential_all_subsets=True)


def exact_images(r):
    n=2*r;full=(1<<n)-1;left=(1<<r)-1;right=full^left
    dist={full:0};parent={};todo=deque([full])
    while todo:
        S=todo.popleft()
        for a in range(n):
            if a==n-1:T=(S&left)|(S>>r)
            else:T=S^(3<<a) if ((S>>a)^(S>>(a+1)))&1 else S
            if T not in dist:dist[T]=dist[S]+1;parent[T]=(S,a);todo.append(T)
    rt=min(d for S,d in dist.items() if S&(S-1)==0)
    entering=min(d for S,d in dist.items() if S&~right==0)
    assert right in dist and rt==r*(r+1)//2 and entering==r*(r+3)//2
    assert all(S==full or S.bit_count()<=r for S in dist)
    # Independent reverse-target BFS, using full preimages and allowing shrink.
    rd={right:0};todo=deque([right]);rparent={}
    while todo:
        S=todo.popleft()
        if S==full:break
        for a in range(n):
            if a==n-1:T=(S&left)|((S&left)<<r)
            else:T=S^(3<<a) if ((S>>a)^(S>>(a+1)))&1 else S
            if T and T not in rd:rd[T]=rd[S]+1;rparent[T]=(S,a);todo.append(T)
    assert rd[full]==entering
    endpoint=min((S for S in dist if S&~right==0),key=dist.get)
    witness=[];S=endpoint
    while S!=full:S,a=parent[S];witness.append(a)
    witness.reverse()
    rows=[swap_row(n,i,i+1) for i in range(n-1)]+[[q%r for q in range(n)]]
    assert set(literal(rows,witness))<=set(range(r,n)) and len(witness)==entering
    return dict(r=r,n=n,rt=rt,image_extension=entering,forward_vertices=len(dist),reverse_vertices=len(rd),entering_word=witness)


def path(adj,start,accept):
    previous={start:None};todo=deque([start])
    while todo:
        q=todo.popleft()
        if accept(q):
            result=[]
            while q is not None:result.append(q);q=previous[q]
            return result[::-1]
        for t in adj[q]:
            if t not in previous:previous[t]=q;todo.append(t)
    raise AssertionError('disconnected graph')


def routing(adj,S,i,j):
    # Produce original edge transpositions with i outside and j inside.
    S=set(S);word=[]
    def apply(x,y):
        if (x in S)!=(y in S):
            if x in S:S.remove(x);S.add(y)
            else:S.remove(y);S.add(x)
        word.append((x,y))
    if i not in S and j in S:return S,word
    if (i in S)==(j in S):
        start=i if i in S else j;desired=i not in S
        P=path(adj,start,lambda q:(q in S)==desired)
        for k in range(len(P)-2,-1,-1):apply(P[k],P[k+1])
    else:
        P=path(adj,i,lambda q:q==j)
        f=next(k for k,q in enumerate(P) if q not in S)
        for k in range(f-1,-1,-1):apply(P[k],P[k+1])
        if j in S:
            assert i not in S
            return S,word
        last=max(k for k,q in enumerate(P) if q in S)
        assert last>=f and last<len(P)-1
        for k in range(last,len(P)-1):apply(P[k],P[k+1])
    assert i not in S and j in S
    return S,word


def contain_pair(adj,S,p,q):
    """Original edge word costing <=2 holes, using a small two-token tree."""
    occupied=set(S);word=[];P=path(adj,p,lambda v:v==q)
    def apply(x,y):
        if (x in occupied)!=(y in occupied):
            if x in occupied:occupied.remove(x);occupied.add(y)
            else:occupied.remove(y);occupied.add(x)
        word.append((x,y))
    positions=[i for i,v in enumerate(P) if v in occupied]
    if len(positions)>=2:
        first,last=positions[0],positions[-1]
        for i in range(first-1,-1,-1):apply(P[i],P[i+1])
        for i in range(last,len(P)-1):apply(P[i],P[i+1])
    else:
        V=set(P);tree={v:[] for v in P}
        for x,y in zip(P,P[1:]):tree[x].append(y);tree[y].append(x)
        frontier=deque(P);tokens=len(positions)
        while tokens<2:
            v=frontier.popleft()
            for t in adj[v]:
                if t in V:continue
                V.add(t);tree[t]=[v];tree[v].append(t);frontier.append(t)
                tokens+=int(t in occupied)
                if tokens==2:break
        initial_size=len(V);assert len(occupied&V)==2
        active=set(V);target={p,q}
        while len(active)>1:
            leaf=next(v for v in sorted(active) if sum(t in active for t in tree[v])==1)
            if (leaf in occupied)!=(leaf in target):
                subadj=[[] for _ in adj]
                for v in active:subadj[v]=[t for t in tree[v] if t in active]
                desired=leaf not in occupied
                walk=path(subadj,leaf,lambda v:(v in occupied)==desired)
                for i in range(len(walk)-2,-1,-1):apply(walk[i],walk[i+1])
            assert (leaf in occupied)==(leaf in target)
            active.remove(leaf)
        assert (next(iter(active)) in occupied)==(next(iter(active)) in target)
        assert len(word)<=2*(initial_size-2)
    assert p in occupied and q in occupied and len(word)<=2*(len(adj)-len(S))
    return occupied,word


def graph_routing_audit():
    graphs=routes=exact_vertices=automata=pair_routes=general_automata=0
    by_n=[]
    for n in range(2,6):
        E=[(i,j) for i in range(n) for j in range(i+1,n)]
        ng=nr=na=npair=ngeneral=0
        rank_one_defect=[]
        if n<=4:
            rank_one_defect=[list(row) for row in product(range(n),repeat=n) if len(set(row))==n-1]
        for mask in range(1<<len(E)):
            edges=[e for k,e in enumerate(E) if mask>>k&1]
            adj=[[] for _ in range(n)]
            for x,y in edges:adj[x].append(y);adj[y].append(x)
            seen={0};todo=deque([0])
            while todo:
                for t in adj[todo.popleft()]:
                    if t not in seen:seen.add(t);todo.append(t)
            if len(seen)!=n:continue
            graphs+=1;ng+=1
            full=(1<<n)-1
            for i in range(n):
                for j in range(n):
                    if i==j:continue
                    D=len(path(adj,i,lambda q:q==j))-1
                    # Multi-source BFS gives the independently exact routing cost.
                    dist={S:0 for S in range(1,full) if not (S>>i&1) and S>>j&1};todo=deque(dist)
                    while todo:
                        S=todo.popleft()
                        for x,y in edges:
                            T=S^((1<<x)|(1<<y)) if ((S>>x)^(S>>y))&1 else S
                            if T not in dist:dist[T]=dist[S]+1;todo.append(T)
                    assert len(dist)==full-1;exact_vertices+=len(dist)
                    for S in range(1,full):
                        source={q for q in range(n) if S>>q&1};T,word=routing(adj,source,i,j)
                        bound=max(len(source),n-len(source),D)
                        assert dist[S]<=len(word)<=bound<=n-1
                        values=source
                        for x,y in word:values={y if q==x else x if q==y else q for q in values}
                        assert values==T
                        routes+=1;nr+=1
            # All labeled rank n-1 rows through n4: build an actual common reset.
            for b in rank_one_defect:
                counts=[b.count(q) for q in range(n)]
                duplicate=counts.index(2);missing=counts.index(0)
                S={q for q in range(n) if b[q]==duplicate};W=[len(edges)]
                while len(S)<n:
                    moved,g=routing(adj,S,missing,duplicate)
                    inverse=[edges.index(tuple(sorted(e))) for e in g[::-1]]
                    u=[len(edges)]+inverse
                    rows=[swap_row(n,*edge) for edge in edges]+[b]
                    row=literal(rows,u);T={q for q in range(n) if row[q] in S}
                    assert len(T)==len(S)+1 and {row[q] for q in T}==S
                    W=u+W;S=T
                rows=[swap_row(n,*edge) for edge in edges]+[b]
                assert len(W)<=(n-1)**2 and len(set(literal(rows,W)))==1
                automata+=1;na+=1
            for p in range(n):
                for q in range(p+1,n):
                    dist={S:0 for S in range(1,full+1) if S>>p&1 and S>>q&1};todo=deque(dist)
                    while todo:
                        S=todo.popleft()
                        for x,y in edges:
                            T=S^((1<<x)|(1<<y)) if ((S>>x)^(S>>y))&1 else S
                            if T not in dist:dist[T]=dist[S]+1;todo.append(T)
                    for S in range(1,full+1):
                        if S.bit_count()<2:continue
                        source={v for v in range(n) if S>>v&1};T,g=contain_pair(adj,source,p,q)
                        assert dist[S]<=len(g)<=2*(n-len(source))
                        pair_routes+=1;npair+=1
            if n<=4:
                for b in product(range(n),repeat=n):
                    rank=len(set(b))
                    if rank==n:continue
                    p,q=next((p,q) for p in range(n) for q in range(p+1,n) if b[p]==b[q])
                    S=set(b);W=[len(edges)]
                    while len(S)>1:
                        old=len(S);T,g=contain_pair(adj,S,p,q)
                        W.extend(edges.index(tuple(sorted(e))) for e in g);W.append(len(edges))
                        S={b[v] for v in T}
                        assert len(S)<old and len(g)+1<=2*(n-old)+1
                    rows=[swap_row(n,*edge) for edge in edges]+[list(b)]
                    assert len(W)<=1+(rank-1)*(2*n-rank-1)<=(n-1)**2
                    assert len(set(literal(rows,W)))==1
                    general_automata+=1;ngeneral+=1
        by_n.append(dict(n=n,connected_graphs=ng,routing_cases=nr,labeled_defect_one_automata=na,
                         containing_pair_cases=npair,labeled_general_singular_automata=ngeneral))
    return dict(connected_graphs=graphs,routing_cases=routes,exact_routing_vertices=exact_vertices,
                labeled_defect_one_automata=automata,containing_pair_cases=pair_routes,
                labeled_general_singular_automata=general_automata,by_n=by_n)


def main():
    data=Path('scripts/direct_attack/data');source=json.loads((data/'transposition_fold_obstruction.json').read_text())
    records=source['records'];assert [z['r'] for z in records]==list(range(1,65))+[100,128,256,512,1024]
    controls=[check_record(z) for z in records]
    exact=[exact_images(r) for r in range(1,10)]
    corruptions=[]
    base=next(z for z in records if z['r']==6)
    for field in ('rt','image_extension','fold_row','inverse_potential_weights','reset_stage_ranks','literal_entering_word'):
        z=deepcopy(base)
        if isinstance(z[field],int):z[field]-=1
        elif field=='literal_entering_word':z[field].pop()
        elif field=='fold_row':z[field][0]=1
        else:z[field][0]-=1
        try:check_record(z)
        except AssertionError:corruptions.append(field)
        else:raise AssertionError('accepted corrupted '+field)
    routing_report=graph_routing_audit()
    report=dict(verified=True,controls=controls,exact_image_scopes=exact,corruptions_rejected=corruptions,
                routing=routing_report,
                status='PROVED paper family and connected-transposition square for any singular letter, with sharper defect-one inverse routing; bounded independent audits COMPUTATIONALLY VERIFIED; every universal linear actual-image extension bound REFUTED; general Cerny OPEN; no formal verification')
    (data/'transposition_fold_obstruction_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,family_controls=len(controls),maximum_n=2048,exact_scopes=len(exact),
                          forward_vertices=sum(z['forward_vertices'] for z in exact),reverse_vertices=sum(z['reverse_vertices'] for z in exact),
                          corruptions_rejected=len(corruptions),routing=routing_report)),flush=True)


if __name__=='__main__':main()
