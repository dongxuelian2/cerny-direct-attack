"""Ordinary subset BFS and connectivity helpers for the lower-family audits.

Standard library only. No synthesis, symmetry reduction or upper-bound cut.
"""
from collections import deque


def bfs(rows, start, success):
    start = frozenset(start)
    todo, words = deque([start]), {start: ''}
    while todo:
        S = todo.popleft()
        if success(S):
            return words[S], words
        for letter, row in zip('ab', rows):
            T = frozenset(row[q] for q in S)
            if T not in words:
                words[T] = words[S]+letter
                todo.append(T)
    return None, words


def strong(rows):
    n = len(rows[0])
    for root in range(n):
        seen, todo = {root}, [root]
        while todo:
            q = todo.pop()
            for row in rows:
                if row[q] not in seen:
                    seen.add(row[q])
                    todo.append(row[q])
        if len(seen) != n:
            return False
    return True
