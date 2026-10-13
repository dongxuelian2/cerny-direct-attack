"""Independent E16/E126 rows, literal words and finite-image certificates."""
from pathlib import Path
from itertools import product,combinations
import hashlib,json,random,math
from check_c4_d125_guarded_unrestricted import strong,pair_dist,reset
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};H=A|B|C;D={1,5};K={1,2}

def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def image(X,row):return {row[q] for q in X}
def pre(row,X):return {q for q,t in enumerate(row) if t in X}
def action(q,word,rows):
    for i in word:q=rows[i][q]
    return q
def make(pair,indices,rows,kind,reason):
    assert pair[0]!=pair[1] and action(pair[0],indices,rows)==action(pair[1],indices,rows)
    if kind=='mandatory':assert set(pair)&H
    else:assert not set(pair)&K
    assert len(indices)<=5
    return dict(type='short_word',pair=list(pair),word=''.join(chr(97+i) for i in indices),length=len(indices),kind=kind,reason=reason)
def lift(R,indices,targets,rows):
    return tuple(next(q for q in sorted(R) if action(q,indices,rows)==t) for t in targets)

def trap(rows,seeds,reason):
    Q=set(range(len(rows[0])));R=Q-K
    for edge,w in seeds.items():assert action(edge[0],w,rows)==action(edge[1],w,rows)
    family=[set(S) for S in combinations(sorted(Q),len(R)) if not any(set(e)<=set(S) for e in seeds)]
    N=len(family);h=max(map(len,seeds.values()));assert R in family and N in (2,3) and h+N<=5
    frames={frozenset(R)}
    for length in range(1,N+1):
        for indices in product(range(len(rows)),repeat=length):
            I={action(q,indices,rows) for q in R}
            if len(I)<len(R):
                pair=next(p for p in combinations(sorted(R),2) if action(p[0],indices,rows)==action(p[1],indices,rows))
                return make(pair,list(indices),rows,'uncovered',reason+'_prefix_collision')
            for edge,w in seeds.items():
                if set(edge)<=I:return make(lift(R,indices,edge,rows),list(indices)+w,rows,'uncovered',reason+'_seed_lift')
            assert I in family;frames.add(frozenset(I))
    assert all(frozenset(image(X,row)) in frames for X in frames for row in rows)
    return dict(type='closed_frames',reason=reason,independent_family_size=N,seed_depth=h,
        edges=[list(e) for e in seeds],frames=sorted(map(sorted,frames)))

def construct(rows,E):
    Q=set(range(len(rows[0])));O=Q-H-D;R=Q-K
    m0=next(i for i,row in enumerate(rows) if pre(row,C)==D)
    t0=next(i for i,row in enumerate(rows) if pre(row,D)==E)
    if len(E)==3:
        seeds={(1,5):[m0],(1,2):[t0,m0],(1,6):[t0,m0],(2,6):[t0,m0]}
        return trap(rows,seeds,'E126_triangle_pendant')
    seeds={(1,5):[m0],(1,6):[t0,m0]}
    for l,row in enumerate(rows):
        x=next((x for x in sorted(O-{2}) if row[x]==row[2]),None)
        if x is not None:
            return trap(rows,seeds|{(2,x):[l]},'E16_O_kernel_path' if x==6 else 'E16_O_kernel_disjoint')
    for l,row in enumerate(rows):
        if row[2]==row[5]:return trap(rows,seeds|{(2,5):[l]},'E16_kernel25_path')
    for row in rows:
        if pre(row,D)==E:
            h,=O-image({5}|(O-{2,6}),row);assert row[2]==h
            assert image({5}|(O-{6}),row)==O
        else:assert image(O,row)==O
    for m,row in enumerate(rows):
        if pre(row,C)!=D:continue
        p,=pre(row,D);assert p in H
        if row[p]==1:
            q=next(q for q in sorted(O) if row[q]==6)
            return make((p,q),[m,t0,m0],rows,'mandatory','E16_M_enters1')
    p0,=pre(rows[m0],D);assert rows[m0][p0]==5 and image(Q,rows[m0])==Q-{1}
    for f,row in enumerate(rows):
        if pre(row,D)!=D:continue
        if row[5]==1:
            q=next(q for q in sorted(O) if row[q]==6)
            if q!=2:return make((5,q),[f,t0,m0],rows,'uncovered','E16_F_5_to1_free')
            x=next(x for x in sorted(O) if rows[m0][x]==2)
            return make((p0,x),[m0,f,t0,m0],rows,'mandatory','E16_F_5_to1_guard')
    t=next((i for i,row in enumerate(rows) if pre(row,D)==E and row[6]==1),None)
    if t is None:
        assert all(pre(row,{1})<={1} for row in rows)
        raise AssertionError('Strong connectivity with state1 backward closed is impossible')
    h,=O-image({5}|(O-{2,6}),rows[t])
    if h!=6:
        return make(lift(R,[t],(1,6),rows),[t,t0,m0],rows,'uncovered','E16_T_hole_not6')
    assert rows[t][2]==6
    if rows[t][1]==1:
        return trap(rows,{(1,5):[m0],(1,6):[t],(1,2):[t,t],(2,6):[t,t]},'E16_T_triangle_pendant')
    assert rows[t][1]==5 and len(set(rows[t]))==len(Q)
    v=rows[t][5];assert v in O-{6}
    assert {action(q,[t,t],rows) for q in R}==Q-{1,v}
    if v!=2:
        return make(lift(R,[t,t],(2,6),rows),[t,t,t,t,m0],rows,'uncovered','E16_T_squared_contains26')
    q=next(q for q in sorted(O) if rows[m0][q]==2)
    return make((p0,q),[m0,t,t,t,m0],rows,'mandatory','E16_T_four_cycle')

def main():
    data=read('c4_d15_guarded_individual_controls.json');uniform=read('finite_independent_image_trap_audit.json')
    for z in (data,uniform):
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert uniform['status']=='pass'
    parent=read('b1_c4_fourth_inventory.json');seed=20261010;rng=random.Random(seed)
    stats=[];examples=[];closures=[];boundaries={};total_binary=total_ternary=0;example_reasons={};closure_counts={}
    for record in data['records']:
        n=record['n'];E=set(record['E']);key=''.join(map(str,sorted(E)));Q=set(range(n));O=Q-H-D;R=Q-K;targets=[A,B,C,D,O]
        z=next(z for z in parent['records'] if z['D']==sorted(D) and z['E']==sorted(E))
        assert z['additional_covered_fibers']==[] and z['mandatory_through_seven']==sorted(H)
        parent_cols={tuple(tuple(f[k]) for k in ('preA','preB','preC','preD')) for f in z['rows']}
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
            nonlocal connected,sync,closed
            if not strong(rows):return
            connected+=1;w=construct(rows,E);dist=pair_dist(rows);hist[w['reason']]=hist.get(w['reason'],0)+1
            if w['type']=='closed_frames':
                frames=list(map(set,w['frames']));assert R in frames
                assert all(len(X)==n-2 for X in frames) and all(image(X,r) in frames for X in frames for r in rows)
                assert len(dist)<n*(n-1)//2;closed+=1
                if closure_counts.get(key,0)<10:
                    closures.append(dict(n=n,E=sorted(E),rows=list(map(list,rows)),certificate=w));closure_counts[key]=closure_counts.get(key,0)+1
                return
            p=tuple(sorted(w['pair']));assert p in dist and dist[p]<=w['length']
            if len(E)==3:assert w['kind']=='uncovered' and w['length']<=4
            if example_reasons.get(w['reason'],0)<5:
                examples.append(dict(n=n,E=sorted(E),rows=list(map(list,rows)),short_merge=w));example_reasons[w['reason']]=example_reasons.get(w['reason'],0)+1
            if len(dist)==n*(n-1)//2:
                sync+=1;dj=min(v for p,v in dist.items() if set(p)&H);dr=min(v for p,v in dist.items() if not set(p)&K);score=[min(dj,dr),dj,dr]
                if key not in boundaries or score>boundaries[key]['selection_score']:
                    rw=reset(rows);assert rw is not None
                    boundaries[key]=dict(n=n,E=sorted(E),rows=list(map(list,rows)),short_merge=w,reset=rw,
                        earliest_J_pair_merging=dj,earliest_R_pair_merging=dr,selection_score=score)
        if n<=8:
            for m in moving:
                for t in supplying:
                    for rows in ((m,t),(t,m)):binary+=1;check(rows)
            m=len(O);assert binary==(256*m*m if len(E)==2 else 512*m)*math.factorial(m)**2
        total_binary+=binary
        if n==7:
            for rows in combinations(pool,3):
                if not any(row in mset for row in rows) or not any(row in tset for row in rows):continue
                ternary+=1;check(rows)
            assert ternary==227328
        total_ternary+=ternary
        for alpha in (3,4):
            for _ in range(3000):
                m=rng.choice(moving);t=rng.choice(supplying);rows=[m,t]
                rows+=rng.sample([r for r in pool if r!=m and r!=t],alpha-2);rng.shuffle(rows)
                seeded+=1;check(rows)
        stats.append(dict(n=n,E=sorted(E),individual_rows=len(pool),complete_binary_ordered_alphabets=binary,
            complete_distinct_ternary_supplier_sets=ternary,seeded_larger_alphabets=seeded,
            strongly_connected_controls=connected,synchronizing_controls=sync,nonsynchronizing_closed_controls=closed,constructive_case_histogram=hist))
        print(json.dumps(stats[-1]),flush=True)
    assert total_binary==146432 and total_ternary==454656 and set(boundaries)=={'16','126'}
    sample=dict(seed=seed,constructive_samples=examples,closed_frame_samples=closures,boundary_controls=boundaries,
        scope='Literal structural controls only; no attaining F witness or sampled-negative exclusion.')
    (ROOT/'c4_d15_guarded_unrestricted_samples.json').write_bytes((json.dumps(sample,indent=2)+'\n').encode())
    names=[Path(__file__).name,'enumerate_c4_d15_guarded_unrestricted.py','c4_d15_guarded_individual_controls.json',
        'c4_d15_guarded_unrestricted_samples.json','PROOF.md#problem4-c4-d15-e16-e126-unrestricted-exclusion','PROOF.md#problem4-finite-independent-image-trap',
        'finite_independent_image_trap_audit.json','check_c4_d125_guarded_unrestricted.py','b1_c4_fourth_inventory.json','b1_c4_fourth_audit.json',
        'PROOF.md#problem4-b1-c4-fourth-space','PROOF.md#problem4-mandatory-core-isolation','mandatory_core_isolation_audit.json','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    report=dict(status='pass',parameter=[13,9,1],B=[0],C=[4],D=[1,5],excluded_E=[[1,6],[1,2,6]],unrestricted_paper_excluded=True,
        complete_individual_fields_per_E=12,complete_individual_rows=8576,
        complete_binary_ordered_alphabets_through_n8=total_binary,complete_distinct_ternary_supplier_sets_at_n7=total_ternary,
        seeded_larger_alphabets=36000,seed=seed,constructive_examples=len(examples),closed_frame_examples=len(closures),finite_control_stats=stats,
        boundary_depths={k:[b['earliest_J_pair_merging'],b['earliest_R_pair_merging']] for k,b in boundaries.items()},
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Paper proofs exclude unrestricted conditional D15/E16/E126 fourth geometries only. Complete finite domains and seeded controls support them. E6/E26, whole third/joint and numerical F unresolved.')
    (ROOT/'c4_d15_guarded_unrestricted_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','finite_control_stats')}),flush=True)
if __name__=='__main__':main()
