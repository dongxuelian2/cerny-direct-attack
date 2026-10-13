"""Complete fourth/third coverage for the whole binary C4/D125 exclusion."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parent=read('b1_c4_fourth_audit.json');inv=read('b1_c4_fourth_inventory.json')
    scan=read('c4_d125_fourth_rows_audit.json');trap=read('common_block_profiles_audit.json');closed=read('closed_merging_block_audit.json')
    for z in (parent,scan,trap,closed):
        assert z['status']=='pass'
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert scan['all_C4_D125_binary_fourth_survivors_excluded'] and not scan['independently_validated_witnesses']
    assert scan['all_parent_fourth_pairs']==27 and scan['raw_individual_rows']==2540160
    assert scan['pointwise_transports_checked']==1068480
    assert scan['checked_representative_pairs_per_implementation']==145980000
    assert closed['binary_C4_D125_E6_paper_excluded'] and closed['complete_M_F_pairs']==12798
    third=next(z for z in read('small_first_third_inventory.json')['records'] if z['id']=='b1_in_c1_third5')
    assert third['B']==[0] and third['C']==[4] and third['D']==[1,2,5] and third['labelled_D']==8
    original=set(map(tuple,third['binary_profile_pairs']));assert len(original)==14
    cut=next(z for z in trap['profile_cuts'] if z['id']==third['id'])
    removed=set(map(tuple,cut['removed_parent_pairs']));remaining=set(map(tuple,cut['remaining_parent_pairs']))
    assert original==removed|remaining and not removed&remaining and len(removed)==5 and len(remaining)==9
    geometries=[z for z in inv['records'] if z['D']==[1,2,5]]
    assert [z['E'] for z in geometries]==[[6],[1,6],[1,2,6]]
    assert [z['labelled_E'] for z in geometries]==[7,14,7]
    summary=next(z for z in parent['counts'] if z['D']==[1,2,5])
    assert summary['remaining_unrestricted_E']==[z['E'] for z in geometries]
    coverage=[]
    for z in geometries:
        assert [p['original_third_rows'] for p in z['pairs']]==third['binary_profile_pairs']
        actual=set(tuple(p['original_third_rows']) for p in z['pairs'] if p['fourth_field_pairs'])
        assert actual==remaining
        pairs=[xy for p in z['pairs'] for xy in p['fourth_field_pairs']];assert len(pairs)==9
        r=next(r for r in scan['complete_pair_scans'] if r['E']==z['E'])
        assert r['zero_candidates_both_algorithms'] and r['parent_field_pairs']==len(pairs)
        assert r['Boolean_companions']==z['additional_covered_fibers']==[]
        coverage.append(dict(E=z['E'],labels=z['labelled_E'],remaining_parent_pairs=sorted(map(list,actual)),
            complete_actual_field_pairs=9,rows=r['raw_rows'],kept_rows=r['kept_rows'],representative_pairs=r['complete_representative_pairs']))
    names=[Path(__file__).name,'PROOF.md#problem4-c4-d125-complete-exclusion','PROOF.md#problem4-c4-d125-row-cover','c4_d125_fourth_rows_audit.json',
        'b1_c4_fourth_inventory.json','b1_c4_fourth_audit.json','PROOF.md#problem4-b1-c4-fourth-space','small_first_third_inventory.json',
        'small_first_third_audit.json','PROOF.md#problem4-small-first-third-admission','common_block_profiles_audit.json',
        'PROOF.md#problem4-common-block-singleton-c-profiles','PROOF.md#problem4-common-collapsing-block-trap','closed_merging_block_audit.json','PROOF.md#problem4-closed-merging-block']
    result=dict(status='pass',parameter=[13,9,1],B=[0],C=[4],D=[1,2,5],excluded_third_id=third['id'],
        whole_binary_third_excluded=True,excluded_D_labels=8,complete_original_third_pairs=14,
        earlier_excluded_parent_pairs=5,newly_removed_previously_remaining_pairs=9,
        complete_fourth_geometries=3,complete_E_labels=28,checked_actual_row_fourth_pairs=27,
        complete_representative_pairs_per_implementation=145980000,coverage=coverage,
        unrestricted_remaining_E=summary['remaining_unrestricted_E'],source_sha256={n:sha(ROOT/n) for n in names},
        scope='Whole binary B0/C4/D125 conditional type exclusion. Unrestricted E6/E16/E126, other third/joint types and both F extrema remain unclassified.')
    (ROOT/'c4_d125_composition_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','coverage')}),flush=True)
if __name__=='__main__':main()
