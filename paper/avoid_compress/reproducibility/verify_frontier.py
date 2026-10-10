"""Independent ordinary subset-BFS audit of all finite frontier certificates."""
import json
from pathlib import Path
from verify_certificates import ac,apply,strong

ROOT=Path(__file__).resolve().parent

def main():
    data=json.loads((ROOT/"frontier_certificates.json").read_text())
    found=set();exact_bin=exact_any=0;unresolved_bin=set();unresolved_any=set()
    for z in data["certificates"]:
        n,s,r=z["n"],z["s"],z["r"];S=set(z["S"]);A=set(z["A"]);rows=z["rows"]
        assert z["alphabet_size"]==len(rows)==2
        assert all(len(row)==n and set(row)<=set(range(n)) for row in rows)
        assert len(S)==s and len(A)==r and A<S
        assert strong(rows) and apply(range(n),z["reaching"],rows)==S
        assert len(apply(range(n),z["reset"],rows))==1
        assert ac(rows,S,A)==z["value"]==len(z["attaining"])
        T=apply(S,z["attaining"],rows)
        assert len(T)<s or not A<=T
        U=min(n-r,(n-s+2)*(n-s+1)//2)
        B=min(U,9) if n>=6 and n-s==3 else U
        assert z["binary_upper"]==B and z["unrestricted_upper"]==B
        assert z["exact_binary"]==(z["value"]==B)
        assert z["exact_unrestricted"]==(z["value"]==B)
        key=(n,s,r)
        assert key not in found;found.add(key)
        if z["exact_binary"]:exact_bin+=1
        else:unresolved_bin.add(key)
        if z["exact_unrestricted"]:exact_any+=1
        else:unresolved_any.add(key)
    expected={(n,s,r) for n in range(2,13) for s in range(2,n+1) for r in range(1,s)}
    expected.add((13,8,1))
    expected.update((13,10,r) for r in (1,2,3))
    assert found==expected and len(found)==290
    assert (exact_bin,exact_any)==(290,290)
    assert unresolved_bin==set()
    assert unresolved_any==set()
    upper=json.loads((ROOT/'codimension_three_upper_audit.json').read_text())
    assert upper['status']=='pass' and upper['all_types_excluded']
    assert upper['ordered_pair_types']==9 and upper['independent_profiles_flags_vectors_match']
    report=dict(verified=True,witnesses=290,exact_binary=290,exact_unrestricted=290,
                maximum_n=13,complete_through_n=12,
                additional_exact_parameters=[dict(n=13,s=8,r=1,value=12)]+[dict(n=13,s=10,r=r,value=9) for r in (1,2,3)],
                unresolved_binary=sorted(unresolved_bin),unresolved_unrestricted=sorted(unresolved_any),
                scope="All binary and unrestricted triples through n=12 plus (13,8,1) and (13,10,r=1,2,3) are exact. Other n>=13 parameters are not classified by this finite file. The codimension-three upper uses the uniform nine-type proof and complete action certificates.")
    (ROOT/"frontier_audit.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report))

if __name__=="__main__":
    main()
