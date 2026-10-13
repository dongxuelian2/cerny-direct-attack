"""Reachable-fiber anchored rank bound and immediate small-model attacks."""
import argparse
import json
from pathlib import Path
from direct_attack.mine import inputs
from direct_attack.native_policy import profile as fast
from direct_attack.image_extension_policy import profile as certificate


def metrics(c):
    n=c['n'];rows=c['rows'];R=sorted(map(int,c['best']))
    e={int(S):v for S,v in c['extension'].items()};G={int(S):v for S,v in c['best'].items()};W={int(S):v for S,v in c['worst'].items()}
    kappa=0;eligible=[]
    for a,row in enumerate(rows):
        for q in range(n):
            fiber=sum(1<<z for z,t in enumerate(row) if t==q)
            for T in R:
                if T&fiber!=T or T.bit_count()<2:continue
                k=T.bit_count()
                if k>kappa:kappa=k;eligible=[]
                if k==kappa:eligible.append((T,a,q))
    assert kappa>=2
    E=[max((v for S,v in e.items() if S.bit_count()==k),default=0) for k in range(n+1)]
    U2=1+sum(E[2:n]);U=1+sum(E[kappa:n]);old=sum(E[1:n])
    candidates=[q for q in range(n) if e[1<<q]==1];assert candidates and E[1]<=n
    one_step_policy=min(G[1<<q] for q in candidates)
    max_one_step_worst=max(W[1<<q] for q in candidates)
    T,a,q=min(eligible,key=lambda item:(G[item[0]],item))
    kappa_policy=1+G[T]
    assert c['best_policy']<=one_step_policy<=kappa_policy<=U<=U2<=old
    assert max_one_step_worst<=U2
    return dict(n=n,kappa=kappa,rank_maxima=E,old_rank_sum=old,first_step_bound=U2,
                capacity_bound=U,one_step_policy=one_step_policy,kappa_policy=kappa_policy,
                max_one_step_worst=max_one_step_worst,
                first_endpoint=dict(image=T,letter=a,target=q),best_policy=c['best_policy'],rt=c['rt'])


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',default='scripts/direct_attack/data/anchored_image_bound');args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);records=[]
    paths=[p for root in sorted(Path('scripts/direct_attack/data').glob('image_extension_policy*')) for p in sorted(root.glob('witness_*.json'))]
    paths+=sorted(Path('scripts/direct_attack/data/alphabet_monotonicity').glob('*/base.json'))
    paths+=sorted(Path('scripts/direct_attack/data/alphabet_monotonicity').glob('*/augmented.json'))
    for path in paths:records.append(dict(file=str(path),**metrics(json.loads(path.read_text()))))
    runs=[];failure=None
    for n in [2,3,4]:
        tested=sync=0
        for rows in inputs(n,'first-map-orbits',0,0,2):
            tested+=1;c=fast(rows,True)
            if c is None:continue
            sync+=1;m=metrics(c)
            if m['capacity_bound']>(n-1)**2:
                saved=certificate([list(row) for row in rows]);m=metrics(saved)
                (out/'witness.json').write_text(json.dumps(saved,indent=2)+'\n',encoding='utf-8')
                failure=m;break
        runs.append(dict(n=n,tested=tested,synchronizing_sc=sync,complete=failure is None))
        if failure is not None:break
    summary=dict(arguments=vars(args),retained_metrics=records,small_cover_runs=runs,first_rank_sum_failure=failure,
                 scope='Paper universal automaton-dependent bound; the n4 square-envelope scan stops at first failure, not a general reset bound.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(retained_cases=len(records),small_cover_runs=runs,first_rank_sum_failure=failure,
                         maximal_retained_one_step_excess=max(r['one_step_policy']-(r['n']-1)**2 for r in records),
                         maximal_retained_kappa_excess=max(r['kappa_policy']-(r['n']-1)**2 for r in records))))


if __name__=='__main__':main()
