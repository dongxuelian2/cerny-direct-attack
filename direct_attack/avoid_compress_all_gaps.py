"""General modular timer for all fixed avoid-or-compress cardinality gaps."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from direct_attack.avoid_compress_sharp_faces import bfs


def construct(r,g,k):
    assert r>=1 and g>=2 and k>=2
    M=k*g+1;n=r+M+1;p=r+1;a=list(range(n));b=list(range(n));b[0]=p
    for q in range(1,p):b[q]=q-1
    for j in range(1,M+1):
        q=p+j-1;a[q]=p+j%M
        b[q]=r if j%g==0 else (p+j if j<M else p+g)
    return [a,b]


def record(r,g,k):
    rs=construct(r,g,k);M=k*g+1;n=r+M+1;s=r+g+1;S=(1<<s)-1;A=(1<<r)-1
    ac,w,vertices=bfs(rs,S,A);assert ac==M+1
    c=[0]*(M-1)+[1]*s;v=c*g+[1];length=g+1+(r+1)*len(v)
    z=dict(n=n,A_size=r,g=g,k=k,M=M,S=S,A=A,ac=ac,
           rows_sha256=sha256(json.dumps(rs,separators=(',',':')).encode()).hexdigest(),explicit_rows=rs if n<=40 else None,
           first_success_word=w,attaining_word=[0]*(M-1)+[1,1],avoid_compress_vertices=vertices,
           reachable_word=[1]*(g+1),macro_c=c,rooted_word=v,root=r+1,rooted_height=r+1,
           reset_length=length,literal_reset_word=([1]*(g+1)+v*(r+1) if length<=5000 else None))
    if n<=12:
        rt,rw,q=bfs(rs,(1<<n)-1);z['finite_exact_reset']=dict(rt=rt,word=rw,vertices=q)
    else:z['finite_exact_reset']=None
    return z


def parameters():
    scopes={(r,g,k) for g in range(3,9) for k in (2,3) for r in (1,2,5)}
    scopes|={(1,g,2) for g in (9,10,11)}
    scopes|={(n-(2*g+2),g,2) for n in (257,513,1025) for g in (3,5,8)}
    return sorted(scopes,key=lambda p:(p[0]+p[1]*p[2]+2,p[1],p[0]))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('direct_attack/data/avoid_compress_all_gaps.json'))
    args=ap.parse_args();records=[record(*p) for p in parameters()]
    out=dict(records=records,status='PROVED paper r>=1 g>=2 k>=2: exact ac=n-|A| for EVERY fixed cardinality gap along infinite state-count progression; existing upper bound attributed; general pointwise cardinality problem and Cerny OPEN; no formal kernel')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(parameters=len(records),maximum_n=max(z['n'] for z in records),maximum_g=max(z['g'] for z in records),finite_reset_scopes=sum(z['finite_exact_reset'] is not None for z in records))),flush=True)


if __name__=='__main__':main()
