"""Exact conditional E12 domains: unique immediate pair12, no SC filter."""
from pathlib import Path
from itertools import product,permutations
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={4};D={5};E={1,2}
def main():
    records=[]
    for n in (6,7,8,9):
        Q=set(range(n));O=Q-A-B-C-D;fields=[]
        for pre in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
            if any(X&Y for i,X in enumerate(pre) for Y in pre[i+1:]):continue
            inputs=sorted(Q-set().union(*pre));rows=[]
            for outputs in permutations(sorted(O),len(inputs)):
                row=[-1]*n
                for X,t in zip(pre,(3,0,4,5)):
                    for q in X:row[q]=t
                for q,t in zip(inputs,outputs):row[q]=t
                rows.append(row)
            if pre[3]!=E:
                assert E<=set(inputs)
                others=[q for q in inputs if q not in E]
                for target in sorted(O):
                    for outputs in permutations(sorted(O-{target}),len(others)):
                        row=[-1]*n
                        for X,t in zip(pre,(3,0,4,5)):
                            for q in X:row[q]=t
                        row[1]=row[2]=target
                        for q,t in zip(others,outputs):row[q]=t
                        rows.append(row)
            rows.sort()
            assert len(rows)==(1 if pre[3]==E else 2)*math.factorial(n-4)
            fields.append(dict(pre=list(map(sorted,pre)),rows=rows))
        assert len(fields)==16
        records.append(dict(n=n,fields=fields,complete_individual_rows=sum(len(f['rows']) for f in fields)))
    names=[Path(__file__).name,'C4_D5_E12_E126_UNRESTRICTED_EXCLUSION.md','b1_c4_fourth_inventory.json',
           'TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md','two_cover_unique_immediate_pair_audit.json']
    result=dict(status='complete_conditional_D5_E12_unique_kernel_domains',records=records,
                complete_individual_rows=sum(r['complete_individual_rows'] for r in records),
                source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
                scope='Exact domains under unique immediate pair12; all suppliers retained. Conditional, not all unrestricted transformations.')
    assert result['complete_individual_rows']==3648
    (ROOT/'c4_d5_e12_unique_kernel_individual_controls.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(dict(status=result['status'],rows=result['complete_individual_rows'])),flush=True)
if __name__=='__main__':main()
