"""Independent rational ranks and ORIGINAL rooted exact-unit budget checks."""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
from math import gcd,factorial
import json
import copy
from .check_order_two_weighted_endpoints import model,particles

ROOT=Path(__file__).resolve().parents[2]


def cyclic_period(d,mask):
    for p in range(1,d+1):
        if d%p==0 and ((mask>>p)|((mask&(2**p-1))<<(d-p)))==mask:return p
    raise AssertionError('period')


@lru_cache(None)
def rational_rank(p,mask):
    rotations=[(mask>>s)|((mask&(2**s-1))<<(p-s)) for s in range(p)]
    canonical=min(rotations)
    if canonical!=mask:return rational_rank(p,canonical)
    rows=[[Fraction(mask>>((q+s)%p)&1) for q in range(p)] for s in range(p)]
    r=0
    for q in range(p):
        candidates=[s for s in range(r,p) if rows[s][q]]
        if not candidates:continue
        j=candidates[0];rows[r],rows[j]=rows[j],rows[r];pivot=rows[r][q]
        rows[r]=[x/pivot for x in rows[r]]
        for s in range(r+1,p):
            if rows[s][q]:
                c=rows[s][q];rows[s]=[x-c*y for x,y in zip(rows[s],rows[r])]
        r+=1
    return r


def tables_check(data):
    tables={};patterns=0
    for z in data['tables']:
        d=z['d'];assert 1<=d<=12 and d not in tables and len(z['rows'])==2**d-2
        maxima=[0]*(d+1)
        for expected,row in enumerate(z['rows'],1):
            mask,p,D,e=row;assert mask==expected and p==cyclic_period(d,mask)
            actual=rational_rank(p,mask&(2**p-1))
            assert actual==D and e==max(0,p-D-1)
            maxima[mask.bit_count()]=max(maxima[mask.bit_count()],e);patterns+=1
        assert z['maxima']==maxima and z['E']==sum(maxima)
        assert sum(maxima)<=(d-1)*max(0,d-3)
        tables[d]=z
    assert set(tables)==set(range(1,13))
    # A tempting cardinality/rank bound is FALSE: coprime weight5 does not
    # give full rank12. This literal Boolean row has exact rank8.
    mask=sum(1<<q for q in (0,1,5,6,9))
    assert cyclic_period(12,mask)==12 and mask.bit_count()==5 and rational_rank(12,mask)==8
    return tables,patterns


def check(data,table_data):
    tables,patterns=tables_check(table_data);seen=set();nstages=nparticles=nsaved=surplus=0;max_n=max_cost=square_inputs=0
    for index,z in enumerate(data['records']):
        F=z['rows'];a,b=F;M,L=model(F);d=L
        for j in range(1,L):d=gcd(d,a[j]-a[j+L])
        assert z['d']==d and d<L and L%d==0
        if index<672:
            assert M==8;signature=tuple(a[q] for q in range(M) if q not in(0,L));assert signature not in seen;seen.add(signature)
        E=tables[d]['E'] if d in tables else (d-1)*max(0,d-3)
        assert z['E']==E and z['bound']==M*M+E-(L-d)
        S=1<<M;reset=[];paid=save=0
        assert len(z['stages'])==M
        for k,st in enumerate(z['stages']):
            assert st['source']==S and S>>M&1 and S.bit_count()==k+1
            U=S&(2**M-1);periodic=all((U>>q&1)==(U>>((q+d)%M)&1) for q in range(M))
            if periodic and U not in(0,2**M-1):
                mask=U&(2**d-1);p=cyclic_period(d,mask);D=rational_rank(p,mask&(2**p-1));e=max(0,p-D-1)
                assert (st['p'],st['D'],st['e'])==(p,D,e)
            else:
                e=0;assert st['e']==0
            image=particles(F,st['word']);T=sum(1<<q for q,x in enumerate(image) if S>>x&1)
            assert T==st['target'] and T>>M&1 and T.bit_count()==S.bit_count()+1
            assert len(st['word'])<=M+e
            saved=k>0 and k%2==0 and not periodic
            assert st['saved_even']==saved and (not saved or len(st['word'])<=M-1)
            if k==2:assert saved and S==(1<<M)|1|(1<<L)
            paid+=e;save+=saved;surplus+=e>0
            reset=st['word']+reset;S=T;nstages+=1
        assert S==2**(M+1)-1 and reset==z['reset_word']
        assert paid<=E and save>=L-d and len(reset)<=M*M+paid-save<=z['bound']
        assert 16*len(reset)<=17*M*M and particles(F,reset)==[M]*(M+1)
        nparticles+=(M+1)*len(reset);nsaved+=save;max_n=max(max_n,M+1);max_cost=max(max_cost,len(reset));square_inputs+=z['bound']<=M*M
    assert len(seen)==factorial(6)-2**3*factorial(3)
    return dict(verified=True,records=len(data['records']),complete_M8=672,exact_table_patterns=patterns,
        E={d:z['E'] for d,z in tables.items()},rooted_unit_stages=nstages,guaranteed_saved_stages=nsaved,
        reset_particles=nparticles,surcharge_parameter_stages=surplus,maximum_n=max_n,maximum_reset_cost=max_cost,
        input_bounds_at_most_square=square_inputs,
        status='Finite rational ranks and rooted payment/reset controls COMPUTATIONALLY VERIFIED; all-n paper proof audited separately, not formal. General Cerny OPEN.')


def main():
    tables=json.loads((ROOT/'scripts/direct_attack/data/rooted_period_rank_tables.json').read_text())
    data=json.loads((ROOT/'scripts/direct_attack/data/rooted_period_rank_payment.json').read_text());out=check(data,tables);rejected=[]
    for mode in range(5):
        bad=copy.deepcopy(data);bad_tables=copy.deepcopy(tables)
        if mode==0:bad['records'][0]['stages'][0]['target']^=1
        if mode==1:bad['records'][0]['bound']-=1
        if mode==2:bad['records'][0]['reset_word'].pop()
        if mode==3:bad_tables['tables'][11]['E']-=1
        if mode==4:bad_tables['tables'][11]['rows'][0][2]-=1
        try:check(bad,bad_tables)
        except(AssertionError,KeyError,ValueError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected;print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
