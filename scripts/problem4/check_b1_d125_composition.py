"""Verify every fourth alternative and all parent pairs for binary D125."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    inventory=read('b1_c14_nonsingleton_fourth_inventory.json')
    parent=read('b1_c14_nonsingleton_fourth_audit.json')
    scan=read('d125_fourth_rows_audit.json')
    assert parent['status']==scan['status']=='pass'
    assert scan['binary_E6_E26_excluded'] and scan['all_parent_fourth_pairs']==12
    assert scan['raw_individual_rows']==241920
    assert scan['checked_representative_pairs_per_implementation']==7164000
    for audit in (parent,scan):
        for n,h in audit['source_sha256'].items():assert sha(ROOT/n)==h,n
    third=next(z for z in read('small_first_third_inventory.json')['records'] if z['id']=='b1_in_c3_third7')
    assert third['D']==[1,2,5] and third['labelled_D']==8
    assert third['binary_profile_pairs']==[[1,5],[2,4],[4,5]]
    records=[z for z in inventory['records'] if z['D']==[1,2,5]]
    assert [z['E'] for z in records]==[[6],[1,6],[2,4],[2,6],[1,2,6]]
    assert sum(z['labelled_E'] for z in records)==29
    summary=next(z for z in parent['counts'] if z['D']==[1,2,5])
    assert summary['remaining_binary_E']==[[6],[2,6]]
    assert summary['remaining_unrestricted_E']==[[6],[1,6],[2,6],[1,2,6]]
    for z in records:
        assert [p['original_third_rows'] for p in z['pairs']]==third['binary_profile_pairs']
        pairs=[xy for p in z['pairs'] for xy in p['fourth_field_pairs']]
        if z['E'] in ([6],[2,6]):
            actual=next(r for r in scan['complete_pair_scans'] if r['E']==z['E'])
            assert actual['parent_field_pairs']==len(pairs) and actual['zero_candidates_both_algorithms']
        else:
            assert not pairs
            if z['E']==[2,4]:
                assert z['E'] in summary['all_alphabet_excluded_E']
                detail=next(d for d in parent['records'] if d['D']==[1,2,5] and d['E']==[2,4])
                assert detail['all_alphabet_excluded'] and detail['mandatory_clique_cuts']
    names=[Path(__file__).name,'PROOF.md#problem4-b1-d125-exclusion','PROOF.md#problem4-d125-fourth-rows','PROOF.md#problem4-d125-row-normalization',
        'd125_fourth_rows_audit.json','b1_c14_nonsingleton_fourth_inventory.json',
        'b1_c14_nonsingleton_fourth_audit.json','PROOF.md#problem4-b1-c14-nonsingleton-d-fourth',
        'small_first_third_inventory.json','small_first_third_audit.json','PROOF.md#problem4-small-first-third-admission']
    report=dict(status='pass',parameter=[13,9,1],B=[0],C=[1,4],D=[1,2,5],
        whole_binary_third_excluded=True,excluded_third_id=third['id'],
        removed_original_third_pairs=3,excluded_D_labels=8,complete_fourth_geometries=5,
        complete_E_labels=29,new_actual_row_fourth_geometries=2,new_actual_row_fourth_pairs=12,
        new_complete_representative_pairs_per_implementation=7164000,
        remaining_binary_E=[],unrestricted_remaining_E=summary['remaining_unrestricted_E'],
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Whole binary D125 third type excluded. Unrestricted D125 and other D/joint types remain. No exact F value or alphabet separation.')
    (ROOT/'b1_d125_composition_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'}),flush=True)

if __name__=='__main__':main()
