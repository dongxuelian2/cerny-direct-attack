"""Independent ranks, periodic mask coverage and actual original extension words."""
from pathlib import Path
from math import gcd
import json
import copy
from .check_rooted_period_rank_payment import rational_rank,cyclic_period
from .check_order_two_weighted_endpoints import model,particles

ROOT=Path(__file__).resolve().parents[2]


def check(data):
    controls=words=paid=particles_count=0
    for z in data['models']:
        F=z['rows'];a,b=F;M,L=model(F);d=L
        for j in range(1,L):d=gcd(d,a[j]-a[j+L])
        assert d==z['d'] and d<L and len(z['controls'])==2**d-2
        for expected,c in enumerate(z['controls'],1):
            mask=c['mask'];assert mask==expected
            p=cyclic_period(d,mask);D=rational_rank(p,mask&(2**p-1));e=max(0,p-D-1)
            assert (c['p'],c['D'],c['e'])==(p,D,e)
            S=(1<<M)|sum(1<<q for q in range(M) if mask>>(q%d)&1)
            for key in ('upper_word','saturation_word'):
                word=c[key];image=particles(F,word);T=sum(1<<q for q,x in enumerate(image) if S>>x&1)
                assert T>>M&1 and T.bit_count()==S.bit_count()+1 and len(word)<=M+e
                words+=1;particles_count+=(M+1)*len(word)
                paid+=len(word)>M
            controls+=1
    return dict(verified=True,models=len(data['models']),complete_periodic_controls=controls,original_words=words,
                forward_particles=particles_count,above_M_saturation_words=paid,
                status='Finite original period-rank extension upper/cost-saturation controls COMPUTATIONALLY VERIFIED. No shortest-word or extra-cost necessity claim; general Cerny OPEN.')


def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/period_rank_extension_controls.json').read_text());out=check(data);rejected=[]
    for mode in range(4):
        bad=copy.deepcopy(data)
        if mode==0:bad['models'][0]['controls'].pop()
        if mode==1:bad['models'][0]['controls'][0]['upper_word']=[0]
        if mode==2:bad['models'][0]['controls'][0]['D']-=1
        if mode==3:bad['models'][0]['controls'][1]['mask']=1
        try:check(bad)
        except(AssertionError,KeyError,ValueError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected;print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
