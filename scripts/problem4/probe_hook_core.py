"""Bounded generalization probe of the codimension-three hook construction.

No unsuccessful probe is an upper bound. Every saved positive record is
checked using ordinary BFS, including image reachability and synchronization.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
from alphabet_check import certificate, pair_distances, verify

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("m", type=int)
    ap.add_argument("--r", type=int, default=1)
    ap.add_argument("--out", type=Path, required=True)
    args=ap.parse_args()
    n,m,r=args.n,args.m,args.r
    k=m+1;L=n-k-1
    assert L>=5 and 1<=r<L+2
    # K={0,...,k-1}; y=0 by rotation, t/c are independent positions.
    best=None;seen=0;sync=0;candidate_subsets=0;certified=[]
    for t in range(1,k):
        for c in range(1,k):
            if c==t:continue
            z=L-1;d=n-1
            a=list(range(n));a[z]=L;a[L]=z;a[L+t]=z;a[L+c]=d;a[d]=L+c
            b=[(i+1)%L for i in range(L)]+[L+(i+1)%k for i in range(k)]+[d]
            rows=[a,b];seen+=1
            distances=pair_distances(rows)
            if len(distances)!=n*(n-1)//2:continue
            sync+=1
            for core in combinations(range(k),2):
                S=list(range(L))+[L+i for i in core]
                compression=min(distances[pair] for pair in combinations(S,2))
                if best is not None and compression<=best["value"]:continue
                candidate_subsets+=1
                record=certificate(rows,S,r)
                if record is None:continue
                assert record["compression"]==compression and verify(record)
                record.update(core_size=k,hook_t=t,hook_c=c,initial_core=list(core))
                certified.append(record)
                if best is None or record["value"]>best["value"]:
                    best=record;print("new_verified_best",best["value"],"compression",compression,
                                      "t/c",t,c,"core",core,flush=True)
    result=dict(n=n,m=m,r=r,transition_variants=seen,synchronizing_variants=sync,
                candidate_subsets=candidate_subsets,best=best,certificates=certified,
                scope="Bounded hook-core family probe, not an upper-bound computation.")
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("best","certificates")}),flush=True)

if __name__=="__main__":main()
