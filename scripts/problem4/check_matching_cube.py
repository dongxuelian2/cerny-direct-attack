"""Exact finite action check, with no SAT or fixed alphabet-size limit.

An alphabet is any subset of the supplied action profiles. If every cube
state can exit, its shortest exit distances range from 1 to at most 8,
and use every value through their maximum. Enumerate all distance vectors
whose first state has distance at least 7. Taking all profiles satisfying
d(v)<=1+d(f(v)) cannot shorten the asserted lower bounds. If their union
still cannot make all states exit, no alphabet realizes that vector.
"""
import argparse
from collections import deque
from itertools import permutations,product
import json
from pathlib import Path


def vectors():
    for duplicate in range(1,8):
        rest=list(range(1,7))+[duplicate]
        if duplicate==7:rest=list(range(1,8))
        for values in set(permutations(rest)):
            yield (7,)+values
    for first in (7,8):
        for values in permutations([q for q in range(1,9) if q!=first]):
            yield (first,)+values


def exit_distances(profiles,dist):
    allowed=[p for p in profiles if all(dist[v]<=1+(0 if p[v]<0 else dist[p[v]]) for v in range(8))]
    reverse=[set() for _ in range(9)]
    for profile in allowed:
        for v,t in enumerate(profile):reverse[8 if t<0 else t].add(v)
    result=[None]*9;result[8]=0;queue=deque([8])
    while queue:
        t=queue.popleft()
        for v in reverse[t]:
            if result[v] is None:result[v]=result[t]+1;queue.append(v)
    return result[:8],allowed


def profile(row,missing=None):
    holes=[frozenset((x,2+y,4+z)) for x,y,z in product(range(2),repeat=3)]
    result=[]
    for H in holes:
        T=frozenset(row[q] for q in H) if missing is None else frozenset([missing]+[row[q] for q in H if q>=2])
        result.append(holes.index(T) if T in holes else -1)
    return tuple(result)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('data',type=Path)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    data=json.loads(args.data.read_text());profiles=set(map(tuple,data['profiles']))
    assert len(profiles)==data['profile_count']
    literal=[]
    for n in (6,7):
        pool=json.loads((args.data.parent/f'early_alphabet_pool_n{n}.json').read_text())
        actual=set()
        for row in pool['records'][8]['letters']:
            missing=None if len(set(row))==n else next(iter(set(range(n))-set(row)))
            p=profile(row,missing);assert p in profiles;actual.add(p)
        literal.append(dict(n=n,pool_letters=len(pool['records'][8]['letters']),profiles=len(actual),all_included=True))
    chain=[tuple(list(range(1,8))+[-1])]
    distances,allowed=exit_distances(chain,tuple(range(8,0,-1)))
    assert distances==list(range(8,0,-1)) and allowed==chain
    count=0;found=None
    for values in vectors():
        count+=1;distances,allowed=exit_distances(profiles,values)
        if all(d is not None for d in distances):
            assert distances[0]>=7 and all(d>=p for d,p in zip(distances,values))
            found=dict(lower_potential=values,actual_exit_distances=distances,alphabet_profiles=allowed);break
    if found is None:assert count==30240
    result=dict(profile_count=len(profiles),distance_vectors_checked=count,
                all_states_exit_with_first_distance_at_least_seven=found is not None,
                witness=found,literal_controls=literal,artificial_positive_control='pass',
                scope='Complete check on the supplied matching-type action profiles; projection proof still requires audit.')
    args.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='witness'}))
    if found:print(json.dumps(found))


if __name__=='__main__':main()
