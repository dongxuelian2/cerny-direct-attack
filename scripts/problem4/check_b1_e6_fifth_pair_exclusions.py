"""Complete independent binary E6/F12,F127 word/port audit.

Literal normalized pairs at n8..10; every individual n13 port.
No generator imports or bounded-solver negatives.
"""
from collections import Counter
from itertools import product,permutations
from math import factorial
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
K={1,2};P={0,3,5,6};A={3};B={0};C={1,4};D={5};E={6}
def L_systems(T):
    for outputs in permutations(T):yield dict(zip(T,outputs)),None
    for q in T:
        if q==2:continue
        blocks=[(2,q)]+[(x,) for x in T if x not in (2,q)]
        for outputs in permutations(T,len(blocks)):
            yield {x:t for block,t in zip(blocks,outputs) for x in block},q
def witness(rows,pair,word,kind):
    assert pair[0]!=pair[1] and len(word)==2
    if kind=='protected':assert set(pair)&P
    else:assert kind=='outside_K' and not set(pair)&K
    image=set(pair)
    for ell in word:image={rows[ell][q] for q in image}
    assert len(image)==1
def literal_pairs(n,F):
    T=(2,*range(7,n));I=tuple(sorted(set(range(n))-P-set(F)))
    assert len(I)==len(T)-(len(F)-2) and not set(I)&K
    hist=Counter();total=0
    for ordinary,q in L_systems(T):
        for preA in (0,3):
            for u in sorted(P-{preA,6}):
                for preD,preE in permutations(sorted(P-{preA,u})):
                    for delta in (1,4):
                        L=[-1]*n;L[1]=L[4]=0;L[preA]=3;L[u]=delta;L[preD]=5;L[preE]=6
                        for x,t in ordinary.items():L[x]=t
                        assert all(t>=0 for t in L)
                        for protect_swap,gamma,outputs in product((False,True),(1,4),permutations(T,len(I))):
                            X=[-1]*n;X[0]=3 if protect_swap else 0;X[3]=0 if protect_swap else 3;X[5]=gamma;X[6]=5
                            for x in F:X[x]=6
                            for x,t in zip(I,outputs):X[x]=t
                            assert all(t>=0 for t in X);rows=(L,X);total+=1
                            if gamma==delta:
                                absent=5-gamma
                                assert absent not in set(L)|set(X);hist['missing_C_target']+=1;continue
                            if gamma==1:
                                t=next(t for t in F if t!=1 and t in outputs);x=I[outputs.index(t)]
                                witness(rows,(5,x),(1,1),'protected');hist['protected_XX']+=1;continue
                            assert gamma==4 and delta==1
                            if len(F)==3:
                                t=next(t for t in (2,7) if t in ordinary.values());x=next(x for x,t0 in ordinary.items() if t0==t)
                                witness(rows,(u,x),(0,1),'protected');hist['protected_LX_F127']+=1;continue
                            if 2 in ordinary.values():
                                x=next(x for x,t in ordinary.items() if t==2)
                                witness(rows,(u,x),(0,1),'protected');hist['protected_LX_F12']+=1;continue
                            assert q is not None and L[2]==L[q]
                            x=I[outputs.index(2)];y=I[outputs.index(q)]
                            witness(rows,(x,y),(1,0),'outside_K');hist['outside_XL_extra_kernel']+=1
    assert total==64*len(T)*factorial(len(T))**2 and hist['missing_C_target']*2==total
    return dict(n=n,F=F,complete_normalized_row_pairs=total,proof_cases=dict(sorted(hist.items())))
def full_ports():
    T=(2,*range(7,13));F12=F127=ordinary_L=missing2=0
    for outputs in permutations(T):
        inverse=dict(zip(outputs,(4,*range(7,13))))
        assert set(inverse)==set(T) and all(x not in K for x in inverse.values());F12+=1
    for outputs in permutations(T,6):
        inverse=dict(zip(outputs,(4,*range(8,13))))
        assert len(inverse)==6 and any(t in inverse for t in (2,7)) and all(x not in K for x in inverse.values());F127+=1
    for ordinary,q in L_systems(T):
        assert len(set(ordinary.values()))>=6 and any(t in ordinary.values() for t in (2,7))
        assert len({ordinary[x] for x in T if x!=2})==6
        if 2 not in ordinary.values():assert q is not None and ordinary[2]==ordinary[q];missing2+=1
        ordinary_L+=1
    assert F12==F127==5040 and ordinary_L==35280 and missing2==4320
    return dict(F12_ordinary_X_systems=F12,F127_ordinary_X_systems=F127,
        ordinary_L_systems=ordinary_L,L_systems_omitting2=missing2)
def normalize_fields(z):
    verified=0
    for p in z['pairs']:
        for i,j in p['fifth_field_pairs']:
            pair=[z['rows'][i],z['rows'][j]]
            suppliers=[row for row in pair if row['preE']==z['F']]
            mergers=[row for row in pair if row['preB']==[1,4]]
            assert len(suppliers)==len(mergers)==1
            X=suppliers[0];L=mergers[0];assert X!=L
            assert sorted([X['preA'],X['preB']])==[[0],[3]]
            assert X['preC']==[5] and X['preD']==[6]
            assert L['preA'] in ([0],[3]) and L['preC'] in ([0],[3],[5])
            pre=[L[key] for key in ('preA','preC','preD','preE')]
            assert all(len(t)==1 for t in pre) and {t[0] for t in pre}==P
            verified+=1
    assert verified==12
    return dict(F=z['F'],field_pairs=verified,labelled_F=z['labelled_F'])
def main():
    inv=json.loads((ROOT/'b1_fifth_inventory.json').read_text(encoding='utf-8'))
    excluded=[normalize_fields(z) for z in inv['records'] if z['E']==[6] and z['F'] in ([1,2],[1,2,7])]
    assert len(excluded)==2
    checks=[]
    for F in ([1,2],[1,2,7]):
        for n in (8,9,10):
            v=literal_pairs(n,F);checks.append(v);print(json.dumps(dict(n=n,F=F,pairs=v['complete_normalized_row_pairs'])),flush=True)
    ports=full_ports()
    kept=[z for z in inv['records'] if z['E']==[6] and z['F'] not in ([2],[1,2],[1,2,7])]
    assert [z['F'] for z in kept]==[[7],[1,7],[2,4],[2,7]]
    assert sum(z['labelled_F'] for z in kept)==19
    assert sum(len(p['fifth_field_pairs']) for z in kept for p in z['pairs'])==268
    assert len({tuple(p['original_third_rows']) for z in kept for p in z['pairs'] if p['fifth_field_pairs']})==14
    names=[Path(__file__).name,'PROOF.md#problem4-b1-e6-f12-f127-exclusion','b1_fifth_inventory.json','b1_fifth_audit.json',
        'PROOF.md#problem4-b1-fifth-entrance','b1_e6_f2_audit.json','PROOF.md#problem4-b1-e6-f2-exclusion',
        'PROOF.md#problem4-b1-partial-cover-fourth','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    result=dict(status='pass',parameter=[13,9,1],alphabet='binary only',excluded=excluded,
        complete_literal_controls=checks,complete_n13_individual_port_controls=ports,
        remaining_binary_E6_fifth_geometry=[z['F'] for z in kept],remaining_labelled_F=19,remaining_field_pairs=268,
        all_original_third_pairs_retained=14,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Two complete conditional binary fifth exclusions. No unrestricted exclusion, whole E6/third/joint exclusion, full n13 pair scan, F value or numerical alphabet separation.')
    (ROOT/'b1_e6_fifth_pair_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',controls=checks,ports=ports,remaining_field_pairs=268)),flush=True)
if __name__=='__main__':main()
