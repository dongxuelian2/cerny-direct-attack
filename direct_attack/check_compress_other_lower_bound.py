"""Independent inverse-fiber edges, exact entry lists and ordinary pair BFS."""
import argparse
from collections import deque
import copy
from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path


def digest(value):return sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def rows(p):
    n=3*p;a=list(range(n));b=list(range(n))
    for q in range(1,2*p,2):a[q],a[q+1]=q+1,q
    for q in range(0,2*p,2):b[q],b[q+1]=q+1,q
    a[2*p]=2*p+1;a[2*p+1]=3;b[2*p]=2
    for q in range(2*p+2,n-1,2):a[q],a[q+1]=q+1,q
    for q in range(2*p+1,n-1,2):b[q],b[q+1]=q+1,q
    return [a,b]


def layers(p):
    C={(x,2*p+1-x) for x in range(1,p+1)}
    A={(x,2*p-1+x) for x in range(2,p+1)}
    E={(h,4*p-h) for h in range(p+1,2*p)}
    B={(x,2*p-3+x) for x in range(4,p+3)}
    F={(h+2,4*p-h) for h in range(p+1,2*p-1)}
    return C,A|E,B|F


def bad(pair,p):return pair[1]<=2*p and sum(pair)%2==1 and sum(pair)>2*p+1 and pair!=(3,2*p)


def word_row(rs,w):
    row=list(range(len(rs[0])))
    for a in w:row=[rs[a][q] for q in row]
    return row


def pair_computations(rs):
    n=len(rs[0]);union=set();minimum=None
    for partner in range(1,n):
        seed=(0,partner);ds={seed:0};todo=deque([seed])
        while todo:
            P=todo.popleft()
            if P[0]==P[1]:minimum=min(minimum,ds[P]) if minimum is not None else ds[P]
            for a in rs:
                T=tuple(sorted((a[P[0]],a[P[1]])))
                if T not in ds:ds[T]=ds[P]+1;todo.append(T)
        union.update(ds)
    pairs=list(combinations(range(n),2));pred={P:[] for P in pairs};distance={};todo=deque()
    for P in pairs:
        for a in rs:
            T=tuple(sorted(a[q] for q in P))
            if T[0]==T[1]:
                if P not in distance:distance[P]=1;todo.append(P)
            else:pred[T].append(P)
    while todo:
        P=todo.popleft()
        for T in pred[P]:
            if T not in distance:distance[T]=distance[P]+1;todo.append(T)
    assert min(distance[0,q] for q in range(1,n))==minimum
    return dict(minimum=minimum,reachable_pairs=len(union),distinct_pairs=sum(q!=t for q,t in union))


def verify(z):
    p=z['p'];n=3*p;assert p>=3 and n==z['n'];rs=rows(p);C,H,U=layers(p);K=(3,2*p);L=(4,2*p+1)
    assert z['rows_sha256']==digest(rs)
    assert z['layer_hashes']=={key:digest(sorted(S)) for key,S in zip(('C','H','U'),(C,H,U))}
    assert z['layer_sizes']=={key:len(S) for key,S in zip(('C','H','U'),(C,H,U))}
    assert not C&H and not H&U and not C&U and L in U
    for f in rs:assert len(set(f))==n-1 and all(t<=q+1 for q,t in enumerate(f))
    kernels=[{P for P in combinations(range(n),2) if f[P[0]]==f[P[1]]} for f in rs]
    assert kernels==[{L},{K}]
    assert all((0,q) not in C|H|U and not bad((0,q),p) for q in range(1,n))
    counts={key:0 for key in ('controls','C_targets','H_targets','U_entries','K_entries')}
    outsideC=set();outsideH=set();outsideU=set();intoK=set()
    fibers=[[[q for q,t in enumerate(f) if t==v] for v in range(n)] for f in rs]
    # Inverse-fiber enumeration visits every noncollapsing original edge exactly once.
    for target in combinations(range(n),2):
        for a,f in enumerate(fibers):
            for q in f[target[0]]:
                for t in f[target[1]]:
                    source=tuple(sorted((q,t)))
                    if bad(source,p):continue
                    assert not bad(target,p)
                    if target in C:
                        need=2*p-2+abs(target[0]-3)
                        available=2*p-2+abs(source[0]-3) if source in C else min(source)
                        assert available+1>=need;counts['C_targets']+=1
                        if source not in C:outsideC.add((a,source,target))
                    if target in H:
                        need=2*p-1+target[0]
                        available=2*p-1+source[0] if source in H else 2*p-2+abs(source[0]-3) if source in C else min(source)
                        assert available+1>=need;counts['H_targets']+=1
                        if source not in H:outsideH.add((a,source,target))
                    if target in U and source not in U:
                        assert source==K;counts['U_entries']+=1;outsideU.add((a,source,target))
                    if target==K:
                        assert source in H and 2*p-1+source[0]>=4*p-2
                        counts['K_entries']+=1;intoK.add((a,source,target))
                    counts['controls']+=1
    assert outsideC=={(0,(2*p-3,2*p+1),(3,2*p-2)),(1,(2*p-2,2*p),(2,2*p-1))}
    expectedH={(0,(1,2*p),(2,2*p+1)),(1,(2*p,2*p+2),(2,2*p+1))}
    if p>=4:expectedH.add((0,(2*p+1,2*p+3),(3,2*p+2)))
    else:expectedH.add((0,(7,8),(3,8)))
    assert outsideH==expectedH,(p,sorted(outsideH-expectedH),sorted(expectedH-outsideH))
    assert intoK=={(0,(2*p-1,2*p+1),K)} and outsideU=={(0,K,L)}
    assert counts==z['transition_counts'] and counts['controls']==8*p*p-2*p
    assert z['lower_bound']==4*p and z['upper_partner']==2 and z['upper_endpoint']==2
    w=z['upper_word'];assert w==[1,0]*p+[0,1]*p
    current=[0,z['upper_partner']]
    for a in w:current=[rs[a][q] for q in current]
    assert current==[2,2]
    extra={}
    if p<=12:
        result=pair_computations(rs);assert result==z['small_forward_star'] and result['minimum']==4*p
        extra=result
    else:assert z['small_forward_star'] is None
    return dict(p=p,n=n,pair_edge_controls=counts['controls'],literal_upper_state_letter_controls=2*len(w),small_pair_computations=extra)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('direct_attack/data/compress_other_lower_bound.json'))
    ap.add_argument('--out',type=Path,default=Path('direct_attack/data/compress_other_lower_bound_checks.json'));args=ap.parse_args();data=json.loads(args.source.read_text())
    assert [z['p'] for z in data['records']]==list(range(3,65))+[100,128,256,512,1024]
    reports=[verify(z) for z in data['records']]
    rs=rows(3);literal=0
    for length in range(1,12):
        for w in product(range(2),repeat=length):
            f=word_row(rs,w);assert f.count(f[0])==1;literal+=1
    assert literal==4094
    mutations=[];base=data['records'][0]
    for key,value in [('lower_bound',11),('rows_sha256','0'*64),('upper_partner',1),('upper_endpoint',0),('upper_word',[0]*12)]:
        z=copy.deepcopy(base);z[key]=value;mutations.append(z)
    z=copy.deepcopy(base);z['layer_hashes']['H']='0'*64;mutations.append(z)
    z=copy.deepcopy(base);z['layer_sizes']['U']+=1;mutations.append(z)
    z=copy.deepcopy(base);z['transition_counts']['K_entries']+=1;mutations.append(z)
    z=copy.deepcopy(base);z['transition_counts']['controls']-=1;mutations.append(z)
    z=copy.deepcopy(base);z['small_forward_star']['minimum']-=1;mutations.append(z)
    for z in mutations:
        try:verify(z)
        except AssertionError:pass
        else:raise AssertionError('corruption accepted')
    out=dict(verified=True,parameters=len(reports),maximum_n=max(z['n'] for z in reports),pair_edge_controls=sum(z['pair_edge_controls'] for z in reports),
             literal_upper_state_letter_controls=sum(z['literal_upper_state_letter_controls'] for z in reports),small_forward_and_reverse_scopes=sum(bool(z['small_pair_computations']) for z in reports),
             literal_n9_words_below_lower_bound=literal,corruptions_rejected=len(mutations),reports=reports,
             boundary='PROVED paper EVERY p>=3, n3p: exact specified-state mu0=4p, general layered directed-pair lower certificate. Only recorded finite scopes COMPUTATIONALLY VERIFIED; prior actual square reset unchanged, ordinary all-n rt and general Cerny OPEN, priority OPEN, no formal kernel')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='reports'}),flush=True)


if __name__=='__main__':main()
