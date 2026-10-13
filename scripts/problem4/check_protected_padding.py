"""Independent subset/transition audit of protected padding and its finite base."""
from collections import deque
import json
from pathlib import Path
from verify_certificates import ac,apply,strong
from protected_padding import construct

ROOT=Path(__file__).resolve().parent

def base_graph():
    # Literal manuscript rows: this computation does not take its input
    # transitions or expected answers from the family generator.
    rows=[[0,1,2,4,3,6,7,8,9,10,11,5],
          [8,0,1,2,3,6,7,4,9,10,4,11]]
    z=dict(rows=rows,S=list(range(8)))
    start=frozenset(z["S"])
    queue=deque([start]);distance={start:0}
    while queue:
        S=queue.popleft();depth=distance[S]
        assert len(S)==8 and 0 in S
        if depth<=9:assert 1 in S
        if depth==10:continue
        for row in rows:
            T=frozenset(row[q] for q in S)
            assert len(T)==8 and 0 in T
            if T not in distance:
                distance[T]=depth+1;queue.append(T)
    assert len(distance)==62
    assert [sum(d==level for d in distance.values()) for level in range(11)]==[1,1,1,1,1,2,4,7,9,13,22]
    states=sorted(distance,key=lambda S:(distance[S],sum(1<<q for q in S)))
    index={S:i for i,S in enumerate(states)}
    graph=[]
    for S in states:
        depth=distance[S]
        successors=[index[frozenset(row[q] for q in S)] for row in rows] if depth<10 else None
        graph.append(dict(S=sorted(S),level=depth,successors=successors))
    assert ac(rows,z["S"],[0])==11 and ac(rows,z["S"],[0,1])==10
    assert len(apply(z["S"],"aaaaaabaaab",rows))<8
    assert 1 not in apply(z["S"],"aaaaaababb",rows)
    result=dict(rows=rows,S=z["S"],graph=graph,vertices=62,
                base_values=[dict(A=[0],value=11),dict(A=[0,1],value=10)],
                scope="Complete short-image certificate through length ten.")
    (ROOT/"protected_padding_base.json").write_text(json.dumps(result,indent=2)+"\n")
    return result

def audit(target,r,base):
    z=construct(target,r);n=z["n"];k=n-12;rows=z["rows"]
    S=set(z["S"]);A=set(z["A"]);H=set(range(12,n));B=set(range(5))|H|{8,9,10};E=B|{11}
    expected_a=base["rows"][0]+list(range(12,n))
    expected_b=base["rows"][1]+list(range(12,n))
    chain=[0]+sorted(H)+[8]
    for q,t in zip(chain,chain[1:]):expected_b[q]=t
    assert rows==[expected_a,expected_b]
    assert len(S)==z["s"] and len(A)==r and A<S
    assert strong(rows) and apply(range(n),"bbb",rows)==E
    e=z["root_retraction"]
    assert all(apply([q],e,rows)==({8} if q==11 else {q}) for q in E)
    assert apply(range(n),z["reaching"],rows)==S
    f="a"+e;h="ab"+e
    # f^3 is the adjacent transposition p_3 <-> p_4 on the b-cycle B.
    assert all(apply([q],f*3,rows)==({4} if q==3 else {3} if q==4 else {q}) for q in B)
    assert rows[1][4]==3
    assert len(apply(B,h,rows))==len(B)-1 and apply(B,h,rows)<=B
    for state in base["graph"]:
        T=set(state["S"])
        assert 0 in T
        for letter,row in zip("ab",base["rows"]):
            assert apply(T|H,letter,rows)=={row[q] for q in T}|H
    assert ac(rows,S,A)==target
    assert len(z["attaining"])==target
    T=apply(S,z["attaining"],rows)
    assert len(T)<len(S) or not A<=T
    assert len(apply(range(n),z["reset"],rows))==1
    return {key:z[key] for key in ("n","s","r","alphabet_size","rows","S","A","value",
                                   "reaching","attaining","reset","source")}

def main():
    base=base_graph()
    records=[audit(target,r,base) for target in (10,11)
             for r in range(2 if target==10 else 1,21)]
    protected_subsets=[]
    for n in range(12,32):
        z=construct(11,n-11)
        H=list(range(12,n))
        for r in range(1,n-10):
            A=[0]+H[:r-1]
            assert len(A)==r and ac(z["rows"],z["S"],A)==11
            protected_subsets.append(dict(n=n,s=n-4,r=r,value=11))
    data=dict(verified=True,base_vertices=62,instances=len(records),maximum_n=max(z["n"] for z in records),
              records=records,
              protected_subset_instances=len(protected_subsets),protected_subsets=protected_subsets,
              scope="Finite checks of a uniform paper proof. Ten-band r=1 is the separately certified (11,7,1) point.")
    (ROOT/"protected_padding_audit.json").write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps({key:data[key] for key in ("verified","base_vertices","instances","maximum_n","protected_subset_instances")}))

if __name__=="__main__":
    main()
