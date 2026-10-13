"""Independent transitions, subset BFS, cell delays and pair-potential audit."""
from collections import deque
from itertools import combinations
from copy import deepcopy
import json
from pathlib import Path
from verify_certificates import ac,apply,strong

ROOT=Path(__file__).resolve().parent

def distances(rows,start):
    dist={q:0 for q in start};queue=deque(start)
    while queue:
        q=queue.popleft()
        for row in rows:
            v=row[q]
            if v not in dist:dist[v]=dist[q]+1;queue.append(v)
    return dist

def rebuild(p,t):
    P=[("P",i) for i in range(p)];X=[("X",i) for i in range(1,t+1)]
    Y=[("Y",i) for i in range(1,t+1)];Z=("Z",0)
    states=P+X+Y+[Z];index={q:i for i,q in enumerate(states)}
    a={q:q for q in states};a[P[-2]],a[P[-1]]=P[-1],P[-2]
    cycle=X+Y+[Z]
    for q,v in zip(cycle,cycle[1:]+cycle[:1]):a[q]=v
    b={Z:Z,P[0]:Y[0],X[-1]:P[-1],Y[-1]:P[-1]}
    for i in range(1,p):b[P[i]]=P[i-1]
    for block in (X,Y):
        for q,v in zip(block,block[1:]):b[q]=v
    return [[index[action[q]] for q in states] for action in (a,b)],states

def potential(E,p,t,labels):
    if len(E)==1:return 0
    q,v=sorted(E);kind,i=labels[q];other,j=labels[v];L=3*t+2
    if (kind,other) in (("P","P"),("P","X"),("X","X")):return L
    if kind=="P":
        rho=min(i,p-2)
        return min(L,2*t+2+rho) if other=="Z" else min(L,max(L-j,2*t+3+rho))
    if kind=="X":
        if other=="Z" or j>i:return 2*t-i+1
        return t-i+1 if i==j else L-j
    return 2*t+1 if other=="Z" else L-j

def audit(z):
    p,t,r=z["p"],z["t"],z["r"];n=p+2*t+1;s=p+t
    assert t>=2 and 1<=r<=p-3 and (z["n"],z["s"])==(n,s)
    rows,labels=rebuild(p,t);S=set(range(s));A=set(range(r))
    assert z["rows"]==rows and z["S"]==sorted(S) and z["A"]==sorted(A)
    assert strong(rows) and apply(range(n),z["reaching"],rows)==S
    assert len(apply(range(n),z["reset"],rows))==1
    expected=min(n-r,3*t+2)
    assert z["value"]==len(z["attaining"])==expected
    # Larger instances have exact finite lower certificates below: pair
    # potentials plus a checked signed cell identity and graph delays.
    # Avoid enumerating an exponentially large subset graph unnecessarily.
    if n<=35:assert ac(rows,S,A)==expected
    T=apply(S,z["attaining"],rows);assert len(T)<s or not A<=T
    avoid="a"*(2*t)+"ba"+"b"*(p-r-1)
    compression="a"*(2*t)+"b"+"a"*t+"b"
    assert r-1 not in apply(S,avoid,rows) and len(avoid)==n-r
    assert len(apply(S,compression,rows))<s and len(compression)==3*t+2
    B=set(range(p))|set(range(p+t,p+2*t));E=B|{n-1};e=z["retraction"]
    assert apply(range(n),"b"*t,rows)==E
    assert all(apply([q],e,rows)==({p+t} if q==n-1 else {q}) for q in E)
    assert apply(B,"ab"+e,rows)==B-{p+t+1}
    assert all(apply([q],"a"*(2*t+1),rows)==({p-1} if q==p-2 else
               {p-2} if q==p-1 else {q}) for q in B)
    cells=[i if kind=="P" else p+i-1 if kind in ("X","Y") else p
           for kind,i in labels]
    ca=list(range(s));ca[p-2],ca[p-1]=p-1,p-2
    for i in range(t):ca[p+i]=p+(i+1)%t
    cb=list(range(s));cb[0]=p
    for i in range(1,p):cb[i]=i-1
    for i in range(t-1):cb[p+i]=p+i+1
    cb[p+t-1]=p-1
    assert sorted(ca)==sorted(cb)==list(range(s))
    assert sorted(cells[q] for q in S)==list(range(s))
    for row,cellrow in zip(rows,(ca,cb)):
        for q in range(n):
            actual=cells[row[q]];predicted=cellrow[cells[q]]
            if q==n-1:assert (actual,predicted)==(p,p+1)
            else:assert actual==predicted
    assert distances(rows,S)[n-1]==t+1
    cell_d=distances([ca,cb],[p+1])
    assert min(cell_d[q] for q in A)==p+t-r-1
    pair_checks=0
    for pair in combinations(range(n),2):
        D=potential(set(pair),p,t,labels)
        if set(pair)<=S:assert D==3*t+2
        for row in rows:assert D<=1+potential({row[q] for q in pair},p,t,labels)
        pair_checks+=1
    return pair_checks

def main():
    data=json.loads((ROOT/"two_block_certificates.json").read_text())
    checks=sum(audit(z) for z in data["records"])
    corruptions=[]
    for field,bad in (("p",data["records"][0]["p"]+1),("r",0),
                      ("value",data["records"][0]["value"]-1),
                      ("reaching",""),("reset",""),("attaining",""),
                      ("S",data["records"][0]["S"][1:])):
        z=deepcopy(data["records"][0]);z[field]=bad;corruptions.append(z)
    z=deepcopy(data["records"][0]);z["rows"][0][0]=z["n"]-1;corruptions.append(z)
    for z in corruptions:
        try:audit(z)
        except AssertionError:continue
        raise AssertionError("corrupted certificate accepted")
    report=dict(verified=True,instances=len(data["records"]),maximum_n=data["maximum_n"],
                pair_checks=checks,transition_inequalities=2*checks,
                corruptions_rejected=len(corruptions),
                subset_bfs_instances=sum(z["n"]<=35 for z in data["records"]),
                larger_potential_cell_certificates=sum(z["n"]>35 for z in data["records"]),
                scope="Independent finite audit supporting the uniform symbolic proof; no extrapolated global upper bound.")
    (ROOT/"two_block_audit.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report))

if __name__=="__main__":main()
