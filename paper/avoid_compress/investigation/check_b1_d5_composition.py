"""Exact complete-branch composition for binary B0/C14/D5 at n13."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
def sha(name):return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()

def main():
    audits=['b1_partial_cover_fourth_audit.json','b1_partial_cover_fourth_pair_exclusion_audit.json',
        'b1_partial_cover_e16_audit.json','b1_partial_cover_e24_audit.json',
        'b1_e6_composition_audit.json','b1_fifth_audit.json','b1_sixth_audit.json',
        'b1_e26_overlap_sixth_audit.json','b1_e26_overlap_rows_audit.json',
        'b1_e26_f7_seventh_audit.json','b1_e26_f7_seventh_rows_audit.json']
    for name in audits:
        data=read(name);assert data['status']=='pass' and data['parameter']==[13,9,1],name
    fourth=read('b1_partial_cover_fourth_inventory.json')['records']
    fifth=read('b1_fifth_inventory.json')['records']
    sixth=read('b1_sixth_inventory.json')['records']
    third=next(z for z in read('small_first_third_inventory.json')['records'] if z['id']=='b1_in_c3_third2')
    assert (third['B'],third['C'],third['D'])==([0],[1,4],[5]) and third['labelled_D']==8
    original_third={tuple(xy) for xy in third['binary_profile_pairs']};assert len(original_third)==14
    E26=next(z for z in fourth if z['E']==[2,6])
    F7=next(z for z in fifth if z['E']==[2,6] and z['F']==[7])
    Gset={tuple(z['G']) for z in sixth if z['E']==[2,6] and z['F']==[7]}
    crossed=[z for z in read('b1_sixth_audit.json')['arbitrary_alphabet_crossed_fiber_exclusions']
        if z['E']==[2,6] and z['F']==[7]]
    assert len(crossed)==4 and all(z['individual_preimage_tuples']==720 and z['disjoint_tuples']==0 for z in crossed)
    rows=read('b1_e26_f7_seventh_rows_audit.json')
    assert rows['whole_binary_G8_G18_G28_excluded'] and rows['checked_retained_pairs_per_implementation']==5689728
    assert all(z['zero_reverse_candidates'] and z['zero_forward_survivors'] for z in rows['complete_pair_scans'])
    assert {tuple(z['G']) for z in crossed}|{(8,),(1,8),(2,8)}==Gset and len(Gset)==7
    F7pairs={tuple(xy) for p in F7['pairs'] for xy in p['fifth_field_pairs']}
    coveredF7={tuple(p['original_fifth_rows']) for z in sixth if z['E']==[2,6] and z['F']==[7]
        for p in z['pairs'] if p['sixth_field_pairs']}
    assert F7pairs==coveredF7 and len(F7pairs)==122
    Fset={tuple(z['F']) for z in fifth if z['E']==[2,6]}
    fivecuts={tuple(z['F']) for z in read('b1_fifth_audit.json')['arbitrary_alphabet_crossed_fiber_exclusions']}
    assert read('b1_e26_overlap_rows_audit.json')['whole_binary_F17_F27_excluded']
    assert fivecuts|{(7,),(1,7),(2,7)}==Fset and len(Fset)==7
    E26pairs={tuple(xy) for p in E26['pairs'] for xy in p['fourth_field_pairs']}
    coveredE26={tuple(p['original_fourth_rows']) for z in fifth if z['E']==[2,6]
        for p in z['pairs'] if p['fifth_field_pairs']}
    assert E26pairs==coveredE26 and len(E26pairs)==41
    known=read('b1_partial_cover_fourth_audit.json')['common_fourth_geometry']
    assert known['excluded_fourth_fiber']==[2]
    Ecuts={tuple(known['excluded_fourth_fiber'])}
    Ecuts|={tuple(x) for x in read('b1_partial_cover_fourth_pair_exclusion_audit.json')['excluded_E']}
    for name in ('b1_partial_cover_e16_audit.json','b1_partial_cover_e24_audit.json'):
        data=read(name);assert data['binary_only'] and data['removed_fourth_field_pairs']==6
        Ecuts.add(tuple(data['E']))
    assert read('b1_e6_composition_audit.json')['whole_binary_E6_fourth_excluded']
    Ecuts|={(6,),(2,6)}
    assert Ecuts=={tuple(z['E']) for z in fourth} and len(Ecuts)==7
    coveredD5={tuple(p['original_rows']) for z in fourth for p in z['pairs'] if p['fourth_field_pairs']}
    assert coveredD5==original_third
    unrestricted=read('b1_e26_f7_seventh_audit.json')['records']
    kept=[z for z in unrestricted if not z['all_alphabet_excluded']]
    assert len(kept)==9 and sum(z['labels'] for z in kept)==33
    assert known['remaining_geometric_orbits']==6 and known['remaining_labelled_E_choices']==30
    names=audits+['b1_partial_cover_fourth_inventory.json','b1_fifth_inventory.json','b1_sixth_inventory.json',
        'small_first_third_inventory.json','B1_PARTIAL_COVER_FOURTH.md','B1_PARTIAL_COVER_E16_EXCLUSION.md',
        'B1_PARTIAL_COVER_E24_EXCLUSION.md','B1_E6_EXCLUSION.md','B1_FIFTH_ENTRANCE.md','B1_SIXTH_ENTRANCE.md',
        'B1_E26_OVERLAP_EXCLUSION.md','B1_E26_F7_SEVENTH.md','B1_E26_F7_SEVENTH_ROWS.md','B1_D5_EXCLUSION.md',Path(__file__).name]
    result=dict(status='pass',parameter=[13,9,1],alphabet='binary only',
        excluded_third_id=third['id'],B=third['B'],C=third['C'],D=third['D'],excluded_third_labels=8,
        whole_binary_E26_F7_excluded=True,whole_binary_E26_fourth_excluded=True,whole_binary_D5_third_excluded=True,
        complete_F7_G=[list(x) for x in sorted(Gset)],complete_E26_F=[list(x) for x in sorted(Fset)],
        complete_D5_E=[list(x) for x in sorted(Ecuts)],removed_F7_fifth_pairs=122,
        removed_E26_fourth_pairs=41,removed_D5_third_pairs=14,remaining_binary_D5_fourth_pairs=0,
        complete_new_coupled_pairs_per_implementation=5689728,unrestricted_fourth_types=6,unrestricted_fourth_labels=30,
        unrestricted_E26_F7_seventh_types=9,unrestricted_E26_F7_seventh_labels=33,
        source_sha256={name:sha(name) for name in names},
        scope='Literal all-level set/pair coverage composes new seventh negatives and explicitly included older exclusion premises. Excludes the entire binary singleton-D5 third geometry and its eight ordinary labels, not the b1_in_c3 joint or any unrestricted third. No exact F value or numerical alphabet separation.')
    (ROOT/'b1_d5_composition_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:result[k] for k in ('status','whole_binary_D5_third_excluded','removed_D5_third_pairs','complete_new_coupled_pairs_per_implementation')}))
if __name__=='__main__':main()
