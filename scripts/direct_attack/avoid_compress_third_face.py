"""Third cardinality face: a permutation and a one-cluster singular letter."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from direct_attack.avoid_compress_sharp_faces import bfs,move


def construct(r,M):
    assert r>=1 and M>=5 and M%2
    p=r+1;n=p+M;a=list(range(n));b=list(range(n));b[0]=p
    for q in range(1,p):b[q]=q-1
    for j in range(1,M+1):
        q=p+j-1;a[q]=p+j%M
        b[q]=(p+j if j<M else p+2) if j%2 else r
    return [a,b]


def record(r,M):
    rs=construct(r,M);n=r+M+1;s=r+3;S=(1<<s)-1;A=(1<<r)-1
    ac,w,vertices=bfs(rs,S,A);assert ac==M+1
    c=[0]*(M-1)+[1]*s;v=c+c+[1];height=r+1
    z=dict(n=n,A_size=r,M=M,S=S,A=A,ac=ac,rows_sha256=sha256(json.dumps(rs,separators=(',',':')).encode()).hexdigest(),
           explicit_rows=rs if n<=40 else None,reachable_word=[1]*3,first_success_word=w,attaining_word=[0]*(M-1)+[1,1],
           avoid_compress_vertices=vertices,macro_c=c,rooted_word=v,root=r+1,rooted_height=height,
           reset_length=3+height*len(v),literal_reset_word=([1]*3+v*height if 3+height*len(v)<=5000 else None))
    if n<=12:
        rt,rw,k=bfs(rs,(1<<n)-1);z['finite_exact_reset']=dict(rt=rt,word=rw,vertices=k)
    else:z['finite_exact_reset']=None
    return z


def finite_counterexample():
    rs=[[2,0,5,1,3,1],[0,1,3,2,4,4]];S=15;A=1
    ac,w,k=bfs(rs,S,A);rt,rw,v=bfs(rs,63)
    assert ac==5 and rt==18
    return dict(n=6,rows=rs,S=S,A=A,reachable_word=[0,0,1,0],ac=ac,attaining_word=w,
                safe_vertices=k,rt=rt,reset_word=rw,full_reset_vertices=v,refuted_bound=4)


def parameters():
    scopes={(r,M) for n in range(7,23) for r in range(1,n-5) for M in [n-r-1] if M>=5 and M%2}
    scopes|={(r,M) for M in range(5,66,2) for r in (1,2,3,5,8,16,31)}
    scopes|={(n-M-1,M) for n in (129,257,513,1025) for M in (5,7,9,11)}
    return sorted(scopes,key=lambda p:(sum(p)+1,p[0]))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/avoid_compress_third_face.json'))
    args=ap.parse_args();records=[record(*p) for p in parameters()]
    out=dict(records=records,finite_counterexample=finite_counterexample(),status='PROVED paper every r>=1 odd M>=5, third face exact ac=n-|A|; finite counterexample refutes ac<=n-|S|+2; finite checks do not establish missing parity; no formal kernel; Cerny OPEN')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(parameters=len(records),maximum_n=max(z['n'] for z in records),finite_reset_scopes=sum(z['finite_exact_reset'] is not None for z in records))),flush=True)


if __name__=='__main__':main()
