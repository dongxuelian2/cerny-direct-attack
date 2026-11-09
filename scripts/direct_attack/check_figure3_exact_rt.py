"""Exact small-parameter reset thresholds for the completed Figure 3 family.

Breadth-first search starts at the full state set and explores both
letter-induced subset images. Therefore the first singleton is reached
at the exact reset threshold. Intended for small parameters only:
the subset state space grows exponentially with p.

The partial transition rules from Szykula, EPTCS 451 (2026),
Fig. 3 and Conjecture 8, are checked wherever they assign a value.
"""

from __future__ import annotations

import argparse
from collections import deque


def transitions(p: int) -> tuple[list[int], list[int]]:
    if p < 3:
        raise ValueError("p must be at least 3")
    n = 3 * p
    a: list[int | None] = [None] * n
    b: list[int | None] = [None] * n
    a[0] = 0
    for j in range(1, p):
        x = 2 * j - 1
        a[x], a[x + 1] = x + 1, x
    a[2 * p - 1], a[2 * p], a[2 * p + 1] = 2 * p, 2 * p + 1, 3
    for x in range(2 * p + 2, n, 2):
        if x + 1 < n:
            a[x], a[x + 1] = x + 1, x
        else:
            a[x] = x
    for x in range(0, 2 * p, 2):
        b[x], b[x + 1] = x + 1, x
    b[2 * p] = 2
    for x in range(2 * p + 1, n, 2):
        if x + 1 < n:
            b[x], b[x + 1] = x + 1, x
        else:
            b[x] = x
    assert all(x is not None for x in a + b)
    return [int(x) for x in a], [int(x) for x in b]


def published_partial(p: int, i: int, letter: str) -> int | None:
    """Literal piecewise formulas of the cited survey, with k = p - 2."""
    k = p - 2
    top = 3 * k + 5
    if letter == "a":
        if i == 0:
            return 0
        if 1 <= i <= 2 * k + 3:
            return i + 1 if i % 2 else i - 1
        if 2 * k + 4 <= i < top and i % 2 == 0:
            return i + 1
        if 2 * k + 7 <= i < top and i % 2 == 1:
            return i - 1
        if i == 2 * k + 5:
            return 3
        if i == top and i % 2 == 0:
            return i
    elif letter == "b":
        if 1 <= i <= 2 * k + 3:
            return i + 1 if i % 2 == 0 else i - 1
        if 2 * k + 5 <= i < top and i % 2 == 1:
            return i + 1
        if 2 * k + 6 <= i < top and i % 2 == 0:
            return i - 1
        if i == 2 * k + 4:
            return 2
        if i == top and i % 2 == 1:
            return i
    else:
        raise ValueError(letter)
    return None


def check_completion(p: int, a: list[int], b: list[int]) -> None:
    missing = []
    for i in range(3 * p):
        for letter, row in (("a", a), ("b", b)):
            original = published_partial(p, i, letter)
            if original is None:
                missing.append((i, letter, row[i]))
            else:
                assert original == row[i], (p, i, letter, original, row[i])
    assert missing == [
        (0, "b", 1),
        (3 * p - 1, "b" if p % 2 else "a", 3 * p - 2),
    ], (p, missing)


def subset_image(mask: int, table: list[int]) -> int:
    result = 0
    while mask:
        bit = mask & -mask
        result |= 1 << table[bit.bit_length() - 1]
        mask -= bit
    return result


def exact_reset_threshold(a: list[int], b: list[int]) -> tuple[int, int]:
    full = (1 << len(a)) - 1
    visited = {full}
    queue = deque([(full, 0)])
    while queue:
        subset, distance = queue.popleft()
        if subset.bit_count() == 1:
            return distance, len(visited)
        for table in (a, b):
            successor = subset_image(subset, table)
            if successor not in visited:
                visited.add(successor)
                queue.append((successor, distance + 1))
    raise AssertionError("No synchronizing word exists")


def check_reset_witness(p: int, a: list[int], b: list[int]) -> int:
    word = (
        "ba" * p + "ab" * (p - 1) + "a" * 4 + "ba" * (p - 2)
        + "".join("a" + "ba" * j for j in range(2 * p - 2, p - 1, -1))
        + "ab" * p
    )
    assert len(word) == 3 * p * p + 4 * p - 1
    subset = (1 << (3 * p)) - 1
    for letter in word:
        subset = subset_image(subset, a if letter == "a" else b)
    assert subset == (1 << 2), (p, subset)
    return len(word)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-p", type=int, default=10)
    args = parser.parse_args()
    if args.max_p < 3:
        parser.error("--max-p must be >= 3")
    print("p,n,exact_rt,constructed_length,reachable_subsets,sharp")
    for p in range(3, args.max_p + 1):
        a, b = transitions(p)
        assert len(set(a)) == len(a) - 1
        assert len(set(b)) == len(b) - 1
        check_completion(p, a, b)
        witness = check_reset_witness(p, a, b)
        exact, visited = exact_reset_threshold(a, b)
        assert exact <= witness
        print(f"{p},{3*p},{exact},{witness},{visited},{exact == witness}")


if __name__ == "__main__":
    main()
