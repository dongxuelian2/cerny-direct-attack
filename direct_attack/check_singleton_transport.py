"""Independent word/target-distance audit of the state-edge policy obstruction."""
from collections import deque
import json
from pathlib import Path
from direct_attack.check_image_policy import verify


def main():
    path=Path('direct_attack/data/singleton_transport/witness.json');c=json.loads(path.read_text());verify(c)
    rows=c['rows'];n=c['n'];Q=frozenset(range(n));edge=c['edge_obstruction']
    q,z,a=edge['source'],edge['target'],edge['letter'];assert rows[a][q]==z
    def apply(w):
        X=Q
        for letter in w:X=frozenset(rows[letter][p] for p in X)
        return X
    w=edge['source_policy_word'];v=edge['shorter_reset_to_target']
    assert apply(w)==frozenset([q]) and apply(v)==frozenset([z]) and v==w+[a]
    assert len(w)==edge['source_cost']==c['best'][str(1<<q)]
    assert len(v)<edge['target_cost']==c['best'][str(1<<z)]
    queue=deque([Q]);d={Q:0}
    while queue:
        X=queue.popleft()
        for row in rows:
            Y=frozenset(row[p] for p in X)
            if Y not in d:d[Y]=d[X]+1;queue.append(Y)
    assert d[frozenset([z])]==len(v)==3
    report=dict(n=n,source=q,target=z,source_policy=len(w),target_policy=edge['target_cost'],
                target_reset_distance=d[frozenset([z])],verified=True)
    Path('direct_attack/data/singleton_transport_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
