"""Exact rank-three family suggested by the n12 extension search."""
import argparse
import json
from pathlib import Path
from direct_attack.native_sparse_policy import profile


def construct(n):
    assert n>=4
    return [[0,1]+[2+(q-1)%(n-2) for q in range(2,n)], [1,2]+[1]*(n-3)+[0]]


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--max-n',type=int,default=63);args=ap.parse_args();assert 4<=args.max_n<=63
    out=Path('scripts/direct_attack/data/three_image_family');out.mkdir(parents=True,exist_ok=True);records=[]
    for n in range(4,args.max_n+1):
        rows=construct(n);p=profile(rows,True);assert p is not None and not p['truncated']
        S=1|(1<<(n-1));L=n-2
        word=[1]+[0]*(L-1)+[1]+[0]*(L-1)
        reset=[1,1]+[0]*(L-1)+[1,1]
        assert p['extension'][S]==p['max_extension']==2*n-4 and p['rt']==p['best_policy']==n+1
        assert p['reachable']==4*n-4
        p.update(target=S,extension_word=word,larger_image=7,reset_word=reset,
                 ordinary_extension=4 if n==4 else n-1,
                 ordinary_preimage_word=[1,1]+[0]*(L-1),ordinary_preimage=[0]+list(range(2,n-1)),
                 ordinary_extension_word=[1,0,1,0] if n==4 else [1,1]+[0]*(L-1),
                 scope='Paper parameter theorem: exact all-image maximum 2n-4 and rt=P=n+1; finite full arrays independently checked.')
        (out/f'n{n}.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
        records.append(dict(n=n,max_extension=p['max_extension'],rt=p['rt'],best_policy=p['best_policy'],reachable=p['reachable']))
    (out/'summary.json').write_text(json.dumps(dict(max_n=args.max_n,records=records),indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(records),max_n=args.max_n,verified=True)))


if __name__=='__main__':main()
