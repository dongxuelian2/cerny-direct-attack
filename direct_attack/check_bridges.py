"""Independent certificate verification by ordinary sets; no search imports."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path

def verify(c):
    assert c['schema']=='direct_attack.partition-distance.v1'
    n,rows,part=c['n'],c['rows'],c['partition']
    assert n>=2 and all(len(r)==n and all(0<=v<n for v in r) for r in rows)
    blocks=[frozenset(q for q in range(n) if b>>q&1) for b in part]
    assert all(blocks) and set.union(*(set(b) for b in blocks))==set(range(n))
    assert sum(len(b) for b in blocks)==n
    states={s:frozenset(q for q in range(n) if s>>q&1) for s in c['states']}
    assert len(states)==len(c['states'])
    expected={frozenset(s) for k in range(1,c['maximum_subset_size']+1) for s in combinations(range(n),k)}
    assert set(states.values())==expected
    assert len(c['potential'])==len(states)
    d={states[s]:v for s,v in zip(c['states'],c['potential'])}
    assert all(type(v) is int and v>=0 for v in d.values())
    def goal(s): return any(not s&b for b in blocks)
    def image(s,row): return frozenset(row[q] for q in s)
    for s,v in d.items():
        if goal(s): assert v==0
        else:
            assert v==1+min(d[image(s,row)] for row in rows)
        for row in rows: assert v<=1+d[image(s,row)]
    s=states[c['start']]
    initial=s
    for a in c['word']:
        assert type(a) is int and 0<=a<len(rows)
        s=image(s,rows[a])
    assert goal(s) and len(c['word'])==c['exact_distance']==d[initial]
    transform=list(range(n))
    for a in c['kernel_word']: transform=[rows[a][q] for q in transform]
    assert transform==c['kernel_transform']
    fibers={frozenset(q for q in range(n) if transform[q]==r) for r in set(transform)}
    assert fibers==set(blocks)
    reached=frozenset(range(n))
    for a in c['reach_word']: reached=image(reached,rows[a])
    assert reached==initial
    assert c['paper_lower_bound']<=c['exact_distance']
    return dict(n=n,exact_distance=c['exact_distance'],vertices=len(d),verified=True)

def main():
    root=Path('direct_attack/data/bridge_obstruction')
    results=[]
    for path in sorted(root.glob('C*.json')):
        c=json.loads(path.read_text())
        results.append(dict(file=str(path),**verify(c)))
    # Deliberately corrupt the dangerous fields: all must be rejected.
    c=json.loads((root/'C12_balanced.json').read_text())
    broken=deepcopy(c)
    broken['potential'][broken['states'].index(broken['start'])]+=1
    try: verify(broken)
    except AssertionError: pass
    else: raise AssertionError('mutated potential accepted')
    broken=deepcopy(c)
    broken['kernel_transform'][0]=(broken['kernel_transform'][0]+1)%broken['n']
    try: verify(broken)
    except AssertionError: pass
    else: raise AssertionError('mutated kernel accepted')
    broken=deepcopy(c)
    broken['word']=broken['word'][:-1]
    try: verify(broken)
    except AssertionError: pass
    else: raise AssertionError('truncated witness accepted')
    broken=deepcopy(c)
    broken['reach_word']=[]
    try: verify(broken)
    except AssertionError: pass
    else: raise AssertionError('empty reach witness accepted')
    report=dict(certificates=len(results),vertices=sum(r['vertices'] for r in results),
                mutation_rejections=4,reports=results)
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='reports'}))

if __name__=='__main__': main()
