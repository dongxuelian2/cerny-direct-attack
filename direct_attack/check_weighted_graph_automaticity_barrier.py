"""Independent literal moment/cut/pool checks, no generator imports."""
from pathlib import Path
from math import gcd
import json
import copy
from .check_order_two_weighted_endpoints import model,particles

ROOT=Path(__file__).resolve().parents[1]


def check(data):
    F=data['rows'];a,b=F;M,L=model(F);S=data['subset'];nu=[1]*M+[2]
    assert M==24 and S==22369621 and a==[24,2,9,4,11,5,18,10,3,8,1,13,24,14,21,16,23,17,6,22,15,20,7,19,0]
    mass=lambda U:U.bit_count()+(U>>M&1);base=mass(S);assert base==14
    image=particles(F,data['reset_word']);assert len(set(image))==1 and len(data['reset_word'])<=M*M
    g=L;power=list(range(M));triangle=0
    def rotate(v,k):return [v[(q-k)%M] for q in range(M)]+[v[M]]
    def push(v,row):
        out=[0]*(M+1)
        for q,x in enumerate(row):out[x]+=v[q]
        return out
    def value(v,s):return sum(v[q] for q in range(M+1) if S>>(M if q==M else (q+s)%M)&1)
    v1=push(nu,a)
    assert push(nu,b)==nu
    for k in range(1,L):
        power=[a[q] for q in power]
        for j in range(1,L-k+1):
            g=gcd(g,power[j]-power[j+L])
            v=rotate(v1,j)
            for _ in range(k):v=push(v,a)
            for s in range(L):assert value(v,s)==base and j+k+s+1<=M;triangle+=1
    assert g==data['triangular_h']==2
    graph=set();canonical=0;best=10**9;lower=0;positive=0
    for s in range(2):assert value(nu,s)==base and value(v1,s)==base;lower+=2
    for j in range(M):
        v2=push(rotate(v1,j),a)
        for s in range(2):assert value(v2,s)==base;lower+=1
        for k in range(M):
            v3=push(rotate(v2,k),a)
            for s in range(2):
                canonical+=1;gain=value(v3,s)-base;cost=j+k+s+3
                if gain>0:positive+=1;best=min(best,cost)
                if cost<=M:
                    v=rotate(v3,s);d=[0,0,0]
                    for q in range(M+1):
                        label=2 if q==M else q%2;d[label]+=v[q]-nu[q]
                    if any(d):
                        assert sorted(d)==[-1,0,1]
                        graph.add((d.index(-1),d.index(1)))
                    assert gain<=0
    assert graph=={(2,0),(2,1),(0,2)} and best==data['three_a_minimum']==25
    image=particles(F,data['three_a_word']);score=sum(nu[q] for q,x in enumerate(image) if S>>x&1)
    assert len(data['three_a_word'])==25 and score==base+1
    # The old triangular pool is too small: permit the actual short tail
    # when searching a b^j a^k b^s. Certify this NEW finite-pool minimum too.
    adaptive=10**9;adaptive_word=None;adaptive_controls=0
    for j in range(M):
        v=rotate(v1,j)
        for k in range(1,M-j):
            v=push(v,a)
            for s in range(min(2,M-j-k)):
                adaptive_controls+=1
                if value(v,s)>base and j+k+s+1<adaptive:
                    adaptive=j+k+s+1;adaptive_word=[0]+[1]*j+[0]*k+[1]*s
    assert adaptive<=M
    image=particles(F,adaptive_word);assert sum(nu[q] for q,x in enumerate(image) if S>>x&1)>base
    h=data['minimum'];cut=dict(data['cut']);assert h==9 and len(cut)==len(data['cut']) and cut[S]==0
    edges=0
    for U,d in cut.items():
        assert type(U)is int and 0<=U<2**(M+1) and 0<=d<h and mass(U)<=base
        if d<h-1:
            for row in F:
                V=sum(1<<q for q,x in enumerate(row) if U>>x&1)
                assert V in cut and cut[V]<=d+1;edges+=1
    image=particles(F,data['word']);target=sum(1<<q for q,x in enumerate(image) if S>>x&1)
    assert len(data['word'])==h and target==data['target'] and mass(target)==15 and target>>M&1
    return dict(verified=True,n=M+1,triangular_words=triangle,three_a_canonical=canonical,
        three_a_successes=positive,zero_one_two_a_controls=lower,weighted_three_a_minimum=best,
        adaptive_one_b_minimum=adaptive,adaptive_controls=adaptive_controls,
        weighted_ordinary_minimum=h,ordinary_root_positive_minimum=h,
        cut_vertices=len(cut),cut_edges=edges,reset_cost=len(data['reset_word']),
        status='Automatic old graph connectivity REFUTED. Literal finite pool/cut controls COMPUTATIONALLY VERIFIED; not formal. Unrestricted weighted M-extension and general Cerny OPEN.')


def main():
    data=json.loads((ROOT/'direct_attack/data/weighted_graph_automaticity_barrier.json').read_text())
    out=check(data);rejected=[]
    for mode in range(6):
        bad=copy.deepcopy(data)
        if mode==0:bad['triangular_h']=1
        if mode==1:bad['subset']^=1
        if mode==2:bad['cut'].pop(0)
        if mode==3:bad['minimum']=8
        if mode==4:bad['three_a_word'].pop()
        if mode==5:bad['reset_word']=[]
        try:check(bad)
        except(AssertionError,KeyError,ValueError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected
    print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
