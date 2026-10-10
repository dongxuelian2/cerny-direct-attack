"""All fourteen B3 joints: geometric third admission and known-cover cut.

No binary row admission is reopened. All B3 joints were already excluded
for binary alphabets; this inventory concerns arbitrary finite alphabets.
"""
from itertools import combinations, product
from pathlib import Path
import hashlib, json, math
from enumerate_small_first_third import covered, fibers, incomparable, rank

ROOT=Path(__file__).resolve().parent
Q=set(range(13)); A={3}; H={0,1,2}; O=Q-A

def inventory():
    joints=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))
    allS=[A|set(points) for points in combinations(sorted(O),8)]
    records=[]; counts={}
    for joint in joints['records']:
        B=set(joint['B']); C=set(joint['C'])
        if len(B)!=3: continue
        cells=[{q for q in O if (int(q in H),int(q in B),int(q in C))==key}
               for key in product((0,1),repeat=3)]
        forms=[T for T in allS if len(T&B)==len(T&C)==1]
        candidates={}
        for D in covered():
            if len(B|C|D)>6 or not incomparable(D,B) or not incomparable(D,C): continue
            valid=[T for T in forms if len(T&D)==1]
            if not valid or rank([[1,int(q in B),int(q in C),int(q in D)] for q in sorted(O)])!=4: continue
            signature=tuple(len(D&cell) for cell in cells)
            if signature in candidates:
                candidates[signature]['labelled_D']+=1; continue
            canonical=set().union(*(set(sorted(cell)[:size]) for cell,size in zip(cells,signature)))
            assert canonical==D
            allowed=fibers(B,C,D)
            assert all(all(len(T&R)==1 for T in valid) for R in allowed)
            mandatory=set.intersection(*valid); remainder=H-mandatory
            candidates[signature]=dict(joint_id=joint['id'],B=sorted(B),C=sorted(C),D=sorted(D),
                cell_signature=list(signature),labelled_D=1,
                orbit_size=math.prod(math.comb(len(cell),size) for cell,size in zip(cells,signature)),
                feasible_nine_sets=len(valid),allowed_preC_fibers=[sorted(R) for R in allowed],
                extra_boolean_fibers=[sorted(R) for R in allowed if R not in (B,C,D)],
                mandatory_through_eight=sorted(mandatory),remaining_P4_cover=sorted(remainder),
                excluded_by_known_bound=len(remainder)<=1)
        for i,record in enumerate(candidates.values(),1):
            assert record['labelled_D']==record['orbit_size']
            record['id']=joint['id']+'_third'+str(i); records.append(record)
        counts[joint['id']]=dict(geometric_orbits=len(candidates),
            labelled_D=sum(v['labelled_D'] for v in candidates.values()),
            extra_boolean_fiber_orbits=sum(bool(v['extra_boolean_fibers']) for v in candidates.values()),
            excluded_orbits=sum(v['excluded_by_known_bound'] for v in candidates.values()))
    names=[Path(__file__).name,'enumerate_small_first_third.py','joint_fiber_orbits.json',
        'THIRD_ENTRANCE_SPACE.md','COMPRESSION_COVER_FLOOR.md','ENTRY_FIBER_FLAG.md',
        'SECOND_ENTRANCE_FIBER.md','LOCAL_EQUALITY_FLAG.md','compression_cover_primary_source.json',
        'third_entrance_inventory.json','small_first_third_inventory.json']
    return dict(status='necessary_B3_third_inventory',parameter=[13,9,1],counts=counts,records=records,
        excluded_profiles=[v['id'] for v in records if v['excluded_by_known_bound']],
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='All fourteen B3 joints, arbitrary finite alphabet, preserving all same-level Boolean fibers. '
              'Known P4 cover-floor cut only; not an automaton-existence test or a new F value.')

if __name__=='__main__':
    result=inventory()
    (ROOT/'b3_third_cover_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(joint_cases=len(result['counts']),geometric_orbits=len(result['records']),
        labelled_D=sum(v['labelled_D'] for v in result['records']),
        extra_boolean_fiber_orbits=sum(bool(v['extra_boolean_fibers']) for v in result['records']),
        excluded_profiles=result['excluded_profiles'])))
