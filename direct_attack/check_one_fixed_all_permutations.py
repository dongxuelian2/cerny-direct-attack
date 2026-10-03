"""Independent all-source audit of the saved all-permutation peak."""

import argparse
import json
from pathlib import Path

from direct_attack.image_extension_policy import profile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    source = Path('direct_attack/data/one_fixed_all_permutations_n8.json')
    record = json.loads(source.read_text(encoding='utf-8'))
    assert record['counts']['tested'] == 40320
    assert record['limit'] == 0 and record['n'] == 8
    peak = record['best']
    rows = [record['base_a'], record['base_b'], peak['c']]
    exact = profile(rows)
    assert exact is not None
    assert max(exact['extension'].values()) == peak['max_e'] == 15
    assert exact['extension'][peak['target']] == 15
    result = {'method': 'ordinary all-source forward transport and policy recurrence',
              'source': str(source), 'n': 8, 'peak_e': 15,
              'peak_target': peak['target'], 'rt': exact['rt'],
              'best_policy': exact['best_policy'], 'verified': True}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
