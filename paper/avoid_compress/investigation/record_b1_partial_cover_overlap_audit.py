"""Record both complete binary overlap-fourth exclusions, paper unchanged."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def main():
    old=read('AUXILIARY_AUDIT_20261009_20.json')
    names=['b1_partial_cover_e24_audit.json','b1_partial_cover_e16_audit.json']
    audits=old['passed_audits']+names;assert len(audits)==36
    sources=set(old['source_sha256'])|set(audits);bindings=0
    for item in audits:
        report=read(item);assert report['status']=='pass'
        for source,digest in report['source_sha256'].items():
            assert sha(ROOT/source)==digest,(item,source);sources.add(source);bindings+=1
    for name in names:
        data=read(name);assert data['removed_fourth_field_pairs']==6
        assert data['kernel_controls']==dict(original_field_pairs=6,row_patterns=96,compatible_kernel_pairs=384)
        assert [v['complete_normalized_row_pairs'] for v in data['complete_literal_controls']]==[512,10368,294912]
        assert data['complete_n13_hard_branch_controls']['full_letter_assignments']==423360
    inventory=read('b1_partial_cover_fourth_inventory.json')['records']
    residual=[v for v in inventory if v['E'] in ([6],[2,6])]
    covered={tuple(p['original_rows']) for z in residual for p in z['pairs'] if p['fourth_field_pairs']}
    assert len(residual)==2 and len(covered)==14
    assert sum(z['labelled_E'] for z in residual)==14
    assert sum(len(p['fourth_field_pairs']) for z in residual for p in z['pairs'])==82
    prefix='b1_partial_cover_overlap';readme='B1_PARTIAL_COVER_OVERLAP_CERTIFICATE_README.md'
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
    checker='check_b1_partial_cover_overlap_package.py';receipt='b1_partial_cover_overlap_package_reproduction.json'
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
    # A geometric fifth-fiber control, not a realizable automaton claim.
    # It prevents extrapolating a common-fifth assertion to disjoint E26.
    fifth_control=dict(C=[1,4],E=[2,6],X=[1,6],Y=[2,4],
        S=[0,1,2,3,5,7,8,9,10],identity='chi_Y=chi_C+chi_E-chi_X',
        scope='Literal geometric/Boolean control only; no automaton, equality or F witness')
    X=set(fifth_control['X']);Y=set(fifth_control['Y']);C=set(fifth_control['C']);E=set(fifth_control['E']);S=set(fifth_control['S'])
    assert len(S)==9 and all(len(S&R)==1 for R in (X,Y,C,E))
    assert all(int(q in Y)==int(q in C)+int(q in E)-int(q in X) for q in range(13))
    assert all(len(R-{1,2})<=1 for R in (X,Y))
    assert all(not R<=Z and not Z<=R for i,R in enumerate((C,E,X,Y)) for Z in (C,E,X,Y)[i+1:])
    active=read('active_research.json');assert active['workers']==[]
    assert active['current_auxiliary_audit']=='AUXILIARY_AUDIT_20261009_20.json'
    entry=active['binary_B1_in_C3_singleton_D_fourth']
    entry['additional_exclusion_proofs']=['B1_PARTIAL_COVER_E24_EXCLUSION.md','B1_PARTIAL_COVER_E16_EXCLUSION.md']
    entry['audits']=list(dict.fromkeys(entry['audits']+names))
    entry['binary_only_excluded_E']=[[1,2],[1,2,6],[2,4],[1,6]]
    entry['remaining_binary_E']=[[6],[2,6]]
    entry['remaining_binary_fourth_geometries']=2;entry['remaining_binary_labelled_E_choices']=14
    entry['remaining_binary_fourth_field_pairs']=82
    active['audited_research_notes']=list(dict.fromkeys(active['audited_research_notes']+entry['additional_exclusion_proofs']))
    active['fifth_fiber_geometric_control_for_E26']=fifth_control
    active['instruction']='Complete-answer goal active and unachieved. Binary B0/C14/D5 fourth E24/E16 now excluded; only E6/E26 remain,82 field pairs covering14 original third pairs. Both overlap proofs preserve extra ordinary kernels and discharge hard cases by closed four-cycles; E24 also uses actual image one-count. Joint23/42, binary third152/784, unrestricted geometry349, both extrema[11,12]. Article/release unchanged.'
    active['next_structural_work']='Attack the two residual B0/C14/D5 fourth geometries E6 and E26. For singleton E6, prove and inventory a fifth entrance while checking the exact depth: a fifth singleton2 is only isolated in P2, so the one-point P3 cover contradiction cannot be reused. For disjoint E26 retain all same-level Boolean fibers: X16,Y24 satisfy chiY=chiC+chiE-chiX and all meet a literal nine-set once. This is a geometric control, not an equality automaton. Never assume common fifth fiber, outside-C injectivity or retracted higher-layer edge caps without proof.'
    active['current_auxiliary_audit']='AUXILIARY_AUDIT_20261009_21.json'
    (ROOT/'active_research.json').write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'CURRENT_FRONTIER.md';text=path.read_text(encoding='utf-8')
    assert '## Both overlapping fourth profiles are excluded' not in text
    text+='''

## Both overlapping fourth profiles are excluded

B1_PARTIAL_COVER_E24_EXCLUSION.md and B1_PARTIAL_COVER_E16_EXCLUSION.md
exclude the six field pairs of E24 and the six of E16 in binary
B0/C14/D5. Both keep every extra ordinary kernel and derive explicit
short protected or outside-K words. The hard profiles have kernels
forming a four-cycle. Each letter image is independent in that graph,
so no distinct pair maps into any of its edges; backward closure makes
synchronization impossible. E24 also has a no-extra-kernel exception,
where literal one-count on S,SF,SF^2 forces two S states into an
immediate L collision. No matrix multiplicity or guessed reaching word
is substituted for actual image coordinates.

Each complete independent kernel audit preserves six original field
pairs,96 row patterns (unused rows retained) and384 kernel pairs.
For each E, complete local n=7,8,9 row-pair controls have512,10,368,
294,912 assignments. Complete individual n13 hard letters include all
seven ordinary labels and423,360 full letters per E. The symbolic
graph arguments cover arbitrary coupled output choices; no n13 row-pair
scan or bounded solver negative is asserted. All392 E24 initial
nine-set controls verify its one-count exception. Both inventories
and audits reproduce byte-identically from a twenty-file certificate.

Binary B0/C14/D5 fourth admission now has only E6/E26:two geometries,
14 labelled choices and82 field pairs, still covering all fourteen
original third pairs. Unrestricted retains six fourth geometries.
Joint23/42, binary third152/784, unrestricted third geometry349 and
both F intervals[11,12] are unchanged. All36 auxiliary audits and531
proof-source bindings pass; the accepted paper,109-file supplement
and source archives remain unchanged, with121 checksum entries verified.

Next fifth-level work must use correct depths. In E6, a fifth singleton2
would only be isolated in P2, so it cannot be rejected using the earlier
one-point P3 floor. In E26, X16,Y24 satisfy chiY=chiC+chiE-chiX; all
four fibers meet S={0,1,2,3,5,7,8,9,10} once and are covered by K12.
This literal geometric control prevents an unsupported common-fifth
assumption, but it is not an automaton or equality witness. The full
goal remains active and unachieved.
'''
    path.write_text(text,encoding='utf-8')
    sources|={'CURRENT_FRONTIER.md','active_research.json',readme,Path(__file__).name,checker,receipt}
    for item in audits:
        for source,digest in read(item)['source_sha256'].items():assert sha(ROOT/source)==digest,(item,source)
    result=dict(date='2026-10-09',status='Audited complete binary E24 and E16 overlap-fourth exclusions',
        previous_historical_audit='AUXILIARY_AUDIT_20261009_20.json',active_workers=[],unresolved=[13,9,1],interval=[11,12],
        paper_and_release_unchanged=True,passed_audits=audits,current_audit_source_bindings_verified=bindings,
        binary_B1_in_C3_D5_fourth=entry,overlap_controls={name:{key:value for key,value in read(name).items() if key!='source_sha256'} for name in names},
        fifth_fiber_geometric_control=fifth_control,
        binary_remaining_first_cases=4,unrestricted_remaining_first_cases=6,binary_remaining_joint_orbits=23,
        unrestricted_remaining_joint_orbits=42,remaining_binary_typed_third_orbits=152,remaining_binary_profile_pairs=784,
        binary_geometric_after_joint_exclusions=205,binary_geometric_after_all_cuts=197,
        unrestricted_geometric_B1_B2=224,unrestricted_geometric_B3=125,unrestricted_geometric_all=349,
        auxiliary_certificate=dict(path=str(dest.relative_to(ROOT)).replace('\\','/'),files=20,sha256=sha(dest)),
        isolated_certificate_reproduction=receipt,accepted_checksum_entries=checks,accepted_artifact_sha256=artifacts,
        source_sha256={filename:sha(ROOT/filename) for filename in sorted(sources)},
        limits='No complete answer, F value or numerical alphabet separation. Binary conditional fourth exclusions only; no full thirteen-state transition-pair scan. Fifth control is geometric only.')
    assert bindings==531
    (ROOT/'AUXILIARY_AUDIT_20261009_21.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],passed_audits=len(audits),source_hashes=len(sources),
        source_bindings=bindings,accepted_checksums=checks,certificate_files=20,
        binary_fourth_geometries=2,binary_fourth_pairs=82,interval=[11,12])))
if __name__=='__main__':main()
