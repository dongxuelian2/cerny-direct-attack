"""Independent inverse-capacity audit of retained multi-permutation peaks."""

import argparse
import json
from pathlib import Path

from direct_attack.image_extension import profile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = Path('direct_attack/data')
    records = []
    for path in sorted(root.glob('rank_two_multi_perm_p*_q*.json')):
        input_record = json.loads(path.read_text(encoding='utf-8'))
        peak = input_record['best']
        rows = [peak['a'], peak['c'], peak['b']]
        exact = profile(rows)
        assert exact is not None
        assert exact['max_cost'] == peak['max_e']
        assert exact['witness']['start'] == peak['target'] or (
            exact['costs'][peak['target']] == peak['max_e']
        )
        rt = min(exact['forward'][1 << q] for q in range(len(rows[0]))
                 if exact['forward'][1 << q] >= 0)
        assert rt == peak['rt']
        records.append({'source': str(path), 'n': len(rows[0]),
                        'max_e': exact['max_cost'], 'rt': rt,
                        'target': peak['target'],
                        'target_e': exact['costs'][peak['target']],
                        'inverse_witness': exact['witness']})
    result = {'method': 'full-powerset reachable capacity and inverse Bellman BFS',
              'records': records}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'checked': len(records),
                      'max_e': max(r['max_e'] for r in records)}))


if __name__ == '__main__':
    main()
