"""Independent full ordinary arrays, complete rank boundary and short-policy words."""
from collections import deque
import json
from pathlib import Path
import time
from direct_attack.audit_sparse_policy import ordinary_forward


def verify(c,family=False):
    rows=c['rows'];n=c['n'];Q=frozenset(range(n));mask=lambda T:sum(1<<q for q in T)
    def apply(T,w):
        for x in w:T=frozenset(rows[x][q] for q in T)
        return T
    assert rows[1]==[(q+1)%n for q in range(n)] and rows[0][:3]==[0,1,1]
    assert set(rows[0])=={0,1} and all(row[:2]==[0,1] for i,row in enumerate(rows) if i!=1)
    p=ordinary_forward(rows)
    for key in ['extension','best','worst','forward']:assert c[key]=={str(T):v for T,v in p[key].items()}
    assert apply(Q,c['known_reset_word'])==frozenset([1]) and len(c['known_reset_word'])==3
    for x in range(len(rows)):
        assert len(apply(Q,[x]))>1
        for y in range(len(rows)):assert len(apply(Q,[x,y]))>1
    assert c['rt']==min(p['forward'][1<<q] for q in Q)==3 and c['best_policy']==min(p['best'][1<<q] for q in Q)
    if family:
        a=[int(q%4 in [1,2]) for q in range(n)];b=[(q+1)%n for q in Q];r=[q%2 for q in Q]
        if c['flipped']:r[-2]=1
        r[-1]=2;assert rows==[a,b,r]
        A=lambda i:frozenset([i%n,(i+1)%n]);B=lambda i:frozenset([i%n,(i+2)%n]);C=lambda i:frozenset([i%n,(i+1)%n,(i+2)%n])
        R={Q}|{frozenset([q]) for q in Q}|{A(q) for q in Q}|{B(q) for q in Q}|{C(q) for q in Q}
        assert {mask(T) for T in R}==set(p['best']) and len(R)==c['reachable']==(15 if n==4 else 4*n+1)
        for T in R:
            for x in range(3):assert apply(T,[x]) in R
        assert apply(Q,c['critical_reach_word'])==C(n-3) and len(c['critical_reach_word'])==n-2
        boundary={};parents={}
        for T in R:
            if len(T)<=2:continue
            for x in range(3):
                U=apply(T,[x])
                if len(U)<=2:boundary.setdefault(U,set()).add(T);parents.setdefault(U,[]).append((T,x))
        if c['flipped'] and n%2==0:
            assert set(boundary)=={A(0),A(1)} and boundary[A(1)]=={C(n-3)}
            assert parents[A(1)]==[(C(n-3),2)] and p['best'][mask(C(n-3))]==p['extension'][mask(C(n-3))]==n-2
            for T in R:
                if len(T)==2 and T!=A(0):assert p['best'][mask(T)]==p['worst'][mask(T)]==p['extension'][mask(T)]+n-2
            merged=[T for T in R if len(T)>=2 and any(len(apply(T,[x]))==1 for x in range(3))]
            assert max(map(len,merged))==2 and all(T!=A(0) and p['best'][mask(T)]>=n-1 for T in merged)
            assert c['best_policy']==n and max(p['extension'].values())==n-1
            word=c['policy_word'];assert len(word)==n and apply(Q,word)==frozenset([1])
            assert word==c['critical_reach_word']+[2,0]
        else:
            assert c['best_policy']==3 and p['extension'][mask(A(1))]==p['best'][mask(A(1))]==2
    return dict(n=n,P=c['best_policy'],rt=3,R=c['reachable'],family=family)


def main():
    started=time.monotonic();records=[];root=Path('direct_attack/data/short_reset_family');summary=json.loads((root/'summary.json').read_text())
    for r in summary['records']:records.append(dict(file=str(root/r['file']),**verify(json.loads((root/r['file']).read_text()),True)))
    for folder in sorted(Path('direct_attack/data').glob('short_reset_policy_n*')):
        s=json.loads((folder/'summary.json').read_text())
        for name in s['records']:records.append(dict(file=str(folder/name),**verify(json.loads((folder/name).read_text()))))
    for n in range(6,64,2):
        x=json.loads((root/f'n{n}_penalty.json').read_text());y=json.loads((root/f'n{n}_control.json').read_text())
        differences=[(i,q) for i in range(3) for q in range(n) if x['rows'][i][q]!=y['rows'][i][q]]
        assert differences==[(2,n-2)] and x['best'].keys()==y['best'].keys()
    c=json.loads((root/'n12_penalty.json').read_text());rejected=[]
    for key in ['best','critical_reach_word','policy_word']:
        d=json.loads(json.dumps(c))
        if key=='best':d[key]['6']-=1
        else:d[key]=d[key][:-1]
        try:verify(d,True)
        except AssertionError:rejected.append(key)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,records=records,corruptions_rejected=rejected,seconds=time.monotonic()-started,
                scope='Every saved e/G/W/forward entry independently recomputed by ordinary ALL-SOURCE BFS. Full closed family, unique winning rank-two boundary parent, critical transport, actual reset/policy words and same-R one-transition controls checked. Universal claims are paper proofs.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(records),corruptions_rejected=rejected,seconds=report['seconds'])),flush=True)


if __name__=='__main__':main()
