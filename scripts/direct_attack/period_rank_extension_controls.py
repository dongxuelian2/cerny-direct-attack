"""ALL periodic patterns on selected models; upper and cost-saturation words only."""
from pathlib import Path
from math import gcd
import json
from .period_rank_polynomials import least_period,rank
from .periodic_three_a_gap import family

ROOT=Path(__file__).resolve().parents[2]


def main():
    chains=json.loads((ROOT/'scripts/direct_attack/data/rooted_period_rank_payment.json').read_text())['records']
    models=[]
    for d,M in ((6,24),(8,32),(9,36),(10,40),(12,72)):
        models.append(next(z['rows'][0] for z in chains if z['d']==d and len(z['rows'][0])==M+1))
    models.append(family(6,2)['rows'][0])
    records=[]
    for a in models:
        M=len(a)-1;L=M//2;d=L
        for j in range(1,L):d=gcd(d,a[j]-a[j+L])
        powers=[list(range(M))]
        for _ in range(L):powers.append([a[q] for q in powers[-1]])
        pool={};controls=[]
        for mask in range(1,2**d-1):
            p=least_period(d,mask);D=rank(p,mask&(2**p-1));e=max(0,p-D-1);K=L-D;key=(p,K)
            if key not in pool:
                options=[]
                for k in range(1,K+1):
                    for j in range(1,L):
                        for s in range(p):
                            x,y=(powers[k][j]+s)%p,(powers[k][j+L]+s)%p
                            if x!=y:options.append((x,y,j+k+s+1,0,j,k,s))
                for j in range(1,L):
                    if a[j]%L==a[j+L]%L:continue
                    k=(-a[j])%L;other=(a[j+L]+k)%M
                    for s in range(p):options.append((p,(a[other]+s)%p,j+k+s+3,1,j,k,s))
                pool[key]=options
            selected=lambda x:x==p or (mask>>x&1)
            options=[o for o in pool[key] if selected(o[0]) and not selected(o[1]) and o[2]<=M+e]
            assert options
            cheapest=min(options,key=lambda o:o[2]);saturation=max(options,key=lambda o:o[2])
            def word(o):
                _,_,cost,kind,j,k,s=o
                return [0]+[1]*j+([0]*k if not kind else [0]+[1]*k+[0])+[1]*s
            controls.append(dict(mask=mask,p=p,D=D,e=e,upper_word=word(cheapest),saturation_word=word(saturation)))
        records.append(dict(rows=[a,list(range(1,M))+[0,M]],d=d,controls=controls))
    (ROOT/'scripts/direct_attack/data/period_rank_extension_controls.json').write_text(json.dumps(dict(
        scope='ALL proper periodic masks on six selected models; saturation words do not assert necessity or minima',models=records),separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(models=len(records),controls=sum(len(z['controls']) for z in records),
        paid_saturation=sum(len(c['saturation_word'])>len(z['rows'][0])-1 for z in records for c in z['controls']))))


if __name__=='__main__':main()
