"""Complete fixed-two-cover graph enumeration and n4 automaton controls."""
from pathlib import Path
from itertools import product,combinations
import hashlib,json
from check_finite_independent_image_trap import forward_pair,reachable
ROOT=Path(__file__).resolve().parent

def shape(G):
    active=set().union(*map(set,G)) if G else set()
    degrees=sorted(sum(q in e for e in G) for q in active)
    if len(G)==2 and len(active)==4 and degrees==[1,1,1,1]:return 'two_disjoint_edges'
    if len(G)==3 and len(active)==3 and degrees==[2,2,2]:return 'triangle'
    if len(G)==3 and len(active)==4 and degrees==[1,1,2,2]:return 'four_vertex_path'
    return None

def covers(G,n,k):
    return [set(S) for S in combinations(range(n),k) if all(set(S)&set(e) for e in G)]

def main():
    premise=json.loads((ROOT/'finite_independent_image_trap_audit.json').read_text());assert premise['status']=='pass'
    for n,h in premise['source_sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
    stats=[];total=0
    for n in range(4,10):
        edges=[e for e in combinations(range(n),2) if set(e)&{0,1}];assert len(edges)==2*n-3
        graphs=qualifying=0;hist={};counts={}
        for mask in range(1<<len(edges)):
            G=[e for i,e in enumerate(edges) if mask&(1<<i)];graphs+=1
            if not G or covers(G,n,1):continue
            family=covers(G,n,2);assert {0,1} in family
            N=len(family);counts[str(N)]=counts.get(str(N),0)+1
            if N<3:continue
            kind=shape(G);assert kind is not None and N==(4 if kind=='two_disjoint_edges' else 3)
            qualifying+=1;hist[kind]=hist.get(kind,0)+1
        assert hist==dict(two_disjoint_edges=(n-2)*(n-3),four_vertex_path=3*(n-2)*(n-3),triangle=n-2)
        total+=graphs;stats.append(dict(n=n,complete_graphs_with_fixed_two_cover=graphs,minimum_cover_two_histogram=counts,
            qualifying_at_least_three_two_covers=qualifying,shape_histogram=hist))
    assert total==43680
    # Semantic controls use the true short-pair graphs, not arbitrary graphs.
    n=4;pool=list(product(range(n),repeat=n));pairs=list(combinations(range(n),2))
    tested=qualified=strong=0;hist={};examples=[]
    for rows in product(pool,repeat=2):
        tested+=1;ds={p:forward_pair(p,rows) for p in pairs}
        if any(d is None for d in ds.values()) or ds[(2,3)]<=5:continue
        qualified+=1;G=[p for p,d in ds.items() if d<=3];kind=shape(G);assert kind is not None
        assert all(set(p)&{0,1} for p,d in ds.items() if d<=5)
        family=covers(G,n,2);assert len(family)>=3
        full=reachable(set(range(n)),rows);assert any(len(S)==1 for S in full)
        connected=True
        for q in range(n):
            todo=[q];seen={q}
            for p in todo:
                for row in rows:
                    if row[p] not in seen:seen.add(row[p]);todo.append(row[p])
            connected &= len(seen)==n
        strong+=int(connected);hist[kind]=hist.get(kind,0)+1
        if len(examples)<4:examples.append(dict(rows=rows,short_pair_graph=G,shape=kind,two_cover_count=len(family),strongly_connected=connected))
    assert tested==65536 and qualified>0
    names=[Path(__file__).name,'PROOF.md#problem4-two-cover-p3-classification','PROOF.md#problem4-finite-independent-image-trap',
        'finite_independent_image_trap_audit.json','check_finite_independent_image_trap.py']
    report=dict(status='pass',uniform_state_range='n>=4',alphabet='arbitrary finite',complete_fixed_cover_graphs_through_n9=total,
        graph_stats=stats,complete_n4_ordered_binary_alphabets=tested,qualifying_synchronizing_controls=qualified,
        qualifying_strongly_connected_controls=strong,semantic_shape_histogram=hist,structural_examples=examples,
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Uniform necessary P3 graph classification under a two-state P5 cover. Full graph/semantic controls support the paper proof. No E6/E26 exclusion, F value or alphabet separation.')
    (ROOT/'two_cover_p3_classification_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','graph_stats','structural_examples')}),flush=True)
if __name__=='__main__':main()
