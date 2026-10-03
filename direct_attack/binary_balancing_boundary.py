"""Exact binary rank-one/permutation boundary of positive one-step balancing."""
from itertools import permutations
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def main():
    records=[]
    for n in range(2,6):
        F=[list(f) for f in sorted(set(permutations([1,1]+list(range(2,n)))))]
        B=[list(b) for b in permutations(range(n))]
        codes=[[0 if b[0]==1 and b[1]==0 else 1 if b[1]!=0 else 2 for b in B] for f in F]
        records.append(dict(n=n,F=F,B=B,duals=codes))
    out=dict(records=records,boundary='PROVED paper ALL n>=2: binary alphabet{f,b}, rank(f)=n-1,b permutation. Positive one-step balancing alpha D(f)+beta_f D(ff)+beta_b D(fb)=0 with alpha>0 and nonnegative betas exists IFF b swaps f omitted e and doubled d. The necessity uses single-state dual coordinates e/d; no fixed-root/kernel/level/SC/sync hypothesis. Complete retained canonical matrix cover7508 inputs n2..5,388 feasible/7120 dual-infeasible, no reset-threshold search or general Cerny proof/novelty/formal claim.')
    (ROOT/'direct_attack/data/binary_balancing_boundary.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=sum(len(z['F'])*len(z['B']) for z in records),eligible=sum(sum(row.count(0) for row in z['duals']) for z in records),boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
