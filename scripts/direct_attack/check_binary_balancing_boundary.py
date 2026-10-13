"""Independent exact finite row/Boolean-dual and completeness audit."""
from copy import deepcopy
from math import factorial
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]

def col(f):
    out=[0]*len(f)
    for q in f:out[q]+=1
    return out

def check(data):
    records=data['records'];assert len(records)==4 and [z['n'] for z in records]==[2,3,4,5]
    inputs=eligible=negative=positive=controls=0;scopes=[]
    for z in records:
        n=z['n'];F=z['F'];B=z['B'];duals=z['duals']
        assert len(F)==factorial(n)//2 and len({tuple(f) for f in F})==len(F)
        assert all(len(f)==n and all(type(q) is int and 1<=q<n for q in f) and col(f)==[0,2]+[1]*(n-2) for f in F)
        assert len(B)==factorial(n) and len({tuple(b) for b in B})==len(B)
        assert all(len(b)==n and sorted(b)==list(range(n)) for b in B)
        assert len(duals)==len(F) and all(len(r)==len(B) for r in duals)
        totals=[0,0,0]
        for i,f in enumerate(F):
            for j,b in enumerate(B):
                cf=col(f);cff=col([f[f[q]] for q in range(n)]);cfb=col([b[f[q]] for q in range(n)]);controls+=2*n
                D=[q-1 for q in cf];E=[q-1 for q in cff];T=[q-1 for q in cfb]
                assert D[0]==E[0]==-1 and D[1]==1 and E[1]>=0
                code=duals[i][j];assert type(code) is int and code in (0,1,2);totals[code]+=1;inputs+=1
                if code==0:
                    assert all(x+y==0 for x,y in zip(D,T)) and b[0]==1 and b[1]==0;eligible+=1
                elif code==1:
                    assert D[0]<0 and E[0]<=0 and T[0]<=0;negative+=1
                else:
                    assert D[1]>0 and E[1]>=0 and T[1]>=0;positive+=1
                assert (code==0)==(b[0]==1 and b[1]==0)
        assert totals[0]==factorial(n)*factorial(n-2)//2
        assert totals[1]==factorial(n)//2*(factorial(n)-factorial(n-1))
        assert totals[2]==factorial(n)//2*(factorial(n-1)-factorial(n-2))
        scopes.append(dict(n=n,inputs=len(F)*len(B),eligible=totals[0],negative_duals=totals[1],positive_duals=totals[2]))
    assert (inputs,eligible,negative,positive)==(7508,388,5989,1131)
    return dict(verified=True,inputs=inputs,eligible=eligible,dual_infeasible=negative+positive,negative_state_duals=negative,positive_state_duals=positive,
                literal_composition_controls=controls,complete_scopes=scopes,
                boundary='Independent exact7508 canonical binary matrix cover n2..5, complete row/permutation counts and single-coordinate Farkas duals for7120 infeasible inputs,388 positive alpha=beta_b=1 witnesses. No LP/gen/solver import, no ordinary threshold rerun, no ALLn computational/formal claim. ALLn equivalence is PROVED paper; general Cerny OPEN.')

def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/binary_balancing_boundary.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    for mode in range(8):
        bad=deepcopy(data)
        if mode==0:bad['records'].pop()
        if mode==1:bad['records'][0]['F'][0][0]=0
        if mode==2:bad['records'][0]['B'].pop()
        if mode==3:bad['records'][0]['duals'][0][0]=0
        if mode==4:bad['records'][0]['duals'][0][1]=1
        if mode==5:bad['records'][-1]['F'].pop()
        if mode==6:bad['records'][-1]['B'][0]=bad['records'][-1]['B'][1][:]
        if mode==7:bad['records'][-1]['duals'][0].pop()
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError('accepted corruption')
    out['corruptions_rejected']=rejected
    (ROOT/'scripts/direct_attack/data/binary_balancing_boundary_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
