"""Exact sharp avoid-or-compress examples; original words are fully charged."""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path


def construct(n, r, gap):
    if gap == 1:
        L=n-r
        assert 1<=r<n
        a=[min(q+1,L) if q<L else q for q in range(n)]
        core=[0]+list(range(L,n));b=[L]*n
        for i,q in enumerate(core):b[q]=core[(i+1)%len(core)]
        A=sum(1<<q for q in core[1:]);S=A|1
        h=[0]*L;t=[1];initial=[];loops=r-1;power=r
        reset_length=r*L+r*(r-1)
        attaining=[0]*L
    else:
        assert gap==2 and 1<=r<=n-3
        M=n-r;a=list(range(n));b=list(range(n))
        for q in range(r-1):b[q]=q+1
        b[r-1]=r
        for j in range(1,M+1):
            q=r+j-1
            a[q]=r+(j%M) if M%2 else (r+1 if j in (1,M) else q+1)
            b[q]=0 if (j%2==M%2) else r+1
        if M%2==0:b[r]=r+1
        A=(1<<r)-1;S=(1<<(r+2))-1
        h=[0]*(M-1)+[1];t=[0,1] if M%2 else [1]
        initial=[1];loops=r;power=r
        reset_length=1+(r+1)*M+r*r*len(t)
        attaining=h
    return [a,b],S,A,dict(initial=initial,h=h,t=t,power=power,loops=loops),reset_length,attaining


def move(mask,row):
    out=0
    while mask:
        bit=mask&-mask;out|=1<<row[bit.bit_length()-1];mask-=bit
    return out


def bfs(rows,S,A=None):
    todo=deque([S]);distance={S:0};parent={}
    size=S.bit_count()
    while todo:
        T=todo.popleft()
        if (A is None and T.bit_count()==1) or (A is not None and (T.bit_count()<size or T&A!=A)):
            word=[];U=T
            while U!=S:
                U,a=parent[U];word.append(a)
            return distance[T],word[::-1],len(distance)
        for i,row in enumerate(rows):
            U=move(T,row)
            if U not in distance:distance[U]=distance[T]+1;parent[U]=(T,i);todo.append(U)
    raise AssertionError('target unreachable')


def flatten(program):
    return program['initial']+program['h']+(program['t']*program['power']+program['h'])*program['loops']


def record(n,r,gap):
    rows,S,A,program,length,attaining=construct(n,r,gap)
    d,w,vertices=bfs(rows,S,A);assert d==n-r
    z=dict(n=n,A_size=r,gap=gap,S=S,A=A,rows_sha256=sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest(),
           explicit_rows=rows if n<=40 else None,reachable_word=[1],ac=d,first_success_word=w,
           attaining_word=attaining,avoid_compress_vertices=vertices,reset_program=program,reset_length=length,
           literal_reset_word=flatten(program) if length<=5000 else None)
    if n<=10:
        rt,rw,v=bfs(rows,(1<<n)-1);z['finite_exact_reset']=dict(rt=rt,word=rw,vertices=v)
    else:z['finite_exact_reset']=None
    return z


def parameters():
    scopes={(n,r,gap) for n in range(2,19) for gap in (1,2) for r in range(1,n-gap+1)}
    scopes={p for p in scopes if p[2]==1 or p[1]<=p[0]-3}
    for n in (30,64,129,257,513,1025):
        for r in sorted({1,2,3,5,8,n//3,n//2,n-3,n-2,n-1}):
            for gap in (1,2):
                if r<=n-(1 if gap==1 else 3):scopes.add((n,r,gap))
    return sorted(scopes)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/avoid_compress_sharp_faces.json'))
    args=ap.parse_args();records=[record(*p) for p in parameters()]
    out=dict(records=records,status='PROVED paper sharp first two cardinality faces; COMPUTATIONALLY VERIFIED only finite scopes; priority OPEN; no formal kernel; general Cerny OPEN')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(parameters=len(records),maximum_n=max(z['n'] for z in records),finite_reset_scopes=sum(z['finite_exact_reset'] is not None for z in records))),flush=True)


if __name__=='__main__':main()
