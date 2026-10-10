"""Complete current application of the uniform common-block lemma."""
from pathlib import Path
from itertools import combinations
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));H={0,1,2}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    base=read('common_block_profile_base.json')
    assert sha(ROOT/base['historical_checkpoint'])==base['historical_checkpoint_sha256']
    lemma=read('common_collapsing_block_audit.json');assert lemma['status']=='pass'
    fourth=read('b1_c4_fourth_audit.json');assert fourth['status']=='pass' and fourth['C']==[4]
    for a in (lemma,fourth):
        for n,h in a['source_sha256'].items():assert sha(ROOT/n)==h,n
    data=read('small_first_third_inventory.json')
    remain=[t for t in data['records'] if t['joint_id'] not in base['binary_excluded_joint_orbits']
        and t['id'] not in base['binary_excluded_third_orbits'] and t['binary_profile_pairs']]
    assert len(remain)==base['remaining_binary_third_orbits']==146
    assert sum(len(t['binary_profile_pairs']) for t in remain)==base['remaining_binary_profile_pairs']==744
    allsets=[set(S) for S in combinations(range(13),9) if 3 in S]
    records=[];remaining_pairs=0
    for t in remain:
        B,C,D=map(set,(t['B'],t['C'],t['D']));bad=[];core=[];cover=[]
        if len(C)==1 and len(D)>=2 and C.isdisjoint(D):
            forms=[S for S in allsets if all(len(S&X)==1 for X in (B,C,D))]
            assert len(forms)==t['feasible_nine_sets']
            common=set.intersection(*forms);K=H-common
            if K<=D:
                bad=[xy for xy in t['binary_profile_pairs'] if all(set(t['rows'][i]['preC'])==D for i in xy)]
                core=sorted(common);cover=sorted(K)
        good=[xy for xy in t['binary_profile_pairs'] if xy not in bad]
        assert good
        remaining_pairs+=len(good)
        if bad:records.append(dict(id=t['id'],B=t['B'],C=t['C'],D=t['D'],mandatory_through_eight=core,
            remaining_P5_cover=cover,removed_parent_pairs=bad,remaining_parent_pairs=good,labels=t['labelled_D']))
    expected=['b1_out_c1_third5','b1_out_c2_third3','b1_out_c2_third5','b1_in_c1_third3','b1_in_c1_third5']
    assert [t['id'] for t in records]==expected
    badpairs=[[1,7],[3,5],[3,7],[5,7],[7,7]]
    assert all(t['removed_parent_pairs']==badpairs and len(t['remaining_parent_pairs'])==9 for t in records)
    assert remaining_pairs==719
    inventory=read('b1_c4_fourth_inventory.json');filtered=[]
    for z in inventory['records']:
        summary=next(s for s in fourth['records'] if s['D']==z['D'] and s['E']==z['E'])
        if summary['all_alphabet_excluded']:continue
        p=next((r for r in records if r['B']==[0] and r['C']==[4] and r['D']==z['D']),None)
        removed=p['removed_parent_pairs'] if p else []
        before=[(r['original_third_rows'],xy) for r in z['pairs'] for xy in r['fourth_field_pairs']]
        after=[(old,xy) for old,xy in before if old not in removed]
        filtered.append(dict(D=z['D'],E=z['E'],labels=z['labelled_E'],before=len(before),after=len(after),
            removed=len(before)-len(after),surviving_field_pairs=[xy for old,xy in after],all_companions_retained=True))
    assert len(filtered)==15 and sum(t['labels'] for t in filtered)==111
    assert sum(t['before'] for t in filtered)==359
    names=[Path(__file__).name,'COMMON_BLOCK_SINGLETON_C_PROFILES.md','COMMON_COLLAPSING_BLOCK_TRAP.md',
        'common_collapsing_block_audit.json','common_block_profile_base.json',base['historical_checkpoint'],
        'small_first_third_inventory.json','small_first_third_audit.json','SMALL_FIRST_THIRD_ADMISSION.md',
        'b1_c4_fourth_inventory.json','b1_c4_fourth_audit.json','B1_C4_FOURTH_SPACE.md',
        'MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md']
    result=dict(status='pass',parameter=[13,9,1],complete_original_remaining_third_geometries=146,
        original_remaining_binary_pairs=744,newly_excluded_binary_profile_pairs=25,
        remaining_binary_third_geometries=146,remaining_binary_profile_pairs=719,profile_cuts=records,
        b1_c4_fourth_after_common_block=filtered,
        original_b1_c4_admitted_fourth_pairs=359,remaining_b1_c4_admitted_fourth_pairs=sum(r['after'] for r in filtered),
        unrestricted_geometric_counts_unchanged=True,source_sha256={n:sha(ROOT/n) for n in names},
        scope='Complete current conditional singleton-C profile cuts from uniform pair-trap lemma; no entire joint/third, exact F value or numerical alphabet separation.')
    (ROOT/'common_block_profiles_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','profile_cuts','b1_c4_fourth_after_common_block')}),flush=True)
if __name__=='__main__':main()
