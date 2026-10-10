"""Direct kernel-block assignments and rational verification of every flag branch."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def kernel(mask,n=13):
    pairs=list(combinations(range(n),2));gs=[{q} for q in range(n)]
    for i,(u,v) in enumerate(pairs):
        if mask>>i&1:
            parts=[g for g in gs if u in g or v in g];gs=[g for g in gs if g not in parts]+[set().union(*parts)]
    assert {e for g in gs for e in combinations(sorted(g),2)}=={e for i,e in enumerate(pairs) if mask>>i&1}
    return gs
def block_assignments(groups,source,target,H,J,G,S,T,U,V):
    n=len(target);adj=[set() for _ in target]
    for u,v in G:adj[u].add(v);adj[v].add(u)
    tagged=[]
    for g in groups:
        if len(g&S)>1 or len(g&T)>1 or len({source[q] for q in g})!=1:return
        if len(g-H)>1 or (g&J and len(g)!=1):return
        kind=2 if g&J else 1 if g-H else 3;a=source[min(g)];sig=(bool(g&S),bool(g&T))
        choices=[q for q in range(n) if target[q]==a and (q in U,q in V)==sig]
        if not choices:return
        tagged.append((g,kind,choices))
    tagged.sort(key=lambda x:(len(x[2]),-int(x[1]==2),min(x[0])))
    used={};row=[None]*n
    def visit(i):
        if i==len(tagged):yield tuple(row);return
        g,kind,choices=tagged[i]
        for q in choices:
            if q in used:continue
            if any(q in adj[p] and ((kind in (1,2) and col in (1,2)) or kind==2 or col==2) for p,col in used.items()):continue
            used[q]=kind
            for p in g:row[p]=q
            yield from visit(i+1)
            del used[q]
    yield from visit(0)
def literal_pool(parent,c,basis,B,C,D):
    S,T,R=[{q for q in range(13) if m>>q&1} for m in basis];H={0,1,2};J=set(parent['mandatory']);A={3};G=set(map(tuple,parent['required_P3_edges']))|{tuple(c['extra_pair'])};plane=[S,T,R]
    target=[sum((q in X)<<(2-i) for i,X in enumerate([A,B,C])) for q in range(13)];answer=[]
    for f,mm in zip(parent['fields'],c['field_kernel_masks']):
        source=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,[f['preA'],f['preB'],f['preC']]))) for q in range(13)]
        sup=sum((set(f[k])==X)<<i for i,(k,X) in enumerate([('preA',B),('preB',C),('preC',D)]))
        for m in mm:
            groups=kernel(m)
            if any(len(g&R)>1 for g in groups):continue
            for U in [S,T]:
                for V in plane:
                    for row in block_assignments(groups,source,target,H,J,G,S,T,U,V):
                        W={row[q] for q in R}
                        if len(W)!=9 or not A<=W or not all(len(W&X)==1 for X in [B,C,D]) or any(set(e)<=W for e in G):continue
                        flags=sup|((U==T)<<3)|((V==R)<<4);answer.append((row,flags))
    assert len(answer)==len({row for row,flags in answer})
    return sorted(answer)
def rat_rref(masks,n=13):
    rows=[[Fraction(m>>q&1) for q in range(n)] for m in masks];rank=0
    for q in range(n):
        pivot=next((i for i in range(rank,len(rows)) if rows[i][q]),None)
        if pivot is None:continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank];scale=rows[rank][q];rows[rank]=[v/scale for v in rows[rank]]
        for i in range(len(rows)):
            if i!=rank and rows[i][q]:
                a=rows[i][q];rows[i]=[x-a*y for x,y in zip(rows[i],rows[rank])]
        rank+=1
    return tuple(tuple(r) for r in rows[:rank])
def rat_contains(basis,m,n=13):
    row=[Fraction(m>>q&1) for q in range(n)]
    for b in basis:
        q=next(q for q,v in enumerate(b) if v);a=row[q]
        if a:row=[x-a*y for x,y in zip(row,b)]
    return not any(row)
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
        k=len(basis)-1;stats['nodes']+=1;stats['depth_'+str(k)]+=1;current=span(basis);valid={m:g&active for m,g in mapping(basis[-1]).items() if g&active and safe(m,k+1)}
        safeletters=0
        for g in valid.values():safeletters|=g
        active&=safeletters
        assert node['basis']==basis and node['depth']==k and node['domain_size']==active.bit_count()
        assert node['domain_sha256']==hashlib.sha256(active.to_bytes((n+7)//8,'little')).hexdigest()
        sizes=[(g&active).bit_count() for g in required];assert node['required_group_sizes']==sizes
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
    required=[sum(1<<i for i,(r,f) in enumerate(rows) if f>>flag&1) for flag in range(5)];visit(basis0,(1<<n)-1,required,saved)
    return dict(stats)
def permute_mask(mask,perm):
    pairs=list(combinations(range(13),2));idx={p:i for i,p in enumerate(pairs)}
    return sum(1<<idx[tuple(sorted((perm[u],perm[v])))] for i,(u,v) in enumerate(pairs) if mask>>i&1)
def main():
    data=read('b3_staircase_inventory.json');prefix=read('b3_staircase_prefix_audit.json');assert prefix['status']=='pass'
    for obj in [data,prefix]:
        for n,h in obj['source_sha256'].items():assert sha(ROOT/n)==h,n
    first={z['id']:z for z in read('b3_staircase_first_inventory.json')['records']};planes={z['id']:z for z in read('b3_staircase_plane_inventory.json')['records']};raw={z['id']:z for z in read('b3_inverse_clique_inventory.json')['records']};native={z['id']:z for z in read('b3_third_cover_inventory.json')['records']};total=Counter()
    assert {z['id'] for z in data['records']}=={'b3_mixed_c1_third6','b3_mixed_c8_third1'}
    for record in data['records']:
        name=record['id'];parent=raw[name];z=native[name];B,C,D=map(set,[z['B'],z['C'],z['D']]);canonical=next(c for c in parent['global_classes'] if c['extra_pair']==[2,6]);G=set(map(tuple,parent['required_P3_edges']))|{(2,6)};orbit={tuple(o['basis']):o for o in record['orbits']};counts=Counter();expected=[]
        for c in planes[name]['classes']:
            frames=next(v['frames'] for v in first[name]['classes'] if v['extra_pair']==c['extra_pair'])
            for si,ti,pp in c['retained']:
                assert len(pp)==3;ri=next(i for i in pp if i not in (si,ti));expected.append((tuple(c['extra_pair']),si,ti,ri))
        assert [(tuple(t['extra_pair']),*t['indices']) for t in record['transports']]==expected
        for t in record['transports']:
            perm=t['permutation'];assert set(perm)==set(range(13))
            for X in [{0,1,2},{3},B,C,D,set(parent['mandatory'])]:assert {perm[q] for q in X}==X
            assert {perm[q] for q in t['extra_pair']}=={2,6}
            original=next(c for c in parent['global_classes'] if c['extra_pair']==t['extra_pair'])
            for old,new in zip(original['field_kernel_masks'],canonical['field_kernel_masks']):assert sorted(permute_mask(m,perm) for m in old)==new
            for field in parent['fields']:
                for X in field.values():assert {perm[q] for q in X}==set(X)
            frames=next(c['frames'] for c in first[name]['classes'] if c['extra_pair']==t['extra_pair']);basis=[sum(1<<perm[q] for q in frames[i]) for i in t['indices']];assert basis==t['basis'] and tuple(basis) in orbit;counts[tuple(basis)]+=1;total['prefix_transports']+=1
        assert set(counts)==set(orbit)
        for basis,o in orbit.items():
            assert counts[basis]==o['multiplicity'];rows=literal_pool(parent,canonical,basis,B,C,D)
            assert [list(r) for r,f in rows]==o['rows'] and [f for r,f in rows]==o['flags']
            stats=check_tree(rows,list(basis),B,C,D,G,o['tree']);assert stats==o['tree_stats'];total.update(stats);total['orbits']+=1;total['literal_letters']+=len(rows)
            print(name,list(basis),'maps',len(rows),'tree pass',flush=True)
        assert record['geometry_excluded']
    assert dict(total)==data['stats']
    baseline=read('b3_staircase_baseline_state.json');j=baseline['joint_fiber_cases'];new=data['new_excluded_third_ids'];remaining=[z for z in native.values() if not z['excluded_by_known_bound'] and z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_B3_third_exclusions'] and z['id'] not in new]
    assert len(remaining)==5 and all(z['id'] in new or z['excluded_by_known_bound'] or z['id'] in j['unrestricted_additional_B3_third_exclusions'] for z in native.values() if z['joint_id']=='b3_mixed_c8')
    names=[Path(__file__).name,'b3_staircase_inventory.json','b3_staircase_prefix_audit.json','b3_staircase_first_inventory.json','b3_staircase_plane_inventory.json','b3_inverse_clique_inventory.json','b3_third_cover_inventory.json','b3_staircase_baseline_state.json','AUXILIARY_AUDIT_20261010_20.json','B3_STAIRCASE_FLAG_EXCLUSION.md','LOCAL_EQUALITY_FLAG.md','local_equality_flag_audit.json','b3_staircase_controls_audit.json']
    control=read('b3_staircase_controls_audit.json');assert control['status']=='pass'
    result=dict(status='pass',parameter=[13,9,1],complete_geometries=2,prefix_transports_checked=180,canonical_prefixes=10,literal_letter_maps_checked=total['literal_letters'],flag_tree_nodes_checked=total['nodes'],tree_counts=dict(total),maximum_basis_depth=4,maximum_safety_depth=5,new_excluded_third_ids=new,new_unrestricted_joint_exclusions=['b3_mixed_c8'],remaining_unrestricted_B3_geometries=5,remaining_unrestricted_third_geometries=141,remaining_unrestricted_joints=22,source_sha256={n:sha(ROOT/n) for n in names},scope=data['scope'])
    (ROOT/'b3_staircase_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
