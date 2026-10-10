"""Independent atom reconstruction and two complete seventh row scans."""
from pathlib import Path
from itertools import combinations
import hashlib,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def mode(G):return 8 if G==[8] else (18 if G==[1,8] else 28)

def main():
    inventory=json.loads((ROOT/'b1_e26_f7_seventh_inventory.json').read_text())
    sources=[z for z in inventory['records'] if any(p['seventh_field_pairs'] for p in z['pairs'])]
    expected=json.loads((ROOT/'b1_e26_f7_seventh_rows_inventory.json').read_text())
    assert expected['status']=='complete_E26_F7_seventh_individual_necessary_row_domain'
    assert len(sources)==len(expected['records'])==7
    lines=[];keys=('preA','preB','preC','preD','preE','preF','preG')
    for source,control in zip(sources,expected['records']):
        code=mode(source['G']);hm=sum(1<<q for q in source['H'])
        assert source['G']==control['G'] and source['H']==control['H']
        outsets=({3},{0},{1,4},{5},{2,6},{7},set(source['G']))
        targets=[];sigs=[]
        for t in range(13):
            sig=tuple(t in X for X in outsets)
            if sig in sigs:continue
            sigs.append(sig);targets.append([q for q in range(13) if tuple(q in X for X in outsets)==sig])
        assert targets==control['target_atoms']==[atom['targets'] for atom in source['target_atoms']]
        assert len(targets)==(8 if code==8 else 9)
        lines.append(f"13 {code} {hm} {len(source['rows'])}");lines.append(str(len(targets)))
        for atom in targets:lines.append(' '.join(map(str,[len(atom),*atom])))
        for row in source['rows']:
            fields=[set(row[key]) for key in keys]
            atoms=[[q for q in range(13) if tuple(q in X for X in fields)==sig] for sig in sigs]
            assert atoms==row['atom_inputs'] and set().union(*map(set,atoms))==set(range(13))
            for inputs in atoms:lines.append(' '.join(map(str,[len(inputs),*inputs])))
        pairs=[xy for p in source['pairs'] for xy in p['seventh_field_pairs']]
        assert len(pairs)==len({tuple(xy) for xy in pairs}) and pairs==control['original_field_pairs']
        lines.append(str(len(pairs)));lines.extend(' '.join(map(str,xy)) for xy in pairs)
        forms=[];fibers=(*outsets[1:],set(source['H']))
        for subset in combinations(range(13),9):
            if 3 in subset and all(len(set(subset)&X)==1 for X in fibers):forms.append(sum(1<<q for q in subset))
        assert sorted(forms)==control['initial_forms'] and len(forms)==source['feasible_nine_sets']
        common=8191
        for S in forms:common&=S
        assert common==sum(1<<q for q in control['protected'])
        assert common&sum(1<<q for q in {0,3,5,7})==sum(1<<q for q in {0,3,5,7})
        assert not common&sum(1<<q for q in {2,6})
    data=('\n'.join(lines)+'\n').encode()
    assert data==(ROOT/'b1_e26_f7_seventh_rows_fields.txt').read_bytes()
    assert hashlib.sha256(data).hexdigest()==expected['manifest_sha256']
    for name,digest in expected['source_sha256'].items():assert sha(ROOT/name)==digest
    compiler=os.environ.get('CXX') or shutil.which('clang++') or shutil.which('g++')
    if compiler is None:raise RuntimeError('C++17 compiler required; set CXX')
    dest=ROOT.parent/'_qa'/'e26_f7_seventh_rows_cpp';dest.mkdir(parents=True,exist_ok=True)
    flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic'];programs=[]
    for name in ('check_e26_f7_seventh_rows','check_e26_f7_seventh_forward'):
        exe=dest/(name+('.exe' if os.name=='nt' else ''))
        run=subprocess.run([compiler,*flags,str(ROOT/(name+'.cpp')),'-o',str(exe)],capture_output=True,text=True)
        if run.returncode:raise RuntimeError(run.stdout+run.stderr)
        assert not run.stderr,run.stderr;programs.append(exe)
    raw=dest/'canonical_raw_rows.txt';kept=dest/'canonical_kept_rows.txt'
    first=subprocess.run([str(programs[0]),str(ROOT/'b1_e26_f7_seventh_rows_fields.txt'),str(raw)],capture_output=True,text=True)
    if first.returncode:raise RuntimeError(first.stdout+first.stderr)
    (dest/'reverse_scan.jsonl').write_bytes(first.stdout.encode())
    assert not first.stderr and sha(raw)==expected['canonical_raw_rows_sha256']
    reverse=[json.loads(v) for v in first.stdout.splitlines()]
    second=subprocess.run([str(programs[1]),str(ROOT/'b1_e26_f7_seventh_rows_fields.txt'),str(raw),str(kept)],capture_output=True,text=True)
    if second.returncode:raise RuntimeError(second.stdout+second.stderr)
    (dest/'forward_scan.jsonl').write_bytes(second.stdout.encode())
    assert not second.stderr and sha(kept)==expected['canonical_kept_rows_sha256']
    forward=[json.loads(v) for v in second.stdout.splitlines()]
    assert len(reverse)==len(forward)==7;reports=[]
    for a,b,control in zip(reverse,forward,expected['records']):
        assert a['status']==b['status']=='complete' and a['mode']==b['mode']==mode(control['G'])
        assert a['H_mask']==b['H_mask']==sum(1<<q for q in control['H'])
        for key in ('raw_individual_rows','kept_individual_rows','raw_normalized_row_pairs','kept_normalized_row_pairs'):
            assert a[key]==control[key],key
        assert a['checked_kept_pairs']==b['checked_kept_pairs']==control['kept_normalized_row_pairs']
        for actual in (a,b):
            assert len(actual['individual_fields'])==len(control['field_rows'])
            for field,original in zip(actual['individual_fields'],control['field_rows']):
                assert all(field[key]==original[key] for key in ('field_row','raw_rows','kept_rows','counts'))
            assert sum(actual['pair_cases'].values())==actual['checked_kept_pairs']
        print(json.dumps(dict(G=control['G'],H=control['H'],complete_pairs=a['checked_kept_pairs'],
            primary_candidates=a['candidate_images'],secondary_survivors=b['pair_cases'].get('surviving_necessary_pair',0))),flush=True)
        assert not a['candidates'] and a['candidate_images']==0 and not a['pair_cases'].get('candidate_row_pair',0)
        assert not b['pair_cases'].get('surviving_necessary_pair',0)
        reports.append(dict(G=control['G'],H=control['H'],raw_individual_rows=a['raw_individual_rows'],
            kept_individual_rows=a['kept_individual_rows'],raw_normalized_row_pairs=a['raw_normalized_row_pairs'],
            checked_kept_pairs=a['checked_kept_pairs'],reverse_pair_cases=a['pair_cases'],forward_pair_cases=b['pair_cases'],
            zero_reverse_candidates=True,zero_forward_survivors=True))
    admission=json.loads((ROOT/'b1_e26_f7_seventh_audit.json').read_text())
    assert admission['status']=='pass'
    for count in admission['counts']:
        scanned=[r['H'] for r in reports if r['G']==count['G']]
        assert scanned==count['remaining_binary_H']
        assert {tuple(h) for h in count['binary_zero_pair_H']+scanned}=={tuple(z['H']) for z in inventory['records'] if z['G']==count['G']}
    names=[Path(__file__).name,'enumerate_b1_e26_f7_seventh_rows.py','b1_e26_f7_seventh_rows_inventory.json',
        'b1_e26_f7_seventh_rows_fields.txt','check_e26_f7_seventh_rows.cpp','check_e26_f7_seventh_forward.cpp',
        'B1_E26_F7_SEVENTH_ROWS.md','b1_e26_f7_seventh_inventory.json','b1_e26_f7_seventh_audit.json',
        'B1_E26_F7_SEVENTH.md','MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json',
        'b1_sixth_inventory.json','b1_sixth_audit.json','B1_SIXTH_ENTRANCE.md','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    result=dict(status='pass',parameter=[13,9,1],E=[2,6],F=[7],alphabet='binary only',
        whole_binary_G8_G18_G28_excluded=True,build_flags=flags,bare_algorithm_controls=3,
        all_manifest_fields_checked=sum(len(z['rows']) for z in sources),
        all_parent_field_pairs_checked=sum(len(p['seventh_field_pairs']) for z in sources for p in z['pairs']),
        canonical_raw_rows_sha256=sha(raw),canonical_kept_rows_sha256=sha(kept),complete_pair_scans=reports,
        raw_individual_rows=sum(r['raw_individual_rows'] for r in reports),
        kept_individual_rows=sum(r['kept_individual_rows'] for r in reports),
        raw_normalized_pair_domain=sum(r['raw_normalized_row_pairs'] for r in reports),
        checked_retained_pairs_per_implementation=sum(r['checked_kept_pairs'] for r in reports),
        source_sha256={name:sha(ROOT/name) for name in names},
        scope='Complete exact-atom row domains and two full negative scans cover every admitted seventh type in all three E26/F7 sixth survivors. Larger alphabets are not excluded. No global F value follows without covering every other third/joint branch.')
    (ROOT/'b1_e26_f7_seventh_rows_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:result[k] for k in ('status','whole_binary_G8_G18_G28_excluded','raw_individual_rows','checked_retained_pairs_per_implementation')}),flush=True)
if __name__=='__main__':main()
