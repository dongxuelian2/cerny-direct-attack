"""Independent forward row generation and literal merging/closure controls."""
from pathlib import Path
from itertools import product,combinations
import hashlib,json,random,math
from collections import deque
from check_c4_d125_guarded_unrestricted import pair_dist,strong,reset
ROOT=Path(__file__).resolve().parent
K={1,2};J={0,3,4,5};E={1,2}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def word(pair,rows):
    X=frozenset(pair);todo=deque([X]);words={X:''}
    while todo:
        X=todo.popleft()
        if len(X)==1:return words[X]
        for i,row in enumerate(rows):
            Y=frozenset(row[q] for q in X)
            if Y not in words:words[Y]=words[X]+chr(97+i);todo.append(Y)
    return None
def action(X,w,rows):
    for ch in w:X={rows[ord(ch)-97][q] for q in X}
    return X
def main():
    data=read('c4_d5_e12_unique_kernel_individual_controls.json')
    generic=read('letter_image_short_pair_cover_audit.json');assert generic['status']=='pass'
    for z in (data,generic):
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,n
    rng=random.Random(20261010);stats=[];examples=[];closures=[];counts={};boundary=None
    total_binary=total_ternary=seeded_total=0
    for record in data['records']:
        n=record['n'];Q=set(range(n));O=Q-J;pool=[];M=set();T=set()
        for field in record['fields']:
            pre=list(map(set,field['pre']));options=[]
            for q in range(n):
                h=next((i for i,X in enumerate(pre) if q in X),None)
                options.append([3,0,4,5][h:h+1] if h is not None else sorted(O))
            raw=[];row=[-1]*n
            def visit(q):
                if q==n:raw.append(tuple(row));return
                for t in options[q]:
                    if any(row[p]==t and {p,q}!=E for p in range(q)):continue
                    row[q]=t;visit(q+1)
                row[q]=-1
            visit(0)
            assert set(raw)==set(map(tuple,field['rows'])) and len(raw)==(1 if pre[3]==E else 2)*math.factorial(n-4)
            pool.extend(raw)
            if pre[2]=={5}:M.update(raw)
            if pre[3]==E:T.update(raw)
        pool=sorted(set(pool));fac=math.factorial(n-4)
        assert len(pool)==24*fac and len(M)==12*fac and len(T)==8*fac and len(M&T)==4*fac
        binary=ternary=seeded=sync=sc=closed=Rwords=Jwords=dual=0;hist={}
        def check(rows):
            nonlocal sync,sc,closed,Rwords,Jwords,dual,boundary
            ds=pair_dist(rows);assert {p for p,d in ds.items() if d==1}=={(1,2)}
            dual+=int(any(r in M&T for r in rows));synchronizing=len(ds)==n*(n-1)//2;sync+=int(synchronizing)
            connected=strong(rows);sc+=int(connected)
            rc=[(d,p) for p,d in ds.items() if not set(p)&K and d<=5]
            jc=[(d,p) for p,d in ds.items() if set(p)&J and d<=3]
            if rc or jc:
                kind='outside_K' if rc else 'mandatory_incident';d,p=min(rc or jc);w=word(p,rows)
                assert len(w)==d and len(action(set(p),w,rows))==1
                if kind=='outside_K':Rwords+=1
                else:Jwords+=1
                label=f'{kind}_{d}';hist[label]=hist.get(label,0)+1
                if counts.get(label,0)<10:
                    examples.append(dict(n=n,rows=list(map(list,rows)),pair=list(p),word=w,length=d,kind=kind));counts[label]=counts.get(label,0)+1
            else:
                assert not synchronizing
                G=set(ds);assert len(G)<n*(n-1)//2
                for row in rows:
                    for p in combinations(range(n),2):
                        target=tuple(sorted(row[q] for q in p))
                        if target[0]==target[1] or target in G:assert p in G
                closed+=1;hist['proper_closed_pair_graph']=hist.get('proper_closed_pair_graph',0)+1
                if len(closures)<10:closures.append(dict(n=n,rows=list(map(list,rows)),edges=list(map(list,sorted(G)))))
            if synchronizing and connected:
                dr=min(d for p,d in ds.items() if not set(p)&K);dj=min(d for p,d in ds.items() if set(p)&J)
                assert dr<=5 or dj<=3
                score=[dr,dj]
                if boundary is None or score>boundary['selection_score']:
                    rw=reset(rows);assert len(action(Q,rw,rows))==1
                    boundary=dict(n=n,rows=list(map(list,rows)),reset=rw,earliest_R_merger=dr,earliest_J_merger=dj,selection_score=score)
        if n<=8:
            for rows in product(pool,repeat=2):
                if not any(r in M for r in rows) or not any(r in T for r in rows):continue
                binary+=1;check(rows)
            assert binary==240*fac*fac
        if n<=7:
            for rows in combinations(pool,3):
                if not any(r in M for r in rows) or not any(r in T for r in rows):continue
                ternary+=1;check(rows)
            assert ternary==math.comb(24*fac,3)-math.comb(12*fac,3)-math.comb(16*fac,3)+math.comb(8*fac,3)
        for alphabet in (3,4):
            for _ in range(3000):
                rows=[rng.choice(sorted(M)),rng.choice(sorted(T))]+[rng.choice(pool) for i in range(alphabet-2)]
                seeded+=1;check(tuple(rows))
        assert binary+ternary+seeded==Rwords+Jwords+closed
        total_binary+=binary;total_ternary+=ternary;seeded_total+=seeded
        stats.append(dict(n=n,individual_rows=len(pool),complete_binary_ordered_alphabets=binary,
                          complete_distinct_ternary_sets=ternary,seeded_alphabets=seeded,synchronizing_controls=sync,
                          strongly_connected_controls=sc,dual_supplier_controls=dual,R_short_words=Rwords,
                          J_short_words=Jwords,proper_closed_graphs=closed,histogram=hist))
        print(json.dumps(stats[-1]),flush=True)
    assert total_binary==147840 and total_ternary==312992 and seeded_total==24000 and boundary is not None
    sample=dict(seed=20261010,constructive_samples=examples,closed_pair_samples=closures,boundary_control=boundary,
                scope='Structural disjunction controls; no attaining F example.')
    (ROOT/'c4_d5_e12_unique_kernel_samples.json').write_bytes((json.dumps(sample,indent=2)+'\n').encode())
    names=[Path(__file__).name,'enumerate_c4_d5_e12_unique_kernel.py','c4_d5_e12_unique_kernel_individual_controls.json',
           'c4_d5_e12_unique_kernel_samples.json','PROOF.md#problem4-c4-d5-e12-e126-unrestricted-exclusion',
           'PROOF.md#problem4-letter-image-short-pair-cover','letter_image_short_pair_cover_audit.json',
           'PROOF.md#problem4-two-cover-unique-immediate-pair','two_cover_unique_immediate_pair_audit.json',
           'check_c4_d125_guarded_unrestricted.py','b1_c4_fourth_inventory.json',
           'PROOF.md#problem4-mandatory-core-isolation','mandatory_core_isolation_audit.json']
    report=dict(status='pass',parameter=[13,9,1],D=[5],excluded_E=[[1,2],[1,2,6]],alphabet='arbitrary finite',
                E12_needs_mandatory_isolation=True,E126_needs_mandatory_isolation=False,
                complete_conditional_individual_rows=3648,unique_kernel_domain_restriction_explicit=True,
                complete_binary_ordered_alphabets_through_n8=total_binary,
                complete_distinct_ternary_sets_through_n7=total_ternary,seeded_larger_alphabets=seeded_total,
                constructive_samples=len(examples),closed_pair_samples=len(closures),control_stats=stats,
                boundary_depths=[boundary['earliest_J_merger'],boundary['earliest_R_merger']],
                source_sha256={n:sha(ROOT/n) for n in names},
                scope='Two conditional arbitrary-alphabet D5 fourth exclusions. E6/E16, whole third and numerical F unresolved.')
    (ROOT/'c4_d5_e12_e126_unrestricted_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','control_stats')}),flush=True)
if __name__=='__main__':main()
