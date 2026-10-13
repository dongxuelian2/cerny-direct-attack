"""Inverse-capacity audit of saved permutation/rank-two finite peaks."""

import argparse
import json
from pathlib import Path

from direct_attack.core import strongly_connected, graph
from direct_attack.image_extension import profile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    path = Path('scripts/direct_attack/data/rank_two_period_audit.json')
    archive = json.loads(path.read_text(encoding='utf-8'))
    assert archive['max_n'] == 8
    checked = 0
    for n_text, entry in archive['summary'].items():
        n = int(n_text)
        examples = entry['examples']
        for kind, example in examples.items():
            rows = [example['a'], example['b']]
            assert len(rows[0]) == n
            assert sorted(rows[0]) == list(range(n))
            assert len(set(rows[1])) == 2
            assert strongly_connected(rows)
            exact = profile(rows)
            assert exact is not None
            rt = min(exact['forward'][1 << q] for q in range(n)
                     if exact['forward'][1 << q] >= 0)
            if kind == 'rt':
                assert rt == example['value']
            elif kind == 'max_e':
                assert exact['max_cost'] == example['value']
                assert exact['costs'][example['target']] == example['value']
                assert len(example['transport_word']) == example['value']
                assert len(example['reset_word']) == rt
                g = graph(rows)
                target = example['target']
                sources = [s for s, d in enumerate(exact['forward'])
                           if d >= 0 and s.bit_count() > target.bit_count()]
                assert any(_apply(g, s, example['transport_word']) & target
                           == _apply(g, s, example['transport_word'])
                           for s in sources)
                assert _apply(g, (1 << n) - 1,
                              example['reset_word']).bit_count() == 1
            elif kind == 'pair_max_e':
                assert max(v for s, v in exact['costs'].items()
                           if s.bit_count() == 2) == example['value']
            else:
                raise AssertionError(kind)
            checked += 1
    result = {'method': 'full-powerset inverse capacity with literal word evaluation',
              'inverse_capacity_peak_checks': checked,
              'max_n': archive['max_n'], 'verified': True}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


def _apply(g, source, word):
    for letter in word:
        source = g[source][letter]
    return source


if __name__ == '__main__':
    main()
