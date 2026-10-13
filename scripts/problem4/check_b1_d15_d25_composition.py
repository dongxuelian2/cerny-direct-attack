"""Literal complete fourth coverage for whole binary D15/D25 negatives."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parent=read('b1_c14_nonsingleton_fourth_audit.json')
    inventory=read('b1_c14_nonsingleton_fourth_inventory.json')
    scan=read('d15_d25_fourth_rows_audit.json')
    assert parent['status']==scan['status']=='pass'
    assert scan['all_D15_D25_binary_fourth_survivors_excluded']
    assert scan['all_parent_fourth_pairs']==98 and scan['raw_individual_rows']==13426560
    assert scan['pointwise_transports_checked']==2784960
    assert scan['checked_representative_pairs_per_implementation']==813607200
    for audit in (parent,scan):
        for n,h in audit['source_sha256'].items():assert sha(ROOT/n)==h,(n,h)
    thirds=read('small_first_third_inventory.json')['records'];records=[]
    for D,identifier,total,geoms,labels in (([1,5],'b1_in_c3_third4',42,8,32),([2,5],'b1_in_c3_third6',56,7,31)):
        t=next(z for z in thirds if z['id']==identifier)
        assert t['D']==D and t['labelled_D']==8
        assert len(t['binary_profile_pairs'])==(3 if D==[1,5] else 14)
        geometries=[z for z in inventory['records'] if z['D']==D]
        summary=next(z for z in parent['counts'] if z['D']==D)
        assert len(geometries)==geoms and sum(z['labelled_E'] for z in geometries)==labels
        assert summary['remaining_binary_field_pairs']==total
        actual=[z['E'] for z in geometries if z['E'] not in summary['all_alphabet_excluded_E']]
        assert actual==summary['remaining_binary_E']==summary['remaining_unrestricted_E']
        coverage=[];count=0
        for z in geometries:
            assert [p['original_third_rows'] for p in z['pairs']]==t['binary_profile_pairs']
            pairs=[xy for p in z['pairs'] for xy in p['fourth_field_pairs']]
            if z['E'] in summary['all_alphabet_excluded_E']:
                proof=next(r for r in parent['records'] if r['D']==D and r['E']==z['E'])
                assert proof['all_alphabet_excluded']
                if D==[1,5]:
                    assert z['E']==[2] and proof['known_compression_cover_cut'] and len(pairs)==9
                else:
                    assert not pairs and all(not p['admissible_tuples'] for p in proof['individual_tuple_controls'])
                coverage.append(dict(E=z['E'],reason='parent arbitrary-alphabet proof',formal_binary_pairs=len(pairs)))
            else:
                r=next(r for r in scan['complete_pair_scans'] if r['D']==D and r['E']==z['E'])
                assert r['zero_candidates_both_algorithms'] and r['parent_field_pairs']==len(pairs)
                assert r['Boolean_companions']==z['additional_covered_fibers'];count+=len(pairs)
                coverage.append(dict(E=z['E'],reason='complete two-implementation actual row negative',formal_binary_pairs=len(pairs)))
        assert count==total
        records.append(dict(D=D,excluded_third_id=identifier,removed_original_third_pairs=len(t['binary_profile_pairs']),
            complete_fourth_geometries=geoms,complete_E_labels=labels,checked_actual_row_fourth_pairs=count,
            unrestricted_remaining_E=summary['remaining_unrestricted_E'],coverage=coverage))
    names=[Path(__file__).name,'PROOF.md#problem4-b1-d15-d25-exclusion','PROOF.md#problem4-d15-d25-row-cover','d15_d25_fourth_rows_audit.json',
        'b1_c14_nonsingleton_fourth_inventory.json','b1_c14_nonsingleton_fourth_audit.json',
        'PROOF.md#problem4-b1-c14-nonsingleton-d-fourth','small_first_third_inventory.json','small_first_third_audit.json','PROOF.md#problem4-small-first-third-admission']
    result=dict(status='pass',parameter=[13,9,1],B=[0],C=[1,4],whole_binary_D15_D25_excluded=True,
        excluded_third_types=records,removed_original_third_pairs=17,complete_fourth_geometries=15,
        complete_E_labels=63,checked_actual_row_fourth_geometries=10,checked_actual_row_fourth_pairs=98,
        new_complete_representative_pairs_per_implementation=813607200,
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Whole binary D15,D25 conditional exclusions only. Unrestricted survivors and other joint types remain; no exact F value.')
    (ROOT/'b1_d15_d25_composition_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','excluded_third_types')}))
if __name__=='__main__':main()
