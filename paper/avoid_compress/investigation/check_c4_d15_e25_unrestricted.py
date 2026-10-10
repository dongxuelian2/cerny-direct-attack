"""Independent raw rows and literal short-word/two-frame proof controls."""
from pathlib import Path
from itertools import product,combinations
import hashlib,json,random,math
from check_c4_d125_guarded_unrestricted import strong,pair_dist,reset
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};H=A|B|C;D={1,5};E={2,5};K={1,2}

def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def image(X,row):return {row[q] for q in X}
def pre(row,X):return {q for q,t in enumerate(row) if t in X}
def action(q,word,rows):
    for i in word:q=rows[i][q]
    return q
def make(pair,indices,rows,kind,reason):
    assert pair[0]!=pair[1] and action(pair[0],indices,rows)==action(pair[1],indices,rows)
    if kind=='mandatory':assert set(pair)&H;assert len(indices)<=5
    else:assert not set(pair)&K;assert len(indices)<=4
    return dict(type='short_word',pair=list(pair),word=''.join(chr(97+i) for i in indices),length=len(indices),kind=kind,reason=reason)
def lift(R,indices,targets,rows):
    return tuple(next(q for q in sorted(R) if action(q,indices,rows)==t) for t in targets)

def construct(rows):
    Q=set(range(len(rows[0])));O=Q-H-D;R=Q-K
    m0=next(i for i,row in enumerate(rows) if pre(row,C)==D)
    t0=next(i for i,row in enumerate(rows) if pre(row,D)==E)
    holes=[]
    for l,row in enumerate(rows):
        h,=O-image(O-{2},row);holes.append(h)
        d,=image(R,row)&D;assert image(R,row)==H|{d}|(O-{h})
        if d==5 and h!=2:
            return make(lift(R,[l],(2,5),rows),[l,t0,m0],rows,'uncovered','free_image_contains_2_5')
    for l,row in enumerate(rows):
        x=next((x for x in sorted(O-{2}) if row[x]==row[2]),None)
        if x is None:continue
        h=holes[t0];v=rows[t0][1]
        if h not in (2,x):
            return make(lift(R,[t0],(2,x),rows),[t0,l],rows,'uncovered','O_kernel_lifted_by_supplier')
        if v!=h:
            y=next(q for q in sorted(O-{2}) if rows[t0][q]==v);seed=[t0]
        else:
            y=next(q for q in sorted(O-{2}) if rows[t0][q]==(x if h==2 else 2));seed=[t0,l]
        assert action(1,seed,rows)==action(y,seed,rows)
        for j,r in enumerate(rows):
            I=image(R,r)
            if {1,y}<=I:return make(lift(R,[j],(1,y),rows),[j]+seed,rows,'uncovered','first_image_contains_1_y')
            if {2,x}<=I:return make(lift(R,[j],(2,x),rows),[j,l],rows,'uncovered','first_image_contains_2_x')
        if x!=y:
            assert all(image(R,r)==R for r in rows)
            return dict(type='closed_frames',reason='mixed_kernel_single_closed_R',frames=[sorted(R)])
        Z={5,x};assert len(Z)==2 and not Z&K
        seeds={(1,5):[m0],(2,5):[t0,m0],(2,x):[l],(1,x):seed}
        frames={frozenset(R)}
        for length in (1,2):
            for indices in product(range(len(rows)),repeat=length):
                targets={action(q,indices,rows) for q in R}
                if len(targets)<len(R):
                    pair=next(p for p in combinations(sorted(R),2) if action(p[0],indices,rows)==action(p[1],indices,rows))
                    return make(pair,list(indices),rows,'uncovered','saturated_prefix_compresses_R')
                for pair,w in seeds.items():
                    if set(pair)<=targets:
                        return make(lift(R,indices,pair,rows),list(indices)+w,rows,'uncovered','saturated_prefix_contains_cross_pair')
                assert targets in (R,Q-Z);frames.add(frozenset(targets))
        assert all(frozenset(image(X,r)) in frames for X in frames for r in rows)
        return dict(type='closed_frames',reason='saturated_two_guard_trap',Z=sorted(Z),frames=sorted(map(sorted,frames)))
    for m,row in enumerate(rows):
        if pre(row,C)!=D:continue
        assert image(O,row)==O
        p,=pre(row,D);assert p in H
        if row[p]==5:
            q=next(q for q in sorted(O) if row[q]==2)
            return make((p,q),[m,t0,m0],rows,'mandatory','M_enters_5')
    p0,=pre(rows[m0],D);assert rows[m0][p0]==1 and image(Q,rows[m0])==Q-{5}
    for f,row in enumerate(rows):
        if pre(row,D)!=D:continue
        assert image(O,row)==O
        if row[1]==5:
            q=next(q for q in sorted(O) if action(q,[m0,f],rows)==2)
            return make((p0,q),[m0,f,t0,m0],rows,'mandatory','F_1_to_5')
    t=next((i for i,row in enumerate(rows) if pre(row,D)==E and row[2]==5),None)
    if t is None:
        assert all(pre(row,{5})<={5} for row in rows)
        raise AssertionError('Strong connectivity with state5 backward closed is impossible')
    h=holes[t]
    if rows[t][1]!=h:
        y=next(q for q in sorted(O-{2}) if rows[t][q]==rows[t][1])
        q=next(q for q in sorted(O) if rows[m0][q]==y)
        return make((p0,q),[m0,t],rows,'mandatory','T_guard1_does_not_fill_hole')
    if rows[t][5]==5 or h==2:
        assert h==2
        q=next(q for q in sorted(Q) if action(q,[m0,t],rows)==5)
        return make((p0,q),[m0,t,t0,m0],rows,'mandatory','T_hole2')
    assert len(set(rows[t]))==len(Q) and rows[t][5]==1
    v=rows[t][h];assert v in O-{h}
    assert {action(q,[t,t],rows) for q in R}==Q-{1,v}
    assert {action(q,[m0,t,t],rows) for q in Q}==Q-{h}
    if v!=2:
        return make(lift(R,[t,t],(2,5),rows),[t,t,t0,m0],rows,'uncovered','T_squared_free_seed')
    q=next(q for q in sorted(Q) if action(q,[m0,t,t],rows)==5)
    return make((p0,q),[m0,t,t,t0,m0],rows,'mandatory','T_squared_mandatory_seed')

def main():
    data=read('c4_d15_e25_individual_controls.json')
    for n,h in data['source_sha256'].items():assert sha(ROOT/n)==h,n
    trap=read('saturated_two_guard_trap_audit.json');assert trap['status']=='pass'
    for n,h in trap['source_sha256'].items():assert sha(ROOT/n)==h,n
    parent=read('b1_c4_fourth_inventory.json');z=next(z for z in parent['records'] if z['D']==sorted(D) and z['E']==sorted(E))
    assert z['additional_covered_fibers']==[] and z['mandatory_through_seven']==sorted(H)
    parent_cols={tuple(tuple(f[k]) for k in ('preA','preB','preC','preD')) for f in z['rows']}
    seed=20261010;rng=random.Random(seed);stats=[];examples=[];closures=[];boundary=None;total_binary=total_ternary=0
    for record in data['records']:
        n=record['n'];Q=set(range(n));O=Q-H-D;R=Q-K;targets=[A,B,C,D,O]
        cols=set()
        for X in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
            if all(sum(q in Y for Y in X)<=1 for q in Q):cols.add(tuple(tuple(sorted(Y)) for Y in X))
        assert cols==parent_cols=={tuple(map(tuple,f['pre'])) for f in record['fields']} and len(cols)==12
        pool=[]
        for field in record['fields']:
            groups=list(map(set,field['pre']));groups.append(Q-set().union(*groups))
            options={q:targets[next(i for i,X in enumerate(groups) if q in X)] for q in Q}
            row=[-1]*n;raw=[]
            def visit(q):
                if q==n:raw.append(tuple(row));return
                for t in sorted(options[q]):
                    if q in R and any(p in R and row[p]==t for p in range(q)):continue
                    row[q]=t;visit(q+1);row[q]=-1
            visit(0);raw.sort();assert raw==list(map(tuple,field['rows']))
            for row in raw:
                assert len(image(R,row))==n-2
                for X,Y in zip(groups,targets):assert pre(row,Y)==X
            pool.extend(raw)
        assert len(pool)==len(set(pool))==record['complete_individual_rows']
        moving=[r for r in pool if pre(r,C)==D];supplying=[r for r in pool if pre(r,D)==E]
        mset=set(moving);tset=set(supplying);assert not mset&tset
        binary=ternary=seeded=connected=sync=closed=0;hist={}
        def check(rows):
            nonlocal connected,sync,boundary,closed
            if not strong(rows):return
            connected+=1;w=construct(rows);dist=pair_dist(rows)
            hist[w['reason']]=hist.get(w['reason'],0)+1
            if w['type']=='closed_frames':
                frames=list(map(set,w['frames']));assert R in frames
                assert all(len(X)==n-2 for X in frames)
                assert all(image(X,row) in frames for X in frames for row in rows)
                assert len(dist)<n*(n-1)//2;closed+=1
                if len(closures)<10:closures.append(dict(n=n,rows=list(map(list,rows)),certificate=w))
                return
            pair=tuple(sorted(w['pair']));assert pair in dist and dist[pair]<=w['length']
            if len(examples)<80:examples.append(dict(n=n,rows=list(map(list,rows)),short_merge=w))
            if len(dist)==n*(n-1)//2:
                sync+=1;dj=min(v for pair,v in dist.items() if set(pair)&H);dr=min(v for pair,v in dist.items() if not set(pair)&K)
                score=[min(dj,dr),dj,dr]
                if boundary is None or score>boundary['selection_score']:
                    reset_word=reset(rows);assert reset_word is not None
                    boundary=dict(n=n,rows=list(map(list,rows)),short_merge=w,reset=reset_word,
                        earliest_J_pair_merging=dj,earliest_R_pair_merging=dr,selection_score=score)
        if n<=8:
            for m in moving:
                for t in supplying:
                    for rows in ((m,t),(t,m)):binary+=1;check(rows)
            m=len(O);assert binary==256*(m*math.factorial(m))**2
        total_binary+=binary
        if n<=7:
            for rows in combinations(pool,3):
                if not any(row in mset for row in rows) or not any(row in tset for row in rows):continue
                ternary+=1;check(rows)
            assert ternary=={6:3456,7:227328}[n]
        total_ternary+=ternary
        for alpha in (3,4):
            for _ in range(3000):
                m=rng.choice(moving);t=rng.choice(supplying);rows=[m,t]
                rows+=rng.sample([r for r in pool if r!=m and r!=t],alpha-2);rng.shuffle(rows)
                seeded+=1;check(rows)
        stats.append(dict(n=n,individual_rows=len(pool),complete_binary_ordered_alphabets=binary,
            complete_distinct_ternary_supplier_sets=ternary,seeded_larger_alphabets=seeded,
            strongly_connected_controls=connected,synchronizing_controls=sync,nonsynchronizing_closed_controls=closed,
            constructive_case_histogram=hist))
        print(json.dumps(stats[-1]),flush=True)
    assert total_binary==87296 and total_ternary==230784 and boundary is not None
    sample=dict(seed=seed,constructive_samples=examples,closed_frame_samples=closures,boundary_control=boundary,
        scope='Literal structural controls only; no attaining F witness or sampled-negative exclusion.')
    (ROOT/'c4_d15_e25_unrestricted_samples.json').write_bytes((json.dumps(sample,indent=2)+'\n').encode())
    names=[Path(__file__).name,'enumerate_c4_d15_e25_unrestricted.py','c4_d15_e25_individual_controls.json',
        'c4_d15_e25_unrestricted_samples.json','C4_D15_E25_UNRESTRICTED_EXCLUSION.md','SATURATED_TWO_GUARD_TRAP.md',
        'saturated_two_guard_trap_audit.json','check_c4_d125_guarded_unrestricted.py','b1_c4_fourth_inventory.json','b1_c4_fourth_audit.json',
        'B1_C4_FOURTH_SPACE.md','MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    report=dict(status='pass',parameter=[13,9,1],B=[0],C=[4],D=[1,5],E=[2,5],unrestricted_E25_paper_excluded=True,
        complete_individual_fields=12,complete_individual_rows=4760,
        complete_binary_ordered_alphabets_through_n8=total_binary,complete_distinct_ternary_supplier_sets_through_n7=total_ternary,
        seeded_larger_alphabets=24000,seed=seed,constructive_examples=len(examples),closed_frame_examples=len(closures),finite_control_stats=stats,
        boundary_depths=[boundary['earliest_J_pair_merging'],boundary['earliest_R_pair_merging']],
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Paper proof excludes unrestricted conditional D15/E25 fourth geometry only. Complete finite domains and seeded controls support it. Remaining E, whole third/joint and numerical F remain unresolved.')
    (ROOT/'c4_d15_e25_unrestricted_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','finite_control_stats')}),flush=True)
if __name__=='__main__':main()
