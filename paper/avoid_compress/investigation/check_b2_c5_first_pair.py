"""Independent unfiltered pair coverage, literal maps and rational flag trees.

Imports only independent checkers. This QA result is not an accepted
frontier update or a claim about either F value.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
from check_c1_word_staircase import literal_pool,check_tree
from check_b3_staircase import permute_mask
PAIRS=list(combinations(range(13),2))
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    scope=read('b2_c5_first_pair_inventory.json');frozen=read('b2_c5_first_pair_scope.json');baseline=read(frozen['baseline']);cp=read(frozen['checkpoint'])
    assert scope['status']=='complete_necessary_exclusion_inventory' and scope['parameter']==frozen['parameter']==[13,9,1]
    assert sha(ROOT/frozen['baseline'])==cp['source_sha256']['active_research.json']
    for obj in (scope,frozen,read('b1_b2_inverse_union_audit.json')):
        for n,h in obj['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert read('b1_b2_inverse_union_audit.json')['status']=='pass'
    name=scope['id'];native=next(z for z in read('b1_b2_inverse_union_inventory.json')['records'] if z['id']==name)
    z=next(z for z in read('small_first_third_inventory.json')['records'] if z['id']==name)
    B,C,D=map(set,(z['B'],z['C'],z['D']));H,A={0,1,2},{3}
    selected={c['P1_mask']:c for c in native['records'] if c['reason']=='retained_overapproximation'};assert len(selected)==4
    assert [c['P1_mask'] for c in scope['classes']]==sorted(selected)
    frames={};expected=[]
    for c in scope['classes']:
        G=set(map(tuple,selected[c['P1_mask']]['G']));F=[set(S) for S in combinations(range(13),9) if 3 in S and all(len(set(S)&X)==1 for X in (B,C,D)) and not any(set(e)<=set(S) for e in G)]
        assert c['G']==selected[c['P1_mask']]['G'] and c['frames']==[sorted(S) for S in F]
        frames[c['P1_mask']]=F
        expected.extend((c['P1_mask'],i,j) for i in range(len(F)) for j in range(len(F)) if i!=j)
    assert len(expected)==12320
    assert [(t['P1_mask'],*t['pair']) for t in scope['transports']]==expected
    representatives={(p['P1_mask'],tuple(p['basis'])):p for p in scope['prefixes']};assert len(representatives)==64
    multiplicities=Counter();checked_perms=set()
    for t in scope['transports']:
        p=tuple(t['permutation']);assert set(p)==set(range(13));g=t['P1_mask'];target=t['target_P1'];basis=tuple(t['basis'])
        assert permute_mask(g,p)==target and target in selected
        if p not in checked_perms:
            for X in (H,A,B,C,D,set(native['mandatory'])):assert {p[q] for q in X}==X
            for f in native['fields']:
                for key in ('preA','preB','preC'):assert {p[q] for q in f[key]}==set(f[key])
                assert sorted(permute_mask(m,p) for m in f['compatible_kernel_masks'])==f['compatible_kernel_masks']
            checked_perms.add(p)
        assert {tuple(sorted((p[u],p[v]))) for u,v in selected[g]['G']}==set(map(tuple,selected[target]['G']))
        for old,new in zip(selected[g]['field_kernel_masks'],selected[target]['field_kernel_masks']):assert sorted(permute_mask(m,p) for m in old)==new
        assert tuple(sum(1<<p[q] for q in frames[g][i]) for i in t['pair'])==basis and (target,basis) in representatives
        multiplicities[(target,basis)]+=1
    assert set(multiplicities)==set(representatives)
    total=Counter();bindings={};maximum_depth=0
    for index,prefix in enumerate(scope['prefixes']):
        assert multiplicities[(prefix['P1_mask'],tuple(prefix['basis']))]==prefix['multiplicity']
        data=prefix
        c=selected[prefix['P1_mask']];parent=dict(mandatory=native['mandatory'],required_P3_edges=c['G'],fields=native['fields']);view=dict(extra_pair=None,field_kernel_masks=c['field_kernel_masks'])
        rows,G=literal_pool(parent,view,prefix['basis'],B,C,D);assert len(rows)==data['letter_count']
        stats=check_tree(rows,prefix['basis'],B,C,D,G,data['tree']);assert stats==data['tree_stats']
        assert hashlib.sha256(json.dumps([list(r) for r,f in rows],separators=(',',':')).encode()).hexdigest()==data['rows_sha256']
        assert hashlib.sha256(json.dumps([f for r,f in rows],separators=(',',':')).encode()).hexdigest()==data['flags_sha256']
        total.update(stats);total['prefixes']+=1;total['literal_letters']+=len(rows)
        maximum_depth=max(maximum_depth,max(int(k[6:]) for k,v in stats.items() if k.startswith('depth_') and v))
        if (index+1)%8==0:print('independent prefixes',index+1,'/64',flush=True)
    assert total['prefixes']==64 and maximum_depth<11
    assert dict(total)==scope['stats'] and maximum_depth==5 and total.get('word_rounds',0)==0
    cells=[{q for q in set(range(13))-A if tuple(q in X for X in (H,B,C))==signature} for signature in __import__('itertools').product((False,True),repeat=3)]
    labels=0
    for size in range(1,5):
        for item in combinations(sorted(set(range(13))-A),size):
            R=set(item)
            if len(R-H)>1 or [len(R&cell) for cell in cells]!=z['cell_signature']:continue
            p={3:3}
            for cell in cells:p.update(zip(sorted(cell&D)+sorted(cell-D),sorted(cell&R)+sorted(cell-R)))
            assert set(p)==set(p.values())==set(range(13)) and all({p[q] for q in X}==X for X in (H,A,B,C)) and {p[q] for q in D}==R
            original=[S for S in (set(X) for X in combinations(range(13),9)) if 3 in S and all(len(S&Y)==1 for Y in (B,C,D))]
            target=[S for S in (set(X) for X in combinations(range(13),9)) if 3 in S and all(len(S&Y)==1 for Y in (B,C,R))]
            assert {frozenset(p[q] for q in S) for S in original}==set(map(frozenset,target));labels+=1
    assert labels==z['labelled_D']==z['orbit_size']
    j=baseline['joint_fiber_cases'];inv=read('small_first_third_inventory.json')['records'];cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],baseline['two_cover_unique_kernel_profile_cuts'],baseline['two_cover_exact_kernel_profile_cuts'],baseline['three_cover_atom_kernel_profile_cuts']]:
        for record in array:cuts.setdefault(record['id'],set()).update(map(tuple,record['removed_parent_pairs']))
    ug=[x for x in inv if x['joint_id'] not in j['unrestricted_excluded_orbits'] and x['id'] not in j['unrestricted_additional_small_first_third_exclusions'] and x['id']!=name]
    bg=[x for x in inv if x['joint_id'] not in j['binary_excluded_orbits'] and x['id'] not in j['binary_additional_small_first_third_exclusions'] and x['id']!=name]
    profiles=lambda x:set(map(tuple,x['binary_profile_pairs']))-cuts.get(x['id'],set())
    assert (len(ug),len(bg),sum(bool(profiles(x)) for x in bg))==(111,98,94)
    assert any(x['joint_id']==z['joint_id'] for x in ug) and any(x['joint_id']==z['joint_id'] and profiles(x) for x in bg)
    sources=[Path(__file__).name,'b2_c5_first_pair_inventory.json','b2_c5_first_pair_scope.json','B2_C5_FIRST_PAIR_STAIRCASE_EXCLUSION.md',frozen['baseline'],frozen['checkpoint'],'check_c1_word_staircase.py','check_b3_staircase.py','b1_b2_inverse_union_inventory.json','b1_b2_inverse_union_audit.json','small_first_third_inventory.json','common_block_profiles_audit.json','LOCAL_EQUALITY_FLAG.md','local_equality_flag_audit.json']
    result=dict(status='pass',parameter=[13,9,1],id=name,global_classes=4,labelled_first_pairs=12320,canonical_prefixes=64,tree_counts=dict(total),maximum_basis_depth=5,labelled_D_transports=labels,new_excluded_third_ids=[name],new_unrestricted_joint_exclusions=[],new_binary_joint_exclusions=[],remaining_unrestricted_geometries=111,remaining_binary_geometries=98,remaining_binary_typed=94,remaining_binary_profiles=sum(len(profiles(x)) for x in bg),remaining_binary_joints=18,remaining_unrestricted_joints=20,source_sha256={n:sha(ROOT/n) for n in sources},scope=frozen['scope'])
    (ROOT/'b2_c5_first_pair_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
