"""Independent finite audit of the uniform codimension-three construction."""
import json
from math import lcm
from pathlib import Path
from verify_certificates import ac,apply,strong
from codimension_three import construct

ROOT=Path(__file__).resolve().parent

def audit(n,r):
    z=construct(n,r);rows=z["rows"];L=n-5
    zz,v,y,t,c,d=L-1,L,L+1,L+2,L+3,L+4
    Q=set(range(n));S=set(z["S"]);A=set(z["A"])
    assert len(S)==n-3 and len(A)==r and A<S
    assert strong(rows) and apply(Q,z["reaching"],rows)==S
    assert len(apply(Q,z["reset"],rows))==1
    assert ac(rows,S,A)==z["value"]==min(n-r,9)
    image=apply(S,z["attaining"],rows)
    assert len(z["attaining"])==z["value"] and (len(image)<len(S) or not A<=image)
    H=[{y,c,d},{t,c,d},{v,t,d},{v,t,c},{v,y,d},{v,y,t},{zz,v,t},{v,y,c},
       {0,v,y},{y,t,c},{0,v,t},{1,y,c},{zz,t,d},{1,v,y},{1,t,d},{2,t,c},{0,v,d}]
    level=[0,1,2,3,3,4,5,5,6,6,7,7,7,8,8,8,8]
    edges=[(1,1),(1,2),(3,4),(2,5),(3,0),(6,7),(5,8),(2,9),(10,11),(12,3),(10,13),(14,15),(9,16)]
    assert Q-S==H[0]
    for i,successors in enumerate(edges):
        for letter,j in zip("ab",successors):
            T=apply(Q-H[i],letter,rows)
            assert len(T)==n-3 and Q-T==H[j] and level[j]<=level[i]+1
    N=lcm(L,4)
    assert apply({d,zz},"b"*4+"a"+"b"*(N-4),rows)=={c,zz}
    assert all(apply({q},"b"*N,rows)=={q} for q in Q)
    return {key:z[key] for key in ("n","s","r","alphabet_size","rows","S","A","value",
                                   "reaching","attaining","reset","source")}

def main():
    records=[audit(n,r) for n in range(10,25) for r in range(1,n-4)]
    data=dict(verified=True,records=records,instances=len(records),maximum_n=24,
              scope="Finite implementation audit; uniform proof is in PROOF.md#problem4-codimension-three-proof.")
    (ROOT/"codimension_three_audit.json").write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps(dict(verified=True,instances=len(records),minimum_n=10,maximum_n=24)))

if __name__=="__main__":
    main()
