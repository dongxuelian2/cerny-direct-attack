"""Independent map/graph and literal automaton checks of cover transfer."""
from pathlib import Path
from itertools import product, combinations
from collections import deque
import hashlib,json
ROOT=Path(__file__).resolve().parent

def dist(pair,rows):
    start=frozenset(pair);seen={start};todo=deque([(start,0)])
    while todo:
        X,d=todo.popleft()
        if len(X)==1:return d
        for row in rows:
            Y=frozenset(row[q] for q in X)
            if Y not in seen:seen.add(Y);todo.append((Y,d+1))
    return None

def subsets(n):return [set(q for q in range(n) if mask>>q&1) for mask in range(1<<n)]
def cover(K,G):return all(set(p)&K for p in G)
def main():
    for name in ['two_cover_unique_immediate_pair_audit.json','two_cover_p3_classification_audit.json']:
        z=json.loads((ROOT/name).read_text());assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    Q=set(range(4));pairs=list(combinations(range(4),2));maps=list(product(range(4),repeat=4));Ks=subsets(4)
    graph_cases=qualified=0
    for row in maps:
        missing=Q-set(row)
        for mask in range(1<<len(pairs)):
            G={p for j,p in enumerate(pairs) if mask>>j&1}
            inverse={p for p in pairs if tuple(sorted((row[p[0]],row[p[1]]))) in G}
            for K in Ks:
                graph_cases+=1
                if cover(K,inverse):
                    qualified+=1;assert cover({row[q] for q in K}|missing,G)
    assert graph_cases==256*64*16
    stats=[];semantic_instances=forbidden_checks=0
    for n,alphabet in [(3,2),(3,3),(4,2)]:
        Q=set(range(n));pairs=list(combinations(range(n),2));pool=list(product(range(n),repeat=n));Ks=subsets(n)
        alphabets=qualifying=covers_tested=0
        for rows in product(pool,repeat=alphabet):
            alphabets+=1;ds={p:dist(p,rows) for p in pairs}
            layers=[{p for p,d in ds.items() if d is not None and d<=h} for h in range(7)]
            for h in range(6):
                for K in Ks:
                    if not cover(K,layers[h+1]):continue
                    for row in rows:
                        assert cover({row[q] for q in K}|(Q-set(row)),layers[h]);covers_tested+=1
            if n>=4 and all(d is not None for d in ds.values()):
                for K in Ks:
                    if len(K)!=2 or not cover(K,layers[5]):continue
                    qualifying+=1
                    isolates=Q-set().union(*map(set,layers[3]))
                    assert len(layers[1])==1
                    assert not any(cover(T,layers[3]) for T in Ks if len(T)<=1)
                    for row in rows:
                        assert len(set(row))>=n-1
                        assert not {row[q] for q in K}<=isolates;forbidden_checks+=1
            semantic_instances+=covers_tested
            covers_tested=0
        stats.append(dict(n=n,alphabet=alphabet,complete_ordered_alphabets=alphabets,
                          qualifying_sync_two_cover_cases=qualifying))
    # A missing output can cover an edge whose two inverse fibers do not exist.
    row=(0,0,2,3);G={(0,1)};K=set();assert cover(K,set()) and not cover(set(),G)
    assert cover(Q-set(row),G)
    names=[Path(__file__).name,'PROOF.md#problem4-letter-image-short-pair-cover',
           'PROOF.md#problem4-two-cover-unique-immediate-pair','two_cover_unique_immediate_pair_audit.json',
           'PROOF.md#problem4-two-cover-p3-classification','two_cover_p3_classification_audit.json']
    report=dict(status='pass',uniform_cover_transfer='all n, h>=0, finite alphabets',
                forbidden_protected_image='n>=4, synchronizing, |K|=2, K covers P5',
                complete_n4_map_graph_cover_instances=graph_cases,
                qualifying_map_graph_covers=qualified,semantic_cover_transfers=semantic_instances,
                semantic_stats=stats,forbidden_image_letter_checks=forbidden_checks,
                missing_output_boundary=dict(row=list(row),graph=list(map(list,G)),K=[]),
                source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
                scope='Uniform elementary cover transfer and credited-refinement consequence; no F value.')
    (ROOT/'letter_image_short_pair_cover_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
