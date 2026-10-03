"""Independent parameter sweep for the m-to-k exact bridge formula."""
import json
from pathlib import Path
from direct_attack.bridge_obstruction import certify
from direct_attack.check_bridges import verify

def main():
    out=Path('direct_attack/data/generalized_bridge'); out.mkdir(parents=True,exist_ok=True)
    records=[]
    parameters=[(2,4,1),(2,4,2),(2,5,1),(2,5,2),(2,7,1),
                (3,4,1),(3,4,2),(3,4,3),(3,5,1),(3,6,1),(4,5,1)]
    for k,m,h in parameters:
        n=k*m*h; block=m*h
        part=[((1<<block)-1)<<(j*block) for j in range(k)]
        start=sum(1<<(j*k*h) for j in range(m))
        label=f'C{n}_k{k}_m{m}_h{h}'
        exact=(m-k)*h*n+k*h
        record=certify(n,part,start,out,label,exact)
        assert record['exact_distance']==exact
        check=verify(json.loads((out/(label+'.json')).read_text()))
        record.update(k=k,m=m,h=h,independently_verified=check['verified'])
        records.append(record); print(json.dumps(record),flush=True)
    report=dict(status='COMPUTATIONALLY VERIFIED',records=records,
                certificates=len(records),vertices=sum(r['states'] for r in records))
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
