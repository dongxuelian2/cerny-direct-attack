from pathlib import Path
from itertools import combinations
from collections import Counter
import json,time,hashlib
ROOT=Path(__file__).resolve().parent
Q=set(range(13)); H={0,1,2}; A={3}
PAIRS=list(combinations(range(13),2))
def read(n):return json.loads((ROOT/n).read_text())
def blocks(mask):
    gs=[{q} for q in Q]
    for i,(u,v) in enumerate(PAIRS):
        if mask>>i&1:
            merge=[g for g in gs if u in g or v in g]
            gs=[g for g in gs if g not in merge]+[set().union(*merge)]
    return gs
def patterns(edges,Jsize):
    adj=[set() for _ in Q]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    answer=[]
    for items in combinations(range(13),10):
        I=set(items)
        if any(adj[q]&I for q in I):continue
        rest=sorted(Q-I)
        for size in range(4):
            for extra in combinations(rest,size):
                T=set(extra);avail=I|T
                isolated=[q for q in sorted(I) if not(adj[q]&avail)]
                for pp in combinations(isolated,Jsize):
                    L=set(pp);answer.append(tuple(2 if q in L else 1 if q in I else 3 if q in T else 0 for q in range(13)))
    return answer
def closure(arrows):
    for root in range(13):
        seen=1<<root
        while True:
            new=seen
            for p in range(13):
                if seen>>p&1:new|=arrows[p]
            if new==seen:break
            seen=new
        if seen!=8191:return seen
    return None
def main():
    start=time.time(); scope=read('b3_staircase_scope.json'); old=read('b3_inverse_clique_inventory.json'); native={z['id']:z for z in read('b3_third_cover_inventory.json')['records']}
    stats=Counter(); results=[]
    for rec in old['records']:
        if rec['geometry_excluded'] or rec['id'] not in scope['selected_geometries']:continue
        z=native[rec['id']];B,C,D=map(set,[z['B'],z['C'],z['D']]);J=set(rec['mandatory'])
        fields=rec['fields']; ins=[[sum((q in X)<<(2-i) for i,X in enumerate(map(set,[f['preA'],f['preB'],f['preC']]))) for q in range(13)] for f in fields]
        supplier=[sum((set(f[k])==target)<<i for i,(k,target) in enumerate([('preA',B),('preB',C),('preC',D)])) for f in fields]
        out=[sum((q in X)<<(2-i) for i,X in enumerate([A,B,C])) for q in range(13)]
        report=[]
        for c in rec['global_classes']:
            if c['reason']!='retained_overapproximation':continue
            edges=set(map(tuple,rec['required_P3_edges']))
            if c['extra_pair'] is not None:edges.add(tuple(c['extra_pair']))
            frames=[set(S) for S in combinations(range(13),9) if 3 in S and all(len(set(S)&X)==1 for X in [B,C,D]) and not any(set(e)<=set(S) for e in edges)]
            pats=patterns(edges,len(J));stats['patterns']+=len(pats)
            catalogue=[]
            for i,mm in enumerate(c['field_kernel_masks']):
                for mask in mm:
                    gs=blocks(mask)
                    catalogue.append((i,mask,[(g,ins[i][min(g)],2 if g&J else 1 if g-H else 3) for g in gs]))
            quotas=[]
            for U in frames:
                atoms=[2*out[q]+(q in U) for q in range(13)];domain={}
                for colours in pats:
                    cnt=[0]*48;targets=[0]*48
                    for q,col in enumerate(colours):
                        if col:k=3*atoms[q]+col-1;cnt[k]+=1;targets[k]|=1<<q
                    union=domain.setdefault(tuple(cnt),[0]*48)
                    for k,v in enumerate(targets):union[k]|=v
                quotas.append(domain)
            retained=[];pairreasons=Counter();digest=hashlib.sha256()
            for si,S in enumerate(frames):
                domains=[]
                for ui,U in enumerate(frames):
                    adj=[0]*13;supply=0;exists=False;allowed=0
                    for i,mask,tagged in catalogue:
                        if any(len(g&S)>1 for g,atom,col in tagged):continue
                        cnt=[0]*48;tagged2=[]
                        for g,atom,col in tagged:
                            key=3*(2*atom+bool(g&S))+col-1;cnt[key]+=1;tagged2.append((g,key))
                        targets=quotas[ui].get(tuple(cnt));stats['quota_tests']+=1
                        if targets is None:continue
                        exists=True;allowed+=1;supply|=supplier[i]
                        for g,key in tagged2:
                            for p in g:adj[p]|=targets[key]
                    domains.append((adj,supply,exists,allowed));digest.update((json.dumps([si,ui,adj,supply,exists,allowed],separators=(',',':'))+'\n').encode())
                for ti,T in enumerate(frames):
                    if ti==si:continue
                    stats['ST_pairs']+=1
                    if not domains[ti][2]:reason='no_moving_letter'
                    elif domains[si][1]|domains[ti][1]!=7:reason='missing_supplier'
                    else:
                        adj=[a|b for a,b in zip(domains[si][0],domains[ti][0])]
                        closed=closure(adj)
                        if closed is not None:reason='maximal_graph_not_SC'
                        else:
                            reason='retained';retained.append([si,ti])
                    pairreasons[reason]+=1
            stats.update(pairreasons);stats['global_classes']+=1
            report.append(dict(extra_pair=c['extra_pair'],frames=[sorted(S) for S in frames],ST_reasons=dict(pairreasons),retained_pairs=retained,domain_sha256=digest.hexdigest()))
        results.append(dict(id=rec['id'],classes=report,excluded=not any(c['retained_pairs'] for c in report)))
        print(rec['id'],len(report),sum(len(c['retained_pairs']) for c in report),round(time.time()-start,2),flush=True)
    result=dict(status='necessary_inventory',parameter=[13,9,1],stats=dict(stats),excluded=[z['id'] for z in results if z['excluded']],records=results,source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in [Path(__file__).name,'b3_staircase_scope.json','B3_STAIRCASE_FLAG_EXCLUSION.md','b3_inverse_clique_inventory.json','b3_third_cover_inventory.json']})
    (ROOT/'b3_staircase_first_inventory.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(stats=result['stats'],excluded=result['excluded'],status=result['status'])),flush=True)
if __name__=='__main__':main()
