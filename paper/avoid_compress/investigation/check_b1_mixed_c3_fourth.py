"""Exact local fourth-entrance controls; no full automaton scan."""
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations, product
from collections import Counter
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parent
Q=set(range(13)); A={3}; B={4}; C={0,1,5}; D={2,6}; H={0,1,2}; J=set(range(7,13))

def chi(X):return [int(q in X) for q in range(13)]
def h(X):return [9*int(q in X)-1 for q in range(13)]
def sub(X,Y):return [x-y for x,y in zip(chi(X),chi(Y))]
def rank(rows):
    work=[[Fraction(x) for x in row] for row in rows]; r=0
    for j in range(13):
        p=next((i for i in range(r,len(work)) if work[i][j]),None)
        if p is None:continue
        work[r],work[p]=work[p],work[r]; v=work[r][j]
        work[r]=[x/v for x in work[r]]
        for i in range(r+1,len(work)):
            v=work[i][j]
            if v:work[i]=[x-v*y for x,y in zip(work[i],work[r])]
        r+=1
    return r

def subsets(X):
    return [set(z) for k in range(len(X)+1) for z in combinations(sorted(X),k)]

def base(E):return [h(X) for X in (A,B,C,D,E)]

def rank_controls():
    counters=Counter(); WD=subsets(D)
    # E=017, both letters use D as preimage(C).
    K=base({0,1,7})
    for rf,rl,wf,wl in product([5,*sorted(J-{7})],sorted(J),WD,WD):
        actual=rank(K+[sub({rf},wf),sub({rl},wl)])<=6
        predicted=((rf==5 and rl==7) or rf==rl) and wf==wl
        assert actual==predicted,('017',rf,rl,wf,wl,actual,predicted)
        counters['E017_two_D_columns']+=1;counters['E017_rank_admitted']+=actual
    # E=07, both letters use D as preimage(C).
    K=base({0,7}); Ps=[{1,5},{5}]+[{1,j} for j in sorted(J-{7})]+[{j} for j in sorted(J-{7})]
    for P,rl,wf,wl in product(Ps,sorted(J),WD,WD):
        actual=rank(K+[h(wf|P),h(wl|{rl})])<=6
        geometry=(P=={1,5} and rl==7) or (len(P)==1 and P!={5} and P=={rl})
        predicted=geometry and wf==wl
        assert actual==predicted,('07',P,rl,wf,wl,actual,predicted)
        counters['E07_two_D_columns']+=1;counters['E07_rank_admitted']+=actual
    for P,rl,wf in product(Ps,sorted(J),[{2},{6}]):
        assert rank(K+[h({rl})])==6
        assert rank(K+[h({rl}),h(wf|P)])==7
        counters['E07_constant_C_columns']+=1
    # E=27, F constant-D: first exclude rF=7 by short counts, then rank.
    K=base({2,7}); KE=subsets({2,7})
    for rf,rl,k in product(sorted(J-{7}),[6,*sorted(J-{7})],KE):
        actual=rank(K+[h({rf}),sub({rl},k)])<=6
        predicted=(rl==6 and k=={7}) or (rl==rf and k=={2,7})
        assert actual==predicted,('27constant',rf,rl,k,actual,predicted)
        counters['E27_constant_D_columns']+=1;counters['E27_constant_rank_admitted']+=actual
    # E=27, F preimage(D)=C with proper nonempty W preimage(6).
    for W,rf,rl,k in product([w for w in subsets(C) if w and w!=C],sorted(J),[6,*sorted(J-{7})],KE):
        actual=rank(K+[sub({rf},W),sub({rl},k)])<=6
        predicted=rl==6 and k=={7}
        assert actual==predicted,('27proper',W,rf,rl,k,actual,predicted)
        counters['E27_proper_C_columns']+=1;counters['E27_proper_rank_admitted']+=actual
    return dict(counters)

def admission_controls():
    data=json.loads((ROOT/'b1_mixed_c3_fourth_inventory.json').read_text(encoding='utf-8'))
    old=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    old=next(z for z in old['records'] if z['id']=='b1_out_c5_third6')
    oldpairs={tuple(z) for z in old['binary_profile_pairs']}
    candidates=[X for X in subsets(Q-A-B) if X and len(X-H)<=1]
    labelled=0; fiber_tests=0; counts=Counter(); rows_checked=0; forms_checked=0
    for j,U in product(sorted(J),subsets(H)):
        E={j}|U; K=base(E);assert rank(K)==5
        admitted=[R for R in candidates if rank(K+[h(R)])==5]
        assert {tuple(sorted(R)) for R in admitted}=={tuple(sorted(R)) for R in (C,D,E)}
        fiber_tests+=len(candidates);labelled+=1
        signature=(len(U&{0,1}),int(2 in U));counts[signature]+=1
    assert labelled==48 and sum(z['labelled_orbit_size'] for z in data['records'])==48
    for z in data['records']:
        E=set(z['E']);F=dict(A=A,B=B,C=C,D=D,E=E)
        base_rows=[(set(v['preA']),set(v['preB']),set(v['preC'])) for v in old['rows']]
        expected=[]
        for i,inputs in enumerate(base_rows):
            for tag,R in F.items():
                parts=[*inputs,R]
                if len(set().union(*parts))!=sum(map(len,parts)):continue
                parts.append(Q-set().union(*parts))
                expected.append((i,tag,[min(len(x),len(y)) for x,y in zip(parts,[A,B,C,D,J])]))
        actual=[(v['base_row'],v['preimage_word'][3],v['capacity']) for v in z['rows']]
        assert expected==actual;rows_checked+=len(actual)
        pairs=[]
        for i,j in combinations_with_replacement(range(len(actual)),2):
            x,y=actual[i],actual[j]
            if tuple(sorted((x[0],y[0]))) not in oldpairs:continue
            if x[1]!='E' and y[1]!='E':continue
            if any(u+v<target for u,v,target in zip(x[2],y[2],[1,1,3,2,6])):continue
            pairs.append([i,j])
        assert pairs==z['binary_fourth_profile_pairs']
        actualforms={tuple(sorted(A|B|{v['c'],v['d']}|(J-{v['hole']}))) for v in z['nine_set_forms']}
        allnine=[set(T) for T in combinations(range(13),9)]
        literal={tuple(sorted(T)) for T in allnine if A|B<=T and len(T&C)==len(T&D)==len(T&E)==1}
        assert actualforms==literal;forms_checked+=len(literal)
    assert [len(z['binary_fourth_profile_pairs']) for z in data['records']]==[41,6,9,6,0,0]
    return dict(labelled_fourth_sets=labelled,covered_boolean_fiber_rank_tests=fiber_tests,
        row_fields=rows_checked,fourth_field_pairs=[41,6,9,6,0,0],nine_set_forms=forms_checked,
        remaining_fourth_shape=[7],remaining_original_pairs=14,remaining_full_fourth_pairs=41)

def row_kernel(row):
    blocks={}
    for q,t in enumerate(row):blocks.setdefault(t,[]).append(q)
    return {tuple(z) for X in blocks.values() for z in combinations(X,2)}

def toy_rows(n,z,rowid):
    E=set(z['E']);targets=[A,B,C,D,set(range(7,n))]
    sets=dict(A=A,B=B,C=C,D=D,E=E);word=z['rows'][rowid]['preimage_word']
    inputs=[sets[k] for k in word];inputs.append(set(range(n))-set().union(*inputs))
    positions=[q for X in inputs for q in sorted(X)]
    options=[sorted(T) for X,T in zip(inputs,targets) for q in sorted(X)]
    result=[]
    for values in product(*options):
        row=[-1]*n
        for q,t in zip(positions,values):row[q]=t
        kernel=row_kernel(row)
        if len(kernel)>4 or any(not set(p)&H or set(p)&{3,4} for p in kernel):continue
        result.append((tuple(row),kernel))
    return result

def strong(rows):
    n=len(rows[0])
    for reverse in (False,True):
        adj=[set() for q in range(n)]
        for row in rows:
            for q,t in enumerate(row):adj[t if reverse else q].add(q if reverse else t)
        seen={0};todo=[0]
        while todo:
            for q in adj[todo.pop()]-seen:seen.add(q);todo.append(q)
        if len(seen)<n:return False
    return True

def synchronizing(rows):
    n=len(rows[0]);seen=set();todo=[];reverse={p:set() for p in combinations(range(n),2)}
    for p in reverse:
        for row in rows:
            image=tuple(sorted({row[q] for q in p}))
            if len(image)==1:seen.add(p);todo.append(p)
            else:reverse[image].add(p)
    while todo:
        for p in reverse[todo.pop()]-seen:seen.add(p);todo.append(p)
    return len(seen)==n*(n-1)//2

def prefix_failure(rows,T,E):
    visited={frozenset(T)};current=visited.copy()
    for depth in range(1,8):
        new=set()
        for V in current:
            for row in rows:
                W=frozenset(row[q] for q in V)
                if len(W)!=len(T) or not A|B<=W or len(W&C)!=1 or len(W&D)!=1 or len(W&E)!=1:return depth
                if W not in visited:new.add(W)
        visited|=new;current=new
        if not current:return None
    return None

def E017_constant_C_count_controls():
    # Literal thirteen-state rows, every ordinary bijection; this is one
    # complete parameterized letter family, not all pairs of rows.
    inputs=[5,*sorted(J-{7})];rows=0;controls=0
    for prot,cv,dv,jv in product((0,1),permutations((0,1)),product(sorted(D),repeat=3),permutations(sorted(J))):
        F=[-1]*13;F[3]=3 if prot==0 else 4;F[4]=4 if prot==0 else 3
        F[2],F[6]=cv
        for q,t in zip((0,1,7),dv):F[q]=t
        for q,t in zip(inputs,jv):F[q]=t
        assert all(t>=0 for t in F);rows+=1
        if F[5]!=7:
            initial=[A|B|{0,d}|(J-{7}) for d in D]
        else:
            initial=[A|B|{5,d}|(J-{hole}) for d,hole in product(D,J-{7})]
        for T in initial:
            U={F[q] for q in T}
            assert len(U)==9 and len(U&C)==len(U&D)==1 and A|B<=U
            assert (7 in U)!=(5 in U);controls+=1
    assert rows==23040 and controls==76800
    return dict(parameterized_n13_F_rows=rows,nine_set_count_controls=controls,
        scope='All ordinary bijections in the E017/constant-C second-step contradiction; not full n=13 transition-pair enumeration')

def literal_controls(n):
    data=json.loads((ROOT/'b1_mixed_c3_fourth_inventory.json').read_text(encoding='utf-8'))
    total=0;hist=Counter();controls=0
    for z in data['records'][1:4]:
        E=set(z['E']);Jtoy=set(range(7,n))
        initial=[A|B|{c,d}|(Jtoy-{hole}) for c,d,hole in product(C,D,Jtoy)]
        initial=[T for T in initial if len(T&E)==1]
        cache={i:toy_rows(n,z,i) for ij in z['binary_fourth_profile_pairs'] for i in ij}
        for i,j in z['binary_fourth_profile_pairs']:
            for (x,kx),(y,ky) in product(cache[i],cache[j]):
                if len(kx|ky)>4:continue
                total+=1
                if not strong((x,y)):hist['not_strong']+=1;continue
                if not synchronizing((x,y)):hist['not_synchronizing']+=1;continue
                for T in initial:
                    failure=prefix_failure((x,y),T,E)
                    assert failure is not None,('unresolved_toy',n,z['E'],x,y,sorted(T))
                    hist['entrance_prefix_'+str(failure)]+=1;controls+=1
    return dict(n=n,row_assignments=total,initial_form_controls=controls,outcomes=dict(sorted(hist.items())),
        scope='All normalized rows at this size with the stated kernel and nonsingleton-fourth premises; not a smaller-size equality theorem')

def main():
    admission=admission_controls();ranks=rank_controls();literal=[];counts=E017_constant_C_count_controls()
    for n in (8,9):
        literal.append(literal_controls(n));print(json.dumps(literal[-1]),flush=True)
    names=[Path(__file__).name,'enumerate_b1_mixed_c3_fourth.py','b1_mixed_c3_fourth_inventory.json',
        'B1_MIXED_C3_FOURTH_ENTRANCE_REDUCTION.md','small_first_third_inventory.json',
        'ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md',
        'LOCAL_EQUALITY_FLAG.md','CODIMENSION_FOUR_P5_DICHOTOMY.md','SINGLETON_THREE_KERNEL_EXCLUSION.md']
    result=dict(status='pass',parameter=[13,9,1],admission=admission,exact_rational_rank_tables=ranks,
        complete_literal_smaller_controls=literal,complete_parameterized_n13_counts=counts,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Conditional common singleton-fourth reduction with exact finite rank tables; all fourteen earlier profiles remain. No full n=13 row scan, F value or alphabet separation.')
    (ROOT/'b1_mixed_c3_fourth_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',admission=admission,ranks=ranks)),flush=True)

if __name__=='__main__':main()
