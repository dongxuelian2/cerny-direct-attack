"""Independent symbolic-core and ordinary-set checks of the codimension-two family."""
import json
from pathlib import Path
from defect_two import construct,construct_one
from check_cofinal import apply
from subset_bfs import bfs,strong

ROOT=Path(__file__).resolve().parent

def audit(z):
    n,L,r=z['n'],z['L'],z['r'];rows=z['rows'];last=L-1;w=L;v=L+1;u=L+2
    rebuilt=[list(range(n)),[None]*n];T=list(range(L));K=[w,v,u]
    rebuilt[0][last]=u;rebuilt[0][u]=last;rebuilt[0][v]=last
    for cycle in (T,K):
        for source,target in zip(cycle,cycle[1:]+cycle[:1]):rebuilt[1][source]=target
    assert rebuilt==rows and strong(rows)
    assert apply(range(n),z['reaching'],rows)==set(z['S'])
    for q in range(n):
        assert apply([q],z['short_unit'],rows)==({u} if q==v else {q})
        assert apply([q],z['second_unit'],rows)==({w} if q==u else {q})
        assert apply([q],z['short_collapse'],rows)==({w} if q in K else {q})
        assert apply([q],z['root_macro'],rows)==({w} if q in K+[last] else {q})
    assert len(apply(range(n),z['reset'],rows))==1
    ac,graph=bfs(rows,z['S'],lambda S:len(S)<n-2 or not set(z['A'])<=S)
    assert len(ac)==6 and len(apply(z['S'],z['attaining'],rows))<n-2
    holes=[{w,u},{w,v},{u,v},{last,v},{0,u},{0,v},{1,w}]
    shortest=[0,1,2,3,4,5,5]
    transitions=[(1,1),(1,2),(3,0),(2,4),(5,6)]
    Q=set(range(n))
    for i,(a_target,b_target) in enumerate(transitions):
        for letter,target in zip('ab',[a_target,b_target]):assert Q-apply(Q-holes[i],letter,rows)==holes[target]
    assert all(set(z['A']).isdisjoint(H) for H in holes)
    return dict(z,safe_short_subsets=sum(len(word)<6 for word in graph.values()))

def main():
    records=[audit(construct(n,r)) for n in range(7,31) for r in range(1,n-5)]
    out=dict(status='Finite checks passed; uniform proof separate.',records=records,count=len(records),maximum_n=30)
    (ROOT/'defect_two_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=out['status'],count=out['count'],maximum_n=30)))
    one=[]
    for n in range(4,31):
        for r in range(1,n-2):
            z=construct_one(n,r);rows=z['rows'];S=set(z['S']);A=set(z['A'])
            assert strong(rows) and apply(range(n),z['reaching'],rows)==S
            assert len(apply(range(n),z['reset'],rows))==1
            for q in range(n):assert apply([q],z['short_unit'],rows)==({0} if q==1 else {q})
            word,_=bfs(rows,S,lambda T:len(T)<n-1 or not A<=T)
            assert len(word)==3 and len(apply(S,z['attaining'],rows))<n-1
            one.append(z)
    report=dict(status='Independent finite checks passed; uniform proof in DEFECT_TWO_PROOF.md.',count=len(one),records=one)
    (ROOT/'defect_one_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(defect_one_checked=len(one),maximum_n=30)))

if __name__=='__main__':main()
