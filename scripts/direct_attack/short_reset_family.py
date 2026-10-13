"""Exact global image-policy penalty P=n despite rt=3, with transition controls."""
import json
from pathlib import Path
from direct_attack.native_sparse_policy import profile


def construct(n,flipped=True):
    a=[int(q%4 in [1,2]) for q in range(n)];b=[(q+1)%n for q in range(n)];c=[q%2 for q in range(n)]
    if flipped:c[-2]=1
    c[-1]=2
    return [a,b,c]


def main():
    root=Path('scripts/direct_attack/data/short_reset_family');root.mkdir(exist_ok=True);records=[]
    parameters=[(n,flipped) for n in range(6,64,2) for flipped in [True,False]]+[(n,True) for n in [4,5,7,9,11]]
    for n,flipped in parameters:
        rows=construct(n,flipped);c=profile(rows,True);assert c is not None and not c['truncated']
        c.update(flipped=flipped,known_reset_word=[0,1,0],critical_triple=sum(1<<q for q in [n-3,n-2,n-1]),
                 critical_reach_word=[2]+[1]*(n-3),scope='Paper theorem even n>=6: P=n, rt=3, max e=n-1. Single-transition controls have P=3 and identical full R. Odd parameters have P=3; n4 is a separate finite boundary.')
        expected=n if flipped and n%2==0 else 3
        assert c['best_policy']==expected and c['rt']==3 and c['reachable']==(15 if n==4 else 4*n+1)
        if flipped and n%2==0:
            c['policy_word']=[2]+[1]*(n-3)+[2,0]
            assert max(c['extension'].values())==n-1 and c['best'][c['critical_triple']]==n-2
        name=f'n{n}_'+('penalty' if flipped else 'control')+'.json';(root/name).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
        records.append(dict(file=name,n=n,flipped=flipped,P=expected,rt=3,R=c['reachable']))
    (root/'summary.json').write_text(json.dumps(dict(records=records),indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(records),records=records)),flush=True)


if __name__=='__main__':main()
