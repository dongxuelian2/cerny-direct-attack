"""Exact probe of fixed-arm extensions of the n5/n6 potential obstructions."""
from math import lcm
import json
from pathlib import Path
from direct_attack.core import bfs,graph
from direct_attack.native_policy import profile


def main():
    out=Path('direct_attack/data/fixed_arm_family');out.mkdir(parents=True,exist_ok=True);records=[]
    for n in range(5,13):
        t=n-4;a=list(range(n));b=list(range(n))
        for q in range(t,n):a[q]=t+(q-t+1)%4
        for q in range(t+1):b[q]=(q+1)%(t+1)
        b[t+1]=0;b[t+2]=t+3;b[t+3]=t+2
        rows=[a,b];p=profile(rows,details=True);assert p is not None
        S=sum(1<<q for q in range(t+1,n));g=graph(rows);f=bfs(g,[(1<<n)-1])
        D=min(d for s,d in enumerate(f) if d>=0 and s & S==s)
        L=lcm(t+1,2);E=[1]*L+([0]+[1]*L)*2;reset=E+([0,0,1]+E)*t
        current=(1<<n)-1
        for x in reset:current=g[current][x]
        assert current==1<<t
        record=dict(n=n,rows=rows,start=S,exact_extension=p['extension'][S],
                    exact_policy=p['best'][S],exact_avoiding=D,proposed_bound=n*(n-3),
                    policy_excess=p['best'][S]-n*(n-3),reset_word=reset,
                    rt=p['rt'],best_policy=p['best_policy'],local_excess=p['local_excess'],local_start=p['local_start'])
        (out/f'n{n}.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        records.append({k:v for k,v in record.items() if k not in ['rows','reset_word']})
        print(json.dumps(records[-1]),flush=True)
    (out/'summary.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
