"""Exact finite controls for PROOF.md#problem4-local-equality-flag; no floating point."""
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import time
from check_short_pair_span import exact_rank

ROOT=Path(__file__).resolve().parent


def coplanar_masks(a,b,c,d):
    if len({a,b,c,d})<4:
        return True
    return any((x&y)==(z&w) and (x^y)==(z^w)
               for x,y,z,w in ((a,b,c,d),(a,c,b,d),(a,d,b,c)))


def image(mask,row):
    result=0
    for q,t in enumerate(row):
        if mask & (1<<q):
            result |= 1<<t
    return result


def prefix_images(rows,S,depth):
    layers=[{sum(1<<q for q in S)}]
    for _ in range(depth):
        layers.append({image(mask,row) for mask in layers[-1] for row in rows})
    return set().union(*layers)


def main():
    started=time.monotonic()
    cube=[]
    for n in range(1,7):
        count=0
        for masks in combinations(range(1<<n),4):
            rows=[[1]+[(mask>>q)&1 for q in range(n)] for mask in masks]
            assert coplanar_masks(*masks)==(exact_rank(rows,n+1)<=3), (n,masks)
            count+=1
        # Coincidences are exact in every dimension, including reordered ones.
        for a in range(1<<n):
            for b in range(1<<n):
                assert coplanar_masks(a,b,a,b)
        cube.append(dict(dimension=n,distinct_quadruples=count))
        print(json.dumps(cube[-1]),flush=True)
    frontier=json.loads((ROOT/'frontier_certificates.json').read_text(encoding='utf-8'))['certificates']
    records=[]
    for z in frontier:
        n,t=z['n'],z['value']
        if t!=n-z['r']:
            continue
        depth=min(2,t-1)
        ranks=[]
        for i in range(depth+1):
            masks=prefix_images(z['rows'],z['S'],i)
            rank=exact_rank([[(mask>>q)&1 for q in range(n)] for mask in masks],n)
            assert rank==i+1,(z,i,rank)
            assert all(mask.bit_count()==z['s'] and
                       all(mask&(1<<q) for q in z['A']) for mask in masks)
            ranks.append(rank)
            if i==1:
                assert len(masks)<=2
            if i==2:
                assert len(masks)<=4
                assert all(coplanar_masks(*four) for four in combinations(masks,4))
        records.append(dict(n=n,s=z['s'],r=z['r'],target=t,prefix_ranks=ranks))
    result=dict(status='all_exact_controls_passed',cube=cube,equality_witnesses=len(records),
                records=records,seconds=time.monotonic()-started,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='Finite controls for a symbolic equality consequence; no new extremal formula.')
    (ROOT/'local_equality_flag_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],equality_witnesses=len(records))),flush=True)


if __name__=='__main__':
    main()
