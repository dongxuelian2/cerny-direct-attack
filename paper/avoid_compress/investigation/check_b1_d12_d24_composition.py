"""Check complete fourth alternatives for whole binary D12/D24 negatives."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parent=read('b1_c14_nonsingleton_fourth_audit.json')
    inventory=read('b1_c14_nonsingleton_fourth_inventory.json')
    scan=read('d12_d24_fourth_rows_audit.json')
    assert parent['status']==scan['status']=='pass'
    assert scan['all_D12_D24_binary_fourth_survivors_excluded']
    assert scan['all_parent_fourth_pairs']==48 and scan['raw_individual_rows']==8305920
    assert scan['pointwise_transports_checked']==4122720
    assert scan['checked_representative_pairs_per_implementation']==162575280
    for audit in (parent,scan):
        for n,h in audit['source_sha256'].items():assert sha(ROOT/n)==h,n
    third=read('small_first_third_inventory.json')['records'];records=[]
    for D,identifier in (([1,2],'b1_in_c3_third3'),([2,4],'b1_in_c3_third5')):
        t=next(z for z in third if z['id']==identifier)
        assert t['D']==D and t['labelled_D']==1
        assert t['binary_profile_pairs']==[[1,5],[2,4],[4,5]]
        geometries=[z for z in inventory['records'] if z['D']==D]
        assert [z['E'] for z in geometries]==([[5],[1,5],[2,5]] if D==[1,2] else [[5],[1,5],[2,5],[1,2,5]])
        assert sum(z['labelled_E'] for z in geometries)==(24 if D==[1,2] else 32)
        summary=next(z for z in parent['counts'] if z['D']==D)
        assert summary['remaining_binary_E']==summary['remaining_unrestricted_E']==[[5],[1,5],[2,5]]
        assert summary['remaining_binary_field_pairs']==24
        total_pairs=0
        for z in geometries:
            assert [p['original_third_rows'] for p in z['pairs']]==t['binary_profile_pairs']
            pairs=[xy for p in z['pairs'] for xy in p['fourth_field_pairs']]
            if z['E']==[1,2,5]:
                assert not pairs and z['E'] in summary['all_alphabet_excluded_E']
                proof=next(r for r in parent['records'] if r['D']==D and r['E']==z['E'])
                assert proof['all_alphabet_excluded'] and proof['mandatory_clique_cuts']
            else:
                r=next(r for r in scan['complete_pair_scans'] if r['D']==D and r['E']==z['E'])
                assert r['zero_candidates_both_algorithms'] and r['parent_field_pairs']==len(pairs)
                assert r['Boolean_companions']==z['additional_covered_fibers'];total_pairs+=len(pairs)
        assert total_pairs==24
        records.append(dict(D=D,excluded_third_id=identifier,removed_original_third_pairs=3,
            complete_fourth_geometries=len(geometries),complete_E_labels=sum(z['labelled_E'] for z in geometries),
            checked_actual_row_fourth_pairs=total_pairs,unrestricted_remaining_E=summary['remaining_unrestricted_E']))
    names=[Path(__file__).name,'B1_D12_D24_EXCLUSION.md','D12_D24_ROW_COVER.md','d12_d24_fourth_rows_audit.json',
        'b1_c14_nonsingleton_fourth_inventory.json','b1_c14_nonsingleton_fourth_audit.json',
        'B1_C14_NONSINGLETON_D_FOURTH.md','small_first_third_inventory.json','small_first_third_audit.json','SMALL_FIRST_THIRD_ADMISSION.md']
    report=dict(status='pass',parameter=[13,9,1],B=[0],C=[1,4],
        whole_binary_D12_D24_excluded=True,excluded_third_types=records,removed_original_third_pairs=6,
        complete_fourth_geometries=7,complete_E_labels=56,checked_actual_row_fourth_geometries=6,
        checked_actual_row_fourth_pairs=48,new_complete_representative_pairs_per_implementation=162575280,
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Whole binary D12,D24 exclusions. Unrestricted E5,E15,E25 and other D/joint types remain; no exact F value or numerical separation.')
    (ROOT/'b1_d12_d24_composition_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
