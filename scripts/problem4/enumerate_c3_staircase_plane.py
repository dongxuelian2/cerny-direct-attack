from pathlib import Path
from itertools import combinations
from collections import Counter
import json,time,sys,hashlib
import enumerate_c3_staircase_first as first
ROOT=first.ROOT;Q=first.Q;H=first.H;A=first.A
def planekey(S,T,R):
    # A plane through three distinct cube vertices contains at most four.
    ss,tt,rr=[tuple(int(q in X) for q in range(13)) for X in [S,T,R]]
    vertices={ss,tt,rr}
    for x,y,z in [(ss,tt,rr),(ss,rr,tt),(tt,rr,ss)]:
        w=tuple(a+b-c for a,b,c in zip(x,y,z))
        if set(w)<={0,1}:vertices.add(w)
    return tuple(sorted(sum(v<<q for q,v in enumerate(row)) for row in vertices))
def main():
    start=time.time();old=first.read('b3_inverse_clique_inventory.json');native={z['id']:z for z in first.read('b3_third_cover_inventory.json')['records']}
    previous={z['id']:z for z in json.loads((ROOT/'c3_staircase_first_inventory.json').read_text())['records']}
    stats=Counter();reports=[]
    subset=set(first.read('c3_staircase_scope.json')['selected_geometries'])
    for rec in old['records']:
        if rec['geometry_excluded'] or (subset and rec['id'] not in subset):continue
        assert rec['id'] in subset
        z=native[rec['id']];B,C,D=map(set,[z['B'],z['C'],z['D']]);J=set(rec['mandatory']);fields=rec['fields']
        ins=[[sum((q in X)<<(2-i) for i,X in enumerate(map(set,[f['preA'],f['preB'],f['preC']]))) for q in range(13)] for f in fields]
        suppliers=[sum((set(f[k])==target)<<i for i,(k,target) in enumerate([('preA',B),('preB',C),('preC',D)])) for f in fields]
        out=[sum((q in X)<<(2-i) for i,X in enumerate([A,B,C])) for q in range(13)];classes=[]
        for c in rec['global_classes']:
            if c['reason']!='retained_overapproximation':continue
            pc=next(v for v in previous[rec['id']]['classes'] if v['extra_pair']==c['extra_pair']);frames=list(map(set,pc['frames']));fmasks=[sum(1<<q for q in X) for X in frames];index={m:i for i,m in enumerate(fmasks)}
            edges=set(map(tuple,rec['required_P3_edges']))
            if c['extra_pair'] is not None:edges.add(tuple(c['extra_pair']))
            patterns=first.patterns(edges,len(J));stats['patterns']+=len(patterns)
            catalogue=[]
            for fi,mm in enumerate(c['field_kernel_masks']):
                for mask in mm:
                    catalogue.append((fi,mask,[(sum(1<<q for q in g),ins[fi][min(g)],2 if g&J else 1 if g-H else 3) for g in first.blocks(mask)]))
            demand={};inputs={};planes={}
            for si,ti in pc['retained_pairs']:
                S,T=fmasks[si],fmasks[ti]
                plist=set()
                for ri,R in enumerate(frames):
                    if ri not in (si,ti):
                        p=tuple(index[v] for v in planekey(frames[si],frames[ti],R) if v in index);plist.add(tuple(sorted(p)))
                planes[(si,ti)]=sorted(plist)
                needed=set(v for p in plist for v in p)
                vals=[]
                for fi,mask,tagged in catalogue:
                    key=0;tags=[]
                    for g,atom,col in tagged:
                        tag=bool(g&S)+2*bool(g&T);k=(4*(3*atom+col-1)+tag);key+=1<<(4*k);tags.append((g,k))
                    vals.append((fi,key,tags))
                inputs[(si,ti)]=vals
                for ui in (si,ti):
                    for vi in needed:demand.setdefault((ui,vi),set()).update(key for fi,key,tags in vals)
            quotas={}
            for (ui,vi),wanted in demand.items():
                U,V=fmasks[ui],fmasks[vi];atom=[4*(3*out[q])+bool(U>>q&1)+2*bool(V>>q&1) for q in range(13)];domain={}
                for colours in patterns:
                    key=0;tags=[]
                    for q,col in enumerate(colours):
                        if col:k=atom[q]+4*(col-1);key+=1<<(4*k);tags.append((q,k))
                    stats['quota_colours']+=1
                    if key not in wanted:continue
                    union=domain.setdefault(key,{})
                    for q,k in tags:union[k]=union.get(k,0)|(1<<q)
                quotas[(ui,vi)]=domain
            reasons=Counter();retained=[];digest=hashlib.sha256()
            for (si,ti),plist in planes.items():
                domains={}
                for ui in (si,ti):
                    for vi in set(v for p in plist for v in p):
                        arrows=[0]*13;supply=0;exists=False
                        for fi,key,tags in inputs[(si,ti)]:
                            target=quotas[(ui,vi)].get(key);stats['quota_tests']+=1
                            if target is None:continue
                            exists=True;supply|=suppliers[fi]
                            for g,k in tags:
                                for p in range(13):
                                    if g>>p&1:arrows[p]|=target[k]
                        domains[(ui,vi)]=(arrows,supply,exists)
                for (ui,vi),(arrows,supply,exists) in sorted(domains.items()):digest.update((json.dumps([si,ti,ui,vi,arrows,supply,exists],separators=(',',':'))+'\n').encode())
                for plane in plist:
                    stats['planes']+=1;adj=[0]*13;supply=0;moving=False;growing=False
                    for ui in (si,ti):
                        for vi in plane:
                            arrows,sup,exists=domains[(ui,vi)];supply|=sup;moving|=exists and ui==ti;growing|=exists and vi not in (si,ti)
                            adj=[a|b for a,b in zip(adj,arrows)]
                    if not moving:reason='no_moving_letter'
                    elif not growing:reason='no_second_dimension'
                    elif supply!=7:reason='missing_supplier'
                    elif first.closure(adj) is not None:reason='maximal_graph_not_SC'
                    else:reason='retained';retained.append([si,ti,list(plane)])
                    reasons[reason]+=1
            stats.update(reasons);stats['global_classes']+=1;classes.append(dict(extra_pair=c['extra_pair'],planes=sum(len(p) for p in planes.values()),reasons=dict(reasons),retained=retained,domain_sha256=digest.hexdigest()))
            print('class',rec['id'],c['extra_pair'],dict(reasons),round(time.time()-start,2),flush=True)
        reports.append(dict(id=rec['id'],classes=classes,excluded=not any(c['retained'] for c in classes)))
        print('geometry',rec['id'],reports[-1]['excluded'],flush=True)
    result=dict(status='necessary_inventory',parameter=[13,9,1],stats=dict(stats),excluded=[z['id'] for z in reports if z['excluded']],records=reports,source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in [Path(__file__).name,'enumerate_c3_staircase_first.py','c3_staircase_first_inventory.json','c3_staircase_scope.json','PROOF.md#problem4-c3-staircase-exclusion','b3_inverse_clique_inventory.json','b3_third_cover_inventory.json']})
    (ROOT/'c3_staircase_plane_inventory.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(stats=result['stats'],excluded=result['excluded'],status=result['status'])),flush=True)
if __name__=='__main__':main()
