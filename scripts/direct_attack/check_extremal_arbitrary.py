"""Every arbitrary-addition score checked with a separate full-cube kernel."""
from collections import Counter
import hashlib,json
from itertools import product
from pathlib import Path
import time
from direct_attack.native_policy import profile
from direct_attack.native_sparse_policy import profile as sparse_profile
from direct_attack.audit_sparse_policy import ordinary_forward


def main():
    root=Path('scripts/direct_attack/data/extremal_arbitrary_letters');summary=json.loads((root/'summary.json').read_text());started=time.monotonic();total=increased=square=short=0;certs=0
    for r in summary['records']:
        source=Path(r['source']);assert hashlib.sha256(source.read_bytes()).hexdigest()==r['source_sha256']
        assert any(c['rows']==r['rows'] for c in json.loads(source.read_text())['records']);n=r['n'];rows=r['rows'];hist=Counter();failures=[]
        for extra in product(range(n),repeat=n):
            case=rows+[list(extra)];p=profile(case);s=sparse_profile(case);assert p is not None and s is not None and not s['truncated']
            assert (p['best_policy'],p['rt'])==(s['best_policy'],s['rt']),(r['label'],extra)
            hist[(p['best_policy'],p['rt'])]+=1
            if p['best_policy']>(n-1)**2:failures.append(list(extra))
        assert [dict(P=P,rt=rt,count=c) for (P,rt),c in sorted(hist.items())]==r['histogram']
        assert failures==r['policy_square_failures']
        assert sum(hist.values())==r['tested']==n**n and max(P for P,rt in hist)==r['peak_policy']
        assert sum(c for (P,rt),c in hist.items() if P>r['base_policy'])==r['increased']
        assert sum(c for (P,rt),c in hist.items() if 2*rt<=n+1)==r['short_reset_budget_cases']
        for key,case in [('base',rows),('peak',rows+[r['peak_extra']])]:
            c=json.loads((root/(r['label']+'_'+key+'.json')).read_text());assert c['rows']==case;p=ordinary_forward(case)
            for field in ['extension','best','worst','forward']:assert c[field]=={str(T):v for T,v in p[field].items()}
            assert c['rt']==min(p['forward'][1<<q] for q in range(n)) and c['best_policy']==min(p['best'][1<<q] for q in range(n));certs+=1
            if key=='base':assert c['best_policy']==r['base_policy'] and c['rt']==r['base_rt']
            else:assert c['best_policy']==r['peak_policy']
        total+=r['tested'];increased+=r['increased'];square+=len(failures);short+=r['short_reset_budget_cases']
    assert total==summary['tested'] and increased==summary['increased'] and square==summary['square_failures']
    report=dict(verified=True,bases=len(summary['records']),tested=total,increased=increased,square_failures=square,
                short_reset_budget_cases=short,ordinary_all_source_certificates=certs,per_input_kernel_agreement=True,seconds=time.monotonic()-started,
                scope='Every arbitrary single-addition score/histogram independently replayed with the previously audited FULL-CUBE transport kernel (generator uses sparse full-image graph). Forty base/peak arrays separately use ordinary ALL-SOURCE BFS. No all-input ordinary BFS claim; multiple arbitrary additions not covered.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)


if __name__=='__main__':main()
