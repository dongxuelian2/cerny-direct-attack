"""Independent exact G28 domains, two full scans, and E6/F7 composition."""
from pathlib import Path
from itertools import combinations
import hashlib,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    inventory=json.loads((ROOT/'b1_g28_seventh_inventory.json').read_text(encoding='utf-8'))
    parent=[z for z in inventory['records'] if z['H'] in ([9],[2,9])]
    expected=json.loads((ROOT/'b1_g28_rows_inventory.json').read_text(encoding='utf-8'))
    assert expected['status']=='complete_G28_individual_necessary_row_domain'
    lines=[];keys=('preA','preB','preC','preD','preE','preF','preG')
    for source,control in zip(parent,expected['records']):
        mode=9 if source['H']==[9] else 29;size=128 if mode==9 else 96
        assert source['H']==control['H'] and len(source['rows'])==size
        lines.append(f'13 {mode} {size}')
        for row in source['rows']:
            fields=[set(row[key]) for key in keys]
            assert sum(map(len,fields))==len(set().union(*fields))
            for key in keys:lines.append(' '.join(map(str,[len(row[key]),*row[key]])))
        pairs=[xy for p in source['pairs'] for xy in p['seventh_field_pairs']]
        assert len(pairs)==len({tuple(xy) for xy in pairs})==(1094 if mode==9 else 243)
        assert pairs==control['original_field_pairs']
        lines.append(str(len(pairs)));lines.extend(' '.join(map(str,xy)) for xy in pairs)
        forms=[];fibers=({0},{1,4},{5},{6},{7},{2,8},set(source['H']))
        for subset in combinations(range(13),9):
            if 3 in subset and all(len(set(subset)&X)==1 for X in fibers):forms.append(sum(1<<q for q in subset))
        assert sorted(forms)==control['initial_forms'] and len(forms)==12
        common=8191
        for S in forms:common&=S
        assert common==sum(1<<q for q in control['protected']) and not common&((1<<2)|(1<<8))
    data=('\n'.join(lines)+'\n').encode('utf-8')
    assert data==(ROOT/'b1_g28_rows_fields.txt').read_bytes()
    assert hashlib.sha256(data).hexdigest()==expected['manifest_sha256']
    for name,digest in expected['source_sha256'].items():assert sha(ROOT/name)==digest
    compiler=os.environ.get('CXX') or shutil.which('clang++') or shutil.which('g++')
    if compiler is None:raise RuntimeError('C++17 compiler required; set CXX')
    dest=ROOT/'experimental'/'g28_rows_cpp';dest.mkdir(parents=True,exist_ok=True)
    flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic'];programs=[]
    for name in ('check_g28_rows','check_g28_forward'):
        exe=dest/(name+('.exe' if os.name=='nt' else ''))
        run=subprocess.run([compiler,*flags,str(ROOT/(name+'.cpp')),'-o',str(exe)],capture_output=True,text=True)
        if run.returncode:raise RuntimeError(run.stdout+run.stderr)
        assert not run.stderr,run.stderr;programs.append(exe)
    raw=dest/'canonical_raw_rows.txt';kept=dest/'canonical_kept_rows.txt'
    first=subprocess.run([str(programs[0]),str(ROOT/'b1_g28_rows_fields.txt'),str(raw)],capture_output=True,text=True)
    if first.returncode:raise RuntimeError(first.stdout+first.stderr)
    assert not first.stderr and sha(raw)==expected['canonical_raw_rows_sha256']
    reverse=[json.loads(v) for v in first.stdout.splitlines()]
    second=subprocess.run([str(programs[1]),str(ROOT/'b1_g28_rows_fields.txt'),str(raw),str(kept)],capture_output=True,text=True)
    if second.returncode:raise RuntimeError(second.stdout+second.stderr)
    assert not second.stderr and sha(kept)==expected['canonical_kept_rows_sha256']
    forward=[json.loads(v) for v in second.stdout.splitlines()]
    assert len(reverse)==len(forward)==len(expected['records'])==2
    reports=[]
    for a,b,control in zip(reverse,forward,expected['records']):
        assert a['status']==b['status']=='complete' and a['mode']==b['mode']==(9 if control['H']==[9] else 29)
        for key in ('raw_individual_rows','kept_individual_rows','raw_normalized_row_pairs','kept_normalized_row_pairs'):
            assert a[key]==control[key],key
        assert a['checked_kept_pairs']==b['checked_kept_pairs']==control['kept_normalized_row_pairs']
        for actual in (a,b):
            assert len(actual['individual_fields'])==len(control['field_rows'])
            for field,original in zip(actual['individual_fields'],control['field_rows']):
                assert all(field[key]==original[key] for key in ('field_row','raw_rows','kept_rows','counts'))
            assert sum(actual['pair_cases'].values())==actual['checked_kept_pairs']
        assert not a['candidates'] and a['candidate_images']==0 and not a['pair_cases'].get('candidate_row_pair',0)
        assert not b['pair_cases'].get('surviving_necessary_pair',0)
        reports.append(dict(H=control['H'],raw_individual_rows=a['raw_individual_rows'],kept_individual_rows=a['kept_individual_rows'],
            raw_normalized_row_pairs=a['raw_normalized_row_pairs'],checked_kept_pairs=a['checked_kept_pairs'],
            reverse_pair_cases=a['pair_cases'],forward_pair_cases=b['pair_cases'],zero_reverse_candidates=True,zero_forward_survivors=True))
        print(json.dumps(dict(H=control['H'],status='pass',complete_pairs=a['checked_kept_pairs'],survivors=0)),flush=True)
    assert [r['raw_individual_rows'] for r in reports]==[31488,19392]
    assert [r['checked_kept_pairs'] for r in reports]==[6550272,1109376]
    seventh=json.loads((ROOT/'b1_g28_seventh_audit.json').read_text(encoding='utf-8'))
    assert seventh['status']=='pass'
    assert {tuple(h) for h in seventh['all_alphabet_crossed_exclusions']+[seventh['binary_only_excluded_H']]+[[9],[2,9]]}=={tuple(z['H']) for z in inventory['records']}
    sixth=json.loads((ROOT/'b1_sixth_inventory.json').read_text(encoding='utf-8'))['records']
    earlier=json.loads((ROOT/'b1_e6_f7_sixth_audit.json').read_text(encoding='utf-8'))
    G8=json.loads((ROOT/'b1_g8_unpaired_audit.json').read_text(encoding='utf-8'))
    assert earlier['status']==G8['status']=='pass' and G8['whole_binary_G8_excluded']
    original={tuple(z['G']) for z in sixth if z['E']==[6] and z['F']==[7]}
    assert {tuple(v) for v in earlier['excluded_G']+[[8],[2,8]]}==original and len(original)==7
    fifth=json.loads((ROOT/'b1_fifth_inventory.json').read_text(encoding='utf-8'))['records']
    remaining=next(z for z in fifth if z['E']==[6] and z['F']==[2,7])
    assert remaining['labelled_F']==6 and sum(len(p['fifth_field_pairs']) for p in remaining['pairs'])==122
    assert len({tuple(p['original_third_rows']) for p in remaining['pairs'] if p['fifth_field_pairs']})==14
    names=[Path(__file__).name,'enumerate_b1_g28_rows.py','b1_g28_rows_inventory.json','b1_g28_rows_fields.txt',
        'check_g28_rows.cpp','check_g28_forward.cpp','PROOF.md#problem4-b1-e6-f7-exclusion',
        'b1_g28_seventh_inventory.json','b1_g28_seventh_audit.json','PROOF.md#problem4-b1-g28-seventh-entrance',
        'PROOF.md#problem4-mandatory-core-isolation','mandatory_core_isolation_audit.json','b1_sixth_inventory.json','PROOF.md#problem4-b1-sixth-entrance',
        'b1_e6_f7_sixth_audit.json','PROOF.md#problem4-b1-e6-f7-paired-sixth-exclusions',
        'b1_g8_unpaired_audit.json','PROOF.md#problem4-b1-e6-f7-g8-exclusion','b1_fifth_inventory.json',
        'PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    result=dict(status='pass',parameter=[13,9,1],branch=dict(E=[6],F=[7],G=[2,8]),alphabet='binary only',
        excluded_H=[[9],[2,9]],whole_binary_G28_excluded=True,whole_binary_E6_F7_excluded=True,build_flags=flags,
        bare_algorithm_controls=3,all_manifest_fields_checked=224,all_parent_field_pairs_checked=1337,
        canonical_raw_rows_sha256=sha(raw),canonical_kept_rows_sha256=sha(kept),complete_pair_scans=reports,
        raw_normalized_pair_domain=43812864,checked_retained_pairs_per_implementation=7659648,
        remaining_binary_E6_F=[[2,7]],remaining_E6_fifth_field_pairs=122,all_original_third_pairs_retained=14,
        source_sha256={name:sha(ROOT/name) for name in names},
        scope='Complete binary G28 H9/H29 domains and two full negative scans. With all new H cases and previous six G cuts excludes entire conditional E6/F7 fifth geometry. No other E/fifth/third/joint or arbitrary-alphabet E6/F7 exclusion, exact F value or numerical separation.')
    (ROOT/'b1_g28_rows_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(dict(status='pass',whole_binary_G28_excluded=True,whole_binary_E6_F7_excluded=True,
        raw_individual_rows=50880,complete_pairs_per_implementation=7659648,remaining_E6_fifth_pairs=122)),flush=True)
if __name__=='__main__':main()
