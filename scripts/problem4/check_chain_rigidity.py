"""Small independent controls for the paper chain-rigidity argument.

This is a finite check of an explicitly bounded transformation family.
The all-parameter result is PROOF.md#problem4-signed-chain-rigidity.
"""
from collections import Counter, deque
from itertools import combinations, permutations


def automaton(t, p, order, signs):
    n = p + 2 * t + 1
    a = list(range(n))
    a[p - 2], a[p - 1] = a[p - 1], a[p - 2]
    for i in range(p, n):
        a[i] = p + (i - p + 1) % (2 * t + 1)
    b = list(range(n))
    b[0] = p + order[0] + t * ((signs >> (t - 1)) & 1)
    for i in range(1, p):
        b[i] = i - 1
    for j, (u, v) in enumerate(zip(order, order[1:])):
        flip = (signs >> j) & 1
        b[p + u] = p + v + t * flip
        b[p + t + u] = p + v + t * (1 - flip)
    b[p + order[-1]] = b[p + t + order[-1]] = p - 1
    return a, b


def image(states, word, a, b):
    for ch in word:
        f = a if ch == "a" else b
        states = {f[x] for x in states}
    return states


def actual_compression_distance(a, b, size):
    """Reverse BFS of literal unordered state pairs, independent of word proof."""
    pairs = list(combinations(range(len(a)), 2))
    index = {pair: i for i, pair in enumerate(pairs)}
    rev = [[] for _ in pairs]
    inf = len(pairs) + 1
    dist = [inf] * len(pairs)
    queue = deque()
    for j, pair in enumerate(pairs):
        for f in (a, b):
            u, v = sorted(f[x] for x in pair)
            if u == v:
                if dist[j] == inf:
                    dist[j] = 1
                    queue.append(j)
            else:
                rev[index[u, v]].append(j)
    while queue:
        j = queue.popleft()
        for i in rev[j]:
            if dist[i] == inf:
                dist[i] = dist[j] + 1
                queue.append(i)
    return min(dist[j] for j, pair in enumerate(pairs) if pair[1] < size)


def proof_word(t, p, order, signs, a, b):
    pos = {v: j for j, v in enumerate(order)}
    start = set(range(p + t))
    for k in range(t + 1):
        current = image(start, "a" * k + "b", a, b)
        assert len(current) == len(start)
        assert set(range(p)) <= current
        bits = [int(p + t + i in current) for i in range(t)]
        assert all((p + i in current) != bool(bits[i]) for i in range(t))
        assert p + 2 * t not in current
        for i in range(t - 1):
            if bits[i] == 0 and bits[i + 1] == 1:
                return "a" * k + "b" + "a" * t + "b" * (t - pos[i]), "inversion"
    beta = (signs >> (t - 1)) & 1
    if beta == 0:
        assert order[0] == t - 1
        return "a" * (t + 1) + "ba" + "b" * (t - pos[0]), "entry_x"
    assert order[0] == 0
    first = image(start, "b", a, b)
    if all(p + t + i in first for i in range(t)):
        if t == 2:
            return "babbaab", "all_y_t2"
        return "bab" + "a" * (t + 1) + "b" * t, "all_y"
    assert order == tuple(range(t)) and signs == 1 << (t - 1)
    return None, "canonical"


def main():
    totals = Counter()
    for t in range(2, 6):
        local = Counter()
        noncanonical_max = 0
        for p in (2, 3, 6, 11):
            for order in permutations(range(t)):
                for signs in range(1 << t):
                    a, b = automaton(t, p, order, signs)
                    s = p + t
                    distance = actual_compression_distance(a, b, s)
                    word, kind = proof_word(t, p, order, signs, a, b)
                    local[kind] += 1
                    if kind == "canonical":
                        assert distance == 3 * t + 2
                        # A control against accidentally dropping the exception.
                        assert distance > 3 * t + 1
                        continue
                    assert len(word) <= 3 * t + 1
                    assert len(image(set(range(s)), word, a, b)) < s
                    assert distance <= len(word)
                    noncanonical_max = max(noncanonical_max, distance)
                    if signs == 1 << (t - 1):
                        # Separate stronger proof for unsigned chain permutations.
                        k = next(j for j, v in enumerate(order) if j != v)
                        i = order[k] - 1
                        j = order.index(i)
                        short = "a" * k + "b" + "a" * t + "b" * (t - j)
                        assert len(short) <= 2 * t
                        assert len(image(set(range(s)), short, a, b)) < s
        totals.update(local)
        print(t, "cases", sum(local.values()), "branch_counts", dict(local),
              "noncanonical_max", noncanonical_max, flush=True)
    print("total", sum(totals.values()), "branch_counts", dict(totals), flush=True)


if __name__ == "__main__":
    main()
