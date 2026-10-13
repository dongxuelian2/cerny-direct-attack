"""Source-independent local Bellman and literal original-label checker."""
from copy import deepcopy
from itertools import permutations
import json
from pathlib import Path

def stepword(rows,w,q):
    for i in w:assert 0<=i<len(rows);q=rows[i][q]
    return q

def bellman(rows,costs,d):
    n=len(rows[0]);assert len(d)==1<<n;edges=0
    for S,value in enumerate(d):
        assert value is None or type(value) is int and value>=0
        if S.bit_count()<=1:assert value==0;continue
        values=[]
        for row,cost in zip(rows,costs):
            T=0
            for q in range(n):
                if S>>q&1:T|=1<<row[q]
            if d[T] is not None:values.append(cost+d[T])
            edges+=1
        assert value==(min(values) if values else None)
    return edges

def verify_word(rows,costs,d,w):
    if d[-1] is None:assert w is None;return 0
    assert w is not None and sum(costs[i] for i in w)==d[-1]
    assert len({stepword(rows,w,q) for q in range(len(rows[0]))})==1
    return len(rows[0])*len(w)

def check(data):
    records=data['records'];assert len(records)==872;seen={n:set() for n in range(3,8)};edges=letters=sync=fail=0
    for z in records:
        n=z['n'];A=z['A'];assert n in seen and tuple(A) not in seen[n] and sorted(A)==list(range(1,n));seen[n].add(tuple(A))
        rows=z['rows'];assert rows[0]==[A[0]]+A and len(rows[1])==n
        for q in range(n):
            inverse=0 if q==0 else A.index(q)+1;assert rows[1][q]==(inverse+1)%n
        for w,row in zip(([1,0],[1,1,0]),z['return_rows']):
            assert row==[stepword(rows,w,q)-1 for q in range(1,n)]
        # Local positive-cost Bellman equations uniquely certify ALL subset
        # distances: finite levels descend to a singleton; None vertices
        # have no edge into the finite part. No Dijkstra or generator import.
        edges+=bellman(rows,[1,1],z['original_costs']);edges+=bellman(z['return_rows'],[2,3],z['return_costs'])
        assert (z['original_costs'][-1] is None)==(z['return_costs'][-1] is None)
        letters+=verify_word(z['return_rows'],[2,3],z['return_costs'],z['return_word'])
        if z['return_word'] is not None:
            original=[0]
            for label in z['return_word']:original+=([1,0] if label==0 else [1,1,0])
            assert len(original)==z['return_costs'][-1]+1 and len({stepword(rows,original,q) for q in range(n)})==1
            letters+=n*len(original);sync+=1;fail+=len(original)>(n-1)**2
    for n in seen:assert seen[n]==set(permutations(range(1,n)))
    z=data['counter'];rows=z['rows'];assert rows==[[0,1,2,4,3,3],[1,3,5,0,2,4]] and z['entered_set']==list(range(5))
    assert z['return_rows']==[[stepword(rows,w,q) for q in range(5)] for w in ([1,0],[1,1,0])]
    assert z['extra_rows']==[[stepword(rows,[0],q) for q in range(5)]]+z['return_rows']
    edges+=bellman(rows,[1,1],z['original_costs']);edges+=bellman(z['return_rows'],[2,3],z['return_costs']);edges+=bellman(z['extra_rows'],[1,2,3],z['extra_costs'])
    assert (z['original_costs'][-1],z['return_costs'][-1],z['extra_costs'][-1])==(25,25,24)
    letters+=verify_word(z['return_rows'],[2,3],z['return_costs'],z['return_word']);letters+=verify_word(z['extra_rows'],[1,2,3],z['extra_costs'],z['extra_word'])
    for labelset,key in (([[1,0],[1,1,0]],'return_word'),([[0],[1,0],[1,1,0]],'extra_word')):
        original=[0]
        for label in z[key]:original+=labelset[label]
        assert len(original)==(26 if key=='return_word' else 25)
        assert len({stepword(rows,original,q) for q in range(6)})==1;letters+=6*len(original)
    return dict(verified=True,cases=len(records),sync=sync,cf_only_square_failures=fail,bellman_edges=edges,literal_particle_letter_controls=letters,
                counter_costs=dict(original=25,cf_only=25,all_three=24,entered_cf=26,entered_all_three=25),
                boundary='Independent complete normal-form permutation coverage n3..7; ALL subset positive-cost Bellman certificates and literal paid returns. All-n qualitative equivalence separately PROVED paper; c/f-only square shortcut REFUTED at n6. No general paid square or formal proof; Cerny OPEN.')

def main():
    data=json.loads(Path('scripts/direct_attack/data/almost_circular_returns.json').read_text());out=check(data);rejected=[]
    for mode in range(8):
        bad=deepcopy(data);z=bad['records'][0]
        if mode==0:z['A'][0]=0
        if mode==1:z['rows'][1][0]=0
        if mode==2:z['return_rows'][0][0]=(z['return_rows'][0][0]+1)%2
        if mode==3:z['original_costs'][3]=99
        if mode==4:bad['counter']['return_costs'][-1]=24
        if mode==5:bad['counter']['extra_word'].pop()
        if mode==6:bad['records'].pop()
        if mode==7:bad['counter']['extra_rows'][0][0]=1
        try:check(bad)
        except (AssertionError,KeyError,ValueError):rejected.append(mode)
        else:raise AssertionError('corruption accepted')
    out['corruptions_rejected']=rejected
    Path('scripts/direct_attack/data/almost_circular_returns_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
