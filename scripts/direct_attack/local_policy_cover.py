"""Complete finite attack on G(S)<=n(n-|S|), checking every reachable S."""
import argparse
from collections import Counter
import json
from pathlib import Path
import time
from direct_attack.core import strongly_connected
from direct_attack.mine import inputs
from direct_attack.native_policy import profile
from direct_attack.image_extension_policy import profile as certificate


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--alphabet',type=int,default=2)
    ap.add_argument('--mode',choices=['exhaustive','first-map-orbits','random'],default='first-map-orbits')
    ap.add_argument('--count',type=int,default=10000);ap.add_argument('--seed',type=int,default=20261001)
    ap.add_argument('--out',required=True);args=ap.parse_args()
    if args.mode=='first-map-orbits' and args.alphabet!=2:raise ValueError('cover is binary only')
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);counts=Counter();best=-1000000000;records=[];started=time.monotonic()
    for i,rows in enumerate(inputs(args.n,args.mode,args.count,args.seed,args.alphabet)):
        counts['tested']+=1
        if not strongly_connected(rows):continue
        counts['strongly_connected']+=1;p=profile(rows)
        if p is None:continue
        counts['synchronizing_sc']+=1
        if p['local_excess']>best:
            best=p['local_excess'];c=certificate(rows);S=p['local_start']
            assert c['best'][S]-args.n*(args.n-S.bit_count())==best
            c['local_bound_witness']=dict(start=S,cost=c['best'][S],bound=args.n*(args.n-S.bit_count()),excess=best)
            name=f'witness_{len(records):03d}.json';records.append(name)
            (out/name).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(dict(source=i,local_excess=best,start=S,size=S.bit_count(),seconds=time.monotonic()-started)),flush=True)
        if p['local_excess']>0:counts['local_bound_violations']+=1;break
    report=dict(arguments=vars(args),counts=dict(counts),max_excess=best,records=records,seconds=time.monotonic()-started,
                proposed='G(S)<=n(n-|S|) for EVERY reachable S',
                scope='Complete distinct-letter inputs only if exhaustive/first-map-orbits finishes without early refutation; overlap not class counts.')
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':main()
