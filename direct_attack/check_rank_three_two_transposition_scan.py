"""Independent all-source checks of retained two-transposition peaks."""

import argparse
from math import comb
import json
from pathlib import Path

from direct_attack.image_extension_policy import profile


def transposition(n, i, j):
    row = list(range(n))
    row[i], row[j] = row[j], row[i]
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    records = []
    for n in (8, 10, 12):
        source = Path(f'direct_attack/data/rank_three_two_transposition_n{n}.json')
        saved = json.loads(source.read_text(encoding='utf-8'))
        assert saved['counts']['tested'] == comb(comb(n, 2), 2)
        assert saved['counts']['over_2n'] == saved['counts']['equal_2n'] == 0
        best = saved['best']
        rows = [saved['base_a'],
                *(transposition(n, *pair) for pair in best['swaps']),
                saved['base_b']]
        exact = profile(rows)
        assert exact is not None
        assert exact['rt'] == best['rt']
        assert max(exact['extension'].values()) == best['max_e'] == 2 * n - 1
        assert exact['extension'][best['target']] == best['max_e']
        assert len(exact['extension']) + 1 == best['images']
        records.append(dict(source=str(source), n=n, swaps=best['swaps'],
                            rt=exact['rt'], P=exact['best_policy'],
                            max_e=best['max_e'], target=best['target'],
                            images=best['images']))
    result = dict(method='independent ordinary all-source image transport and policy recurrence',
                  records=records, verified=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'checked': len(records), 'verified': True}))


if __name__ == '__main__':
    main()
