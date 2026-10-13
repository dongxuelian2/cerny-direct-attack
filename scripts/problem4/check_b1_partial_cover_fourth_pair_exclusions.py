"""Independent literal and all-port audits for binary E12/E126 exclusions.

The proof handles arbitrary ordinary labels symbolically; smaller complete
rows test every stated word. No thirteen-state pair enumeration is claimed.
"""
from collections import Counter
from itertools import permutations,product
from pathlib import Path
from math import factorial
import hashlib,json
ROOT=Path(__file__).resolve().parent
K={1,2};PROTECTED={0,3,5}

def merge(rows,pair,word,kind):
    assert len(set(pair))==2 and len(word)==2
    if kind=='protected':assert set(pair)&PROTECTED
    else:assert kind=='outside' and not set(pair)&K
    image=set(pair)
    for letter in word:image={rows[letter][q] for q in image}
    assert len(image)==1,(rows,pair,word)

def ordinary_L(T):
    for outputs in permutations(T):yield dict(zip(T,outputs)),None
    for q in T:
        if q==2:continue
        blocks=[(2,q)]+[(x,) for x in T if x not in (2,q)]
        for outputs in permutations(T,len(blocks)):
            yield {x:t for block,t in zip(blocks,outputs) for x in block},q

def literal_pairs(n,E):
    T=(2,*range(6,n));hist=Counter();total=0
    ordinary_F=tuple(x for x in range(n) if x not in {0,3,5}|set(E))
    assert len(ordinary_F)==len(T)-(len(E)-2) and not set(ordinary_F)&K
    for ordinary,q in ordinary_L(T):
        for p,swap,delta in product((0,3),(False,True),(1,4)):
            L=[-1]*n;L[1]=L[4]=0;L[3 if p==0 else 0]=3
            u=5 if swap else p;v=p if swap else 5
            L[u]=delta;L[v]=5
            for x,t in ordinary.items():L[x]=t
            assert all(t>=0 for t in L)
            for protect_swap,gamma,outputs in product((False,True),(1,4),permutations(T,len(ordinary_F))):
                F=[-1]*n;F[0]=3 if protect_swap else 0;F[3]=0 if protect_swap else 3;F[5]=gamma
                for x in E:F[x]=5
                for x,t in zip(ordinary_F,outputs):F[x]=t
                assert all(t>=0 for t in F);rows=(L,F);total+=1
                if delta==gamma:
                    absent=next(x for x in (1,4) if x!=delta)
                    assert absent not in set(L)|set(F);hist['missing_C_target']+=1;continue
                if gamma==1:
                    target=next(x for x in E if x!=1 and x in set(outputs))
                    outside=ordinary_F[outputs.index(target)]
                    merge(rows,(5,outside),(1,1),'protected');hist['protected_FF']+=1;continue
                assert gamma==4 and delta==1
                if len(E)==3:
                    target=next(x for x in (2,6) if x in ordinary.values())
                    x=next(x for x,t in ordinary.items() if t==target)
                    merge(rows,(u,x),(0,1),'protected');hist['protected_LF_E126']+=1;continue
                if 2 in ordinary.values():
                    x=next(x for x,t in ordinary.items() if t==2)
                    merge(rows,(u,x),(0,1),'protected');hist['protected_LF_E12']+=1;continue
                assert q is not None and L[2]==L[q]
                first=ordinary_F[outputs.index(2)];second=ordinary_F[outputs.index(q)]
                merge(rows,(first,second),(1,0),'outside');hist['outside_FL_extra_kernel']+=1
    assert total==32*len(T)*factorial(len(T))**2
    assert hist['missing_C_target']*2==total
    return dict(n=n,E=E,complete_transition_pair_controls=total,proof_cases=dict(sorted(hist.items())),
        scope='Every normalized pair under necessary row/port templates; local pair premises, no smaller-n equality claim.')

def ports():
    T=(2,*range(6,13));E12_count=E126_count=0;Lcount=missing2=0
    for outputs in permutations(T):
        inputs=(4,*range(6,13));inverse=dict(zip(outputs,inputs))
        assert set(inverse)==set(T) and all(x not in K for x in inverse.values())
        assert inverse[2]!=5;E12_count+=1
    for outputs in permutations(T,7):
        inputs=(4,*range(7,13));inverse=dict(zip(outputs,inputs))
        assert len(inverse)==7 and all(x not in K for x in inverse.values())
        assert any(x in inverse for x in (2,6));E126_count+=1
    for ordinary,q in ordinary_L(T):
        assert len(set(ordinary.values()))>=7 and any(x in ordinary.values() for x in (2,6))
        assert len({ordinary[x] for x in T if x!=2})==7
        if 2 not in ordinary.values():
            assert q is not None and ordinary[2]==ordinary[q];missing2+=1
        Lcount+=1
    assert E12_count==E126_count==40320 and Lcount==322560 and missing2==35280
    return dict(complete_E12_F_output_systems=E12_count,complete_E126_F_output_systems=E126_count,
        complete_L_output_systems=Lcount,L_systems_missing_target2=missing2,
        scope='Complete individual thirteen-state port systems; coupling is covered by the paper proof, not pair enumeration.')

def main():
    literal=[]
    for E in ([1,2],[1,2,6]):
        for n in (7,8,9):
            current=literal_pairs(n,E);literal.append(current)
            print(json.dumps(dict(E=E,n=n,complete_pairs=current['complete_transition_pair_controls'])),flush=True)
    port_controls=ports()
    data=json.loads((ROOT/'b1_partial_cover_fourth_inventory.json').read_text(encoding='utf-8'))
    discharged=[];kept=[];old_pairs=set()
    for z in data['records']:
        count=sum(len(p['fourth_field_pairs']) for p in z['pairs'])
        if z['E'] in ([1,2],[1,2,6]):
            assert count==6;discharged.append(dict(id=z['id'],E=z['E'],field_pairs=count))
        elif not z['excluded_by_known_bound']:
            kept.append(z);old_pairs.update(tuple(p['original_rows']) for p in z['pairs'] if p['fourth_field_pairs'])
    assert len(discharged)==2 and len(kept)==4 and sum(z['labelled_E'] for z in kept)==22
    assert sum(len(p['fourth_field_pairs']) for z in kept for p in z['pairs'])==94 and len(old_pairs)==14
    names=[Path(__file__).name,'PROOF.md#problem4-b1-partial-cover-fourth','b1_partial_cover_fourth_inventory.json',
        'b1_partial_cover_fourth_audit.json','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-second-entrance-fiber',
        'PROOF.md#problem4-third-entrance-space','PROOF.md#problem4-local-equality-flag','PROOF.md#problem4-codimension-four-p5-dichotomy']
    result=dict(status='pass',parameter=[13,9,1],binary_only=True,excluded_E=[[1,2],[1,2,6]],
        complete_literal_controls=literal,complete_n13_individual_port_controls=port_controls,
        discharged_fourth_field_pairs=discharged,remaining_binary_fourth_geometries=4,
        remaining_binary_labelled_E_choices=22,remaining_binary_fourth_field_pairs=94,
        original_binary_third_pairs_retained=14,unrestricted_fourth_geometries_unchanged=6,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete conditional binary E12/E126 fourth exclusion via literal two-letter witnesses and symbolic port counting. '
              'No whole third/joint exclusion, full thirteen-state transition-pair scan, F value or numerical alphabet separation.')
    (ROOT/'b1_partial_cover_fourth_pair_exclusion_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',literal_assignments=[z['complete_transition_pair_controls'] for z in literal],
        ports=port_controls,remaining_geometries=4,remaining_field_pairs=94)),flush=True)

if __name__=='__main__':main()
