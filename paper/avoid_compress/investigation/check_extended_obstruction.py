"""Saved complete-cover checks and independent BFS of the explicit controls.

Run both C++ covers to reproduce the upper bound itself. This script checks
their saved complete metadata, the independent width/orbit audits and the
actual reachable-image lower witnesses in the finite frontier.
"""
from collections import deque
import json
from pathlib import Path
from verify_certificates import ac,apply,strong

ROOT=Path(__file__).resolve().parent


def main():
    first=json.loads((ROOT/"extended_n12.json").read_text())
    inverse=json.loads((ROOT/"inverse_n12.json").read_text())
    for report in (first,inverse):
        assert (report["n"],report["s"],report["target"])==(12,9,10)
        assert report["completed"] and not report["compression_witness_found"]
        assert report["first_classes"]==report["visited_classes"]==303
        assert report["candidate_strong_sync"]==0 and report["rows"]==[[],[]] and report["S"]==[]
        assert not report.get("orbit_export_mode",False)
    assert (first["tree_nodes"],first["pruned_nodes"],first["complete_maps"])==(13325576985,5658183662,1315233389)
    assert (inverse["assignments"],inverse["discarded"],inverse["leaves"])==(4020074488,19995760,1374921673)
    control=json.loads((ROOT/"inverse_control_n5.json").read_text())
    assert control["compression_witness_found"] and control["candidate_strong_sync"]==1
    rows,S=control["rows"],frozenset(control["S"])
    todo=deque([(S,0)]);seen={S};compression=None
    while todo:
        states,depth=todo.popleft()
        if len(states)<2:compression=depth;break
        for row in rows:
            image=frozenset(row[q] for q in states)
            if image not in seen:seen.add(image);todo.append((image,depth+1))
    assert compression==10 and strong(rows)
    todo=deque([frozenset(range(5))]);seen={todo[0]}
    while todo:
        states=todo.popleft()
        for row in rows:
            image=frozenset(row[q] for q in states)
            if image not in seen:seen.add(image);todo.append(image)
    assert S in seen and any(len(image)==1 for image in seen)
    records=json.loads((ROOT/"frontier_certificates.json").read_text())["certificates"]
    lowers=[]
    for r in (1,2):
        z=next(z for z in records if (z["n"],z["s"],z["r"])==(12,9,r))
        assert z["alphabet_size"]==2 and strong(z["rows"])
        assert len(z["S"])==9 and len(z["A"])==r and set(z["A"])<set(z["S"])
        assert apply(range(12),z["reaching"],z["rows"])==set(z["S"])
        assert len(apply(range(12),z["reset"],z["rows"]))==1
        assert ac(z["rows"],z["S"],z["A"])==z["value"]==9
        lowers.append(dict(n=12,s=9,r=r,value=9))
    orbit=json.loads((ROOT/"inverse_enumeration_audit.json").read_text())
    assert orbit["verified"] and [(r["n"],r["canonical_first_forms"],r["second_orbits"],r["all_orbits_covered"])
                                  for r in orbit["records"]]==[(5,13,1065,True),(6,23,9272,True)]
    widths=json.loads((ROOT/"extended_width_audit.json").read_text())
    assert widths["verified"] and widths["cases"]==1000 and widths["maximum_pair_bits"]==120 and widths["maximum_hole_words"]==9
    result=dict(verified=True,binary_exact_points=lowers,unrestricted_interval=[9,10],
                first_forms=303,independent_completed_covers=2,counts_agree_expected=True,
                forward_assignments=first["tree_nodes"],inverse_assignments=inverse["assignments"],
                eligible_maps=0,positive_pair_control_verified=True,
                independent_labelled_orbit_audit=True,width_audit_cases=1000,
                scope="Only F_bin(12,9,1)=F_bin(12,9,2)=9. Negative C++ covers must be rerun to reproduce the upper bound.")
    (ROOT/"extended_obstruction_audit.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result))


if __name__=="__main__":main()
