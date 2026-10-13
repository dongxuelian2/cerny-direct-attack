"""Independent certificate checker. Standard library only; never calls a solver."""
from __future__ import annotations
import json
from pathlib import Path

class CertificateError(ValueError):
    pass

def need(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)

def integer(x: object) -> bool:
    return type(x) is int

def read_json(path: str | Path) -> dict:
    p = Path(path)
    need(p.stat().st_size <= 64_000_000, 'Input exceeds the 64 MB safety limit.')
    with p.open(encoding='utf-8') as f:
        obj = json.load(f)
    need(isinstance(obj, dict), 'The JSON root must be an object.')
    return obj

def validate_automaton(a: dict) -> tuple[int, list[str], list[list[int]]]:
    need(isinstance(a, dict), 'automaton must be an object')
    n = a.get('n')
    need(integer(n) and 1 <= n <= 16, 'n must be an integer in [1, 16]')
    letters, rows = a.get('letters'), a.get('transitions')
    need(isinstance(letters, list) and 1 <= len(letters) <= 16, '1..16 letters required')
    need(all(isinstance(x,str) and x for x in letters), 'Letters must be nonempty strings')
    need(len(set(letters)) == len(letters), 'Duplicate letters')
    need(isinstance(rows,list) and len(rows)==len(letters), 'One row per letter required')
    for row in rows:
        need(isinstance(row,list) and len(row)==n, 'Each transition row must have n entries')
        need(all(integer(x) and 0 <= x < n for x in row), 'Transition outside state space')
    return n, letters, rows

def image_independent(mask: int, row: list[int], n: int) -> int:
    # Deliberately separate from the bit-loop used in the search program.
    targets = {row[q] for q in range(n) if (mask // (2 ** q)) % 2 == 1}
    return sum(2 ** q for q in targets)

def check(cert: dict) -> dict:
    need(cert.get('schema') == 'orion.sync-certificate.v1', 'Unknown certificate schema')
    n, letters, rows = validate_automaton(cert.get('automaton'))
    full = (1 << n)-1
    kind = cert.get('kind')
    if kind == 'nonsynchronizing':
        inv = cert.get('closed_masks')
        need(isinstance(inv,list) and all(integer(x) and 1<=x<=full for x in inv), 'Bad invariant masks')
        states = set(inv)
        need(len(states)==len(inv) and full in states, 'Invariant must include full set, without duplicates')
        need(all(x & (x-1) for x in states), 'Invariant contains a singleton')
        for s in states:
            for row in rows:
                need(image_independent(s,row,n) in states, 'Invariant is not transition-closed')
        return {'verified':True, 'kind':kind, 'n':n, 'invariant_states':len(states)}
    need(kind in ('exact','bounds'), 'Unknown certificate kind')
    d, word = cert.get('potential'), cert.get('word')
    need(isinstance(d,list) and len(d)==1<<n, 'Potential must include all 2^n masks, including mask 0')
    need(all(integer(x) and x>=0 for x in d), 'Potential must contain nonnegative integers')
    need(isinstance(word,list) and all(integer(x) and 0<=x<len(letters) for x in word), 'Bad word')
    need(len(word)<=1_000_000, 'Word exceeds validation limit')
    for q in range(n):
        need(d[1<<q]==0, 'Singleton potential must be zero')
    edges = 0
    for s in range(1,full+1):
        for row in rows:
            t = image_independent(s,row,n)
            need(d[s] <= d[t]+1, f'Invalid local inequality at mask {s}: {d[s]} > {d[t]}+1')
            edges += 1
    s = full
    for x in word:
        s = image_independent(s,rows[x],n)
    need(s != 0 and s & (s-1)==0, 'The witness word does not synchronize')
    need(cert.get('lower_bound')==d[full], 'Incorrect recorded lower bound')
    need(cert.get('upper_bound')==len(word), 'Incorrect recorded upper bound')
    if kind=='exact':
        need(d[full]==len(word), 'Exactness requires matching upper and lower bounds')
    return {'verified':True,'kind':kind,'n':n,'lower_bound':d[full],
            'upper_bound':len(word),'checked_edges':edges}

if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('certificate')
    args=p.parse_args()
    try:
        print(json.dumps(check(read_json(args.certificate)),indent=2))
    except (ValueError,OSError,TypeError) as e:
        p.exit(2, f'VERIFICATION FAILED: {e}\n')
