"""Independent verification of stochastic proposals, also testing every r."""
import json
from pathlib import Path
from alphabet_check import bfs, certificate, verify, apply

ROOT=Path(__file__).resolve().parent

def main():
    certified=[]
    names=["mutate_n11_s7_r1_k2.json","mutate_n11_s8_r1_k3.json",
           "mutate_n12_s8_r1_k2.json","mutate_n12_s9_r1_k3.json",
           "mutate_n12_s8_r1_k2_more.json","mutate_n12_s8_r2_k2_more.json"]
    names += [name for name in ("mutate_n11_s8_r1_k3_more.json",
                               "mutate_n12_s9_r2_k3_more.json")
              if (ROOT/name).exists()]
    for name in names:
        data=json.loads((ROOT/name).read_text())
        n,s=data["n"],data["s"]
        rows=data["rows"]
        S={q for q in range(n) if data["S_mask"]>>q&1}
        A={q for q in range(n) if data["A_mask"]>>q&1}
        assert len(S)==s and len(A)==data["r"] and A<S
        word,_=bfs(rows,S,lambda T:len(T)<s or not A<=T)
        assert len(word)==data["value"]
        for r in range(1,s):
            z=certificate(rows,S,r)
            assert z is not None and verify(z)
            z["source"]=name
            z["attains_known_upper"]=z["value"]==min(n-r,(n-s+2)*(n-s+1)//2)
            certified.append(z)
        print(json.dumps(dict(source=name,n=n,s=s,alphabet_size=len(rows),
                              scores={r:certified[-s+1+r-1]["value"] for r in range(1,s)})))
    report=dict(certificates=certified,
                scope="Finite lower witnesses only; no search failure is an upper bound.")
    (ROOT/"mutation_certificates.json").write_text(json.dumps(report,indent=2)+"\n")

if __name__=="__main__":
    main()
