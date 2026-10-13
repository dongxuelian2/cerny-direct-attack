"""Complete SC binary unit-letter normal forms and exact finite policy tests."""
from math import gcd
import json
from pathlib import Path
from direct_attack.native_sparse_policy import profile


def construct(n,j,h):
    assert 1<=h<n and 0<=j<=h
    b=list(range(n));b[h]=0
    return [list(range(1,n))+[j],b]


def reset_word(n,j,h):
    assert gcd(n-j,h)==1
    if j==0:return ([1]+[0]*h)*(n-2)+[1]
    return [0]*j+([1]+[0]*h)*(n-j-1)


def main():
    root=Path('scripts/direct_attack/data/unit_tail_family');root.mkdir(exist_ok=True);records=[]
    for n in range(2,13):
        for h in range(1,n):
            for j in range(h+1):
                rows=construct(n,j,h);p=profile(rows,True);sync=gcd(n-j,h)==1
                assert (p is not None)==sync
                c=p if sync else dict(n=n,rows=rows)
                c.update(j=j,h=h,synchronizing=sync)
                if sync:
                    c['reset_word']=reset_word(n,j,h)
                    assert p['rt']<=len(c['reset_word'])<=(n-1)**2
                    assert p['best_policy']==p['rt'] and p['max_extension']<=n
                name=f'n{n}_j{j}_h{h}.json';(root/name).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
                records.append(dict(file=name,n=n,j=j,h=h,synchronizing=sync))
    (root/'summary.json').write_text(json.dumps(dict(records=records),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),sync=sum(r['synchronizing'] for r in records),max_n=12)),flush=True)


if __name__=='__main__':main()
