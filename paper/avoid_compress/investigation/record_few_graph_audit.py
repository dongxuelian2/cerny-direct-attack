"""Adopt a complete scope only after every proof and reproduction gate."""
from pathlib import Path
import argparse,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def read(n):return json.loads((ROOT/n).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def residual(inv,state):
    j=state['joint_fiber_cases'];cuts={}
    for arr in [read('common_block_profiles_audit.json')['profile_cuts'],state['two_cover_unique_kernel_profile_cuts'],
                state['two_cover_exact_kernel_profile_cuts'],state['three_cover_atom_kernel_profile_cuts']]:
        for z in arr:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    profiles=lambda z:set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())
    u=[z for z in inv if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    b=[z for z in inv if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    return u,b,profiles
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scope',required=True);args=ap.parse_args()
    scope=read(args.scope);tag=scope['output_tag'];names=scope['selected'];output=ROOT/scope['authority_output'];assert not output.exists()
    old=read(scope['checkpoint']);active=read('active_research.json');base=read(scope['baseline'])
    assert active==base and active['current_auxiliary_audit']==scope['checkpoint'] and active['workers']==[]
    assert digest(ROOT/scope['baseline'])==old['source_sha256']['active_research.json']
    for n,h in old['source_sha256'].items():assert digest(ROOT/n)==h,n
    for n,h in scope['source_sha256'].items():assert digest(ROOT/n)==h,n
    for n,h in read(scope['parent_domains'])['historical_source_bindings'].items():assert digest(ROOT/n)==h,n
    datafiles=[n+'_'+tag+'_inventory.json' for n in names]
    additions=[n+'_'+tag+'_audit.json' for n in names]+[tag+'_controls_audit.json',tag+'_composition_audit.json']
    audits=old['passed_audits']+additions;assert len(audits)==len(set(audits))==len(old['passed_audits'])+len(names)+2
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for n in audits:
        obj=read(n);assert obj['status']=='pass',n
        for f,h in obj['source_sha256'].items():assert digest(ROOT/f)==h,(n,f);sources.add(f);bindings+=1
    for n in datafiles+[args.scope]:
        sources.add(n)
        for f,h in read(n)['source_sha256'].items():assert digest(ROOT/f)==h,f;sources.add(f)
    c=read(tag+'_composition_audit.json');controls=read(tag+'_controls_audit.json')
    assert c['new_excluded_third_ids']==names and c['interval']==old['interval']==[11,12]
    assert controls['rejected_invalid_metadata']==12 and controls['independently_verified_native_domains']==len(names)
    receipt=read(tag+'_certificate_reproduction.json');assert receipt['status']=='pass'
    assert receipt['audits_reproduced_byte_identically']==len(names)+3 and receipt['data_files_reproduced_byte_identically']==len(names)
    assert len(receipt['runs'])==2*len(names)+3 and all(r['exit']==0 for r in receipt['runs'])
    archive=ROOT/receipt['archive'];assert digest(archive)==receipt['sha256'];prefix=tag+'_first_pair'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==receipt['files']
        lines=z.read(prefix+'/CHECKSUMS.txt').decode().splitlines()
        assert len(lines)==receipt['checksum_entries']==receipt['files']-1
        for line in lines:
            h,n=line.split('  ',1);assert hashlib.sha256(z.read(prefix+'/'+n)).hexdigest()==h
    isolated=PAPER/'_qa'/(prefix+'_reproduction')/prefix
    for n in additions+datafiles+['basis_column_reaching_audit.json']:assert (isolated/n).read_bytes()==(ROOT/n).read_bytes(),n
    checks=0
    for manifest,folder in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert digest(folder/n)==h,n;checks+=1
    assert checks==old['accepted_checksum_entries']==121
    for n,h in old['accepted_artifact_sha256'].items():assert digest(PAPER/n)==h,n
    inv=read('small_first_third_inventory.json')['records'];before_u,before_b,_=residual(inv,active)
    assert set(names)<={z['id'] for z in before_u}
    assert c['new_binary_geometry_exclusions']==[n for n in names if n in {z['id'] for z in before_b}]
    j=active['joint_fiber_cases']
    for alphabet in ('unrestricted','binary'):
        field=alphabet+'_additional_small_first_third_exclusions';new=set(c['new_'+alphabet+'_geometry_exclusions'])
        assert not new&set(j[field]);j[field]=sorted(set(j[field])|new)
        field=alphabet+'_excluded_orbits';new=set(c['new_'+alphabet+'_joint_exclusions'])
        assert not new&set(j[field]);j[field]=sorted(set(j[field])|new)
    u,b,profiles=residual(inv,active)
    ug,bg,bt,bp=len(u),len(b),sum(bool(profiles(z)) for z in b),sum(len(profiles(z)) for z in b)
    uj,bj=len({z['joint_id'] for z in u}),len({z['joint_id'] for z in b if profiles(z)})
    assert [ug,bg,bt,bp,uj,bj]==[c[k] for k in ('remaining_unrestricted_geometries','remaining_binary_geometries',
          'remaining_binary_typed','remaining_binary_profiles','remaining_unrestricted_joints','remaining_binary_joints')]
    for k in ('two_cover_unique_kernel_profile_cuts','two_cover_exact_kernel_profile_cuts','three_cover_atom_kernel_profile_cuts'):
        assert active[k]==base[k]
    j.update(binary_remaining_orbits=bj,unrestricted_remaining_orbits=uj,latest_few_graph_audit=tag+'_composition_audit.json')
    admission=active['small_first_third_admission']
    admission.update(remaining_binary_typed_orbits=bt,remaining_binary_profile_pairs=bp,
                     remaining_geometric_after_joint_and_third_exclusions=bg,
                     unrestricted_remaining_geometric_in_B1_B2_inventory=ug,latest_exclusion_audit=tag+'_composition_audit.json')
    admission['latest_exclusion_audits'].append(tag+'_composition_audit.json')
    active['b3_third_cover']['combined_unrestricted_remaining_geometries']=ug
    coverage=dict(proof='FEW_GRAPH_FIRST_PAIR_CERTIFICATES.md',audits=additions,scope_file=args.scope,
                  new_unrestricted_third_exclusions=c['new_unrestricted_geometry_exclusions'],
                  new_binary_third_exclusions=c['new_binary_geometry_exclusions'],
                  new_unrestricted_joint_exclusions=c['new_unrestricted_joint_exclusions'],new_binary_joint_exclusions=c['new_binary_joint_exclusions'],
                  labelled_first_pairs=c['complete_labelled_first_pairs'],retained_P1_classes=c['retained_P1_classes'],
                  flag_counts=c['tree_counts'],maximum_basis_depth=c['maximum_basis_depth'],column_additional_deletions=c['column_rules_additional_deletions'],
                  remaining_unrestricted_geometries=ug,remaining_binary_geometries=bg,remaining_binary_typed=bt,remaining_binary_profiles=bp,
                  remaining_unrestricted_joints=uj,remaining_binary_joints=bj,certificate=receipt['archive'],scope=c['scope'])
    active.setdefault('few_graph_first_pair_cuts',[]).append(coverage);active['current_auxiliary_audit']=output.name
    active['instruction']=f'Goal active/unachieved. Full scope {tag} is certified excluded. Unrestricted{ug}/joints{uj}; binary{bt} types/{bp} profiles/{bg} geometries/joints{bj}. Both F(13,9,1) remain [11,12]. Accepted partial paper and publication unchanged.'
    active['general_solver_status']=f'Complete first-pair scopes with {c["retained_P1_classes"]} retained graphs, {c["complete_labelled_first_pairs"]} labelled pairs and {c["tree_counts"]["prefixes"]} representatives pass independent native-domain, literal/rational flag checks, twelve metadata corruptions, and isolated byte-exact regeneration. No F value or alphabet separation follows.'
    active['next_structural_work']=f'Attack remaining{ug} unrestricted geometries and binary{bt} types/{bp} profiles. Reuse scope-parametrized full-pair drivers; preserve native fields, whole-graph transports, all four profile-cut lists and actual reachability. The28 older budget-exhausted probes remain unknown. Column deductions need full actual prefix spans at depth>=4. Do not substitute counts for F values.'
    sources|={Path(__file__).name,'FEW_GRAPH_CERTIFICATE_README.md','package_few_graph_certificate.py',
              tag+'_certificate_reproduction.json','FEW_GRAPH_FIRST_PAIR_CERTIFICATES.md',receipt['archive']}
    result=dict(old)
    result.update(date='2026-10-11',status='Audited complete few-graph first-pair cuts',previous_historical_audit=scope['checkpoint'],
                  passed_audits=audits,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,
                  active_workers=[],accepted_checksum_entries=checks,remaining_binary_typed_third_orbits=bt,
                  remaining_binary_profile_pairs=bp,binary_geometric_after_all_cuts=bg,
                  unrestricted_geometric_B1_B2=ug,unrestricted_geometric_B3=0,unrestricted_geometric_all=ug,
                  remaining_binary_third_types=bt,remaining_binary_third_pairs=bp,
                  remaining_unrestricted_B1_B2_third_types=ug,remaining_unrestricted_third_types=ug,
                  remaining_binary_geometric_after_joint_and_third_cuts=bg,binary_remaining_joint_orbits=bj,
                  unrestricted_remaining_joint_orbits=uj,latest_few_graph_first_pair_cuts=coverage,
                  new_auxiliary_certificates=[dict(path=receipt['archive'],files=receipt['files'],sha256=receipt['sha256'],
                                                   reproduction=tag+'_certificate_reproduction.json')],limits=c['scope'])
    frontier=ROOT/'CURRENT_FRONTIER.md';content=frontier.read_text(encoding='utf-8');heading='## Complete few-graph first pairs: '+tag
    assert heading not in content
    content+='\n'+heading+'\n\n'+(
        f'11 October2026. Full arbitrary-alphabet certificates exclude '+', '.join(names)+'. '
        f'{c["retained_P1_classes"]} retained immediate graphs and {c["complete_labelled_first_pairs"]} labelled first pairs '
        f'are covered by {c["tree_counts"]["prefixes"]} representatives. '
        f'{c["tree_counts"]["literal_letters"]} literal maps and {c["tree_counts"]["nodes"]} flag nodes are checked '
        f'independently, with maximum basis depth {c["maximum_basis_depth"]}. '
        f'Column deletions: {c["column_rules_additional_deletions"]}. Native graph / field transports are complete; '
        'twelve corrupted metadata records are rejected by the actual checker before its first literal-pool call. '
        f'The immutable certificate regenerates {len(names)+3} audits and {len(names)} inventories byte-identically. '
        f'All{len(audits)} audits, {bindings} bindings and{checks} publication checksums pass.\n\n'
        f'Unrestricted frontier:{ug} B1/B2 geometries, B3=0,{uj} joints. Binary:{bt} types,{bp} profiles,{bg} geometries,{bj} joints. '
        'All four previous binary profile-cut lists remain merged. Whole-joint exclusions unrestricted: '
        +(', '.join(c['new_unrestricted_joint_exclusions']) or 'none')+'; binary: '
        +(', '.join(c['new_binary_joint_exclusions']) or 'none')+'.\n\n'
        'Both F_bin(13,9,1) and F(13,9,1) remain [11,12]. No complete formula, alphabet separation or new '
        'numerical extremum follows. Accepted partial-answer paper and publication artifacts remain unchanged. '
        'The full goal remains active and unachieved.\n')
    # Every gate precedes all authoritative writes.
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n');frontier.write_text(content,encoding='utf-8')
    result['source_sha256']={n:digest(ROOT/n) for n in sorted(sources)};output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',authority=output.name,audits=len(audits),sources=len(sources),bindings=bindings,
                         publication_checksums=checks,binary=[bt,bp,bg,bj],unrestricted=[ug,0,ug,uj],interval=[11,12])))
if __name__=='__main__':main()
