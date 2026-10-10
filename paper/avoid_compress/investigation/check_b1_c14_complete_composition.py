"""Verify all seven original third types composing a whole binary joint cut."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    files=['small_first_third_audit.json','compression_cover_floor_audit.json','b1_d5_composition_audit.json',
           'b1_d125_composition_audit.json','b1_d12_d24_composition_audit.json','b1_d15_d25_composition_audit.json']
    audits={n:read(n) for n in files}
    for name,a in audits.items():
        assert a['status']=='pass',name
        for n,h in a['source_sha256'].items():assert sha(ROOT/n)==h,(name,n)
    records=[r for r in read('small_first_third_inventory.json')['records'] if r['joint_id']=='b1_in_c3']
    assert len(records)==7 and [r['D'] for r in records]==[[2],[5],[1,2],[1,5],[2,4],[2,5],[1,2,5]]
    assert [len(r['binary_profile_pairs']) for r in records]==[14,14,3,3,3,14,3]
    floor=audits['compression_cover_floor_audit.json']
    assert records[0]['id'] in floor['third_intersection_controls']['excluded_profiles']
    d5=audits['b1_d5_composition_audit.json'];d125=audits['b1_d125_composition_audit.json']
    assert d5['whole_binary_D5_third_excluded'] and d5['removed_D5_third_pairs']==14
    assert d125['whole_binary_third_excluded'] and d125['removed_original_third_pairs']==3
    coverage={records[0]['id']:'compression_cover_floor_audit.json',d5['excluded_third_id']:'b1_d5_composition_audit.json',
              d125['excluded_third_id']:'b1_d125_composition_audit.json'}
    for name,flag in [('b1_d12_d24_composition_audit.json','whole_binary_D12_D24_excluded'),
                      ('b1_d15_d25_composition_audit.json','whole_binary_D15_D25_excluded')]:
        a=audits[name];assert a[flag]
        for z in a['excluded_third_types']:
            assert z['excluded_third_id'] not in coverage
            t=next(t for t in records if t['id']==z['excluded_third_id'])
            assert z['D']==t['D'] and z['removed_original_third_pairs']==len(t['binary_profile_pairs'])
            coverage[t['id']]=name
    assert set(coverage)=={t['id'] for t in records} and sum(len(t['binary_profile_pairs']) for t in records)==54
    names=files+[Path(__file__).name,'B1_C14_COMPLETE_BINARY_EXCLUSION.md','small_first_third_inventory.json',
                 'SMALL_FIRST_THIRD_ADMISSION.md']
    result=dict(status='pass',parameter=[13,9,1],B=[0],C=[1,4],excluded_joint_id='b1_in_c3',
        whole_binary_joint_excluded=True,complete_third_geometries=7,complete_original_third_pairs=54,
        coverage=[dict(id=t['id'],D=t['D'],pairs=len(t['binary_profile_pairs']),audit=coverage[t['id']]) for t in records],
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Entire binary B0/C14 normalized joint at equality12 only; unrestricted and other joint cases remain, both numerical extrema unresolved.')
    (ROOT/'b1_c14_complete_composition_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','coverage')}))
if __name__=='__main__':main()
