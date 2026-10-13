"""Standard-library audit of the binary obstruction's data and lower witness.

This verifies saved run agreement and the explicit lower bound. The two C++
programs must be run to reproduce the finite negative cover itself.
"""
import json
from pathlib import Path
from verify_certificates import ac,apply,strong

ROOT=Path(__file__).resolve().parent

def main():
    z=json.loads((ROOT/'binary_obstruction_witness.json').read_text());rows=z['rows'];n=11;S=set(z['S']);A=set(z['A'])
    assert (z['n'],z['s'],z['r'],z['value'])==(11,8,1,9)
    assert strong(rows) and apply(range(n),z['reaching'],rows)==S
    assert len(apply(range(n),z['reset'],rows))==1 and ac(rows,S,A)==9
    assert len(z['attaining'])==9 and (len(apply(S,z['attaining'],rows))<8 or not A<=apply(S,z['attaining'],rows))
    assert len(apply(S,'ababbbaba',rows))<8
    zstate,v,y,t,c,d=5,6,7,8,9,10
    H=[{y,c,d},{t,c,d},{v,t,d},{v,t,c},{v,y,d},{v,y,t},{zstate,v,t},{v,y,c},
       {0,v,y},{y,t,c},{0,v,t},{1,y,c},{zstate,t,d},{1,v,y},{1,t,d},{2,t,c},{0,v,d}]
    level=[0,1,2,3,3,4,5,5,6,6,7,7,7,8,8,8,8]
    transition=[(1,1),(1,2),(3,4),(2,5),(3,0),(6,7),(5,8),(2,9),(10,11),(12,3),(10,13),(14,15),(9,16)]
    Q=set(range(n));assert Q-S==H[0]
    for i,successors in enumerate(transition):
        for letter,j in zip('ab',successors):
            image=apply(Q-H[i],letter,rows)
            assert len(image)==8 and Q-image==H[j] and level[j]<=level[i]+1
    assert all(A.isdisjoint(holes) for holes in H)
    e='aa';assert all(apply([q],e,rows)==({y} if q==t else {q}) for q in Q)
    assert all(apply([q],'b'*12,rows)=={q} for q in Q)
    # Independently check each pair is mergeable by ordinary forward BFS.
    from collections import deque
    for x in range(n):
        for q in range(x+1,n):
            seen={frozenset((x,q))};todo=deque(seen);merged=False
            while todo:
                pair=todo.popleft()
                if len(pair)==1:merged=True;break
                for row in rows:
                    image=frozenset(row[state] for state in pair)
                    if image not in seen:seen.add(image);todo.append(image)
            assert merged
    comparisons=[]
    for n in (6,7,8,9,11):
        first=json.loads((ROOT/f'decision_n{n}.json').read_text())
        second=json.loads((ROOT/f'decision_independent_n{n}.json').read_text())
        for key in ('n','s','target','completed','compression_witness_found','first_classes','visited_classes','candidate_strong_sync'):assert first[key]==second[key],(n,key)
        assert first['completed'] and not first['compression_witness_found'] and first['candidate_strong_sync']==0
        assert first['tree_nodes']==second['assignments'] and first['pruned_nodes']==second['discarded'] and first['complete_maps']==second['leaves']
        comparisons.append(dict(n=n,first_classes=first['first_classes'],assignments=first['tree_nodes'],prunes=first['pruned_nodes'],leaves=first['complete_maps']))
    for name in ('decision_n5.json','decision_independent_n5.json'):
        control=json.loads((ROOT/name).read_text());assert control['compression_witness_found']
        from collections import deque
        start=frozenset(control['S']);todo=deque([(start,0)]);seen={start};distance=None
        while todo:
            pair,length=todo.popleft()
            if len(pair)<2:distance=length;break
            for row in control['rows']:
                image=frozenset(row[q] for q in pair)
                if image not in seen:seen.add(image);todo.append((image,length+1))
        assert distance==10
    report=dict(binary_lower_witness_verified=True,hole_table_verified=True,pairs_checked=55,run_counts_match=True,comparisons=comparisons,
                scope='Binary maximum at (11,8,1) only. Original unrestricted-alphabet F is not refuted by this result.')
    (ROOT/'binary_obstruction_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__':main()
