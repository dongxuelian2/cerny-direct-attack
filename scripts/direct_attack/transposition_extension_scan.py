"""Exact ternary transposition additions to slow sparse image families."""
from itertools import combinations
import json
from pathlib import Path
import time
from direct_attack.native_sparse_policy import profile


def main():
    root=Path('scripts/direct_attack/data/transposition_extension_scan');root.mkdir(exist_ok=True);records=[];started=time.monotonic()
    for n in [16,24,32]:
        for rank in [3,4,5]:
            if rank==3:
                L=n-1;base=[[(q+1)%L for q in range(L)]+[L],[L]*(L-1)+[L-2,0]]
            else:
                k=rank-1;base=[list(range(k))+list(range(k+1,n))+[k],list(range(1,k+1))+[1]*(n-k-1)+[0]]
            scores=[];best=(-1,-1);retained=[];rejected=0
            for q,r in combinations(range(n),2):
                c=list(range(n));c[q],c[r]=c[r],c[q];rows=base+[c];p=profile(rows,limit=20000)
                assert p is not None
                if p['truncated']:rejected+=1;scores.append([q,r,None]);continue
                value=(p['max_extension'],p['best_policy']);scores.append([q,r,*value,p['rt'],p['reachable']])
                if value>best:
                    best=value;p=profile(rows,True,limit=20000);p.update(transposition=[q,r],base_rank=rank)
                    name=f'n{n}_r{rank}_peak{len(retained):02d}.json';(root/name).write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8');retained.append(name)
            record=dict(n=n,rank=rank,scores=scores,best=best,records=retained,truncated_rejections=rejected)
            records.append(record);print(json.dumps(dict(n=n,rank=rank,best=best,retained=len(retained),rejected=rejected,seconds=time.monotonic()-started)),flush=True)
    (root/'summary.json').write_text(json.dumps(dict(records=records,seconds=time.monotonic()-started,
         boundary='All single transpositions of the three stated base families at n16/24/32; truncated graphs rejected. No coverage of arbitrary ternary DFAs.'),indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
