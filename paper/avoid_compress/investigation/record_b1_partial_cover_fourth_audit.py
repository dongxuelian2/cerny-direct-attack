"""Checkpoint the common-fourth reduction and two binary fourth cuts."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_19.json')
    names=['b1_partial_cover_fourth_audit.json','b1_partial_cover_fourth_pair_exclusion_audit.json']
    audits=old['passed_audits']+names;assert len(audits)==34
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        data=read(item);assert data['status']=='pass'
        for source,digest in data['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source);bindings+=1
    common=read(names[0]);cuts=read(names[1]);geometry=common['common_fourth_geometry']
    assert geometry['complete_geometric_orbits']==7 and geometry['complete_labelled_E_choices']==31
    assert geometry['remaining_binary_fourth_field_pairs']==106 and cuts['remaining_binary_fourth_field_pairs']==94
    assert cuts['remaining_binary_fourth_geometries']==4 and cuts['remaining_binary_labelled_E_choices']==22
    prefix='b1_partial_cover_fourth';readme='B1_PARTIAL_COVER_FOURTH_CERTIFICATE_README.md'
    dependencies=set(names)
    for name in names:dependencies|=set(read(name)['source_sha256'])
    contents={filename:(ROOT/filename).read_bytes() for filename in dependencies}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n' for filename,value in sorted(contents.items())).encode('utf-8')
    assert len(contents)==20
    dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None and len(archive.namelist())==20
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_b1_partial_cover_fourth_package.py';receipt='b1_partial_cover_fourth_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['inventories_reproduced_byte_identically']==reproduction['audits_reproduced_byte_identically']==2
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']}
    assert artifacts==old['accepted_artifact_sha256'] and checks==121
    active=read('active_research.json');assert active['workers']==[]
    assert active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_19.json'
    assert active['joint_fiber_cases']['binary_remaining_orbits']==23 and active['joint_fiber_cases']['unrestricted_remaining_orbits']==42
    entry=dict(parameter=[13,9,1],B=[0],C=[1,4],D=[5],proof='B1_PARTIAL_COVER_FOURTH.md',
        audits=names,complete_K_cover_kernel_patterns=646,complete_kernel_pairs=6555,
        common_E_for_arbitrary_finite_alphabet=True,complete_fourth_geometries=7,complete_labelled_E_choices=31,
        all_alphabet_excluded_E=[2],binary_only_excluded_E=[[1,2],[1,2,6]],
        remaining_binary_E=[[6],[1,6],[2,4],[2,6]],remaining_binary_fourth_geometries=4,
        remaining_binary_labelled_E_choices=22,remaining_binary_fourth_field_pairs=94,
        original_binary_third_pairs_retained=14,unrestricted_remaining_fourth_geometries=6,
        unrestricted_remaining_labelled_E_choices=30,
        scope='Geometry-specific common-fourth reduction and conditional cuts; no entire third/joint exclusion or F value')
    active['binary_B1_in_C3_singleton_D_fourth']=entry
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['B1_PARTIAL_COVER_FOURTH.md']))
    active['instruction']='Complete-answer goal active and unachieved. At B0/C14/D5 a common fresh fourth E is proved for all alphabets; E2 is cut all-alphabet, E12/E126 binary-only. Binary four fourth geometries/94 pairs still cover14 original third pairs. Joint23 binary/42 unrestricted; binary third152/784, unrestricted geometry349; both extrema[11,12]. Article and release unchanged this turn.'
    active['next_structural_work']='At B0/C14/D5, attack E6,E16,E24,E26 under effective K12 cover, preserving all extra2 collisions. Binary E12/E126 are fully excluded with two-letter witnesses. E16/E24 share only one point with C and permit an ordinary extra kernel: retain those cases and use actual image one-count constraints when ports alone leave a shield. E6 may need the fifth entrance. No outside-C injectivity, solver timeout negative or retracted higher-layer edge cap is permitted.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_20.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    assert '## Common fourth entrance in the partial-cover B1/C2 branch' not in text
    text+='''

## Common fourth entrance in the partial-cover B1/C2 branch

B1_PARTIAL_COVER_FOURTH.md retains K={1,2} as the effective P5 cover
for B={0},C={1,4}; it does not treat C as a cover. Complete independent
kernel admission has646 row patterns /6,555 pairs over54 original
typed pairs. The already excluded D={2} is only a retained control.
A literal full-letter control permits kernels14 and26 with K-cover
and protected isolation, showing why extra2 collisions cannot simply
be omitted; it is not a synchronizing equality witness.

For D={5}, a common fresh fourth fiber E is proved for every alphabet
using the dimension-five annihilator and private-cell Boolean columns.
All additional preimages are classified; no extra Boolean fiber is
discarded. Exact admission has seven E geometries /31 labelled choices.
E={2} is excluded all-alphabet: mandatory through seven makes2 isolated
in P3, reducing K to an impossible one-point P3 cover by the known bound.

For binary alphabets, E={1,2} and E={1,2,6} are excluded by explicit
two-letter protected/outside-K collisions. Strong incoming C-target
coverage is used only for binary. Complete literal n=7,8,9 pair controls
have256,3,456,73,728 assignments per E. Individual n13 port controls
enumerate40,320 F systems for each E and322,560 L systems. The paper
proof covers arbitrary coupled ordinary labels; no n13 transition-pair
scan or higher-layer edge cap is used. The two exclusions remove twelve
fourth-field pairs; four E geometries /22 labelled choices /94 field
pairs remain and still cover all fourteen earlier D={5} typed pairs.
Unrestricted retains six fourth geometries /30 labelled choices.

No whole third or joint is removed. Binary23/unrestricted42 joint cases,
binary third152/784, unrestricted third geometry349 and both F intervals
[11,12] are unchanged. The twenty-file auxiliary certificate reproduces
both generators and both independent audits byte-identically. All34
auxiliary audits and507 proof-source bindings pass; accepted article,
source archives and109-file supplement remain byte-identical, with121
current checksum entries verified. The goal is active and unachieved.
'''
    path.write_text(text,encoding='utf-8')
    sources|={'CURRENT_FRONTIER.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    for item in audits:
        for source,digest in read(item)['source_sha256'].items():assert sha(ROOT/source)==digest,(item,source)
    result=dict(date='2026-10-09',status='Audited partial-cover common-fourth reduction and two binary fourth exclusions',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_19.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        common_fourth=entry,complete_literal_controls=cuts['complete_literal_controls'],
        complete_n13_individual_port_controls=cuts['complete_n13_individual_port_controls'],
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=23,
        unrestricted_remaining_joint_orbits=42,remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=20,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='No complete answer, F value or numerical alphabet separation. Geometry-specific common-fourth proof and conditional binary cuts only; ordinary full n13 transition pairs are not enumerated.')
    assert bindings==507
    (ROOT/'AUXILIARY_AUDIT_20261009_20.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_audits=len(audits),source_hashes=len(sources),
        source_bindings=bindings,accepted_checksums=checks,certificate_files=20,
        binary_fourth_geometries=4,binary_fourth_pairs=94,interval=[11,12])))

if __name__=='__main__':main()
