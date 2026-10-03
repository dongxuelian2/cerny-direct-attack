"""Independent ordinary reverse BFS, full image/parent arrays and unary controls."""
from collections import deque
import json
from pathlib import Path
import time
from direct_attack.ordinary_reverse_policy import profile
from direct_attack.audit_sparse_policy import ordinary_forward


def verify(c):
    rows=c['rows'];n=c['n'];j=c['j'];assert 4<=j<=n-3
    a=[1]*n;a[0]=a[j-1]=0;assert rows==[a,list(range(1,n))+[j]]
    Q=frozenset(range(n));mask=lambda T:sum(1<<q for q in T)
    def apply(T,w):
        for x in w:T=frozenset(rows[x][q] for q in T)
        return T
    suffix=lambda s:frozenset(range(s,n))
    pairs={frozenset([i,i+1]) for i in range(n-1)}|{frozenset([n-1,j])}
    R={suffix(s) for s in range(j+1)}|pairs|{frozenset([q]) for q in range(n)}
    p=profile(rows);assert p is not None
    assert set(p['best'])=={mask(T) for T in R} and len(R)==c['reachable']==2*n+j+1
    for key in ['extension','best','worst','forward']:assert c[key]=={str(T):v for T,v in p[key].items()}
    if n<=12:
        f=ordinary_forward(rows)
        for key in ['extension','best','worst','forward']:assert f[key]==p[key]
    # Explicit reachability, closure, strong connectivity, and unary nonsynchronization.
    for s in range(j+1):assert apply(Q,[1]*s)==suffix(s)
    assert {apply(Q,[0]+[1]*i) for i in range(n)}==pairs
    for T in R:
        for x in range(2):assert apply(T,[x]) in R
    for start in range(n):
        seen={start};queue=deque([start])
        while queue:
            q=queue.popleft()
            for row in rows:
                if row[q] not in seen:seen.add(row[q]);queue.append(row[q])
        assert len(seen)==n
    assert rows[0][0]==0 and rows[0][1]==1
    cycle=suffix(j);assert len(cycle)>=3 and apply(cycle,[1])==cycle and len(set(rows[1][q] for q in cycle))==len(cycle)
    assert c['known_reset_word']==[0,1,0] and apply(Q,c['known_reset_word'])==frozenset([1])
    for x in range(2):
        assert len(apply(Q,[x]))>1
        for y in range(2):assert len(apply(Q,[x,y]))>1
    boundary={}
    for T in R:
        if len(T)<=2:continue
        for x in range(2):
            U=apply(T,[x])
            if len(U)<=2:boundary.setdefault(U,set()).add((T,x))
    A0=frozenset([0,1]);one=frozenset([1])
    assert set(boundary)=={A0,one} and boundary[one]=={(suffix(j),0)}
    assert boundary[A0]=={(suffix(s),0) for s in range(j)}
    for s in range(1,j+1):
        parents={(T,x) for T in R if len(T)>len(suffix(s)) for x in range(2) if apply(T,[x])<=suffix(s)}
        assert parents=={(suffix(s-1),1)}
        assert p['extension'][mask(suffix(s))]==1 and p['best'][mask(suffix(s))]==p['worst'][mask(suffix(s))]==s
    for S in pairs:
        if S==A0:
            assert p['extension'][mask(S)]==p['best'][mask(S)]==1 and p['worst'][mask(S)]==j+1
        else:
            i=min(S);assert p['extension'][mask(S)]==i and p['best'][mask(S)]==p['worst'][mask(S)]==j+i
    merged=[(T,x) for T in R if len(T)>1 for x in range(2) if len(apply(T,[x]))==1]
    assert all(x==0 and apply(T,[x])==one for T,x in merged)
    assert max(map(lambda z:len(z[0]),merged))==n-j and {T for T,x in merged if len(T)==n-j}=={suffix(j)}
    assert c['policy_word']==[1]*j+[0] and apply(Q,c['policy_word'])==one
    assert c['rt']==min(p['forward'][1<<q] for q in range(n))==3
    assert c['best_policy']==min(p['best'][1<<q] for q in range(n))==j+1
    assert c['max_extension']==max(p['extension'].values())==n-1
    for q in range(n):
        assert p['extension'][1<<q]==(j if q==0 else q)
        assert p['best'][1<<q]==(2*j if q==0 else j+q)
        assert p['worst'][1<<q]==(2*j+n-2 if q==0 else j+n+q-2)
    return dict(n=n,j=j,P=j+1,rt=3,R=len(R),all_source_cross_check=n<=12)


def main():
    started=time.monotonic();root=Path('direct_attack/data/irreducible_short_reset');records=[]
    for r in json.loads((root/'summary.json').read_text())['records']:
        records.append(dict(file=r['file'],**verify(json.loads((root/r['file']).read_text()))))
    c=json.loads((root/'n12_j9.json').read_text());rejected=[]
    for key in ['j','policy_word','best']:
        d=json.loads(json.dumps(c))
        if key=='j':d[key]-=1
        elif key=='policy_word':d[key]=d[key][:-1]
        else:d[key]['2']-=1
        try:verify(d)
        except AssertionError:rejected.append(key)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,records=records,corruptions_rejected=rejected,seconds=time.monotonic()-started,
                scope='Every e/G/W/forward entry recomputed on ordinary actual-image graph by per-target reverse BFS; n<=12 also ordinary ALL-SOURCE BFS. Full image family, every suffix unit parent, rank-two boundary, SC, both unary nonsynchronization controls, optimal reset/policy words and corruption rejection. Arbitrary-n claims are paper proofs.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),all_source_cross_checks=sum(r['all_source_cross_check'] for r in records),corruptions_rejected=rejected,seconds=report['seconds'])),flush=True)


if __name__=='__main__':main()
