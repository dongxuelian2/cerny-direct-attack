from itertools import product,permutations
from direct_attack.core import canonical_map
from direct_attack.native_build.probe_paid_one_cluster_bridge import reach
from direct_attack.check_paid_one_cluster_word import distances
from direct_attack.native_build.probe_short_weak_stationarity import deviations,phase
import json,sys,time

n=int(sys.argv[1]);start=time.monotonic();maps=list(product(range(n),repeat=n));perms=list(permutations(range(n)))
reps=[f for f in maps if canonical_map(f,perms)==f];tested=sync=0;unknown=0
for a in reps:
    for b in maps:
        if a==b:continue
        tested+=1
        if any(len(reach(q,[a,b]))<n for q in range(n)):continue
        d=distances([a,b])
        if d[-1] is None:continue
        sync+=1;ds=deviations([a,b],n);z=phase(ds)
        if 'unknown' in z:unknown+=1
        if 'separator' in z:
            print(json.dumps(dict(rows=[a,b],n=n,cap=n,rt=d[-1],separator=z,vectors=len(ds),tested=tested,sync=sync,unknown=unknown,seconds=time.monotonic()-start,
                boundary='EXPLORATORY discovery. Exact integer strict separator retained, but ALL literal words need independent verification. Refutes only universal max-support-cost n for weak full-Q stationarity with singular positive mass.')),flush=True)
            raise SystemExit
print(json.dumps(dict(n=n,completed=True,tested=tested,sync=sync,unknown=unknown,seconds=time.monotonic()-start,boundary='EXPLORATORY float phaseI feasible controls; not independent exact positive mixture verification or all-n proof.')),flush=True)
