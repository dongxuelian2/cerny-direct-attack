"""Independent monoid closure and certificates; exact native score replay."""
from collections import Counter,deque
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
from direct_attack.native_policy import profile
from direct_attack.check_image_policy import verify


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--pairs',action='store_true');args=ap.parse_args()
    root=Path('scripts/direct_attack/data/extremal_shortcut_pairs' if args.pairs else 'scripts/direct_attack/data/extremal_shortcuts');summary=json.loads((root/'summary.json').read_text());total=0
    for r in summary['records']:
        source=Path(r['source']);assert hashlib.sha256(source.read_bytes()).hexdigest()==r['source_sha256']
        assert any(c['rows']==r['rows'] for c in json.loads(source.read_text())['records'])
        rows=r['rows'];n=r['n'];identity=tuple(range(n));seen={identity};queue=deque([identity])
        while queue:
            u=queue.popleft()
            for row in rows:
                v=tuple(row[q] for q in u)
                if v not in seen:seen.add(v);queue.append(v)
        assert len(seen)==r['monoid_size']
        assert r.get('complete',True),'A stopped counterexample run requires its dedicated shortest-word audit, not full histogram replay.'
        eligible=sorted(u for u in seen if len(set(u))>=n-1 and u!=identity and list(u) not in rows)
        additions=([list(u)] for u in seen) if not args.pairs else ([list(u),list(v)] for u,v in combinations(eligible,2))
        hist=Counter()
        for extras in additions:
            p=profile(rows+extras);assert p is not None
            hist[(p['best_policy'],p['rt'])]+=1
        expected={(c['policy'],c['rt']):c['count'] for c in r['histogram']}
        assert hist==expected and max(P for P,rt in hist)==r['peak_policy']
        assert sum(v for (P,rt),v in hist.items() if P>r['base_policy'])==r['increased']
        peak_extras=r['peak_extra'] if r.get('mode') else [r['peak_extra']]
        peak_words=r['peak_word'] if r.get('mode') else [r['peak_word']]
        actuals=[]
        for word in peak_words:
            actual=list(identity)
            for a in word:actual=[rows[a][q] for q in actual]
            actuals.append(actual)
        assert actuals==peak_extras
        if args.pairs:assert len(actuals)==2 and actuals[0]!=actuals[1] and all(tuple(u) in eligible for u in actuals)
        for name,P in [('base',r['base_policy']),('peak',r['peak_policy'])]:
            c=json.loads((root/(r['label']+'_'+name+'.json')).read_text());verify(c)
            assert c['rows']==(rows if name=='base' else rows+actuals) and c['best_policy']==P
        assert sum(hist.values())==r['tested'];total+=r['tested']
    assert total==summary['tested']
    report=dict(verified=True,bases=len(summary['records']),tested=total,increased=summary['increased'],
                ordinary_set_certificates=2*len(summary['records']),
                boundary='All transformation closures independently enumerated; every score histogram replayed by the previously audited unrestricted native kernel. Ordinary-set policy BFS checks 40 base/peak certificates, not every scored addition.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':main()
