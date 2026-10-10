"""Independent admission checks for the necessary synthesis cuts.

Uses ordinary forward pair BFS and literal vertex-cover enumeration.
Finite controls, not a solver UNSAT certificate or a global upper bound.
"""
from itertools import combinations
import hashlib
import json
from pathlib import Path
from alphabet_check import pair_distances, certificate, verify

ROOT = Path(__file__).resolve().parent


def main():
    records = []
    certificates = json.loads((ROOT/'frontier_certificates.json').read_text(encoding='utf-8'))['certificates']
    for z in certificates:
        n, s, t = z['n'], z['s'], z['value']
        m, h = n-s, t-2*(n-s)
        if not (m >= 2 and n >= 2*m and h >= 1):
            continue
        rows = z['rows']
        distances = pair_distances(rows)
        edges = [pair for pair, d in distances.items() if d <= h]
        cover = next((C for C in combinations(range(n), m-1)
                      if all(x in C or y in C for x, y in edges)), None)
        assert cover is not None, z
        phi = {pair: min(d,t) for pair,d in distances.items()}
        for (x,y), value in phi.items():
            for row in rows:
                image = tuple(sorted((row[x],row[y])))
                assert value <= 1+(0 if image[0] == image[1] else phi[image])
        T = (m+2)*(m+1)//2
        refinement_caps={j:T+j-t for j in range(1,m+1) if 0<=T+j-t<=m}
        assert all(sum(v <= j for v in phi.values()) <= cap
                   for j,cap in refinement_caps.items())
        order = list(cover)+[q for q in range(n) if q not in cover]
        renamed = {q:i for i,q in enumerate(order)}
        new_rows = [[renamed[row[q]] for q in order] for row in rows]
        if len(set(new_rows[0])) == n:
            new_rows.reverse()
        new_S = {renamed[q] for q in z['S']}
        checked = certificate(new_rows,new_S,z['r'])
        assert checked is not None and checked['value'] >= t and verify(checked)
        records.append(dict(n=n,s=s,r=z['r'],target=t,h=h,cover=list(cover),
                            relabeled_cover=list(range(m-1)),refinement_caps=refinement_caps))
        if (n,s,z['r']) == (13,8,1):
            (ROOT.parent/'_qa'/'span_control_n13_rows.json').write_text(json.dumps(new_rows)+'\n',encoding='utf-8')
    result = dict(status='all_admission_controls_passed',count=len(records),records=records,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  scope='Finite positive controls for auxiliary necessary cuts; exact frontier unchanged.')
    (ROOT/'span_synthesis_controls.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],count=len(records))))


if __name__ == '__main__':
    main()
