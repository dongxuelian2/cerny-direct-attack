"""Freeze complete C3 cuts only after independent isolated regeneration."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=ROOT/'AUXILIARY_AUDIT_20261010_22.json';assert not output.exists();oldname='AUXILIARY_AUDIT_20261010_21.json';old=read(oldname)
    for n,h in old['source_sha256'].items():assert sha(ROOT/n)==h,n
    additions=['c3_staircase_prefix_audit.json','c3_staircase_audit.json'];audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==119;sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        obj=read(n);assert obj['status']=='pass',n
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    datafiles=['c3_staircase_first_inventory.json','c3_staircase_plane_inventory.json','c3_staircase_inventory.json','c3_staircase_scope.json']
    for n in datafiles:
        obj=read(n);sources.add(n)
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,f;sources.add(f)
    prefix,audit=map(read,additions)
    assert (prefix['global_classes'],prefix['ordered_first_pairs'],prefix['retained_first_pairs'],prefix['common_planes_checked'],prefix['retained_planes'])==(101,39436,19968,411558,53766)
    assert (audit['canonical_prefixes'],audit['prefix_transports_checked'],audit['four_vertex_planes_checked'],audit['literal_letter_maps_checked'],audit['flag_tree_nodes_checked'])==(406,53790,24,748788,6152)
    assert audit['tree_counts']['missing_required_group']==4958 and audit['tree_counts']['maximal_graph_not_SC']==786 and audit['tree_counts']['internal_nodes']==408
    assert audit['new_unrestricted_joint_exclusions']==['b3_mixed_c3']
    receipt=read('c3_staircase_certificate_reproduction.json');assert receipt['status']=='pass' and (receipt['audits_reproduced_byte_identically'],receipt['data_files_reproduced_byte_identically'])==(2,3)
    assert receipt['files']>0 and receipt['checksum_entries']==receipt['files']-1 and sha(ROOT/receipt['archive'])==receipt['sha256']
    with zipfile.ZipFile(ROOT/receipt['archive']) as z:
        assert z.testzip() is None and len(z.namelist())==receipt['files']
        for line in z.read('c3_staircase/CHECKSUMS.txt').decode().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('c3_staircase/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/c3_staircase_reproduction/c3_staircase'
    for n in additions+datafiles[:3]:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for manifest,folder in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert sha(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert sha(PAPER/n)==h,n
    active=read('active_research.json');assert active==read('c3_staircase_baseline_state.json') and active['workers']==[] and active['current_auxiliary_audit']==oldname
    j=active['joint_fiber_cases'];assert not(set(audit['new_excluded_third_ids'])&set(j['unrestricted_additional_B3_third_exclusions']))
    j['unrestricted_additional_B3_third_exclusions']+=audit['new_excluded_third_ids'];j['unrestricted_excluded_orbits']=sorted(set(j['unrestricted_excluded_orbits'])|set(audit['new_unrestricted_joint_exclusions']))
    inv=read('small_first_third_inventory.json')['records'];b3=read('b3_third_cover_inventory.json')['records']
    u12=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    u3=[z for z in b3 if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']]
    assert (len(u12),len(u3),43-len(j['unrestricted_excluded_orbits']))==(136,1,21) and u3[0]['id']=='b3_mixed_c1_third2'
    assert active['small_first_third_admission']['remaining_binary_typed_orbits']==105 and active['small_first_third_admission']['remaining_binary_profile_pairs']==448
    j.update(unrestricted_remaining_orbits=21,c3_staircase_audit=additions[1])
    active['b3_third_cover'].update(excluded_profiles=j['unrestricted_additional_B3_third_exclusions'],unrestricted_remaining_B3_geometries=1,combined_unrestricted_remaining_geometries=137,latest_exclusion_audit=additions[1])
    coverage=dict(proof='C3_STAIRCASE_EXCLUSION.md',audits=additions,scope_file='c3_staircase_scope.json',inventories=datafiles[:3],previous_geometries=5,selected_geometries=4,global_classes=101,ordered_first_pairs=39436,common_planes=411558,retained_prefixes=53790,canonical_prefixes=406,literal_letters=748788,flag_nodes=6152,four_vertex_planes=24,new_unrestricted_third_exclusions=audit['new_excluded_third_ids'],new_unrestricted_joint_exclusions=audit['new_unrestricted_joint_exclusions'],remaining_unrestricted_B3_geometries=1,remaining_unrestricted_third_geometries=137,remaining_unrestricted_joints=21,certificate=receipt['archive'],scope=audit['scope'])
    active['c3_staircase_cuts']=coverage;active['current_auxiliary_audit']=output.name
    active['instruction']='Goalactive/unachieved. Complete C3 staircase domains excludeallfourremainingC3thirdgeometries andthewholeC3joint. Remainingunrestricted136+1=137,joint21,first5;binary105/448,geometry120,joint18unchanged. BothF(13,9,1)remain[11,12]. Acceptedpartial-answerpaper/releaseunchanged.'
    active['next_structural_work']='Finish the sole remaining B3 geometry b3_mixed_c1_third2: complete all retained first-pair/plane domains, normalize variable immediate extra edges and preserve all actual R choices for four-vertex planes. Reuse literal kernel-atom pools and staircase basis flags. Then generalize to remaining136B1/B2geometries andbinary105/448profiles, preserving allfourcutlists. No basis-image-safety sufficiency, invariant-plane shortcut, boundedalphabet assumption or numericalFclaim from provisional negatives.'
    active['general_solver_status']='Complete101immediategraphs,39436firstpairs,411558secondplanes,53790actualbasischoices and406canonicalprefixorbits support fourC3thirdexclusions. Independent directblock assignment reconstructs748788letters; rationaltreecheckverifies6152nodes; all24four-vertexplanes keep bothRchoices. Remaining18binary/21unrestrictedjoints and137unrestrictedthirdrecords; no numericalFvalue or alphabetseparation.'
    heading='## Complete C3 staircase exclusion';frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');assert heading not in content
    content+='\n\n'+heading+'''

10 October2026. ThefourremainingC3thirdgeometries areexcluded using
actualstaircase imagebases andcomplete arbitrary-alphabet letterdomains.
All101retainedimmediategraphs,39436firstpairs and411558secondplanes are
independentlychecked. The53790actualRchoices,includingbothRchoices in
all24four-vertexplanes, transportto406canonicalprefixorbits. Thefullplane
condition onf(T) isretained; thefourthvertexisnotassumed actualorinvariant.

Thegenerator reconstructs748788labelledletters withallatompermutations.
Theindependentchecker assignsblocks directly andcompares canonical
row/flagdigests, thenusesits ownreconstructedmaps andrational elimination
tocheckevery6152flag-tree node. Thereare4958missing-grouprejections,
786properclosed-setrejections and408internalall-childrenrejections.
Characteristicrow ranks overthegenerator'sprime areexact byHadamard.
Thecompactcertificate storescounts/digests ratherthan repeatedletterlists.

ThewholeC3joint isexcluded bycompositionwithprior completecuts.
Remainingunrestricted136+1=137thirdgeometries,joint21,first5;
binary105/448/120/joint18unchanged. Threeinventories andtwoaudits
reproducebyte-identically inisolation. All119audits and121publication
checksums pass;sixacceptedartifactsareunchanged. BothF(13,9,1)remain
[11,12],goalactive/unachieved,andtheacceptedpaperremainsapartialanswer.
'''
    sources|={Path(__file__).name,'C3_STAIRCASE_CERTIFICATE_README.md','package_c3_staircase_certificate.py','c3_staircase_certificate_reproduction.json'}
    result=dict(old);result.update(date='2026-10-10',status='Audited complete four-geometry C3 staircase exclusion',previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,unrestricted_remaining_joint_orbits=21,unrestricted_geometric_B1_B2=136,unrestricted_geometric_B3=1,unrestricted_geometric_all=137,remaining_unrestricted_B1_B2_third_types=136,remaining_unrestricted_third_types=137,c3_staircase_cuts=coverage,new_auxiliary_certificates=[dict(path=receipt['archive'],files=receipt['files'],sha256=receipt['sha256'],reproduction='c3_staircase_certificate_reproduction.json')],limits=audit['scope'])
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n');frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:sha(ROOT/n) for n in sorted(sources)};output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=119,sources=len(sources),bindings=bindings,accepted_checksums=checks,binary=[105,448,120,18],unrestricted=[136,1,137,21,5],interval=[11,12])))
if __name__=='__main__':main()
