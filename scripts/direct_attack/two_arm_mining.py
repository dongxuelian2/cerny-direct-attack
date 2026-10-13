"""Structured attack: shared-cycle arms, defect orientation and internal permutations."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time
from direct_attack.native_policy import profile
from direct_attack.image_extension_policy import profile as certificate


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--max-n',type=int,default=12)
    ap.add_argument('--permutations',type=int,default=20);ap.add_argument('--seed',type=int,default=20261002)
    ap.add_argument('--out',default='scripts/direct_attack/data/image_extension_policy_two_arms');args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);rng=random.Random(args.seed)
    records=[];maxima={};counts=Counter();started=time.monotonic();failures=[]
    for n in range(5,args.max_n+1):
        for t in range(n-2):
            a=list(range(n))
            for q in range(t,n):a[q]=t+(q-t+1)%(n-t)
            rest=list(range(t+1,n-1));perms=[rest,rest[::-1],rest[1:]+rest[:1],rest[-1:]+rest[:-1]]
            if len(rest)>1:
                swap=list(rest);swap[-2],swap[-1]=swap[-1],swap[-2];perms.append(swap)
            for _ in range(args.permutations):p=list(rest);rng.shuffle(p);perms.append(p)
            perms=list(dict.fromkeys(map(tuple,perms)))
            for direction in [1,-1]:
                for defect in [t+1,n-1]:
                    # The rest excludes the selected defect source.
                    movable=[q for q in range(t+1,n) if q!=defect]
                    for pi in perms:
                        targets=[movable[rest.index(q)] for q in pi]
                        b=list(range(n))
                        for q in range(t+1):b[q]=(q+direction)%(t+1)
                        b[defect]=b[t]
                        for q,z in zip(movable,targets):b[q]=z
                        rows=[a,b];counts['tested']+=1;p=profile(rows)
                        if p is None:continue
                        counts['synchronizing_sc']+=1
                        r=dict(n=n,arm=t,main_cycle=n-t,direction=direction,defect=defect,rows=rows,
                               best_policy=p['best_policy'],rt=p['rt'],local_excess=p['local_excess'],local_start=p['local_start'])
                        records.append(r)
                        if p['best_policy']>maxima.get(n,0):
                            maxima[n]=p['best_policy'];print(json.dumps({k:v for k,v in r.items() if k!='rows'}),flush=True)
                        if p['best_policy']>(n-1)**2:
                            c=certificate(rows);c['structured_parameters']=r
                            path=out/f'witness_{len(failures):03d}.json';failures.append(str(path))
                            path.write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
                            counts['square_violations']+=1
    report=dict(arguments=vars(args),counts=dict(counts),maxima=maxima,records=records,failures=failures,
                seconds=time.monotonic()-started,scope='Finite structured parameter search; not complete DFA coverage.')
    (out/'summary.json').write_text(json.dumps(report,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='records'}))


if __name__=='__main__':main()
