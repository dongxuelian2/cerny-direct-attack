"""Literal B3 mandatory cores and the whole singleton-C guard joint."""
from pathlib import Path
from itertools import combinations
import json,hashlib
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};H={0,1,2}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    reports=['b3_third_cover_audit.json','two_cover_unique_immediate_pair_audit.json','mandatory_core_isolation_audit.json']
    for n in reports:
        z=read(n);assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f
    inv=read('b3_third_cover_inventory.json')['records'];allS=[set(S) for S in combinations(range(13),9) if 3 in S]
    records=[];new=[];allids=[]
    for z in inv:
        B,C,D=map(set,(z['B'],z['C'],z['D']))
        forms=[S for S in allS if all(len(S&X)==1 for X in (B,C,D))]
        assert len(forms)==z['feasible_nine_sets'];J=set.intersection(*forms)
        assert sorted(J)==z['mandatory_through_eight'];K=H-J
        if len(K)>2:continue
        assert len(B)==3 and len(list(combinations(sorted(B),2)))==3
        allids.append(z['id'])
        if not z['excluded_by_known_bound']:new.append(z['id'])
        records.append(dict(id=z['id'],mandatory=sorted(J),residual_P5_cover=sorted(K),
                            forced_P1_pairs=list(map(list,combinations(sorted(B),2))),historical_known_cut=z['excluded_by_known_bound']))
    assert len(new)==11
    labels=0
    for guard_pair in combinations(sorted(H),2):
        C=H-set(guard_pair)
        for ordinary in sorted(Q-H-A):
            B=set(guard_pair)|{ordinary}
            assert len(B)==3 and len(C)==1 and len(list(combinations(sorted(B),2)))==3
            assert len(H-C)==2;labels+=1
    assert labels==27
    remaining=[z for z in inv if not z['excluded_by_known_bound'] and z['id'] not in new]
    assert len(remaining)==114
    assert all(not (H&set(z['mandatory_through_eight'])) for z in remaining)
    assert {z['id'] for z in inv if z['joint_id']=='b3_mixed_c2'}<=set(allids)
    names=[Path(__file__).name,'PROOF.md#problem4-b3-two-cover-unique-kernel-exclusion',*reports,
           'b3_third_cover_inventory.json','PROOF.md#problem4-b3-third-cover','PROOF.md#problem4-third-entrance-space',
           'PROOF.md#problem4-mandatory-core-isolation','PROOF.md#problem4-two-cover-unique-immediate-pair','PROOF.md#problem4-compression-cover-floor',
           'PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-second-entrance-fiber']
    result=dict(status='pass',parameter=[13,9,1],all_inventory_unrestricted_excluded_ids=allids,
                newly_excluded_previously_remaining_ids=new,new_unrestricted_third_types=11,remaining_unrestricted_B3_types=114,
                excluded_unrestricted_joint_ids=['b3_mixed_c2'],whole_joint_labelled_choices=labels,records=records,
                source_sha256={n:sha(ROOT/n) for n in names},
                scope='B3 arbitrary-alphabet unique-kernel contradictions with an explicit stripped cover, including one whole joint. Three-cover remainder and F unresolved.')
    (ROOT/'b3_two_cover_unique_kernel_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','records','all_inventory_unrestricted_excluded_ids')}),flush=True)
if __name__=='__main__':main()
