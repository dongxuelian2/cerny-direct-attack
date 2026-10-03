"""Independent ordinary per-target reverse policies for ALL saved binary n2..5 covers."""
from collections import Counter
import json
from pathlib import Path
import time
from direct_attack.mine import inputs
from direct_attack.ordinary_reverse_policy import profile


def main():
    started=time.monotonic();records=[]
    for n in [2,3,4,5]:
        root=Path(f'direct_attack/data/seed_budget_binary_n{n}');frozen=json.loads((root/'summary.json').read_text());counts=Counter();hist=Counter()
        for rows in inputs(n,'first-map-orbits',0,0,2):
            counts['tested']+=1;p=profile(rows)
            if p is None:continue
            counts['sc_synchronizing']+=1;R=[frozenset(q for q in range(n) if S>>q&1) for S in p['best']]
            mask=lambda T:sum(1<<q for q in T)
            merged=[T for T in R if len(T)>1 and any(len({row[q] for q in T})==1 for row in rows)]
            kappa=max(map(len,merged));P=min(p['best'][1<<q] for q in range(n))
            F=1+min(p['best'][mask(T)] for T in merged)
            Fk=1+min(p['best'][mask(T)] for T in merged if len(T)==kappa)
            Wk=1+max(p['worst'][mask(T)] for T in merged if len(T)==kappa)
            hist[(F-P,Fk-P)]+=1
            if F>P:counts['normal_form_refutations']+=1
            if Fk>(n-1)**2:counts['anchor_square_refutations']+=1
            if Wk>(n-1)**2:counts['anchor_all_ties_refutations']+=1
        assert dict(counts)==frozen['counts'],(n,counts,frozen['counts'])
        assert [dict(normal_gap=k[0],anchor_gap=k[1],count=v) for k,v in sorted(hist.items())]==frozen['histogram']
        records.append(dict(n=n,counts=dict(counts),histogram=frozen['histogram'],verified=True));print(json.dumps(dict(n=n,counts=dict(counts),verified=True,seconds=time.monotonic()-started)),flush=True)
    report=dict(verified=True,records=records,seconds=time.monotonic()-started,
        boundary='Every binary covering input n2..5 is independently enumerated and scored using ordinary image closure and per-target reverse graph BFS, without a native scorer. All counters and full gap histograms agree. Covers overlap isomorphism classes; unary/duplicate inputs cannot be SC synchronizing at n>=2.')
    Path('direct_attack/data/seed_budget_binary_cover_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
