"""Retain pair-distance certificates, an odd-state obstruction and complete small cut covers."""
from itertools import combinations, permutations
from pathlib import Path
import json
from direct_attack.pu_prefix_graph import profile, strong, forward_closed
from direct_attack.native_sparse_policy import profile as native

ROOT=Path('direct_attack/data/pu_prefix')

def odd_rows(n):
    assert n>=5 and n%2
    a=[1,0]+list(range(3,n))+[2]
    b=list(range(n));b[1],b[2]=2,1
    u=list(range(n));u[0]=n-1
    return [a,b,u]

def small_cover(n):
    ps=list(permutations(range(n)));index={p:i for i,p in enumerate(ps)};identity=index[tuple(range(n))]
    nonid=[i for i in range(len(ps)) if i!=identity]
    table=[[index[tuple(b[a[q]] for q in range(n))] for b in ps] for a in ps]
    cache={}
    def group(B):
        key=tuple(B)
        if key not in cache:
            seen={identity};queue=[identity]
            for g in queue:
                for p in B:
                    h=table[g][p]
                    if h not in seen:seen.add(h);queue.append(h)
            cache[key]=seen
        return cache[key]
    redundancy=[]
    if n==4:
        for B in combinations(nonid,4):
            removable=next((p for p in B if p in group(tuple(q for q in B if q!=p))),None)
            assert removable is not None
            redundancy.append(dict(basis=list(B),removable=removable))
    cap=1 if n==2 else 3;cuts=[];basis_count=0
    for size in range(1,cap+1):
        for B in combinations(nonid,size):
            if any(p in group(tuple(q for q in B if q!=p)) for p in B):continue
            basis_count+=1;G=group(B)
            for k in range(1,n):
                S=set(range(k));safe=[]
                for s in range(n):
                    for t in range(n):
                        if s==t:continue
                        distances={(s,t):0};queue=[(s,t)]
                        for x,y in queue:
                            if distances[x,y]>=n-1:continue
                            for p in B:
                                pair=(ps[p][x],ps[p][y])
                                if pair not in distances:distances[pair]=distances[x,y]+1;queue.append(pair)
                        if not any(x not in S and y in S for x,y in distances):safe.append([s,t])
                arcs={(ps[g][s],ps[g][t]) for s,t in safe for g in G}
                assert not strong(n,arcs)
                closed=forward_closed(n,arcs)
                cuts.append(dict(basis=list(B),cut_size=k,safe_units=safe,closed_vertices=sorted(closed)))
    return dict(n=n,permutations=ps,basis_cap=cap,bases=basis_count,quadruple_redundancy=redundancy,cuts=cuts)

def main():
    ROOT.mkdir(exist_ok=True);families=[];small=[]
    for n in list(range(5,22,2))+[31,63,101]:
        rows=odd_rows(n);p=profile(rows,True);assert p['max_extension']==n+1
        S=set([0]+list(range(3,n-1,2)))
        entering=[c['distance']+1 for c in p['pairs'] if c['source'] not in S and c['target'] in S]
        assert min(entering)==n+1 and p['pair_vertices']==n*(n-1)
        p['designated_target']=sorted(S);p['designated_word']=[2]+[0]*n
        if n<=11:
            z=native(rows,True);assert z['reachable']==(1<<n)-1 and z['max_extension']==n+1
            small.append(z)
        families.append(p)
    covers=[small_cover(n) for n in range(2,5)]
    existing=json.loads(Path('direct_attack/data/permutation_units/samples.json').read_text())
    samples=[]
    for i,z in enumerate(existing):
        if z['n']<=5:
            p=profile(z['rows'],True);assert p['max_extension']==z['max_extension']
            samples.append(dict(source_index=i,certificate=p))
    for name,value in [('families',families),('small_arrays',small),('small_covers',covers),('retained_samples',samples)]:
        (ROOT/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    summary=dict(verified=True,family_states=[p['n'] for p in families],sample_certificates=len(samples),
                 small_full_arrays=len(small),covers=[dict(n=c['n'],bases=c['bases'],cuts=len(c['cuts']),
                 quadruples=len(c['quadruple_redundancy'])) for c in covers],
                 scope='All PU alphabets for n<=4 via irredundant permutation bases and all safe units; finite samples do not prove the odd family.')
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
