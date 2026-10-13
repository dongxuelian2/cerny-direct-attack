"""Independent integer row elimination, particle annular sums and subset word search."""
import argparse
from collections import deque
import copy
from itertools import product
import json,math
from pathlib import Path


def add_integer(v,B):
    v=list(v)
    for p,b in sorted(B.items()):
        if v[p]:
            c=v[p];v=[b[p]*x-c*y for x,y in zip(v,b)]
            g=0
            for x in v:g=math.gcd(g,abs(x))
            if g:v=[x//g for x in v]
    p=next((i for i,x in enumerate(v) if x),None)
    if p is None:return False
    g=0
    for x in v:g=math.gcd(g,abs(x))
    sign=1 if v[p]>0 else -1;B[p]=[sign*x//g for x in v];return True


def action(fs,word):
    image=list(range(len(fs[0])))
    for a in word:image=[fs[a][q] for q in image]
    return image


def particle(v,mapping):
    out=[0]*len(v)
    for q,x in enumerate(v):out[mapping[q]]+=x
    return out


def basis(vectors):
    out={}
    for v in vectors:add_integer(v,out)
    return out


def bounded_orbit(vectors,fs):
    n=len(fs[0]);powers=[action(fs,[0]*h) for h in range(n)]
    return basis(particle(v,tab) for v in vectors for tab in powers)


def shapes(fs):
    n=len(fs[0]);cycles=set();heights=[]
    for q in range(n):
        path=[];v=q
        while v not in path:path.append(v);v=fs[0][v]
        i=path.index(v);cycles.update(path[i:]);heights.append(i)
    start=next(iter(cycles));orbit={start};v=fs[0][start]
    while v!=start:orbit.add(v);v=fs[0][v]
    assert orbit==cycles
    return cycles,max(heights)


def compositions(total,k):
    if k==1:yield (total,);return
    for last in range(total,-1,-1):
        for prefix in compositions(total-last,k-1):yield prefix+(last,)


def audit_generators(u,fs,r,cap,suffix,target):
    B={};count=0
    for length in range(cap+1):
        for word in product(range(len(fs)),repeat=length):
            if sum(a!=0 for a in word)>r:continue
            count+=1;row=particle(u,action(fs,list(word)+[0]*suffix));add_integer(row,B)
    assert len(B)==target
    return count


def image_mask(fs,S,a):return sum(1<<q for q in {fs[a][p] for p in range(len(fs[0])) if S>>p&1})


def inverse_mask(fs,S,a):return sum(1<<p for p,q in enumerate(fs[a]) if S>>q&1)


def reset_distance(fs):
    n=len(fs[0]);todo=deque([(1<<n)-1]);dist={(1<<n)-1:0}
    while todo:
        S=todo.popleft()
        if S and not S&(S-1):return dist[S]
        for a in range(len(fs)):
            T=image_mask(fs,S,a)
            if T not in dist:dist[T]=dist[S]+1;todo.append(T)
    return None


def relative_extension(fs,C,ell,S):
    target=S
    for _ in range(ell):target=inverse_mask(fs,target,0)
    todo=deque([(target,[])]);seen={target}
    while todo:
        T,word=todo.popleft()
        if (T&C).bit_count()>S.bit_count():return word,T&C
        for a in range(len(fs)):
            U=inverse_mask(fs,T,a)
            if U not in seen:seen.add(U);todo.append((U,[a]+word))
    return None


def reset_certificate(fs,C,ell,m):
    n=len(fs[0]);todo=deque([(C,[])]);seen={C};start=None
    while todo:
        R,u=todo.popleft();projected=R
        for _ in range(ell):projected=image_mask(fs,projected,0)
        if projected.bit_count()<m:start=u;break
        for a in range(len(fs)):
            T=image_mask(fs,R,a)
            if T not in seen:seen.add(T);todo.append((T,u+[a]))
    assert start is not None and len(start)<=n-m+1
    w0=start+[0]*ell;mapping=action(fs,w0)
    q=next(q for q in range(m) if sum(mapping[p]==q for p in range(m))>1)
    S=sum(1<<p for p in range(m) if mapping[p]==q);word=w0;extensions=[]
    while S!=C:
        prefix,T=relative_extension(fs,C,ell,S);assert len(prefix)<=n
        factor=prefix+[0]*ell;word=factor+word;extensions.append(dict(S=S,prefix=prefix,T=T));S=T
    word=[0]*ell+word;assert action(fs,word)==[q]*n
    bound=(m-1)*(n-1)+m*ell;assert len(word)<=bound<=(n-1)**2
    return dict(endpoint=q,word=word,word_length=len(word),bound=bound,initial_prefix=start,extensions=extensions)


def audit_case(z):
    fs=z['rows'];n=len(fs[0]);C,ell=shapes(fs);m=len(C)
    assert C==set(range(m)) and z['m']==m>=2 and z['ell']==ell>=1 and ell<=n-m
    assert all(len(f)==n and all(0<=q<n for q in f) for f in fs)
    annular=terms=words=nontrivial=nonzero=proper_nonzero=0;expected_layers=[]
    for seed in range(1,len(fs)):
        u=[sum(fs[seed][p]==q for p in C)-(q in C) for q in range(n)]
        L=bounded_orbit([u],fs);previous={}
        for r in range(n):
            M=basis(particle(v,action(fs,[0]*ell)) for v in L.values());d=len(M);k=len(L)-d
            expected_layers.append(dict(seed=seed,r=r,dimension_L=len(L),d=d,k=k))
            if any(u):
                B17=d+k-1;words+=audit_generators(u,fs,r,B17,0,len(L))
                B18=d+ell*r+ell-1
                if B18<B17:words+=audit_generators(u,fs,r,B18,0,len(L))
                if d:words+=audit_generators(u,fs,r,d-1+min(k,ell*r),ell,d)
            if r:
                kap=min(n-m,ell*r);lo=max(0,kap-r);hi=m+kap-r-1
                for seq in product(range(1,len(fs)),repeat=r):
                    omega=[0]*n
                    for total in range(hi,lo-1,-1):
                        for h in compositions(total,r+1):
                            block=[0]*h[0]
                            for j,a in enumerate(seq):block+=[a]+[0]*(h[j+1]+(ell if j==r-1 else 0))
                            assert len(block)-ell+1<=n
                            row=particle(u,action(fs,block));omega=[a+b for a,b in zip(omega,row)];terms+=1
                    assert sum(omega)==0 and all(omega[q]==0 for q in range(m,n))
                    B={p:v[:] for p,v in previous.items()};assert not add_integer(omega,B)
                    annular+=1;nontrivial+=len(previous)<m-1
                    nonzero+=any(omega);proper_nonzero+=any(omega) and len(previous)<m-1
            previous=M
            if r<n-1:
                sources=list(L.values())+[particle(v,f) for v in L.values() for f in fs[1:]]
                L=bounded_orbit(sources,fs)
    assert z['layers']==expected_layers
    rt=reset_distance(fs);relative=[];certificate=None
    if rt is not None:
        mask=(1<<m)-1
        for S in range(1,mask):
            prefix,T=relative_extension(fs,mask,ell,S);assert len(prefix)<=n
            literal_map=action(fs,prefix+[0]*ell)
            assert T==sum(1<<p for p in range(m) if S>>literal_map[p]&1) and T.bit_count()>S.bit_count()
            relative.append(dict(S=S,prefix=prefix,T=T))
        certificate=reset_certificate(fs,mask,ell,m)
        assert rt<=certificate['word_length']
    return dict(case=z['case'],n=n,m=m,ell=ell,annular=annular,terms=terms,actual_words=words,nontrivial=nontrivial,
                nonzero_annular_sums=nonzero,proper_nonzero_memberships=proper_nonzero,
                reset_threshold=rt,all_proper_cycle_extensions=relative,reset_certificate=certificate)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,default=Path('scripts/direct_attack/data/one_cluster_annular_controls.json'));ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/one_cluster_annular_controls_checks.json'));args=ap.parse_args()
    data=json.loads(args.data.read_text(encoding='utf-8'));assert data['seed']==2026100202 and len(data['cases'])==16 and data['counter'] is None
    records=[audit_case(z) for z in data['cases']]
    for key,local in [('annular_controls','annular'),('annular_summands','terms'),('actual_word_controls','actual_words'),('nontrivial_memberships','nontrivial')]:assert data[key]==sum(z[local] for z in records)
    corruptions=[]
    for kind in range(3):
        z=copy.deepcopy(data['cases'][0])
        if kind==0:z['ell']+=1
        elif kind==1:z['layers'][0]['dimension_L']+=1
        else:z['rows'][0][0]=0
        try:audit_case(z)
        except AssertionError:corruptions.append(kind)
        else:raise AssertionError('accepted corruption')
    out=dict(verified=True,cases=records,annular_controls=sum(z['annular'] for z in records),annular_summands=sum(z['terms'] for z in records),actual_word_controls=sum(z['actual_words'] for z in records),
        nontrivial_memberships=sum(z['nontrivial'] for z in records),synchronizing_cases=sum(z['reset_threshold'] is not None for z in records),
        relative_extension_certificates=sum(len(z['all_proper_cycle_extensions']) for z in records),corruptions_rejected=corruptions,
        nonzero_annular_sums=sum(z['nonzero_annular_sums'] for z in records),proper_nonzero_memberships=sum(z['proper_nonzero_memberships'] for z in records),
        boundary='Independent exact finite fixed-seed mixed-control annular membership, actual-word generation bounds, complete cycle-subset extension and charged common reset certificates in16 retained inputs only. General one-cluster upper proof is separately reconstructed on paper, not formally verified or all-parameter computationally checked; source lower-bound section not audited; general Cerny OPEN.')
    assert out['proper_nonzero_memberships']>=2
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'}),flush=True)


if __name__=='__main__':main()
