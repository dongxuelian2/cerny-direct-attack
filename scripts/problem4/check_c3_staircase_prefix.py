"""Independent quota-bounded active-vertex search and exact plane determinants."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def quota_targets(edges,out,counts):
    n=len(out);adj=[set() for _ in out]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    active=sorted((q for q in range(n) if adj[q]),key=lambda q:(-len(adj[q]),q))
    isolated=[q for q in range(n) if not adj[q]];atoms=len(counts)//3
    capacity=[out.count(a) for a in range(atoms)]
    if any(sum(counts[3*a:3*a+3])>capacity[a] for a in range(atoms)):return None
    remaining=list(counts);labels={};answer=[0]*len(counts);found=False
    iso=[sum(out[q]==a for q in isolated) for a in range(atoms)]
    usedatoms=sorted(set(out));pending=[sum(out[q]==a for q in active) for a in range(atoms)]
    def visit(i):
        nonlocal found
        if i==len(active):
            if any(sum(remaining[3*a:3*a+3])>iso[a] for a in usedatoms):return
            found=True
            for q,col in labels.items():
                if col:answer[3*out[q]+col-1]|=1<<q
            for q in isolated:
                for col in range(1,4):
                    if remaining[3*out[q]+col-1]:answer[3*out[q]+col-1]|=1<<q
            return
        q=active[i];a=out[q];pending[a]-=1
        for col in range(4):
            k=3*a+col-1
            if col and not remaining[k]:continue
            if any((col in (1,2) and labels[p] in (1,2)) or (col==2 and labels[p]>0) or (labels[p]==2 and col>0) for p in adj[q] if p in labels):continue
            if col:remaining[k]-=1
            if sum(remaining[3*a:3*a+3])<=pending[a]+iso[a]:
                labels[q]=col;visit(i+1);del labels[q]
            if col:remaining[k]+=1
        pending[a]+=1
    visit(0)
    return answer if found else None
def non_sc(arrows,n):
    for root in range(n):
        reached={root};stack=[root]
        while stack:
            p=stack.pop()
            for q in range(n):
                if q not in reached and arrows[p]>>q&1:reached.add(q);stack.append(q)
        if len(reached)<n:return reached
    return None
def exact_plane(S,T,R,frames):
    x=[int(q in T)-int(q in S) for q in range(13)]
    y=[int(q in R)-int(q in S) for q in range(13)]
    p,q=next((p,q) for p,q in combinations(range(13),2) if x[p]*y[q]!=x[q]*y[p])
    determinant=x[p]*y[q]-x[q]*y[p];answer=[]
    for i,W in enumerate(frames):
        z=[int(v in W)-int(v in S) for v in range(13)]
        aa=z[p]*y[q]-z[q]*y[p];bb=x[p]*z[q]-x[q]*z[p]
        if all(determinant*z[v]==aa*x[v]+bb*y[v] for v in range(13)):answer.append(i)
    assert 3<=len(answer)<=4
    return tuple(answer)
def partitions(edges):
    result={};pairs=list(combinations(range(13),2))
    for flags in product((0,1),repeat=len(edges)):
        selected={e for e,f in zip(edges,flags) if f};groups=[{q} for q in range(13)]
        for u,v in selected:
            merge=[g for g in groups if u in g or v in g];groups=[g for g in groups if g not in merge]+[set().union(*merge)]
        full={e for g in groups for e in combinations(sorted(g),2)}
        if full==selected:result[sum(1<<pairs.index(e) for e in selected)]=groups
    return result
def main():
    first=read('c3_staircase_first_inventory.json');second=read('c3_staircase_plane_inventory.json');scope=read('c3_staircase_scope.json')
    checkpoint=read('AUXILIARY_AUDIT_20261010_21.json');baseline=read('c3_staircase_baseline_state.json')
    assert sha(ROOT/'c3_staircase_baseline_state.json')==checkpoint['source_sha256']['active_research.json']
    for data in [scope,first,second,read('b3_inverse_clique_inventory.json')]:
        for n,h in data['source_sha256'].items():assert sha(ROOT/n)==h,n
    raw=read('b3_inverse_clique_inventory.json');native={z['id']:z for z in read('b3_third_cover_inventory.json')['records']}
    j=baseline['joint_fiber_cases'];current=[z for z in raw['records'] if not z['geometry_excluded'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions'] and native[z['id']]['joint_id'] not in j['unrestricted_excluded_orbits']];assert len(current)==5
    assert len(set(scope['selected_geometries']))==4 and set(scope['selected_geometries'])<={z['id'] for z in current}
    saved1={z['id']:z for z in first['records']};saved2={z['id']:z for z in second['records']}
    assert set(saved1)==set(saved2)==set(scope['selected_geometries'])
    stats1=Counter();stats2=Counter();quotacalls=0;closed=0
    for rec in current:
        if rec['id'] not in saved1:continue
        z=native[rec['id']];B,C,D=map(set,[z['B'],z['C'],z['D']]);H={0,1,2};J=set(rec['mandatory']);A={3};Q=set(range(13))
        fields=rec['fields'];outbase=tuple(sum((q in X)<<(2-i) for i,X in enumerate([A,B,C])) for q in range(13))
        supplies=[sum((set(f[k])==t)<<i for i,(k,t) in enumerate([('preA',B),('preB',C),('preC',D)])) for f in fields]
        selectedclasses=[c for c in rec['global_classes'] if c['reason']=='retained_overapproximation']
        assert [c['extra_pair'] for c in saved1[rec['id']]['classes']]==[c['extra_pair'] for c in selectedclasses]==[c['extra_pair'] for c in saved2[rec['id']]['classes']]
        for c,c1,c2 in zip(selectedclasses,saved1[rec['id']]['classes'],saved2[rec['id']]['classes']):
            G=set(map(tuple,rec['required_P3_edges']));immediate=set(combinations(sorted(B),2))
            if c['extra_pair'] is not None:G.add(tuple(c['extra_pair']));immediate.add(tuple(c['extra_pair']))
            frames=[set(S) for S in combinations(range(13),9) if A<=set(S) and all(len(set(S)&X)==1 for X in [B,C,D]) and not any(set(e)<=set(S) for e in G)]
            assert c1['frames']==[sorted(S) for S in frames]
            parts=partitions(sorted(immediate));catalog=[]
            for fi,(f,masks) in enumerate(zip(fields,c['field_kernel_masks'])):
                source=tuple(sum((q in X)<<(2-i) for i,X in enumerate(map(set,[f['preA'],f['preB'],f['preC']]))) for q in range(13))
                for m in masks:
                    gs=parts[m];assert all(len({source[q] for q in g})==1 and len(g-H)<=1 and (not(g&J) or len(g)==1) for g in gs)
                    catalog.append((fi,[(g,source[min(g)],2 if g&J else 1 if g-H else 3) for g in gs]))
            cache={}
            def domain(inputs,outputs):
                nonlocal quotacalls
                factor=1<<len(inputs);atoms=factor*8
                out=tuple(factor*outbase[q]+sum((q in U)<<i for i,U in enumerate(outputs)) for q in range(13))
                arrows=[0]*13;supplier=0;exists=False;allowed=0
                for fi,tagged in catalog:
                    counts=[0]*(3*atoms);tags=[]
                    for g,a,col in tagged:
                        assert all(len(g&S)<=1 for S in inputs)
                        k=3*(factor*a+sum(bool(g&S)<<i for i,S in enumerate(inputs)))+col-1;counts[k]+=1;tags.append((g,k))
                    key=(out,tuple(counts))
                    if key not in cache:cache[key]=quota_targets(G,out,counts);quotacalls+=1
                    targets=cache[key]
                    if targets is None:continue
                    exists=True;allowed+=1;supplier|=supplies[fi]
                    for g,k in tags:
                        for p in g:arrows[p]|=targets[k]
                return arrows,supplier,exists,allowed
            digest1=hashlib.sha256();domains1={};retained=[];reasons1=Counter()
            for si,S in enumerate(frames):
                for ui,U in enumerate(frames):
                    value=domain([S],[U]);domains1[(si,ui)]=value
                    digest1.update((json.dumps([si,ui,*value],separators=(',',':'))+'\n').encode())
                for ti,T in enumerate(frames):
                    if ti==si:continue
                    left,right=domains1[(si,si)],domains1[(si,ti)]
                    if not right[2]:reason='no_moving_letter'
                    elif left[1]|right[1]!=7:reason='missing_supplier'
                    elif non_sc([a|b for a,b in zip(left[0],right[0])],13) is not None:reason='maximal_graph_not_SC';closed+=1
                    else:reason='retained';retained.append([si,ti])
                    reasons1[reason]+=1
            assert retained==c1['retained_pairs'] and dict(reasons1)==c1['ST_reasons'] and digest1.hexdigest()==c1['domain_sha256'],(rec['id'],c['extra_pair'],'first')
            stats1.update(reasons1);stats1['ST_pairs']+=sum(reasons1.values());stats1['global_classes']+=1
            digest2=hashlib.sha256();reasons2=Counter();planecount=0;kept2=[]
            for si,ti in retained:
                planes=sorted({exact_plane(frames[si],frames[ti],R,frames) for ri,R in enumerate(frames) if ri not in (si,ti)})
                needed=sorted({v for p in planes for v in p});domains2={}
                for ui in (si,ti):
                    for vi in needed:domains2[(ui,vi)]=domain([frames[si],frames[ti]],[frames[ui],frames[vi]])[:3]
                for (ui,vi),value in sorted(domains2.items()):digest2.update((json.dumps([si,ti,ui,vi,*value],separators=(',',':'))+'\n').encode())
                for plane in planes:
                    arrows=[0]*13;supplier=0;moving=False;growing=False
                    for ui in (si,ti):
                        for vi in plane:
                            adj,sup,exists=domains2[(ui,vi)];supplier|=sup;moving|=exists and ui==ti;growing|=exists and vi not in (si,ti)
                            arrows=[a|b for a,b in zip(arrows,adj)]
                    if not moving:reason='no_moving_letter'
                    elif not growing:reason='no_second_dimension'
                    elif supplier!=7:reason='missing_supplier'
                    elif non_sc(arrows,13) is not None:reason='maximal_graph_not_SC';closed+=1
                    else:reason='retained';kept2.append([si,ti,list(plane)])
                    reasons2[reason]+=1;planecount+=1
            assert kept2==c2['retained']
            assert dict(reasons2)==c2['reasons'] and planecount==c2['planes'] and digest2.hexdigest()==c2['domain_sha256'],(rec['id'],c['extra_pair'],'second')
            stats2.update(reasons2);stats2['planes']+=planecount;stats2['global_classes']+=1
        assert not saved2[rec['id']]['excluded'];print(rec['id']+': pass',flush=True)
    for key,val in stats1.items():assert first['stats'][key]==val,key
    for key,val in stats2.items():assert second['stats'][key]==val,key
    assert second['excluded']==[] and stats1['global_classes']==101 and stats1['ST_pairs']==39436 and stats1['retained']==19968 and stats2['retained']==53766
    names=[Path(__file__).name,'PROOF.md#problem4-c3-staircase-exclusion','c3_staircase_scope.json','c3_staircase_baseline_state.json','AUXILIARY_AUDIT_20261010_21.json','c3_staircase_first_inventory.json','c3_staircase_plane_inventory.json','b3_inverse_clique_inventory.json','b3_inverse_clique_audit.json','b3_third_cover_inventory.json','PROOF.md#problem4-local-equality-flag','local_equality_flag_audit.json','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-second-entrance-fiber','PROOF.md#problem4-third-entrance-space']
    result=dict(status='pass',parameter=[13,9,1],selected_geometries=4,global_classes=101,ordered_first_pairs=39436,retained_first_pairs=19968,common_planes_checked=stats2['planes'],retained_planes=53766,first_reasons={k:stats1[k] for k in ['no_moving_letter','missing_supplier','maximal_graph_not_SC','retained']},second_reasons={k:stats2[k] for k in ['no_moving_letter','no_second_dimension','missing_supplier','maximal_graph_not_SC','retained']},exact_domain_digests_checked=202,distinct_quota_queries=quotacalls,closed_graphs_checked=closed,source_sha256={n:sha(ROOT/n) for n in names},scope='Complete first-image and depth-two plane domains for the four selected C3 staircase geometries. Retained domains are necessary overapproximations only.')
    (ROOT/'c3_staircase_prefix_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
