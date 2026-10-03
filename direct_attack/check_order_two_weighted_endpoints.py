"""Independent original particle/mass checks. No generator imports."""
from pathlib import Path
from math import factorial
import json
import copy

ROOT=Path(__file__).resolve().parents[1]


def model(F):
    a,b=F;M=len(a)-1;L=M//2
    assert M>=6 and M%2==0 and b==list(range(1,M))+[0,M]
    assert a[M]==0 and a[0]==a[L]==M
    assert sorted(a[q] for q in range(M) if q not in (0,L))==[q for q in range(M) if q not in (0,L)]
    return M,L


def particles(F,word):
    image=list(range(len(F[0])))
    for c in word:
        assert type(c) is int and c in (0,1)
        image=[F[c][q] for q in image]
    return image


def check(data):
    endpoint_particles=sync=nonsync=sharp=0;seen=set()
    for index,z in enumerate(data['endpoints']):
        F=z['rows'];M,L=model(F);a,b=F
        if index<720:
            assert M==8
            signature=tuple(a[q] for q in range(M) if q not in (0,L))
            assert signature not in seen;seen.add(signature)
        mixed=[j for j in range(1,L) if a[j]%L!=a[j+L]%L]
        if z.get('nonsync'):
            assert not mixed
            blocks=[[q,q+L] for q in range(L)]+[[M]]
            label=lambda q:L if q==M else q%L
            for row in F:
                induced=[]
                for block in blocks:
                    target={label(row[q]) for q in block};assert len(target)==1
                    induced.append(next(iter(target)))
                assert sorted(induced)==list(range(L+1))
            nonsync+=1;continue
        assert len(mixed)>=2 and z['j']==min(mixed)<=L-2
        for direction,key in ((1,'positive_word'),(-1,'negative_word')):
            word=z[key];assert len(word)<=M
            image=particles(F,word)
            mass=sum(2 if q==M else 1 for q,x in enumerate(image) if x==M)
            assert mass==2+direction and (image[M]==M)==(direction==1)
            endpoint_particles+=(M+1)*len(word)
            sharp+=int(len(word)==M)
        sync+=1
    assert len(seen)==factorial(6)
    canonical=positive=lower_controls=forward=0
    for z in data['weighted_three_a_controls']:
        F=z['rows'];M,L=model(F);a,b=F;p=z['p'];S=z['subset']
        assert z['m']==2 and M==8*p and p>=3
        assert S==(1<<M)|sum(1<<q for q in range(M) if q%p!=p-1)
        nu=[1]*M+[2];base=sum(nu[q] for q in range(M+1) if S>>q&1)
        def push(v,row):
            out=[0]*(M+1)
            for q,x in enumerate(row):out[x]+=v[q]
            return out
        def rotate(v,k):return [v[(q-k)%M] for q in range(M)]+[v[M]]
        def mass(v,s):return sum(v[q] for q in range(M+1) if S>>(M if q==M else (q+s)%M)&1)
        assert sum(nu)==M+2 and push(nu,b)==nu
        v1=push(nu,a)
        assert v1==[nu[q]+int(q==0)-int(q==L) for q in range(M+1)]
        for s in range(p):assert mass(nu,s)==base and mass(v1,s)==base;lower_controls+=2
        best=10**9;success=0
        for j in range(M):
            v2=push(rotate(v1,j),a)
            for s in range(p):assert mass(v2,s)<=base;lower_controls+=1
            for k in range(M):
                v3=push(rotate(v2,k),a)
                for s in range(p):
                    canonical+=1
                    if mass(v3,s)>base:
                        success+=1;best=min(best,j+k+s+3)
        assert success==8 and best==M+p-1
        image=particles(F,z['three_a_word'])
        value=sum(nu[q] for q,x in enumerate(image) if S>>x&1)
        assert len(z['three_a_word'])==best and value==base+1
        positive+=success;forward+=(M+1)*best
    return dict(verified=True,endpoint_inputs=sync+nonsync,sync_endpoint_inputs=sync,nonsync=nonsync,
                complete_M8=720,endpoint_particles=endpoint_particles,cost_M_words=sharp,
                weighted_three_a_canonical=canonical,weighted_three_a_successes=positive,
                zero_one_two_a_controls=lower_controls,barrier_forward_particles=forward,
                status='Finite controls COMPUTATIONALLY VERIFIED. Endpoint and infinite barrier proofs paper, not formal. General weighted extension and Cerny OPEN.')


def main():
    data=json.loads((ROOT/'direct_attack/data/order_two_weighted_endpoints.json').read_text())
    out=check(data);rejected=[]
    index=next(i for i,z in enumerate(data['endpoints']) if not z.get('nonsync'))
    for mode in range(5):
        bad=copy.deepcopy(data)
        if mode==0:bad['endpoints'][1]=bad['endpoints'][0]
        if mode==1:bad['endpoints'][index]['positive_word']=[0]
        if mode==2:bad['endpoints'][index]['negative_word']=bad['endpoints'][index]['positive_word']
        if mode==3:bad['weighted_three_a_controls'][0]['subset']^=1
        if mode==4:bad['weighted_three_a_controls'][0]['three_a_word'].pop()
        try:check(bad)
        except (AssertionError,KeyError,ValueError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected
    print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
