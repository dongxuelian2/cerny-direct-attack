"""Independent per-target reverse-graph audit of mixed-rank search peaks."""
import argparse
import json
from pathlib import Path

from direct_attack.ordinary_reverse_policy import profile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path('scripts/direct_attack/data/mixed_rank_extension_n16'))
    args = ap.parse_args()
    summary = json.loads((args.root/'summary.json').read_text(encoding='utf-8'))
    results = []
    for name in summary['records']:
        saved = json.loads((args.root/name).read_text(encoding='utf-8'))
        ordinary = profile(saved['rows'])
        assert ordinary is not None
        for field in ('extension','best','worst','forward'):
            assert saved[field] == {str(S):v for S,v in ordinary[field].items()}
        n = saved['n']
        assert saved['rt'] == min(ordinary['forward'][1<<q] for q in range(n))
        assert saved['best_policy'] == min(ordinary['best'][1<<q] for q in range(n))
        assert saved['max_extension'] == max(ordinary['extension'].values())
        assert saved['max_extension'] == ordinary['extension'][saved['extension_start']]
        results.append(dict(file=name,n=n,e=saved['max_extension'],P=saved['best_policy'],
                            rt=saved['rt'],images=len(ordinary['forward']),all_arrays=True))
    assert max((x['e'],x['P']) for x in results) == tuple(summary['best'])
    result = dict(verified=True,records=results,
                  scope='Every retained array independently recomputed including all strict-subset arrivals and shortest-parent ties; full adaptive stream is not replayed by this checker.')
    (args.root/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,certificates=len(results),images=sum(x['images'] for x in results))))


if __name__ == '__main__':
    main()
