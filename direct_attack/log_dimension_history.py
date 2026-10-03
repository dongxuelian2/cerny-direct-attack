"""Generate binary-block ordinary inverse histories; no policy solver."""
import argparse
import json
from pathlib import Path


def record(d):
    assert d >= 3
    n = (1 << d) - 1
    blocks = [[(1 << i) - 1, (1 << (i + 1)) - 2] for i in range(d)]
    stages = [dict(child=1, parent=2, label=['b', 0], cost=1)]
    stages += [dict(child=k, parent=k + 1, label=[k, 0], cost=1)
               for k in range(2, n)]
    return dict(d=d, n=n, blocks=blocks, alphabet_symbols=1 + 2*n * (n - 1),
                indegree=1 + 2*n * (n - 1), outdegree=1 + 2*n * (n - 1),
                stages=stages, proper_stages=n-2, raw_dimension=d,
                normalized_dimension=d-1, rt=2, best_singleton_policy=2,
                worst_singleton_policy=n-1, policy_status='ordinary inverse and actual-image shortest phases',
                actual_parent_membership=[dict(target=k, method='original units from each outside state to least target state',
                                                charged_cost=n-k) for k in range(2,n)],
                short_reset=[[n-1, 0], ['b', 0]],
                long_reset=[[k, 0] for k in range(n-1, 1, -1)] + [['b', 0]],
                long_reset_cost=n-1, endpoint=0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='direct_attack/data/log_dimension_history.json')
    args = ap.parse_args()
    records = [record(d) for d in range(3, 13)]
    data = dict(status='COMPUTATIONAL certificate; all-d paper proof separate',
                definition='LOG_DIMENSION_SHORTEST_EXTENSION_HISTORY.md',
                records=records, scope=dict(parameters=len(records), max_n=records[-1]['n']))
    Path(args.out).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(data['scope']))


if __name__ == '__main__':
    main()
