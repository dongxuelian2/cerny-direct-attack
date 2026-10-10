"""Record the alphabet-independent joint and third-profile exclusions."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def main():
    old=read('AUXILIARY_AUDIT_20261009_17.json');name='compression_cover_floor_audit.json';new=read(name)
    audits=old['passed_audits']+[name];sources=set(audits)
    for item in audits:
        data=read(item);assert data['status']=='pass'
        for source,digest in data['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source)
    assert new['admission']['excluded_joint']=='b1_in_c2'
    assert new['third_intersection_controls']['excluded_third_orbits']==11
    assert new['third_intersection_controls']['complete_labelled_D_choices']==1482
    active=read('active_research.json');assert active['workers']==[]
    joint=active['joint_fiber_cases'];oldj=set(joint['binary_excluded_orbits']);oldu=set(joint['unrestricted_excluded_orbits'])
    oldthird=set(joint['binary_additional_small_first_third_exclusions']);cuts=set(new['third_intersection_controls']['excluded_profiles'])
    assert len(oldj)==19 and not oldu and joint['binary_remaining_orbits']==24
    records=read('small_first_third_inventory.json')['records']
    before=[v for v in records if v['joint_id'] not in oldj and v['id'] not in oldthird and v['binary_profile_pairs']]
    assert len(before)==161 and sum(len(v['binary_profile_pairs']) for v in before)==884
    newj=oldj|{'b1_in_c2'};newu=oldu|{'b1_in_c2'};newthird=oldthird|cuts
    kept=[v for v in records if v['joint_id'] not in newj and v['id'] not in newthird and v['binary_profile_pairs']]
    geometric_joint_only=[v for v in records if v['joint_id'] not in newj]
    geometric_all=[v for v in records if v['joint_id'] not in newj and v['id'] not in newthird]
    unrestricted=[v for v in records if v['joint_id'] not in newu and v['id'] not in cuts]
    assert len(kept)==152 and sum(len(v['binary_profile_pairs']) for v in kept)==784
    assert len(geometric_joint_only)==205 and len(geometric_all)==197 and len(unrestricted)==224
    additional=[v for v in records if v['id'] in cuts and v['joint_id']!='b1_in_c2']
    assert len(additional)==8 and sum(bool(v['binary_profile_pairs']) for v in additional)==6
    assert sum(len(v['binary_profile_pairs']) for v in additional)==58
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    prefix='compression_cover_floor';readme='COMPRESSION_COVER_FLOOR_CERTIFICATE_README.md'
    contents={filename:(ROOT/filename).read_bytes() for filename in set(new['source_sha256'])|{name}}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n' for filename,value in sorted(contents.items())).encode('utf-8')
    assert len(contents)==16
    dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert len(archive.namelist())==16
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_compression_cover_floor_package.py';receipt='compression_cover_floor_package_reproduction.json'
    subprocess.run([sys.executable,str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['reproduced_audit_byte_identical'] and reproduction['reproduced_inventory_byte_identical']
    joint['binary_excluded_orbits']=sorted(newj);joint['binary_remaining_orbits']=23
    joint['unrestricted_excluded_orbits']=sorted(newu);joint['unrestricted_remaining_orbits']=42
    joint['binary_additional_small_first_third_exclusions']=sorted(newthird)
    joint['unrestricted_additional_small_first_third_exclusions']=sorted(cuts)
    joint['compression_cover_floor_audit']=name
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['COMPRESSION_COVER_FLOOR.md']))
    active['compression_cover_floor']=dict(parameter=[13,9,1],proof='COMPRESSION_COVER_FLOOR.md',audit=name,
        known_primary_source='compression_cover_primary_source.json',h1_through10_floors=[1,1,2,2,2,3,3,3,3,4],
        excluded_joint='b1_in_c2',additional_third_profiles=[v['id'] for v in additional],
        alphabet='arbitrary finite',scope='Existing compression-bound corollary and protected-image stripping; no new F value')
    small=active['small_first_third_admission'];small['remaining_geometric_after_joint_exclusions']=205
    small['remaining_geometric_after_joint_and_third_exclusions']=197
    small['remaining_binary_typed_orbits']=152;small['remaining_binary_profile_pairs']=784
    small['unrestricted_remaining_geometric_in_B1_B2_inventory']=224
    small['latest_exclusion_audits']=list(dict.fromkeys(small['latest_exclusion_audits']+[name]))
    active['paper_reference_title_correction_pending']=dict(key='szykula2018',incorrect='Shortest Reset Word',correct='Shortest Reset Words',
        source='compression_cover_primary_source.json',instruction='Correct at the next paper/release rebuild; no mathematical claim changes.')
    active['instruction']='Complete-answer goal active and unachieved. Existing Frankl-Pin compression bounds and protected-image intersections exclude whole b1_in_c2 plus eight extra third geometries for every finite alphabet. Joint23 binary/42 unrestricted; third binary152/784; both extrema[11,12]. B1/B2 unrestricted geometric inventory224, not allB3. Paper/release unchanged; workers terminal.'
    active['general_solver_status']='86 old bounded diagnostics remain uncertified. Complete proofs exclude20 binary joint records, one of them for every finite alphabet, plus eight new all-alphabet third-profile cuts beyond that joint. No full13-state transition scan, F value or numerical alphabet separation is claimed.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_18.json'
    active['next_structural_work']='At(13,9,1), joint23 binary/42 unrestricted remain; binary third152/784. Extend the P4 mandatory-image-intersection/known compression-floor cut to complete B3 third admission; the235 original B1/B2 orbits do not cover B3. Preserve all extra Boolean fibers. Binary B1_in_c3 remains after its D2 exclusion and may reuse the effective two-point H-cover, without importing C2/C3 budgets. Correct the independently verified Szykula2018 bibliography title to plural Reset Words at the next PDF/release rebuild. Never use solver timeouts or retracted edge caps as negatives.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    sources|={'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    result=dict(date='2026-10-09',status='Audited arbitrary-alphabet whole-joint and eight additional third exclusions via known compression bounds',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_17.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,new_all_alphabet_joint_exclusion='b1_in_c2',
        additional_all_alphabet_third_profiles=[v['id'] for v in additional],joint_and_third_controls=new['admission'],
        third_intersection_controls=new['third_intersection_controls'],finite_row_domains=new['complete_small_row_controls'],
        frontier_controls=new['frontier_controls'],random_controls=new['seeded_larger_alphabet_controls'],
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=23,
        unrestricted_remaining_joint_orbits=42,remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_in_B1_B2_inventory=224,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=16,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='No complete answer, F value or numerical alphabet separation. Known compression-theorem corollary with symbolic protected-isolation proof and complete labelled intersections; B3 is outside the235-orbit data. Finite automata controls are not full13-state enumeration.')
    (ROOT/'AUXILIARY_AUDIT_20261009_18.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,certificate_files=16,
        binary_joint=23,unrestricted_joint=42,binary_third=152,earlier_pairs=784,active_workers=0)))
if __name__=='__main__':main()
