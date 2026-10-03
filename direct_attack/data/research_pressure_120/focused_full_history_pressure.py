"""Exploratory ALL-optimal pressure on new Hamming neighbors, with cube cuts."""
from collections import deque
from hashlib import sha256
from itertools import combinations,product
import json,time
from pathlib import Path
from direct_attack.data.research_pressure_118.all_optimal_full_history_pressure import add_basis,rational_rank,MOD

def capacity(n,d):
    partition=(1<<d)-1-max(1,2*d-n)
    return partition if n==d else max(partition,3*(1<<(d-2))-2)

def analyse(rows,deadline):
    n=len(rows[0]);assert 2<=n<=16
    # Hadamard on the augmented +/-1 matrix: every Boolean h-minor has |det|<MOD.
    assert all((h+1)**(h+1)<MOD**2*4**h for h in range(1,n+1))
    Q=(1<<n)-1;inv=[];pred=[[] for _ in range(Q+1)]
    for f in rows:
        masks=[sum(1<<q for q,t in enumerate(f) if t==x) for x in range(n)];table=[0]*(Q+1)
        for S in range(1,Q+1):b=S&-S;table[S]=table[S^b]|masks[b.bit_length()-1]
        inv.append(table)
        for S,T in enumerate(table):pred[T].append(S)
    dd={Q:0};todo=deque([Q])
    while todo:
        T=todo.popleft()
        for S in pred[T]:
            if S not in dd:dd[S]=dd[T]+1;todo.append(S)
    targets=[1<<q for q in range(n) if (1<<q) in dd]
    if not targets:return dict(sync=False)
    rt=min(dd[S] for S in targets);threshold=min(n,(rt+n-2)//(n-1))
    if threshold<2 or rt>capacity(n,threshold):return dict(sync=True,rt=rt,capacity_excluded=True)
    failed=set();nodes=cuts=0
    def dfs(S,basis,path,history):
        nonlocal nodes,cuts
        if time.monotonic()>deadline:raise TimeoutError
        nodes+=1
        if len(basis)>threshold:cuts+=1;return None
        if S==Q:
            d=rational_rank(history,n);assert d==len(basis)
            assert rt>(n-1)*(d-1)
            return dict(rows=rows,word=path[::-1],history=history,rank=d,rt=rt)
        key=(S,basis)
        if key in failed:return None
        for a,f in enumerate(inv):
            T=f[S]
            if dd.get(T)!=dd[S]-1:continue
            answer=dfs(T,add_basis(basis,T,n),path+[a],history+[T])
            if answer is not None:return answer
        failed.add(key);return None
    for S in targets:
        if dd[S]!=rt:continue
        basis=add_basis(add_basis((),Q,n),S,n);result=dfs(S,basis,[],[S])
        if result:return dict(sync=True,counter=result)
    return dict(sync=True,rt=rt,all_optimal_paths_excluded=True,threshold=threshold,nodes=nodes,cuts=cuts,memo_states=len(failed))

def main():
    start=time.monotonic();deadline=start+120;seeds=[];seed_files=[]
    for p in sorted(Path('direct_attack/data/n6_extremal').glob('*.certificate.json')):
        z=json.loads(p.read_text(encoding='utf-8'));seeds.append(z['automaton']['transitions']);seed_files.append(str(p))
    for n in range(7,13):
        a=list(range(1,n))+[0];b=list(range(n));b[-1]=0;seeds.append([a,b])
    seen={tuple(tuple(f) for f in rs) for rs in seeds};stream=sha256();counts={};counter=None;timedout=None
    for si,base in enumerate(seeds):
        n=len(base[0]);entry=counts.setdefault(str(n),dict(new_inputs=0,sync=0,capacity_excluded=0,all_path_searches=0,dfs_nodes=0,maximum_rt=0))
        cells=list(product(range(2),range(n)))
        maxdistance=2 if n==6 else 1
        for k in range(1,maxdistance+1):
            for edits in combinations(cells,k):
                for replacements in product(*[[t for t in range(n) if t!=base[a][q]] for a,q in edits]):
                    if time.monotonic()>deadline:timedout=dict(seed=si,n=n,distance=k);break
                    rows=[f[:] for f in base]
                    for (a,q),t in zip(edits,replacements):rows[a][q]=t
                    key=tuple(tuple(f) for f in rows)
                    if key in seen:continue
                    seen.add(key)
                    try:z=analyse(rows,deadline)
                    except TimeoutError:timedout=dict(seed=si,n=n,distance=k);break
                    entry['new_inputs']+=1;entry['sync']+=z['sync'];entry['capacity_excluded']+=z.get('capacity_excluded',False)
                    entry['all_path_searches']+=z.get('all_optimal_paths_excluded',False);entry['dfs_nodes']+=z.get('nodes',0)
                    entry['maximum_rt']=max(entry['maximum_rt'],z.get('rt',0))
                    stream.update(json.dumps([rows,z],separators=(',',':')).encode()+b'\n')
                    if 'counter' in z:counter=z['counter'];break
                if timedout or counter:break
            if timedout or counter:break
        print(json.dumps(dict(seed=si,n=n,cumulative=entry,seconds=time.monotonic()-start)),flush=True)
        if timedout or counter:break
    out=dict(seed_files=seed_files,planned_seed_count=len(seeds),scope='distinct non-baseline Hamming neighbors: <=2 entries at n6, one entry for C7..C12; no ALL-input or arbitrary alphabet coverage',
             counts=counts,semantic_sha256=stream.hexdigest(),counter=counter,timedout=timedout,seconds=time.monotonic()-start,
             modulus=MOD,exactness_bound='every Boolean minor through dimension16 is smaller than prime1000003 by the squared Hadamard bound; field rank and rational rank agree',
             boundary='EXPLORATORY only, not independently audited. Capacity exclusions are consequences of the separate paper lemma, not additional computational evidence. General Cerny and ALL/SOME full-history cost/rank hypotheses OPEN.')
    Path('direct_attack/native_build/focused_full_history_pressure.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(completed_new_inputs=sum(z['new_inputs'] for z in counts.values()),all_path_searches=sum(z['all_path_searches'] for z in counts.values()),timedout=timedout,counter=counter,seconds=out['seconds'])),flush=True)

if __name__=='__main__':main()
