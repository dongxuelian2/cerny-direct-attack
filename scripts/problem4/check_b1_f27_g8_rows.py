"""Independent exact F27/G8 domains and two complete independent scans."""
from pathlib import Path
from itertools import combinations
import hashlib,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    inventory=json.loads((ROOT/'b1_f27_g8_seventh_inventory.json').read_text(encoding='utf-8'))
    parent=[z for z in inventory['records'] if z['H'] in ([9],[2,9])]
    expected=json.loads((ROOT/'b1_f27_g8_rows_inventory.json').read_text(encoding='utf-8'))
    assert expected['status']=='complete_F27_G8_individual_necessary_row_domain'
    lines=[];keys=('preA','preB','preC','preD','preE','preF','preG')
    for source,control in zip(parent,expected['records']):
        mode=9 if source['H']==[9] else 29;size=128 if mode==9 else 80
        assert source['H']==control['H'] and len(source['rows'])==size
        lines.append(f'13 {mode} {size}')
        for row in source['rows']:
            fields=[set(row[key]) for key in keys]
            assert sum(map(len,fields))==len(set().union(*fields))
            for key in keys:lines.append(' '.join(map(str,[len(row[key]),*row[key]])))
        pairs=[xy for p in source['pairs'] for xy in p['seventh_field_pairs']]
        assert len(pairs)==len({tuple(xy) for xy in pairs})==(1094 if mode==9 else 162)
        assert pairs==control['original_field_pairs']
        lines.append(str(len(pairs)));lines.extend(' '.join(map(str,xy)) for xy in pairs)
        forms=[];fibers=({0},{1,4},{5},{6},{2,7},{8},set(source['H']))
        for subset in combinations(range(13),9):
            if 3 in subset and all(len(set(subset)&X)==1 for X in fibers):forms.append(sum(1<<q for q in subset))
        assert sorted(forms)==control['initial_forms'] and len(forms)==12
        common=8191
        for S in forms:common&=S
        assert common==sum(1<<q for q in control['protected']) and not common&((1<<2)|(1<<7))
    data=('\n'.join(lines)+'\n').encode('utf-8')
    assert data==(ROOT/'b1_f27_g8_rows_fields.txt').read_bytes()
    assert hashlib.sha256(data).hexdigest()==expected['manifest_sha256']
    for name,digest in expected['source_sha256'].items():assert sha(ROOT/name)==digest
    compiler=os.environ.get('CXX') or shutil.which('clang++') or shutil.which('g++')
    if compiler is None:raise RuntimeError('C++17 compiler required; set CXX')
    dest=ROOT/'experimental'/'f27_g8_rows_cpp';dest.mkdir(parents=True,exist_ok=True)
    flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic'];programs=[]
    for name in ('check_f27_g8_rows','check_f27_g8_forward'):
        exe=dest/(name+('.exe' if os.name=='nt' else ''))
        run=subprocess.run([compiler,*flags,str(ROOT/(name+'.cpp')),'-o',str(exe)],capture_output=True,text=True)
        if run.returncode:raise RuntimeError(run.stdout+run.stderr)
        assert not run.stderr,run.stderr;programs.append(exe)
    raw=dest/'canonical_raw_rows.txt';kept=dest/'canonical_kept_rows.txt'
    first=subprocess.run([str(programs[0]),str(ROOT/'b1_f27_g8_rows_fields.txt'),str(raw)],capture_output=True,text=True)
    if first.returncode:raise RuntimeError(first.stdout+first.stderr)
    assert not first.stderr and sha(raw)==expected['canonical_raw_rows_sha256']
    reverse=[json.loads(v) for v in first.stdout.splitlines()]
    second=subprocess.run([str(programs[1]),str(ROOT/'b1_f27_g8_rows_fields.txt'),str(raw),str(kept)],capture_output=True,text=True)
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
    assert [r['raw_individual_rows'] for r in reports]==[25920,11712]
    assert [r['checked_kept_pairs'] for r in reports]==[5859072,241920]
    seventh=json.loads((ROOT/'b1_f27_g8_seventh_audit.json').read_text(encoding='utf-8'))
    assert seventh['status']=='pass'
    assert {tuple(h) for h in seventh['all_alphabet_crossed_exclusions']+[seventh['binary_only_excluded_H']]+[[9],[2,9]]}=={tuple(z['H']) for z in inventory['records']}
    sixth=json.loads((ROOT/'b1_sixth_inventory.json').read_text(encoding='utf-8'))['records']
    residual=[z for z in sixth if z['E']==[6] and z['F']==[2,7] and z['G'] in ([1,8],[2,8])]
    assert [z['G'] for z in residual]==[[1,8],[2,8]]
    assert sum(len(p['sixth_field_pairs']) for z in residual for p in z['pairs'])==105
    cover={tuple(p['original_fifth_rows']) for z in residual for p in z['pairs'] if p['sixth_field_pairs']}
    assert len(cover)==93
    for key,total in (('original_fourth_rows',41),('original_third_rows',14)):
        assert len({tuple(p[key]) for z in residual for p in z['pairs'] if p['sixth_field_pairs']})==total
    names=[Path(__file__).name,'enumerate_b1_f27_g8_rows.py','b1_f27_g8_rows_inventory.json','b1_f27_g8_rows_fields.txt',
        'check_f27_g8_rows.cpp','check_f27_g8_forward.cpp','PROOF.md#problem4-b1-e6-f27-g8-exclusion',
        'b1_f27_g8_seventh_inventory.json','b1_f27_g8_seventh_audit.json','PROOF.md#problem4-b1-f27-g8-seventh-entrance',
        'PROOF.md#problem4-mandatory-core-isolation','mandatory_core_isolation_audit.json','b1_sixth_inventory.json',
        'b1_sixth_audit.json','PROOF.md#problem4-b1-sixth-entrance','b1_fifth_inventory.json','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    result=dict(status='pass',parameter=[13,9,1],branch=dict(E=[6],F=[2,7],G=[8]),alphabet='binary only',
        excluded_H=[[9],[2,9]],whole_binary_E6_F27_G8_excluded=True,build_flags=flags,
        bare_algorithm_controls=3,all_manifest_fields_checked=208,all_parent_field_pairs_checked=1256,
        canonical_raw_rows_sha256=sha(raw),canonical_kept_rows_sha256=sha(kept),complete_pair_scans=reports,
        raw_normalized_pair_domain=33583104,checked_retained_pairs_per_implementation=6100992,
        remaining_binary_E6_F27_G=[[1,8],[2,8]],remaining_sixth_field_pairs=105,
        remaining_original_fifth_pairs=93,all_original_fourth_pairs_retained=41,all_original_third_pairs_retained=14,
        source_sha256={name:sha(ROOT/name) for name in names},
        scope='Complete binary E6/F27/G8 H9/H29 domains and two full negative scans. Composing all seven H cuts excludes this sixth geometry. E6/F27 retains G18/G28 and93 of122 original fifth field pairs. No whole F/E/third/joint or arbitrary-alphabet G8 exclusion, exact F value or numerical separation.')
    (ROOT/'b1_f27_g8_rows_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(dict(status='pass',whole_binary_E6_F27_G8_excluded=True,
        raw_individual_rows=37632,complete_pairs_per_implementation=6100992,remaining_E6_F27_fifth_pairs=93)),flush=True)
if __name__=='__main__':main()
