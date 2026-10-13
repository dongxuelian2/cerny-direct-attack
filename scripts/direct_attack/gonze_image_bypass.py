"""Reconstruct the published quadratic exact-reaching family and certify rank-skipping into-images."""
from pathlib import Path
import json
from direct_attack.native_sparse_policy import profile as native

ROOT=Path('scripts/direct_attack/data/gonze_bypass')

def rows_for(n):
    assert n>=7 and n%4==3
    a=[1,2,3,0,6,5,4];b=[5,1,4,3,2,0,6]
    while len(a)<n:
        old=len(a)
        for row in [a,b]:
            row.extend([old,old+1])
            for q in [old-2,old-1]:
                if row[q]==q:row[q],row[q+2]=q+2,q
    c=list(range(n));c[1]=2;c[3]=0
    return [a,b,c]

def apply(rows,T,word):
    for i in word:T={rows[i][q] for q in T}
    return T

def certificate(n):
    rows=rows_for(n);m=(n-3)//4;k=(n-5)//2;Q=set(range(n));S=Q-{k+1,k+3}
    word=[2,0]+[1,0]*m+[2]+[i%2 for i in range(m)]
    assert len(word)==3*(n+1)//4 and apply(rows,Q,word)<=S
    trajectory=[sorted(Q)];T=Q
    for i in word:T={rows[i][q] for q in T};trajectory.append(sorted(T))
    assert len(T)==n-4
    final=sorted(T)
    # Exact rank n-2 BFS retains only that closed rank range, independently of into-image search.
    full=frozenset(Q);goal=frozenset(S);paths={full:[]};queue=[full]
    for T in queue:
        if T==goal:break
        for i,row in enumerate(rows):
            U=frozenset(row[q] for q in T)
            if len(U)>=n-2 and U not in paths:paths[U]=paths[T]+[i];queue.append(U)
    exact=paths[goal];published=(n*n+5*n)//4-6;assert len(exact)==published
    # Construct an ordinary inverse-growing reset, with no reachability assumption on intermediate preimages.
    inverse_set={0};reset=[];phases=[]
    while len(inverse_set)<n:
        for j in range(n):
            w=[2]+[0,1]*j
            U={q for q in Q if next(iter(apply(rows,{q},w))) in inverse_set}
            if len(U)>len(inverse_set):break
        else:raise AssertionError('Missing ordinary extension')
        phases.append(dict(target=sorted(inverse_set),word=w,preimage=sorted(U)))
        inverse_set=U;reset=w+reset
    assert apply(rows,Q,reset)=={0}
    explicit=([2,0,1,0,1]*(m+2))+([2,0,1]*(2*m-1))+[2]
    assert reset==explicit and len(reset)==(11*n-1)//4
    return dict(n=n,rows=rows,target=sorted(S),exact_reaching=published,exact_word=exact,
                bypass_word=word,bypass_length=len(word),bypass_target=final,
                bypass_trajectory=trajectory,reset_word=reset,ordinary_inverse_phases=phases)

def main():
    ROOT.mkdir(exist_ok=True);cases=[];arrays=[]
    for n in list(range(7,40,4))+[63,103]:
        c=certificate(n);cases.append(c)
        if n<=11:
            z=native(c['rows'],True);mask=sum(1<<q for q in c['target'])
            assert z['extension'][mask]==c['bypass_length'];arrays.append(z)
    for name,value in [('cases',cases),('small_arrays',arrays)]:
        (ROOT/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    summary=dict(verified=True,states=[c['n'] for c in cases],source='Gonze--Jungers2018 Prop2, arXiv1805.02540; permutation recursion arXiv1704.04047 page13',
                 all_n_claim='Explicit into-image word <=3(n+1)/4 for n>=7,n=3 mod4; published quadratic exact reach does NOT refute actual-image e<=2n.',
                 exact_into_formula='Finite only; no all-n shortest into-image formula asserted.')
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
