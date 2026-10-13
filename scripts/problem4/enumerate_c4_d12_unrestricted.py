"""Complete individual D12 rows, without binary-active field shortcuts."""
from pathlib import Path
from itertools import product,permutations
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};D={1,2};K=D
def main():
    records=[]
    for E in ({5},{1,5}):
        for n in (6,7,8,9):
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
            assert len(fields)==(16 if len(E)==1 else 12)
            m=len(O);expected=(32+8*m*m)*math.factorial(m) if len(E)==1 else (24+16*m)*math.factorial(m)
            count=sum(len(f['rows']) for f in fields);assert count==expected
            records.append(dict(n=n,E=sorted(E),fields=fields,complete_individual_rows=count))
    names=[Path(__file__).name,'PROOF.md#problem4-c4-d12-unrestricted-exclusion','b1_c4_fourth_inventory.json']
    report=dict(status='complete_D12_individual_control_domains',records=records,
        complete_individual_rows=sum(r['complete_individual_rows'] for r in records),
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Complete individual control rows only; no binary restriction or negative theorem inferred.')
    assert report['complete_individual_rows']==7328
    (ROOT/'c4_d12_individual_controls.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps(dict(status=report['status'],rows=report['complete_individual_rows'])),flush=True)
if __name__=='__main__':main()
