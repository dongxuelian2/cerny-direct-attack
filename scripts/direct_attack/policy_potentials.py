"""Attack uniform rank potentials for the exact image-extension recurrence."""
import json
from pathlib import Path


def main():
    records=[];failures=[]
    for root in sorted(Path('scripts/direct_attack/data').glob('image_extension_policy*')):
        for path in sorted(root.glob('witness_*.json')):
            p=json.loads(path.read_text());n=p['n'];values={int(s):v for s,v in p['best'].items()}
            S=max(values,key=lambda s:values[s]-n*(n-s.bit_count()))
            excess=values[S]-n*(n-S.bit_count())
            record=dict(file=str(path),n=n,start=S,size=S.bit_count(),cost=values[S],
                        proposed_bound=n*(n-S.bit_count()),excess=excess)
            records.append(record)
            if excess>0:failures.append(record)
    out=dict(checked=len(records),proposed='G(S)<=n(n-|S|) for every reachable image S',
             failures=failures,records=records,status='REFUTED' if failures else 'UNREFUTED ON SAVED INPUTS')
    Path('scripts/direct_attack/data/policy_rank_potentials.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(checked=len(records),failures=len(failures),worst=max((r['excess'] for r in records),default=None))))
    for r in failures[:5]:print(json.dumps(r))


if __name__=='__main__':main()
