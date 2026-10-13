"""Ordinary-set checks for a completely reachable union-cost obstruction."""
from collections import deque
import json
from pathlib import Path
from direct_attack.check_image_policy import verify


def main():
    root=Path('scripts/direct_attack/data/complete_union_obstruction')
    c=json.loads((root/'witness.json').read_text());verify(c);rows=c['rows'];n=len(rows[0]);Q=frozenset(range(n))
    queue=deque([Q]);reach={Q:[]}
    while queue:
        X=queue.popleft()
        for a,row in enumerate(rows):
            Y=frozenset(row[q] for q in X)
            if Y not in reach:reach[Y]=reach[X]+[a];queue.append(Y)
    assert len(reach)==(1<<n)-1
    f=json.loads((root/'summary.json').read_text())['runs'][-1]['failure']
    sets={name:frozenset(q for q in range(n) if f[name]>>q&1) for name in ['S','T','U','target']}
    assert sets['S']|sets['T']==sets['U'] and sets['U']!=Q
    records={}
    for name in ['S','T','U']:
        start=sets[name];queue=deque([start]);distance={start:0}
        while queue:
            X=queue.popleft()
            if len(X)>len(start):cost=distance[X];break
            for row in rows:
                Y=frozenset(q for q,z in enumerate(row) if z in X)
                if Y not in distance:distance[Y]=distance[X]+1;queue.append(Y)
        else:raise AssertionError('No growth')
        assert cost==f['costs'][str(f[name])]==c['extension'][str(f[name])]
        records[name]=dict(set=sorted(start),cost=cost,examined_vertices=len(distance))
    def forward(X,w):
        for a in w:X=frozenset(rows[a][q] for q in X)
        return X
    def pre(X,w):
        for a in reversed(w):X=frozenset(q for q,z in enumerate(rows[a]) if z in X)
        return X
    word=f['word'];assert len(word)==records['U']['cost']
    assert pre(sets['U'],word)==sets['target']==Q
    assert forward(Q,word)<sets['U']
    assert all(len(pre(sets[name],word))<=len(sets[name]) for name in ['S','T'])
    assert records['U']['cost']<min(records['S']['cost'],records['T']['cost'])
    report=dict(verified=True,records=records,word=word,word_image=sorted(forward(Q,word)),
                complete_reach_words=[dict(set=sorted(X),word=w) for X,w in sorted(reach.items(),key=lambda t:(len(t[0]),sorted(t[0])))],
                modular_capacity=True,boundary='Complete reachability implies rho(X)=|X|. State minimum n4 is proved on paper over arbitrary alphabets; this scan is only a fixed-cycle binary search.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='complete_reach_words'}))


if __name__=='__main__':main()
