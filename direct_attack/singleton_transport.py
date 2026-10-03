"""Attack the directed state-edge Lipschitz condition for singleton policies."""
from collections import deque
import json
from pathlib import Path
from direct_attack.core import graph,strongly_connected
from direct_attack.mine import inputs
from direct_attack.native_policy import profile
from direct_attack.image_extension_policy import profile as certificate
from direct_attack.check_image_policy import verify


def policy_word(rows,start,c):
    n=len(rows[0]);Q=(1<<n)-1;g=graph(rows);best={int(s):v for s,v in c['best'].items()}
    e={int(s):v for s,v in c['extension'].items()};S=1<<start;word=[]
    while S!=Q:
        for T in sorted(best):
            if T.bit_count()<=S.bit_count() or best[T]+e[S]!=best[S]:continue
            queue=deque([T]);ws={T:[]};found=None
            while queue:
                X=queue.popleft();w=ws[X]
                if X & S==X:found=w;break
                if len(w)==e[S]:continue
                for a,Y in enumerate(g[X]):
                    if Y not in ws:ws[Y]=w+[a];queue.append(Y)
            if found is not None:
                assert len(found)==e[S];word=found+word;S=T;break
        else:raise AssertionError('No optimal shortest extension target')
    assert len(word)==best[1<<start];X=Q
    for a in word:X=g[X][a]
    assert X==1<<start
    return word


def main():
    out=Path('direct_attack/data/singleton_transport');out.mkdir(exist_ok=True);counts={}
    for n in range(2,7):
        tested=sync=0
        for rows in inputs(n,'first-map-orbits',0,0,2):
            tested+=1
            if not strongly_connected(rows):continue
            p=profile(rows,details=True)
            if p is None:continue
            sync+=1
            failures=[(q,z,a) for a,row in enumerate(rows) for q,z in enumerate(row)
                      if p['best'][1<<z]>p['best'][1<<q]+1]
            if not failures:continue
            q,z,a=failures[0];c=json.loads(json.dumps(certificate(rows)));verify(c)
            word=policy_word(rows,q,c);transported=word+[a];X=(1<<n)-1;g=graph(rows)
            for letter in transported:X=g[X][letter]
            assert X==1<<z and len(transported)<p['best'][1<<z]
            c['edge_obstruction']=dict(source=q,target=z,letter=a,source_cost=p['best'][1<<q],
                                       target_cost=p['best'][1<<z],source_policy_word=word,
                                       shorter_reset_to_target=transported)
            (out/'witness.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
            counts[n]=dict(tested=tested,synchronizing_sc=sync,completed=False)
            report=dict(counts=counts,first_n=n,status='REFUTED',
                        proposed='G({q a})<=G({q})+1 for every state-edge',
                        scope='Binary-minimal within SC synchronization; higher-n cover stops on first refutation.')
            (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(c['edge_obstruction']));print(json.dumps(report));return
        counts[n]=dict(tested=tested,synchronizing_sc=sync,completed=True)
        print(json.dumps(dict(n=n,**counts[n])),flush=True)
    raise RuntimeError('No obstruction through the declared cover')


if __name__=='__main__':main()
