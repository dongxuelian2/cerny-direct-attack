"""Exact singleton-D kernel/permutation controls and independent literal rows."""
from collections import Counter
from itertools import combinations,permutations,product
from pathlib import Path
import hashlib,json
from alphabet_check import pair_distances,strong
ROOT=Path(__file__).resolve().parent
C={0,1,5};H={0,1,2};R={2}|set(range(6,13));E={2,7}
G={tuple(v) for v in combinations(sorted(C),2)}|{(2,7)}

def partitions(values):
    work=[()]
    for q in values:
        following=[]
        for blocks in work:
            following.append(blocks+((q,),))
            for j in range(len(blocks)):
                following.append(blocks[:j]+(blocks[j]+(q,),)+blocks[j+1:])
        work=following
    return work

def kernels():
    full=partitions(sorted(R));kept=[]
    for blocks in full:
        p={tuple(v) for block in blocks for v in combinations(block,2)}
        if p<=G:kept.append(blocks)
    assert len(full)==4140 and len(kept)==2
    assert sorted(map(len,kept))==[7,8]
    assert all(set(v)-H for blocks in kept if len(blocks)==7 for v in blocks)
    counts=Counter()
    for values in permutations(sorted(R)):
        F=dict(zip(sorted(R),values));inverse={v:q for q,v in F.items()}
        if F[2] not in E:
            pair={inverse[2],inverse[7]};assert not pair&H;counts['outside_FL']+=1
        elif F[2]==7:
            if F[7]!=2:
                pair={inverse[inverse[2]],inverse[inverse[7]]};assert not pair&H
                counts['outside_F2L']+=1
            else:counts['swap_E_backward_graph']+=1
        else:
            assert F[2]==2
            if F[7]==7:counts['fixed_q_self_only_if_L_misses_q']+=1
            else:
                x=inverse[7];assert x!=7 and x not in H
                counts['outside_LFL_if_L_misses_q']+=1
    assert sum(counts.values())==40320
    return dict(R_abstract_kernels=4140,F_admitted_kernels=2,F_R_permutations=40320,
        permutation_case_histogram=dict(sorted(counts.items())))

def closure_controls():
    # L: pre(C)={6}; missing one E endpoint. F: pre(C)=C and either
    # missing an E endpoint or permuting E. Other inputs have R outputs.
    tests=0
    for mu,nu in product((2,7),(2,7,'swap')):
        L={q:{4} for q in C};L[6]=set(C)
        # The two protected inputs can output a and an R point. Each is
        # considered with conservative R possibilities; neither can form G.
        L.update({q:{3}|(R-{mu}) for q in (3,4)})
        L.update({q:R-{mu} for q in R-{6}})
        F={q:set(C) for q in C};F.update({3:{3,4},4:{3,4}})
        if nu=='swap':
            F[2]={7};F[7]={2};F.update({q:R-E for q in R-E})
        else:F.update({q:R-{nu} for q in R})
        for possible in (L,F):
            for x,y in combinations(range(13),2):
                if (x,y) in G:continue
                assert not any(tuple(sorted((u,v))) in G for u in possible[x] for v in possible[y] if u!=v)
                tests+=1
    return tests

def literal():
    n=8;RR={2,6,7};count=0;hist=Counter()
    for delta,cv in product(sorted(C),product(sorted(C),repeat=3)):
        fC=dict(zip(sorted(C),cv))
        if {delta}|set(cv)!=C:continue
        for mode in range(3):
            for mu in sorted(RR):
                for lv in permutations(sorted(RR-{mu})):
                    L=[-1]*n;Fbase=[-1]*n
                    if mode==0:p,r=3,4;Fbase[3]=4;Fbase[4]=3
                    elif mode==1:p,r=4,3;Fbase[3]=3;Fbase[4]=4
                    else:p,r=4,3;Fbase[3]=4;Fbase[4]=3
                    L[p]=3;L[6]=delta
                    for q in C:L[q]=4
                    L[r]=lv[0];L[2]=L[7]=lv[1]
                    mappings=[dict(zip(sorted(RR),v)) for v in permutations(sorted(RR))]
                    for targets in permutations(sorted(RR),2):
                        mappings.append({2:targets[0],7:targets[0],6:targets[1]})
                    assert len(mappings)==12
                    for mapR in mappings:
                        F=Fbase.copy()
                        for q,v in (fC|mapR).items():F[q]=v
                        assert all(v>=0 for v in L+F)
                        assert {tuple(v) for row in (L,F) for v in combinations(range(n),2) if row[v[0]]==row[v[1]]}<=G
                        d=pair_distances([L,F]);outside=[v for pair,v in d.items() if not set(pair)&H and v<=5]
                        if outside:reason='outside_pair_'+str(min(outside))
                        elif not strong([L,F]):reason='not_strongly_connected'
                        else:
                            assert len(d)<28;reason='nonsynchronizing'
                        hist[reason]+=1;count+=1
    assert count==7776
    return dict(n=n,complete_row_assignments=count,outcomes=dict(sorted(hist.items())),
        scope='Entire small normalized row control; the n=13 result uses the symbolic proof')

def main():
    K=kernels();closures=closure_controls();small=literal()
    data=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    joint=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))
    target=next(z for z in data['records'] if z['id']=='b1_out_c5_third2')
    assert target['D']==[6] and len(target['binary_profile_pairs'])==3
    excluded_joint={z['id'] for z in joint['records'] if len(z['B'])==3}|{'b2_mixed_c12','b1_out_c6','b1_in_c5'}
    excluded_third={f'b1_out_c5_third{i}' for i in (1,2,3,5,7,9)}
    remaining=[z for z in data['records'] if z['joint_id'] not in excluded_joint and z['id'] not in excluded_third and z['binary_profile_pairs']]
    assert len(remaining)==168 and sum(len(z['binary_profile_pairs']) for z in remaining)==927
    Ds=[z['D'] for z in remaining if z['joint_id']=='b1_out_c5']
    assert Ds==[[0,6],[2,6],[0,1,6],[0,2,6],[0,1,2,6]]
    names=[Path(__file__).name,'B1_MIXED_C3_SINGLETON_EXCLUSION.md',
        'BINARY_SINGLETON_FIRST_SECOND_COVER.md','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md',
        'THIRD_ENTRANCE_SPACE.md','LOCAL_EQUALITY_FLAG.md','CODIMENSION_FOUR_P5_DICHOTOMY.md',
        'SINGLETON_THREE_KERNEL_EXCLUSION.md','small_first_third_inventory.json','joint_fiber_orbits.json','alphabet_check.py']
    result=dict(status='pass',parameter=[13,9,1],kernels=K,universal_backward_checks=closures,literal_control=small,
        frontier=dict(additional_binary_third_profile_exclusions=['b1_out_c5_third2'],
            b1_C3_mixed_remaining_D=Ds,remaining_binary_joint=26,remaining_unrestricted_joint=43,
            remaining_binary_typed_third_orbits=168,remaining_binary_profile_pairs=927,extremal_interval=[11,12]),
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Symbolic binary singleton-D exclusion, exact kernel/permutation/closure checks and a complete independent small row-family control. No full thirteen-state row scan, new F value or alphabet separation.')
    (ROOT/'b1_mixed_c3_singleton_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',R_kernels=4140,F_R_permutations=40320,literal_rows=7776,frontier=result['frontier'])))

if __name__=='__main__':main()
