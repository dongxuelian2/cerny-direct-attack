"""Independent literal row cover and constructive short-pair proof controls."""
from pathlib import Path
from itertools import product,combinations
from collections import deque
import hashlib,json,random
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};D={1,2,5};E={6};K={1,2};J={0,3,4,6}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def image(S,row):return {row[q] for q in S}
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

def strong(rows):
    n=len(rows[0])
    for source in range(n):
        todo=[source];seen={source}
        for q in todo:
            for row in rows:
                if row[q] not in seen:seen.add(row[q]);todo.append(row[q])
        if len(seen)!=n:return False
    return True

def preD(row):return {q for q,t in enumerate(row) if t in D}
def kernels(row):return [(x,y) for x,y in combinations(range(len(row)),2) if row[x]==row[y]]
def action(q,word,rows):
    for i in word:q=rows[i][q]
    return q

def constructive(rows):
    n=len(rows[0]);Q=set(range(n));O=Q-A-B-C-D
    assert strong(rows)
    mixed=[(i,p) for i,row in enumerate(rows) for p in kernels(row) if not set(p)<=D]
    if not mixed:
        assert all(R<=D or len(R)<=1 for R in map(preD,rows))
        assert all(set(p)<=D for p in pair_dist(rows))
        return None
    t,pair=mixed[0];k=next(q for q in pair if q in D);x=next(q for q in pair if q in O)
    paths={};todo=deque()
    for i,row in enumerate(rows):
        R=preD(row)
        if R!=D:
            assert len(R)==1 and R<=J
            p=next(iter(R));v=row[p]
            if v not in paths:paths[v]=(p,[i]);todo.append(v)
    preserving=[i for i,row in enumerate(rows) if preD(row)==D]
    while todo:
        v=todo.popleft();p,word=paths[v]
        for i in preserving:
            q=rows[i][v];assert q in D
            if q not in paths:paths[q]=(p,word+[i]);todo.append(q)
    assert set(paths)==D
    p,prefix=paths[k];assert len(prefix)<=3 and action(p,prefix,rows)==k
    assert O<=image(Q,rows[prefix[0]])
    S=Q
    for i in prefix:S=image(S,rows[i])
    assert O<=S
    q=next(q for q in Q if action(q,prefix,rows)==x);assert q!=p
    word=prefix+[t];assert len(word)<=4 and action(p,word,rows)==action(q,word,rows)
    return dict(pair=[p,q],word=''.join(chr(97+i) for i in word),length=len(word))

def reset(rows):
    start=frozenset(range(len(rows[0])));todo=deque([start]);words={start:''}
    while todo:
        S=todo.popleft();w=words[S]
        if len(S)==1:return w
        for i,row in enumerate(rows):
            T=frozenset(image(S,row))
            if T not in words:words[T]=w+chr(97+i);todo.append(T)
    return None

def main():
    control=read('c4_d125_e6_individual_controls.json')
    for n,h in control['source_sha256'].items():assert sha(ROOT/n)==h,n
    parent=read('b1_c4_fourth_inventory.json')
    z=next(z for z in parent['records'] if z['D']==[1,2,5] and z['E']==[6])
    assert z['mandatory_through_seven']==sorted(J) and z['additional_covered_fibers']==[]
    actual_cols={tuple(tuple(f[k]) for k in ('preA','preB','preC','preD')) for f in z['rows']}
    assert len(actual_cols)==16
    stats=[];examples=[];seed=20261010;rng=random.Random(seed)
    for record in control['records']:
        n=record['n'];Q=set(range(n));O=Q-A-B-C-D;targets=[A,B,C,D,O];pool=[]
        tuples=[]
        for pre in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
            compatible=True
            for q in Q:
                pattern=tuple(q in X for X in pre)
                if sum(pattern)>1:compatible=False;break
            if compatible:tuples.append(tuple(tuple(sorted(X)) for X in pre))
        assert len(tuples)==16 and set(tuples)==actual_cols
        assert set(tuples)=={tuple(map(tuple,f['pre'])) for f in record['fields']}
        for field in record['fields']:
            pre=list(map(set,field['pre']));inputs=[*pre,Q-set().union(*pre)];group={q:i for i,X in enumerate(inputs) for q in X}
            rows=[];row=[-1]*n
            def visit(q):
                if q==n:rows.append(tuple(row));return
                for t in sorted(targets[group[q]]):
                    if q not in K and any(p not in K and row[p]==t for p in range(q)):continue
                    row[q]=t;visit(q+1);row[q]=-1
            visit(0);rows.sort();assert rows==list(map(tuple,field['rows']))
            for row in rows:
                assert len(image(Q-K,row))==n-2
                for R,T in zip(pre,targets[:4]):assert {q for q in Q if row[q] in T}==R
                R=preD(row);ker=kernels(row)
                if R==D:
                    assert image(O,row)==O and all(set(p)<=D for p in ker)
                else:
                    assert len(R)==1 and R<=J and O<=set(row)
                    if pre[2]==D:assert all(set(p)<=D for p in ker)
                    else:
                        assert R==E
                        for pair in ker:
                            if not set(pair)<=D:assert len(set(pair)&D)==1 and len(set(pair)&O)==1
            pool.extend(rows)
        assert len(pool)==record['complete_individual_rows']=={7:144,8:360,9:1440}[n]
        assert len(set(pool))==len(pool)
        total=connected=synchronizing=witnesses=closed=0
        for alpha in (2,3,4):
            for j in range(2000):
                rows=rng.sample(pool,alpha);total+=1
                if not strong(rows):continue
                connected+=1;w=constructive(rows);dist=pair_dist(rows)
                if len(dist)==n*(n-1)//2:synchronizing+=1
                if w is None:closed+=1;assert len(dist)<n*(n-1)//2
                else:
                    witnesses+=1;assert min(v for p,v in dist.items() if set(p)&J)<=4
                    if len(examples)<60:examples.append(dict(n=n,rows=[list(r) for r in rows],short_merge=w))
        stats.append(dict(n=n,complete_individual_rows=len(pool),seeded_alphabets=total,
            strongly_connected=connected,synchronizing=synchronizing,constructive_short_merge_witnesses=witnesses,
            closed_nonsynchronizing=closed))
    boundary=[[3,4,4,7,0,4,5,6],[0,7,6,3,4,6,5,7],[0,5,1,3,4,2,6,7]]
    assert strong(boundary);dist=pair_dist(boundary);assert len(dist)==28
    earliest=min(v for p,v in dist.items() if set(p)&J);assert earliest==4
    w=constructive(boundary);assert w and w['length']==4
    reset_word=reset(boundary);assert reset_word is not None
    sample=dict(seed=seed,short_merge_controls=examples,boundary=dict(n=8,rows=boundary,
        earliest_J_pair_merging=4,short_merge=w,reset=reset_word,scope='Structural boundary only, not an attaining F witness.'))
    (ROOT/'c4_d125_e6_unrestricted_samples.json').write_bytes((json.dumps(sample,indent=2)+'\n').encode())
    names=[Path(__file__).name,'enumerate_c4_d125_e6_unrestricted.py','c4_d125_e6_individual_controls.json',
        'c4_d125_e6_unrestricted_samples.json','PROOF.md#problem4-c4-d125-e6-unrestricted-exclusion','b1_c4_fourth_inventory.json',
        'b1_c4_fourth_audit.json','PROOF.md#problem4-b1-c4-fourth-space','PROOF.md#problem4-closed-merging-block','closed_merging_block_audit.json',
        'PROOF.md#problem4-mandatory-core-isolation','mandatory_core_isolation_audit.json','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    report=dict(status='pass',parameter=[13,9,1],B=[0],C=[4],D=[1,2,5],E=[6],
        unrestricted_E6_paper_excluded=True,all_individual_fields=16,complete_individual_control_rows=1944,
        finite_row_controls=stats,seeded_alphabets=sum(s['seeded_alphabets'] for s in stats),
        seed=seed,constructive_samples=len(examples),boundary_J_merge_depth=4,
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Uniform paper proof excludes unrestricted B0/C4/D125/E6 at equality12. Finite individual rows and seeded alphabets support the proof; E16/E126, whole D/joint, numerical F and alphabet separation remain unproved.')
    (ROOT/'c4_d125_e6_unrestricted_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
