"""Independent complete n4 controls for the fixed two-by-two image trap."""
from pathlib import Path
from itertools import product,combinations
from collections import deque
import hashlib,json
ROOT=Path(__file__).resolve().parent
K={0,1};Z={2,3};Q=set(range(4));R=Q-K;C=Q-Z

def forward_distance(pair,rows):
    start=frozenset(pair);todo=deque([(start,0)]);seen={start}
    while todo:
        X,d=todo.popleft()
        if len(X)==1:return d
        for row in rows:
            Y=frozenset(row[q] for q in X)
            if Y not in seen:seen.add(Y);todo.append((Y,d+1))
    return None

def closure(rows):
    frames={frozenset(R)}
    for _ in range(2):
        for X in list(frames):
            for row in rows:
                Y=frozenset(row[q] for q in X)
                assert Y in (R,C);frames.add(Y)
    assert all(frozenset(row[q] for q in X) in frames for X in frames for row in rows)
    return sorted(map(sorted,frames))

def main():
    pool=[row for row in product(range(4),repeat=4) if row[2]!=row[3]]
    assert len(pool)==192
    qualified=sync=total=0;by_alpha=[]
    for alpha in (1,2):
        count=hits=0
        for rows in product(pool,repeat=alpha):
            count+=1;ds={p:forward_distance(p,rows) for p in combinations(range(4),2)}
            if any(ds[tuple(sorted((k,z)))] is None or ds[tuple(sorted((k,z)))]>2 for k in K for z in Z):continue
            if ds[(2,3)] is not None and ds[(2,3)]<=4:continue
            hits+=1;closure(rows)
            assert not all(v is not None for v in ds.values())
        total+=count;qualified+=hits;by_alpha.append(dict(alphabet_size=alpha,complete_ordered_controls=count,qualified_nonsynchronizing=hits))
    assert total==37056
    rows=[(2,3,2,3),(2,3,1,0)]
    assert all((d:=forward_distance((k,z),rows)) is not None and d<=2 for k in K for z in Z)
    assert forward_distance((2,3),rows) is None and forward_distance((0,1),rows) is None
    for q in Q:
        todo=[q];seen={q}
        for p in todo:
            for row in rows:
                if row[p] not in seen:seen.add(row[p]);todo.append(row[p])
        assert seen==Q
    names=[Path(__file__).name,'SATURATED_TWO_GUARD_TRAP.md']
    report=dict(status='pass',complete_individual_rows=192,complete_ordered_alphabets=total,
        finite_control_stats=by_alpha,qualified_nonsynchronizing_controls=qualified,
        strongly_connected_nonsynchronizing_control=dict(rows=rows,closed_frames=closure(rows)),
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Paper proof for all n>=4 and finite alphabets; complete n4 one/two-letter controls supplement it. No new extremum.')
    (ROOT/'saturated_two_guard_trap_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
