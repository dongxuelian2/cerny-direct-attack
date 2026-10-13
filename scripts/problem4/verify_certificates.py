"""Small independent set implementation; reconstruct inputs before calling it."""
from collections import deque


def apply(states, word, rows):
    states = set(states)
    for letter in word:
        states = {rows['ab'.index(letter)][q] for q in states}
    return states


def ac(rows, S, A):
    start = frozenset(S)
    A = set(A)
    distances = {start: 0}
    todo = deque([start])
    while todo:
        T = todo.popleft()
        if len(T) < len(S) or not A <= T:
            return distances[T]
        for row in rows:
            U = frozenset(row[q] for q in T)
            if U not in distances:
                distances[U] = distances[T] + 1
                todo.append(U)
    return None


def strong(rows):
    n = len(rows[0])
    for root in range(n):
        seen = {root}
        todo = [root]
        while todo:
            q = todo.pop()
            for row in rows:
                if row[q] not in seen:
                    seen.add(row[q])
                    todo.append(row[q])
        if len(seen) != n:
            return False
    return True
