"""Original-pair controls for a sharp failure of whole single-fiber stability."""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

def digest(x):
    return sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def sc(rows):
    n=len(rows[0]);back=[[] for _ in range(n)]
    for f in rows:
        for q,t in enumerate(f):back[t].append(q)
    for rev in (False,True):
        seen={0};todo=[0]
        for q in todo:
            for t in back[q] if rev else [f[q] for f in rows]:
                if t not in seen:seen.add(t);todo.append(t)
        if len(seen)!=n:return False
    return True

def pair_relations(rows):
    n=len(rows[0]);pairs=list(combinations(range(n),2));pred={P:[] for P in pairs};good=set()
    for P in pairs:
        for f in rows:
            T=tuple(sorted(f[q] for q in P))
            if T[0]==T[1]:good.add(P)
            else:pred[T].append(P)
    todo=list(good)
    for P in todo:
        for T in pred[P]:
            if T not in good:good.add(T);todo.append(T)
    dead=set(pairs)-good;todo=list(dead)
    for P in todo:
        for T in pred[P]:
            if T not in dead:dead.add(T);todo.append(T)
    return sorted(good),sorted(set(pairs)-dead)

def blocks(n,eq):
    parent=list(range(n))
    def root(q):
        while parent[q]!=q:q=parent[q]
        return q
    for p,q in eq:parent[root(p)]=root(q)
    return sorted(sorted(q for q in range(n) if root(q)==r) for r in {root(q) for q in range(n)})

def small(n):
    maps=list(product(range(n),repeat=n));single=[]
    for f in maps:
        nontrivial=[sum(t==q for t in f) for q in set(f) if sum(t==q for t in f)>1]
        if len(nontrivial)==1:single.append(f)
    h=sha256();count=0;hist={}
    for f,b in product(single,maps):
        rows=[f,b]
        if not sc(rows):continue
        merge,stable=pair_relations(rows);assert merge==stable
        P=blocks(n,stable);assert set(stable)==set(Pair for C in P for Pair in combinations(C,2))
        assert all((p,q) in stable for p,q in combinations(range(n),2) if f[p]==f[q])
        r=len(P);count+=1;hist[r]=hist.get(r,0)+1
        h.update(json.dumps([f,b,P,r],separators=(',',':')).encode()+b'\n')
    return dict(n=n,all_labeled_binary_inputs=len(single)*len(maps),single_fiber_letters=len(single),strongly_connected=count,
                minimum_rank_histogram={str(k):v for k,v in hist.items()},semantic_sha256=h.hexdigest())

def arbitrary_scope(n):
    maps=list(product(range(n),repeat=n));stream=sha256();count=0
    for f,g in product(maps,repeat=2):
        rows=[f,g];_,stable=pair_relations(rows);P=blocks(n,stable)
        images={frozenset(range(n))};todo=list(images)
        for X in todo:
            for row in rows:
                Y=frozenset(row[q] for q in X)
                if Y not in images:images.add(Y);todo.append(Y)
        r=min(map(len,images));count+=1
        stream.update(json.dumps([f,g,P,r],separators=(',',':')).encode()+b'\n')
    return dict(n=n,all_labeled_binary_inputs=count,semantic_sha256=stream.hexdigest())

def original_rows(m):
    N=2*m;n=N+1;f=list(range(n));f[0]=m;f[1]=f[m]=f[N]=0;f[m+1]=N
    g=list(range(1,N))+[0,m+1]
    return [f,g]

def apply_pair(P,rows,word):
    for a in word:P=tuple(sorted(rows[a][q] for q in P))
    return P

def family(m):
    rows=original_rows(m);N=2*m;n=N+1;assert sc(rows)
    f,g=rows;root=[g[f[q]] for q in range(n)];word=[0,1]*(m-1)
    basins=[list(range(1,m+1))+[N],[0]+list(range(m+1,N))]
    assert [root[q] for q in (1,m+1)]==[1,m+1]
    instability=[1,0] if m==2 else [1]*(m-1)+[0]+[1]*(m+1)+[0]
    assert apply_pair((1,m),rows,instability)==(0,N)
    z=dict(m=m,n=n,rows_sha256=digest(rows),ranks=[n-2,n-1],kernel_f=[1,m,N],kernel_g=[m,N],
           stable_classes_sha256=digest(blocks(n,[(m,N)])),minimum_rank=2,minimum_rank_word=word,minimum_rank_threshold=2*m-2,
           rooted_row_sha256=digest(root),root_heights_max=m-1,basins_sha256=digest(basins),unstable_kernel_pair=[1,m],
           instability_prefix=instability,deadlock_result=[0,N],deadlock_pair_count=m+1,least_group_quotient_classes=1,
           two_minimum_kernel_witnesses=[word,[1]+word],antipodal_block_reset_threshold=2*m-3)
    if m<=24:
        merge,stable=pair_relations(rows);assert stable==[(m,N)]
        dead=[P for P in combinations(range(n),2) if P not in set(merge)]
        assert len(dead)==m+1
        z['pair_relations_sha256']=digest([merge,stable]);z['all_original_pairs']=n*(n-1)//2
    return z

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('direct_attack/data/single_fiber_stability_boundary.json'));args=ap.parse_args()
    out=dict(arbitrary=[arbitrary_scope(n) for n in (2,3)],small=[small(n) for n in (2,3,4)],family=[family(m) for m in list(range(2,65))+[100,128,256,512,1024]],
             boundary='REFUTED paper whole single-fiber kernel stability, EVERY odd n>=5 binary SC ranks n-2/n-1. State-minimal n5 over ANY finite alphabet by paper proof. Minimum rank2, exact minimum-rank-word length n-3, stable double class only, universal least permutation quotient. These inputs are nonsynchronizing, not Cerny counterexamples. Priority and general Cerny OPEN; finite independent controls only, no formal claim.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(small_inputs=sum(z['all_labeled_binary_inputs'] for z in out['small']),small_sc=sum(z['strongly_connected'] for z in out['small']),family=len(out['family']),maximum_n=max(z['n'] for z in out['family']),boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
