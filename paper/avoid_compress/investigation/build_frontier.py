"""Assemble complete finite lower witnesses through n=12."""
import json
from pathlib import Path
from alphabet_check import certificate
from cofinal_family import construct,boundary
from defect_two import construct as defect_two,construct_one

ROOT=Path(__file__).resolve().parent

def main():
    pool=[]
    for name,key in (("formula_certificates.json","certificates"),
                     ("mutation_certificates.json","certificates"),
                     ("codimension_three_audit.json","records"),
                     ("subdivide_probe.json","certificates")):
        pool.extend(json.loads((ROOT/name).read_text())[key])
    for name in ("reuse_n11.json","reuse_n12.json"):
        pool.extend(dict(z,source=name) for z in json.loads((ROOT/name).read_text())["results"])
    for n in (11,12):
        for r in range(1,n):
            for s in range(r+3,n):
                g=s-r-1;M=n-r-1
                if M<2*g:
                    continue
                base=boundary(r,g) if M==2*g else construct(r,g,M)
                z=certificate(base["rows"],base["S"],r)
                assert z and z["value"]==n-r
                z["source"]="cofinal construction independently certified at finite parameter"
                pool.append(z)
        for r in range(1,n-5):
            base=defect_two(n,r);z=certificate(base["rows"],base["S"],r)
            assert z and z["value"]==6
            z["source"]="codimension-two construction"
            pool.append(z)
        for r in range(1,n-2):
            base=construct_one(n,r);z=certificate(base["rows"],base["S"],r)
            assert z and z["value"]==3
            z["source"]="codimension-one construction"
            pool.append(z)
    best={}
    for z in pool:
        if not 2<=z["n"]<=12 or len(z["rows"])!=2:
            continue
        key=z["n"],z["s"],z["r"]
        if key not in best or z["value"]>best[key]["value"]:
            best[key]=z
    records=[];unresolved_bin=[];unresolved_any=[]
    for n in range(2,13):
        for s in range(2,n+1):
            for r in range(1,s):
                z=best[n,s,r];U=min(n-r,(n-s+2)*(n-s+1)//2)
                upper=9 if (n,s,r) in {(11,8,1),(12,9,1),(12,9,2)} else U
                assert z["value"]<=upper
                record={key:z[key] for key in ("n","s","r","value","rows","S","A",
                                                "reaching","attaining","reset","source")}
                record.update(alphabet_size=2,binary_upper=upper,unrestricted_upper=U,
                              exact_binary=z["value"]==upper,
                              exact_unrestricted=z["value"]==U)
                records.append(record)
                if record["value"]<upper:
                    unresolved_bin.append(dict(n=n,s=s,r=r,lower=record["value"],upper=upper))
                if record["value"]<U:
                    unresolved_any.append(dict(n=n,s=s,r=r,lower=record["value"],upper=U))
    assert len(records)==286
    assert not unresolved_bin
    assert {(z["n"],z["s"],z["r"]) for z in unresolved_any}=={(11,8,1),(12,9,1),(12,9,2)}
    extra=json.loads((ROOT/"n13_proposal_audit.json").read_text())["binary_reductions"][0]
    assert (extra["n"],extra["s"],extra["r"],extra["value"])==(13,8,1,12)
    record={key:extra[key] for key in ("n","s","r","value","rows","S","A",
                                      "reaching","attaining","reset")}
    record.update(alphabet_size=2,binary_upper=12,unrestricted_upper=12,
                  exact_binary=True,exact_unrestricted=True,
                  source="Independent BFS audit of binary reduction at (13,8,1)")
    records.append(record)
    for r in (1,2,3):
        extra=next(z for z in pool if (z['n'],z['s'],z['r'])==(13,10,r) and z['value']==9)
        record={key:extra[key] for key in ('n','s','r','value','rows','S','A','reaching','attaining','reset','source')}
        record.update(alphabet_size=2,binary_upper=9,unrestricted_upper=10,
                      exact_binary=True,exact_unrestricted=False)
        records.append(record)
        unresolved_any.append(dict(n=13,s=10,r=r,lower=9,upper=10))
    data=dict(maximum_n=13,complete_through_n=12,certificates=records,
              unresolved_binary=unresolved_bin,unresolved_unrestricted=unresolved_any,
              scope="Complete finite frontier through n=12 plus (13,8,1) and (13,10,r=1,2,3). No assertion for other n>=13 parameters.")
    (ROOT/"frontier_certificates.json").write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps(dict(witnesses=290,exact_binary=290,exact_unrestricted=284,
                         unresolved_binary=unresolved_bin,unresolved_unrestricted=unresolved_any)))

if __name__=="__main__":
    main()
