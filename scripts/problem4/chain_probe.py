"""Test a direct reachable-image chain variant; finite evidence only."""
import json
from pathlib import Path
from audit_small import bfs, strong

def chain(n, s, r):
    m = n-s
    assert m >= 1 and s >= 2 and 1 <= r < s
    a = [max(q-1, 0) if q <= m else q for q in range(n)]
    b = list(range(n))
    b[0] = b[m] = m+1
    for q in range(m+1, n-1):
        b[q] = q+1
    b[n-1] = m
    S = frozenset([0] + list(range(m+1, n)))
    A = frozenset(range(n-r, n))
    return [a,b], S, A

def main():
    results = []
    for n in range(4, 15):
        for s in range(3, n):
            for r in range(1, s-1):
                rows,S,A = chain(n,s,r)
                assert strong(rows)
                reaching,_ = bfs(rows, range(n), lambda T:T==S)
                reset,_ = bfs(rows, range(n), lambda T:len(T)==1)
                attaining,_ = bfs(rows, S, lambda T:len(T)<s or not A <= T)
                assert reaching is not None
                bound = min(n-r,(n-s+2)*(n-s+1)//2)
                results.append(dict(n=n,s=s,r=r,value=None if attaining is None else len(attaining),candidate_bound=bound,
                                    synchronizing=reset is not None,
                                    rows=rows,S=sorted(S),A=sorted(A),reaching=reaching,
                                    attaining=attaining,reset=reset))
    out=dict(exhaustive_all_automata=False,scope='Finite chain variant, n=4..14; no uniform claim.',results=results)
    Path(__file__).with_name('chain_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(records=len(results),sharp=sum(z['value']==z['candidate_bound'] for z in results),
                         failures_in_linear_dominated_range=[(z['n'],z['s'],z['r'],z['value'],z['candidate_bound'])
                         for z in results if z['n']-z['r']<=2*(z['n']-z['s'])+1 and z['value']!=z['candidate_bound']][:12])))

if __name__=='__main__':main()
