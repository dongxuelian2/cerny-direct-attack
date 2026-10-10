"""Independent E16 short-word and closed-four-cycle audit, no generators."""
from pathlib import Path
from collections import Counter
from itertools import combinations,permutations,product
from math import factorial
import hashlib,json
from check_b1_partial_cover_fourth import independent_partitions,canonical,kernel
ROOT=Path(__file__).resolve().parent
K={1,2};PROTECTED={0,3,5};C={1,4}

def kernel_controls():
    data=json.loads((ROOT/'b1_partial_cover_e16_inventory.json').read_text(encoding='utf-8'))
    old=next(v for v in json.loads((ROOT/'b1_partial_cover_fourth_inventory.json').read_text(encoding='utf-8'))['records'] if v['E']==[1,6])
    assert [(p['original_third_rows'],p['rows']) for p in data['pairs']]==[(p['original_rows'],xy) for p in old['pairs'] for xy in p['fourth_field_pairs']]
    for row in data['rows']:
        inputs=[set(row[key]) for key in ('preA','preB','preC','preD')]
        inputs.append(set(range(13))-set().union(*inputs))
        expected={tuple(parts) for parts in product(*[independent_partitions(tuple(sorted(X)),cap,tuple(sorted(PROTECTED)))
            for X,cap in zip(inputs,[1,1,2,1,8])])}
        assert expected=={canonical(v['fields']) for v in row['patterns']} and len(expected)==len(row['patterns'])
        for pat in row['patterns']:assert kernel(pat['fields'])=={tuple(p) for p in pat['kernel']}
    for pair in data['pairs']:
        x,y=pair['rows'];assert pair['kernel_pairs']==[list(ij) for ij in product(range(len(data['rows'][x]['patterns'])),range(len(data['rows'][y]['patterns'])))]
    result=dict(original_field_pairs=len(data['pairs']),row_patterns=sum(len(r['patterns']) for r in data['rows']),
        compatible_kernel_pairs=sum(len(p['kernel_pairs']) for p in data['pairs']))
    assert result['original_field_pairs']==6 and result['compatible_kernel_pairs']==384
    return result

def merge(rows,pair,word,kind):
    assert len(set(pair))==2 and len(word)<=3
    if kind=='protected':assert set(pair)&PROTECTED
    else:assert kind=='outside' and not set(pair)&K
    image=set(pair)
    for letter in word:image={rows[letter][q] for q in image}
    assert len(image)==1,(rows,pair,word)

def closed_graph(rows):
    G={(1,4),(1,6),(2,4),(2,6)};allkernels=set()
    for row in rows:
        image=set(row);assert all(not set(edge)<=image for edge in G)
        immediate={pair for pair in combinations(range(len(row)),2) if row[pair[0]]==row[pair[1]]}
        assert immediate<=G;allkernels|=immediate
        for x,y in combinations(range(len(row)),2):assert tuple(sorted((row[x],row[y]))) not in G
    assert allkernels==G

def reason(L,F,u,J):
    T={2}|set(J);Ioutside=(4,*[x for x in J if x!=6]);delta=L[u];gamma=F[5];rows=(L,F)
    if gamma==delta:
        assert next(x for x in C if x!=gamma) not in set(L)|set(F);return 'missing_C_target'
    if gamma==1:
        pre6=next((x for x in (2,*Ioutside) if F[x]==6),None)
        if pre6 is not None:
            merge(rows,(5,pre6),(1,1),'protected');return 'gamma1_protected_FF'
        assert {F[x] for x in Ioutside}==T-{6}
        r=next(x for x in Ioutside if F[x]==F[2])
        if r!=4:
            x=next(x for x in Ioutside if F[x]==2);y=next(x for x in Ioutside if F[x]==r)
            merge(rows,(x,y),(1,1),'outside');return 'gamma1_outside_FF'
        pre2=next((x for x in T if L[x]==2),None)
        if pre2 is not None:
            merge(rows,(u,pre2),(0,1),'protected');return 'gamma1_protected_LF'
        assert {L[x] for x in J}==set(J)
        q=next(x for x in J if L[x]==L[2])
        if q!=6:
            x=next(x for x in Ioutside if F[x]==2);y=next(x for x in Ioutside if F[x]==q)
            merge(rows,(x,y),(1,0),'outside');return 'gamma1_outside_FL'
        closed_graph(rows);return 'gamma1_closed_four_cycle'
    assert gamma==4 and delta==1
    pre6=next((x for x in T if L[x]==6),None)
    if pre6 is not None:
        merge(rows,(u,pre6),(0,1),'protected');return 'gamma4_protected_LF'
    assert {L[x] for x in J}==T-{6}
    q=next(x for x in J if L[x]==L[2])
    if q!=6:
        x=next(x for x in J if L[x]==2);y=next(x for x in J if L[x]==q)
        merge(rows,(x,y),(0,0),'outside');return 'gamma4_outside_LL'
    outside_image={F[x] for x in Ioutside};z=next(iter(T-outside_image))
    if z not in (2,6):
        x=next(x for x in Ioutside if F[x]==2);y=next(x for x in Ioutside if F[x]==6)
        merge(rows,(x,y),(1,0),'outside');return 'gamma4_outside_FL'
    if z==6:
        if F[2]!=6:
            assert 6 not in set(L)|set(F);return 'gamma4_missing_incoming6'
        r=next(x for x in Ioutside if F[x]==2)
        x=5 if r==4 else next(x for x in Ioutside if F[x]==r)
        merge(rows,(r,x),(1,1,0),'outside');return 'gamma4_outside_FFL_z6'
    assert z==2 and outside_image==set(J)
    if F[2]==2:
        r=next(x for x in Ioutside if F[x]==6)
        if r==4:
            merge(rows,(2,5),(1,1,0),'protected');return 'gamma4_protected_FFL_unique'
        x=next(x for x in J if L[x]==2);y=next(x for x in J if L[x]==r)
        merge(rows,(x,y),(0,1,0),'outside');return 'gamma4_outside_LFL_unique'
    r=next(x for x in Ioutside if F[x]==F[2])
    if r!=4:
        x=next(x for x in J if L[x]==2);y=next(x for x in J if L[x]==r)
        merge(rows,(x,y),(0,1),'outside');return 'gamma4_outside_LF_extra'
    closed_graph(rows);return 'gamma4_closed_four_cycle'

def ordinary_maps(inputs,targets):
    for outputs in permutations(targets):yield dict(zip(inputs,outputs))
    for q in inputs:
        if q==2:continue
        blocks=[(2,q)]+[(x,) for x in inputs if x not in (2,q)]
        for outputs in permutations(targets,len(blocks)):
            yield {x:t for block,t in zip(blocks,outputs) for x in block}

def literal_controls(n):
    J=tuple(range(6,n));T=(2,*J);I=(2,4,*range(7,n));left=[];right=[]
    for ordinary,p,swap,delta in product(ordinary_maps(T,T),(0,3),(False,True),(1,4)):
        L=[-1]*n;L[1]=L[4]=0;L[3 if p==0 else 0]=3;u=5 if swap else p;v=p if swap else 5
        L[u]=delta;L[v]=5
        for x,t in ordinary.items():L[x]=t
        assert all(x>=0 for x in L);left.append((L,u))
    for ordinary,swap,gamma in product(ordinary_maps(I,T),(False,True),(1,4)):
        F=[-1]*n;F[0]=3 if swap else 0;F[3]=0 if swap else 3;F[1]=F[6]=5;F[5]=gamma
        for x,t in ordinary.items():F[x]=t
        assert all(x>=0 for x in F);right.append(F)
    hist=Counter()
    for (L,u),F in product(left,right):hist[reason(L,F,u,J)]+=1
    total=sum(hist.values());k=n-5;assert total==32*k*k*factorial(k)**2 and hist['missing_C_target']*2==total
    assert hist['gamma1_closed_four_cycle']>0 and hist['gamma4_closed_four_cycle']>0
    return dict(n=n,complete_normalized_row_pairs=total,proof_cases=dict(sorted(hist.items())),
        scope='Complete over-approximate local templates, no equality claim for smaller n.')

def literal_kernel(row):
    groups={}
    for x,t in enumerate(row):groups.setdefault(t,[]).append(x)
    return {p for group in groups.values() for p in combinations(group,2)}

def ports():
    J=tuple(range(6,13));T=(2,*J);counts=Counter()
    for j in J:
        Ioutside=(4,*[x for x in J if x!=j]);G={(1,4),(2,4),(1,j),(2,j)}
        for gamma in (1,4):
            delta=next(x for x in C if x!=gamma)
            l_targets=J if gamma==1 else tuple(x for x in T if x!=j)
            f_targets=tuple(x for x in T if x!=j) if gamma==1 else J
            for outputs in permutations(l_targets):
                for p,swap in product((0,3),(False,True)):
                    L=[-1]*13;L[1]=L[4]=0;L[3 if p==0 else 0]=3;u=5 if swap else p;v=p if swap else 5
                    L[u]=delta;L[v]=5
                    for x,t in zip(J,outputs):L[x]=t
                    L[2]=L[j]
                    assert literal_kernel(L)=={(1,4),(2,j)} and all(not set(edge)<=set(L) for edge in G)
                    counts[f'gamma{gamma}_L_letters']+=1
            for outputs in permutations(f_targets):
                for swap in (False,True):
                    F=[-1]*13;F[0]=3 if swap else 0;F[3]=0 if swap else 3;F[1]=F[j]=5;F[5]=gamma
                    for x,t in zip(Ioutside,outputs):F[x]=t
                    F[2]=F[4]
                    assert literal_kernel(F)=={(1,j),(2,4)} and all(not set(edge)<=set(F) for edge in G)
                    counts[f'gamma{gamma}_F_letters']+=1
    assert counts==Counter(gamma1_L_letters=141120,gamma4_L_letters=141120,
        gamma1_F_letters=70560,gamma4_F_letters=70560)
    return dict(all_hard_branch_full_letter_systems=dict(counts),full_letter_assignments=sum(counts.values()),
        all_seven_fresh_E_labels_checked=True,
        scope='Complete individual n13 hard letters; arbitrary coupling is discharged by the symbolic closed graph, not n13 pair enumeration.')

def main():
    kernels=kernel_controls();literal=[]
    for n in (7,8,9):
        z=literal_controls(n);literal.append(z);print(json.dumps(dict(n=n,pairs=z['complete_normalized_row_pairs'])),flush=True)
    port_controls=ports()
    names=[Path(__file__).name,'enumerate_b1_partial_cover_e16.py','b1_partial_cover_e16_inventory.json',
        'B1_PARTIAL_COVER_E16_EXCLUSION.md','B1_PARTIAL_COVER_FOURTH.md',
        'b1_partial_cover_fourth_inventory.json','check_b1_partial_cover_fourth.py',
        'ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md',
        'LOCAL_EQUALITY_FLAG.md','CODIMENSION_FOUR_P5_DICHOTOMY.md']
    result=dict(status='pass',parameter=[13,9,1],binary_only=True,E=[1,6],kernel_controls=kernels,
        complete_literal_controls=literal,complete_n13_hard_branch_controls=port_controls,
        removed_fourth_field_pairs=6,remaining_binary_fourth_geometries_after_E16_and_E24=2,
        remaining_binary_labelled_E_choices=14,remaining_binary_fourth_field_pairs=82,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete conditional binary E16 exclusion via explicit short words and backward-closed four-cycle; no whole third/joint exclusion, F value or alphabet separation.')
    (ROOT/'b1_partial_cover_e16_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',kernel_controls=kernels,literal_pairs=[z['complete_normalized_row_pairs'] for z in literal],
        n13_full_letter_controls=port_controls['full_letter_assignments'],remaining_fourth_pairs=82)),flush=True)
if __name__=='__main__':main()
