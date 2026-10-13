"""Probe the structured five-state local rank-potential obstruction."""
import json
from pathlib import Path
from direct_attack.core import bfs,graph
from direct_attack.native_policy import profile


def main():
    out=Path('scripts/direct_attack/data/local_rank_family');out.mkdir(parents=True,exist_ok=True);records=[]
    for n in range(5,13):
        a=[0]+list(range(2,n))+[1];b=list(range(n));b[0]=1;b[1]=0;b[2]=0;b[3]=4;b[4]=3
        rows=[a,b];p=profile(rows,details=True);assert p is not None
        S=((1<<n)-1)^3;g=graph(rows);f=bfs(g,[(1<<n)-1])
        D=min(d for t,d in enumerate(f) if d>=0 and t & S==t)
        reach=[1,0,0,1]+[0]*(n-2)+[1]+[0]*(n-2)
        current=(1<<n)-1
        for x in reach:current=g[current][x]
        assert current==S
        E=[1,1]+([0,1,1]*(n-3));reset=E+[0,0,1]+E;current=(1<<n)-1
        for x in reset:current=g[current][x]
        assert current.bit_count()==1
        record=dict(n=n,rows=rows,start=S,exact_extension=p['extension'][S],
                    exact_policy=p['best'][S],exact_avoiding=D,reach_word=reach,
                    reset_word=reset,rt=p['rt'],best_policy=p['best_policy'],
                    local_excess=p['local_excess'],local_start=p['local_start'])
        (out/f'n{n}.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        records.append({k:v for k,v in record.items() if k not in ['rows','reach_word','reset_word']})
        print(json.dumps(records[-1]),flush=True)
    (out/'summary.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
