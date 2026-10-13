"""Raw labelled maps independently test quotient and incoming coverage criteria."""
from pathlib import Path
from itertools import product
import json,hashlib
ROOT=Path(__file__).resolve().parent
def blocks(row):
    return tuple(tuple(i for i,x in enumerate(row) if x==v) for v in sorted(set(row)))
def canon(row):return tuple(sorted(blocks(row)))
def quotient(source,pi,cells):
    if any(len({source[q] for q in b})!=1 for b in pi):return None
    return tuple(sum(source[b[0]]==i for b in pi) for i in range(cells))
def main():
    partition_cases=raw_cases=binary_cases=raw_binary=0;stats=[]
    for n in (2,3,4,5):
        maps=list(product(range(n),repeat=n));pis=sorted({canon(row) for row in maps})
        details=[(row,canon(row),frozenset(row)) for row in maps]
        for cells in range(1,4 if n<5 else 3):
            labels=list(product(range(cells),repeat=n));count=0
            for target in labels:
                cap=tuple(target.count(i) for i in range(cells));actual={source:set() for source in labels}
                rows=[]
                for row,pi,img in details:
                    source=tuple(target[x] for x in row);actual[source].add(pi);raw_cases+=1
                    rows.append((source,pi,img))
                for source in labels:
                    expected=set()
                    for pi in pis:
                        q=quotient(source,pi,cells);count+=1
                        if q is not None and all(x<=y for x,y in zip(q,cap)):expected.add(pi)
                    assert expected==actual[source],(n,cells,target,source)
                if n<=4 and cells<=2:
                    raw=set()
                    for s,p,img in rows:
                        for t,r,img2 in rows:
                            raw_binary+=1
                            if len(img|img2)==n:raw.add((s,t,p,r))
                    expected=set()
                    for s in labels:
                        for t in labels:
                            for p in actual[s]:
                                q=quotient(s,p,cells)
                                for r in actual[t]:
                                    v=quotient(t,r,cells);binary_cases+=1
                                    if all(x+y>=z for x,y,z in zip(q,v,cap)):expected.add((s,t,p,r))
                    assert expected==raw,(n,cells,target)
            partition_cases+=count;stats.append(dict(n=n,atoms=cells,partitions=len(pis),single_criterion_instances=count))
    names=[Path(__file__).name,'PROOF.md#problem4-three-cover-atom-kernel-compatibility']
    report=dict(status='pass',single_partition_criterion_instances=partition_cases,raw_map_output_instances=raw_cases,
        binary_partition_coverage_instances=binary_cases,raw_binary_map_output_instances=raw_binary,stats=stats,
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Complete labelled-map controls of uniform single-letter quotient and two-letter incoming coverage criteria. No F theorem.')
    (ROOT/'general_atom_kernel_controls_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('stats','source_sha256')}),flush=True)
if __name__=='__main__':main()
