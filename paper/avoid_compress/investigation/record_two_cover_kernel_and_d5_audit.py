"""Freeze new two-cover third cuts and two-root D5 fourth cuts."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_15.json';assert not output.exists()
    old=read('AUXILIARY_AUDIT_20261010_14.json')
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['letter_image_short_pair_cover_audit.json','c4_d5_e12_e126_unrestricted_audit.json',
               'singleton_c_d5_e12_e126_transport_audit.json','two_cover_third_unique_kernel_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==98
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        z=read(n);assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    generic,controls,transport,unique=map(read,additions)
    assert generic['complete_n4_map_graph_cover_instances']==262144 and generic['semantic_cover_transfers']==6638520
    assert controls['complete_conditional_individual_rows']==3648
    assert controls['complete_binary_ordered_alphabets_through_n8']==147840
    assert controls['complete_distinct_ternary_sets_through_n7']==312992 and controls['boundary_depths']==[6,4]
    assert (transport['labelled_extensions_checked'],transport['Boolean_identities_checked'])==(128,512)
    assert (unique['two_cover_geometries'],unique['exact_fields_reconstructed'],unique['global_kernel_classes_checked'])==(43,311,765)
    receipts=['singleton_c_d5_e12_e126_certificate_reproduction.json','two_cover_third_unique_kernel_certificate_reproduction.json'];certificates=[]
    for n,expected in zip(receipts,[(37,36),(34,33)]):
        r=read(n);assert r['status']=='pass' and (r['files'],r['checksum_entries'])==expected
        assert sha(ROOT/r['archive'])==r['sha256']
        with zipfile.ZipFile(ROOT/r['archive']) as z:
            assert z.testzip() is None;prefix=z.namelist()[0].split('/')[0]
            for line in z.read(prefix+'/CHECKSUMS.txt').decode().splitlines():
                h,f=line.split('  ',1);assert hashlib.sha256(z.read(prefix+'/'+f)).hexdigest()==h
        certificates.append(dict(path=r['archive'],files=r['files'],sha256=r['sha256'],reproduction=n))
    assert read(receipts[0])['data_files_reproduced_byte_identically']==3 and read(receipts[0])['audits_reproduced_byte_identically']==7
    assert read(receipts[1])['audits_reproduced_byte_identically']==1
    checks=0
    for manifest,folder in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,f=line.split('  ',1);assert sha(folder/f)==h,f;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active['workers']==[] and active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261010_14.json'
    joint=active['joint_fiber_cases'];admission=active['small_first_third_admission'];inv=read('small_first_third_inventory.json')['records']
    assert (admission['remaining_binary_typed_orbits'],admission['remaining_binary_profile_pairs'])==(140,655)
    prior={z['id']:set(map(tuple,z['removed_parent_pairs'])) for z in read('common_block_profiles_audit.json')['profile_cuts']}
    bad={z['id']:set(map(tuple,z['removed_parent_pairs'])) for z in unique['all_inventory_binary_pair_cuts']}
    existing=[z for z in inv if z['joint_id'] not in joint['binary_excluded_orbits'] and z['id'] not in joint['binary_additional_small_first_third_exclusions']]
    assert len(existing)==185
    newly_bad=sum(len((set(map(tuple,z['binary_profile_pairs']))-prior.get(z['id'],set()))&bad.get(z['id'],set())) for z in existing)
    assert newly_bad==38
    whole_u=set(unique['all_inventory_unrestricted_excluded_ids']);new_binary_geo=[];new_binary_types=[]
    for z in existing:
        rem=set(map(tuple,z['binary_profile_pairs']))-prior.get(z['id'],set())
        if z['id'] in whole_u or (rem and rem<=bad.get(z['id'],set())):
            new_binary_geo.append(z['id'])
            if rem:new_binary_types.append(z['id'])
    assert len(new_binary_geo)==15 and len(new_binary_types)==12
    new_u=[z['id'] for z in inv if z['joint_id'] not in joint['unrestricted_excluded_orbits']
           and z['id'] not in joint['unrestricted_additional_small_first_third_exclusions'] and z['id'] in whole_u]
    assert len(new_u)==15
    joint['binary_additional_small_first_third_exclusions']+=new_binary_geo
    joint['unrestricted_additional_small_first_third_exclusions']+=new_u
    remaining=[z for z in existing if z['id'] not in new_binary_geo];assert len(remaining)==170
    binary=[z for z in remaining if set(map(tuple,z['binary_profile_pairs']))-prior.get(z['id'],set())-bad.get(z['id'],set())]
    pairs=sum(len(set(map(tuple,z['binary_profile_pairs']))-prior.get(z['id'],set())-bad.get(z['id'],set())) for z in binary)
    assert (len(binary),pairs)==(128,617)
    unrestricted=[z for z in inv if z['joint_id'] not in joint['unrestricted_excluded_orbits']
                  and z['id'] not in joint['unrestricted_additional_small_first_third_exclusions']]
    assert len(unrestricted)==203
    assert len([z for z in read('b3_third_cover_inventory.json')['records'] if not z['excluded_by_known_bound']])==125
    active['two_cover_unique_kernel_profile_cuts']=unique['all_inventory_binary_pair_cuts']
    active['two_cover_third_unique_kernel_cuts']=dict(proof='TWO_COVER_THIRD_UNIQUE_KERNEL_CUTS.md',audit=additions[3],
        new_binary_whole_types=new_binary_types,new_binary_geometry_exclusions=new_binary_geo,new_unrestricted_types=new_u,
        new_binary_parent_pairs_removed=38,two_cover_geometries=43,exact_fields=311,global_kernel_classes=765,
        scope=unique['scope'])
    admission.update(remaining_binary_typed_orbits=128,remaining_binary_profile_pairs=617,
        remaining_geometric_after_joint_and_third_exclusions=170,unrestricted_remaining_geometric_in_B1_B2_inventory=203,
        latest_exclusion_audit=additions[3])
    admission['latest_exclusion_audits']+=additions
    joint['two_cover_third_unique_kernel_audit']=additions[3]
    c4=active['B1_in_C1_complete_fourth_space']
    assert (c4['remaining_binary_geometries'],c4['remaining_binary_E_labels'],c4['remaining_binary_fourth_pairs'])==(4,29,164)
    spaces=[z for z in c4['filtered_binary_pair_spaces'] if z['E'] not in ([1,2],[1,2,6])]
    assert (len(spaces),sum(z['labels'] for z in spaces),sum(z['after'] for z in spaces))==(2,21,82)
    c4.update(remaining_binary_geometries=2,remaining_binary_E_labels=21,remaining_binary_fourth_pairs=82,
              remaining_unrestricted_geometries=2,remaining_unrestricted_E_labels=21,filtered_binary_pair_spaces=spaces,
              scope='C4 only singletonD5 E6/E16 remains after complete arbitrary-alphabet E12/E126 cuts')
    c4['latest_exclusion_audits']+=additions[:3]
    for branch in c4['branches']:
        if branch['D']==[5]:
            branch['all_alphabet_excluded_E']+=[[1,2],[1,2,6]]
            branch['remaining_unrestricted_E']=[[6],[1,6]];branch['remaining_binary_E']=[[6],[1,6]]
            branch['remaining_binary_field_pairs']=82
            assert branch['remaining_original_third_pairs']==14
    active['singleton_C_D5_E12_E126_cuts']=dict(proof='C4_D5_E12_E126_UNRESTRICTED_EXCLUSION.md',audits=additions[:3],
        coverage=transport['coverage'],labelled_extensions=128,Boolean_identities=512,
        new_current_binary_fourth_pairs_removed_both_roots=164,whole_third_types_removed=0,
        conditional_row_domain='unique immediate pair12; nonsupplying singular letters retained',
        complete_individual_rows=3648,complete_binary_controls=147840,complete_ternary_sets=312992,
        seeded_controls=24000,scope=transport['scope'])
    active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. Two-cover unique-kernel cuts remove15 unrestricted thirdtypes,12 binary types and38 currentpairs; binary128/617,geometry170,joint22/42; unrestricted203+125=328. C4 D5 E12/E126 excluded atbothroots, leaving E6/E16,2/21/82binary and2/21unrestricted. Both F(13,9,1) remain[11,12]; accepted paper/release unchanged.'
    active['next_structural_work']='Attack C4 D5 E6/E16 with exact next fibers, and refine surviving two-cover global kernel classes using actual input-atom compatibility and cover transfer. Merge common_block_profiles_audit and two_cover_unique_kernel_profile_cuts for every current binary count. Use uniqueP1 only with explicit two-stateP5cover. No admission-as-realization claim or sampled-negative numerical upper.'
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8')
    heading='## Two-cover kernel restrictions and singleton-D5 fourth cuts';assert heading not in content
    content+='\n\n'+heading+'''

10 October2026. LETTER_IMAGE_SHORT_PAIR_COVER.md proves directly that
if K covers P_(h+1), f(K) union missing outputs covers P_h, for any
letter and h>=0. Together with the credited unique-kernel restriction
and tau(P3)=2, no letter can send both residual cover states to P3
isolates. Complete checks cover262,144 n4 map/graph/cover instances
and6,638,520 semantic transfers in full small binary/ternary domains.
Missing outputs are retained explicitly.

C4_D5_E12_E126_UNRESTRICTED_EXCLUSION.md excludes E12 (both guards
enter protected5) and E126 (three immediate pairs) for arbitrary
alphabets at both roots. The corrected exact E12 unique-kernel
domain retains singular nonsuppliers as well as dual suppliers;
independent raw enumeration matches3,648 rows at n6..9. Complete
controls cover147,840 binary ordered alphabets through n8 and312,992
ternary sets through n7, plus24,000 seeded larger alphabets. Every
sync control has a literal R merger within5 or J merger within3;
proper closed graphs certify remaining controls, without an SC
filter. Structural boundary(J,R)=(6,4) is not an attaining F example.
All128 labelled transports/512 Boolean identities pass. Only E6/E16
remain:2geometries/21labels/82binary fourth pairs,2/21unrestricted.
All14 original thirdprofiles still extend at each root.

TWO_COVER_THIRD_UNIQUE_KERNEL_CUTS.md applies the same established
unique-P1 restriction to every explicit two-cover third geometry.
All43 historical geometries,311 exact atom fields and765 global
kernel classes are independently reconstructed. Rank>=12, forced
kernels and all three suppliers are necessary; retained classes are
an overapproximation, never asserted realizable. After previous cuts,
15 unrestricted thirdtypes,12 binary types and38 currentbinary pairs
are newly removed. Binary third128/617,geometric170,joint22/42;
unrestricted B1/B2third203+B3third125=328. Common-block and new
unique-kernel profile cuts must be combined for subsequent counts.

The37-file D5 certificate reproduces three data files and seven
audits byte-identically in isolation. The34-file broader third-field
certificate regenerates its complete audit byte-identically with
historical premises explicit. All98 accumulated audits and bindings
pass;121 publication checksums and six accepted artifacts are unchanged.
Both numerical F(13,9,1) extrema remain[11,12]. The complete-answer
goal remains active/unachieved; these structural cuts give neither
a new numerical F value nor alphabet separation.
'''
    sources|={Path(__file__).name,'SINGLETON_C_D5_E12_E126_CERTIFICATE_README.md',
        'package_singleton_c_d5_e12_e126_certificate.py','check_singleton_c_d5_e12_e126_certificate_package.py',
        'TWO_COVER_THIRD_UNIQUE_KERNEL_CERTIFICATE_README.md','package_two_cover_third_unique_kernel_certificate.py',*receipts}
    # All fallible structural assertions precede these authoritative writes.
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier.write_text(content,encoding='utf-8')
    result=dict(old)
    result.update(date='2026-10-10',status='Audited two-cover global-kernel and two-root D5 fourth exclusions',
        previous_historical_audit='AUXILIARY_AUDIT_20261010_14.json',passed_audits=audits,
        current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,active_workers=[],
        remaining_binary_typed_third_orbits=128,remaining_binary_profile_pairs=617,
        remaining_binary_third_types=128,remaining_binary_third_pairs=617,
        binary_geometric_after_all_cuts=170,remaining_binary_geometric_after_joint_and_third_cuts=170,
        unrestricted_geometric_B1_B2=203,unrestricted_geometric_all=328,
        remaining_unrestricted_B1_B2_third_types=203,remaining_unrestricted_third_types=328,
        remaining_binary_C4_fourth_geometries=2,remaining_binary_C4_fourth_labels=21,remaining_binary_C4_fourth_pairs=82,
        remaining_unrestricted_C4_fourth_geometries=2,remaining_unrestricted_C4_fourth_labels=21,
        B0_C4_fourth_space=c4,two_cover_third_unique_kernel_cuts=active['two_cover_third_unique_kernel_cuts'],
        singleton_C_D5_E12_E126_cuts=active['singleton_C_D5_E12_E126_cuts'],new_auxiliary_certificates=certificates,
        accepted_checksum_entries=checks,source_sha256={n:sha(ROOT/n) for n in sorted(sources)},
        limits='Conditional two-cover third and fourth exclusions only. Numerical F(13,9,1) remains[11,12], all-parameter goal unachieved.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),bindings=bindings,accepted_checksums=checks,
        binary_third=128,binary_pairs=617,binary_geometry=170,unrestricted_third=328,C4=[2,21,82],interval=[11,12])))
if __name__=='__main__':main()
