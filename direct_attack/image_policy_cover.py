"""Complete binary image-policy check with a certified cardinality-sum shortcut."""
import argparse
from collections import Counter
import json
from pathlib import Path
import time
from direct_attack.core import strongly_connected
from direct_attack.image_extension import profile as extension_profile
from direct_attack.image_extension_policy import profile as policy_profile
from direct_attack.mine import inputs


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,default=6)
    ap.add_argument('--alphabet',type=int,default=2)
    ap.add_argument('--mode',choices=['first-map-orbits','exhaustive','random'],default='first-map-orbits')
    ap.add_argument('--count',type=int,default=10000);ap.add_argument('--seed',type=int,default=20260930)
    ap.add_argument('--out',default='direct_attack/data/image_extension_policy_n6')
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    if args.mode=='first-map-orbits' and args.alphabet!=2:raise ValueError('first-map covering is binary only')
    counts=Counter();best=0;max_bound=0;started=time.monotonic();witnesses=0
    for i,rows in enumerate(inputs(args.n,args.mode,args.count,args.seed,args.alphabet)):
        counts['tested']+=1
        if not strongly_connected(rows):continue
        counts['strongly_connected']+=1
        p=extension_profile(rows)
        if p is None:continue
        counts['synchronizing']+=1
        bound=sum(v or 0 for v in p['max_cost_by_rank']);max_bound=max(max_bound,bound)
        if bound<=(args.n-1)**2:counts['certified_by_rank_sum']+=1;continue
        counts['exact_policy_required']+=1;c=policy_profile(rows);cost=c['best_policy']
        if cost>best:
            best=cost;file=f'witness_{witnesses:03d}.json';witnesses+=1
            (out/file).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(dict(source=i,best_policy=cost,rank_sum=bound,seconds=time.monotonic()-started)),flush=True)
        if cost>(args.n-1)**2:counts['violates_square']+=1
    summary=dict(arguments=vars(args),counts=dict(counts),max_rank_sum=max_bound,
                 max_policy_in_unpruned_cases=best,seconds=time.monotonic()-started,
                 scope='Distinct-letter inputs: exhaustive is complete, first-map-orbits is a complete binary cover with overlap, random is sampling.',
                 shortcut='Every phase has positive cardinality gain, so any greedy policy costs at most the sum over ranks of maximum e(S).')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
