"""Finite paid controls for the all-n weak-stationary counterfamily."""
from fractions import Fraction
import json
from pathlib import Path

def rows(n):return [[0]+list(range(2,n))+[1],[1]+[0]*(n-2)+[1]]

def action(fs,w):
    f=list(range(len(fs[0])))
    for a in w:f=[fs[a][q] for q in f]
    return f

def support(n):
    N=n-2;k=(n+1)//2;high=range(k+1,n);out=[]
    def emit(kind,j,weight):
        w=[1,1]+[0]*(j-1) if kind=='B' else [1]+[0]*(n-2)+[1]+[0]*(j-1)
        f=action(rows(n),w);out.append(dict(kind=kind,j=j,weight=[weight.numerator,weight.denominator],word=w,row_counts=[f.count(q) for q in range(n)]))
    for j in high:emit('B',j,Fraction(1,N))
    if n%2:
        emit('B',1,Fraction(1,2*N));emit('R',1,Fraction(1,2*n))
        for j in range(2,k+1):emit('R',j,Fraction(1,n))
    else:
        for j in range(1,k+1):emit('R',j,Fraction(1,n))
    return out

def main():
    records=[]
    for n in list(range(4,65))+[127,257]:
        fs=rows(n);K=(3*n+1)//2-1;phi=[n-2]+[0]*((n+1)//2-1)+[-2]*(n-(n+1)//2)
        supp=support(n);total=sum((Fraction(*z['weight']) for z in supp),Fraction(0));assert total==1
        average=[sum((Fraction(*z['weight'])*z['row_counts'][q] for z in supp),Fraction(0)) for q in range(n)];assert average==[1]*n
        assert max(len(z['word']) for z in supp)==K
        reset=[1]+[0]*(n-2)+[1];assert len(set(action(fs,reset)))==1
        records.append(dict(n=n,rows=fs,N=n-2,K=K,lower_cap=K-1,separator_phi=phi,strict_margin=-sum(phi),
                            exact_reset_threshold=n,reset=reset,support=supp))
    out=dict(records=records,status='PROVED paper EVERY n>=4: exact maximum stationary singular-support cost ceil(3n/2)-1, ordinary rt n; attaining support SC sync. Finite controls independently checked separately; no expected-cost, general upper bound or formal proof claim. General Cerny OPEN.')
    Path('scripts/direct_attack/data/weak_stationary_linear_cost.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(parameters=len(records),maximum_n=257,supported_words=sum(len(z['support']) for z in records),status=out['status'])),flush=True)

if __name__=='__main__':main()
