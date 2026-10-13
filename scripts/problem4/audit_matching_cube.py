"""Independent inverse-case action generation followed by literal subset images.

The primary builder scans forward partial rows. This checker instead fixes
the inverse fibers of 01 and 23, constructs full twelve-state rows, and
computes the eight images by ordinary sets. Every allowed core case is
explicitly classified; labels 6,...,11 represent external outputs.
"""
import argparse
from itertools import permutations,product
import json
from pathlib import Path


def extend(partial,missing):
    unused=sorted(set(range(12))-set(partial.values())-({missing} if missing is not None else set()))
    assert len(unused)==6
    return [partial[q] for q in range(6)]+unused


def rows():
    # Permutations: inverse 01 is K or E2, inverse 23 is a distinct
    # member of K,E2,E3. The two remaining core sources are free.
    pairs=((0,1),(2,3),(4,5))
    for i in (0,1):
        for j in range(3):
            if i==j:continue
            for x,y in product(permutations(pairs[i]),permutations(pairs[j])):
                fixed=dict(zip(x,(0,1)))|dict(zip(y,(2,3)))
                free=sorted(set(range(6))-set(fixed))
                for values in permutations(sorted(set(range(12))-set(fixed.values())),2):
                    yield extend(fixed|dict(zip(free,values)),None),None,'permutation'
    # Singular rows: 0,1 have a common image c. When missing is in 01,
    # inverse 23 is E2 or E3. When missing is in 23, inverse 01 is E2.
    # Otherwise inverse 01 is E2 and inverse 23 is E3.
    for missing in range(12):
        if missing in (0,1):
            for pair in pairs[1:]:
                for oriented in permutations(pair):
                    fixed=dict(zip(oriented,(2,3)))
                    for c in sorted(set(range(12))-{missing,2,3}):
                        base=fixed|{0:c,1:c};free=sorted(set(range(6))-set(base))
                        for values in permutations(sorted(set(range(12))-set(base.values())-{missing}),2):
                            yield extend(base|dict(zip(free,values)),missing),missing,'missing01'
        elif missing in (2,3):
            for oriented in permutations((2,3)):
                fixed=dict(zip(oriented,(0,1)))
                for c in sorted(set(range(12))-{missing,0,1}):
                    base=fixed|{0:c,1:c}
                    for values in permutations(sorted(set(range(12))-set(base.values())-{missing}),2):
                        yield extend(base|dict(zip((4,5),values)),missing),missing,'missing23'
        else:
            for left,right in product(permutations((2,3)),permutations((4,5))):
                fixed=dict(zip(left,(0,1)))|dict(zip(right,(2,3)))
                for c in sorted(set(range(12))-{missing,0,1,2,3}):
                    yield extend(fixed|{0:c,1:c},missing),missing,'missing_other'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('data',type=Path)
    ap.add_argument('--profiles-text',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    observed=set();counts={'permutation':0,'missing01':0,'missing23':0,'missing_other':0}
    holes=[frozenset((x,2+y,4+z)) for x,y,z in product(range(2),repeat=3)]
    Q=set(range(12))
    for result in rows():
        row,missing=result[:2];kind=result[-1];counts[kind]+=1
        assert len(row)==12
        assert len(set(row))==(12 if missing is None else 11)
        if missing is not None:assert set(row)==Q-{missing} and row[0]==row[1]
        for edge,allowed in (((0,1),{(0,1),(2,3)}),((2,3),{(0,1),(2,3),(4,5)})):
            inverse={pair for pair in __import__('itertools').combinations(range(12),2)
                     if {row[q] for q in pair}==set(edge)}
            assert inverse<=allowed
        p=[]
        for H in holes:
            image={row[q] for q in Q-H};assert len(image)==9
            following=frozenset(Q-image)
            p.append(holes.index(following) if following in holes else -1)
        observed.add(tuple(p))
    data=json.loads(args.data.read_text());assert set(map(tuple,data['profiles']))==observed
    assert counts==dict(permutation=896,missing01=4032,missing23=2016,missing_other=224)
    assert len(observed)==177
    args.profiles_text.write_text(''.join(' '.join(map(str,p))+'\n' for p in sorted(observed)))
    output=dict(status='pass',method='Inverse cases and literal full-row subset images',
                counts=counts,profiles=len(observed),all_primary_profiles_equal=True,
                scope='Complete independent matching-type projection audit, not a global maximum.')
    args.out.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output))


if __name__=='__main__':main()
