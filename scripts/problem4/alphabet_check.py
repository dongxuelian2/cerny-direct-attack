"""Independent ordinary-set checks for any finite alphabet (Python >=3.10)."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path

LETTERS = "abcdefghijklmnopqrstuvwxyz"

def apply(states, word, rows):
    states = set(states)
    for letter in word:
        states = {rows[LETTERS.index(letter)][q] for q in states}
    return states

def bfs(rows, start, success):
    start = frozenset(start)
    todo = deque([start])
    words = {start: ""}
    while todo:
        S = todo.popleft()
        if success(S):
            return words[S], words
        for letter, row in zip(LETTERS, rows):
            T = frozenset(row[q] for q in S)
            if T not in words:
                words[T] = words[S] + letter
                todo.append(T)
    return None, words

def strong(rows):
    n = len(rows[0])
    for root in range(n):
        todo, seen = [root], {root}
        while todo:
            q = todo.pop()
            for row in rows:
                t = row[q]
                if t not in seen:
                    seen.add(t)
                    todo.append(t)
        if len(seen) != n:
            return False
    return True

def pair_distances(rows):
    """Forward BFS for each pair; independent of reverse pair-closure code."""
    n = len(rows[0])
    result = {}
    for pair in combinations(range(n), 2):
        word, _ = bfs(rows, pair, lambda S: len(S) == 1)
        if word is not None:
            result[pair] = len(word)
    return result

def certificate(rows, S, r):
    n, s = len(rows[0]), len(S)
    assert 1 <= len(rows) <= 26
    assert all(len(row) == n and set(row) <= set(range(n)) for row in rows)
    if not strong(rows):
        return None
    distances = pair_distances(rows)
    if len(distances) != n*(n-1)//2:
        return None
    reaching, _ = bfs(rows, range(n), lambda T: T == frozenset(S))
    if reaching is None:
        return None
    compression, _ = bfs(rows, S, lambda T: len(T) < s)
    assert compression is not None
    reset, _ = bfs(rows, range(n), lambda T: len(T) == 1)
    assert reset is not None
    _, images = bfs(rows, S, lambda T: False)
    scores = {q: min(len(word) for T, word in images.items()
                     if len(T) < s or q not in T) for q in S}
    if r:
        A = sorted(sorted(S, key=lambda q: (-scores[q], q))[:r])
        attaining, _ = bfs(rows, S, lambda T: len(T) < s or not set(A) <= T)
        value = len(attaining)
        assert value == min(scores[q] for q in A)
        assert value <= min(n-r, (n-s+2)*(n-s+1)//2)
    else:
        A, attaining, value = [], compression, len(compression)
    return dict(n=n, s=s, r=r, alphabet_size=len(rows), rows=rows,
                S=sorted(S), A=A, value=value, compression=len(compression),
                reaching=reaching, attaining=attaining, reset=reset,
                state_scores={str(q): scores[q] for q in sorted(S)})

def verify(z):
    rows, S, A = z["rows"], set(z["S"]), set(z["A"])
    n, s, r = z["n"], z["s"], z["r"]
    assert len(rows) == z["alphabet_size"]
    assert len(S) == s and len(A) == r and A <= S
    assert strong(rows) and apply(range(n), z["reaching"], rows) == S
    assert len(apply(range(n), z["reset"], rows)) == 1
    word, _ = bfs(rows, S, lambda T: len(T) < s or (r and not A <= T))
    assert len(word) == z["value"] == len(z["attaining"])
    image = apply(S, z["attaining"], rows)
    assert len(image) < s or (r and not A <= image)
    comp, _ = bfs(rows, S, lambda T: len(T) < s)
    assert len(comp) == z["compression"]
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    data = json.loads(args.file.read_text())
    z = data.get("witness", data)
    assert z is not None and verify(z)
    print(json.dumps(dict(verified=True, n=z["n"], s=z["s"], r=z["r"],
                          alphabet_size=z["alphabet_size"], value=z["value"])))
