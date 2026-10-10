"""Complete labelled individual rows for the two guarded E fibers."""
from pathlib import Path
from itertools import product,permutations
import hashlib,json
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};D={1,2,5};K={1,2}

def main():
    records=[]
    for E in ({1,6},{1,2,6}):
        for n in (7,8,9):
            Q=set(range(n));O=Q-A-B-C-D;targets=[A,B,C,D,O];fields=[]
            for pre in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
                if any(X&Y for i,X in enumerate(pre) for Y in pre[i+1:]):continue
                inputs=[*pre,Q-set().union(*pre)];options=[]
                for X,Y in zip(inputs,targets):
                    free=sorted(X-K);guard=sorted(X&K);choices=[]
                    for v in permutations(sorted(Y),len(free)):
                        for w in product(sorted(Y),repeat=len(guard)):
                            choices.append(dict(zip(free,v))|dict(zip(guard,w)))
                    options.append(choices)
                rows=[]
                for parts in product(*options):
                    row=[-1]*n
                    for part in parts:
                        for q,t in part.items():row[q]=t
                    assert min(row)>=0;rows.append(row)
                rows.sort();assert all(a<b for a,b in zip(rows,rows[1:]))
                fields.append(dict(pre=list(map(sorted,pre)),rows=rows))
            assert len(fields)==12
            count=sum(len(f['rows']) for f in fields)
            assert count==({7:156,8:384,9:1368} if len(E)==2 else {7:228,8:456,9:1368})[n]
            records.append(dict(n=n,E=sorted(E),fields=fields,complete_individual_rows=count))
    names=[Path(__file__).name,'C4_D125_E16_E126_UNRESTRICTED_EXCLUSION.md',
        'UNIVERSAL_FREE_IMAGE_TRAP.md','b1_c4_fourth_inventory.json']
    report=dict(status='complete_guarded_E_individual_controls',records=records,
        complete_individual_rows=sum(r['complete_individual_rows'] for r in records),
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Complete individual control domains only; no sampled negative exclusion.')
    (ROOT/'c4_d125_guarded_individual_controls.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps(dict(status=report['status'],rows=report['complete_individual_rows'])),flush=True)
if __name__=='__main__':main()
