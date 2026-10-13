"""Complete individual E16/E126 fields with exact D15 output atom."""
from pathlib import Path
from itertools import product,permutations
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};D={1,5};K={1,2}

def main():
    records=[]
    for E in ({1,6},{1,2,6}):
        for n in (7,8,9):
            Q=set(range(n));O=Q-A-B-C-D;targets=[A,B,C,D,O];fields=[]
            for pre in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
                if any(X&Y for i,X in enumerate(pre) for Y in pre[i+1:]):continue
                inputs=[*pre,Q-set().union(*pre)];options=[]
                for X,Y in zip(inputs,targets):
                    free=sorted(X-K);guard=sorted(X&K);parts=[]
                    for v in permutations(sorted(Y),len(free)):
                        for w in product(sorted(Y),repeat=len(guard)):
                            parts.append(dict(zip(free,v))|dict(zip(guard,w)))
                    options.append(parts)
                rows=[]
                for parts in product(*options):
                    row=[-1]*n
                    for part in parts:
                        for q,t in part.items():row[q]=t
                    assert min(row)>=0;rows.append(row)
                rows.sort();assert all(a<b for a,b in zip(rows,rows[1:]))
                fields.append(dict(pre=list(map(sorted,pre)),rows=rows))
            m=len(O);count=sum(len(f['rows']) for f in fields)
            assert len(fields)==12 and count==(40*m if len(E)==2 else 24*m+32)*math.factorial(m)
            records.append(dict(n=n,E=sorted(E),fields=fields,complete_individual_rows=count))
    names=[Path(__file__).name,'PROOF.md#problem4-c4-d15-e16-e126-unrestricted-exclusion','b1_c4_fourth_inventory.json']
    report=dict(status='complete_D15_E16_E126_individual_control_domains',records=records,
        complete_individual_rows=sum(r['complete_individual_rows'] for r in records),
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Complete individual row domains only; no binary-active restriction or exclusion inferred here.')
    assert report['complete_individual_rows']==8576
    (ROOT/'c4_d15_guarded_individual_controls.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps(dict(status=report['status'],rows=report['complete_individual_rows'])),flush=True)
if __name__=='__main__':main()
