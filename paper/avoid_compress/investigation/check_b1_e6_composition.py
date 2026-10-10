"""Exact set coverage composing the complete conditional binary E6 cut."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent

def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def sha(name):return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()

def main():
    names=['b1_fifth_audit.json','b1_sixth_audit.json','b1_e6_f2_audit.json','b1_e6_fifth_pair_audit.json',
        'b1_e6_overlap_fifth_audit.json','b1_g28_rows_audit.json','b1_f27_g8_rows_audit.json',
        'b1_f27_paired_g_seventh_audit.json','b1_f27_paired_g_rows_audit.json']
    for name in names:
        z=read(name);assert z['status']=='pass' and z['parameter']==[13,9,1],name
    fifth=read('b1_fifth_inventory.json')['records'];sixth=read('b1_sixth_inventory.json')['records']
    fourth=read('b1_partial_cover_fourth_inventory.json')['records']
    E6=next(z for z in fourth if z['E']==[6]);E26=next(z for z in fourth if z['E']==[2,6])
    F27_G={tuple(z['G']) for z in sixth if z['E']==[6] and z['F']==[2,7]}
    crossed=[z for z in read('b1_sixth_audit.json')['arbitrary_alphabet_crossed_fiber_exclusions']
        if z['E']==[6] and z['F']==[2,7]]
    assert len(crossed)==4 and all(z['individual_preimage_tuples']==720 and z['disjoint_tuples']==0 for z in crossed)
    assert read('b1_f27_g8_rows_audit.json')['whole_binary_E6_F27_G8_excluded']
    assert read('b1_f27_paired_g_rows_audit.json')['whole_binary_G18_G28_excluded']
    assert {tuple(z['G']) for z in crossed}|{(8,),(1,8),(2,8)}==F27_G and len(F27_G)==7
    E6_F={tuple(z['F']) for z in fifth if z['E']==[6]}
    excluded={(read('b1_e6_f2_audit.json')['excluded_fifth'][0],)}
    excluded|={tuple(z['F']) for z in read('b1_e6_fifth_pair_audit.json')['excluded']}
    excluded|={tuple(z) for z in read('b1_e6_overlap_fifth_audit.json')['excluded_F']}
    assert read('b1_g28_rows_audit.json')['whole_binary_E6_F7_excluded']
    excluded|={(7,),(2,7)}
    assert excluded==E6_F and len(E6_F)==7
    eliminated_fifth_pairs={(tuple(z['F']),tuple(xy)) for z in fifth if z['E']==[6] for p in z['pairs'] for xy in p['fifth_field_pairs']}
    E6fourth={tuple(xy) for p in E6['pairs'] for xy in p['fourth_field_pairs']}
    assert len(E6fourth)==41 and len(eliminated_fifth_pairs)==414
    represented_E6fourth={tuple(p['original_fourth_rows']) for z in fifth if z['E']==[6] for p in z['pairs'] if p['fifth_field_pairs']}
    assert represented_E6fourth==E6fourth
    remaining=[z for z in fifth if z['E']==[2,6] and z['F'] in ([7],[1,7],[2,7])]
    assert [z['F'] for z in remaining]==read('b1_fifth_audit.json')['remaining_E26_fifth_geometry']
    assert len(remaining)==3 and sum(z['labelled_F'] for z in remaining)==18
    assert sum(len(p['fifth_field_pairs']) for z in remaining for p in z['pairs'])==161
    E26fourth={tuple(xy) for p in E26['pairs'] for xy in p['fourth_field_pairs']}
    coverage4={tuple(p['original_fourth_rows']) for z in remaining for p in z['pairs'] if p['fifth_field_pairs']}
    coverage3={tuple(p['original_third_rows']) for z in remaining for p in z['pairs'] if p['fifth_field_pairs']}
    assert len(E26fourth)==41 and coverage4==E26fourth and len(coverage3)==14
    selected=[z for z in sixth if z['E']==[2,6] and z['F']==[7] and z['G'] in ([8],[1,8],[2,8])]
    assert len(selected)==3 and sum(z['labelled_G'] for z in selected)==15
    assert sum(len(p['sixth_field_pairs']) for z in selected for p in z['pairs'])==443
    assert len({tuple(p['original_fifth_rows']) for z in selected for p in z['pairs'] if p['sixth_field_pairs']})==122
    names+=['b1_fifth_inventory.json','b1_sixth_inventory.json','b1_partial_cover_fourth_inventory.json',
        'B1_FIFTH_ENTRANCE.md','B1_SIXTH_ENTRANCE.md','B1_PARTIAL_COVER_FOURTH.md','B1_E6_F2_EXCLUSION.md',
        'B1_E6_F12_F127_EXCLUSION.md','B1_E6_F17_EXCLUSION.md','B1_E6_F24_EXCLUSION.md',
        'B1_E6_F7_EXCLUSION.md','B1_E6_F27_G8_EXCLUSION.md','B1_F27_PAIRED_G_SEVENTH.md',
        'B1_E6_F27_PAIRED_G_EXCLUSION.md','B1_E6_EXCLUSION.md',Path(__file__).name]
    assert len(names)==len(set(names))
    result=dict(status='pass',parameter=[13,9,1],alphabet='binary only',whole_binary_E6_F27_excluded=True,
        whole_binary_E6_fourth_excluded=True,excluded_E=[6],complete_F27_G=[list(x) for x in sorted(F27_G)],
        complete_E6_F=[list(x) for x in sorted(E6_F)],eliminated_raw_E6_fifth_pairs=414,
        removed_E6_fourth_field_pairs=41,excluded_E_labels=E6['labelled_E'],
        remaining_binary_E=[[2,6]],remaining_fourth_geometries=1,remaining_fourth_labels=E26['labelled_E'],
        remaining_fourth_field_pairs=41,remaining_fifth_geometries=3,remaining_fifth_labels=18,remaining_fifth_field_pairs=161,
        remaining_selected_sixth_geometries=3,remaining_selected_sixth_labels=15,remaining_selected_sixth_field_pairs=443,
        all_original_third_pairs_retained=14,all_original_E26_fourth_pairs_retained=41,
        complete_new_paired_G_pairs_per_implementation=119664,
        source_sha256={name:sha(name) for name in names},
        scope='Complete set-by-set composition of new paired-G negatives and explicitly included older conditional exclusion premises. Excludes binary E6/F27 then all seven E6 fifths and entire E6 fourth. Does not rerun all earlier proofs here. No unrestricted E6, whole D5/third/joint or extremal F value or numerical separation.')
    (ROOT/'b1_e6_composition_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(dict(status='pass',whole_binary_E6_excluded=True,remaining_fourth_pairs=41,
        remaining_fifth_pairs=161,remaining_selected_sixth_pairs=443)),flush=True)
if __name__=='__main__':main()
