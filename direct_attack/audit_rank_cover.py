"""Independently audit the conjugation/centralizer reduction of rank covers."""
from itertools import permutations,combinations
from math import factorial,comb
import json
from pathlib import Path


def conjugate(row,p):
    out=[0]*len(row)
    for q,z in enumerate(row):out[p[q]]=p[z]
    return tuple(out)


def canonicalize(a):
    n=len(a);remaining=set(range(n));cycles=[]
    while remaining:
        q=min(remaining);cycle=[]
        while q not in cycle:cycle.append(q);remaining.remove(q);q=a[q]
        cycles.append(cycle)
    cycles.sort(key=lambda c:(len(c),c));p=[0]*n;offset=0;holes=[];last=0
    for c in cycles:
        if len(c)!=last:holes.append(offset);last=len(c)
        for i,q in enumerate(c):p[q]=offset+i
        offset+=len(c)
    return conjugate(a,p),tuple(p),tuple(holes)


def main():
    records=[]
    for n in range(2,6):
        ps=list(permutations(range(n)));centralizers={};count=0
        for a in ps:
            A,p,holes=canonicalize(a)
            if A not in centralizers:
                cs=[h for h in ps if conjugate(A,h)==A]
                centralizers[A]={z:next(h for h in cs if h[z] in holes) for z in range(n)}
            for hole in range(n):
                for x,y in combinations(range(n),2):
                    for targets in permutations(q for q in range(n) if q!=hole):
                        b=[None]*n;b[x]=b[y]=targets[0];i=1
                        for q in range(n):
                            if q not in (x,y):b[q]=targets[i];i+=1
                        B=conjugate(b,p);h=centralizers[A][p[hole]];C=conjugate(B,h)
                        assert conjugate(A,h)==A
                        assert set(range(n))-set(C)=={h[p[hole]]}
                        assert h[p[hole]] in holes and len(set(C))==n-1
                        assert sorted(C.count(q) for q in set(C))==[1]*(n-2)+[2]
                        count+=1
        assert count==factorial(n)*n*comb(n,2)*factorial(n-1)
        records.append(dict(n=n,labeled_pairs=count,canonical_cycle_types=len(centralizers),verified=True))
    summaries=[]
    for root in sorted(Path('direct_attack/data').glob('image_extension_policy_rank_cover_n*')):
        path=root/'summary.json'
        if not path.exists():continue
        data=json.loads(path.read_text());n=data['arguments']['n'];expected=0
        for event in data['records']:
            if event['event']!='class':continue
            expected+=len(set(event['parts']))*comb(n,2)*factorial(n-1)
            assert event['tested']==expected
        assert data['result']['event']=='completed' and data['result']['tested']==expected
        summaries.append(dict(file=str(path),tested=expected,verified=True))
    report=dict(conjugation=records,covers=summaries)
    Path('direct_attack/data/rank_cover_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
