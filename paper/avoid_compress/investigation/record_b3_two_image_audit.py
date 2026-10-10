"""Freeze verified two-image cuts after isolated regeneration and artifact checks."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_20.json';assert not output.exists()
    oldname='AUXILIARY_AUDIT_20261010_19.json';old=read(oldname)
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['two_image_letter_controls_audit.json','b3_two_image_audit.json'];audits=old['passed_audits']+additions
    assert len(audits)==len(set(audits))==114;sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        obj=read(n);assert obj['status']=='pass',n
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    for n in ['b3_first_image_inventory.json','b3_two_image_inventory.json','b3_two_image_scope.json']:
        obj=read(n);sources.add(n)
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,f;sources.add(f)
    control,audit=map(read,additions)
    assert (control['field_kernel_two_image_instances'],control['literal_map_instances'],control['positive_domains'])==(1865920,1180224,87344)
    assert (audit['selected_geometries'],audit['global_classes'],audit['ordered_first_pairs'],audit['retained_first_pairs'],audit['common_planes_checked'])==(28,67,21930,8861,238933)
    assert (audit['exact_domain_digests_checked'],audit['distinct_quota_queries'],audit['closed_graphs_checked'])==(134,555963,91779)
    assert audit['new_unrestricted_joint_exclusions']==['b3_mixed_c4','b3_mixed_c5','b3_mixed_c7','b3_mixed_c9']
    receipt=read('b3_two_image_certificate_reproduction.json')
    assert receipt['status']=='pass' and (receipt['files'],receipt['checksum_entries'],receipt['audits_reproduced_byte_identically'],receipt['data_files_reproduced_byte_identically'])==(40,39,2,2)
    assert sha(ROOT/receipt['archive'])==receipt['sha256']
    with zipfile.ZipFile(ROOT/receipt['archive']) as z:
        assert z.testzip() is None and len(z.namelist())==40
        for line in z.read('b3_two_image/CHECKSUMS.txt').decode().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('b3_two_image/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/b3_two_image_reproduction/b3_two_image'
    for n in additions+['b3_first_image_inventory.json','b3_two_image_inventory.json']:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for manifest,folder in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active==read('b3_two_image_baseline_state.json') and active['workers']==[] and active['current_auxiliary_audit']==oldname
    j=active['joint_fiber_cases'];assert not(set(audit['new_excluded_third_ids'])&set(j['unrestricted_additional_B3_third_exclusions']))
    j['unrestricted_additional_B3_third_exclusions']+=audit['new_excluded_third_ids'];j['unrestricted_excluded_orbits']=sorted(set(j['unrestricted_excluded_orbits'])|set(audit['new_unrestricted_joint_exclusions']))
    inv=read('small_first_third_inventory.json')['records'];b3=read('b3_third_cover_inventory.json')['records']
    u12=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3 if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']]
    assert (len(u12),len(u3),43-len(j['unrestricted_excluded_orbits']))==(136,7,23)
    assert active['small_first_third_admission']['remaining_binary_typed_orbits']==105 and active['small_first_third_admission']['remaining_binary_profile_pairs']==448
    j.update(unrestricted_remaining_orbits=23,b3_two_image_audit=additions[1])
    active['b3_third_cover'].update(excluded_profiles=j['unrestricted_additional_B3_third_exclusions'],unrestricted_remaining_B3_geometries=7,combined_unrestricted_remaining_geometries=143,latest_exclusion_audit=additions[1])
    coverage=dict(proof='B3_TWO_IMAGE_PLANE.md',audits=additions,scope_file='b3_two_image_scope.json',inventories=['b3_first_image_inventory.json','b3_two_image_inventory.json'],previous_geometries=35,selected_geometries=28,global_classes=67,ordered_first_pairs=21930,common_planes=238933,exact_domain_digests=134,new_unrestricted_third_exclusions=audit['new_excluded_third_ids'],new_unrestricted_joint_exclusions=audit['new_unrestricted_joint_exclusions'],remaining_unrestricted_B3_geometries=7,remaining_unrestricted_third_geometries=143,remaining_unrestricted_joints=23,certificate=receipt['archive'],scope=audit['scope'])
    active['b3_two_image_plane_cuts']=coverage;active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. Complete two-image/common-plane domains exclude28 additional unrestrictedB3 geometries andfourwholejoints. Remainingunrestricted136+7=143,joint23,first5;binary105/448,geometry120,joint18unchanged. Both F(13,9,1) remain[11,12]. Accepted partial-answer paper/release unchanged.'
    active['next_structural_work']='Attack seven remaining B3 geometries(c1_third2,c1_third6,c3_third1,c3_third4,c3_third6,c3_third9,c8_third1) using simultaneous pair transitions or higher equality flags. The largest c1_third2 second-image domain is not certified by this selected negative scope. Other retained planes are necessary overapproximations only. Then remainingB1/B2binary/unrestricted cases. Preserve all feasible images, Boolean companions, arbitrary alphabets and allfourprofile-cut lists; no invariant-plane shortcut or higher-layer edge cap.'
    active['general_solver_status']='Independent literal-colouring and quota-bounded active-vertex domains plus exact determinant plane enumeration certify28 additionalB3third cuts. Remaining18binary/23unrestricted joints,105/448binary and143unrestricted thirdrecords. No complete thirteen-state automaton scan, attaining-alphabet result, numerical F value or alphabet separation.'
    heading='## Exact B3 two-image domains and common depth-two planes';frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');assert heading not in content
    content+='\n\n'+heading+'''

10 October2026. The equality flag requires every first image to be S or
one common distinct T, and all second images to lie in one affine plane.
Every depth-two image belongs to the complete feasible independent nine-set
family. Exact kernel-block saturation bits for S,T and output membership
bits for U,V extend the frozen one-letter atoms to96typequotas. The
generator enumerates full output colours; the independent checker uses
quota-bounded active-vertex search and fills isolated outputs exactly.
All arrows, existence and supplier flags match in134domain digests.
Planes are generated by Boolean parallelograms and independently checked
by exact integer determinants. No letter is required to preserve the plane.

The selected complete negative scope comprises28of35currentB3geometries,
all67previouslyretainedglobalgraphs,21930orderedfirst-imagepairs and238933
commonplanes. All are excluded by missing movement, missing dimension,
missing supplier or a non-SC maximal graph. The checker makes555963
distinctquotatests and91779closed-graphchecks. Small labelled-map controls
cover1865920domaininstances against1180224rawmapinstances. Fourwholejoints
(b3_mixed_c4,c5,c7,c9) are additionally excluded. Other geometries are not
rejected by this certificate, and positive maximal graphs are not witnesses.

Remainingunrestricted136+7=143thirdgeometries,joint23,first5;binary
105types/448profiles/120geometries/joint18unchanged. The40-file isolated
certificate reproduces twoinventories andtwoaudits byte-identically.
All114accumulatedaudits and121publicationchecksums pass; sixaccepted
artifacts remainunchanged. Both F(13,9,1) remain[11,12]; thegoal isactive/
unachieved andthe accepted paper remainsapartialanswer.
'''
    sources|={Path(__file__).name,'B3_TWO_IMAGE_CERTIFICATE_README.md','package_b3_two_image_certificate.py','b3_two_image_certificate_reproduction.json'}
    result=dict(old);result.update(date='2026-10-10',status='Audited complete selected B3 two-image/common-plane exclusion',previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,unrestricted_remaining_joint_orbits=23,unrestricted_geometric_B1_B2=136,unrestricted_geometric_B3=7,unrestricted_geometric_all=143,remaining_unrestricted_B1_B2_third_types=136,remaining_unrestricted_third_types=143,b3_two_image_plane_cuts=coverage,new_auxiliary_certificates=[dict(path=receipt['archive'],files=40,sha256=receipt['sha256'],reproduction='b3_two_image_certificate_reproduction.json')],limits=audit['scope'])
    # Finish fallible checks before authoritative state changes.
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n');frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:sha(ROOT/n) for n in sorted(sources)};output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=114,sources=len(sources),bindings=bindings,accepted_checksums=checks,binary=[105,448,120,18],unrestricted=[136,7,143,23,5],interval=[11,12])))
if __name__=='__main__':main()
