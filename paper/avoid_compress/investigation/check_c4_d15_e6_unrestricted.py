"""Independent full supplier controls, forward words and pair/image closures."""
from pathlib import Path
from itertools import product,combinations
from collections import deque
import hashlib,json,random,math
from check_c4_d125_guarded_unrestricted import strong,pair_dist,reset
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};H=A|B|C;D={1,5};E={6};K={1,2};G0={(1,5),(2,6)}

def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def image(X,row):return {row[q] for q in X}
def pre(row,X):return {q for q,t in enumerate(row) if t in X}
def action(q,w,rows):
    for ch in w:q=rows[ord(ch)-97][q]
    return q

def forward_word(pair,rows):
    start=frozenset(pair);todo=deque([start]);words={start:''}
    while todo:
        X=todo.popleft();w=words[X]
        if len(X)==1:return w
        for i,row in enumerate(rows):
            Y=frozenset(row[q] for q in X)
            if Y not in words:words[Y]=w+chr(97+i);todo.append(Y)
    return None

def closed_certificate(rows,dist):
    Q=set(range(len(rows[0])));P1={p for p,d in dist.items() if d==1};G=set(dist)
    assert len(G)<len(Q)*(len(Q)-1)//2
    if P1=={(1,5)}:
        assert all(pre(row,D)<=D or len(pre(row,D))<=1 for row in rows)
        assert G=={(1,5)};reason='closed_D15_block'
    else:reason='proper_closed_pair_graph'
    for row in rows:
        for p in combinations(sorted(Q),2):
            if row[p[0]]==row[p[1]]:assert p in G
            elif tuple(sorted((row[p[0]],row[p[1]]))) in G:assert p in G
    return dict(type='closed_pair_graph',reason=reason,edges=[list(p) for p in sorted(G)])

def main():
    data=read('c4_d15_e6_individual_controls.json');classification=read('two_cover_unique_immediate_pair_audit.json')
    for z in (data,classification):
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert classification['status']=='pass'
    parent=read('b1_c4_fourth_inventory.json');z=next(z for z in parent['records'] if z['D']==sorted(D) and z['E']==sorted(E))
    assert z['additional_covered_fibers']==[] and z['mandatory_through_seven']==sorted(H|E)
    parent_cols={tuple(tuple(f[k]) for k in ('preA','preB','preC','preD')) for f in z['rows']}
    seed=20261010;rng=random.Random(seed);stats=[];examples=[];closures=[];boundary=None;total_binary=total_ternary=0;reason_examples={}
    for record in data['records']:
        n=record['n'];Q=set(range(n));O=Q-H-D;R=Q-K;targets=[A,B,C,D,O]
        cols=set()
        for X in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
            if all(sum(q in Y for Y in X)<=1 for q in Q):cols.add(tuple(tuple(sorted(Y)) for Y in X))
        assert cols==parent_cols=={tuple(map(tuple,f['pre'])) for f in record['fields']} and len(cols)==16
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
        mset={r for r in pool if pre(r,C)==D};tset={r for r in pool if pre(r,D)==E};intersection=mset&tset
        m=len(O);fac=math.factorial(m)
        assert len(mset)==16*m*fac and len(tset)==8*m*(m+1)*fac and len(intersection)==8*m*fac
        binary=ternary=seeded=connected=sync=closed=dual=words=0;hist={}
        def check(rows):
            nonlocal connected,sync,closed,dual,words,boundary
            dual+=int(any(r in intersection for r in rows));dist=pair_dist(rows)
            assert dist[(1,5)]==1
            synchronizing=len(dist)==n*(n-1)//2;sync+=int(synchronizing)
            connected_here=strong(rows);connected+=int(connected_here)
            candidates=[(d,p) for p,d in dist.items() if not set(p)&K and d<=5]
            if not candidates:
                assert not synchronizing
                cert=closed_certificate(rows,dist);closed+=1;hist[cert['reason']]=hist.get(cert['reason'],0)+1
                if sum(s['certificate']['reason']==cert['reason'] for s in closures)<5:closures.append(dict(n=n,rows=list(map(list,rows)),certificate=cert))
                return
            d,p=min(candidates);w=forward_word(p,rows);assert w is not None and len(w)==d<=5
            assert action(p[0],w,rows)==action(p[1],w,rows) and not set(p)&K;words+=1
            hist[f'outside_K_word_length_{d}']=hist.get(f'outside_K_word_length_{d}',0)+1
            short=dict(type='short_word',pair=list(p),word=w,length=d,kind='uncovered')
            if reason_examples.get(d,0)<10:
                examples.append(dict(n=n,rows=list(map(list,rows)),short_merge=short));reason_examples[d]=reason_examples.get(d,0)+1
            if synchronizing and connected_here:
                dj=min(v for pair,v in dist.items() if set(pair)&H);score=[d,dj]
                if boundary is None or score>boundary['selection_score']:
                    rw=reset(rows);assert rw is not None
                    boundary=dict(n=n,rows=list(map(list,rows)),short_merge=short,reset=rw,
                        earliest_J_pair_merging=dj,earliest_R_pair_merging=d,selection_score=score)
        if n<=8:
            for rows in product(pool,repeat=2):
                if not any(r in mset for r in rows) or not any(r in tset for r in rows):continue
                binary+=1;check(rows)
            assert binary==64*m*m*(4*m+7)*fac*fac
        total_binary+=binary
        if n==7:
            for rows in combinations(pool,3):
                if not any(r in mset for r in rows) or not any(r in tset for r in rows):continue
                ternary+=1;check(rows)
            assert ternary==718688
        total_ternary+=ternary
        for alpha in (3,4):
            for _ in range(3000):
                # Retain both the separate-supplier and dual-supplier routes.
                if rng.randrange(2):rows=[rng.choice(sorted(intersection))]
                else:rows=sorted(set((rng.choice(sorted(mset)),rng.choice(sorted(tset)))))
                rows+=rng.sample([r for r in pool if r not in rows],alpha-len(rows));rng.shuffle(rows)
                seeded+=1;check(rows)
        assert words+closed==binary+ternary+seeded
        stats.append(dict(n=n,individual_rows=len(pool),dual_supplier_rows=len(intersection),complete_binary_ordered_alphabets=binary,
            complete_distinct_ternary_supplier_sets=ternary,seeded_larger_alphabets=seeded,controls_with_dual_supplier=dual,
            synchronizing_controls=sync,strongly_connected_controls=connected,outside_K_short_words=words,
            nonsynchronizing_cover_certificates=closed,control_histogram=hist))
        print(json.dumps(stats[-1]),flush=True)
    assert total_binary==409344 and total_ternary==718688 and boundary is not None
    sample=dict(seed=seed,constructive_samples=examples,closed_pair_samples=closures,boundary_control=boundary,
        scope='Literal structural controls only; no attaining F example or sampled-negative theorem.')
    (ROOT/'c4_d15_e6_unrestricted_samples.json').write_bytes((json.dumps(sample,indent=2)+'\n').encode())
    names=[Path(__file__).name,'enumerate_c4_d15_e6_unrestricted.py','c4_d15_e6_individual_controls.json',
        'c4_d15_e6_unrestricted_samples.json','C4_D15_E6_UNRESTRICTED_EXCLUSION.md','TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md',
        'two_cover_unique_immediate_pair_audit.json','CLOSED_MERGING_BLOCK.md','closed_merging_block_audit.json',
        'check_c4_d125_guarded_unrestricted.py','b1_c4_fourth_inventory.json','b1_c4_fourth_audit.json','B1_C4_FOURTH_SPACE.md',
        'MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    report=dict(status='pass',parameter=[13,9,1],B=[0],C=[4],D=[1,5],E=sorted(E),unrestricted_E6_paper_excluded=True,
        needs_strong_connectivity=False,needs_mandatory_isolation=False,complete_individual_fields=16,complete_individual_rows=7344,
        complete_binary_ordered_alphabets_through_n8=total_binary,complete_distinct_ternary_supplier_sets_at_n7=total_ternary,
        seeded_larger_alphabets=18000,seed=seed,constructive_examples=len(examples),closed_frame_examples=len(closures),finite_control_stats=stats,
        boundary_depths=[boundary['earliest_J_pair_merging'],boundary['earliest_R_pair_merging']],
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Paper proof excludes arbitrary-alphabet conditional D15/E6 fourth geometry. All finite supplier controls retain dual suppliers and check synchronization without an SC filter. Whole D15 third composition and numerical F require a separate audit.')
    (ROOT/'c4_d15_e6_unrestricted_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','finite_control_stats')}),flush=True)
if __name__=='__main__':main()
