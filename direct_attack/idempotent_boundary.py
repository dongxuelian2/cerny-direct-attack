"""Complete binary permutation/idempotent cover n2..5, two exact boundaries."""
from itertools import product
import hashlib
import json
from pathlib import Path
from direct_attack.permutation_units import partitions,representative
from direct_attack.native_sparse_policy import profile
from direct_attack.ordinary_reverse_policy import profile as independent
from direct_attack.audit_sparse_policy import ordinary_forward

ROOT=Path('direct_attack/data/idempotent_boundary')

def main():
    ROOT.mkdir(exist_ok=True);summary=[];witnesses=[];ordinary_count=0
    for n in range(2,6):
        tested=accepted=violations=0;first=None;digest=hashlib.sha256()
        for part in partitions(n):
            for b in product(range(n),repeat=n):
                if not all(b[b[q]]==b[q] for q in range(n)):continue
                rows=[representative(part),list(b)];tested+=1;p=profile(rows,True);o=independent(rows)
                assert (p is None)==(o is None)
                if p is not None:
                    accepted+=1;ordinary_count+=1
                    for key in ['extension','best','worst','forward']:assert p[key]==o[key]
                    if p['max_extension']>n-len(part)+1:
                        violations+=1
                        if first is None:first=dict(parts=part,bound=n-len(part)+1,witness=p)
                digest.update(json.dumps([rows,p],sort_keys=True,separators=(',',':')).encode())
        r=dict(n=n,tested=tested,accepted=accepted,rejected=tested-accepted,violations=violations,sha256=digest.hexdigest())
        summary.append(r)
        if first is not None:witnesses.append(first)
        print(json.dumps(r),flush=True)
    rows=[[0,0,2,2,4],[1,2,3,4,0]];p=profile(rows,True)
    assert p['max_extension']==10 and p['extension'][24]==10 and rows[0]==[rows[0][q] for q in rows[0]]
    for key,value in ordinary_forward(rows).items():assert p[key]==value
    witnesses.append(dict(parts=[5],bound=5,witness=p,note='Letter order is idempotent then cycle; target {3,4}.'))
    for i,c in enumerate(witnesses):
        p=c['witness'];assert p['max_extension']>c['bound']
        for key,value in ordinary_forward(p['rows']).items():assert p[key]==value
        (ROOT/('mixed_counter.json' if i==0 else 'circular_counter.json')).write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
    (ROOT/'witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n',encoding='utf-8')
    result=dict(cover=summary,ordinary_all_arrays=ordinary_count,all_source_witnesses=len(witnesses),verified=True,
                scope='All permutation cycle types times ALL idempotent maps n2..5, including identity/constant controls. The n5 minimum is within binary permutation/idempotent DFAs, not arbitrary larger alphabets. Every accepted array has ordinary reverse BFS; witnesses also ALL-SOURCE.')
    (ROOT/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
