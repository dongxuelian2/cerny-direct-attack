"""Adopt one complete replayed graph-quotient exclusion after all audit gates."""
from hashlib import sha256
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;PAPER=HERE.parent;ROOT=PAPER/'investigation';sys.path.insert(0,str(ROOT))
from check_few_graph_composition import residual
NAME='b1_out_c3_third10';PREVIOUS='AUXILIARY_AUDIT_20261011_12.json';NEXT='AUXILIARY_AUDIT_20261011_13.json'
def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def encoded(d):return (json.dumps(d,indent=2)+'\n').encode()
def main():
    output=ROOT/NEXT;assert not output.exists()
    old=read(ROOT/PREVIOUS);active=read(ROOT/'active_research.json');assert active['current_auxiliary_audit']==PREVIOUS
    for n,h in old['source_sha256'].items():assert digest(ROOT/n)==h,n
    auditfile=NAME+'_graph_quotient_full_audit.json';audit=read(ROOT/auditfile)
    assert audit['status']=='pass' and audit['new_excluded_third_ids']==[NAME] and audit['complete_conditional_geometry_exclusion']
    assert audit['parameter']==[13,9,1] and audit['target_ac']==12 and audit['interval']==[11,12]
    assert audit['checked_prefixes']==audit['canonical_prefixes']==887 and audit['labelled_first_pairs']==330708
    assert audit['metadata_corruptions_rejected']==14 and audit['byte_identical_scope_and_audit_reports']==4
    reports=old['passed_audits']+[auditfile];assert len(reports)==len(set(reports))
    sources=set(old['source_sha256'])|set(reports)|{PREVIOUS,'../_qa/'+Path(__file__).name,'check_few_graph_composition.py'};bindings=0
    for name in reports:
        d=read(ROOT/name);assert d['status']=='pass',name
        for f,h in d['source_sha256'].items():assert digest(ROOT/f)==h,(name,f);sources.add(f);bindings+=1
    full=read(HERE/(NAME+'_graph_quotient_full_probe.json'));replay=read(HERE/(NAME+'_full_quotient_reproduction.json'))
    assert full['status']=='complete_independently_checked_QA_only' and full['complete_scope'] and full['candidate'] is None
    assert replay['status']=='pass' and replay['complete_conditional_flag_tree_certificate'] and len(replay['runs'])==4
    assert all(r['exit']==0 for r in replay['runs']) and digest(HERE/replay['archive'])==replay['sha256']
    checks=0
    for manifest,folder in ((PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')):
        for line in manifest.read_text().splitlines():
            h,n=line.split('  ',1);assert digest(folder/n)==h,n;checks+=1
    assert checks==old['accepted_checksum_entries']==121
    for n,h in old['accepted_artifact_sha256'].items():assert digest(PAPER/n)==h,n
    inventory=read(ROOT/'small_first_third_inventory.json')['records'];before_u,before_b,profiles=residual(inventory,active)
    assert len(before_u)==old['unrestricted_geometric_all']==84 and len(before_b)==old['binary_geometric_after_all_cuts']==77
    assert NAME in {z['id'] for z in before_u};new_b=[NAME] if NAME in {z['id'] for z in before_b} else []
    joint=active['joint_fiber_cases']
    for alphabet,names in (('unrestricted',[NAME]),('binary',new_b)):
        field=alphabet+'_additional_small_first_third_exclusions'
        assert not set(names)&set(joint[field]);joint[field]=sorted(set(joint[field])|set(names))
    u,b,profiles=residual(inventory,active)
    new_ju=sorted({z['joint_id'] for z in before_u}-{z['joint_id'] for z in u})
    new_jb=sorted({z['joint_id'] for z in before_b if profiles(z)}-{z['joint_id'] for z in b if profiles(z)})
    for alphabet,names in (('unrestricted',new_ju),('binary',new_jb)):
        field=alphabet+'_excluded_orbits';joint[field]=sorted(set(joint[field])|set(names))
    u,b,profiles=residual(inventory,active);ug,bg,bt,bp=len(u),len(b),sum(bool(profiles(z)) for z in b),sum(len(profiles(z)) for z in b)
    uj,bj=len({z['joint_id'] for z in u}),len({z['joint_id'] for z in b if profiles(z)})
    assert ug==83 and bg==77-len(new_b)
    joint.update(binary_remaining_orbits=bj,unrestricted_remaining_orbits=uj,latest_graph_quotient_audit=auditfile)
    admission=active['small_first_third_admission']
    admission.update(remaining_binary_typed_orbits=bt,remaining_binary_profile_pairs=bp,remaining_geometric_after_joint_and_third_exclusions=bg,
        unrestricted_remaining_geometric_in_B1_B2_inventory=ug,latest_exclusion_audit=auditfile)
    admission['latest_exclusion_audits'].append(auditfile);active['b3_third_cover']['combined_unrestricted_remaining_geometries']=ug
    coverage=dict(id=NAME,proof='../_qa/GRAPH_FIRST_TRANSPORTS.md',audit=auditfile,raw_graph_classes=679,canonical_graph_classes=26,
        labelled_first_pairs=330708,canonical_prefixes=887,tree_counts=audit['tree_counts'],maximum_basis_depth=audit['maximum_basis_depth'],
        certificate=audit['archive'],new_unrestricted_geometry_exclusions=[NAME],new_binary_geometry_exclusions=new_b,
        new_unrestricted_joint_exclusions=new_ju,new_binary_joint_exclusions=new_jb,scope=audit['scope'])
    active.setdefault('graph_first_quotient_cuts',[]).append(coverage);active['current_auxiliary_audit']=NEXT
    active['instruction']=f'Goal active/unachieved. Complete graph-first quotient excludes {NAME}. Unrestricted{ug}/joints{uj}; binary{bt} types/{bp} profiles/{bg} geometries/joints{bj}. Both F(13,9,1) remain [11,12]. Paper and publication unchanged.'
    active['general_solver_status']='Complete graph-first quotient, all native graphs/ordered pairs, independent literal/rational flag checks, fourteen metadata controls and four byte-identical isolated reports. No F value or alphabet separation.'
    frontier=ROOT/'CURRENT_FRONTIER.md';text=frontier.read_text(encoding='utf-8');heading='## Complete graph-first quotient: '+NAME
    assert heading not in text
    text+='\n'+heading+'\n\n'+(
        f'11 October2026. The complete conditional arbitrary-alphabet exclusion covers all679 retained graphs, '
        f'330708 labelled ordered first pairs and887 representatives on26 target graphs. '
        f'{audit["tree_counts"]["literal_letters"]} literal maps and{audit["tree_counts"]["nodes"]} flag nodes pass independent checks. '
        'Twelve metadata corruptions and two bijective graph-preserving protection violations are rejected. '
        'The immutable package regenerates the scope, both metadata audits and the complete flag report byte-identically.\n\n'
        f'Unrestricted frontier:{ug} geometries,{uj} joints. Binary:{bt} types,{bp} profiles,{bg} geometries,{bj} joints. '
        'Both F values at (13,9,1) remain [11,12]. No new numerical extremum or alphabet separation. '
        'Accepted partial-answer paper and release unchanged; complete-answer goal active and unachieved.\n')
    result=dict(old);result.update(date='2026-10-11',status='Audited complete graph-first quotient cut',previous_historical_audit=PREVIOUS,
        passed_audits=reports,current_audit_source_bindings_verified=bindings,paper_and_release_unchanged=True,accepted_checksum_entries=checks,
        remaining_binary_typed_third_orbits=bt,remaining_binary_profile_pairs=bp,binary_geometric_after_all_cuts=bg,
        unrestricted_geometric_B1_B2=ug,unrestricted_geometric_B3=0,unrestricted_geometric_all=ug,
        remaining_binary_third_types=bt,remaining_binary_third_pairs=bp,remaining_unrestricted_B1_B2_third_types=ug,
        remaining_unrestricted_third_types=ug,remaining_binary_geometric_after_joint_and_third_cuts=bg,
        binary_remaining_joint_orbits=bj,unrestricted_remaining_joint_orbits=uj,latest_graph_first_quotient_cut=coverage,
        new_auxiliary_certificates=[dict(path=audit['archive'],files=replay['files'],sha256=replay['sha256'],
            reproduction='../_qa/'+NAME+'_full_quotient_reproduction.json')],limits=audit['scope'])
    # Prepare every byte/hash before the authoritative writes.
    active_bytes=encoded(active);frontier_bytes=text.encode();hashes={n:digest(ROOT/n) for n in sorted(sources)}
    hashes['active_research.json']=sha256(active_bytes).hexdigest();hashes['CURRENT_FRONTIER.md']=sha256(frontier_bytes).hexdigest()
    result['source_sha256']=hashes;checkpoint_bytes=encoded(result)
    (ROOT/'active_research.json').write_bytes(active_bytes);frontier.write_bytes(frontier_bytes);output.write_bytes(checkpoint_bytes)
    print(json.dumps(dict(status='pass',authority=NEXT,audits=len(reports),sources=len(hashes),bindings=bindings,
        publication_checksums=checks,unrestricted=[ug,uj],binary=[bt,bp,bg,bj],interval=[11,12])),flush=True)
if __name__=='__main__':main()
