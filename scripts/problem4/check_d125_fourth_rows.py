"""Independent atoms, all720 symmetries, full row hashes and two pair scans."""
from pathlib import Path
from itertools import combinations,permutations
import hashlib,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((ROOT/n).read_text())

def main():
    parent=read('b1_c14_nonsingleton_fourth_inventory.json')
    expected=read('d125_fourth_rows_inventory.json')
    assert expected['status']=='complete_D125_active_fourth_literal_rows'
    sources=[z for z in parent['records'] if z['D']==[1,2,5] and z['E'] in ([6],[2,6])]
    assert len(sources)==len(expected['records'])==2
    lines=[];controls=[];symmetry_checks=0
    for z,c in zip(sources,expected['records']):
        assert z['E']==c['E']
        outsets=({3},{0},{1,4},{1,2,5})
        signatures=[];targets=[]
        for t in range(13):
            sig=tuple(t in X for X in outsets)
            if sig not in signatures:
                signatures.append(sig)
                targets.append([q for q in range(13) if tuple(q in X for X in outsets)==sig])
        assert targets==c['target_atoms']==[a['targets'] for a in z['target_atoms']]
        assert len(targets)==6 and not z['additional_covered_fibers']
        pairs=[xy for p in z['pairs'] for xy in p['fourth_field_pairs']]
        active=sorted({i for xy in pairs for i in xy});pos={f:i for i,f in enumerate(active)}
        assert active==c['active_original_fields'] and pairs==c['original_field_pairs']
        reduced_pairs=[[pos[a],pos[b]] for a,b in pairs]
        assert reduced_pairs==c['normalized_field_pairs']
        lines.append(f"13 {c['mode']} {c['E_mask']} {len(active)}");lines.append('6')
        for atom in targets:lines.append(' '.join(map(str,[len(atom),*atom])))
        atom_fields=[]
        for old in active:
            f=z['rows'][old];pre=[set(f[k]) for k in ('preA','preB','preC','preD')]
            atoms=[[q for q in range(13) if tuple(q in X for X in pre)==sig] for sig in signatures]
            assert atoms==f['atom_inputs'];atom_fields.append(atoms)
            for inp in atoms:lines.append(' '.join(map(str,[len(inp),*inp])))
        lines.append(str(len(pairs)));lines.extend(' '.join(map(str,xy)) for xy in reduced_pairs)
        forms=sorted(sum(1<<q for q in S) for S in combinations(range(13),9)
                     if 3 in S and all(len(set(S)&X)==1 for X in (*outsets[1:],set(z['E']))))
        assert forms==c['initial_forms'] and len(forms)==z['feasible_nine_sets']
        common=set.intersection(*[{q for q in range(13) if S>>q&1} for S in forms])
        assert sorted(common)==c['protected']==z['mandatory_through_seven']
        for tail in permutations(range(7,13)):
            g=list(range(7))+list(tail)
            for X in map(set,targets):assert {g[q] for q in X}==X
            for row in atom_fields:
                for X in map(set,row):assert {g[q] for q in X}==X
            assert sorted(sum(1<<g[q] for q in range(13) if S>>q&1) for S in forms)==forms
            symmetry_checks+=1
        controls.append(c)
    manifest=('\n'.join(lines)+'\n').encode()
    assert manifest==(ROOT/'d125_fourth_rows_fields.txt').read_bytes()
    assert hashlib.sha256(manifest).hexdigest()==expected['manifest_sha256']
    for n,h in expected['source_sha256'].items():assert sha(ROOT/n)==h,n
    compiler=os.environ.get('CXX') or shutil.which('clang++') or shutil.which('g++')
    if not compiler:raise RuntimeError('C++17 compiler required; set CXX')
    dest=ROOT/'experimental'/'d125_fourth_audit';dest.mkdir(parents=True,exist_ok=True)
    flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic'];programs=[]
    for n in ('check_d125_fourth_rows','check_d125_fourth_forward'):
        exe=dest/(n+('.exe' if os.name=='nt' else ''))
        run=subprocess.run([compiler,*flags,str(ROOT/(n+'.cpp')),'-o',str(exe)],capture_output=True,text=True)
        assert run.returncode==0 and not run.stderr,(n,run.stdout,run.stderr)
        programs.append(exe)
    raw=dest/'raw.txt';transports=dest/'transports.txt';kept=dest/'kept.txt'
    first=subprocess.run([str(programs[0]),str(ROOT/'d125_fourth_rows_fields.txt'),str(raw),str(transports)],capture_output=True,text=True)
    assert first.returncode==0 and not first.stderr,(first.stdout,first.stderr)
    (dest/'reverse.jsonl').write_text(first.stdout)
    assert sha(raw)==expected['canonical_raw_rows_sha256']
    reverse=[json.loads(line) for line in first.stdout.splitlines()]
    second=subprocess.run([str(programs[1]),str(ROOT/'d125_fourth_rows_fields.txt'),str(raw),str(transports),str(kept)],capture_output=True,text=True)
    assert second.returncode==0 and not second.stderr,(second.stdout,second.stderr)
    (dest/'forward.jsonl').write_text(second.stdout)
    assert sha(kept)==expected['canonical_kept_rows_sha256']
    forward=[json.loads(line) for line in second.stdout.splitlines()]
    high_masks=sum(int(line.split()[3])>>32!=0 for line in kept.read_text().splitlines())
    assert high_masks>0
    assert len(reverse)==len(forward)==2;reports=[]
    for a,b,c in zip(reverse,forward,controls):
        assert a['status']==b['status']=='complete' and a['mode']==b['mode']==c['mode']
        assert a['H_mask']==b['H_mask']==c['E_mask']
        for key in ('raw_individual_rows','kept_individual_rows'):assert a[key]==c[key]
        assert a['raw_normalized_row_pairs']==c['raw_literal_pair_product']
        assert a['kept_normalized_row_pairs']==c['kept_literal_pair_product']
        assert a['checked_kept_pairs']==b['checked_kept_pairs']
        for actual in (a,b):
            assert len(actual['individual_fields'])==len(c['field_rows'])
            for f,old in zip(actual['individual_fields'],c['field_rows']):
                assert all(f[k]==old[k] for k in ('field_row','raw_rows','kept_rows','counts'))
            assert sum(actual['pair_cases'].values())==actual['checked_kept_pairs']
        assert a['individual_fields']==b['individual_fields']
        sizes=[f['representatives'] for f in a['individual_fields']]
        assert a['checked_kept_pairs']==sum(sizes[x]*c['field_rows'][y]['kept_rows'] for x,y in c['normalized_field_pairs'])
        assert a['candidate_images']==0 and not a['candidates'] and not a['pair_cases'].get('candidate_row_pair',0)
        assert not b['pair_cases'].get('surviving_necessary_pair',0)
        reports.append(dict(E=c['E'],raw_rows=c['raw_individual_rows'],kept_rows=c['kept_individual_rows'],
            raw_literal_pair_product=c['raw_literal_pair_product'],kept_literal_pair_product=c['kept_literal_pair_product'],
            representatives_per_field=sizes,complete_representative_pairs=a['checked_kept_pairs'],
            parent_field_pairs=len(c['original_field_pairs']),reverse_pair_cases=a['pair_cases'],
            forward_pair_cases=b['pair_cases'],zero_candidates_both_algorithms=True))
    names=[Path(__file__).name,'enumerate_d125_fourth_rows.py','d125_fourth_rows_inventory.json',
        'd125_fourth_rows_fields.txt','check_d125_fourth_rows.cpp','check_d125_fourth_forward.cpp',
        'PROOF.md#problem4-d125-row-normalization','PROOF.md#problem4-d125-fourth-rows','b1_c14_nonsingleton_fourth_inventory.json',
        'b1_c14_nonsingleton_fourth_audit.json','PROOF.md#problem4-b1-c14-nonsingleton-d-fourth',
        'PROOF.md#problem4-mandatory-core-isolation','mandatory_core_isolation_audit.json','PROOF.md#problem4-local-equality-flag','PROOF.md#problem4-entry-fiber-flag']
    report=dict(status='pass',parameter=[13,9,1],D=[1,2,5],alphabet='binary only',
        binary_E6_E26_excluded=True,build_flags=flags,bare_algorithm_controls=3,
        independent_symmetry_checks=symmetry_checks,high_initial_masks_checked=high_masks,
        all_parent_fourth_pairs=sum(r['parent_field_pairs'] for r in reports),
        canonical_raw_rows_sha256=sha(raw),canonical_kept_rows_sha256=sha(kept),
        pointwise_transports_sha256=sha(transports),
        pointwise_transports_checked=sum(r['kept_rows'] for r in reports),
        complete_pair_scans=reports,raw_individual_rows=sum(r['raw_rows'] for r in reports),
        checked_representative_pairs_per_implementation=sum(r['complete_representative_pairs'] for r in reports),
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Complete binary D125/E6,E26 negatives, including all twelve parent fields. Unrestricted alphabets and other D types remain; no global F value.')
    (ROOT/'d125_fourth_rows_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','complete_pair_scans')}),flush=True)

if __name__=='__main__':main()
