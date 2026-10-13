"""Reproducible exploratory tables; output is computational evidence only."""
import csv
import json
from pathlib import Path
from anchor_quotient import solve, path


def main():
    out = Path('scripts/anchors/structural_results')
    out.mkdir(exist_ok=True)
    rows = []
    for r in range(2, 15):
        for m in [2, 3, 4, 5, 8, 12, 20]:
            n = r+m
            d = solve(n, r)
            value = d[m, (1 << r)-1]
            row = dict(n=n, r=r, hidden=m, B=value, intercept=value-3*n,
                       proposed=3*n+2*r-11, vertices=len(d))
            rows.append(row)
        print(r, [(x['hidden'],x['B'],x['intercept']) for x in rows if x['r']==r], flush=True)
    with (out/'fixed_r.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    n,r = 13,9
    d=solve(n,r)
    data = {'status':'COMPUTATIONALLY VERIFIED', 'n':n, 'r':r,
            'distance':d[n-r,(1<<r)-1], 'distances':[
                [j,x,v] for (j,x),v in sorted(d.items())],
            'path':path(n,r,d)}
    (out/'C13_r9.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
