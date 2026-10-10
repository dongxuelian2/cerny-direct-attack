"""Independent full coverage and two coupled E6/F7/G8 row scans."""
from pathlib import Path
from itertools import combinations
import hashlib,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    inventory=json.loads((ROOT/'b1_seventh_inventory.json').read_text(encoding='utf-8'))
    parent=[z for z in inventory['records'] if z['H'] in ([9],[2,9])]
    expected=json.loads((ROOT/'b1_g8_unpaired_rows.json').read_text(encoding='utf-8'))
    assert expected['status']=='complete_individual_necessary_row_domain'
    # Reconstruct every manifest field and original labelled pair, no generator import.
    lines=[]
    keys=('preA','preB','preC','preD','preE','preF','preG')
    for source,control in zip(parent,expected['records']):
        mode=9 if source['H']==[9] else 29
        assert source['H']==control['H'] and len(source['rows'])==128
        lines.append(f'13 {mode} 128')
        for row in source['rows']:
            fields=[set(row[key]) for key in keys]
            assert sum(map(len,fields))==len(set().union(*fields))
            for key in keys:lines.append(' '.join(map(str,[len(row[key]),*row[key]])))
        pairs=[xy for p in source['pairs'] for xy in p['seventh_field_pairs']]
        assert len(pairs)==len({tuple(xy) for xy in pairs})==1094
        assert pairs==control['original_field_pairs']
        lines.append('1094');lines.extend(' '.join(map(str,xy)) for xy in pairs)
        forms=[];fibers=({0},{1,4},{5},{6},{7},{8},set(source['H']))
        for subset in combinations(range(13),9):
            if 3 in subset and all(len(set(subset)&X)==1 for X in fibers):
                forms.append(sum(1<<q for q in subset))
        assert sorted(forms)==control['initial_forms']
        assert len(forms)==(8 if mode==9 else 12)
    data=('\n'.join(lines)+'\n').encode('utf-8')
    assert data==(ROOT/'b1_g8_unpaired_fields.txt').read_bytes()
    assert hashlib.sha256(data).hexdigest()==expected['manifest_sha256']
    for name,digest in expected['source_sha256'].items():assert sha(ROOT/name)==digest
    compiler=os.environ.get('CXX') or shutil.which('clang++') or shutil.which('g++')
    if compiler is None:raise RuntimeError('C++17 compiler required; set CXX')
    dest=ROOT.parent/'_qa'/'g8_unpaired_cpp';dest.mkdir(parents=True,exist_ok=True)
    flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic'];programs=[]
    for name in ('check_g8_unpaired_rows','check_g8_unpaired_forward'):
        exe=dest/(name+('.exe' if os.name=='nt' else ''))
        run=subprocess.run([compiler,*flags,str(ROOT/(name+'.cpp')),'-o',str(exe)],capture_output=True,text=True)
        if run.returncode:raise RuntimeError(run.stdout+run.stderr)
        assert not run.stderr,run.stderr;programs.append(exe)
    raw=dest/'canonical_raw_rows.txt';kept=dest/'canonical_kept_rows.txt'
    first=subprocess.run([str(programs[0]),str(ROOT/'b1_g8_unpaired_fields.txt'),str(raw)],capture_output=True,text=True)
    if first.returncode:raise RuntimeError(first.stdout+first.stderr)
    assert not first.stderr and sha(raw)==expected['canonical_raw_rows_sha256']
    reverse=[json.loads(v) for v in first.stdout.splitlines()]
    second=subprocess.run([str(programs[1]),str(ROOT/'b1_g8_unpaired_fields.txt'),str(raw),str(kept)],capture_output=True,text=True)
    if second.returncode:raise RuntimeError(second.stdout+second.stderr)
    assert not second.stderr and sha(kept)==expected['canonical_kept_rows_sha256']
    forward=[json.loads(v) for v in second.stdout.splitlines()]
    assert len(reverse)==len(forward)==len(expected['records'])==2
    reports=[]
    for a,b,control in zip(reverse,forward,expected['records']):
        assert a['status']==b['status']=='complete'
        assert a['mode']==b['mode']==(9 if control['H']==[9] else 29)
        for key in ('raw_individual_rows','kept_individual_rows','raw_normalized_row_pairs','kept_normalized_row_pairs'):
            assert a[key]==control[key],key
        assert a['checked_kept_pairs']==b['checked_kept_pairs']==control['kept_normalized_row_pairs']
        for actual in (a,b):
            assert len(actual['individual_fields'])==128
            for field,original in zip(actual['individual_fields'],control['field_rows']):
                assert all(field[key]==original[key] for key in ('field_row','raw_rows','kept_rows','counts'))
            assert sum(actual['pair_cases'].values())==actual['checked_kept_pairs']
        assert not a['candidates'] and a['candidate_images']==0 and not a['pair_cases'].get('candidate_row_pair',0)
        assert not b['pair_cases'].get('surviving_necessary_pair',0)
        reports.append(dict(H=control['H'],raw_individual_rows=a['raw_individual_rows'],
            kept_individual_rows=a['kept_individual_rows'],raw_normalized_row_pairs=a['raw_normalized_row_pairs'],
            checked_kept_pairs=a['checked_kept_pairs'],reverse_pair_cases=a['pair_cases'],forward_pair_cases=b['pair_cases'],
            zero_reverse_candidates=True,zero_forward_necessary_survivors=True))
        print(json.dumps(dict(H=control['H'],status='pass',complete_pairs=a['checked_kept_pairs'],survivors=0)),flush=True)
    assert [r['checked_kept_pairs'] for r in reports]==[91664640,18539136]
    prior=json.loads((ROOT/'b1_e6_f7_g8_seventh_audit.json').read_text(encoding='utf-8'))
    paired=json.loads((ROOT/'paired_seventh_cpp_audit.json').read_text(encoding='utf-8'))
    core=json.loads((ROOT/'b1_seventh_audit.json').read_text(encoding='utf-8'))
    assert prior['status']==paired['status']==core['status']=='pass'
    assert prior['excluded_H']==[[1,2],[1,9],[2,4],[1,2,9]]
    assert paired['complete_n13_normalized_row_pairs']==663552000 and core['excluded_H']==[2]
    assert {tuple(v) for v in prior['excluded_H']+[core['excluded_H']]+[[9],[2,9]]}=={tuple(z['H']) for z in inventory['records']}
    sixth=json.loads((ROOT/'b1_sixth_inventory.json').read_text(encoding='utf-8'))['records']
    remaining=next(z for z in sixth if z['E']==[6] and z['F']==[7] and z['G']==[2,8])
    assert remaining['labelled_G']==5 and sum(len(p['sixth_field_pairs']) for p in remaining['pairs'])==365
    assert len({tuple(p['original_fifth_rows']) for p in remaining['pairs'] if p['sixth_field_pairs']})==122
    names=[Path(__file__).name,'enumerate_b1_g8_unpaired_rows.py','b1_g8_unpaired_rows.json',
        'b1_g8_unpaired_fields.txt','check_g8_unpaired_rows.cpp','check_g8_unpaired_forward.cpp',
        'B1_E6_F7_G8_EXCLUSION.md','b1_seventh_inventory.json','b1_seventh_audit.json','B1_SEVENTH_ENTRANCE.md',
        'MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','b1_sixth_inventory.json',
        'b1_e6_f7_g8_seventh_audit.json','paired_seventh_cpp_audit.json','B1_E6_F7_G8_PAIRED_SEVENTH_EXCLUSIONS.md',
        'ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    result=dict(status='pass',parameter=[13,9,1],branch=dict(E=[6],F=[7],G=[8]),alphabet='binary only',
        excluded_H=[[9],[2,9]],whole_binary_G8_excluded=True,build_flags=flags,
        positive_negative_algorithm_controls=3,all_manifest_fields_checked=256,all_parent_field_pairs_checked=2188,
        canonical_raw_rows_sha256=sha(raw),canonical_kept_rows_sha256=sha(kept),complete_pair_scans=reports,
        raw_normalized_pair_domain=2045318400,checked_retained_pairs_per_implementation=110203776,
        remaining_binary_E6_F7_G=[[2,8]],remaining_E6_F7_field_pairs=365,all_original_fifth_pairs_retained=122,
        source_sha256={name:sha(ROOT/name) for name in names},
        scope='Complete binary H9/H29 row-domain and two coupled negative scans; combined with audited H2/paired-H premises excludes entire conditional E6/F7/G8 geometry. No other G, whole fifth/third/joint exclusion, arbitrary-alphabet G8 exclusion, exact F value or numerical separation.')
    (ROOT/'b1_g8_unpaired_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(dict(status='pass',whole_binary_G8_excluded=True,raw_row_domain=280800,
        complete_coupled_pairs_per_implementation=110203776,remaining_E6_F7_field_pairs=365)),flush=True)
if __name__=='__main__':main()
