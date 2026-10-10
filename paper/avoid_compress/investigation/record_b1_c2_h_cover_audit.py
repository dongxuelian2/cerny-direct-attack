"""Record the full binary b1_in_c4 exclusion; preserve both F intervals."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_16.json');name='b1_c2_h_cover_audit.json';new=read(name)
    audits=old['passed_audits']+[name];sources=set(audits)
    for item in audits:
        data=read(item);assert data['status']=='pass'
        for source,digest in data['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source)
    assert [z['kernel_pairs'] for z in new['kernels']]==[497,54]
    assert [z['complete_row_assignments'] for z in new['complete_literal_smaller_controls']]==[752,11952,301824]
    active=read('active_research.json');assert active['workers']==[]
    joint=active['joint_fiber_cases'];oldj=set(joint['binary_excluded_orbits']);oldthird=set(joint['binary_additional_small_first_third_exclusions'])
    assert len(oldj)==18 and joint['binary_remaining_orbits']==25
    records=read('small_first_third_inventory.json')['records']
    before=[v for v in records if v['joint_id'] not in oldj and v['id'] not in oldthird and v['binary_profile_pairs']]
    assert len(before)==163 and sum(len(v['binary_profile_pairs']) for v in before)==901
    selected=[v for v in before if v['joint_id']=='b1_in_c4']
    assert [v['D'] for v in selected]==[[4],[1,4]] and [len(v['binary_profile_pairs']) for v in selected]==[14,3]
    assert [v['labelled_D'] for v in selected]==[9,18]
    newj=oldj|{'b1_in_c4'}
    kept=[v for v in records if v['joint_id'] not in newj and v['id'] not in oldthird and v['binary_profile_pairs']]
    geometric=[v for v in records if v['joint_id'] not in newj]
    assert len(kept)==161 and sum(len(v['binary_profile_pairs']) for v in kept)==884 and len(geometric)==208
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    prefix='b1_c2_h_cover';readme='B1_C2_H_COVER_CERTIFICATE_README.md'
    contents={filename:(ROOT/filename).read_bytes() for filename in set(new['source_sha256'])|{name}}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n'
        for filename,value in sorted(contents.items())).encode('utf-8')
    assert len(contents)==13
    dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert len(archive.namelist())==13
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_b1_c2_h_cover_package.py';receipt='b1_c2_h_cover_package_reproduction.json'
    subprocess.run([sys.executable,str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['reproduced_audit_byte_identical'] and reproduction['reproduced_inventory_byte_identical']
    joint['binary_excluded_orbits']=sorted(newj);joint['binary_remaining_orbits']=24
    joint['binary_C2_H_cover_audit']=name
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['B1_C2_H_COVER_EXCLUSION.md']))
    active['binary_C2_H_cover_exclusion']=dict(parameter=[13,9,1],B=[0],C=[1,2],third_profiles=[[4],[1,4]],
        proof='B1_C2_H_COVER_EXCLUSION.md',audit=name,original_pairs_discharged=17,
        scope='Conditional binary full joint exclusion using effective C-cover, no C3 budget, new F value or alphabet separation')
    small=active['small_first_third_admission'];small['remaining_geometric_after_joint_exclusions']=208
    small['remaining_binary_typed_orbits']=161;small['remaining_binary_profile_pairs']=884
    small['latest_exclusion_audits']=list(dict.fromkeys(small['latest_exclusion_audits']+[name]))
    active['instruction']='Complete-answer goal active and unachieved. Full binary b1_in_c4 is excluded for both D profiles, all17 pairs, using effective C-cover and short words/backward graphs. Binary joint24/unrestricted43; residual third admission161/884; both extrema[11,12]. Accepted article/release unchanged; workers terminal.'
    active['general_solver_status']='86 old bounded diagnostics remain uncertified. Separate complete proofs exclude19 binary joint records, now including b1_in_c4 via both third profiles. No full13-state transition scan, new F value or numerical alphabet separation is claimed.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_17.json'
    active['next_structural_work']='At(13,9,1), binary joint24/unrestricted43 remain. Next B={0},C={1} (b1_in_c2) has D={2},{4},{2,4}, fourteen pairs each. C is singleton and mandatory through9, so H0,1 are protected in P5; the effective P5 cover is {2}. For D={2}, allH points appear mandatory/isolate throughP4: audit the candidate all-alphabet permutation obstruction first, without yet claiming it. Then re-derive all D4/D24 fibers and row kernels. Do not import the C2/C3 collision budgets. Keep extra Boolean fibers in B2 profiles; solver timeouts are not negatives.'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    sources|={'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    result=dict(date='2026-10-09',status='Audited binary B1/C2 effective-H-cover whole joint exclusion; no new F value',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_16.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,new_binary_joint_exclusion='b1_in_c4',third_profiles_discharged=[[4],[1,4]],
        original_profile_pairs_discharged=17,immediate_kernel_controls=new['kernels'],ordinary_port_controls=new['complete_n13_ordinary_port_controls'],
        literal_control_row_assignments=[752,11952,301824],binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=24,unrestricted_remaining_joint_orbits=43,
        remaining_binary_typed_third_orbits=161,remaining_binary_profile_pairs=884,remaining_geometric_after_joint_exclusions=208,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=13,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='No complete answer, new F value or numerical alphabet separation. Complete symbolic conditional binary joint exclusion with independent kernel/graph/row and individual ordinary-port controls, not full13-state transition enumeration.')
    (ROOT/'AUXILIARY_AUDIT_20261009_17.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',audits=len(audits),sources=len(sources),accepted_checks=checks,certificate_files=13,
        binary_joint=24,unrestricted_joint=43,remaining_binary_typed_third=161,remaining_letter_pairs=884,active_workers=0)))

if __name__=='__main__':main()
