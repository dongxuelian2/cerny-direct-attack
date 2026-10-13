"""Complete allowed-map controls for matching stabilization and path obstruction."""
from pathlib import Path
from itertools import permutations,combinations
import json,hashlib,math
ROOT=Path(__file__).resolve().parent
E={(0,1)};P2={(0,1),(0,2)};P3=P2|{(2,3)}
def pull(G,row):
    return {p for p in combinations(range(len(row)),2) if row[p[0]]!=row[p[1]] and tuple(sorted(row[q] for q in p)) in G}
def cover(K,G):return all(set(p)&K for p in G)
def maps(n):
    pool=[tuple(p) for p in permutations(range(n))]
    for targets in permutations(range(n),n-1):
        pool.append((targets[0],targets[0],*targets[1:]))
    assert len(pool)==len(set(pool))==2*math.factorial(n)
    return pool
def main():
    for name in ['two_cover_unique_immediate_pair_audit.json','two_cover_p3_classification_audit.json',
                 'finite_independent_image_trap_audit.json','mandatory_core_isolation_audit.json']:
        z=json.loads((ROOT/name).read_text());assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    stats=[];raw=matching=singular=perm=0;singleton_boundary=None;growth_boundary=None
    for n in (4,5,6):
        pool=maps(n);raw+=len(pool);mc=sc=pc=0
        matchingG={(0,1),(2,3)}
        extensions=[matchingG]+[matchingG|{tuple(sorted((a,b)))} for a in (0,1) for b in (2,3)]
        for row in pool:
            for G3 in extensions:
                if not pull(E,row)<=matchingG or not pull(matchingG,row)<=G3:continue
                assert pull(matchingG,row)<=matchingG;mc+=1
            if len(set(row))==n-1:
                if not pull(E,row)<=P2 or not pull(P2,row)<=P3:continue
                pre={q for q,t in enumerate(row) if t in {0,1}}
                singleton=next(iter(pre)) if len(pre)==1 else None
                isolated=singleton is None or all(singleton not in p for p in P3)
                if isolated:
                    assert not pull(P2,row);sc+=1
                elif (2,3) in pull(P2,row) and singleton_boundary is None:
                    singleton_boundary=dict(n=n,row=list(row),preE=sorted(pre),new_edge=[2,3])
            else:
                if not pull(E,row)<=P2 or not pull(P2,row)<=P3 or (2,3) not in pull(P2,row):continue
                for K in combinations(range(n),2):
                    K=set(K)
                    if not cover(K,P3) or not cover(K,pull(P3,row)) or not cover(K,pull(pull(P3,row),row)):continue
                    new_neighbors=[p for p in pull(P3,row)|pull(pull(P3,row),row) if 1 in p and p!=(0,1)]
                    assert new_neighbors;pc+=1
                    if growth_boundary is None:growth_boundary=dict(n=n,row=list(row),K=sorted(K),new_leaf_edges=list(map(list,sorted(new_neighbors))))
        matching+=mc;singular+=sc;perm+=pc
        stats.append(dict(n=n,complete_fixed_kernel_maps=len(pool),matching_controls=mc,singular_path_controls=sc,permutation_growth_controls=pc))
    assert raw==1728 and matching>0 and singular>0 and perm>0 and singleton_boundary is not None and growth_boundary is not None
    names=[Path(__file__).name,'PROOF.md#problem4-two-cover-protected-kernel-obstruction',
           'PROOF.md#problem4-two-cover-unique-immediate-pair','two_cover_unique_immediate_pair_audit.json',
           'PROOF.md#problem4-two-cover-p3-classification','two_cover_p3_classification_audit.json',
           'PROOF.md#problem4-finite-independent-image-trap','finite_independent_image_trap_audit.json',
           'PROOF.md#problem4-mandatory-core-isolation','mandatory_core_isolation_audit.json']
    report=dict(status='pass',complete_fixed_kernel_maps=raw,matching_stabilization_controls=matching,
                singular_path_controls=singular,permutation_growth_controls=perm,stats=stats,
                singleton_isolation_boundary=singleton_boundary,permutation_growth_boundary=growth_boundary,
                source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
                scope='Uniform written two-cover one-count kernel obstruction; exhaustive graph/map controls n4..6. No F maximum.')
    (ROOT/'two_cover_protected_kernel_graph_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','stats')}),flush=True)
if __name__=='__main__':main()
