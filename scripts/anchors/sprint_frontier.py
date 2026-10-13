"""Historical frontier BFS; ordinary finite evidence, now covered by proof."""
import argparse
import json
import time
from pathlib import Path
from dense_quotient import solve_dense


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--min-r',type=int,default=18)
    p.add_argument('--max-r',type=int,default=23)
    p.add_argument('--m',type=int,default=2)
    args=p.parse_args()
    rows=[]
    for r in range(args.min_r,args.max_r+1):
        start=time.monotonic()
        d=solve_dense(r,args.m)
        N=1<<r
        value=d[(args.m+1)*N-1]
        L=(r-1).bit_length()-1
        expected=3*(r+args.m)+L*r-(1<<(L+1))-3
        row=dict(r=r,m=args.m,B=value,expected=expected,
                 states=len(d)-1,seconds=round(time.monotonic()-start,3))
        rows.append(row)
        print(row,flush=True)
        del d
    out=Path('scripts/anchors/sprint_results')
    out.mkdir(exist_ok=True)
    (out/f'frontier_m{args.m}_r{args.min_r}_{args.max_r}.json').write_text(
        json.dumps(rows,indent=2)+'\n',encoding='utf-8',newline='\n')


if __name__=='__main__':
    main()
