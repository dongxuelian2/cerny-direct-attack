"""Independent literal atoms, all5040 symmetries, raw hashes and coupled scans."""
from pathlib import Path
from itertools import combinations,permutations
import hashlib,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((ROOT/n).read_text())

def main():
    parent=read('b1_c14_nonsingleton_fourth_inventory.json');expected=read('d12_d24_fourth_rows_inventory.json')
    assert expected['status']=='complete_D12_D24_raw_fourth_field_domain'
    sources=[z for z in parent['records'] if z['D'] in ([1,2],[2,4]) and z['E'] in ([5],[1,5],[2,5])]
    assert len(sources)==len(expected['records'])==6
    lines=[];symmetry_checks=0
    for z,c in zip(sources,expected['records']):
        assert z['D']==c['D'] and z['E']==c['E']
        outsets=({3},{0},{1,4},set(z['D']));signatures=[];targets=[]
        for t in range(13):
            sig=tuple(t in X for X in outsets)
            if sig not in signatures:
                signatures.append(sig);targets.append([q for q in range(13) if tuple(q in X for X in outsets)==sig])
        assert targets==c['target_atoms']==[a['targets'] for a in z['target_atoms']]
        pairs=[xy for p in z['pairs'] for xy in p['fourth_field_pairs']]
        active=sorted({i for xy in pairs for i in xy});pos={f:i for i,f in enumerate(active)}
        assert active==c['active_original_fields'] and pairs==c['original_field_pairs']
        remapped=[[pos[a],pos[b]] for a,b in pairs];assert remapped==c['normalized_field_pairs']
        lines.append(f"13 {c['mode']} {c['E_mask']} {len(active)}");lines.append('6')
        for atom in targets:lines.append(' '.join(map(str,[len(atom),*atom])))
        atom_fields=[]
        for old in active:
            f=z['rows'][old];pre=[set(f[k]) for k in ('preA','preB','preC','preD')]
            atoms=[[q for q in range(13) if tuple(q in X for X in pre)==sig] for sig in signatures]
            assert atoms==f['atom_inputs'];atom_fields.append(atoms)
            for inp in atoms:lines.append(' '.join(map(str,[len(inp),*inp])))
        lines.append(str(len(pairs)));lines.extend(' '.join(map(str,p)) for p in remapped)
        forms=sorted(sum(1<<q for q in S) for S in combinations(range(13),9)
                     if 3 in S and all(len(set(S)&X)==1 for X in (*outsets[1:],set(z['E']))))
        assert forms==c['initial_forms'] and len(forms)==z['feasible_nine_sets']
        assert c['additional_covered_fibers']==z['additional_covered_fibers']
        for F in z['additional_covered_fibers']:
            assert all(sum(S>>q&1 for q in F)==1 for S in forms)
        common=set.intersection(*[{q for q in range(13) if S>>q&1} for S in forms])
        assert sorted(common)==c['protected']==z['mandatory_through_seven']
        for tail in permutations(range(6,13)):
            g=list(range(6))+list(tail)
            for X in map(set,targets+z['additional_covered_fibers']):assert {g[q] for q in X}==X
            for row in atom_fields:
                for X in map(set,row):assert {g[q] for q in X}==X
            assert sorted(sum(1<<g[q] for q in range(13) if S>>q&1) for S in forms)==forms
            symmetry_checks+=1
    manifest=('\n'.join(lines)+'\n').encode()
    assert manifest==(ROOT/'d12_d24_fourth_rows_fields.txt').read_bytes()
    assert hashlib.sha256(manifest).hexdigest()==expected['manifest_sha256']
    for n,h in expected['source_sha256'].items():assert sha(ROOT/n)==h,n
    compiler=os.environ.get('CXX') or shutil.which('clang++') or shutil.which('g++')
    if not compiler:raise RuntimeError('C++17 compiler required; set CXX')
    dest=ROOT.parent/'_qa'/'d12_d24_fourth_audit';dest.mkdir(parents=True,exist_ok=True)
    flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic'];programs=[]
    for n in ('check_d12_d24_fourth_rows','check_d12_d24_fourth_forward'):
        exe=dest/(n+('.exe' if os.name=='nt' else ''))
        result=subprocess.run([compiler,*flags,str(ROOT/(n+'.cpp')),'-o',str(exe)],capture_output=True,text=True)
        assert result.returncode==0 and not result.stderr,(n,result.stdout,result.stderr);programs.append(exe)
    raw=dest/'raw.txt';transports=dest/'transports.txt';kept_a=dest/'kept_reverse.txt';kept_b=dest/'kept_forward.txt'
    first=subprocess.run([str(programs[0]),str(ROOT/'d12_d24_fourth_rows_fields.txt'),str(raw),str(transports),str(kept_a)],capture_output=True,text=True)
    assert first.returncode==0 and not first.stderr,(first.stdout,first.stderr)
    (dest/'reverse.jsonl').write_text(first.stdout);assert sha(raw)==expected['canonical_raw_rows_sha256']
    reverse=[json.loads(line) for line in first.stdout.splitlines()]
    print('All reverse geometry scans complete; raw-domain hash matches Python.',flush=True)
    second=subprocess.run([str(programs[1]),str(ROOT/'d12_d24_fourth_rows_fields.txt'),str(raw),str(transports),str(kept_b)],capture_output=True,text=True)
    assert second.returncode==0 and not second.stderr,(second.stdout,second.stderr)
    (dest/'forward.jsonl').write_text(second.stdout);assert sha(kept_a)==sha(kept_b)
    forward=[json.loads(line) for line in second.stdout.splitlines()]
    high_masks=0;transport_rows=0
    with kept_b.open() as f:
        for line in f:
            transport_rows+=1;high_masks+=int(line.split()[3])>>32!=0
    assert high_masks>0 and len(reverse)==len(forward)==6;reports=[]
    for a,b,c in zip(reverse,forward,expected['records']):
        assert a['status']==b['status']=='complete' and a['mode']==b['mode']==c['mode']
        assert a['H_mask']==b['H_mask']==c['E_mask'] and a['raw_individual_rows']==c['raw_individual_rows']
        assert a['raw_normalized_row_pairs']==c['raw_literal_pair_product']
        assert a['checked_kept_pairs']==b['checked_kept_pairs']
        for actual in (a,b):
            assert len(actual['individual_fields'])==len(c['field_rows'])
            for f,old in zip(actual['individual_fields'],c['field_rows']):
                assert all(f[k]==old[k] for k in ('field_row','raw_rows'))
                assert sum(f['counts'].values())==f['raw_rows']
            assert sum(actual['pair_cases'].values())==actual['checked_kept_pairs']
        assert a['individual_fields']==b['individual_fields']
        fields=a['individual_fields'];sizes=[f['representatives'] for f in fields]
        assert a['kept_normalized_row_pairs']==sum(fields[x]['kept_rows']*fields[y]['kept_rows'] for x,y in c['normalized_field_pairs'])
        assert a['checked_kept_pairs']==sum(sizes[x]*fields[y]['kept_rows'] for x,y in c['normalized_field_pairs'])
        assert a['candidate_images']==0 and not a['candidates'] and not a['pair_cases'].get('candidate_row_pair',0)
        assert not b['pair_cases'].get('surviving_reachable_pair',0)
        reports.append(dict(D=c['D'],E=c['E'],Boolean_companions=c['additional_covered_fibers'],
            raw_rows=c['raw_individual_rows'],kept_rows=a['kept_individual_rows'],raw_literal_pair_product=c['raw_literal_pair_product'],
            kept_literal_pair_product=a['kept_normalized_row_pairs'],representatives_per_field=sizes,
            complete_representative_pairs=a['checked_kept_pairs'],parent_field_pairs=len(c['original_field_pairs']),
            individual_fields=fields,reverse_pair_cases=a['pair_cases'],forward_pair_cases=b['pair_cases'],zero_candidates_both_algorithms=True))
        print(json.dumps(dict(D=c['D'],E=c['E'],complete_pairs=a['checked_kept_pairs'],zero_candidates=True)),flush=True)
    assert transport_rows==sum(r['kept_rows'] for r in reports)
    names=[Path(__file__).name,'enumerate_d12_d24_fourth_rows.py','d12_d24_fourth_rows_inventory.json',
        'd12_d24_fourth_rows_fields.txt','check_d12_d24_fourth_rows.cpp','check_d12_d24_fourth_forward.cpp',
        'D12_D24_ROW_COVER.md','b1_c14_nonsingleton_fourth_inventory.json','b1_c14_nonsingleton_fourth_audit.json',
        'B1_C14_NONSINGLETON_D_FOURTH.md','MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json',
        'LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md']
    report=dict(status='pass',parameter=[13,9,1],alphabet='binary only',
        all_D12_D24_binary_fourth_survivors_excluded=True,build_flags=flags,bare_algorithm_controls=3,
        independent_symmetry_checks=symmetry_checks,high_initial_masks_checked=high_masks,
        all_parent_fourth_pairs=sum(r['parent_field_pairs'] for r in reports),
        canonical_raw_rows_sha256=sha(raw),canonical_kept_rows_sha256=sha(kept_b),
        pointwise_transports_sha256=sha(transports),pointwise_transports_checked=transport_rows,
        complete_pair_scans=reports,raw_individual_rows=sum(r['raw_rows'] for r in reports),
        checked_representative_pairs_per_implementation=sum(r['complete_representative_pairs'] for r in reports),
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Complete binary D12/D24 E5,E15,E25 actual row negatives with all companions and48 fourth pairs. Unrestricted and other D types remain; no global F value.')
    (ROOT/'d12_d24_fourth_rows_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','complete_pair_scans')}),flush=True)
if __name__=='__main__':main()
