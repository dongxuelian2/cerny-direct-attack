"""Independent per-input cover and constructive unrestricted proof checks."""
from pathlib import Path
from itertools import product,combinations
from collections import deque
import hashlib,json,random
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};D={1,2,5};K={1,2};e=6
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def image(S,row):return {row[q] for q in S}
def pre(row,T):return {q for q,t in enumerate(row) if t in T}
def strong(rows):
    n=len(rows[0])
    for source in range(n):
        todo=[source];seen={source}
        for q in todo:
            for row in rows:
                if row[q] not in seen:seen.add(row[q]);todo.append(row[q])
        if len(seen)!=n:return False
    return True
def pair_dist(rows):
    n=len(rows[0]);pairs=list(combinations(range(n),2));back={p:[] for p in pairs};dist={};todo=deque()
    for p in pairs:
        for row in rows:
            t=tuple(sorted({row[q] for q in p}))
            if len(t)==1:
                if p not in dist:dist[p]=1;todo.append(p)
            else:back[t].append(p)
    while todo:
        p=todo.popleft()
        for old in back[p]:
            if old not in dist:dist[old]=dist[p]+1;todo.append(old)
    return dist
def action(q,word,rows):
    for i in word:q=rows[i][q]
    return q
def reset(rows):
    start=frozenset(range(len(rows[0])));todo=deque([start]);words={start:''}
    while todo:
        S=todo.popleft();w=words[S]
        if len(S)==1:return w
        for i,row in enumerate(rows):
            T=frozenset(image(S,row))
            if T not in words:words[T]=w+chr(97+i);todo.append(T)
    return None

def construct(rows,E):
    n=len(rows[0]);R=set(range(n))-K;O=set(range(n))-A-B-C-D
    m=next(i for i,row in enumerate(rows) if pre(row,C)==D)
    t=next(i for i,row in enumerate(rows) if pre(row,D)==E)
    assert all(O<=image(R,row) for row in rows)
    if len(E)==3:
        l,q=next((i,q) for i,row in enumerate(rows) for q in sorted(R) if row[q] in K)
        x=next(x for x in sorted(R) if rows[l][x]==e);word=[l,t,m]
    else:
        direct=next(((i,q) for i,row in enumerate(rows) for q in sorted(R) if row[q]==1),None)
        if direct:
            l,q=direct;x=next(x for x in sorted(R) if rows[l][x]==e);word=[l,t,m]
        else:
            f=next(i for i,row in enumerate(rows) if row[2]==1)
            assert pre(rows[f],D)==D and image(O,rows[f])==O
            sentinel=next(x for x in sorted(O) if rows[f][x]==e)
            l,q=next((i,q) for i,row in enumerate(rows) for q in sorted(R) if row[q]==2)
            x=next(x for x in sorted(R) if rows[l][x]==sentinel);word=[l,f,t,m]
    assert q!=x and q in R and x in R
    assert action(q,word,rows)==action(x,word,rows)
    assert len(word)<= (3 if len(E)==3 else 4)
    return dict(pair=[q,x],word=''.join(chr(97+i) for i in word),length=len(word))

def main():
    data=read('c4_d125_guarded_individual_controls.json')
    for n,h in data['source_sha256'].items():assert sha(ROOT/n)==h,n
    parent=read('b1_c4_fourth_inventory.json');seed=20261010;rng=random.Random(seed)
    stats=[];examples=[];boundaries={};total_pairs=0
    for record in data['records']:
        n=record['n'];E=set(record['E']);Q=set(range(n));R=Q-K;O=Q-A-B-C-D;targets=[A,B,C,D,O]
        z=next(z for z in parent['records'] if z['D']==sorted(D) and z['E']==sorted(E))
        assert z['additional_covered_fibers']==[]
        parent_cols={tuple(tuple(f[k]) for k in ('preA','preB','preC','preD')) for f in z['rows']}
        cols=[]
        for choice in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
            if all(sum(q in X for X in choice)<=1 for q in Q):cols.append(tuple(tuple(sorted(X)) for X in choice))
        assert len(cols)==12 and set(cols)==parent_cols
        assert set(cols)=={tuple(map(tuple,f['pre'])) for f in record['fields']}
        pool=[]
        for field in record['fields']:
            groups=list(map(set,field['pre']));groups.append(Q-set().union(*groups))
            options={q:targets[next(i for i,X in enumerate(groups) if q in X)] for q in Q}
            row=[-1]*n;rows=[]
            def visit(q):
                if q==n:rows.append(tuple(row));return
                for v in sorted(options[q]):
                    if q in R and any(p in R and row[p]==v for p in range(q)):continue
                    row[q]=v;visit(q+1);row[q]=-1
            visit(0);rows.sort();assert rows==list(map(tuple,field['rows']))
            for row in rows:
                assert len(image(R,row))==n-2 and O<=image(R,row)
                for X,Y in zip(groups,targets):assert pre(row,Y)==X
                if pre(row,D)==D:assert image(O,row)==O
            pool.extend(rows)
        assert len(pool)==len(set(pool))==record['complete_individual_rows']
        moving=[r for r in pool if pre(r,C)==D];supplying=[r for r in pool if pre(r,D)==E]
        assert set(moving).isdisjoint(supplying)
        complete=connected=synchronizing=sampled=sample_connected=0;max_depth=0
        def check(rows,sample):
            nonlocal connected,synchronizing,sample_connected,max_depth
            if not strong(rows):return
            if sample:sample_connected+=1
            else:connected+=1
            w=construct(rows,E);dist=pair_dist(rows)
            earliest=min(v for p,v in dist.items() if set(p)<=R)
            assert earliest<=w['length']<= (3 if len(E)==3 else 4)
            if len(dist)==n*(n-1)//2:synchronizing+=1
            max_depth=max(max_depth,earliest)
            if len(examples)<60:examples.append(dict(n=n,E=sorted(E),rows=[list(r) for r in rows],short_merge=w,earliest_R_pair_merging=earliest))
            if earliest==4 and len(E)==2 and 'E16' not in boundaries:
                reset_word=reset(rows)
                if reset_word is not None:boundaries['E16']=dict(n=n,rows=[list(r) for r in rows],earliest_R_pair_merging=4,short_merge=w,reset=reset_word)
            if earliest==3 and len(E)==3 and 'E126' not in boundaries:
                reset_word=reset(rows)
                if reset_word is not None:boundaries['E126']=dict(n=n,rows=[list(r) for r in rows],earliest_R_pair_merging=3,short_merge=w,reset=reset_word)
        for m in moving:
            for t in supplying:
                for rows in ((m,t),(t,m)):complete+=1;check(rows,False)
        total_pairs+=complete
        for alpha in (3,4):
            for _ in range(3000):
                m=rng.choice(moving);t=rng.choice(supplying)
                rest=rng.sample([r for r in pool if r!=m and r!=t],alpha-2)
                rows=[m,t,*rest];rng.shuffle(rows);sampled+=1;check(rows,True)
        stats.append(dict(n=n,E=sorted(E),individual_rows=len(pool),complete_binary_ordered_alphabets=complete,
            binary_strongly_connected=connected,seeded_larger_alphabets=sampled,seeded_strongly_connected=sample_connected,
            synchronizing_controls=synchronizing,maximum_earliest_R_pair_depth=max_depth))
        print(json.dumps(stats[-1]),flush=True)
    assert total_pairs==207360
    # Literal essential-hypothesis controls for the uniform trap.
    controls=[];cycle=[1,2,0]
    for omitted,b,sentinel,expected in [('cover',[2,1,2],2,[False,True,True]),
        ('seed',[1,1,2],2,[True,False,True]),('free_image',[1,1,2],1,[True,True,False])]:
        rows=[cycle,b];dist=pair_dist(rows);R={1,2}
        actual=[all(0 in p for p,d in dist.items() if d<=2),dist.get((0,sentinel),99)<=1,
            all(sentinel in image(R,row) for row in rows)]
        assert actual==expected and strong(rows)
        w=reset(rows);assert w is not None
        controls.append(dict(omitted=omitted,rows=rows,e=sentinel,hypotheses=actual,reset=w))
    sample=dict(seed=seed,constructive_samples=examples,boundary_controls=boundaries,
        omitted_hypothesis_controls=controls,scope='Structural controls only; no attaining F witness or sampled-negative theorem.')
    (ROOT/'c4_d125_guarded_unrestricted_samples.json').write_bytes((json.dumps(sample,indent=2)+'\n').encode())
    names=[Path(__file__).name,'enumerate_c4_d125_guarded_unrestricted.py','c4_d125_guarded_individual_controls.json',
        'c4_d125_guarded_unrestricted_samples.json','C4_D125_E16_E126_UNRESTRICTED_EXCLUSION.md',
        'UNIVERSAL_FREE_IMAGE_TRAP.md','b1_c4_fourth_inventory.json','b1_c4_fourth_audit.json',
        'B1_C4_FOURTH_SPACE.md','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md',
        'MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json']
    result=dict(status='pass',parameter=[13,9,1],B=[0],C=[4],D=[1,2,5],
        unrestricted_excluded_E=[[1,6],[1,2,6]],complete_individual_rows=3960,
        complete_binary_ordered_alphabets=total_pairs,seeded_larger_alphabets=sum(s['seeded_larger_alphabets'] for s in stats),
        stats=stats,seed=seed,omitted_hypothesis_controls=3,boundary_depths={k:v['earliest_R_pair_merging'] for k,v in boundaries.items()},
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Paper proofs exclude unrestricted guarded E16/E126 conditional geometries. Complete finite rows and binary controls plus seeded larger controls support the proof; whole D composition and numerical F remain unproved here.')
    (ROOT/'c4_d125_guarded_unrestricted_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('stats','source_sha256')}),flush=True)
if __name__=='__main__':main()
