"""Independent raw rows and constructive cover/isolation contradiction controls."""
from pathlib import Path
from itertools import product,combinations
import hashlib,json,random,math
from check_c4_d125_guarded_unrestricted import strong,pair_dist,reset
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};H=A|B|C;D={1,5};E={1,2};K=E
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
    assert len(indices)<=4
    return dict(pair=list(pair),word=''.join(chr(97+i) for i in indices),length=len(indices),kind=kind,reason=reason)
def construct(rows):
    Q=set(range(len(rows[0])));O=Q-H-D;R=Q-K
    m0=next(i for i,row in enumerate(rows) if pre(row,C)==D)
    t0=next(i for i,row in enumerate(rows) if pre(row,D)==E)
    assert O<=image(R,rows[t0])
    for l,row in enumerate(rows):
        pair=next((pair for pair in combinations(sorted(O),2) if row[pair[0]]==row[pair[1]]),None)
        if pair:
            u=next(q for q in sorted(R) if rows[t0][q]==pair[0]);v=next(q for q in sorted(R) if rows[t0][q]==pair[1])
            return make((u,v),[t0,l],rows,'uncovered','kernel_inside_O')
    for m,row in enumerate(rows):
        if pre(row,C)!=D:continue
        assert image(O,row)==O
        p=next(iter(pre(row,D)));assert p in H
        if row[p]==1:
            q=next(q for q in sorted(O) if row[q]==2)
            return make((p,q),[m,t0,m0],rows,'mandatory','supplier_enters_guard1')
    p0=next(iter(pre(rows[m0],D)));assert rows[m0][p0]==5
    for f,row in enumerate(rows):
        if pre(row,D)!=D:continue
        assert image(O,row)==O
        if row[5]==1:
            q=next(q for q in sorted(O) if row[q]==2)
            if q!=2:return make((5,q),[f,t0,m0],rows,'uncovered','preserver_5_to_1_free_preimage2')
            q=next(q for q in sorted(O) if rows[m0][q]==2)
            return make((p0,q),[m0,f,t0,m0],rows,'mandatory','preserver_5_to_1_fixed2')
    t=next((i for i,row in enumerate(rows) if pre(row,D)==E and row[2]==1),None)
    if t is None:
        assert all(pre(row,{1})<={1} for row in rows)
        raise AssertionError('Strong connectivity with state1 backward closed is impossible')
    q=next(q for q in sorted(R) if rows[t][q]==2);assert q==5 or q in O-{2}
    if q==5:
        x=next(x for x in sorted(O) if rows[m0][x]==2)
        return make((p0,x),[m0,t,t0,m0],rows,'mandatory','T_2_to_1_preimage2_is5')
    u=next(x for x in sorted(R) if rows[t0][x]==2);v=next(x for x in sorted(R) if rows[t0][x]==q)
    return make((u,v),[t0,t,t0,m0],rows,'uncovered','T_2_to_1_ordinary_preimage2')

def main():
    data=read('c4_d15_e12_individual_controls.json')
    for n,h in data['source_sha256'].items():assert sha(ROOT/n)==h,n
    parent=read('b1_c4_fourth_inventory.json');z=next(z for z in parent['records'] if z['D']==sorted(D) and z['E']==sorted(E))
    assert z['additional_covered_fibers']==[] and z['mandatory_through_seven']==sorted(H)
    parent_cols={tuple(tuple(f[k]) for k in ('preA','preB','preC','preD')) for f in z['rows']}
    seed=20261010;rng=random.Random(seed);stats=[];examples=[];boundary=None;total_binary=total_ternary=0
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
            row=[-1]*n;rows=[]
            def visit(q):
                if q==n:rows.append(tuple(row));return
                for t in sorted(options[q]):
                    if q in R and any(p in R and row[p]==t for p in range(q)):continue
                    row[q]=t;visit(q+1);row[q]=-1
            visit(0);rows.sort();assert rows==list(map(tuple,field['rows']))
            for row in rows:
                assert len(image(R,row))==n-2
                for X,Y in zip(groups,targets):assert pre(row,Y)==X
                if pre(row,D)==E:assert image({5}|(O-{2}),row)==O
                else:assert image(O,row)<=O
            pool.extend(rows)
        assert len(pool)==len(set(pool))==record['complete_individual_rows']
        moving=[r for r in pool if pre(r,C)==D];supplying=[r for r in pool if pre(r,D)==E]
        mset=set(moving);tset=set(supplying);assert not mset&tset
        binary=ternary=seeded=connected=sync=0;hist={}
        def check(rows):
            nonlocal connected,sync,boundary
            if not strong(rows):return
            connected+=1;w=construct(rows);dist=pair_dist(rows);pair=tuple(sorted(w['pair']))
            assert pair in dist and dist[pair]<=w['length']<=4
            hist[w['reason']]=hist.get(w['reason'],0)+1
            if len(examples)<80:examples.append(dict(n=n,rows=[list(r) for r in rows],short_merge=w))
            if len(dist)==n*(n-1)//2:
                sync+=1;dj=min(v for pair,v in dist.items() if set(pair)&H);dr=min(v for pair,v in dist.items() if not set(pair)&K)
                score=[min(dj,dr),dj,dr]
                if boundary is None or score>boundary['selection_score']:
                    reset_word=reset(rows);assert reset_word is not None
                    boundary=dict(n=n,rows=[list(r) for r in rows],short_merge=w,reset=reset_word,
                        earliest_J_pair_merging=dj,earliest_R_pair_merging=dr,selection_score=score)
        for m in moving:
            for t in supplying:
                for rows in ((m,t),(t,m)):binary+=1;check(rows)
        m=len(O);assert binary==256*m*math.factorial(m)**2;total_binary+=binary
        if n<=7:
            for rows in combinations(pool,3):
                if not any(row in mset for row in rows) or not any(row in tset for row in rows):continue
                ternary+=1;check(rows)
            assert ternary=={6:3456,7:97280}[n]
        total_ternary+=ternary
        for alpha in (3,4):
            for _ in range(3000):
                m=rng.choice(moving);t=rng.choice(supplying);rows=[m,t]
                rows+=rng.sample([r for r in pool if r!=m and r!=t],alpha-2);rng.shuffle(rows)
                seeded+=1;check(rows)
        stats.append(dict(n=n,individual_rows=len(pool),complete_binary_ordered_alphabets=binary,
            complete_distinct_ternary_supplier_sets=ternary,seeded_larger_alphabets=seeded,
            strongly_connected_controls=connected,synchronizing_controls=sync,contradiction_word_cases=hist))
        print(json.dumps(stats[-1]),flush=True)
    assert total_binary==619776 and total_ternary==100736 and boundary is not None
    sample=dict(seed=seed,constructive_samples=examples,boundary_control=boundary,
        scope='Literal structural controls only; no attaining F witness or sampled-negative exclusion.')
    (ROOT/'c4_d15_e12_unrestricted_samples.json').write_bytes((json.dumps(sample,indent=2)+'\n').encode())
    names=[Path(__file__).name,'enumerate_c4_d15_e12_unrestricted.py','c4_d15_e12_individual_controls.json',
        'c4_d15_e12_unrestricted_samples.json','PROOF.md#problem4-c4-d15-e12-unrestricted-exclusion',
        'check_c4_d125_guarded_unrestricted.py','b1_c4_fourth_inventory.json','b1_c4_fourth_audit.json',
        'PROOF.md#problem4-b1-c4-fourth-space','PROOF.md#problem4-mandatory-core-isolation','mandatory_core_isolation_audit.json',
        'PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    report=dict(status='pass',parameter=[13,9,1],B=[0],C=[4],D=[1,5],E=[1,2],unrestricted_E12_paper_excluded=True,
        complete_individual_fields=12,complete_individual_rows=3384,
        complete_binary_ordered_alphabets_through_n9=total_binary,complete_distinct_ternary_supplier_sets_through_n7=total_ternary,
        seeded_larger_alphabets=24000,seed=seed,constructive_examples=len(examples),finite_control_stats=stats,
        boundary_depths=[boundary['earliest_J_pair_merging'],boundary['earliest_R_pair_merging']],
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Paper proof excludes unrestricted conditional D15/E12 fourth geometry only. Complete finite rows/supplier alphabets and seeded controls support the proof; remaining E, whole third/joint and numerical F are unresolved.')
    (ROOT/'c4_d15_e12_unrestricted_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','finite_control_stats')}),flush=True)
if __name__=='__main__':main()
