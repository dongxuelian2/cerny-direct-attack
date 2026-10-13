"""Complete small-state cover of two permutations and one rank-two map.

Fix one representative for each first-permutation cycle type. Then exhaust
the second permutation and every labeled rank-two map relative to it.
"""

import argparse
from collections import Counter
from itertools import permutations
import json
from pathlib import Path

from direct_attack.core import strongly_connected
from direct_attack.rank_two_multi_perm_search import rank_two_rows, score
from direct_attack.rank_two_period_audit import partitions, representative


def run(n):
    counts = Counter()
    best_rt = None
    best_e = None
    for parts in partitions(n):
        a = representative(parts)
        for c in permutations(range(n)):
            for b in rank_two_rows(n):
                counts['tested'] += 1
                rows = (a, c, b)
                if not strongly_connected(rows):
                    continue
                counts['strongly_connected'] += 1
                result = score(rows)
                if result is None:
                    continue
                counts['synchronizing'] += 1
                counts['rt_over_n_plus_1'] += result['rt'] > n + 1
                counts['e_over_2n'] += result['max_e'] > 2 * n
                if best_rt is None or result['rt'] > best_rt['rt']:
                    best_rt = {**result, 'a': a, 'c': c, 'b': b}
                if best_e is None or result['max_e'] > best_e['max_e']:
                    best_e = {**result, 'a': a, 'c': c, 'b': b}
    return {'n': n, 'scope': 'one first-permutation cycle representative; all second permutations and rank-two rows',
            'counts': dict(counts), 'best_rt': best_rt, 'best_e': best_e}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.n)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
