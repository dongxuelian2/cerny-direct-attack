"""Check the complete uniform certificate; optionally rebuild every audit.

No SAT solver or bound on alphabet size is used. Symbolic domain reductions
are specified in PROOF.md#problem4-codimension-three-upper-proof and its case notes.
"""
import argparse
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess
import sys
from collections import deque
from verify_certificates import strong

ROOT = Path(__file__).resolve().parent
GENERATORS = ['triangle_reduced_actions.py', 'path2_reduced_actions.py',
              'path3_mixing_actions.py', 'path3_closed_T_actions.py',
              'type4_reduced_actions.py', 'type6_closed_II_actions.py', 'type7_reduced_actions.py']
NATIVE = [('audit_triangle_actions.cpp','triangle_actions_independent.json'),
          ('audit_path2_actions.cpp','path2_actions_independent.json'),
          ('audit_path3_mixing.cpp','path3_mixing_independent.json'),
          ('audit_path3_closed_T.cpp','path3_closed_T_independent.json'),
          ('audit_path3_no_T.cpp','path3_no_T_independent.json'),
          ('audit_type4_actions.cpp','type4_actions_independent.json'),
          ('audit_type6_closed_II.cpp','type6_closed_II_independent.json'),
          ('audit_type6_breakers.cpp','type6_breaker_independent.json'),
          ('audit_type7_actions.cpp','type7_actions_independent.json'),
          ('audit_type7_breakers.cpp','type7_breaker_independent.json'),
          ('matching_cube_profiles.cpp','matching_cube_profiles.json')]
DOMAINS = ['audit_triangle_mixing.py','audit_path2_domains.py','audit_path3_mixing.py',
           'audit_path3_closed_T_domains.py','audit_path3_no_T.py','audit_type4_domains.py',
           'check_type5_exclusion.py','audit_type6_domains.py','audit_type7_domains.py']
NOTES = ['PROOF.md#problem4-codimension-three-upper-proof','PROOF.md#problem4-short-pair-structure','PROOF.md#problem4-early-pair-types',
         'PROOF.md#problem4-triangle-early-exclusion','PROOF.md#problem4-triangle-mixing-case-a','PROOF.md#problem4-path2-early-exclusion',
         'PROOF.md#problem4-path3-early-exclusion','PROOF.md#problem4-type4-early-exclusion','PROOF.md#problem4-type5-early-exclusion',
         'PROOF.md#problem4-type6-early-exclusion','PROOF.md#problem4-type7-early-exclusion','PROOF.md#problem4-matching-early-exclusion']

def run(args, stdout=None):
    result = subprocess.run([str(a) for a in args], cwd=ROOT, text=True, encoding='utf-8',
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(f'{args}: {result.stdout}\n{result.stderr}')
    if stdout:
        stdout.write_text(result.stdout,encoding='utf-8')

def rebuild(compiler, build):
    build.mkdir(parents=True,exist_ok=True)
    for n in (6,7):
        run([sys.executable,'-B','early_pair_alphabet_pool.py',n,'--out',f'early_alphabet_pool_n{n}.json'])
    for source in GENERATORS:
        run([sys.executable,'-B',source])
    for source,report in NATIVE:
        exe=build/(Path(source).stem+'.exe')
        run([compiler,'-O2','-std=c++17',source,'-o',exe]);run([exe,report])
    run([sys.executable,'-B','check_matching_cube.py','matching_cube_profiles.json','--out','matching_cube_check.json'])
    profiles=build/'matching_profiles.txt'
    run([sys.executable,'-B','audit_matching_cube.py','matching_cube_profiles.json',
         '--profiles-text',profiles,'--out','matching_cube_audit.json'])
    exe=build/'audit_matching_distances.exe'
    run([compiler,'-O2','-std=c++17','audit_matching_distances.cpp','-o',exe])
    run([exe,profiles],ROOT/'matching_distance_audit.json')
    for source in DOMAINS:
        run([sys.executable,'-B',source])

def load(name):
    return json.loads((ROOT/name).read_text(encoding='utf-8'))

def projections(pyfile, cppfile, counts, candidates):
    py=load(pyfile);cpp=load(cppfile)
    assert cpp['status']=='pass'
    records=py.get('records',[py]);independent=cpp['records']
    assert len(records)==len(independent)==len(counts)
    out=[]
    for a,b,count,ncand in zip(records,independent,counts,candidates,strict=True):
        flags=a.get('profile_core_closed',a.get('profiles'))
        assert flags==b['profiles'],pyfile
        assert a['profile_count']==b['profile_count']==count
        assert a['distance_vectors']==b['distance_vectors']
        vectors=[z['distance_vector'] for z in a['candidates']]
        assert vectors==b['candidate_vectors'] and len(vectors)==ncand
        assert b['all_candidates_core_closed']
        out.append(dict(name=b['name'],profiles=count,vectors=b['distance_vectors'],
                        candidates=ncand,all_candidate_rows_core_closed=True))
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rerun',action='store_true')
    ap.add_argument('--compiler',default='clang++');ap.add_argument('--build-dir',type=Path,default=ROOT/'experimental'/'uniform_upper_build')
    args=ap.parse_args()
    if args.rerun:rebuild(args.compiler,args.build_dir.resolve())
    # Three pairs use at most six states. This orbit check therefore covers
    # the abstract classification, rather than extrapolating state counts.
    pairs=list(combinations(range(6),2));K=(0,1)
    stabilizer=[p for p in permutations(range(6)) if set(p[:2])=={0,1}]
    def canonical(a,b):
        return min((tuple(sorted(p[q] for q in a)),tuple(sorted(p[q] for q in b))) for p in stabilizer)
    expected=[((0,2),e) for e in ((1,2),(0,3),(1,3),(2,3),(3,4))]+[
              ((2,3),e) for e in ((0,2),(0,4),(2,4),(4,5))]
    actual={canonical(a,b) for a in pairs if a!=K for b in pairs if b not in (K,a)}
    assert actual=={canonical(a,b) for a,b in expected} and len(actual)==9
    for n in (6,7):
        pool=load(f'early_alphabet_pool_n{n}.json')
        for f in pool['records'][1]['letters']:
            if len(set(f))==n:assert f[0]==0
            else:assert 0 not in f
            assert all(f[q]!=0 for q in range(1,n))
    cert=[]
    for spec in [('triangle_reduced_actions.json','triangle_actions_independent.json',[11,38,61],[0,3,0]),
                 ('path2_reduced_actions.json','path2_actions_independent.json',[22],[1]),
                 ('path3_mixing_actions.json','path3_mixing_independent.json',[24],[1]),
                 ('path3_closed_T_actions.json','path3_closed_T_independent.json',[19],[0]),
                 ('type4_reduced_actions.json','type4_actions_independent.json',[33,37],[0,0]),
                 ('type6_closed_II_actions.json','type6_closed_II_independent.json',[19],[1]),
                 ('type7_reduced_actions.json','type7_actions_independent.json',[21,39,37,27,23,23,33],[0,0,0,0,0,2,0])]:
        cert.extend(projections(*spec))
    mc=load('matching_cube_check.json');ma=load('matching_cube_audit.json');md=load('matching_distance_audit.json')
    assert mc['profile_count']==ma['profiles']==177
    assert mc['distance_vectors_checked']==md['distance_vectors']==30240
    assert not mc['all_states_exit_with_first_distance_at_least_seven'] and mc['witness'] is None
    assert md['candidates']==0 and ma['all_primary_profiles_equal'] and md['artificial_chain_control']
    controls=['triangle_mixing_audit.json','path2_domain_audit.json','path3_mixing_audit.json',
              'path3_closed_T_audit.json','path3_no_T_audit.json','type4_domain_audit.json',
              'type5_exclusion_audit.json','type6_domain_audit.json','type7_domain_audit.json']
    for name in controls:
        assert load(name)['status']=='pass',name
    for tag in ('type6','type7'):
        py=load(f'{tag}_domain_audit.json');cpp=load(f'{tag}_breaker_independent.json')
        for a,b in zip(py['reports'],cpp['records']):
            for key in ('n','compatible_letters','breaker_checks','keeper_checks'):assert a[key]==b[key]
        assert [r['n'] for r in cpp['records']]==[6,7,9]
    # Natural five-state triangle boundary control, independently using
    # ordinary subset images rather than the projected-action formula.
    rows=[[3,3,2,1,4],[0,2,1,4,3],[1,0,2,3,4]]
    assert strong(rows)
    def bfs(start):
        todo=deque([start]);seen={start:0}
        while todo:
            S=todo.popleft()
            for f in rows:
                T=frozenset(f[q] for q in S)
                if T not in seen:seen[T]=seen[S]+1;todo.append(T)
        return seen
    Q=frozenset(range(5));S=frozenset((2,4));whole=bfs(Q);local=bfs(S)
    D=set(map(frozenset,((0,1,3),(0,2,4),(1,2,3),(1,2,4))))
    assert S in whole and any(len(T)==1 for T in whole)
    assert min(d for T,d in local.items() if Q-T not in D)==4
    assert min(d for T,d in local.items() if len(T)<2)==9
    files=NOTES+GENERATORS+[s for s,_ in NATIVE]+DOMAINS+[
          'early_pair_alphabet_pool.py','early_alphabet_pool_n6.json','early_alphabet_pool_n7.json',
          'check_matching_cube.py','audit_matching_cube.py','audit_matching_distances.cpp',
          'verify_certificates.py','check_codimension_three_upper.py']
    report=dict(status='pass',theorem='Every (n-3)-subset compresses in at most nine letters for n>=6',
                hypotheses=['strongly connected','synchronizing','arbitrary finite alphabet'],
                reachability_required_for_upper=False,ordered_pair_types=9,all_types_excluded=True,
                action_domains=cert,matching=dict(profiles=177,distance_vectors=30240,candidates=0),
                component_controls=controls,independent_profiles_flags_vectors_match=True,
                triangle_boundary_control=dict(n=5,projected_exit=4,actual_compression=9,reachable_strong_synchronizing=True),
                rebuilt_current_run=args.rerun,

                consequence='F_bin(n,n-3,r)=F(n,n-3,r)=min(n-r,9) for n>=5, 1<=r<n-3, using independently checked lower witnesses.',
                limits='Partial answer. No all-parameter replacement formula, alphabet separation or formal proof-assistant certification.')
    (ROOT/'codimension_three_upper_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f"Nine types; {len(cert)} action domains plus matching; all independent audits pass")

if __name__=='__main__':main()
