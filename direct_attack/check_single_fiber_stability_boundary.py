"""Independent FULL monoids, forward subset graphs, and literal lifted rows."""
import argparse
from collections import deque
import copy
from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path

def digest(x):return sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def sc(rows):
    n=len(rows[0]);adj=[set() for _ in range(n)]
    for f in rows:
        for q,t in enumerate(f):adj[q].add(t)
    for q in range(n):
        seen={q};todo=[q]
        for p in todo:
            for t in adj[p]:
                if t not in seen:seen.add(t);todo.append(t)
        if len(seen)!=n:return False
    return True

def monoid(rows):
    identity=tuple(range(len(rows[0])));seen={identity};todo=deque([identity])
    while todo:
        h=todo.popleft()
        for f in rows:
            v=tuple(f[t] for t in h)
            if v not in seen:seen.add(v);todo.append(v)
    return seen

def partition(eq):
    n=len(eq);used=set();out=[]
    for q in range(n):
        if q in used:continue
        C=[t for t in range(n) if eq[q][t]];used.update(C);out.append(C)
    return out

def check_small(z):
    n=z['n'];maps=list(product(range(n),repeat=n));single=[]
    for f in maps:
        fibers={q:[p for p,t in enumerate(f) if t==q] for q in set(f)}
        if sum(len(C)>1 for C in fibers.values())==1:single.append(f)
    assert z['single_fiber_letters']==len(single) and z['all_labeled_binary_inputs']==len(single)*len(maps)
    h=sha256();count=transforms=minimum_controls=0;hist={}
    for f,b in product(single,maps):
        rows=[f,b]
        if not sc(rows):continue
        M=monoid(rows);transforms+=len(M);r=min(len(set(v)) for v in M)
        minima=[v for v in M if len(set(v))==r];minimum_controls+=len(minima)
        stable=[[all(v[p]==v[q] for v in minima) for q in range(n)] for p in range(n)]
        merge=[[any(v[p]==v[q] for v in M) for q in range(n)] for p in range(n)]
        assert stable==merge
        P=partition(stable);assert len(P)==r
        for v in minima:
            assert all((v[p]==v[q])==stable[p][q] for p,q in combinations(range(n),2))
        for p,q in combinations(range(n),2):assert f[p]!=f[q] or stable[p][q]
        assert all(not stable[p][q] or stable[row[p]][row[q]] for row in rows for p,q in combinations(range(n),2))
        count+=1;hist[r]=hist.get(r,0)+1
        h.update(json.dumps([f,b,P,r],separators=(',',':')).encode()+b'\n')
    assert z['strongly_connected']==count and z['semantic_sha256']==h.hexdigest()
    assert z['minimum_rank_histogram']=={str(k):v for k,v in hist.items()}
    return dict(n=n,all_labeled_binary_inputs=z['all_labeled_binary_inputs'],strongly_connected=count,
                full_original_transformations=transforms,all_minimum_rank_kernel_controls=minimum_controls)

def check_arbitrary(z):
    n=z['n'];maps=list(product(range(n),repeat=n));stream=sha256();count=transforms=prefix_controls=0
    for f,g in product(maps,repeat=2):
        M=monoid([f,g]);transforms+=len(M);r=min(len(set(v)) for v in M)
        minima=[v for v in M if len(set(v))==r]
        merge=[[any(v[p]==v[q] for v in M) for q in range(n)] for p in range(n)]
        stable=[[all(merge[v[p]][v[q]] for v in M) for q in range(n)] for p in range(n)]
        meet=[[all(v[p]==v[q] for v in minima) for q in range(n)] for p in range(n)]
        assert stable==meet
        prefix_controls+=len(M)*n*(n-1)//2;P=partition(stable);count+=1
        stream.update(json.dumps([f,g,P,r],separators=(',',':')).encode()+b'\n')
    assert count==z['all_labeled_binary_inputs'] and stream.hexdigest()==z['semantic_sha256']
    return dict(n=n,all_labeled_binary_inputs=count,full_original_transformations=transforms,
                all_original_prefix_pair_controls=prefix_controls)

def rows_from_lift(m):
    N=2*m;n=N+1;pi=list(range(N))+[m]
    F=list(range(N));F[0],F[m],F[1],F[m+1]=m,0,0,m
    G=[(i+1)%N for i in range(N)]
    f=[F[t] for t in pi];f[m+1]=N
    g=[G[t] for t in pi]
    return [f,g],pi,[F,G]

def literal(rows,word):
    h=list(range(len(rows[0])))
    for a in word:h=[rows[a][t] for t in h]
    return h

def orbit_can_merge(rows,P):
    seen={P};todo=[P]
    for p,q in todo:
        for f in rows:
            x,y=sorted((f[p],f[q]))
            if x==y:return True
            if (x,y) not in seen:seen.add((x,y));todo.append((x,y))
    return False

def orbit_reaches_deadlock(rows,P,dead):
    seen={P};todo=[P]
    for p,q in todo:
        if (p,q) in dead:return True
        for f in rows:
            x,y=sorted((f[p],f[q]))
            if x!=y and (x,y) not in seen:seen.add((x,y));todo.append((x,y))
    return False

def height_forest(row,roots):
    n=len(row);back=[[] for _ in range(n)]
    for q,t in enumerate(row):back[t].append(q)
    heights={q:0 for q in roots};targets={q:q for q in roots};todo=list(roots)
    for t in todo:
        for q in back[t]:
            if q not in heights:heights[q]=heights[t]+1;targets[q]=targets[t];todo.append(q)
    assert len(heights)==n
    return heights,targets

def check_family(z,deep=True):
    m=z['m'];N=2*m;n=N+1;rows,pi,quotient=rows_from_lift(m);f,g=rows
    assert z['n']==n and z['rows_sha256']==digest(rows) and z['ranks']==[len(set(row)) for row in rows]==[n-2,n-1]
    assert sc(rows)
    fibers_f=[C for t in set(f) if len(C:=[q for q in range(n) if f[q]==t])>1]
    fibers_g=[C for t in set(g) if len(C:=[q for q in range(n) if g[q]==t])>1]
    assert fibers_f==[z['kernel_f']]==[[1,m,N]] and fibers_g==[z['kernel_g']]==[[m,N]]
    assert all(pi[rows[a][q]]==quotient[a][pi[q]] for a in (0,1) for q in range(n))
    assert all(row[(q+m)%N]==(row[q]+m)%N for row in quotient for q in range(N))
    classes=[[q] for q in range(N) if q!=m]+[[m,N]];classes.sort(key=lambda C:C[0])
    assert z['stable_classes_sha256']==digest(classes)
    assert z['minimum_rank']==2 and z['minimum_rank_threshold']==2*m-2 and z['antipodal_block_reset_threshold']==2*m-3
    root=literal(rows,[0,1]);assert z['rooted_row_sha256']==digest(root)
    heights,targets=height_forest(root,[1,m+1]);assert max(heights.values())==z['root_heights_max']==m-1
    basins=[[q for q in range(n) if targets[q]==t] for t in (1,m+1)]
    assert z['basins_sha256']==digest(basins)
    word=[0,1]*(m-1);assert z['minimum_rank_word']==word and z['two_minimum_kernel_witnesses']==[word,[1]+word]
    assert targets[0]!=targets[1] and targets[g[0]]==targets[g[1]]
    expected_prefix=[1,0] if m==2 else [1]*(m-1)+[0]+[1]*(m+1)+[0]
    assert z['instability_prefix']==expected_prefix and z['unstable_kernel_pair']==[1,m]
    P=[1,m];particle_controls=0
    for a in expected_prefix:
        P=[rows[a][q] for q in P];particle_controls+=2
    assert sorted(P)==z['deadlock_result']==[0,N]
    assert (pi[P[0]]-pi[P[1]])%N==m
    assert z['deadlock_pair_count']==m+1 and z['least_group_quotient_classes']==1
    # Local distance steps cover every distance used in the all-pair paper proof.
    local=0
    for k in range(1,m-1):
        P=sorted((quotient[0][1],quotient[0][1+k]));assert P==[0,1+k];local+=2
    assert sorted((quotient[0][m],quotient[0][m+1]))==[0,m];local+=2
    if m>=3:assert sorted((quotient[0][m],quotient[0][N-1]))==[0,N-1];local+=2
    literal_controls=0
    if m<=24:
        h=literal(rows,word);k=literal(rows,[1]+word)
        assert h==[targets[q] for q in range(n)] and len(set(h))==len(set(k))==2
        assert h[0]!=h[1] and k[0]==k[1]
        literal_controls=n*(2*len(word)+1)
    out=dict(m=m,n=n,original_macro_controls=2*n,instability_particle_controls=particle_controls,
             literal_minimum_word_controls=literal_controls,local_quotient_distance_controls=local)
    if deep and m<=24:
        pairs=list(combinations(range(n),2));merge=[P for P in pairs if orbit_can_merge(rows,P)]
        expected=[P for P in pairs if (pi[P[0]]-pi[P[1]])%N!=m]
        assert merge==expected
        dead=set(pairs)-set(merge)
        stable=[P for P in pairs if not orbit_reaches_deadlock(rows,P,dead)]
        assert stable==[(m,N)]
        assert z['pair_relations_sha256']==digest([merge,stable]) and z['all_original_pairs']==len(pairs)
        out['all_forward_original_pair_orbits']=len(pairs)
        out['all_forward_original_stability_orbits']=len(pairs)
    if deep and m<=5:
        M=monoid(rows);r=min(len(set(v)) for v in M);minima=[v for v in M if len(set(v))==r];assert r==2
        all_stable=[P for P in combinations(range(n),2) if all(v[P[0]]==v[P[1]] for v in minima)]
        assert all_stable==[(m,N)]
        images={frozenset(range(n)):0};todo=deque(images)
        while todo:
            X=todo.popleft()
            for row in rows:
                Y=frozenset(row[q] for q in X)
                if Y not in images:images[Y]=images[X]+1;todo.append(Y)
        assert min(map(len,images))==2 and min(t for X,t in images.items() if len(X)==2)==2*m-2
        out.update(full_original_transformations=len(M),all_minimum_rank_transformations=len(minima),complete_forward_subset_vertices=len(images))
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,default=Path('direct_attack/data/single_fiber_stability_boundary.json'));ap.add_argument('--out',type=Path,default=Path('direct_attack/data/single_fiber_stability_boundary_checks.json'));args=ap.parse_args()
    data=json.loads(args.data.read_text(encoding='utf-8'));assert [z['n'] for z in data['small']]==[2,3,4]
    assert [z['n'] for z in data['arbitrary']]==[2,3]
    assert [z['m'] for z in data['family']]==list(range(2,65))+[100,128,256,512,1024]
    arbitrary=[check_arbitrary(z) for z in data['arbitrary']];small=[check_small(z) for z in data['small']];family=[check_family(z) for z in data['family']]
    corruptions=[]
    for field,value in [('ranks',[4,4]),('minimum_rank',1),('minimum_rank_threshold',1),('antipodal_block_reset_threshold',2),('kernel_f',[1,2]),('instability_prefix',[0]),('deadlock_result',[0,2]),('root_heights_max',2),('least_group_quotient_classes',2),('minimum_rank_word',[0])]:
        bad=copy.deepcopy(data['family'][0]);bad[field]=value
        try:check_family(bad,deep=False)
        except AssertionError:corruptions.append(field)
        else:raise AssertionError('accepted corruption '+field)
    out=dict(verified=True,arbitrary=arbitrary,small=small,family=family,corruptions_rejected=corruptions,
             totals=dict(arbitrary_inputs=sum(z['all_labeled_binary_inputs'] for z in arbitrary),
                         arbitrary_full_original_transformations=sum(z['full_original_transformations'] for z in arbitrary),
                         arbitrary_all_original_prefix_pair_controls=sum(z['all_original_prefix_pair_controls'] for z in arbitrary),
                         small_inputs=sum(z['all_labeled_binary_inputs'] for z in small),small_sc=sum(z['strongly_connected'] for z in small),
                         small_full_original_transformations=sum(z['full_original_transformations'] for z in small),
                         small_all_minimum_rank_kernel_controls=sum(z['all_minimum_rank_kernel_controls'] for z in small),
                         family_parameters=len(family),maximum_n=max(z['n'] for z in family),
                         original_macro_controls=sum(z['original_macro_controls'] for z in family),
                         instability_particle_controls=sum(z['instability_particle_controls'] for z in family),
                         literal_minimum_word_controls=sum(z['literal_minimum_word_controls'] for z in family),
                         local_quotient_distance_controls=sum(z['local_quotient_distance_controls'] for z in family),
                         all_forward_original_pair_orbits=sum(z.get('all_forward_original_pair_orbits',0) for z in family),
                         all_forward_original_stability_orbits=sum(z.get('all_forward_original_stability_orbits',0) for z in family),
                         family_full_original_transformations=sum(z.get('full_original_transformations',0) for z in family),
                         family_all_minimum_rank_transformations=sum(z.get('all_minimum_rank_transformations',0) for z in family),
                         complete_forward_subset_vertices=sum(z.get('complete_forward_subset_vertices',0) for z in family)),
             boundary='finite independent controls only; all-m family and ANY-alphabet n5 minimality paper proofs, not formalized; nonsynchronizing inputs are not Cerny counterexamples; priority and general Cerny OPEN')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(verified=True,**out['totals'],corruptions_rejected=len(corruptions),boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
