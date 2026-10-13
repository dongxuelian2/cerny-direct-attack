"""An unbounded maximum-seed penalty with rt=P=2 and F_kappa=n-2."""
import json
from pathlib import Path
from direct_attack.native_sparse_policy import profile


def construct(n):
    assert n>=6 and n%2==0;j=n-4
    a=[q%2 for q in range(n)];a[j+1]=0
    return [a,[(q+1)%n for q in range(n)],[0,0]+[(q-1)%3 for q in range(2,n)]]


def main():
    root=Path('scripts/direct_attack/data/maximum_seed_family');root.mkdir(exist_ok=True);records=[]
    for n in list(range(6,64,6))+[8,14,20]:
        rows=construct(n);c=profile(rows,True);metrics=profile(rows,seed_budget=True);assert c is not None and not c['truncated']
        j=n-4;T=sum(1<<q for q in [j,j+1,j+2]);c.update(seed_budget=metrics,large_seed=T,
            seed_reach_word=[2]+[1]*j,forced_seed_reset_word=[2]+[1]*j+[0],reset_word=[0,2],
            valid_parameter=n%6==0,scope='Paper family n=6h>=6 has P=rt=2 and F_kappa=n-2. n=6h+2 controls have an extra cheaply reached c-merged triple and F_kappa=2.')
        assert c['rt']==c['best_policy']==2 and c['reachable']==4*n+1
        if n%6==0:assert metrics['kappa']==3 and metrics['anchor_image']==T and metrics['anchor_best']==n-2 and c['best'][T]==n-3
        else:assert metrics['anchor_best']==2
        (root/f'n{n}.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8');records.append(dict(n=n,valid_parameter=n%6==0,P=2,Fk=metrics['anchor_best'],R=c['reachable']))
    (root/'summary.json').write_text(json.dumps(dict(records=records),indent=2)+'\n',encoding='utf-8');print(json.dumps(records))


if __name__=='__main__':main()
