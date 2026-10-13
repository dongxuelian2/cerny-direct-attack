"""Complete designated pairs of rank-two letters, each nonsync with a."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from direct_attack.core import strongly_connected
from direct_attack.rank_two_multi_perm_search import cycle_pair, rank_two_rows, score
from direct_attack.rank_two_period_audit import collision


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', type=int, required=True)
    parser.add_argument('--q', type=int, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    n = args.p + args.q
    a = cycle_pair(args.p, args.q)
    candidates = [b for b in rank_two_rows(n) if collision(a, b) is None]
    counts = Counter()
    best_rt = None
    best_e = None
    for b, c in combinations(candidates, 2):
        counts['tested_pairs'] += 1
        rows = (a, b, c)
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
            best_rt = {**result, 'a': a, 'b': b, 'c': c}
        if best_e is None or result['max_e'] > best_e['max_e']:
            best_e = {**result, 'a': a, 'b': b, 'c': c}
    result = {'scope': 'fixed disjoint-cycle a; every unordered distinct pair of rank-two rows each nonsynchronizing with a',
              'p': args.p, 'q': args.q, 'n': n,
              'nonsync_single_letter_candidates': len(candidates),
              'counts': dict(counts), 'best_rt': best_rt, 'best_e': best_e}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
