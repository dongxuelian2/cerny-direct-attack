"""Refute union cost transfer even with every nonempty image reachable."""
from collections import deque
from itertools import product
import json
from pathlib import Path
from direct_attack.native_complete_policy import profile as native
from direct_attack.image_extension_policy import profile as certificate


def first_growth(rows,S):
    queue=deque([S]);words={S:[]};k=S.bit_count()
    while queue:
        X=queue.popleft()
        if X.bit_count()>k:return X,list(reversed(words[X]))
        for a,row in enumerate(rows):
            Y=sum(1<<q for q,z in enumerate(row) if X>>z&1)
            if Y not in words:words[Y]=words[X]+[a];queue.append(Y)
    raise AssertionError('No extension')


def main():
    out=Path('scripts/direct_attack/data/complete_union_obstruction');out.mkdir(parents=True,exist_ok=True)
    runs=[]
    for n in [2,3,4]:
        tested=complete=0;failure=None
        for a in product(range(n),repeat=n):
            rows=[list(a),[(q+1)%n for q in range(n)]];tested+=1;p=native(rows,True)
            if p is None:continue
            complete+=1
            for S in range(1,(1<<n)-1):
                for T in range(S+1,(1<<n)-1):
                    U=S|T
                    if U==(1<<n)-1:continue
                    if p['extension'][U]<min(p['extension'][S],p['extension'][T]):
                        target,word=first_growth(rows,U)
                        failure=dict(n=n,S=S,T=T,U=U,target=target,word=word,
                                     costs={str(X):p['extension'][X] for X in [S,T,U]})
                        c=certificate(rows);assert c['extension']==p['extension']
                        (out/'witness.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
                        break
                if failure:break
            if failure:break
        runs.append(dict(n=n,tested=tested,completely_reachable=complete,failure=failure,
                         scan_complete=failure is None,scope='All second maps with a fixed full-cycle first structure; n4 stops at first failure.'))
    assert runs[-1]['failure'] is not None
    (out/'summary.json').write_text(json.dumps(dict(runs=runs),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(runs))


if __name__=='__main__':main()
