"""Freeze the complete two-geometry staircase exclusion after reproduction."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_21.json';assert not output.exists();oldname='AUXILIARY_AUDIT_20261010_20.json';old=read(oldname)
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['b3_staircase_prefix_audit.json','b3_staircase_controls_audit.json','b3_staircase_audit.json'];audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==117
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        obj=read(n);assert obj['status']=='pass',n
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    datafiles=['b3_staircase_first_inventory.json','b3_staircase_plane_inventory.json','b3_staircase_inventory.json','b3_staircase_scope.json']
    for n in datafiles:
        obj=read(n);sources.add(n)
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,f;sources.add(f)
    prefix,control,audit=map(read,additions)
    assert (prefix['global_classes'],prefix['ordered_first_pairs'],prefix['retained_first_pairs'],prefix['common_planes_checked'],prefix['retained_planes'])==(8,3920,1932,44136,180)
    assert (control['constant_cardinality_families'],control['characteristic_span_memberships'],control['block_assignment_domains'],control['literal_map_instances'],control['positive_domains'])==(2238,21378,202848,1055552,22400)
    assert (audit['canonical_prefixes'],audit['literal_letter_maps_checked'],audit['flag_tree_nodes_checked'])==(10,305280,190)
    assert audit['tree_counts']['missing_required_group']==164 and audit['tree_counts']['maximal_graph_not_SC']==11 and audit['maximum_safety_depth']==5
    assert audit['new_excluded_third_ids']==['b3_mixed_c1_third6','b3_mixed_c8_third1'] and audit['new_unrestricted_joint_exclusions']==['b3_mixed_c8']
    receipt=read('b3_staircase_certificate_reproduction.json');assert receipt['status']=='pass' and (receipt['files'],receipt['checksum_entries'],receipt['audits_reproduced_byte_identically'],receipt['data_files_reproduced_byte_identically'])==(45,44,3,3)
    assert sha(ROOT/receipt['archive'])==receipt['sha256']
    with zipfile.ZipFile(ROOT/receipt['archive']) as z:
        assert z.testzip() is None and len(z.namelist())==45
        for line in z.read('b3_staircase/CHECKSUMS.txt').decode().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('b3_staircase/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/b3_staircase_reproduction/b3_staircase'
    for n in additions+datafiles[:3]:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for manifest,folder in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active==read('b3_staircase_baseline_state.json') and active['workers']==[] and active['current_auxiliary_audit']==oldname
    j=active['joint_fiber_cases'];assert not(set(audit['new_excluded_third_ids'])&set(j['unrestricted_additional_B3_third_exclusions']))
    j['unrestricted_additional_B3_third_exclusions']+=audit['new_excluded_third_ids'];j['unrestricted_excluded_orbits']=sorted(set(j['unrestricted_excluded_orbits'])|set(audit['new_unrestricted_joint_exclusions']))
    inv=read('small_first_third_inventory.json')['records'];b3=read('b3_third_cover_inventory.json')['records']
    u12=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3 if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']]
    assert (len(u12),len(u3),43-len(j['unrestricted_excluded_orbits']))==(136,5,22)
    assert {z['id'] for z in u3}=={'b3_mixed_c1_third2','b3_mixed_c3_third1','b3_mixed_c3_third4','b3_mixed_c3_third6','b3_mixed_c3_third9'}
    assert active['small_first_third_admission']['remaining_binary_typed_orbits']==105 and active['small_first_third_admission']['remaining_binary_profile_pairs']==448
    j.update(unrestricted_remaining_orbits=22,b3_staircase_audit=additions[2])
    active['b3_third_cover'].update(excluded_profiles=j['unrestricted_additional_B3_third_exclusions'],unrestricted_remaining_B3_geometries=5,combined_unrestricted_remaining_geometries=141,latest_exclusion_audit=additions[2])
    coverage=dict(proof='B3_STAIRCASE_FLAG_EXCLUSION.md',audits=additions,scope_file='b3_staircase_scope.json',inventories=datafiles[:3],previous_geometries=7,selected_geometries=2,global_classes=8,ordered_first_pairs=3920,common_planes=44136,retained_prefixes=180,canonical_prefixes=10,literal_letters=305280,flag_nodes=190,maximum_safety_depth=5,new_unrestricted_third_exclusions=audit['new_excluded_third_ids'],new_unrestricted_joint_exclusions=audit['new_unrestricted_joint_exclusions'],remaining_unrestricted_B3_geometries=5,remaining_unrestricted_third_geometries=141,remaining_unrestricted_joints=22,certificate=receipt['archive'],scope=audit['scope'])
    active['b3_staircase_cuts']=coverage;active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. Complete staircase image-flag domains exclude two more unrestrictedB3 geometries andthewholeC8joint. Remainingunrestricted136+5=141,joint22,first5;binary105/448,geometry120,joint18unchanged. Both F(13,9,1) remain[11,12]. Accepted partial-answer paper/release unchanged.'
    active['next_structural_work']='Apply staircase flags to remaining B3c1_third2 andfourC3geometries. Forc1_third2 first finish the large complete depth-two plane domain (not included in the two-geometry certificate); preserve all Boolean companions and actual-image basis choices. Generalize exact kernel-atom letter enumeration with symmetry transports before testing B1/B2binary/unrestricted. Actual staircase basis exists because equality flags growone atatime; never assert basis-image safety implies allword safety or a retainedflag realizes an automaton.'
    active['general_solver_status']='Complete arbitrary-alphabet literal pools, tenprefixorbits and190staircase nodes exclude2additionalB3thirdgeometries atdepth<=5. Independent directblock assignments, rational flagcheck, all180transports andisolated3data/3audit reproduction pass. Remaining18binary/22unrestrictedjoints,105/448binary and141unrestrictedthirdrecords. No numericalFvalue or alphabetseparation.'
    heading='## Complete B3 staircase equality-flag exclusion';frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');assert heading not in content
    content+='\n\n'+heading+'''

10 October2026. Exact equality dimensions permit an actual staircase
basis R0=S,R1,...: eachnextRi is an actualletterimage ofthe previous
basisvector outsidethe currentprefixspan. Allletters sendearlier basis
vectors intothe prescribednextprefixspan. Enumerateevery possible next
image, retainall compatibleletters, andtestsafeimages, mandatory supplier/
chain-step domains andthe maximaltransitiongraph. Basis-image safety is
only necessary andis neverasserted toguarantee allword safety.

Complete selectedC1third6/C8third1 domains contain8immediategraphs,
3920firstpairs and44136secondplanes. All180retainedprefixes transport
to8C1+2C8orbits. Fullcolouring/atombijection enumeration retains305280
literalletters, withall permutations. Independent directkernel-block
assignment matches everymap, andrational elimination checks all190flag
nodes andeverybranch. Modularranks areexact byHadamard(3^13<p).
Elevennodes haveproperclosedsets;164lackrequiredgroups;15internal
nodes haveallchildrenrejected. Safetythroughdepth5 suffices. Small
controls check2238constant-cardinalityfamilies,21378spanmemberships,
202848blockdomains and1055552labelledmapinstances.

Boththirdgeometries areexcluded, completingthe wholeC8joint using
previouscertificates. Remainingunrestricted136+5=141thirdgeometries,
joint22,first5. Binary105/448/120/joint18 isunchanged. The45-file
isolatedcertificate reproduces threeinventories andthreeaudits byte-
identically. All117audits and121publicationchecksums pass; sixaccepted
artifacts areunchanged. BothF(13,9,1) remain[11,12],goalactive/unachieved,
andtheacceptedpaper remainsapartialanswer.
'''
    sources|={Path(__file__).name,'B3_STAIRCASE_CERTIFICATE_README.md','package_b3_staircase_certificate.py','b3_staircase_certificate_reproduction.json'}
    result=dict(old);result.update(date='2026-10-10',status='Audited complete two-geometry B3 staircase exclusion',previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,unrestricted_remaining_joint_orbits=22,unrestricted_geometric_B1_B2=136,unrestricted_geometric_B3=5,unrestricted_geometric_all=141,remaining_unrestricted_B1_B2_third_types=136,remaining_unrestricted_third_types=141,b3_staircase_cuts=coverage,new_auxiliary_certificates=[dict(path=receipt['archive'],files=45,sha256=receipt['sha256'],reproduction='b3_staircase_certificate_reproduction.json')],limits=audit['scope'])
    # All checks precede authoritative writes.
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n');frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:sha(ROOT/n) for n in sorted(sources)};output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=117,sources=len(sources),bindings=bindings,accepted_checksums=checks,binary=[105,448,120,18],unrestricted=[136,5,141,22,5],interval=[11,12])))
if __name__=='__main__':main()
