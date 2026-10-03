"""Exhaust all single generated-map additions to retained near-extremal bases."""
from collections import Counter
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time
from direct_attack.alphabet_monotonicity import monoid_words
from direct_attack.native_policy import profile
from direct_attack.image_extension_policy import profile as certificate


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--pairs',action='store_true');args=ap.parse_args()
    root=Path('direct_attack/data/extremal_shortcut_pairs' if args.pairs else 'direct_attack/data/extremal_shortcuts');root.mkdir(parents=True,exist_ok=True)
    records=[];started=time.monotonic()
    for n in [5,6]:
        source=Path(f'direct_attack/data/n{n}_extremal/summary.json')
        for record in json.loads(source.read_text())['records']:
            rows=record['rows'];base=profile(rows);assert base is not None
            words=monoid_words(rows);hist=Counter();increased=0;peak=-1;peak_word=None;peak_extra=None
            eligible=[extra for extra in words if len(set(extra))>=n-1 and extra!=tuple(range(n)) and list(extra) not in rows]
            additions=([list(extra)] for extra in words) if not args.pairs else ([list(u),list(v)] for u,v in combinations(eligible,2))
            tested=0;complete=True
            for extras in additions:
                p=profile(rows+extras);assert p is not None;tested+=1
                hist[(p['best_policy'],p['rt'])]+=1
                increased+=p['best_policy']>base['best_policy']
                if p['best_policy']>peak:
                    peak=p['best_policy'];peak_word=[words[tuple(extra)] for extra in extras];peak_extra=extras
                if args.pairs and tested%100000==0:print(json.dumps(dict(n=n,label=record['label'],tested=tested,peak=peak,seconds=time.monotonic()-started)),flush=True)
                if p['best_policy']>(n-1)**2:complete=False;break
            label=f'n{n}_{record["label"]}'
            for name,r in [('base',rows),('peak',rows+peak_extra)]:
                c=certificate(r)
                assert c['best_policy']==(base['best_policy'] if name=='base' else peak)
                (root/(label+'_'+name+'.json')).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
            result=dict(n=n,label=label,rows=rows,source=str(source).replace('\\','/'),
                        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),base_policy=base['best_policy'],
                        base_rt=base['rt'],monoid_size=len(words),tested=tested,increased=increased,
                        peak_policy=peak,peak_extra=peak_extra,peak_word=peak_word,
                        mode='unit_defect_pairs' if args.pairs else 'single',eligible_pair_letters=len(eligible),complete=complete,
                        histogram=[dict(policy=P,rt=rt,count=count) for (P,rt),count in sorted(hist.items())])
            records.append(result);print(json.dumps({k:v for k,v in result.items() if k not in ['rows','histogram']}),flush=True)
    summary=dict(records=records,tested=sum(r['tested'] for r in records),increased=sum(r['increased'] for r in records),mode='unit_defect_pairs' if args.pairs else 'single',
                 seconds=time.monotonic()-started,
                 boundary='Finite single generated-map additions, or pairs of distinct generated rank>=n-1 maps excluding original labels and identity, to 20 retained near-extremal bases. Each pair run stops on a square-policy failure. No arbitrary multiple-shortcut coverage.')
    (root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='records'}))


if __name__=='__main__':main()
