"""Independent labelled-orbit coverage audit of inverse enumeration at n=5,6.

The C++ diagnostic exports all strongly connected leaves without pruning.
This checker generates every labelled rank-one first map and every allowed
labelled second map. Explicit permutation conjugacy, not component discovery,
proves that the exported rows cover every required orbit at these sizes.
"""
import argparse
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def strong(rows):
    n=len(rows[0])
    for root in range(n):
        seen={root};queue=[root]
        for q in queue:
            for row in rows:
                if row[q] not in seen:seen.add(row[q]);queue.append(row[q])
        if len(seen)!=n:return False
    return True


def conjugate(row,perm):
    out=[0]*len(row)
    for q in range(len(row)):out[perm[q]]=perm[row[q]]
    return tuple(out)


def audit(n,exports):
    permutations_n=list(permutations(range(n)))
    observed={}
    for line in (exports/f"inverse_orbit_n{n}.jsonl").read_text().splitlines():
        z=json.loads(line);a,b=tuple(z["a"]),tuple(z["b"])
        assert strong([a,b])
        observed.setdefault(a,set()).add(b)
    labels={row for row in product(range(n),repeat=n) if len(set(row))==n-1}
    required=set()
    for row in labels:
        power=[q for q in range(n)]
        for _ in range(4):power=[row[q] for q in power]
        if len(set(power))>=n-3:required.add(row)
    covered=set();maps=orbits=0
    for a,actual in observed.items():
        first_orbit={conjugate(a,perm) for perm in permutations_n}
        assert not covered&first_orbit
        covered|=first_orbit
        centralizer=[perm for perm in permutations_n if conjugate(a,perm)==a]
        canonical_cache={}
        def canonical(b):
            if b not in canonical_cache:
                orbit={conjugate(b,perm) for perm in centralizer};key=min(orbit)
                canonical_cache.update((row,key) for row in orbit)
            return canonical_cache[b]
        kernel=[pair for pair in combinations(range(n),2) if a[pair[0]]==a[pair[1]]]
        assert len(kernel)==1;p,q=kernel[0]
        expected=set()
        for perm in permutations_n:
            collapsed=list(perm);collapsed[q]=collapsed[p]
            for b in (perm,tuple(collapsed)):
                if strong([a,b]):expected.add(canonical(b));maps+=1
        actual_canonical={canonical(b) for b in actual}
        assert actual_canonical==expected,(n,a,expected-actual_canonical,actual_canonical-expected)
        orbits+=len(expected)
    assert covered==required,(n,len(covered),len(required))
    report=json.loads((exports/f"inverse_orbit_n{n}.json").read_text())
    assert report["completed"] and report["visited_classes"]==report["first_classes"]==len(observed)
    return dict(n=n,labelled_rank_one_first_maps=len(labels),required_first_maps=len(required),
                canonical_first_forms=len(observed),labelled_strong_second_maps=maps,
                second_orbits=orbits,all_orbits_covered=True,
                scope="No-pruning inverse enumeration versus all labelled maps modulo explicit conjugacy.")


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--exports-dir",type=Path,default=ROOT)
    args=ap.parse_args()
    records=[audit(n,args.exports_dir) for n in (5,6)]
    report=dict(verified=True,records=records,
                scope="Finite coverage audit only; the parameter-uniform normalization needs its mathematical proof.")
    (ROOT/"inverse_enumeration_audit.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report))


if __name__=="__main__":main()
