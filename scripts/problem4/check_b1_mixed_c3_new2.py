"""Independent complete kernels, finite core cover and small literal row controls.

The thirteen-state exclusion is symbolic. Small j=0,1 completed row scans
are independent controls, not an extrapolation to all ordinary permutations.
"""
from collections import Counter
from itertools import combinations,permutations,product
from pathlib import Path
import hashlib,json,math
from alphabet_check import pair_distances,strong

ROOT=Path(__file__).resolve().parent
C={0,1,5};H={0,1,2};A={3};B={4};Q=set(range(13));O=set(range(6,13));R=O|{2}
BASE={tuple(v) for v in combinations(sorted(C),2)}|{(2,6)}
CASES=[{0},{5},{0,1},{0,5}]

def partitions(values):
    answer=[]
    def visit(j,blocks):
        if j==len(values):answer.append(tuple(tuple(v) for v in blocks));return
        for v in blocks:v.append(values[j]);visit(j+1,blocks);v.pop()
        blocks.append([values[j]]);visit(j+1,blocks);blocks.pop()
    visit(0,[]);return answer

def pairs(blocks):return {tuple(v) for block in blocks for v in combinations(block,2)}

def kernels():
    raw=partitions(sorted(R));moving=[]
    for blocks in raw:
        p=pairs(blocks)
        if not p or len(p)>1 or any(not set(v)&H for v in p):continue
        moving.append(blocks)
    assert len(raw)==4140 and len(moving)==7
    assert {next(iter(pairs(v))) for v in moving}=={(2,q) for q in sorted(O)}
    reports=[]
    for U in CASES:
        V=C-U;inputs=V|O;allk=partitions(sorted(inputs));admitted=[]
        for blocks in allk:
            if len(blocks)>8 or not pairs(blocks)<=BASE:continue
            admitted.append(blocks)
        assert len(admitted)==1 and len(admitted[0])==8
        assert {frozenset(v) for v in admitted[0]}=={frozenset(V)}|{frozenset([q]) for q in O}
        off_blocks=[block for block in admitted[0] if set(block)-H]
        if 5 in V:assert len(off_blocks)==8
        else:assert len(off_blocks)==7
        reports.append(dict(U=sorted(U),D=sorted(U|{2}),abstract_kernels=len(allk),
            admitted_kernels=1,blocks_with_nonH_input=len(off_blocks)))
    assert sum(v['abstract_kernels'] for v in reports)==50574
    # Independently check every injection of the fixed E+J blocks to R.
    blocks=[{2,6}]+[{q} for q in range(7,13)];injections=omitted_not_E=0
    for mu in sorted(R):
        for outputs in permutations(sorted(R-{mu})):
            injections+=1;pre=dict(zip(outputs,blocks))
            assert all(block-H for block in pre.values())
            if mu not in (2,6):
                omitted_not_E+=1
                x=next(iter(pre[2]-H));y=next(iter(pre[6]-H));assert x!=y
    assert injections==40320 and omitted_not_E==30240
    return dict(L_abstract_kernels=4140,L_admitted_unlabelled_extra_partner_kernels=7,
        F_R_kernel_reports=reports,F_abstract_kernels=50574,
        fixed_E_R_output_injections=injections,omissions_outside_E_rejected_by_LL=omitted_not_E)

def core_maps(U):
    D=U|{2};answer=[]
    for delta,values in product(sorted(C),product(sorted(C),repeat=len(D))):
        g=dict(zip(sorted(D),values))
        fp={tuple(v) for v in combinations(sorted(D),2) if g[v[0]]==g[v[1]]}
        if not fp<=BASE:continue
        if {delta}|set(g.values())!=C:continue
        answer.append((delta,g))
    assert len(answer)==(6 if len(U)==1 else 24)
    return answer

def classify(U,delta,g,e,mu,x):
    if e==2:
        if mu==2:return 'ordinary_closed'
        if delta in U:return 'outside_LFL_D'
        if x!=6:return 'outside_LFL_E'
        return 'q_only_self_incoming'
    assert e==6
    if g[5] in U:return 'outside_FFL_D'
    if x!=6:return 'outside_FFL_E'
    if delta in U and mu==6:return 'outside_LFL_D'
    if delta not in U and mu==2:return 'outside_LFL_E'
    if U=={5}:
        return 'outside_F3L' if delta==5 else 'backward_graph_U5'
    assert U=={0,5} and g[5]==1
    if g[0]==1:return 'backward_graph_U05'
    if g[0]==0 and g[2]==5:
        return 'outside_LF2L' if delta==0 else 'zero_only_self_incoming'
    assert g[0]==5 and g[2]==0
    return 'outside_F4L'

def graph_for(reason):
    if reason=='backward_graph_U5':return BASE|{(2,5),(0,6),(1,6)}
    assert reason=='backward_graph_U05'
    return BASE|{(0,2),(2,5),(1,6)}

def protected(L,F,delta,mode):
    if mode==0:L[3]=3;L[4]=delta;F[3]=4;F[4]=3
    elif mode==1:L[3]=delta;L[4]=3;F[3]=3;F[4]=4
    else:L[3]=delta;L[4]=3;F[3]=4;F[4]=3

def universal_graph(U,delta,g,mu,reason,mode):
    G=graph_for(reason);L={q:set(R-{mu}) for q in R};F={q:set(range(7,13)) for q in range(7,13)}
    lp=[-1]*13;fp=[-1]*13;protected(lp,fp,delta,mode)
    L.update({q:{lp[q]} for q in (3,4)});F.update({q:{fp[q]} for q in (3,4)})
    L.update({q:{4} for q in C})
    F.update({q:{v} for q,v in g.items()});F.update({q:{6} for q in C-U});F[6]={2}
    assert set(L)==set(F)==Q and (3,4) not in G
    # Only distinct output pairs are tested. Direct kernels are separately BASE.
    for possible in (L,F):
        for x,y in combinations(sorted(Q),2):
            if (x,y) in G:continue
            assert not any(tuple(sorted((u,v))) in G for u in possible[x] for v in possible[y] if u!=v)
    return 2*len(list(combinations(Q,2)))

def core_audit():
    reports=[];closures=0
    for U in ({5},{0,5}):
        hist=Counter();canonical=Counter()
        for delta,g in core_maps(U):
            for e,mu,x in product((2,6),(2,6),(6,7)):
                reason=classify(U,delta,g,e,mu,x);hist[reason]+=1
                if e==6 and x==6 and g[5] not in U and mu==(2 if delta in U else 6):
                    canonical[reason]+=1
                    if reason.startswith('backward_graph'):
                        for mode in range(3):closures+=universal_graph(U,delta,g,mu,reason,mode)
        assert sum(hist.values())==(48 if U=={5} else 192)
        assert sum(canonical.values())==(4 if U=={5} else 8)
        reports.append(dict(U=sorted(U),port_configurations=sum(hist.values()),histogram=dict(sorted(hist.items())),
            canonical_core_cases=sum(canonical.values()),canonical_histogram=dict(sorted(canonical.items()))))
    return dict(reports=reports,port_configurations=240,canonical_core_cases=12,
                universal_set_valued_backward_pair_checks=closures)

def word_pair(L,F,pair,word):
    x,y=pair
    for letter in word:
        row=L if letter=='L' else F;x,y=row[x],row[y]
    assert x==y

def pre_nonH(row,target):
    q=next(q for q,v in enumerate(row) if v==target and q not in H)
    return q

def verify_reason(U,delta,g,L,F,mu):
    if 5 in C-U:
        pair=(pre_nonH(F,2),pre_nonH(F,6));word_pair(L,F,pair,'FL');return 'outside_FL'
    V=C-U;e=F[next(iter(V))]
    if mu not in (2,6):
        word_pair(L,F,(pre_nonH(L,2),pre_nonH(L,6)),'LL');return 'outside_LL'
    if e not in (2,6):
        word_pair(L,F,(pre_nonH(F,2),pre_nonH(F,6)),'FL');return 'outside_FL'
    x=next(q for q,v in enumerate(F) if v==(6 if e==2 else 2));reason=classify(U,delta,g,e,mu,x)
    if reason=='ordinary_closed':
        ordinary=set(range(6,len(L)));assert all(L[q] in ordinary and F[q] in ordinary for q in ordinary)
    elif reason=='q_only_self_incoming':
        assert all(v!=6 for v in L) and [q for q,v in enumerate(F) if v==6]==[6]
    elif reason=='zero_only_self_incoming':
        assert all(v!=0 for v in L) and [q for q,v in enumerate(F) if v==0]==[0]
    elif reason.startswith('backward_graph'):
        G=graph_for(reason)
        for row in (L,F):
            for p,q in combinations(range(len(row)),2):
                if row[p]==row[q]:assert (p,q) in G
                elif tuple(sorted((row[p],row[q]))) in G:assert (p,q) in G
    elif reason=='outside_LFL_D':
        word_pair(L,F,(pre_nonH(L,delta),pre_nonH(L,2)),'LFL')
    elif reason=='outside_LFL_E':
        target=x if e==2 else 6
        word_pair(L,F,(pre_nonH(L,delta),pre_nonH(L,target)),'LFL')
    elif reason=='outside_FFL_D':
        word_pair(L,F,(5,pre_nonH(F,2)),'FFL')
    elif reason=='outside_FFL_E':
        word_pair(L,F,(5,pre_nonH(F,x)),'FFL')
    elif reason=='outside_F3L':word_pair(L,F,(5,6),'FFFL')
    elif reason=='outside_LF2L':word_pair(L,F,(pre_nonH(L,0),pre_nonH(L,6)),'LFFL')
    elif reason=='outside_F4L':word_pair(L,F,(5,6),'FFFFL')
    else:raise AssertionError(reason)
    return reason

def literal_family(jcount):
    n=7+jcount;ordinary=set(range(6,n));Rlocal=ordinary|{2};Js=set(range(7,n));total=0
    outcomes=Counter();proof=Counter();byU={}
    for U in CASES:
        V=C-U;D=U|{2};local=Counter();count=0
        for delta,g in core_maps(U):
            for mode in range(3):
                for mu in sorted(Rlocal):
                    for lv in permutations(sorted(Rlocal-{mu})):
                        L=[-1]*n;Fbase=[-1]*n;protected(L,Fbase,delta,mode)
                        for q in C:L[q]=4
                        for block,target in zip([{2,6}]+[{q} for q in sorted(Js)],lv):
                            for q in block:L[q]=target
                        for fv in permutations(sorted(Rlocal)):
                            F=Fbase.copy()
                            for q,v in g.items():F[q]=v
                            for block,target in zip([V]+[{q} for q in sorted(ordinary)],fv):
                                for q in block:F[q]=target
                            assert all(0<=v<n for v in L+F)
                            reason=verify_reason(U,delta,g,L,F,mu);proof[reason]+=1
                            dist=pair_distances([L,F]);short=[d for (x,y),d in dist.items() if x not in H and y not in H and d<=5]
                            if short:result='uncovered_pair_depth_'+str(min(short))
                            elif not strong([L,F]):result='not_strongly_connected'
                            else:
                                assert len(dist)<n*(n-1)//2
                                result='nonsynchronizing'
                            outcomes[result]+=1;local[result]+=1;total+=1;count+=1
        assert count==len(core_maps(U))*3*math.factorial(jcount+2)**2
        byU[str(sorted(U))]=dict(assignments=count,outcomes=dict(sorted(local.items())))
    assert total==60*3*math.factorial(jcount+2)**2
    return dict(n=n,J_points=jcount,complete_row_assignments=total,outcomes=dict(sorted(outcomes.items())),
                symbolic_case_checks=dict(sorted(proof.items())),by_U=byU,
                scope='Complete small normalized kernel-row controls, not an n-state F bound')

def frontier():
    data=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    joint=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))
    subset=[z for z in data['records'] if z['joint_id']=='b1_out_c5']
    excluded=[z['id'] for z in subset if set(z['D']) in [U|{2} for U in CASES]]
    assert excluded==['b1_out_c5_third3','b1_out_c5_third5','b1_out_c5_third7','b1_out_c5_third9']
    assert all(len(z['binary_profile_pairs'])==3 for z in subset if z['id'] in excluded)
    remaining=[z for z in subset if z['id'] not in excluded+['b1_out_c5_third1']]
    assert [z['D'] for z in remaining]==[[6],[0,6],[2,6],[0,1,6],[0,2,6],[0,1,2,6]]
    oldjoint={z['id'] for z in joint['records'] if len(z['B'])==3}|{'b2_mixed_c12','b1_out_c6','b1_in_c5'}
    oldthird=set(excluded)|{'b1_out_c5_third1'}
    admitted=[z for z in data['records'] if z['joint_id'] not in oldjoint and z['id'] not in oldthird and z['binary_profile_pairs']]
    assert len(admitted)==169 and sum(len(z['binary_profile_pairs']) for z in admitted)==930
    return dict(additional_binary_third_profile_exclusions=excluded,b1_C3_mixed_remaining_D=[z['D'] for z in remaining],
        remaining_binary_joint=26,remaining_unrestricted_joint=43,remaining_binary_typed_third_orbits=169,
        remaining_binary_profile_pairs=930,extremal_interval=[11,12])

def main():
    K=kernels();core=core_audit();literal=[literal_family(j) for j in (0,1)];front=frontier()
    names=[Path(__file__).name,'PROOF.md#problem4-b1-mixed-c3-new-point-2-exclusion','PROOF.md#problem4-binary-singleton-first-second-cover',
        'PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-second-entrance-fiber','PROOF.md#problem4-third-entrance-space','PROOF.md#problem4-local-equality-flag',
        'PROOF.md#problem4-codimension-four-p5-dichotomy','PROOF.md#problem4-singleton-three-kernel-exclusion',
        'small_first_third_inventory.json','joint_fiber_orbits.json','alphabet_check.py']
    result=dict(status='pass',parameter=[13,9,1],proof='PROOF.md#problem4-b1-mixed-c3-new-point-2-exclusion',
        kernels=K,core_cases=core,complete_literal_small_families=literal,frontier=front,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Symbolic binary exclusion of four third profiles. Complete abstract kernels/core-port checks and independent literal small-row controls. No full thirteen-state scan, new F value or alphabet separation.')
    (ROOT/'b1_mixed_c3_new2_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',F_kernel_partitions=K['F_abstract_kernels'],L_kernel_partitions=4140,
        L_output_injections=40320,core_ports=240,canonical_cores=12,
        literal_rows=[v['complete_row_assignments'] for v in literal],frontier=front)))

if __name__=='__main__':main()
