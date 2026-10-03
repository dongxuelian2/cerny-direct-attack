"""Brute-force audit of the pair-threshold vertex-cover pruning decision."""
from itertools import combinations
import json
from pathlib import Path
from direct_attack.near_full_search import covers


def main():
    cases = 0
    for n in range(2, 6):
        pairs = list(combinations(range(n), 2))
        subsets = [frozenset(q for q in range(n) if mask >> q & 1) for mask in range(1 << n)]
        for graph in range(1 << len(pairs)):
            edges = [edge for i, edge in enumerate(pairs) if graph >> i & 1]
            for port in [None] + list(range(n)):
                forbidden = set() if port is None else {port}
                for budget in range(n + 1):
                    brute = any(len(H) <= budget and not H & forbidden
                                and all(H & set(e) for e in edges) for H in subsets)
                    returned = list(covers(edges, budget, forbidden))
                    assert bool(returned) == brute
                    assert all(len(H) <= budget and not H & forbidden
                               and all(H & set(e) for e in edges) for H in returned)
                    cases += 1
    out = dict(n_max=5, graph_budget_forbidden_cases=cases, verified=True,
               scope='Complete cover existence decision; protected-subset mining uses heuristic filler states.')
    Path('direct_attack/data/vertex_cover_checks.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(out))


if __name__ == '__main__': main()
