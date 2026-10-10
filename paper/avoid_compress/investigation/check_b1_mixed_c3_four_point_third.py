"""Independent complete split kernels and normalized row controls.

The n=13 result is the accompanying symbolic proof, not an extrapolation
from the small controls. No arbitrary ordinary permutation is fixed.
"""
from collections import Counter
from itertools import combinations,permutations,product
from pathlib import Path
import hashlib,json
from alphabet_check import pair_distances,strong
ROOT=Path(__file__).resolve().parent
C={0,1,5};H={0,1,2};U={0,1};D=H|{6};Q=set(range(13));O={5}|set(range(6,13))
CT={tuple(v) for v in combinations(sorted(C),2)}

def partitions(values):
    answer=[]
    def visit(j,blocks):
        if j==len(values):answer.append(tuple(tuple(v) for v in blocks));return
        for block in blocks:
            block.append(values[j]);visit(j+1,blocks);block.pop()
        blocks.append([values[j]]);visit(j+1,blocks);blocks.pop()
    visit(0,[]);return answer

def pairs(blocks):return {tuple(v) for block in blocks for v in combinations(block,2)}

def f_cores():
    answer=[]
    for values in product(sorted(C),repeat=4):
        g=dict(zip(sorted(D),values));K={p for p in combinations(sorted(D),2) if g[p[0]]==g[p[1]]}
        if not K or len(CT|K)>4 or len(set(values))<2:continue
        extra=K-CT
        E=next(iter(extra)) if extra else (0,1)
        assert len(K)==1 or K=={(0,1),(2,6)}
        answer.append((g,E))
    assert len(answer)==42
    return answer

def l_kernels(RR,E):
    return [blocks for blocks in partitions(sorted(RR))
        if len(pairs(blocks)|CT|{E})<=4 and all(set(p)&H for p in pairs(blocks))]

def kernel_audit():
    RR={2}|set(range(6,13));rawL=partitions(sorted(RR));rawD=partitions(sorted(D))
    rawF=partitions([5]+list(range(7,13)))
    assert (len(rawL),len(rawD),len(rawF))==(4140,15,877)
    reports=[];Ltotal=0
    for E in sorted(set(E for g,E in f_cores())):
        kept=l_kernels(RR,E);assert len(kept)==(8 if E==(0,1) else 2 if E==(2,6) else 1)
        hist=Counter()
        for blocks in kept:
            kp=pairs(blocks)
            assert not kp or (len(kp)==1 and next(iter(kp))[0]==2)
            for values in permutations(sorted(RR),len(blocks)):
                inv={v:blocks[j] for j,v in enumerate(values)}
                off=[d for d in (2,6) if d in inv and set(inv[d])-H]
                assert off
                if not kp:
                    hist['bijective_L']+=1
                else:
                    extra=set(next(iter(kp)));mu=next(iter(RR-set(values)))
                    assert all(set(v)-H for v in blocks)
                    hist['missing_extra_endpoint' if mu in extra else 'outside_LL']+=1
                Ltotal+=1
        reports.append(dict(F_kernel=list(E),admitted_L_kernels=len(kept),L_output_assignments=sum(hist.values()),
            outcomes=dict(sorted(hist.items()))))
    assert Ltotal==564480
    Fhist=Counter()
    for values in permutations(sorted(RR),7):
        missing=next(iter(RR-set(values)))
        Fhist['missing_D_endpoint' if missing in (2,6) else 'outside_FFL']+=1
    assert sum(Fhist.values())==40320
    return dict(L_abstract_kernels=4140,F_D_abstract_kernels=15,F_R_abstract_kernels=877,
        F_D_core_maps=42,protected_core_maps=114,L_complete_output_assignments=Ltotal,
        F_complete_output_assignments=40320,L_reports=reports,F_output_outcomes=dict(sorted(Fhist.items())))

def protected(L,F,delta,mode):
    if mode==0:L[3]=3;L[4]=delta;F[3]=4;F[4]=3
    elif mode==1:L[3]=delta;L[4]=3;F[3]=3;F[4]=4
    else:L[3]=delta;L[4]=3;F[3]=4;F[4]=3

def star(v,T):return {tuple(sorted((v,t))) for t in T if v!=t}

def graph(kind,g,x=None):
    G={tuple(v) for v in combinations(sorted(H),2)}
    if kind=='join':return G|set().union(*(star(v,O) for v in H))
    if kind in ('U_join','U_join_two_star'):
        G|=set().union(*(star(v,O) for v in U))|{(2,6)}
        if kind=='U_join_two_star':G|=star(2,O-{5})
        return G
    u=next(v for v in U if g[v]==5);h=next(iter(U-{u}))
    G|=star(u,{5,6})|star(2,O-{5})
    if kind=='fixed_h':G|=star(h,O)
    else:
        assert kind=='chain_h';G|=star(h,{5,6,x})
    return G

def universal_graph(kind,g,E,Lkind,nu,mode,x=None,y=None,q=None,mu=None,e=None):
    G=graph(kind,g,x);RR={2}|set(range(6,13));J=set(range(7,13))
    lp=[-1]*13;fp=[-1]*13;protected(lp,fp,5,mode)
    L={v:{lp[v]} for v in (3,4)};F={v:{fp[v]} for v in (3,4)}
    L.update({v:{4} for v in C});F.update({v:{target} for v,target in g.items()})
    if Lkind=='singular':
        L.update({v:RR-{mu} for v in RR});LK=CT|{(2,q)}
    elif Lkind=='fix_two':
        L[2]={2};L.update({v:RR-{2} for v in RR-{2}});LK=CT
    else:
        assert Lkind=='E_permutation';L[2]={e};L[6]={next(iter({2,6}-{e}))}
        L.update({v:set(J) for v in J});LK=CT
    inputs={5}|J;targets=RR-{nu}
    if x is not None:
        F[x]={6};inputs.remove(x);targets.remove(6)
    if y is not None:
        F[y]={x};inputs.remove(y);targets.remove(x)
    F.update({v:set(targets) for v in inputs})
    assert set(L)==set(F)==Q and LK|CT|{E}<=G and (3,4) not in G
    checks=0
    for row in (L,F):
        for a,b in combinations(sorted(Q),2):
            if (a,b) not in G:
                assert not any(tuple(sorted((c,d))) in G for c in row[a] for d in row[b] if c!=d),(kind,a,b)
            checks+=1
    return checks

def graph_audit():
    hist=Counter();checks=0
    for g,E in f_cores():
        if g[6]!=5 or set(g.values())!=C:continue
        assert g[2]==5 or g[2] in U
        for mode in range(3):
            if E==(0,1):
                for q in range(6,13):
                    checks+=universal_graph('join',g,E,'singular',2,mode,q=q,mu=2);hist['join']+=1
            elif E in ((0,6),(1,6)):
                u=E[0];h=next(iter(U-{u}))
                for x in range(7,13):
                    if g[h]==h:
                        checks+=universal_graph('fixed_h',g,E,'fix_two',2,mode,x=x);hist['fixed_h']+=1
                    else:
                        for y in set(range(7,13))-{x}:
                            checks+=universal_graph('chain_h',g,E,'fix_two',2,mode,x=x,y=y);hist['chain_h']+=1
            elif E==(2,6):
                for nu in (2,6):
                    for mu in (2,6):
                        checks+=universal_graph('U_join',g,E,'singular',nu,mode,q=6,mu=mu);hist['U_join']+=1
                    for e in (2,6):
                        checks+=universal_graph('U_join',g,E,'E_permutation',nu,mode,e=e);hist['U_join']+=1
                checks+=universal_graph('U_join_two_star',g,E,'fix_two',2,mode);hist['U_join_two_star']+=1
    assert sum(hist.values())==312
    return dict(complete_symbolic_graph_configurations=sum(hist.values()),
        histogram=dict(sorted(hist.items())),set_valued_backward_checks=checks)

def off_pre(row,target):return next(i for i,v in enumerate(row) if v==target and i not in H)

def word_pair(L,F,pair,word,protected_pair=False):
    a,b=pair;assert a!=b
    if protected_pair:assert set(pair)&{3,4}
    else:assert not set(pair)&H
    for ch in word:
        row=L if ch=='L' else F;a,b=row[a],row[b]
    assert a==b,(pair,word)

def literal_graph(G,L,F):
    assert (3,4) not in G
    for row in (L,F):
        for a,b in combinations(range(len(row)),2):
            if row[a]==row[b]:assert (a,b) in G
            elif tuple(sorted((row[a],row[b]))) in G:assert (a,b) in G

def forward_pair_distances(L,F):
    # Ordinary forward BFS on unordered pair states, using integer labels.
    # This does not use the symbolic backward graphs or their case words.
    n=len(L);pp=list(combinations(range(n),2));trans=[[-2]*(n*n) for _ in range(2)]
    for j,row in enumerate((L,F)):
        for a,b in pp:
            c,d=row[a],row[b]
            trans[j][a*n+b]=-1 if c==d else min(c,d)*n+max(c,d)
    result={}
    for a,b in pp:
        start=a*n+b;todo=[start];depth=[0];seen=1<<start;pos=0;found=False
        while pos<len(todo) and not found:
            state=todo[pos];step=depth[pos]+1;pos+=1
            for j in (0,1):
                target=trans[j][state]
                if target==-1:
                    result[a,b]=step;found=True;break
                bit=1<<target
                if not seen&bit:
                    seen|=bit;todo.append(target);depth.append(step)
    return result

def verify_reason(L,F,g,E):
    RR={2}|set(range(6,len(L)));delta=L[3] if L[3]!=3 else L[4];p=next(v for v in (3,4) if L[v]==delta)
    LK={z for z in combinations(sorted(RR),2) if L[z[0]]==L[z[1]]}
    mu=next(iter(RR-set(L))) if LK else None
    if LK and mu not in set(next(iter(LK))):
        a,b=next(iter(LK));word_pair(L,F,(off_pre(L,a),off_pre(L,b)),'LL');return 'outside_LL'
    if delta in U:
        d=next(v for v in (2,6) if any(target==v and i not in H for i,target in enumerate(L)))
        word_pair(L,F,(p,off_pre(L,d)),'LFL');return 'outside_LFL_delta'
    if F[6] in U:
        d=next(v for v in (2,6) if v in F)
        word_pair(L,F,(6,off_pre(F,d)),'FFL');return 'outside_FFL_six'
    assert delta==F[6]==5
    nu=next(iter(RR-set(F)))
    if nu not in (2,6):
        word_pair(L,F,(off_pre(F,2),off_pre(F,6)),'FFL');return 'outside_FFL_missing'
    if not LK and L[2] not in (2,6):
        word_pair(L,F,(off_pre(L,2),off_pre(L,6)),'LFL');return 'outside_LFL_bijection'
    if LK and mu not in (2,6):
        word_pair(L,F,(off_pre(L,2),off_pre(L,6)),'LFL');return 'outside_LFL_singular'
    if E!=(2,6):
        if nu==6:
            x=off_pre(F,2);y=off_pre(F,x);word_pair(L,F,(x,y),'FFFL');return 'outside_F3L'
        x=off_pre(F,6)
        if (not LK and L[2]==6) or (LK and mu==6):
            word_pair(L,F,(off_pre(L,2),off_pre(L,x)),'LFFL');return 'outside_LF2L'
        if E in ((0,1),(0,2),(1,2)):
            if not LK:
                assert all(L[v] not in H and F[v] not in H for v in range(len(L)) if v not in H)
                return 'H_no_external_predecessor'
            literal_graph(graph('join',g),L,F);return 'backward_join'
        assert E in ((0,6),(1,6)) and not LK and L[2]==2
        if x==5:
            word_pair(L,F,(2,p),'LFFL',True);return 'protected_LF2L'
        u=E[0];h=next(iter(U-{u}))
        if g[h]==h:kind='fixed_h'
        else:
            y=off_pre(F,x)
            if y==5:
                word_pair(L,F,(2,p),'LFFFL',True);return 'protected_LF3L'
            assert y>=7;kind='chain_h'
        literal_graph(graph(kind,g,x),L,F);return 'backward_'+kind
    if LK:
        literal_graph(graph('U_join',g),L,F);return 'backward_U_join_singular'
    if nu==2 and L[2]==2:
        literal_graph(graph('U_join_two_star',g),L,F);return 'backward_U_join_two_star'
    other=next(iter({2,6}-{L[2]}));z=off_pre(L,other)
    if z!=6:
        if nu==2:
            word_pair(L,F,(off_pre(L,2),off_pre(L,z)),'LLF');return 'outside_L2F'
        word_pair(L,F,(off_pre(F,2),off_pre(F,z)),'FLF');return 'outside_FLF'
    literal_graph(graph('U_join',g),L,F);return 'backward_U_join_permutation'

def literal_family(n):
    RR={2}|set(range(6,n));J=set(range(7,n));total=0;hist=Counter();proof=Counter();byE={}
    kernel_cache={E:l_kernels(RR,E) for g,E in f_cores()}
    for g,E in f_cores():
        local=byE.setdefault(str(list(E)),Counter())
        deltas=[v for v in sorted(C) if {v}|set(g.values())==C]
        for delta,mode in product(deltas,range(3)):
            for blocks in kernel_cache[E]:
                for lv in permutations(sorted(RR),len(blocks)):
                    L=[-1]*n;Fb=[-1]*n;protected(L,Fb,delta,mode)
                    for v in C:L[v]=4
                    for block,target in zip(blocks,lv):
                        for v in block:L[v]=target
                    for values in permutations(sorted(RR),1+len(J)):
                        F=Fb.copy()
                        for v,target in g.items():F[v]=target
                        for v,target in zip([5]+sorted(J),values):F[v]=target
                        assert all(0<=v<n for v in L+F)
                        assert len({z for row in (L,F) for z in combinations(range(n),2) if row[z[0]]==row[z[1]]}|CT)<=4
                        reason=verify_reason(L,F,g,E);proof[reason]+=1
                        dist=forward_pair_distances(L,F)
                        if total<64:assert dist==pair_distances([L,F])
                        outside=[d for pair,d in dist.items() if not set(pair)&H and d<=5]
                        protected_bad=[d for pair,d in dist.items() if set(pair)&{3,4} and d<=6]
                        if outside:outcome='outside_pair_'+str(min(outside))
                        elif protected_bad:outcome='protected_pair_'+str(min(protected_bad))
                        elif not strong([L,F]):outcome='not_strongly_connected'
                        else:
                            assert len(dist)<n*(n-1)//2;outcome='nonsynchronizing'
                        hist[outcome]+=1;local[outcome]+=1;total+=1
    assert total=={7:1872,8:18792,9:331776}[n]
    return dict(n=n,complete_row_assignments=total,outcomes=dict(sorted(hist.items())),
        symbolic_case_checks=dict(sorted(proof.items())),by_F_kernel={k:dict(sorted(v.items())) for k,v in sorted(byE.items())},
        scope='Complete small normalized row control under the stated pair-cover and protected-isolation premises, not an n-state F bound')

def frontier():
    data=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    joint=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))
    identity='b1_out_c5_third11';record=next(z for z in data['records'] if z['id']==identity)
    assert record['D']==[0,1,2,6] and len(record['binary_profile_pairs'])==3
    oldjoint={z['id'] for z in joint['records'] if len(z['B'])==3}|{'b2_mixed_c12','b1_out_c6','b1_in_c5'}
    oldthird={f'b1_out_c5_third{i}' for i in (1,2,3,4,5,7,8,9,11)}
    kept=[z for z in data['records'] if z['joint_id'] not in oldjoint and z['id'] not in oldthird and z['binary_profile_pairs']]
    assert len(kept)==165 and sum(len(z['binary_profile_pairs']) for z in kept)==918
    Ds=[z['D'] for z in kept if z['joint_id']=='b1_out_c5'];assert Ds==[[2,6],[0,2,6]]
    return dict(additional_binary_third_profile_exclusions=[identity],b1_C3_mixed_remaining_D=Ds,
        remaining_binary_joint=26,remaining_unrestricted_joint=43,remaining_binary_typed_third_orbits=165,
        remaining_binary_profile_pairs=918,extremal_interval=[11,12])

def main():
    K=kernel_audit();graphs=graph_audit();literal=[]
    for n in (7,8,9):
        literal.append(literal_family(n));print(json.dumps(dict(control_n=n,assignments=literal[-1]['complete_row_assignments'])),flush=True)
    front=frontier()
    names=[Path(__file__).name,'B1_MIXED_C3_FOUR_POINT_THIRD_EXCLUSION.md','ENTRY_FIBER_FLAG.md',
        'SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md','LOCAL_EQUALITY_FLAG.md',
        'CODIMENSION_FOUR_P5_DICHOTOMY.md','SINGLETON_THREE_KERNEL_EXCLUSION.md',
        'small_first_third_inventory.json','joint_fiber_orbits.json','alphabet_check.py']
    result=dict(status='pass',parameter=[13,9,1],kernels=K,universal_graphs=graphs,
        complete_literal_small_families=literal,frontier=front,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Conditional binary D={0,1,2,6} symbolic exclusion with complete finite kernel/graph cover and independent normalized row controls. No full thirteen-state scan, new F value or alphabet separation.')
    (ROOT/'b1_mixed_c3_four_point_third_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',graph_configurations=graphs['complete_symbolic_graph_configurations'],
        literal_rows=[v['complete_row_assignments'] for v in literal],frontier=front)),flush=True)

if __name__=='__main__':main()
