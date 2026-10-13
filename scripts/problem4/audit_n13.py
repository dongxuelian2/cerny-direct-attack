"""Independent literal certificates and bounded binary reductions of n=13 proposals."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path
from alphabet_check import apply,bfs,certificate,pair_distances,strong,verify

ROOT=Path(__file__).resolve().parent

def main():
    records=[]
    for s,k in ((9,2),(8,2),(9,3),(8,3)):
        data=json.loads((ROOT/f"mutate_n13_s{s}_r1_k{k}.json").read_text())
        S={q for q in range(13) if data["S_mask"]>>q&1}
        z=certificate(data["rows"],S,1)
        assert z and verify(z) and z["value"]==data["value"]
        z["source"]="Independently audited stochastic proposal"
        records.append(z)
        print(json.dumps({key:z[key] for key in ("n","s","r","alphabet_size","value","compression")}))
    ternary=records[-1]
    assert ternary["value"]==12
    (ROOT/"ternary_n13_certificate.json").write_text(json.dumps(ternary,indent=2)+"\n")
    rows=ternary["rows"];identity=tuple(range(13));todo=deque([identity]);group={identity:""}
    while todo:
        row=todo.popleft()
        for i in (0,2):
            T=tuple(rows[i][q] for q in row)
            if T not in group:group[T]=group[row]+"abc"[i];todo.append(T)
    assert len(group)==54
    reductions=[]
    for perm,word in group.items():
        binary=[list(perm),rows[1]]
        if not strong(binary) or len(pair_distances(binary))!=78:continue
        # Every actual reachable size-eight image is checked in this fixed scope.
        _,images=bfs(binary,range(13),lambda S:False)
        for S in images:
            if len(S)!=8:continue
            z=certificate(binary,S,1)
            assert z and verify(z)
            if z["value"]>=12:
                z["permutation_word_in_ternary_base"]=word;reductions.append(z)
                print("binary attaining reduction found",word)
                break
        if reductions:break
    out=dict(certificates=records,binary_reductions=reductions,permutation_group_order=54,
             scope="Finite positive certificates. Binary reduction failures cover only the fixed 54-permutation group with one fixed singular letter.")
    (ROOT/"n13_proposal_audit.json").write_text(json.dumps(out,indent=2)+"\n")
    print("binary attaining reductions",len(reductions))

if __name__=="__main__":main()
