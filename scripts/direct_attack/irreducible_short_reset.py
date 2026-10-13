"""Binary irreducibly synchronizing family: rt=3, P=j+1, 4<=j<=n-3."""
import json
from pathlib import Path
from direct_attack.native_sparse_policy import profile


def construct(n,j):
    assert 4<=j<=n-3
    a=[1]*n;a[0]=a[j-1]=0
    return [a,list(range(1,n))+[j]]


def main():
    root=Path('scripts/direct_attack/data/irreducible_short_reset');root.mkdir(exist_ok=True);records=[]
    for n in range(7,64):
        for j in sorted({4,n//2,n-3}):
            if not 4<=j<=n-3:continue
            c=profile(construct(n,j),True);assert c is not None and not c['truncated']
            c.update(j=j,known_reset_word=[0,1,0],policy_word=[1]*j+[0],
                     scope='Paper theorem for all n>=7 and 4<=j<=n-3; deleting either letter loses synchronization.')
            assert c['rt']==3 and c['best_policy']==j+1 and c['reachable']==2*n+j+1 and c['max_extension']==n-1
            name=f'n{n}_j{j}.json';(root/name).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
            records.append(dict(file=name,n=n,j=j,rt=3,P=j+1,R=2*n+j+1))
    (root/'summary.json').write_text(json.dumps(dict(records=records),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),maximum_n=63,verified_native_formulas=True)),flush=True)


if __name__=='__main__':main()
