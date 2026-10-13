"""Close duplicate-letter/unary cases omitted by combinations of distinct maps."""
from collections import Counter
import json
from pathlib import Path
from direct_attack.mine import maps
from direct_attack.core import graph,reverse,bfs
from direct_attack.partition_attack import partitions

def main():
    records=[]
    for n in range(2,6):
        counts=Counter(); parts=list(partitions(n))
        for row in maps(n):
            counts['maps']+=1; g=graph([row]); rev=reverse(g)
            if bfs(rev,[1<<q for q in range(n)])[-1]<0: continue
            counts['synchronizing_maps']+=1
            for part in parts:
                k=len(part)
                d=bfs(rev,[s for s in range(1,1<<n) if any(not s&b for b in part)])
                for s in range(1,1<<n):
                    m=s.bit_count()
                    if m<k: continue
                    counts['partition_subset_tests']+=1
                    assert 0<=d[s]<=(m-k+1)*(n-k+1),(n,row,part,s,d[s])
        records.append(dict(n=n,counters=dict(counts),rank_excess_violations=0,complete=True))
    Path('scripts/direct_attack/data/unary_partition_checks.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(records))

if __name__=='__main__': main()
