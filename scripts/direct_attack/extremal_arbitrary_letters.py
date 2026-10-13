"""Exhaust EVERY single arbitrary transformation added to retained near-extremals."""
from collections import Counter
import hashlib,json
from itertools import product
from pathlib import Path
import time
from direct_attack.native_sparse_policy import profile


def main():
    root=Path('scripts/direct_attack/data/extremal_arbitrary_letters');root.mkdir(exist_ok=True);records=[];started=time.monotonic()
    for n in [5,6]:
        source=Path(f'scripts/direct_attack/data/n{n}_extremal/summary.json')
        for base_record in json.loads(source.read_text())['records']:
            rows=base_record['rows'];base=profile(rows);hist=Counter();increased=0;peak=-1;best_extra=None;tested=0;failures=[];short=0
            for extra in product(range(n),repeat=n):
                p=profile(rows+[list(extra)]);assert p is not None and not p['truncated'];tested+=1
                assert p['rt']<=base['rt'];hist[(p['best_policy'],p['rt'])]+=1
                if 2*p['rt']<=n+1:short+=1;assert p['best_policy']<=(n-1)**2
                if p['best_policy']>base['best_policy']:increased+=1
                if p['best_policy']>peak:peak=p['best_policy'];best_extra=list(extra)
                if p['best_policy']>(n-1)**2:failures.append(list(extra))
            label=f'n{n}_{base_record["label"]}'
            for key,r in [('base',rows),('peak',rows+[best_extra])]:
                c=profile(r,True);(root/(label+'_'+key+'.json')).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
            result=dict(n=n,label=label,rows=rows,source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                        base_policy=base['best_policy'],base_rt=base['rt'],tested=tested,increased=increased,
                        peak_policy=peak,peak_extra=best_extra,policy_square_failures=failures,short_reset_budget_cases=short,
                        histogram=[dict(P=P,rt=rt,count=count) for (P,rt),count in sorted(hist.items())])
            records.append(result);print(json.dumps({k:v for k,v in result.items() if k not in ['rows','histogram','source_sha256']}),flush=True)
    report=dict(records=records,tested=sum(r['tested'] for r in records),increased=sum(r['increased'] for r in records),
                square_failures=sum(len(r['policy_square_failures']) for r in records),seconds=time.monotonic()-started,
                scope='Every single n^n transformation added to each of 20 retained binary n5/6 near-extremal bases, including duplicate/identity/constant maps. Arbitrary multiple additions or arbitrary ternary inputs are not covered.')
    (root/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='records'}),flush=True)


if __name__=='__main__':main()
