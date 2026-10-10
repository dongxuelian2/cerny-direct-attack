"""Literal full output-image sets, independent of active-core colour generation."""
from pathlib import Path
from itertools import combinations,product
import json,hashlib
ROOT=Path(__file__).resolve().parent;Q=set(range(13));H={0,1,2};A={3};PAIRS=list(combinations(range(13),2));BITS={p:1<<i for i,p in enumerate(PAIRS)}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def literal_quotas(edges,out,Jsize):
    adj=[set() for q in range(13)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    answer={};count=0
    for items in combinations(range(13),10):
        I=set(items)
        if any(adj[q]&I for q in I):continue
        rest=sorted(Q-I)
        for size in range(4):
            for extra in combinations(rest,size):
                T=set(extra);available=I|T;isolated=[q for q in sorted(I) if not(adj[q]&available)]
                for protected in combinations(isolated,Jsize):
                    L=set(protected);counts=[0]*24;targets=[0]*24
                    for tagged,colour in [(I-L,1),(L,2),(T,3)]:
                        for q in tagged:counts[3*out[q]+colour-1]+=1;targets[3*out[q]+colour-1]|=1<<q
                    union=answer.setdefault(tuple(counts),[0]*24)
                    for k,v in enumerate(targets):union[k]|=v
                    count+=1
    return answer,count
def kernel_blocks(edges):
    allclasses=[]
    for flags in product((0,1),repeat=len(edges)):
        chosen={e for e,flag in zip(edges,flags) if flag};blocks=[{q} for q in Q]
        for u,v in chosen:
            merge=[g for g in blocks if u in g or v in g];blocks=[g for g in blocks if g not in merge]+[set().union(*merge)]
        full={e for g in blocks for e in combinations(sorted(g),2)}
        if chosen==full:allclasses.append((sum(BITS[e] for e in chosen),blocks))
    return allclasses
def main():
    data=read('b3_inverse_clique_inventory.json');baseline=read('b3_inverse_clique_baseline_state.json');old=read('AUXILIARY_AUDIT_20261010_18.json')
    assert sha(ROOT/'b3_inverse_clique_baseline_state.json')==old['source_sha256']['active_research.json']
    reports=['inverse_clique_letter_controls_audit.json','three_cover_atom_kernel_audit.json','b3_third_cover_audit.json','mandatory_core_isolation_audit.json']
    for z in [data]+[read(n) for n in reports]:
        if z is not data:assert z['status']=='pass'
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,n
    allinv=read('b3_third_cover_inventory.json')['records'];j=baseline['joint_fiber_cases']
    inv=[z for z in allinv if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']]
    saved={z['id']:z for z in data['records']};native={z['id']:z for z in read('three_cover_atom_kernel_inventory.json')['records']}
    assert len(inv)==len(saved)==63;classes=missing=closedcount=kept=lettercases=outputsets=transports=closed_transports=0;excluded=[]
    frames=[set(S) for S in combinations(range(13),9) if 3 in S]
    covered=[set(R) for size in range(1,5) for R in combinations(sorted(Q-A),size) if len(set(R)-H)<=1]
    for z in inv:
        s=saved[z['id']];ns=native[z['id']];assert s['fields']==[{k:f[k] for k in ['preA','preB','preC']} for f in ns['fields']]
        J=set(s['mandatory']);assert J==set(ns['mandatory']) and not(J&H)
        B,C,D=map(set,[z['B'],z['C'],z['D']]);triangle=set(combinations(sorted(B),2));required=triangle|set(combinations(sorted(C),2))|set(combinations(sorted(D),2))
        assert s['required_P3_edges']==[list(e) for e in sorted(required)]
        cells=[{q for q in Q-A if tuple(int(q in X) for X in [H,B,C])==sig} for sig in product((0,1),repeat=3)]
        labels=[R for R in covered if [len(R&cell) for cell in cells]==z['cell_signature']]
        assert len(labels)==z['labelled_D']==z['orbit_size']
        for R in labels:
            perm={3:3}
            for cell in cells:
                source=sorted(cell&D)+sorted(cell-D);target=sorted(cell&R)+sorted(cell-R)
                perm.update(zip(source,target))
            assert set(perm)==set(perm.values())==Q
            assert all({perm[q] for q in X}==X for X in [H,A,B,C]) and {perm[q] for q in D}==R
            feasible=[S for S in frames if all(len(S&X)==1 for X in [B,C,R])]
            assert len(feasible)==z['feasible_nine_sets'] and set.intersection(*feasible)=={perm[q] for q in J}
            for c in s['global_classes']:
                if c['reason']!='maximal_graph_not_SC':continue
                closed={perm[q] for q in c['closed_set']}
                arrows={perm[p]:{perm[q] for q in row} for p,row in enumerate(c['maximal_arrows'])}
                assert all(arrows[p]<=closed for p in closed);closed_transports+=1
            transports+=1
        extra=[None]+[list(e) for e in PAIRS if e not in triangle and set(e)&H and not(set(e)&J)]
        assert [c['extra_pair'] for c in s['global_classes']]==extra
        out=[sum((q in X)<<(2-i) for i,X in enumerate([A,B,C])) for q in range(13)];cache={};retained=False
        for c in s['global_classes']:
            globaledges=triangle|({tuple(c['extra_pair'])} if c['extra_pair'] is not None else set());G=required|globaledges;key=tuple(sorted(G))
            if key not in cache:
                cache[key],total=literal_quotas(G,out,len(J));outputsets+=total
            quotas=cache[key];catalog=kernel_blocks(sorted(globaledges));allowed=[];arrows=[0]*13
            for f,previous in zip(s['fields'],ns['fields']):
                source=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,[f['preA'],f['preB'],f['preC']]))) for q in range(13)]
                valid=[];atomcompatible=[]
                for mask,blocks in catalog:
                    counts=[0]*24;tagged=[]
                    if any(len({source[q] for q in group})!=1 for group in blocks):continue
                    for group in blocks:
                        colour=2 if group&J else 1 if group-H else 3;k=3*source[min(group)]+colour-1
                        counts[k]+=1;tagged.append((group,k))
                    if all(sum(counts[3*k:3*k+3])<=out.count(k) for k in range(8)):atomcompatible.append(mask)
                    targets=quotas.get(tuple(counts));lettercases+=1
                    if targets is None:continue
                    valid.append(mask)
                    for group,k in tagged:
                        for q in group:arrows[q]|=targets[k]
                assert set(atomcompatible)=={m for m in previous['compatible_kernel_masks'] if not m&~sum(BITS[e] for e in globaledges)}
                allowed.append(sorted(valid))
            assert allowed==c['field_kernel_masks'],(z['id'],c['extra_pair'])
            assert [sorted(q for q in Q if mask>>q&1) for mask in arrows]==c['maximal_arrows']
            good=[i for i,a in enumerate(allowed) if a]
            suppliers=[any(set(s['fields'][i][key])==target for i in good) for key,target in [('preA',B),('preB',C),('preC',D)]]
            assert suppliers==c['suppliers'];classes+=1
            if not all(suppliers):assert c['reason']=='missing_supplier' and c['closed_set'] is None;missing+=1;continue
            if c['reason']=='maximal_graph_not_SC':
                R=set(c['closed_set']);assert R and R!=Q and all(not (mask&~sum(1<<q for q in R)) for p,mask in enumerate(arrows) if p in R)
                closedcount+=1;continue
            assert c['reason']=='retained_overapproximation' and c['closed_set'] is None
            for root in Q:
                R={root};work=[root]
                while work:
                    p=work.pop()
                    for q in Q-R:
                        if arrows[p]>>q&1:R.add(q);work.append(q)
                assert R==Q
            retained=True;kept+=1
        assert s['geometry_excluded']==(not retained)
        if not retained:excluded.append(z['id'])
    assert (classes,missing,closedcount,kept,len(excluded))==(1713,1378,137,198,28)
    remaining=[z for z in inv if z['id'] not in excluded];assert len(remaining)==35
    newjoints=sorted(({z['joint_id'] for z in inv})-{z['joint_id'] for z in remaining})
    assert newjoints==['b3_mixed_c10','b3_mixed_c11','b3_mixed_c6']
    assert all(v['id'] in excluded or v['excluded_by_known_bound'] or v['id'] in j['unrestricted_additional_B3_third_exclusions'] for v in allinv if v['joint_id'] in newjoints)
    names=[Path(__file__).name,'B3_INVERSE_CLIQUE_MAXIMAL_GRAPH.md','b3_inverse_clique_inventory.json',
        'b3_inverse_clique_baseline_state.json','AUXILIARY_AUDIT_20261010_18.json','three_cover_atom_kernel_inventory.json',
        'b3_third_cover_inventory.json',*reports]
    result=dict(status='pass',parameter=[13,9,1],current_geometries=63,global_classes_checked=classes,
        classes_missing_supplier=missing,classes_maximal_graph_not_SC=closedcount,retained_global_classes=kept,
        literal_full_output_set_colourings=outputsets,field_kernel_quota_tests=lettercases,new_excluded_third_ids=excluded,
        labelled_D_transports_checked=transports,closed_set_transports_checked=closed_transports,
        new_unrestricted_joint_exclusions=newjoints,remaining_unrestricted_B3_geometries=35,
        remaining_unrestricted_third_geometries=171,remaining_unrestricted_joints=27,
        source_sha256={n:sha(ROOT/n) for n in names},scope=data['scope'])
    (ROOT/'b3_inverse_clique_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
