"""Replay every designated transposition score; independent all-source peak arrays."""
from itertools import combinations
import json
from pathlib import Path
import time
from direct_attack.native_sparse_policy import profile
from direct_attack.check_rank_three_search import verify


def main():
    root=Path('scripts/direct_attack/data/transposition_extension_scan');s=json.loads((root/'summary.json').read_text());records=[];started=time.monotonic();tested=0
    assert [(x['n'],x['rank']) for x in s['records']]==[(n,r) for n in [16,24,32] for r in [3,4,5]]
    for item in s['records']:
        n=item['n'];rank=item['rank'];L=n-1
        if rank==3:base=[[(q+1)%L for q in range(L)]+[L],[L]*(L-1)+[L-2,0]]
        else:
            k=rank-1;base=[list(range(k))+list(range(k+1,n))+[k],list(range(1,k+1))+[1]*(n-k-1)+[0]]
        assert [x[:2] for x in item['scores']]==[list(t) for t in combinations(range(n),2)]
        for score in item['scores']:
            q,r=score[:2];swap=list(range(n));swap[q],swap[r]=swap[r],swap[q];p=profile(base+[swap],limit=20000);assert p is not None
            actual=[q,r,None] if p['truncated'] else [q,r,p['max_extension'],p['best_policy'],p['rt'],p['reachable']]
            assert actual==score;tested+=1
        assert item['truncated_rejections']==0
        assert item['best']==list(max(tuple(x[2:4]) for x in item['scores']))
        for name in item['records']:
            c=json.loads((root/name).read_text());q,r=c['transposition'];swap=list(range(n));swap[q],swap[r]=swap[r],swap[q]
            assert c['rows']==base+[swap];v=verify(c,rank);v.update(file=name);records.append(v)
    report=dict(verified=True,tested=tested,records=records,seconds=time.monotonic()-started,
                boundary='All designated native scores replayed; all 21 retained arrays independently recomputed via ordinary all-source forward BFS. No arbitrary ternary coverage.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(tested=tested,independent_peak_arrays=len(records),seconds=report['seconds'])))


if __name__=='__main__':main()
