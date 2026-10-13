"""Finite actions used after the uniform triangle mixing reduction.

This is research proof data, not a new exact maximum. Case A and Case B
with f(2)=1 have separate pure exclusions. Complete projection proofs and
an independent forward-row audit must accompany any theorem using this.
"""
from itertools import permutations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CORE={0,1,2}


def actions(D):
    E=set().union(*D)-CORE
    outs=range(3,max(E)+len(E)+1)
    profiles={}
    def add(row,missing=None):
        p=[]
        for H in D:
            if missing is None:J=frozenset(row[q] for q in H)
            elif {0,1}<=H:J=frozenset([missing]+[row[q] for q in H])
            else:J=frozenset([missing]+[row[q] for q in H if q not in (0,1)])
            assert len(J)==3
            if len(J&CORE)<2:return
            p.append(D.index(J) if J in D else -1)
        key=tuple(p)
        closed=set(row.values())<=CORE|E
        profiles.setdefault(key,[]).append(dict(row=row,missing=missing,core_closed=closed))
    for core in permutations(range(3)):
        if {q for q in CORE if core[q] in (0,1)} not in ({0,1},{0,2}):continue
        for values in permutations(outs,len(E)):
            add(dict(enumerate(core))|dict(zip(sorted(E),values)))
    for missing in (0,1):
        for c,t in permutations(CORE-{missing},2):
            for values in permutations(outs,len(E)):
                add({0:c,1:c,2:t}|dict(zip(sorted(E),values)),missing)
    # Case B with f(2)=2. Its unique external preimage of 1 may be
    # represented in E or may be external. The latter cannot pass the
    # domains used here, because they contain a 01x hole set.
    for v in E:
        for c in outs:
            rest=sorted(E-{v})
            for values in permutations([q for q in outs if q!=c],len(rest)):
                add({0:c,1:c,2:2,v:1}|dict(zip(rest,values)),0)
    # Case C: f(0)=f(1) and f(2) are distinct external outputs.
    # Any represented source sent to 1 or 2 is chosen explicitly.
    for left,right in permutations(E,2):
        for c,t in permutations(outs,2):
            rest=sorted(E-{left,right})
            for values in permutations([q for q in outs if q not in (c,t)],len(rest)):
                add({0:c,1:c,2:t,left:1,right:2}|dict(zip(rest,values)),0)
    return profiles


def check(profiles,size):
    candidates=[];checked=0
    for d in permutations(range(1,size+1)):
        checked+=1
        allowed=[p for p in profiles if all(d[q]<=1+(d[p[q]] if p[q]>=0 else 0) for q in range(size))]
        reached=set()
        for _ in range(size):
            reached|={q for p in allowed for q in range(size) if p[q]<0 or p[q] in reached}
        if len(reached)==size:
            closed=all(row['core_closed'] for p in allowed for row in profiles[p])
            candidates.append(dict(distance_vector=d,alphabet_profiles=allowed,all_allowed_rows_core_closed=closed))
    return dict(distance_vectors=checked,candidates=candidates)


def main():
    records=[]
    families=[('case_b_equal',[(0,1,2),(0,1,3),(0,2,3),(1,2,3)]),
              ('case_b_two_external',[(0,1,3),(0,2,4),(1,2,3),(1,2,4)]),
              ('case_c',[(0,1,3),(0,1,4),(0,2,3),(0,2,4),(1,2,3),(1,2,4)])]
    for name,holes in families:
        D=list(map(frozenset,holes));profiles=actions(D);check_data=check(profiles,len(D))
        if name=='case_b_two_external':
            assert len(check_data['candidates'])==3
            assert all(z['all_allowed_rows_core_closed'] for z in check_data['candidates'])
        else:assert not check_data['candidates']
        records.append(dict(name=name,holes=holes,profile_count=len(profiles),
                            profiles=sorted(profiles),
                            profile_core_closed=[dict(profile=p,all_rows_core_closed=all(z['core_closed'] for z in profiles[p]))
                                                 for p in sorted(profiles)],**check_data))
    result=dict(records=records,
                scope='Complete reduced action checks; uniform triangle reduction and independent projection audit are required.')
    (ROOT/'triangle_reduced_actions.json').write_text(json.dumps(result,indent=2)+'\n')
    for z in records:print(z['name'],z['profile_count'],z['distance_vectors'],len(z['candidates']))


if __name__=='__main__':main()
