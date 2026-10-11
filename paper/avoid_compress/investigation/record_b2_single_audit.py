"""Adopt five unrestricted / four additional binary one-class negatives."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    oldname='AUXILIARY_AUDIT_20261011_04.json';output=ROOT/'AUXILIARY_AUDIT_20261011_05.json'
    assert not output.exists();old=read(oldname)
    for n,h in old['source_sha256'].items():assert digest(ROOT/n)==h,n
    scope=read('b2_single_scope.json');active=read('active_research.json');baseline=read(scope['baseline'])
    assert active==baseline and active['current_auxiliary_audit']==scope['checkpoint']==oldname and active['workers']==[]
    assert digest(ROOT/scope['baseline'])==old['source_sha256']['active_research.json']
    for n,h in scope['source_sha256'].items():assert digest(ROOT/n)==h,n
    for n,h in read('b2_single_parent_domains.json')['historical_source_bindings'].items():assert digest(ROOT/n)==h,n
    datafiles=[n+'_single_inventory.json' for n in scope['selected']]
    additions=[n+'_single_audit.json' for n in scope['selected']]+['b2_single_composition_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==140
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        report=read(n);assert report['status']=='pass',n
        for f,h in report['source_sha256'].items():assert digest(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    for n in datafiles+['b2_single_scope.json']:
        sources.add(n)
        for f,h in read(n)['source_sha256'].items():assert digest(ROOT/f)==h,f;sources.add(f)
    composition=read('b2_single_composition_audit.json');names=scope['selected']
    assert composition['new_excluded_third_ids']==names and len(names)==5
    assert composition['maximum_basis_depth']==3 and composition['column_rules_additional_deletions']==0
    receipt=read('b2_single_certificate_reproduction.json');assert receipt['status']=='pass'
    assert receipt['audits_reproduced_byte_identically']==7 and receipt['data_files_reproduced_byte_identically']==5
    assert len(receipt['runs'])==12 and all(r['exit']==0 for r in receipt['runs'])
    archive=ROOT/receipt['archive'];assert digest(archive)==receipt['sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==receipt['files']
        lines=z.read('b2_single_first_pair/CHECKSUMS.txt').decode().splitlines()
        assert len(lines)==receipt['checksum_entries']==receipt['files']-1
        for line in lines:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('b2_single_first_pair/'+n)).hexdigest()==h
    isolated=PAPER/'_qa/b2_single_first_pair_reproduction/b2_single_first_pair'
    for n in additions+datafiles+['basis_column_reaching_audit.json']:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for manifest,folder in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert digest(folder/n)==h,n;checks+=1
    assert checks==121
    for n,h in old['accepted_artifact_sha256'].items():assert digest(PAPER/n)==h,n
    j=active['joint_fiber_cases']
    for prefix,key in [('unrestricted','new_unrestricted_geometry_exclusions'),('binary','new_binary_geometry_exclusions')]:
        new=set(composition[key]);field=prefix+'_additional_small_first_third_exclusions'
        assert not new&set(j[field]);j[field]=sorted(set(j[field])|new)
        field=prefix+'_excluded_orbits';new=set(composition['new_'+prefix+'_joint_exclusions'])
        assert not new&set(j[field]);j[field]=sorted(set(j[field])|new)
    assert composition['new_unrestricted_joint_exclusions']==['b2_mixed_c12'] and composition['new_binary_joint_exclusions']==[]
    j.update(binary_remaining_orbits=17,unrestricted_remaining_orbits=18,b2_single_audit='b2_single_composition_audit.json')
    inv=read('small_first_third_inventory.json')['records'];cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],active['two_cover_unique_kernel_profile_cuts'],
                  active['two_cover_exact_kernel_profile_cuts'],active['three_cover_atom_kernel_profile_cuts']]:
        for z in array:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    profile=lambda z:set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())
    u=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    b=[z for z in inv if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    assert (len(u),len(b),sum(bool(profile(z)) for z in b),sum(len(profile(z)) for z in b))==(101,89,85,404)
    assert len({z['joint_id'] for z in u})==18 and len({z['joint_id'] for z in b if profile(z)})==17
    for k in ('two_cover_unique_kernel_profile_cuts','two_cover_exact_kernel_profile_cuts','three_cover_atom_kernel_profile_cuts'):
        assert active[k]==baseline[k]
    admission=active['small_first_third_admission']
    admission.update(remaining_binary_typed_orbits=85,remaining_binary_profile_pairs=404,
                     remaining_geometric_after_joint_and_third_exclusions=89,
                     unrestricted_remaining_geometric_in_B1_B2_inventory=101,latest_exclusion_audit='b2_single_composition_audit.json')
    admission['latest_exclusion_audits'].append('b2_single_composition_audit.json')
    active['b3_third_cover']['combined_unrestricted_remaining_geometries']=101
    coverage=dict(proof='B2_SINGLE_CLASS_FIRST_PAIR_EXCLUSION.md',audits=additions,scope_file='b2_single_scope.json',
                  new_unrestricted_third_exclusions=composition['new_unrestricted_geometry_exclusions'],
                  new_binary_third_exclusions=composition['new_binary_geometry_exclusions'],
                  new_unrestricted_joint_exclusions=['b2_mixed_c12'],new_binary_joint_exclusions=[],
                  labelled_first_pairs=composition['complete_labelled_first_pairs'],
                  flag_counts=composition['tree_counts'],maximum_basis_depth=3,column_additional_deletions=0,
                  remaining_unrestricted_geometries=101,remaining_binary_geometries=89,
                  remaining_binary_typed=85,remaining_binary_profiles=404,remaining_unrestricted_joints=18,
                  remaining_binary_joints=17,certificate=receipt['archive'],scope=composition['scope'])
    active['b2_single_first_pair_cuts']=coverage;active['current_auxiliary_audit']=output.name
    active['instruction']='Goal active/unachieved. A further five unrestricted and four binary B2 geometries are excluded. The whole b2_mixed_c12 joint is now excluded unrestricted; it was already excluded binary. Unrestricted101/joints18; binary85 types/404 profiles/89 geometries/joints17. Both F(13,9,1) remain [11,12]. Accepted partial paper and publication unchanged.'
    active['general_solver_status']='The five single-class first-pair domains, literal maps and shallow flags pass independent full coverage and rational checks and byte-exact isolated regeneration. Supplier and proper-closed-set rules terminate every branch before depth4. No additional column rule, numerical bound or alphabet separation is inferred.'
    active['next_structural_work']='Attack the remaining101 unrestricted geometries and binary85 types/404 profiles. Preserve every native field in relabelling, all four profile-cut lists and actual reachability. Extend complete staircase covers; old28 budget-exhausted probes are unknown. The column rules require a full actual prefix span at depth>=4. Do not substitute structural counts for F values.'
    sources|={Path(__file__).name,'B2_SINGLE_CERTIFICATE_README.md','package_b2_single_certificate.py',
              'b2_single_certificate_reproduction.json','B2_SINGLE_CLASS_FIRST_PAIR_EXCLUSION.md',receipt['archive']}
    result=dict(old)
    result.update(date='2026-10-11',status='Audited five unrestricted/four binary one-class B2 first-pair cuts',
                  previous_historical_audit=oldname,passed_audits=audits,current_audit_source_bindings_verified=bindings,
                  paper_and_release_unchanged=True,active_workers=[],accepted_checksum_entries=checks,
                  remaining_binary_typed_third_orbits=85,remaining_binary_profile_pairs=404,
                  binary_geometric_after_all_cuts=89,unrestricted_geometric_B1_B2=101,
                  unrestricted_geometric_B3=0,unrestricted_geometric_all=101,
                  remaining_binary_third_types=85,remaining_binary_third_pairs=404,
                  remaining_unrestricted_B1_B2_third_types=101,remaining_unrestricted_third_types=101,
                  remaining_binary_geometric_after_joint_and_third_cuts=89,
                  binary_remaining_joint_orbits=17,unrestricted_remaining_joint_orbits=18,
                  b2_single_first_pair_cuts=coverage,
                  new_auxiliary_certificates=[dict(path=receipt['archive'],files=receipt['files'],sha256=receipt['sha256'],
                                                   reproduction='b2_single_certificate_reproduction.json')],limits=composition['scope'])
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8')
    heading='## Five single-class B2 first-pair cuts';assert heading not in content
    content+='\n'+heading+'\n\n'+(
        '11 October 2026. Five full arbitrary-alphabet certificates exclude '+', '.join(names)+'. '
        'Each has exactly one retained immediate graph class. All labelled ordered first pairs, whole-graph '
        'and native-kernel transports, literal maps and complete flag branches are checked independently. '
        'The trees stop at depth at most three, using supplier and proper-closed-set rejections. '
        'Column restrictions are unused. The immutable package regenerates seven audits and five inventories '
        'byte-identically in twelve isolated runs. All140 old/new audits and121 publication checksums pass.\n\n'
        'Unrestricted frontier:101 B1/B2 geometries, B3=0,18 joints. Binary:85 typed families,404 profiles,89 '
        'geometries,17 joints. This is five new unrestricted and four additional binary geometry exclusions; '
        'b2_mixed_c12 was already excluded binary and is now also excluded unrestricted. All four prior '
        'binary profile-cut lists remain merged. Both first-family sets remain b1_out,b2_in,b2_mixed.\n\n'
        'Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. There is no numerical extremum, alphabet '
        'separation or complete formula. The accepted partial-answer paper and publication artifacts '
        'are unchanged. The goal remains active and unachieved.\n')
    # No authority mutation occurs until every gate above has succeeded.
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n')
    frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:digest(ROOT/n) for n in sorted(sources)}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',audits=140,sources=len(sources),bindings=bindings,publication_checksums=checks,
                         binary=[85,404,89,17],unrestricted=[101,0,101,18],interval=[11,12])))
if __name__=='__main__':main()
