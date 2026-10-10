"""Checkpoint the complete B3 cover cut and citation-only paper rebuild."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    old=read('AUXILIARY_AUDIT_20261009_18.json');name='b3_third_cover_audit.json';new=read(name)
    audits=old['passed_audits']+[name];assert len(audits)==32
    sources=set(old['source_sha256'])|set(audits)
    bindings=0
    for item in audits:
        data=read(item);assert data['status']=='pass'
        for source,digest in data['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source);bindings+=1
    assert new['complete_geometric_orbits']==127 and new['complete_labelled_D_choices']==827
    assert new['additional_boolean_fiber_orbits']==18 and new['unrestricted_geometric_remaining']==349
    prefix='b3_third_cover';readme='B3_THIRD_COVER_CERTIFICATE_README.md'
    contents={filename:(ROOT/filename).read_bytes() for filename in set(new['source_sha256'])|{name}}
    contents['README.md']=(ROOT/readme).read_bytes()
    contents['CHECKSUMS.txt']=''.join(hashlib.sha256(value).hexdigest()+'  '+filename+'\n' for filename,value in sorted(contents.items())).encode('utf-8')
    assert len(contents)==18
    dest=ROOT/'certificates'/f'{prefix}.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,value in sorted(contents.items()):
            info=zipfile.ZipInfo(prefix+'/'+filename,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,value)
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None and len(archive.namelist())==18
        for filename,value in contents.items():assert archive.read(prefix+'/'+filename)==value
    checker='check_b3_third_cover_package.py';receipt='b3_third_cover_package_reproduction.json'
    subprocess.run([sys.executable,'-B',str(ROOT/checker)],cwd=ROOT,check=True)
    reproduction=read(receipt)
    assert reproduction['status']=='pass' and reproduction['sha256']==sha(dest)
    assert reproduction['reproduced_audit_byte_identical'] and reproduction['reproduced_inventory_byte_identical']
    paper_audit=json.loads((PAPER/'_qa/reference_variant_release_audit.json').read_text(encoding='utf-8'))
    assert paper_audit['status']=='pass' and paper_audit['source_diff_is_title_only'] and paper_audit['pdf_text_diff_is_title_only']
    assert paper_audit['reproducibility_archive_byte_identical'] and paper_audit['current_checksum_entries_verified']==121
    artifacts={filename:sha(PAPER/filename) for filename in old['accepted_artifact_sha256']}
    assert artifacts==paper_audit['accepted_artifact_sha256']
    assert artifacts['release/reproducibility.zip']==old['accepted_artifact_sha256']['release/reproducibility.zip']
    checks=0
    for table,base in [(PAPER/'SHA256SUMS.txt',PAPER),(PAPER/'release/ARCHIVE_SHA256SUMS.txt',PAPER/'release')]:
        for line in table.read_text(encoding='utf-8').splitlines():
            digest,filename=line.split('  ',1);assert sha(base/filename)==digest;checks+=1
    assert checks==121
    active=read('active_research.json');assert active['workers']==[]
    assert active['current_auxiliary_audit'] in ('AUXILIARY_AUDIT_20261009_18.json','AUXILIARY_AUDIT_20261009_19.json')
    joint=active['joint_fiber_cases'];assert joint['binary_remaining_orbits']==23 and joint['unrestricted_remaining_orbits']==42
    assert all(v.startswith('b3_') for v in new['excluded_profiles'])
    joint['unrestricted_additional_B3_third_exclusions']=new['excluded_profiles']
    joint['b3_third_cover_audit']=name
    active['b3_third_cover']=dict(parameter=[13,9,1],proof='B3_THIRD_COVER.md',audit=name,
        complete_joint_cases=14,geometric_orbits=127,labelled_D_choices=827,
        extra_boolean_fiber_orbits=18,excluded_profiles=new['excluded_profiles'],
        unrestricted_remaining_B3_geometries=125,combined_B1_B2_B3_geometries=362,
        combined_unrestricted_remaining_geometries=349,alphabet='arbitrary finite',
        scope='Necessary geometry and existing-bound corollary only; binary B3 already excluded; no F value')
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+['B3_THIRD_COVER.md']))
    active.pop('paper_reference_title_correction_pending',None)
    active['paper_reference_title_variant_alignment']=dict(status='complete',key='szykula2018',
        uses_article_pdf_plural_title=True,publisher_metadata_singular_is_valid_variant=True,
        report='../_qa/reference_variant_release_audit.json',math_unchanged=True,
        supplement_files_unchanged=109,pdf_pages=7,latex_warnings=0,
        historical_primary_metadata='compression_cover_primary_source.json is an immutable earlier audit snapshot; its pending field is superseded here')
    active['instruction']='Complete-answer goal active and unachieved. Complete B3 third admission now127/827 with18 extra-fiber orbits; two additional all-alphabet third cuts. Combined geometric362, unrestricted residual349. Joint23 binary/42 unrestricted; binary third152/784; both extrema[11,12]. Paper citation title aligned with article PDF variant,7pages zero warnings; math and109-file supplement unchanged.'
    active['general_solver_status']='86 old bounded diagnostics remain uncertified. Complete proofs exclude20 binary joint records, one for every alphabet. Known-cover cut excludes13 of362 all-alphabet third geometries, with18 B3 extra-fiber orbits retained. No full13-state transition scan, F value or numerical alphabet separation is claimed.'
    active['next_structural_work']='At(13,9,1), binary23/unrestricted42 joints remain. All B1/B2/B3 third geometry is now inventoried, with349 unrestricted geometries surviving the known-cover cut. Binary B1_in_c3 remains after D2 exclusion: exploit its effective two-point H-cover without importing C2/C3 kernel budgets. Further entrances must preserve all same-level Boolean fibers. Never use solver timeouts or retracted edge caps as negatives.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_19.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    frontier='''

## B3 third geometry is now complete; two additional all-alphabet cuts

B3_THIRD_COVER.md and b3_third_cover_audit.json extend the known-cover
intersection test to all fourteen B3 joints. There are127 geometric
orbits /827 labelled D choices, with eighteen extra-Boolean-fiber orbits
retained. The independent bit-mask checker matches all36 previously
inventoried B3 third geometries and tests409,365 literal nine-family
memberships and7,397 candidate-R span cases. Rank over F_101 is exact
over Q by the proved bound on Boolean minors; no float or timeout is used.

The two exclusions are b3_mixed_c4_third2 (B014,C24,D02) and
b3_mixed_c6_third5 (B014,C02,D24). The same three Boolean one-count
equations force states1,2 into every image through depth eight. Each
singleton is isolated in P4 by the protected-pair inequality. Stripping
these two H points leaves the one-point cover{0}, contrary to known
three-letter compression of Q minus{0}. The two joints themselves
remain admitted for unrestricted alphabets; other D geometries survive.

Combined B1/B2/B3 geometry is362 orbits /2,309 labelled choices. The
known-cover cut excludes13 geometries, leaving224 B1/B2 +125 B3 =349
unrestricted geometries. This counts necessary configurations, not
automata. Binary admission remains23 joints and152 typed third orbits /
784 pairs because its B3 joints were already excluded. Unrestricted
joint admission remains42. Both extrema at(13,9,1) remain[11,12].

The new eighteen-file auxiliary certificate reproduces its generator
and independent checker byte-identically. All32 auxiliary audits and
their current source bindings pass. The accepted manuscript has a
citation-title variant alignment only, and has been recompiled with
seven pages, zero warnings and current-page visual review. Its109-file
supplement and reproducibility ZIP remain byte-identical. The article
PDF has plural Reset Words, while DROPS metadata has singular Reset
Word: the earlier instruction calling the singular a typo is superseded
by this verified variant distinction. Main source and extracted PDF
text differ only in this reference title. The arXiv source and complete
submission archives are refreshed;121 current checksum entries pass.
The complete-answer goal remains active and unachieved.
'''
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    if '## B3 third geometry is now complete;' not in text:
        path.write_text(text+frontier,encoding='utf-8')
    # JOINT_FIBER_ORBITS.md is bound by the historical joint proof audit.
    # Keep its bytes intact; the current delta belongs in the frontier
    # and new proof note instead of rewriting a verified proof dependency.
    sources|={'CURRENT_FRONTIER.md','JOINT_FIBER_ORBITS.md','active_research.json',readme,
        Path(__file__).name,checker,receipt,'../_qa/reference_variant_release_audit.json',
        '../_qa/check_reference_variant_release.py','../_qa/align_reference_pdf_title.py',
        '../_qa/reference_variant_before.json'}
    # Recheck proof bindings after the mutable frontier notes are updated.
    for item in audits:
        for source,digest in read(item)['source_sha256'].items():assert sha(ROOT/source)==digest,(item,source)
    result=dict(date='2026-10-09',status='Audited complete B3 geometry and two known-bound cuts; citation-only manuscript rebuild',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_18.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        mathematical_paper_and_supplement_unchanged=True,paper_and_release_unchanged=False,
        passed_audits=audits,current_audit_source_bindings_verified=bindings,
        b3_controls={key:value for key,value in new.items() if key not in ('source_sha256','scope')},
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,
        binary_remaining_joint_orbits=23,unrestricted_remaining_joint_orbits=42,
        remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=18,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,paper_reference_variant_audit='../_qa/reference_variant_release_audit.json',
        accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        previous_accepted_artifact_sha256=old['accepted_artifact_sha256'],
        accepted_artifact_delta_reason='Citation title convention aligned to article PDF; publisher singular metadata is valid; math/supplement unchanged',
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='No complete answer, new F value or numerical alphabet separation. Necessary B3 geometry and conditional known-cover corollary only. Full thirteen-state row enumeration has not occurred.')
    (ROOT/'AUXILIARY_AUDIT_20261009_19.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_auxiliary_audits=len(audits),source_hashes=len(sources),
        current_source_bindings=bindings,accepted_checksums=checks,auxiliary_certificate_files=18,
        binary_joints=23,unrestricted_joints=42,binary_third_orbits=152,binary_pairs=784,
        unrestricted_geometric_all=349,interval=[11,12])))

if __name__=='__main__':main()
