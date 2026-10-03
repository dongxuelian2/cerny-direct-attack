"""No generator import: exact gcd, graph, stage and forward reset checks."""
from pathlib import Path
from math import gcd,factorial
import json
import copy
from .check_order_two_weighted_endpoints import model,particles

ROOT=Path(__file__).resolve().parents[1]


def check(data):
    seen=set();stages=forward=edges=residual=0;minM=maxM=0
    for index,z in enumerate(data['records']):
        F=z['rows'];a,b=F;M,L=model(F);g=L;A=list(range(M))
        for k in range(1,L):
            A=[a[q] for q in A]
            for j in range(1,L-k+1):g=gcd(g,A[j]-A[j+L])
        assert z['h']==g and g<L
        if index==len(data['records'])-2:
            assert a==[12,8,9,5,1,4,12,2,3,7,11,10,0] and g==2
            inverse={a[q]:q for q in range(1,M) if q!=L};inverse_gcd=L
            for j in range(1,L):inverse_gcd=gcd(inverse_gcd,inverse[j]-inverse[j+L])
            assert inverse_gcd==1
        if index==len(data['records'])-1:
            assert a==[12,2,11,10,9,3,12,8,5,4,1,7,0] and g==2
            assert min(j for j in range(1,L) if a[j]%L!=a[j+L]%L)==4>L-g-1
        if index<672:
            assert M==8;signature=tuple(a[q] for q in range(M) if q not in(0,L))
            assert signature not in seen;seen.add(signature)
        R=[set() for _ in range(g+1)]
        label=lambda q:g if q==M else q%g
        for x,y,j,k,s in z['residual_edges']:
            assert x!=y and 0<=x<=g and 0<=y<=g and 0<j<M and j!=L and 0<=k<M and 0<=s<g
            assert j+k+s+3<=M
            # Literal full weighted image, aggregated on h colors plus root.
            word=[0]+[1]*j+[0]+[1]*k+[0]+[1]*s
            image=particles(F,word);D=[0]*(g+1)
            for q,t in enumerate(image):D[label(t)]+=2 if q==M else 1
            for q in range(M+1):D[label(q)]-=2 if q==M else 1
            expected=[int(t==y)-int(t==x) for t in range(g+1)]
            assert D==expected
            R[x].add(y);edges+=1
        for q in range(g+1):
            reached={q};todo=[q]
            for x in todo:
                for y in R[x]:
                    if y not in reached:reached.add(y);todo.append(y)
            assert len(reached)==g+1
        S=1<<M;word=[];mass=lambda U:U.bit_count()+(U>>M&1)
        for st in z['stages']:
            assert st['source']==S and len(st['word'])<=M
            image=particles(F,st['word'])
            T=sum(2**q for q,t in enumerate(image) if S>>t&1)
            assert T==st['target'] and mass(T)>mass(S)
            S=T;word=st['word']+word;stages+=1
        assert S==2**(M+1)-1 and word==z['reset_word'] and len(word)<=M*M
        assert particles(F,word)==[M]*(M+1)
        forward+=(M+1)*len(word);residual+=g>1;maxM=max(maxM,M)
    assert len(seen)==factorial(6)-2**3*factorial(3)
    return dict(verified=True,records=len(data['records']),complete_M8=672,residual_inputs=residual,
                original_stages=stages,residual_edge_words=edges,reset_forward_particles=forward,
                maximum_n=maxM+1,status='Finite criteria and ORIGINAL resets COMPUTATIONALLY VERIFIED. General sufficient theorem PROVED paper; automatic connectivity and Cerny OPEN; not formal.')


def main():
    data=json.loads((ROOT/'direct_attack/data/order_two_weighted_graph_criterion.json').read_text())
    out=check(data);rejected=[]
    for mode in range(5):
        bad=copy.deepcopy(data)
        if mode==0:bad['records'][0]['h']=4
        if mode==1:bad['records'][0]['residual_edges'].pop()
        if mode==2:bad['records'][0]['stages'][0]['target']^=1
        if mode==3:bad['records'][0]['reset_word'].pop()
        if mode==4:bad['records'][1]=bad['records'][0]
        try:check(bad)
        except(AssertionError,ValueError,KeyError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected
    print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
