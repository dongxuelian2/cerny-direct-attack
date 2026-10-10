"""Adversarial finite check of the set-pair lemma used for synthesis cuts."""
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
from alphabet_check import pair_distances

ROOT=Path(__file__).resolve().parent

def maximum_sequence(n,m,edges):
    holes=[set(H) for H in combinations(range(n),m)]
    masks=[]
    for H in holes:
        masks.append(sum(1<<i for i,E in enumerate(edges) if set(E)&H))
    @lru_cache(None)
    def length(P):
        return max([0]+[1+length(P&C) for C in masks if P&C!=P])
    return length((1<<len(edges))-1)

def main():
    count=0
    for n in range(3,7):
        allpairs=list(combinations(range(n),2))
        for m in range(1,min(3,n-2)+1):
            for q in range(1,m+2):
                for edges in combinations(allpairs,q):
                    assert maximum_sequence(n,m,edges)==q
                    count+=1
    z=json.loads((ROOT/"ternary_control_n5.json").read_text())["witness"]
    distances=pair_distances(z["rows"])
    sizes={h:sum(value<=h for value in distances.values()) for h in range(1,4)}
    assert all(sizes[h]<=h for h in sizes)
    report=dict(verified=True,pair_families_checked=count,positive_control_counts=sizes,
                scope="Checks a proved combinatorial pruning lemma, not a negative automaton theorem.")
    (ROOT/"short_pair_structure_audit.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report))

if __name__=="__main__":
    main()
