"""Literal finite alphabet pools for the nine ordered short-pair types.

Every letter in a tight compression automaton has rank n or n-1 with a
single common kernel. Enumerating permutations and collapsing the second
kernel endpoint generates every such transformation exactly once. The
early-pair inequalities are necessary for any actual witness, for any
alphabet size. This builder is presently bounded to n<=8.
"""
import argparse
from itertools import combinations, permutations
import json
from pathlib import Path


def patterns():
    return ([((0, 1), (0, 2), last) for last in
             ((1, 2), (0, 3), (1, 3), (2, 3), (3, 4))] +
            [((0, 1), (2, 3), last) for last in
             ((0, 2), (0, 4), (2, 4), (4, 5))])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("n",type=int)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    n=args.n;assert 6<=n<=8
    pairs=list(combinations(range(n),2));types=patterns();pools=[[] for _ in types]
    for perm in permutations(range(n)):
        collapsed=list(perm);collapsed[1]=collapsed[0]
        for row in (list(perm),collapsed):
            if row==list(range(n)):continue
            images=[None if row[x]==row[y] else tuple(sorted((row[x],row[y])))
                    for x,y in pairs]
            for i,sequence in enumerate(types):
                values={pair:d+1 for d,pair in enumerate(sequence)}
                if all(values.get(pair,4)<=1+(0 if image is None else
                                             values.get(image,10))
                       for pair,image in zip(pairs,images)):
                    pools[i].append(row)
    records=[dict(pattern=i,early_pairs=sequence,letters=pool,alphabet_pool_size=len(pool))
             for i,(sequence,pool) in enumerate(zip(types,pools))]
    for record in records:
        assert len(set(map(tuple,record["letters"])))==len(record["letters"])
    result=dict(n=n,s=n-3,target=10,records=records,
                scope="Complete individual-letter pools for tight compression and nine early-pair types; no existence or nonexistence assertion.")
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print([(z["pattern"],z["alphabet_pool_size"]) for z in records])


if __name__=="__main__":main()
