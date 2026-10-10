"""Compose the complete binary B1/C3 mixed joint exclusion and checkpoint."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_15.json');name='b1_mixed_c3_singleton_fourth_audit.json';new=read(name)
    audits=old['passed_audits']+[name];sources=set(audits)
    for item in audits:
        data=read(item);assert data['status']=='pass'
        for source,digest in data['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source)
    assert new['immediate_kernel_and_graph_controls']['fourth_field_pairs']==41
    assert new['immediate_kernel_and_graph_controls']['compatible_kernel_pairs']==555
    assert [v['row_assignments'] for v in new['complete_literal_smaller_controls']]==[111168,1272672]
    active=read('active_research.json');assert active['workers']==[]
    joint=active['joint_fiber_cases'];oldj=set(joint['binary_excluded_orbits']);oldthird=set(joint['binary_additional_small_first_third_exclusions'])
    assert len(oldj)==17 and joint['b1_C3_mixed_remaining_D']==[[2,6]]
    assert oldthird=={f'b1_out_c5_third{i}' for i in (1,2,3,4,5,7,8,9,10,11)}
    inventory=read('small_first_third_inventory.json');records=inventory['records']
    before=[v for v in records if v['joint_id'] not in oldj and v['id'] not in oldthird and v['binary_profile_pairs']]
    assert len(before)==164 and sum(len(v['binary_profile_pairs']) for v in before)==915
    last=[v for v in before if v['joint_id']=='b1_out_c5']
    assert len(last)==1 and last[0]['id']=='b1_out_c5_third6' and last[0]['D']==[2,6]
    assert len(last[0]['binary_profile_pairs'])==14
    newj=oldj|{'b1_out_c5'}
    kept=[v for v in records if v['joint_id'] not in newj and v['id'] not in oldthird and v['binary_profile_pairs']]
    geometric=[v for v in records if v['joint_id'] not in newj]
    assert len(kept)==163 and sum(len(v['binary_profile_pairs']) for v in kept)==901 and len(geometric)==210
    jointdata=read('joint_fiber_orbits.json');singleton_C3=[v['id'] for v in jointdata['records'] if len(v['B'])==1 and len(v['C'])==3]
    assert set(singleton_C3)=={'b1_out_c5','b1_out_c6','b1_in_c5'} and set(singleton_C3)<=newj
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    prefix='b1_mixed_c3_singleton_fourth';readme='B1_MIXED_C3_SINGLETON_FOURTH_CERTIFICATE_README.md'
    contents={filename:(ROOT/filename).read_bytes() for filename in set(new['source_sha256'])|{name}}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n'
        for filename,value in sorted(contents.items())).encode('utf-8')
    assert len(contents)==15
    dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert len(archive.namelist())==15
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_b1_mixed_c3_singleton_fourth_package.py';receipt='b1_mixed_c3_singleton_fourth_package_reproduction.json'
    subprocess.run([sys.executable,str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['reproduced_audit_byte_identical'] and reproduction['reproduced_inventory_byte_identical']
    joint['binary_excluded_orbits']=sorted(newj);joint['binary_remaining_orbits']=25
    joint['b1_C3_mixed_remaining_D']=[]
    joint['b1_C3_mixed_third_audits']=list(dict.fromkeys(joint['b1_C3_mixed_third_audits']+['b1_mixed_c3_fourth_audit.json',name]))
    joint['b1_C3_mixed_entire_joint_excluded']=True
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['B1_MIXED_C3_SINGLETON_FOURTH_EXCLUSION.md']))
    active['binary_b1_mixed_disjoint_fourth']['fourth_field_pairs_remaining']=0
    active['binary_b1_mixed_disjoint_fourth']['original_pairs_remaining']=0
    active['binary_b1_mixed_disjoint_fourth']['singleton_exclusion_proof']='B1_MIXED_C3_SINGLETON_FOURTH_EXCLUSION.md'
    active['binary_b1_mixed_disjoint_fourth']['singleton_exclusion_audit']=name
    active['binary_b1_mixed_disjoint_fourth']['scope']='Complete conditional binary joint exclusion after composing all eleven third profiles; no F value or alphabet separation'
    active['binary_n13_singleton_first_second_fiber_bound']=dict(parameter=[13,9,1],equality_target=12,
        premise='|B|=1',maximum_second_fiber_size=2,excluded_joint_orbits=sorted(singleton_C3),
        proofs=['BINARY_SINGLETON_FIRST_SECOND_COVER.md','B1_MIXED_C3_SINGLETON_FOURTH_EXCLUSION.md'],
        audits=['singleton_first_second_cover_audit.json','b1_mixed_c3_fourth_audit.json',name],
        scope='Conditional binary equality at thirteen states; no unrestricted bound or new F value')
    small=active['small_first_third_admission'];small['remaining_geometric_after_joint_exclusions']=210
    small['remaining_binary_typed_orbits']=163;small['remaining_binary_profile_pairs']=901
    small['latest_exclusion_audits']=joint['b1_C3_mixed_third_audits']
    active['instruction']='Complete-answer goal active and unachieved. All41 singleton-fourth pairs in disjoint B1/C3/D2 are excluded; composing all11 D-profile proofs removes the whole binary joint b1_out_c5. Binary equality with singleton B now requires |C|<=2. Binary joint25/unrestricted43; third admission163/901; both extrema[11,12]. Accepted article/release unchanged; all workers terminal.'
    active['general_solver_status']='86 old bounded diagnostics remain uncertified. Complete separate proofs exclude18 binary joint records, including whole B1/C3 mixed via all11 third profiles. No full13-state transition scan, new F value or numerical alphabet separation is claimed.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_16.json'
    active['next_structural_work']='At(13,9,1), binary joint25/unrestricted43 remain. All singleton-B cases now have |C|<=2. The small covered profile B={0},C={1,2} (b1_in_c4) retains only D={4} and {1,4}, with14 and3 earlier pairs; re-derive its complete common-entrance/Boolean-fiber row cover without applying the C3 kernel budget. Binary third admission163/901. Keep extra Boolean fibers in B2 profiles. No numerical alphabet separation or complete answer yet; do not infer negatives from unchanged solver timeouts.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    sources|={'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    result=dict(date='2026-10-09',status='Audited full binary B1/C3 mixed joint exclusion; no new F value',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_15.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,new_binary_joint_exclusion='b1_out_c5',
        singleton_first_implies_second_size_at_most=2,original_third_pairs_discharged=14,fourth_field_pairs_discharged=41,
        immediate_kernel_controls=new['immediate_kernel_and_graph_controls'],n13_hole_controls=new['complete_n13_hole_controls'],
        literal_control_row_assignments=[111168,1272672],binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=25,unrestricted_remaining_joint_orbits=43,
        remaining_binary_typed_third_orbits=163,remaining_binary_profile_pairs=901,remaining_geometric_after_joint_exclusions=210,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=15,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='No complete answer, new F value or numerical alphabet separation. Complete symbolic conditional binary joint exclusion with full kernel admission and independent graph/row/hole controls, not full13-state transition enumeration.')
    (ROOT/'AUXILIARY_AUDIT_20261009_16.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,certificate_files=15,
        binary_joint=25,unrestricted_joint=43,remaining_binary_typed_third=163,remaining_letter_pairs=901,
        singleton_B_requires_C_at_most=2,active_workers=0)))

if __name__=='__main__':main()
