"""Independent rows, complete small supplier alphabets, literal contradiction words."""
from pathlib import Path
from itertools import product,combinations
from collections import deque
import hashlib,json,random
from check_c4_d125_guarded_unrestricted import strong,pair_dist,reset
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};D={1,2};K=D;e=5;H=A|B|C
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def image(X,row):return {row[q] for q in X}
def pre(row,X):return {q for q,t in enumerate(row) if t in X}
def action(q,word,rows):
    for i in word:q=rows[i][q]
    return q
def kernels(row):return [p for p in combinations(range(len(row)),2) if row[p[0]]==row[p[1]]]
def word(pair,indices,rows,kind,reason):
    assert pair[0]!=pair[1] and action(pair[0],indices,rows)==action(pair[1],indices,rows)
    return dict(pair=list(pair),word=''.join(chr(97+i) for i in indices),length=len(indices),kind=kind,reason=reason)

def e5_contradiction(rows):
    Q=set(range(len(rows[0])));O=Q-H-D;J=H|{e}
    m=next(i for i,row in enumerate(rows) if pre(row,C)==D)
    entering=pre(rows[m],D);assert len(entering)==1 and entering<=J
    p=next(iter(entering));d=rows[m][p];assert d in D and O<=set(rows[m])
    for t,row in enumerate(rows):
        if pre(row,D)!={e} or pre(row,C)==D:continue
        ordinary=image(O-{e},row);missing=O-ordinary;assert len(missing)==1
        if row[d] not in missing:
            x=next(x for x in sorted(O-{e}) if row[x]==row[d])
            q=next(q for q in sorted(Q) if rows[m][q]==x)
            return word((p,q),[m,t],rows,'mandatory','entering_guard_misses_hole')
    assert all(O<=set(row) for row in rows)
    mixed=[(t,pair) for t,row in enumerate(rows) for pair in kernels(row) if not set(pair)<=D]
    if not mixed:
        assert all(pre(row,D)==D or len(pre(row,D))==1 for row in rows)
        return None
    t,pair=mixed[0];k=next(q for q in pair if q in D);x=next(q for q in pair if q in O)
    paths={};todo=deque()
    for i,row in enumerate(rows):
        R=pre(row,D)
        if R!=D:
            assert len(R)==1 and R<=J
            p=next(iter(R));v=row[p]
            if v not in paths:paths[v]=(p,[i]);todo.append(v)
    preserving=[i for i,row in enumerate(rows) if pre(row,D)==D]
    for i in preserving:assert image(O,rows[i])==O
    while todo:
        v=todo.popleft();p,prefix=paths[v]
        for i in preserving:
            q=rows[i][v];assert q in D
            if q not in paths:paths[q]=(p,prefix+[i]);todo.append(q)
    assert set(paths)==D
    p,prefix=paths[k];assert len(prefix)<=2
    S=Q
    for i in prefix:S=image(S,rows[i])
    assert O<=S
    q=next(q for q in sorted(Q) if action(q,prefix,rows)==x)
    return word((p,q),prefix+[t],rows,'mandatory','last_entrance_to_mixed_kernel')

def e15_contradiction(rows):
    Q=set(range(len(rows[0])));O=Q-H-D
    m0=next(i for i,row in enumerate(rows) if pre(row,C)==D)
    t0=next(i for i,row in enumerate(rows) if pre(row,D)=={1,e})
    for m,row in enumerate(rows):
        if pre(row,C)!=D:continue
        p=next(iter(pre(row,D)));assert p in H and image(O,row)==O
        if row[p]==1:
            q=next(q for q in sorted(O) if row[q]==e)
            return word((p,q),[m,t0,m0],rows,'mandatory','supplier_enters_guard1')
    p0=next(iter(pre(rows[m0],D)));assert rows[m0][p0]==2
    for f,row in enumerate(rows):
        if pre(row,D)==D and row[2]==1:
            x=next(x for x in sorted(O) if row[x]==e)
            q=next(q for q in sorted(O) if rows[m0][q]==x)
            return word((p0,q),[m0,f,t0,m0],rows,'mandatory','preserver_sends_2_to_1')
    for t,row in enumerate(rows):
        if pre(row,D)!={1,e}:continue
        missing=O-image(O-{e},row);assert len(missing)==1
        hole=next(iter(missing));assert row[2] in O
        if row[2]!=hole:
            x=next(x for x in sorted(O-{e}) if row[x]==row[2])
            q=next(q for q in sorted(O) if rows[m0][q]==x)
            return word((p0,q),[m0,t],rows,'mandatory','guard2_misses_hole')
        if row[e]==1:
            if hole!=e:
                x=next(x for x in sorted(O-{e}) if row[x]==e)
                return word((e,x),[t,t0,m0],rows,'uncovered','ordinary_enters_guard1_with_e_in_image')
            q=next(q for q in sorted(O) if rows[m0][q]==e)
            return word((p0,q),[m0,t,t0,m0],rows,'mandatory','ordinary_enters_guard1_through_hole')
    assert all(pre(row,{1})<={1} for row in rows)
    raise AssertionError('Strong connectivity with backward-closed state1 is impossible')

def main():
    data=read('c4_d12_individual_controls.json')
    for n,h in data['source_sha256'].items():assert sha(ROOT/n)==h,n
    parent=read('b1_c4_fourth_inventory.json');seed=20261010;rng=random.Random(seed)
    stats=[];examples=[];examples_per={1:0,2:0};boundaries={};total_binary=0
    for record in data['records']:
        n=record['n'];E=set(record['E']);Q=set(range(n));R=Q-K;O=Q-H-D;J=H|{e} if len(E)==1 else H
        z=next(z for z in parent['records'] if z['D']==sorted(D) and z['E']==sorted(E))
        assert z['additional_covered_fibers']==[] and z['mandatory_through_seven']==sorted(J)
        parent_cols={tuple(tuple(f[k]) for k in ('preA','preB','preC','preD')) for f in z['rows']}
        cols=set()
        for X in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
            if all(sum(q in Y for Y in X)<=1 for q in Q):cols.add(tuple(tuple(sorted(Y)) for Y in X))
        assert cols==parent_cols=={tuple(map(tuple,f['pre'])) for f in record['fields']}
        targets=[A,B,C,D,O];pool=[]
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
                if pre(row,D)==D:assert image(O,row)==O
                if pre(row,C)==D:assert O<=set(row)
            pool.extend(rows)
        assert len(pool)==len(set(pool))==record['complete_individual_rows']
        moving=[r for r in pool if pre(r,C)==D];supplying=[r for r in pool if pre(r,D)==E]
        mset=set(moving);tset=set(supplying)
        binary=connected=seeded=seed_connected=sync=closed=0;hist={}
        def check(rows,sample):
            nonlocal connected,seed_connected,sync,closed
            if not strong(rows):return
            if sample:seed_connected+=1
            else:connected+=1
            w=e5_contradiction(rows) if len(E)==1 else e15_contradiction(rows)
            dist=pair_dist(rows);synchronizing=len(dist)==n*(n-1)//2
            sync+=synchronizing
            if w is None:
                closed+=1;assert not synchronizing and all(set(p)<=D for p in dist);return
            pair=tuple(sorted(w['pair']));assert pair in dist and dist[pair]<=w['length']
            if w['kind']=='mandatory':assert set(pair)&J and w['length']<=(3 if len(E)==1 else 4)
            else:assert set(pair)<=R and w['length']<=3
            hist[w['reason']]=hist.get(w['reason'],0)+1
            if examples_per[len(E)]<40:
                examples.append(dict(n=n,E=sorted(E),rows=[list(r) for r in rows],short_merge=w));examples_per[len(E)]+=1
            tag='E5' if len(E)==1 else 'E15'
            if synchronizing:
                dj=min(v for p,v in dist.items() if set(p)&J)
                dr=min(v for p,v in dist.items() if set(p)<=R)
                if tag not in boundaries or (dj,dr)>(boundaries[tag]['earliest_J_pair_merging'],boundaries[tag]['earliest_R_pair_merging']):
                    reset_word=reset(rows);assert reset_word is not None
                    boundaries[tag]=dict(n=n,rows=[list(r) for r in rows],short_merge=w,
                        earliest_J_pair_merging=dj,earliest_R_pair_merging=dr,reset=reset_word)
        if n<=8:
            for a in pool:
                for b in pool:
                    if not (a in mset or b in mset) or not (a in tset or b in tset):continue
                    binary+=1;check([a,b],False)
            expected={6:704,7:5888,8:99072}[n] if len(E)==1 else {6:256,7:2048,8:27648}[n]
            assert binary==expected
        total_binary+=binary
        for alpha in (3,4):
            for _ in range(3000):
                m=rng.choice(moving);t=rng.choice(supplying);rows=[m] if m==t else [m,t]
                rows+=rng.sample([r for r in pool if r not in rows],alpha-len(rows));rng.shuffle(rows)
                seeded+=1;check(rows,True)
        stats.append(dict(n=n,E=sorted(E),individual_rows=len(pool),complete_binary_ordered_alphabets=binary,
            binary_strongly_connected=connected,seeded_larger_alphabets=seeded,seeded_strongly_connected=seed_connected,
            synchronizing_controls=sync,closed_nonsynchronizing_controls=closed,contradiction_word_cases=hist,
            supplier_overlap_rows=len(mset&tset)))
        print(json.dumps(stats[-1]),flush=True)
    assert total_binary==135616
    # Keep the actual wide initial family as literal sets; no uint64 truncation.
    forms=[set(S) for S in combinations(range(13),9) if 3 in S and {0,4,5}<=set(S) and len(set(S)&D)==1]
    assert len(forms)==70 and set.intersection(*forms)==H|{e}
    assert (1<<69).bit_length()==70 and 69>=64
    sample=dict(seed=seed,constructive_samples=examples,boundary_controls=boundaries,
        wide_E5_initial_family=[sorted(S) for S in forms],wide_family_control_bit=69,
        scope='Literal structural controls; no attaining F witnesses or sampled-negative theorem.')
    (ROOT/'c4_d12_unrestricted_samples.json').write_bytes((json.dumps(sample,indent=2)+'\n').encode())
    names=[Path(__file__).name,'enumerate_c4_d12_unrestricted.py','c4_d12_individual_controls.json',
        'c4_d12_unrestricted_samples.json','C4_D12_UNRESTRICTED_EXCLUSION.md',
        'check_c4_d125_guarded_unrestricted.py','b1_c4_fourth_inventory.json','b1_c4_fourth_audit.json',
        'B1_C4_FOURTH_SPACE.md','CLOSED_MERGING_BLOCK.md','closed_merging_block_audit.json',
        'MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    report=dict(status='pass',parameter=[13,9,1],B=[0],C=[4],D=[1,2],
        unrestricted_excluded_E=[[5],[1,5]],complete_individual_rows=7328,
        complete_binary_ordered_alphabets_through_n8=total_binary,seeded_larger_alphabets=48000,
        finite_control_stats=stats,seed=seed,constructive_examples=len(examples),wide_initial_family_size=70,
        wide_family_control_bit=69,boundary_depths={k:[v['earliest_J_pair_merging'],v['earliest_R_pair_merging']] for k,v in boundaries.items()},
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Paper proofs exclude both unrestricted conditional D12 fourth geometries. Finite complete rows/binary controls and seeded larger alphabets support the proofs; whole third transport/composition and numerical F remain unproved here.')
    (ROOT/'c4_d12_unrestricted_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','finite_control_stats')}),flush=True)
if __name__=='__main__':main()
