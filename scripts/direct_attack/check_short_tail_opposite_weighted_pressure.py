"""Independently certify retained weighted minima; no driver coverage claim."""
from pathlib import Path
import json
import copy
from .check_order_two_weighted_endpoints import particles

ROOT=Path(__file__).resolve().parents[2]


def check(z):
    a=z['a'];M=z['M'];L=M//2;assert len(a)==M+1 and M%2==0 and a[M]==0
    b=list(range(1,M))+[0,M];F=[a,b];K=[q for q in range(M) if a[q]==M]
    assert len(K)==2 and K[0]>0 and K[1]==K[0]+L and L not in K
    assert sorted(a[q] for q in range(M) if q not in K)==[q for q in range(M) if q not in(0,L)]
    cycle=[M];q=a[M]
    while q!=M:assert q not in cycle;cycle.append(q);q=a[q]
    tail=[L]
    while tail[-1]!=M:assert a[tail[-1]] not in tail;tail.append(a[tail[-1]])
    tau,h=len(cycle),len(tail)-1;assert tau==z['tau'] and h==z['h'] and 2<=h<tau
    S=z['subset'];U=S&(2**M-1);assert 0<U<2**M-1 and all((U>>q&1)==(U>>((q+L)%M)&1) for q in range(M))
    mass=lambda X:X.bit_count()+int(bool(X>>M&1));base=mass(S);d=z['peak']
    assert type(d) is int and d>0 and len(z['word'])==d
    img=particles(F,z['word']);T=sum(1<<q for q,x in enumerate(img) if S>>x&1);assert mass(T)>base
    cut={}
    for X,depth in z['cut']:
        assert X not in cut and 0<=X<2**(M+1) and type(depth) is int and 0<=depth<d and mass(X)<=base;cut[X]=depth
    assert S in cut and cut[S]==0
    edges=0
    for X,depth in cut.items():
        if depth==d-1:continue
        for row in F:
            Y=sum(1<<q for q,x in enumerate(row) if X>>x&1)
            assert Y in cut and cut[Y]<=depth+1;edges+=1
    assert len(z['reset_word'])<=M*M and particles(F,z['reset_word'])==[M]*(M+1)
    paired=h==tau-1 and len(cycle)-1==len(tail)-1 and all((x+L)%M==y for x,y in zip(cycle[1:],tail[:-1]))
    return dict(M=M,n=M+1,tau=tau,h=h,paired_class=paired,weighted_minimum=d,
        cut_vertices=len(cut),cut_edges=edges,reset_upper=len(z['reset_word']),
        status='Retained exact weighted minimum and actual reset COMPUTATIONALLY VERIFIED; generator proposal counts EXPLORATORY, not absence coverage. General Cerny OPEN.')


def main():
    names=['short_tail_opposite_weighted_M6','short_tail_opposite_weighted_M8','short_tail_opposite_weighted_M10',
        'short_tail_opposite_weighted_M12_sample2000','short_tail_opposite_weighted_M14_sample1000',
        'short_tail_opposite_weighted_M16_sample500','short_tail_opposite_weighted_M18_sample250',
        'short_tail_opposite_weighted_M20_sample100']
    data=[json.loads((ROOT/'scripts/direct_attack/data'/ (name+'.json')).read_text()) for name in names]
    out=[check(z) for z in data];rejected=[]
    for mode in range(6):
        bad=copy.deepcopy(data[0])
        if mode==0:bad['word'].pop()
        if mode==1:bad['peak']-=1
        if mode==2:bad['cut']=[pair for pair in bad['cut'] if pair[0]!=bad['subset']]
        if mode==3:bad['cut'].append(bad['cut'][0])
        if mode==4:bad['reset_word'].pop()
        if mode==5:bad['h']+=1
        try:check(bad)
        except(AssertionError,ValueError,KeyError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    print(json.dumps(dict(verified=True,retained_controls=out,corruptions_rejected=rejected),sort_keys=True))


if __name__=='__main__':main()
