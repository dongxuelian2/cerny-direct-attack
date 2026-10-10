"""Independent exhaustive bit-mask check of every B3 third geometry.

Does not import the generator or its rational-rank/fiber routines.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parent
FULL=(1<<13)-1; A=1<<3; OUT=FULL^A; H=7

def mask(points): return sum(1<<x for x in points)
def points(value): return [q for q in range(13) if value>>q&1]
def incomparable(x,y): return bool(x&~y) and bool(y&~x)

def rank101(columns):
    # Every square minor here has order <=5 and entries 0,1.
    # Hadamard bounds its magnitude by 5**(5/2)<101, so no nonzero
    # rational minor vanishes modulo this prime.
    work=[[int(bool(col>>q&1)) for col in columns] for q in points(OUT)]
    pivot=0
    for j in range(len(columns)):
        index=next((i for i in range(pivot,len(work)) if work[i][j]),None)
        if index is None: continue
        work[pivot],work[index]=work[index],work[pivot]
        scale=pow(work[pivot][j],-1,101)
        work[pivot]=[x*scale%101 for x in work[pivot]]
        for i in range(pivot+1,len(work)):
            factor=work[i][j]
            if factor: work[i]=[(x-factor*y)%101 for x,y in zip(work[i],work[pivot])]
        pivot+=1
    return pivot

def signature(d,b,c):
    cells=list(product((0,1),repeat=3))
    return tuple(sum((d>>q&1) and (int(bool(H>>q&1)),int(bool(b>>q&1)),int(bool(c>>q&1)))==key
                     for q in points(OUT)) for key in cells)

def main():
    inventory=json.loads((ROOT/'b3_third_cover_inventory.json').read_text(encoding='utf-8'))
    for name,digest in inventory['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    allS=[t for t in range(FULL+1) if t&A and t.bit_count()==9]
    allD=[d for d in range(1,FULL+1) if not d&A and d.bit_count()<=4 and (d&~H).bit_count()<=1]
    assert len(allS)==495 and len(allD)==79
    joints=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))['records']
    rows={z['id']:z for z in inventory['records']}; verified=set()
    labelled=intersections=span_tests=0; literal_excluded=0; summaries={}
    for joint in joints:
        if len(joint['B'])!=3: continue
        b=mask(joint['B']); c=mask(joint['C'])
        current={tuple(v['cell_signature']):v for v in rows.values() if v['joint_id']==joint['id']}
        assert len(current)==len([v for v in rows.values() if v['joint_id']==joint['id']])
        seen=Counter(); cuts=0
        for d in allD:
            if (b|c|d).bit_count()>6 or not incomparable(d,b) or not incomparable(d,c): continue
            if rank101([OUT,b,c,d])!=4: continue
            forms=[t for t in allS if (t&b).bit_count()==(t&c).bit_count()==(t&d).bit_count()==1]
            if not forms: continue
            sig=signature(d,b,c); assert sig in current
            z=current[sig]; seen[sig]+=1; labelled+=1; intersections+=len(allS)
            common=FULL
            for t in forms: common&=t
            assert len(forms)==z['feasible_nine_sets']
            excluded=(H&~common).bit_count()<=1
            assert excluded==z['excluded_by_known_bound']; literal_excluded+=excluded
            if d!=mask(z['D']): continue
            verified.add(z['id']); cuts+=excluded
            assert points(common)==z['mandatory_through_eight']
            assert points(H&~common)==z['remaining_P4_cover']
            allowed=set()
            for R in allD:
                if any(R!=X and not incomparable(R,X) for X in (b,c,d)): continue
                span_tests+=1
                if rank101([OUT,b,c,d,R])!=4: continue
                if all((t&R).bit_count()==1 for t in forms): allowed.add(R)
            assert allowed=={mask(R) for R in z['allowed_preC_fibers']},z['id']
            assert allowed-{b,c,d}=={mask(R) for R in z['extra_boolean_fibers']}
        assert set(seen)==set(current)
        for sig,count in seen.items(): assert count==current[sig]['labelled_D']==current[sig]['orbit_size']
        summaries[joint['id']]=dict(geometric_orbits=len(current),labelled_D=sum(seen.values()),
            extra_boolean_fiber_orbits=sum(bool(z['extra_boolean_fibers']) for z in current.values()),excluded_orbits=cuts)
    assert summaries==inventory['counts'] and verified==set(rows)
    assert len(summaries)==14 and len(rows)==127 and labelled==827
    assert sum(bool(v['extra_boolean_fibers']) for v in rows.values())==18
    assert set(inventory['excluded_profiles'])=={'b3_mixed_c4_third2','b3_mixed_c6_third5'}
    assert literal_excluded==3
    old=json.loads((ROOT/'third_entrance_inventory.json').read_text(encoding='utf-8'))
    old_keys={}
    for z in old['records']:
        key=(z['case'],tuple(z['D'])); old_keys[key]=z
    matched=0
    for z in rows.values():
        if z['joint_id'] not in old['counts']: continue
        historical=old_keys[(z['joint_id'],tuple(z['D']))]
        assert z['feasible_nine_sets']==historical['feasible_nine_sets']
        assert z['labelled_D']==historical['labelled_D']
        assert {tuple(R) for R in z['allowed_preC_fibers']}=={tuple(R['R']) for R in historical['allowed_preC_fibers']}
        matched+=1
    assert matched==len(old_keys)==36
    oldsmall=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))['records']
    oldcut=json.loads((ROOT/'compression_cover_floor_inventory.json').read_text(encoding='utf-8'))
    assert len(oldsmall)==235 and len(oldcut['excluded_third_profiles'])==11
    assert len(oldsmall)+len(rows)==362 and sum(v['labelled_D'] for v in oldsmall)+labelled==2309
    # Separate literal Boolean audit of both excluded equations; swapping
    # C,D changes no equation and does not identify the two joint orbits.
    truth=[]
    for x0,x1,x2,x4 in product((0,1),repeat=4):
        if x0+x1+x4==x2+x4==x0+x2==1: truth.append([x0,x1,x2,x4])
    assert truth==[[0,1,1,0]]
    names=set(inventory['source_sha256'])|{Path(__file__).name,'b3_third_cover_inventory.json',
        'B3_THIRD_COVER.md','compression_cover_floor_inventory.json'}
    result=dict(status='pass',parameter=[13,9,1],arbitrary_finite_alphabet=True,
        complete_joint_cases=14,complete_geometric_orbits=127,complete_labelled_D_choices=labelled,
        literal_nine_family_membership_tests=intersections,independent_candidate_R_span_tests=span_tests,
        additional_boolean_fiber_orbits=18,historical_third_orbits_matched=matched,
        excluded_profiles=inventory['excluded_profiles'],excluded_labelled_D_choices=literal_excluded,
        Boolean_equation_solutions=truth,combined_geometric_orbits=362,combined_labelled_D_choices=2309,
        combined_excluded_orbits=13,unrestricted_geometric_remaining=349,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sorted(names)},
        scope='Complete necessary B3 geometry, extra fibers and known-cover intersection cut; no full automaton search, F value or numerical alphabet separation.')
    (ROOT/'b3_third_cover_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}))

if __name__=='__main__': main()
