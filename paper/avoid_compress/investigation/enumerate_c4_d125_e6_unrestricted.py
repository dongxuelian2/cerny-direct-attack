"""Complete individual fields/rows for finite controls of the paper lemma."""
from pathlib import Path
from itertools import product,permutations
import hashlib,json
ROOT=Path(__file__).resolve().parent
K={1,2};A={3};B={0};C={4};D={1,2,5};E={6}
def main():
    reports=[]
    for n in (7,8,9):
        Q=set(range(n));O=Q-A-B-C-D;targets=[A,B,C,D,O];fields=[];rawtuples=0
        for pre in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
            rawtuples+=1
            if any(x&y for i,x in enumerate(pre) for y in pre[i+1:]):continue
            inputs=[*pre,Q-set().union(*pre)];options=[]
            for source,target in zip(inputs,targets):
                free=sorted(source-K);guards=sorted(source&K);choices=[]
                for values in permutations(sorted(target),len(free)):
                    for g in product(sorted(target),repeat=len(guards)):
                        choices.append(dict(zip([*free,*guards],[*values,*g])))
                options.append(choices)
            rows=[]
            for parts in product(*options):
                row=[-1]*n
                for part in parts:
                    for q,t in part.items():row[q]=t
                assert min(row)>=0;rows.append(row)
            rows.sort();assert len(rows)==len(set(map(tuple,rows)))
            fields.append(dict(pre=[sorted(p) for p in pre],rows=rows))
        assert rawtuples==120 and len(fields)==16
        reports.append(dict(n=n,raw_preimage_tuples=rawtuples,fields=fields,complete_individual_rows=sum(len(f['rows']) for f in fields)))
    names=[Path(__file__).name,'C4_D125_E6_UNRESTRICTED_EXCLUSION.md']
    report=dict(status='complete_individual_control_rows',records=reports,
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Complete finite individual row controls only. The uniform paper argument, not finite negative samples, excludes unrestricted E6 at(13,9,1).')
    (ROOT/'c4_d125_e6_individual_controls.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps([dict(n=z['n'],fields=len(z['fields']),rows=z['complete_individual_rows']) for z in reports]),flush=True)
if __name__=='__main__':main()
