"""Independent literal block assignments, pair coverage and rational tree audit."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,hashlib
from check_b3_staircase import kernel,block_assignments,rat_rref,rat_contains,permute_mask
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def literal_pool(parent,c,basis,B,C,D):
    S,T=[{q for q in range(13) if m>>q&1} for m in basis];H={0,1,2};J=set(parent['mandatory']);G=set(map(tuple,parent['required_P3_edges']))
    if c['extra_pair'] is not None:G.add(tuple(c['extra_pair']))
    target=[sum((q in X)<<(2-i) for i,X in enumerate([{3},B,C])) for q in range(13)];answer=[]
    for field,mm in zip(parent['fields'],c['field_kernel_masks']):
        source=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,[field['preA'],field['preB'],field['preC']]))) for q in range(13)]
        supplier=sum((set(field[k])==X)<<i for i,(k,X) in enumerate([('preA',B),('preB',C),('preC',D)]))
        for m in mm:
            groups=kernel(m)
            if any(len(g&T)>1 for g in groups):continue
            for U in [S,T]:
                for row in block_assignments(groups,source,target,H,J,G,S,S,U,U):
                    W={row[q] for q in T}
                    if len(W)!=9 or 3 not in W or not all(len(W&X)==1 for X in [B,C,D]) or any(set(e)<=W for e in G):continue
                    answer.append((row,supplier|((U==T)<<3)))
    assert len(answer)==len({r for r,f in answer})
    return sorted(answer),G
def replay_words(rows,S,active,required,rounds,stats):
    n=len(rows);forced_bad=False
    def digest(domain):return hashlib.sha256(domain.to_bytes((n+7)//8,'little')).hexdigest()
    def bad(word,allowed):
        assert 1<=len(word)<=11 and set(word)<=allowed
        image={q for q in range(13) if S>>q&1}
        for i in word:image={rows[i][0][q] for q in image}
        assert len(image)<9 or 3 not in image
    for ri,record in enumerate(rounds):
        assert not forced_bad
        assert record['before_size']==active.bit_count() and record['before_sha256']==digest(active)
        domains=[g&active for g in required];assert all(domains)
        premises=[[j,g.bit_length()-1] for j,g in enumerate(domains) if g.bit_count()==1]
        assert record['singleton_premises']==premises and premises
        forced={i for j,i in premises};deleted=set()
        if 'forced_bad_word' in record:
            assert record['deletions']==[] and ri==len(rounds)-1;bad(record['forced_bad_word'],forced);forced_bad=True
        for deletion in record['deletions']:
            i=deletion['letter'];assert active>>i&1 and i not in forced and i not in deleted
            bad(deletion['word'],forced|{i});deleted.add(i)
        assert [d['letter'] for d in record['deletions']]==sorted(deleted)
        for i in deleted:active&=~(1<<i)
        assert record['after_size']==active.bit_count() and record['after_sha256']==digest(active)
        stats['word_rounds']+=1
        if 'forced_bad_word' not in record:stats['word_deletions']+=len(deleted)
    return active,forced_bad

def check_tree(rows,basis0,B,C,D,G,saved):
    n=len(rows);images={};spans={};masks9=[sum(1<<q for q in S) for S in combinations(range(13),9) if 3 in S];stats=Counter()
    def mapping(m):
        if m not in images:
            ix=[q for q in range(13) if m>>q&1];answer={}
            for i,(row,flags) in enumerate(rows):
                out=set(row[q] for q in ix)
                if len(out)==9 and 3 in out:
                    mask=sum(1<<q for q in out);answer[mask]=answer.get(mask,0)|(1<<i)
            images[m]=answer
        return images[m]
    def span(basis):
        key=rat_rref(basis);assert len(key)==len(basis)
        if key not in spans:spans[key]={m for m in masks9 if rat_contains(key,m)}
        return spans[key]
    def safe(m,d):
        S={q for q in range(13) if m>>q&1}
        return (d>10 or len(S&B)==1) and (d>9 or len(S&C)==1) and (d>8 or len(S&D)==1) and (d>8 or not any(set(e)<=S for e in G))
    def visit(basis,active,required,node):
        k=len(basis)-1;assert k<11,'Depth11 is a candidate, not a rejection';stats['nodes']+=1;stats['depth_'+str(k)]+=1;current=span(basis);valid={m:g&active for m,g in mapping(basis[-1]).items() if g&active and safe(m,k+1)}
        safeletters=0
        for g in valid.values():safeletters|=g
        active&=safeletters
        if node['word_propagation']:assert k>=3 and active.bit_count()<=10000
        active,forced_bad=replay_words(rows,basis0[0],active,required,node['word_propagation'],stats)
        valid={m:g&active for m,g in valid.items() if g&active}
        assert node['basis']==basis and node['depth']==k and node['domain_size']==active.bit_count()
        assert node['domain_sha256']==hashlib.sha256(active.to_bytes((n+7)//8,'little')).hexdigest()
        sizes=[(g&active).bit_count() for g in required];assert node['required_group_sizes']==sizes
        if forced_bad:assert node['reason']=='forced_short_word';stats['forced_short_word']+=1;return
        missing=next((i for i,x in enumerate(sizes) if x==0),None)
        if missing is not None:assert node['reason']=='missing_required_group' and node['missing_group']==missing;stats['missing_required_group']+=1;return
        adjacency=[set() for _ in range(13)]
        for i,(row,flags) in enumerate(rows):
            if active>>i&1:
                for p,q in enumerate(row):adjacency[p].add(q)
        if node['reason']=='maximal_graph_not_SC':
            R=set(node['closed_set']);assert R and len(R)<13 and all(adjacency[p]<=R for p in R);stats['maximal_graph_not_SC']+=1;return
        for root in range(13):
            reached={root};work=[root]
            while work:
                p=work.pop()
                for q in adjacency[p]-reached:reached.add(q);work.append(q)
            assert len(reached)==13
        choices=sorted(m for m in valid if m not in current)
        if not choices:assert node['reason']=='no_growth';stats['no_growth']+=1;return
        assert node['reason']=='all_children_rejected' and [c['next_image'] for c in node['children']]==choices and k<11
        for m,child in zip(choices,node['children']):
            allowed=span(basis+[m]);following=0
            for out,g in valid.items():
                if out in allowed:following|=g
            visit(basis+[m],active&following,required+[valid[m]],child['node'])
        stats['internal_nodes']+=1
    required=[sum(1<<i for i,(r,f) in enumerate(rows) if f>>flag&1) for flag in range(4)];visit(basis0,(1<<n)-1,required,saved)
    return dict(stats)

def main():
    data=read('c1_word_staircase_inventory.json');scope=read('c1_word_staircase_scope.json');baseline=read('c1_word_staircase_baseline_state.json');old=read('AUXILIARY_AUDIT_20261010_22.json')
    assert sha(ROOT/'c1_word_staircase_baseline_state.json')==old['source_sha256']['active_research.json']
    for obj in [data,scope,read('b3_inverse_clique_inventory.json')]:
        for n,h in obj['source_sha256'].items():assert sha(ROOT/n)==h,n
    name='b3_mixed_c1_third2';assert data['id']==name and scope['selected_geometries']==[name]
    parent=next(z for z in read('b3_inverse_clique_inventory.json')['records'] if z['id']==name);native=read('b3_third_cover_inventory.json')['records'];z=next(z for z in native if z['id']==name);B,C,D=map(set,[z['B'],z['C'],z['D']])
    j=baseline['joint_fiber_cases'];remaining=[z for z in native if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions']];assert [z['id'] for z in remaining]==[name]
    selected=[c for c in parent['global_classes'] if c['reason']=='retained_overapproximation'];assert [c['extra_pair'] for c in data['classes']]==[c['extra_pair'] for c in selected] and len(selected)==22
    expected=[];frames_by_edge={};classes={tuple(c['extra_pair'] or []):c for c in parent['global_classes']};fieldcache=set();masks_cache={};counts=Counter();total=Counter()
    for c,sc in zip(selected,data['classes']):
        G=set(map(tuple,parent['required_P3_edges']))|({tuple(c['extra_pair'])} if c['extra_pair'] else set())
        frames=[set(X) for X in combinations(range(13),9) if 3 in X and all(len(set(X)&Y)==1 for Y in [B,C,D]) and not any(set(e)<=set(X) for e in G)]
        assert [sorted(X) for X in frames]==sc['frames'];frames_by_edge[tuple(c['extra_pair'] or [])]=frames
        for si in range(len(frames)):
            for ti in range(len(frames)):
                if si!=ti:expected.append((tuple(c['extra_pair'] or []),si,ti))
    assert len(expected)==44082 and [(tuple(t['extra_pair'] or []),*t['indices']) for t in data['transports']]==expected
    orbit={(tuple(o['extra_pair']),tuple(o['basis'])):o for o in data['orbits']};assert len(orbit)==len(data['orbits'])==317
    for transport in data['transports']:
        perm=tuple(transport['permutation']);assert set(perm)==set(range(13));edge=tuple(transport['extra_pair'] or []);ce=tuple(transport['canonical_extra']);basis=tuple(transport['basis'])
        assert tuple(sorted(perm[q] for q in edge))==ce and ce in classes
        if perm not in fieldcache:
            for X in [{0,1,2},{3},B,C,D,set(parent['mandatory'])]:assert {perm[q] for q in X}==X
            for field in parent['fields']:
                for X in field.values():assert {perm[q] for q in X}==set(X)
            fieldcache.add(perm)
        cachekey=(perm,edge,ce)
        if cachekey not in masks_cache:
            for oldm,newm in zip(classes[edge]['field_kernel_masks'],classes[ce]['field_kernel_masks']):assert sorted(permute_mask(m,perm) for m in oldm)==newm
            oldg=set(map(tuple,parent['required_P3_edges']))|({edge} if edge else set());newg=set(map(tuple,parent['required_P3_edges']))|({ce} if ce else set())
            assert {tuple(sorted((perm[u],perm[v]))) for u,v in oldg}==newg;masks_cache[cachekey]=True
        frames=frames_by_edge[edge];assert tuple(sum(1<<perm[q] for q in frames[i]) for i in transport['indices'])==basis and (ce,basis) in orbit
        counts[(ce,basis)]+=1;total['prefix_transports']+=1
    assert set(counts)==set(orbit)
    for oi,((edge,basis),o) in enumerate(orbit.items()):
        assert counts[(edge,basis)]==o['multiplicity'];rows,G=literal_pool(parent,classes[edge],basis,B,C,D)
        assert len(rows)==o['letter_count']
        assert hashlib.sha256(json.dumps([list(r) for r,f in rows],separators=(',',':')).encode()).hexdigest()==o['rows_sha256']
        assert hashlib.sha256(json.dumps([f for r,f in rows],separators=(',',':')).encode()).hexdigest()==o['flags_sha256']
        stats=check_tree(rows,list(basis),B,C,D,G,o['tree']);assert stats==o['tree_stats'];total.update(stats);total['orbits']+=1;total['literal_letters']+=len(rows)
        if (oi+1)%10==0:print('independent orbits',oi+1,'/',len(orbit),flush=True)
    assert dict(total)==data['stats'];assert data['new_excluded_third_ids']==[name]
    after=[z for z in native if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions'] and z['id']!=name];assert after==[]
    newjoints=sorted({z['joint_id'] for z in native if z['joint_id'] not in j['unrestricted_excluded_orbits'] and all(v['excluded_by_known_bound'] or v['id'] in j['unrestricted_additional_B3_third_exclusions'] or v['id']==name for v in native if v['joint_id']==z['joint_id'])});assert newjoints==['b3_mixed_c1']
    controls=read('b3_staircase_controls_audit.json');assert controls['status']=='pass'
    words=read('c1_word_controls_audit.json');assert words['status']=='pass' and (words['positive_controls'],words['adversarial_controls_rejected'])==(2,7)
    names=[Path(__file__).name,'check_b3_staircase.py','c1_word_staircase_inventory.json','c1_word_staircase_scope.json','c1_word_staircase_baseline_state.json','AUXILIARY_AUDIT_20261010_22.json','C1_WORD_STAIRCASE_EXCLUSION.md','B3_STAIRCASE_FLAG_EXCLUSION.md','b3_inverse_clique_inventory.json','b3_inverse_clique_audit.json','b3_third_cover_inventory.json','LOCAL_EQUALITY_FLAG.md','local_equality_flag_audit.json','b3_staircase_controls_audit.json','c1_word_controls_audit.json']
    result=dict(status='pass',parameter=[13,9,1],global_classes_checked=22,prefix_transports_checked=44082,canonical_prefixes=317,literal_letter_maps_checked=total['literal_letters'],flag_tree_nodes_checked=total['nodes'],tree_counts=dict(total),maximum_basis_depth=max(int(k[6:]) for k,v in total.items() if k.startswith('depth_') and v),new_excluded_third_ids=[name],new_unrestricted_joint_exclusions=newjoints,new_unrestricted_first_case_exclusions=['b3_mixed'],remaining_unrestricted_B3_geometries=0,remaining_unrestricted_third_geometries=136,remaining_unrestricted_joints=20,remaining_unrestricted_first_cases=4,source_sha256={n:sha(ROOT/n) for n in names},scope=data['scope'])
    (ROOT/'c1_word_staircase_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
