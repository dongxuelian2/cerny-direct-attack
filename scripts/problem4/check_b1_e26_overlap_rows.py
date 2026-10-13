"""Independent overlapping-atom row domains and complete E26 overlap sixth scans."""
from pathlib import Path
from itertools import combinations
import hashlib,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    inventory=json.loads((ROOT/'b1_e26_overlap_sixth_inventory.json').read_text())
    sources=[z for z in inventory['records'] if any(p['sixth_field_pairs'] for p in z['pairs'])]
    expected=json.loads((ROOT/'b1_e26_overlap_rows_inventory.json').read_text())
    assert expected['status']=='complete_E26_overlap_individual_necessary_row_domain'
    assert len(sources)==len(expected['records'])==5
    lines=[];keys=('preA','preB','preC','preD','preE','preF')
    for source,control in zip(sources,expected['records']):
        mode=17 if source['F']==[1,7] else 27;hm=sum(1<<q for q in source['G'])
        assert source['F']==control['F'] and source['G']==control['G']
        outsets=({3},{0},{1,4},{5},{2,6},set(source['F']))
        atom_targets=[];sigs=[]
        for t in range(13):
            sig=tuple(t in X for X in outsets)
            if sig in sigs:continue
            sigs.append(sig);atom_targets.append([q for q in range(13) if tuple(q in X for X in outsets)==sig])
        assert atom_targets==control['target_atoms']==[atom['targets'] for atom in source['target_atoms']]
        assert len(atom_targets)==8
        lines.append(f"13 {mode} {hm} {len(source['rows'])}");lines.append('8')
        for targets in atom_targets:lines.append(' '.join(map(str,[len(targets),*targets])))
        for row in source['rows']:
            fields=[set(row[key]) for key in keys]
            atoms=[[q for q in range(13) if tuple(q in X for X in fields)==sig] for sig in sigs]
            assert atoms==row['atom_inputs'] and set().union(*map(set,atoms))==set(range(13))
            for inputs in atoms:lines.append(' '.join(map(str,[len(inputs),*inputs])))
        pairs=[xy for p in source['pairs'] for xy in p['sixth_field_pairs']]
        assert len(pairs)==len({tuple(xy) for xy in pairs}) and pairs==control['original_field_pairs']
        lines.append(str(len(pairs)));lines.extend(' '.join(map(str,xy)) for xy in pairs)
        forms=[];fibers=({0},{1,4},{5},{2,6},set(source['F']),set(source['G']))
        for subset in combinations(range(13),9):
            if 3 in subset and all(len(set(subset)&X)==1 for X in fibers):forms.append(sum(1<<q for q in subset))
        assert sorted(forms)==control['initial_forms'] and len(forms)==source['feasible_nine_sets']
        common=8191
        for S in forms:common&=S
        assert common==sum(1<<q for q in control['protected']) and not common&sum(1<<q for q in {1,2,6,7})
    data=('\n'.join(lines)+'\n').encode()
    assert data==(ROOT/'b1_e26_overlap_rows_fields.txt').read_bytes()
    assert hashlib.sha256(data).hexdigest()==expected['manifest_sha256']
    for name,digest in expected['source_sha256'].items():assert sha(ROOT/name)==digest
    compiler=os.environ.get('CXX') or shutil.which('clang++') or shutil.which('g++')
    if compiler is None:raise RuntimeError('C++17 compiler required; set CXX')
    dest=ROOT/'experimental'/'e26_overlap_rows_cpp';dest.mkdir(parents=True,exist_ok=True)
    flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic'];programs=[]
    for name in ('check_e26_overlap_rows','check_e26_overlap_forward'):
        exe=dest/(name+('.exe' if os.name=='nt' else ''))
        run=subprocess.run([compiler,*flags,str(ROOT/(name+'.cpp')),'-o',str(exe)],capture_output=True,text=True)
        if run.returncode:raise RuntimeError(run.stdout+run.stderr)
        assert not run.stderr,run.stderr;programs.append(exe)
    raw=dest/'canonical_raw_rows.txt';kept=dest/'canonical_kept_rows.txt'
    first=subprocess.run([str(programs[0]),str(ROOT/'b1_e26_overlap_rows_fields.txt'),str(raw)],capture_output=True,text=True)
    if first.returncode:raise RuntimeError(first.stdout+first.stderr)
    (dest/'reverse_scan.jsonl').write_bytes(first.stdout.encode())
    assert not first.stderr and sha(raw)==expected['canonical_raw_rows_sha256']
    reverse=[json.loads(v) for v in first.stdout.splitlines()]
    second=subprocess.run([str(programs[1]),str(ROOT/'b1_e26_overlap_rows_fields.txt'),str(raw),str(kept)],capture_output=True,text=True)
    if second.returncode:raise RuntimeError(second.stdout+second.stderr)
    (dest/'forward_scan.jsonl').write_bytes(second.stdout.encode())
    assert not second.stderr and sha(kept)==expected['canonical_kept_rows_sha256']
    forward=[json.loads(v) for v in second.stdout.splitlines()]
    assert len(reverse)==len(forward)==5;reports=[]
    for a,b,control in zip(reverse,forward,expected['records']):
        assert a['status']==b['status']=='complete' and a['mode']==b['mode']==(17 if control['F']==[1,7] else 27)
        assert a['G_mask']==b['G_mask']==sum(1<<q for q in control['G'])
        for key in ('raw_individual_rows','kept_individual_rows','raw_normalized_row_pairs','kept_normalized_row_pairs'):
            assert a[key]==control[key],key
        assert a['checked_kept_pairs']==b['checked_kept_pairs']==control['kept_normalized_row_pairs']
        for actual in (a,b):
            assert len(actual['individual_fields'])==len(control['field_rows'])
            for field,original in zip(actual['individual_fields'],control['field_rows']):
                assert all(field[key]==original[key] for key in ('field_row','raw_rows','kept_rows','counts'))
            assert sum(actual['pair_cases'].values())==actual['checked_kept_pairs']
        print(json.dumps(dict(F=control['F'],G=control['G'],complete_pairs=a['checked_kept_pairs'],
            primary_candidates=a['candidate_images'],secondary_survivors=b['pair_cases'].get('surviving_necessary_pair',0))),flush=True)
        assert not a['candidates'] and a['candidate_images']==0 and not a['pair_cases'].get('candidate_row_pair',0)
        assert not b['pair_cases'].get('surviving_necessary_pair',0)
        reports.append(dict(F=control['F'],G=control['G'],raw_individual_rows=a['raw_individual_rows'],
            kept_individual_rows=a['kept_individual_rows'],raw_normalized_row_pairs=a['raw_normalized_row_pairs'],
            checked_kept_pairs=a['checked_kept_pairs'],reverse_pair_cases=a['pair_cases'],forward_pair_cases=b['pair_cases'],
            zero_reverse_candidates=True,zero_forward_survivors=True))
    assert [r['raw_individual_rows'] for r in reports]==[8640,12000,5280,5280,9600]
    assert [r['checked_kept_pairs'] for r in reports]==[0,912384,345600,82944,0]
    seventh=json.loads((ROOT/'b1_e26_overlap_sixth_audit.json').read_text())
    assert seventh['status']=='pass'
    for count in seventh['counts']:
        scanned=[r['G'] for r in reports if r['F']==count['F']]
        assert scanned==count['remaining_binary_G']
        assert {tuple(h) for h in count['binary_zero_pair_G']+scanned}=={tuple(z['G']) for z in inventory['records'] if z['F']==count['F']}
    fifth=json.loads((ROOT/'b1_fifth_inventory.json').read_text())['records']
    F7=next(z for z in fifth if z['E']==[2,6] and z['F']==[7])
    assert F7['labelled_F']==6 and sum(len(p['fifth_field_pairs']) for p in F7['pairs'])==122
    assert len({tuple(p['original_third_rows']) for p in F7['pairs'] if p['fifth_field_pairs']})==14
    assert len({tuple(p['original_fourth_rows']) for p in F7['pairs'] if p['fifth_field_pairs']})==41
    removed=[z for z in fifth if z['E']==[2,6] and z['F'] in ([1,7],[2,7])]
    assert sum(len(p['fifth_field_pairs']) for z in removed for p in z['pairs'])==39
    sixth=json.loads((ROOT/'b1_sixth_inventory.json').read_text())['records']
    residual=[z for z in sixth if z['E']==[2,6] and z['F']==[7] and z['G'] in ([8],[1,8],[2,8])]
    assert len(residual)==3 and sum(z['labelled_G'] for z in residual)==15
    assert sum(len(p['sixth_field_pairs']) for z in residual for p in z['pairs'])==443
    names=[Path(__file__).name,'enumerate_b1_e26_overlap_rows.py','b1_e26_overlap_rows_inventory.json',
        'b1_e26_overlap_rows_fields.txt','check_e26_overlap_rows.cpp','check_e26_overlap_forward.cpp',
        'PROOF.md#problem4-b1-e26-overlap-exclusion','b1_e26_overlap_sixth_inventory.json','b1_e26_overlap_sixth_audit.json',
        'PROOF.md#problem4-b1-e26-overlap-sixth','PROOF.md#problem4-mandatory-core-isolation','mandatory_core_isolation_audit.json',
        'b1_fifth_inventory.json','b1_fifth_audit.json','PROOF.md#problem4-b1-fifth-entrance',
        'b1_sixth_inventory.json','b1_sixth_audit.json','PROOF.md#problem4-b1-sixth-entrance','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    result=dict(status='pass',parameter=[13,9,1],E=[2,6],alphabet='binary only',
        whole_binary_F17_F27_excluded=True,build_flags=flags,bare_algorithm_controls=3,
        removed_fifth_field_pairs=39,remaining_binary_F=[[7]],remaining_fifth_labels=6,remaining_fifth_field_pairs=122,
        remaining_binary_G=[[8],[1,8],[2,8]],remaining_sixth_geometries=3,remaining_sixth_labels=15,remaining_sixth_field_pairs=443,
        all_original_third_pairs_retained=14,all_original_fourth_pairs_retained=41,
        all_manifest_fields_checked=244,all_parent_field_pairs_checked=156,
        canonical_raw_rows_sha256=sha(raw),canonical_kept_rows_sha256=sha(kept),complete_pair_scans=reports,
        raw_individual_rows=40800,kept_individual_rows=27264,raw_normalized_pair_domain=2592000,
        checked_retained_pairs_per_implementation=1340928,
        source_sha256={name:sha(ROOT/name) for name in names},
        scope='Complete overlapping-atom row domains and two full negative scans, covering all eight sixth types per fifth, exclude entire binary E26/F17,F27. Zero-pair types checked independently. Larger alphabets retain cases. E26/F7 and all third parents remain; no whole E26/third/joint or extremal F value.')
    (ROOT/'b1_e26_overlap_rows_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(dict(status='pass',whole_binary_F17_F27_excluded=True,raw_rows=40800,
        complete_pairs_per_implementation=1340928)),flush=True)
if __name__=='__main__':main()
