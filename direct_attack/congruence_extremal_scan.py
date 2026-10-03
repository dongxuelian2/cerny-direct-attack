"""Exact congruence scan on retained n=4,5,6 binary near-extremals."""
import json
from pathlib import Path


def partitions(n):
    def visit(labels, maximum):
        if len(labels) == n:
            if 1 < maximum + 1 < n:
                yield tuple(labels)
            return
        for label in range(maximum + 2):
            yield from visit(labels + [label], max(maximum, label))

    yield from visit([0], 0)


def congruences(rows):
    n = len(rows[0])
    for labels in partitions(n):
        if all(len({labels[row[q]] for q in range(n) if labels[q] == c}) == 1
               for row in rows for c in range(max(labels) + 1)):
            yield labels


def main():
    cases = []
    for n in (4, 5, 6):
        for path in sorted(Path(f'direct_attack/data/n{n}_extremal').glob('*.profile.json')):
            profile = json.loads(path.read_text(encoding='utf-8'))
            assert profile['n'] == n
            found = list(congruences(profile['rows']))
            cases.append(dict(path=path.as_posix(), n=n, rt=profile['rt'],
                              congruences=found))
    assert len(cases) == 22
    result = dict(scope='retained binary near-extremal isomorphism classes, n=4..6',
                  cases=cases,
                  simple=sum(not case['congruences'] for case in cases),
                  nonsimple=sum(bool(case['congruences']) for case in cases))
    out = Path('direct_attack/data/congruence_extremal_scan.json')
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(cases=len(cases), simple=result['simple'],
                          nonsimple=result['nonsimple'],
                          square_extremal_nonsimple=sum(bool(x['congruences'])
                              for x in cases if x['rt'] == (x['n'] - 1) ** 2))))


if __name__ == '__main__':
    main()
