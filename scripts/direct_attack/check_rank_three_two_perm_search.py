"""Independent all-source image-transport check of retained random peaks."""

import argparse
import json
from pathlib import Path

from direct_attack.core import strongly_connected
from direct_attack.image_extension_policy import profile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    records = []
    for name in ('rank_three_two_perm_n8_10k',
                 'rank_three_two_perm_n8_200k',
                 'rank_three_two_perm_n10_100k'):
        source = Path('scripts/direct_attack/data') / (name + '.json')
        saved = json.loads(source.read_text(encoding='utf-8'))
        best = saved['best']
        rows = [*best['permutations'], best['rank_three']]
        assert strongly_connected(rows)
        exact = profile(rows)
        assert exact is not None
        assert exact['rt'] == best['rt']
        assert max(exact['extension'].values()) == best['max_e']
        assert exact['extension'][best['target']] == best['max_e']
        assert len(exact['extension']) + 1 == best['images']
        assert saved['counts']['over_2n'] == 0
        records.append(dict(source=str(source), n=saved['n'],
                            rt=exact['rt'], P=exact['best_policy'],
                            max_e=best['max_e'], target=best['target'],
                            images=best['images']))
    result = dict(method='ordinary all-source image transport and policy recurrence',
                  records=records, verified=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(checked=len(records), verified=True)))


if __name__ == '__main__':
    main()
