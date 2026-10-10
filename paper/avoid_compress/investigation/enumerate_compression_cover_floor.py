"""Known compression-bound cover floor on the intact joint inventory."""
from pathlib import Path
from itertools import combinations
import hashlib,json
ROOT=Path(__file__).resolve().parent

def floor(n,h):
    forbidden=[k for k in range(n-1) if (k+2)*(k+1)//2<=h]
    return max(forbidden,default=-1)+1

def inventory():
    joint=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'));rows=[]
    for z in joint['records']:
        protected={3}
        if len(z['B'])==1:protected.update(z['B'])
        if len(z['C'])==1:protected.update(z['C'])
        cover=set(range(3))-protected
        rows.append(dict(id=z['id'],B=z['B'],C=z['C'],protected_through_nine=sorted(protected),
            remaining_P5_cover=sorted(cover),excluded_by_known_bound=len(cover)<floor(13,5)))
    allS=[{3}|set(T) for T in combinations(sorted(set(range(13))-{3}),8)]
    third=[]
    for z in json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))['records']:
        fibers=[set(z[key]) for key in ('B','C','D')]
        forms=[T for T in allS if all(len(T&X)==1 for X in fibers)]
        assert len(forms)==z['feasible_nine_sets'] and forms
        mandatory=set.intersection(*forms);cover=set(range(3))-mandatory
        third.append(dict(id=z['id'],joint_id=z['joint_id'],B=z['B'],C=z['C'],D=z['D'],
            mandatory_through_eight=sorted(mandatory),remaining_P4_cover=sorted(cover),
            excluded_by_known_bound=len(cover)<floor(13,4)))
    return dict(status='necessary_cover_floor_inventory',parameter=[13,9,1],records=rows,third_records=third,
        cover_size_floors={str(h):floor(13,h) for h in range(1,11)},
        excluded_joints=[z['id'] for z in rows if z['excluded_by_known_bound']],
        excluded_third_profiles=[z['id'] for z in third if z['excluded_by_known_bound']],alphabet='arbitrary finite',
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
            [Path(__file__).name,'joint_fiber_orbits.json','small_first_third_inventory.json','compression_cover_primary_source.json']},
        scope='Necessary arbitrary-alphabet cut from the existing compression theorem; no new F value.')

if __name__=='__main__':
    out=inventory();(ROOT/'compression_cover_floor_inventory.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=out['status'],excluded_joints=out['excluded_joints'],floors=out['cover_size_floors'])))
