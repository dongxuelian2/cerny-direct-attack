"""Independent retraction enumeration and unreachable-preimage diagnosis."""
from itertools import combinations,product
import json
from pathlib import Path
from direct_attack.permutation_units import partitions,representative
from direct_attack.ordinary_reverse_policy import profile
from direct_attack.audit_sparse_policy import ordinary_forward

ROOT=Path('scripts/direct_attack/data/idempotent_boundary')

def main():
    stored=json.loads((ROOT/'summary.json').read_text());cover=[]
    for n in range(2,6):
        tested=accepted=violations=0;maps=set()
        for k in range(1,n+1):
            for roots in combinations(range(n),k):
                others=[q for q in range(n) if q not in roots]
                for targets in product(roots,repeat=len(others)):
                    b=list(range(n))
                    for q,t in zip(others,targets):b[q]=t
                    assert all(b[b[q]]==b[q] for q in range(n));maps.add(tuple(b))
        for part in partitions(n):
            for b in maps:
                tested+=1;p=profile([representative(part),list(b)])
                if p is not None:
                    accepted+=1;violations+=int(max(p['extension'].values())>n-len(part)+1)
        r=dict(n=n,tested=tested,accepted=accepted,rejected=tested-accepted,violations=violations)
        expected=next(v for v in stored['cover'] if v['n']==n)
        assert all(r[k]==expected[k] for k in r);cover.append(r)
    for filename in ['mixed_counter.json','circular_counter.json']:
        c=json.loads((ROOT/filename).read_text());o=ordinary_forward(c['rows'])
        for key in ['extension','best','worst','forward']:assert c[key]=={str(S):v for S,v in o[key].items()}
    c=json.loads((ROOT/'circular_counter.json').read_text());rows=c['rows'];Q=frozenset(range(5));S=frozenset([3,4])
    distances={S:0};words={S:[]};queue=[S]
    for U in queue:
        if len(U)>2:continue
        for x,row in enumerate(rows):
            V=frozenset(q for q in Q if row[q] in U)
            if V not in distances:distances[V]=distances[U]+1;words[V]=words[U]+[x];queue.append(V)
    cost=min(v for T,v in distances.items() if len(T)>2)
    winners=[T for T in queue if len(T)>2 and distances[T]==cost]
    assert cost==5<c['extension']['24']==10
    mask=lambda T:sum(1<<q for q in T)
    assert all(str(mask(T)) not in c['forward'] for T in winners)
    assert frozenset([0,1,4]) in winners
    certificate=dict(target=24,unrestricted_preimage_cost=5,actual_image_cost=10,
                     unreachable_preimages=[dict(mask=mask(T),forward_word=list(reversed(words[T]))) for T in winners])
    mixed=json.loads((ROOT/'mixed_counter.json').read_text())
    assert mixed['extension']['18']==5 and mixed['best']['9']==4<mixed['forward']['9']==5
    assert mixed['worst']['1']==5>mixed['best']['1']==4
    report=dict(verified=True,cover=cover,all_source_witnesses=2,certificate=certificate,
                boundary='State minimum n5 in the binary permutation/idempotent class. All actual-capacity arrays checked. Full preimages at the earlier cost are explicitly unreachable; no unrestricted square refutation.')
    (ROOT/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)

if __name__=='__main__':main()
