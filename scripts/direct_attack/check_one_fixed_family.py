"""Independent ordinary-set all-source checks of the one-fixed-point family."""
from collections import deque
import json
from pathlib import Path
import time
from direct_attack.audit_sparse_policy import ordinary_forward


def verify(c):
    n=c['n'];L=n-1;f=L;rows=c['rows'];Q=frozenset(range(n))
    assert rows==[[(q+1)%L for q in range(L)]+[L],[L]*(L-1)+[L-2,0]]
    def apply(S,w):
        for a in w:S=frozenset(rows[a][q] for q in S)
        return S
    R={Q}|{frozenset([q]) for q in Q}
    for j in range(L):R|={frozenset([f,j]),frozenset([j,(j-2)%L]),frozenset([f,j,(j-2)%L])}
    reach={Q};queue=deque([Q])
    while queue:
        T=queue.popleft()
        for a in range(2):
            U=apply(T,[a]);assert U in R
            if U not in reach:reach.add(U);queue.append(U)
    assert reach==R
    if n>=6:assert len(R)==4*n-2
    P=frozenset([f,0,L-2]);S=frozenset([L-3,L-1])
    assert c['larger_image']==sum(1<<q for q in P) and c['target']==sum(1<<q for q in S)
    assert apply(P,c['extension_word'])==S and len(c['extension_word'])==2*L
    assert apply(Q,c['reset_word'])==frozenset([f]) and len(c['reset_word'])==n+2
    p=ordinary_forward(rows)
    for key in ['extension','best','worst','forward']:assert c[key]=={str(T):v for T,v in p[key].items()}
    assert c['reachable']==len(R) and c['max_extension']==max(p['extension'].values())
    assert c['rt']==min(p['forward'][1<<q] for q in Q)==n+2
    assert c['best_policy']==min(p['best'][1<<q] for q in Q)==n+2
    if n>=6:assert p['extension'][c['target']]==c['max_extension']==2*L
    else:assert c['max_extension']==6
    return dict(n=n,images=len(R),max_extension=c['max_extension'],rt=c['rt'],all_entries_checked=True)


def main():
    root=Path('scripts/direct_attack/data/one_fixed_family');started=time.monotonic()
    records=[verify(json.loads(p.read_text())) for p in sorted(root.glob('n*.json'),key=lambda p:int(p.stem[1:]))]
    scan=json.loads(Path('scripts/direct_attack/data/one_fixed_three_image_scan.json').read_text());parameters=0
    for item in scan:
        n=item['n'];L=n-1
        assert [x[0] for x in item['values']]==list(range(1,L))
        for r,e,P,rt,M in item['values']:
            a=ordinary_forward([[(q+1)%L for q in range(L)]+[L],[L]*(L-1)+[r,0]])
            assert e==max(a['extension'].values()) and P==min(a['best'][1<<q] for q in range(n))
            assert rt==min(a['forward'][1<<q] for q in range(n)) and M==len(a['forward']);parameters+=1
    c=json.loads((root/'n8.json').read_text());rejected=[]
    for field in ['extension_word','rt','target']:
        d=json.loads(json.dumps(c))
        if field=='extension_word':d[field]=d[field][:-1]
        else:d[field]+=1
        try:verify(d)
        except AssertionError:rejected.append(field)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,records=records,scan_parameters_checked=parameters,corruptions_rejected=rejected,
                seconds=time.monotonic()-started,boundary='Every saved family entry and every scan summary independently checked. Arbitrary-n theorem is the paper proof; n5 is excluded.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),scan_parameters=parameters,corruptions_rejected=rejected,seconds=report['seconds'])))


if __name__=='__main__':main()
