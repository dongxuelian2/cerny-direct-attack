"""Independent set reachability/fiber capacity and anchored profile audit."""
from collections import deque
from copy import deepcopy
import json
from pathlib import Path
from direct_attack.check_image_policy import verify as policy_verify


def verify(c,m):
    n=c['n'];rows=c['rows'];Q=frozenset(range(n));R={Q};queue=deque([Q])
    step=lambda S,row:frozenset(row[q] for q in S)
    while queue:
        for row in rows:
            T=step(queue[0],row)
            if T not in R:R.add(T);queue.append(T)
        queue.popleft()
    mask=lambda S:sum(1<<q for q in S)
    assert set(map(int,c['best']))=={mask(S) for S in R}
    merged=[T for T in R if any(len(step(T,row))==1 for row in rows)]
    kappa=max(map(len,merged));assert kappa>=2
    E=[]
    for k in range(n+1):E.append(max((c['extension'][str(mask(S))] for S in R if len(S)==k and S!=Q),default=0))
    assert m['kappa']==kappa and m['rank_maxima']==E
    old=sum(E[1:n]);U2=1+sum(E[2:n]);U=1+sum(E[kappa:n])
    assert m['old_rank_sum']==old and m['first_step_bound']==U2 and m['capacity_bound']==U
    assert E[1]<=n and E[n-1]<=n
    first=m['first_endpoint'];T=frozenset(q for q in Q if first['image']>>q&1)
    assert T in R and len(T)==kappa and step(T,rows[first['letter']])==frozenset([first['target']])
    assert c['extension'][str(1<<first['target'])]==1
    costs=[c['best'][str(mask(S))] for S in merged if len(S)==kappa]
    assert m['kappa_policy']==1+min(costs)
    seeds=[q for q in Q if c['extension'][str(1<<q)]==1];assert seeds
    assert m['one_step_policy']==min(c['best'][str(1<<q)] for q in seeds)
    assert m['max_one_step_worst']==max(c['worst'][str(1<<q)] for q in seeds)
    assert c['best_policy']<=m['one_step_policy']<=m['kappa_policy']<=U<=U2<=old
    assert m['max_one_step_worst']<=U2 and m['best_policy']==c['best_policy'] and m['rt']==c['rt']
    return dict(n=n,kappa=kappa,old_bound=old,new_bound=U,policy=c['best_policy'],verified=True)


def main():
    root=Path('scripts/direct_attack/data/anchored_image_bound');c=json.loads((root/'summary.json').read_text())
    records=[]
    for m in c['retained_metrics']:
        case=json.loads(Path(m['file']).read_text());records.append(dict(file=m['file'],**verify(case,m)))
    witness=json.loads((root/'witness.json').read_text());policy_verify(witness)
    result=verify(witness,c['first_rank_sum_failure']);assert result['n']==4 and result['new_bound']==10>9
    # Same-monoid shortcut improves this upper bound while worsening P.
    shortcut=[r for r in records if 'semigroup_n4' in r['file']]
    base=next(r for r in shortcut if r['file'].endswith('base.json'));aug=next(r for r in shortcut if r['file'].endswith('augmented.json'))
    assert base['new_bound']==7 and aug['new_bound']==6 and base['policy']==4<aug['policy']==5
    rejected=[]
    for field in ['capacity','profile_bound','first_target']:
        meta=deepcopy(c['first_rank_sum_failure'])
        if field=='capacity':meta['kappa']+=1
        elif field=='profile_bound':meta['capacity_bound']-=1
        else:meta['first_endpoint']['target']=(meta['first_endpoint']['target']+1)%4
        try:verify(witness,meta)
        except AssertionError:rejected.append(field)
        else:raise AssertionError('Corruption accepted: '+field)
    report=dict(records=records,rank_sum_refutation=result,corruptions_rejected=rejected,verified=True,
                boundary='Independent set reachability and capacity. Source e/G arrays are separately checked by the integrated inverse policy audits; the new refutation is checked here too.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),rank_sum_refutation=result,corruptions_rejected=len(rejected),verified=True)))


if __name__=='__main__':main()
