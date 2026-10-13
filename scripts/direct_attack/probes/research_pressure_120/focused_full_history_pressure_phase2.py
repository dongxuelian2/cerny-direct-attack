"""Exact distance-two C7..C12 neighbors; disjoint from the first run."""
from hashlib import sha256
from itertools import combinations,product
import json,time
from pathlib import Path
from direct_attack.probes.research_pressure_120.focused_full_history_pressure import analyse,MOD

start=time.monotonic();deadline=start+180;counts={};stream=sha256();counter=None;timedout=None
for n in range(7,13):
    base=[list(range(1,n))+[0],list(range(n))];base[1][-1]=0
    entry=dict(planned_inputs=n*(2*n-1)*(n-1)**2,new_inputs=0,sync=0,capacity_excluded=0,all_path_searches=0,dfs_nodes=0,maximum_rt=0)
    counts[str(n)]=entry
    for edits in combinations(list(product(range(2),range(n))),2):
        for replacements in product(*[[t for t in range(n) if t!=base[a][q]] for a,q in edits]):
            if time.monotonic()>deadline:timedout=dict(n=n,edits=edits,replacements=replacements);break
            rows=[f[:] for f in base]
            for (a,q),t in zip(edits,replacements):rows[a][q]=t
            try:z=analyse(rows,deadline)
            except TimeoutError:timedout=dict(n=n,edits=edits,replacements=replacements);break
            entry['new_inputs']+=1;entry['sync']+=z['sync'];entry['capacity_excluded']+=z.get('capacity_excluded',False)
            entry['all_path_searches']+=z.get('all_optimal_paths_excluded',False);entry['dfs_nodes']+=z.get('nodes',0)
            entry['maximum_rt']=max(entry['maximum_rt'],z.get('rt',0));stream.update(json.dumps([rows,z],separators=(',',':')).encode()+b'\n')
            if 'counter' in z:counter=z['counter'];break
        if counter or timedout:break
    print(json.dumps(dict(n=n,cumulative=entry,seconds=time.monotonic()-start)),flush=True)
    if counter or timedout:break
    assert entry['new_inputs']==entry['planned_inputs']
out=dict(scope='ALL exact distance-two labeled transition-table neighbors of C7..C12; disjoint from phase1 within these n. No ALL-automata coverage.',
         counts=counts,semantic_sha256=stream.hexdigest(),counter=counter,timedout=timedout,seconds=time.monotonic()-start,modulus=MOD,
         boundary='EXPLORATORY only; not independently audited. ALL-shortest-path search and certified small-Boolean-matrix field rank, with capacity cuts, do not prove a universal cost/rank theorem. Cerny OPEN.')
Path('scripts/direct_attack/native_build/focused_full_history_pressure_phase2.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(completed_new_inputs=sum(z['new_inputs'] for z in counts.values()),all_path_searches=sum(z['all_path_searches'] for z in counts.values()),counter=counter,timedout=timedout,seconds=out['seconds'])),flush=True)
