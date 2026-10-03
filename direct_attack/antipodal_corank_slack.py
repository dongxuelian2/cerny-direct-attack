"""Circular corank-one family requiring neutral singular steps."""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path

def rows(m):
    assert m>=3
    n=2*m;a=[(q+1)%n for q in range(n)];f=list(range(n))
    f[0],f[1],f[2],f[m],f[m+1]=1,m,m+1,2,m
    return [a,f]

def digest(rs):return sha256(json.dumps(rs,separators=(',',':')).encode()).hexdigest()

def ordinary(rs):
    n=len(rs[0]);Q=(1<<n)-1;images=[]
    for row in rs:
        im=[0]*(Q+1)
        for S in range(1,Q+1):
            b=S&-S;im[S]=im[S^b]|(1<<row[b.bit_length()-1])
        images.append(im)
    todo=deque([Q]);prev={Q:None};end=None
    while todo:
        S=todo.popleft()
        if S&(S-1)==0:end=S;break
        for i,im in enumerate(images):
            T=im[S]
            if T not in prev:prev[T]=(S,i);todo.append(T)
    assert end is not None
    word=[];T=end
    while prev[T] is not None:T,i=prev[T];word.append(i)
    return len(word),word[::-1]

def minimum_singular(rs):
    # Generator quotients by the zero-cost cycle; the checker uses full
    # ordinary subsets and 0/1 BFS instead.
    n=len(rs[0]);Q=(1<<n)-1
    def rotate(S):return ((S<<1)&Q)|(S>>(n-1))
    lookup=[-1]*(Q+1);lookup[0]=0
    for S in range(1,Q+1):
        if lookup[S]>=0:continue
        orbit=[];T=S
        while T not in orbit:orbit.append(T);T=rotate(T)
        c=min(orbit)
        for T in orbit:lookup[T]=c
    im=[0]*(Q+1)
    for S in range(1,Q+1):
        b=S&-S;im[S]=im[S^b]|(1<<rs[1][b.bit_length()-1])
    todo=deque([Q]);prev={Q:None};end=None
    while todo:
        S=todo.popleft()
        if S&(S-1)==0:end=S;break
        T=S
        for k in range(n):
            U=lookup[im[T]]
            if U not in prev:prev[U]=(S,k,im[T]);todo.append(U)
            T=rotate(T)
    pieces=[];T=end
    while prev[T] is not None:
        S,k,V=prev[T];j=0
        while V!=T:V=rotate(V);j+=1
        pieces.append([0]*k+[1]+[0]*j);T=S
    return dict(minimum_f=len(pieces),original_word=sum(pieces[::-1],[]),visited_necklaces=len(prev))

def record(m):
    rs=rows(m);n=2*m
    g=[(rs[1][rs[1][q]]+m-1)%n for q in range(n)]
    heights=[]
    for q in range(n):
        seen=set();t=0
        while q!=m+1:
            assert q not in seen;seen.add(q);q=g[q];t+=1
        heights.append(t)
    H=max(heights);assert H==(4 if m==3 else 2*m-3)
    z=dict(m=m,n=n,rows_sha256=digest(rs),explicit_rows=rs if m<=9 else None,
           excluded=0,duplicate=m,kernel_pair=[1,m+1],
           minimum_required_f_lower=n if m==3 else n+1,
           required_corank_slack_lower=1 if m==3 else 2,
           original_rooted_macro=[1,1]+[0]*(m-1),root=m+1,
           rooted_height=H,reset_length=(m+1)*H,
           square_slack=(n-1)**2-(m+1)*H,
           simple=True,strongly_connected=True,paper_parameter_scope='EVERY odd m>=3')
    if m<=9:
        rt,w=ordinary(rs);z['finite_exact_rt']=rt;z['finite_shortest_word']=w
        z['finite_minimum_f']=minimum_singular(rs)
    return z

def generate():
    parameters=list(range(3,66,2))+[101,257,513,1025]
    return dict(status='PROVED paper: forced neutral singular steps and explicit rooted square reset; no formal verification',
                records=[record(m) for m in parameters],
                finite_exact_parameters=[3,5,7,9],
                conjecture='minimum f=n+1 for every odd m>=5; upper only finite m5/7/9',
                boundary='general Cerny and a slack-aware length bound OPEN; no growing-slack theorem')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('direct_attack/data/antipodal_corank_slack.json'))
    args=ap.parse_args();z=generate();args.out.write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(records=len(z['records']),maximum_n=max(r['n'] for r in z['records']),finite_exact_parameters=z['finite_exact_parameters'])),flush=True)

if __name__=='__main__':main()
