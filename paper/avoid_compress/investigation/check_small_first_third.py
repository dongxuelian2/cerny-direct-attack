"""Independent literal B1/B2 admission and B2/C4 symbolic-case audit."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import hashlib,json
from check_short_pair_span import exact_rank

ROOT=Path(__file__).resolve().parent
Q=set(range(13)); A={3}; H={0,1,2}; O=Q-A

def incomparable(x,y): return not x<=y and not y<=x

def rank_columns(B,C,D,R=None):
    rows=[[1,int(q in B),int(q in C),int(q in D)] for q in sorted(O)]
    if R is not None:
        rows=[row+[int(q in R)] for q,row in zip(sorted(O),rows)]
    return exact_rank(rows,len(rows[0]))

def row_key(row): return tuple(tuple(row[k]) for k in ('preA','preB','preC'))

def independent_profiles(B,C,D,allowed):
    rows={}
    for pa,pb,pc in product((A,B),(A,B,C),[A]+allowed):
        choices={q:tuple(v for v in sorted(Q) if
           ((v in A),(v in B),(v in C))==((q in pa),(q in pb),(q in pc))) for q in Q}
        if any(not v for v in choices.values()): continue
        forced={tuple(z) for z in combinations(sorted(Q),2)
                if choices[z[0]]==choices[z[1]] and len(choices[z[0]])==1}
        if len(forced)>4 or any(not set(z)&H for z in forced): continue
        classes={targets:{q for q in Q if choices[q]==targets} for targets in set(choices.values())}
        capacity={targets:min(len(targets),len(inputs)) for targets,inputs in classes.items()}
        key=tuple(tuple(sorted(v)) for v in (pa,pb,pc))
        rows[key]=(forced,capacity)
    pairs=set()
    for pair in combinations_with_replacement(sorted(rows),2):
        if tuple(sorted(B)) not in [v[0] for v in pair]: continue
        if tuple(sorted(C)) not in [v[1] for v in pair]: continue
        if tuple(sorted(D)) not in [v[2] for v in pair]: continue
        if B&C and any(v[0]==(3,) and set(v[2])==B for v in pair): continue
        if len(rows[pair[0]][0]|rows[pair[1]][0])>4: continue
        targets=set(rows[pair[0]][1])|set(rows[pair[1]][1])
        targets|={tuple(v for v in sorted(Q) if
            ((v in A),(v in B),(v in C))==key) for key in product((False,True),repeat=3)}
        if any(sum(rows[v][1].get(group,0) for v in pair)<len(group) for group in targets): continue
        pairs.add(pair)
    return rows,pairs

def geometry():
    data=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    joint=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))
    allD=[set(z) for size in range(1,5) for z in combinations(sorted(O),size) if len(set(z)-H)<=1]
    allS=[A|set(z) for z in combinations(sorted(O),8)]
    assert len(allD)==79 and len(allS)==495
    summaries={}; extra=0
    for entry in joint['records']:
        B=set(entry['B']);C=set(entry['C'])
        if len(B)>2: continue
        records=[z for z in data['records'] if z['joint_id']==entry['id']]
        byD={tuple(z['D']):z for z in records}
        cells=[{q for q in O if (q in H,q in B,q in C)==key} for key in product((False,True),repeat=3)]
        counts=Counter()
        for D in allD:
            if len(B|C|D)>6 or not incomparable(D,B) or not incomparable(D,C): continue
            feasible=[S for S in allS if len(S&B)==len(S&C)==len(S&D)==1]
            if not feasible or rank_columns(B,C,D)!=4: continue
            canonical=tuple(sorted(q for cell in cells for q in sorted(cell)[:len(cell&D)]))
            assert canonical in byD;counts[canonical]+=1
        assert set(counts)==set(byD)
        for key,z in byD.items():
            D=set(key);feasible=[S for S in allS if len(S&B)==len(S&C)==len(S&D)==1]
            assert counts[key]==z['labelled_D']==z['orbit_size']
            assert len(feasible)==z['feasible_nine_sets']
            allowed=[R for R in allD if all(R==X or incomparable(R,X) for X in (B,C,D))
                and rank_columns(B,C,D,R)==4 and all(len(S&R)==1 for S in feasible)]
            assert {tuple(sorted(R)) for R in allowed}=={tuple(v) for v in z['allowed_preC_fibers']}
            rows,pairs=independent_profiles(B,C,D,allowed)
            stored=[row_key(v) for v in z['rows']]
            assert len(stored)==len(set(stored)) and set(stored)==set(rows)
            actual={tuple(sorted((stored[x],stored[y]))) for x,y in z['binary_profile_pairs']}
            assert actual==pairs
            extra+=any(R not in (B,C,D) for R in allowed)
        summary=dict(geometric=len(records),labelled=sum(counts.values()),
            binary_typed=sum(bool(z['binary_profile_pairs']) for z in records),
            binary_pairs=sum(len(z['binary_profile_pairs']) for z in records))
        assert summary==data['counts'][entry['id']];summaries[entry['id']]=summary
    assert len(summaries)==29 and len(data['records'])==235
    assert sum(v['binary_typed'] for v in summaries.values())==182
    assert sum(v['binary_pairs'] for v in summaries.values())==965
    # A real additional Boolean fiber is retained, not overwritten by D.
    B={0,4};C={1,5};D={0,5};R={1,4};S={0,1,3,6,7,8,9,10,11}
    assert all(len(S&X)==1 for X in (B,C,D,R))
    assert all(int(q in R)==int(q in B)+int(q in C)-int(q in D) for q in O)
    return summaries,extra

def partitions(values):
    answer=[]
    def visit(j,blocks):
        if j==len(values):answer.append(tuple(tuple(v) for v in blocks));return
        for v in blocks:
            v.append(values[j]);visit(j+1,blocks);v.pop()
        blocks.append([values[j]]);visit(j+1,blocks);blocks.pop()
    visit(0,[]);return answer

def four_point():
    B={0,4};C={0,1,2,5};W={1,2,5};J=set(range(7,13));R={6}|J
    inventory=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    chosen=[z for z in inventory['records'] if z['joint_id']=='b2_mixed_c12']
    assert len(chosen)==8 and sum(z['labelled_D'] for z in chosen)==59
    assert {tuple(z['D']) for z in chosen if z['binary_profile_pairs']}=={(1,6),(1,2,6)}
    assert all(len(z['binary_profile_pairs'])==1 for z in chosen if z['binary_profile_pairs'])
    for z in chosen:
        assert {tuple(v) for v in z['allowed_preC_fibers']}=={tuple(sorted(B)),tuple(sorted(C)),tuple(z['D'])}
    # No singleton third-preimage can supply all three W outputs if M(C)=a.
    # H subset C makes an outside one-count fiber's difference from C <=1.
    base={(0,4),(0,2),(0,5),(2,5)}
    kernel_counts=[];groups=[]
    for inputs,available in [({2,5}|J,base),({5}|J,None),({4}|J,None)]:
        allk=partitions(sorted(inputs));admitted=[]
        for blocks in allk:
            if len(blocks)>7:continue
            pairs={tuple(z) for v in blocks for z in combinations(v,2)}
            if any(not set(z)&H for z in pairs):continue
            if available is not None and not pairs<=available:continue
            admitted.append(blocks)
        assert len(admitted)==1 and len(admitted[0])==7
        assert all(set(v)-H for v in admitted[0])
        kernel_counts.append(len(allk));groups.append(admitted[0])
    assert kernel_counts==[4140,877,877]
    reports=[]
    for D in ({1,6},{1,2,6}):
        U=D&H;raw=kept=short=closed=ports=0
        for mvalues,f6 in product(product(sorted(W),repeat=len(D)),sorted(W)):
            raw+=1; M=dict(zip(sorted(D),mvalues));M.update({0:3,4:3,3:4})
            F={3:3,6:f6};F.update({q:0 if q in D else 4 for q in C})
            forced={tuple(z) for row in (M,F) for z in combinations(sorted(row),2) if row[z[0]]==row[z[1]]}
            if len(forced)>4 or any(not set(z)&H for z in forced):continue
            if set(mvalues)|{f6}!=W:continue
            kept+=1
            witness=next((row for row in (M,F) if row[6] in U),None)
            if witness is not None:
                short+=1;blocks=groups[0 if len(D)==2 else 1] if witness is M else groups[2]
                x,y=witness[6],6
                for row in (M,F,M):x,y=row[x],row[y]
                assert x==y==3
                for block in blocks:
                    q=next(q for q in block if q not in H)
                    assert q!=6 and witness[6] in D and 6 in D
                    # Assigning this block to output 6 gives the actual
                    # distinct outside pair (6,q) -> (row[6],6) in D.
                    ports+=1
            else:
                closed+=1
                assert all(value not in U for row in (M,F) for q,value in row.items() if q not in U)
                assert not R&U
        assert raw==(27 if len(D)==2 else 81)
        assert closed==2 and short+closed==kept
        reports.append(dict(D=sorted(D),core_assignments=raw,immediate_and_indegree_admitted=kept,
            short_pair_cases=short,backward_closed_U_cases=closed,pre6_kernel_ports=ports))
    return dict(geometric_orbits=8,labelled_D=59,binary_typed_profiles=2,
        complete_R_kernel_counts=kernel_counts,admitted_R_kernels=[1,1,1],core_reports=reports,
        excluded_binary_joint='b2_mixed_c12',binary_second_fiber_maximum_size_n13=3)

def main():
    summaries,extra=geometry(); focused=four_point()
    names=[Path(__file__).name,'enumerate_small_first_third.py','small_first_third_inventory.json',
        'B2_FOUR_POINT_SECOND_EXCLUSION.md','check_short_pair_span.py','THIRD_ENTRANCE_SPACE.md',
        'SECOND_ENTRANCE_FIBER.md','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md',
        'BINARY_THIRD_ENTRANCE_CROSSING.md','joint_fiber_orbits.json','alphabet_check.py',
        'SMALL_FIRST_THIRD_ADMISSION.md','SINGLETON_THREE_KERNEL_EXCLUSION.md',
        'CODIMENSION_FOUR_P5_DICHOTOMY.md']
    result=dict(status='pass',parameter=[13,9,1],joint_cases=29,geometric_third_orbits=235,
        binary_typed_third_orbits=182,binary_profile_pairs=965,extra_fiber_geometric_orbits=extra,
        counts=summaries,four_point_second_exclusion=focused,
        remaining_binary_joint=28,remaining_unrestricted_joint=43,extremal_interval=[11,12],
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Independent literal geometry/augmented rank and typed-row admission, plus the symbolic binary B2/C4 exclusion. No full row enumeration, new F value or alphabet separation.')
    (ROOT/'small_first_third_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('status','joint_cases','geometric_third_orbits',
        'binary_typed_third_orbits','binary_profile_pairs','extra_fiber_geometric_orbits',
        'four_point_second_exclusion','remaining_binary_joint','remaining_unrestricted_joint')}))

if __name__=='__main__':main()
