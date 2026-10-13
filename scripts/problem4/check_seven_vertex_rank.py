"""Compare two complete graph classifications and independent literal controls."""
import argparse
from itertools import combinations, permutations
import hashlib
import json
from pathlib import Path
import random
import subprocess
from check_short_pair_span import exact_rank, independent_sets

ROOT=Path(__file__).resolve().parent
PAIRS=list(combinations(range(7),2))


def rank_of_maximum_sets(code):
    families=independent_sets(7,{pair for i,pair in enumerate(PAIRS) if code&(1<<i)})
    alpha=max(s for s,sets in enumerate(families) if sets)
    return alpha,exact_rank([[(mask>>q)&1 for q in range(7)] for mask in families[alpha]],7)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rerun',action='store_true')
    ap.add_argument('--compiler',default='clang++')
    ap.add_argument('--build-dir',type=Path,default=ROOT/'experimental'/'seven-rank-build')
    args=ap.parse_args()
    components=[('audit_seven_vertex_rank.cpp','seven_vertex_rank_audit.json'),
                ('audit_seven_vertex_rank_independent.cpp','seven_vertex_rank_independent.json')]
    if args.rerun:
        args.build_dir.mkdir(parents=True,exist_ok=True)
        for source,report in components:
            exe=args.build_dir/(Path(source).stem+'.exe')
            subprocess.run([args.compiler,'-std=c++17','-O3',str(ROOT/source),'-o',str(exe)],check=True)
            subprocess.run([str(exe),str(ROOT/report)],check=True)
    a,b=[json.loads((ROOT/report).read_text(encoding='utf-8')) for _,report in components]
    for key in ('vertices','graphs','alpha_three','maximum_set_rank_seven','cycle_codes'):
        assert a[key]==b[key],key
    assert a['status']==b['status']=='pass' and a['graphs']==2**21
    index={pair:i for i,pair in enumerate(PAIRS)}
    cycles=set()
    for order in permutations(range(1,7)):
        sequence=(0,)+order
        cycles.add(sum(1<<index[tuple(sorted((sequence[i],sequence[(i+1)%7])))] for i in range(7)))
    assert len(cycles)==360 and cycles==set(a['cycle_codes'])
    chord_controls=0
    for code in cycles:
        assert rank_of_maximum_sets(code)==(3,7)
        for bit in range(21):
            if not code&(1<<bit):
                alpha,rank=rank_of_maximum_sets(code|(1<<bit))
                assert alpha!=3 or rank<7
                chord_controls+=1
    seed=7052026;rng=random.Random(seed)
    for _ in range(1000):
        code=rng.randrange(1<<21)
        alpha,rank=rank_of_maximum_sets(code)
        assert (alpha==3 and rank==7)==(code in cycles)
    names=[name for pair in components for name in pair]+[Path(__file__).name]
    result=dict(status='pass',labeled_graphs=2**21,independence_three_graphs=a['alpha_three'],
                full_rank_graphs=360,independent_cycle_codes_match=True,
                chord_controls=chord_controls,random_controls=1000,seed=seed,
                source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
                scope='Complete seven-vertex graph classification only; uniform reduction separate.')
    (ROOT/'seven_vertex_rank_check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':
    main()
