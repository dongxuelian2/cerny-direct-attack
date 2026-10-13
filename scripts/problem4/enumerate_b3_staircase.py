"""Complete prefix transports, literal letter pools, and modular equality-flag trees."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,hashlib
import b3_staircase_letter_generator as lg
ROOT=Path(__file__).resolve().parent;P=1000000007
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rref(masks):
    rows=[[int(m>>q&1) for q in range(13)] for m in masks];rank=0
    for q in range(13):
        pivot=next((i for i in range(rank,len(rows)) if rows[i][q]),None)
        if pivot is None:continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank];inv=pow(rows[rank][q],P-2,P);rows[rank]=[v*inv%P for v in rows[rank]]
        for i in range(len(rows)):
            if i!=rank and rows[i][q]:
                a=rows[i][q];rows[i]=[(x-a*y)%P for x,y in zip(rows[i],rows[rank])]
        rank+=1
    return tuple(tuple(r) for r in rows[:rank])
def contains(basis,m):
    row=[int(m>>q&1) for q in range(13)]
    for b in basis:
        q=next(q for q,v in enumerate(b) if v);a=row[q]
        if a:row=[(x-a*y)%P for x,y in zip(row,b)]
    return not any(row)
def canonical(name,basis,extra,controls):
    normalize=list(range(13));outside=next(q for q in extra if q not in {0,1,2})
    if name=='b3_mixed_c8_third1':normalize[outside],normalize[6]=6,outside
    transformed=[{normalize[q] for q in S} for S in basis];edge={normalize[q] for q in extra};cells={}
    for q in range(13):cells.setdefault(tuple(q in X for X in controls)+(q in edge,),[]).append(q)
    order={}
    for cell in cells.values():order.update(zip(sorted(cell,key=lambda q:(tuple(q in S for S in transformed),q)),sorted(cell)))
    perm=[order[normalize[q]] for q in range(13)]
    masks=[sum(1<<perm[q] for q in S) for S in basis]
    return masks,perm
def tree(rows,basis0,B,C,D,G):
    n=len(rows);allletters=(1<<n)-1;inputs={};spans={};stats=Counter()
    masks9=[sum(1<<q for q in S) for S in combinations(range(13),9) if 3 in S];sets={m:{q for q in range(13) if m>>q&1} for m in masks9}
    groups=[sum(1<<i for i,(r,f) in enumerate(rows) if f>>flag&1) for flag in range(5)]
    edges=[[sum(1<<i for i,(r,f) in enumerate(rows) if r[p]==q) for q in range(13)] for p in range(13)]
    def images(m):
        if m not in inputs:
            incoming=[q for q in range(13) if m>>q&1];answer={}
            for i,(r,f) in enumerate(rows):
                out=0
                for q in incoming:out|=1<<r[q]
                if out.bit_count()==9 and out>>3&1:answer[out]=answer.get(out,0)|(1<<i)
            inputs[m]=answer
        return inputs[m]
    def span(basis):
        key=rref(basis)
        if key not in spans:spans[key]=frozenset(m for m in masks9 if contains(key,m))
        return key,spans[key]
    def safe(m,d):
        S=sets[m]
        return (d>10 or len(S&B)==1) and (d>9 or len(S&C)==1) and (d>8 or len(S&D)==1) and (d>8 or not any(set(e)<=S for e in G))
    def visit(basis,active,required):
        k=len(basis)-1;rank,current=span(basis);assert len(rank)==len(basis)
        stats['nodes']+=1;stats['depth_'+str(k)]+=1
        mapping=images(basis[-1]);valid={m:g&active for m,g in mapping.items() if g&active and safe(m,k+1)};safeletters=0
        for g in valid.values():safeletters|=g
        active&=safeletters
        node=dict(basis=basis,depth=k,domain_size=active.bit_count(),domain_sha256=hashlib.sha256(active.to_bytes((n+7)//8,'little')).hexdigest(),required_group_sizes=[(active&g).bit_count() for g in required])
        missing=next((i for i,g in enumerate(required) if not(g&active)),None)
        if missing is not None:node.update(reason='missing_required_group',missing_group=missing);stats['missing_required_group']+=1;return node
        adj=[sum(1<<q for q in range(13) if edges[p][q]&active) for p in range(13)];closed=lg.first.closure(adj)
        if closed is not None:node.update(reason='maximal_graph_not_SC',closed_set=[q for q in range(13) if closed>>q&1]);stats['maximal_graph_not_SC']+=1;return node
        assert k<11,'A surviving complete flag is not an exclusion'
        choices=sorted((m,g) for m,g in valid.items() if m not in current)
        if not choices:node.update(reason='no_growth');stats['no_growth']+=1;return node
        children=[]
        for m,group in choices:
            _,allowed=span(basis+[m]);following=0
            for out,g in valid.items():
                if out in allowed:following|=g
            children.append(dict(next_image=m,node=visit(basis+[m],active&following,required+[group])))
        node.update(reason='all_children_rejected',children=children);stats['internal_nodes']+=1;return node
    result=visit(basis0,allletters,groups)
    return result,dict(stats)
def main():
    baseline=read('b3_staircase_baseline_state.json');checkpoint=read('AUXILIARY_AUDIT_20261010_20.json');assert sha(ROOT/'b3_staircase_baseline_state.json')==checkpoint['source_sha256']['active_research.json']
    first={z['id']:z for z in read('b3_staircase_first_inventory.json')['records']};planes=read('b3_staircase_plane_inventory.json');raw={z['id']:z for z in read('b3_inverse_clique_inventory.json')['records']};native={z['id']:z for z in read('b3_third_cover_inventory.json')['records']}
    records=[];total=Counter()
    for rec in planes['records']:
        name=rec['id'];parent=raw[name];z=native[name];B,C,D=map(set,[z['B'],z['C'],z['D']]);controls=[{0,1,2},{3},B,C,D];orbit={};transports=[]
        for c in rec['classes']:
            frames=next(v['frames'] for v in first[name]['classes'] if v['extra_pair']==c['extra_pair'])
            for si,ti,pp in c['retained']:
                assert len(pp)==3;ri=next(i for i in pp if i not in [si,ti]);basis=[set(frames[i]) for i in [si,ti,ri]];masks,perm=canonical(name,basis,c['extra_pair'],controls);key=tuple(masks)
                orbit.setdefault(key,0);orbit[key]+=1;transports.append(dict(extra_pair=c['extra_pair'],indices=[si,ti,ri],basis=masks,permutation=perm))
        expected=8 if name=='b3_mixed_c1_third6' else 2;assert len(orbit)==expected
        c=next(c for c in parent['global_classes'] if c['extra_pair']==[2,6]);G=set(map(tuple,parent['required_P3_edges']))|{(2,6)};entries=[]
        for basis,multiplicity in sorted(orbit.items()):
            S,T,R=[{q for q in range(13) if m>>q&1} for m in basis];rows=lg.letters(parent,c,S,T,R,[S,T,R],B,C,D);proof,stats=tree(rows,list(basis),B,C,D,G)
            total.update(stats);total['orbits']+=1;total['literal_letters']+=len(rows)
            entries.append(dict(basis=list(basis),multiplicity=multiplicity,rows=[list(r) for r,f in rows],flags=[f for r,f in rows],tree=proof,tree_stats=stats))
            print(name,list(basis),len(rows),stats,flush=True)
        records.append(dict(id=name,transports=transports,orbits=entries,geometry_excluded=True));total['prefix_transports']+=len(transports)
    assert total['orbits']==10 and total['prefix_transports']==180
    names=[Path(__file__).name,'b3_staircase_letter_generator.py','enumerate_b3_staircase_first.py','PROOF.md#problem4-b3-staircase-flag-exclusion','b3_staircase_scope.json','b3_staircase_baseline_state.json','AUXILIARY_AUDIT_20261010_20.json','b3_staircase_first_inventory.json','b3_staircase_plane_inventory.json','b3_inverse_clique_inventory.json','b3_third_cover_inventory.json']
    result=dict(status='complete_necessary_exclusion_inventory',parameter=[13,9,1],stats=dict(total),records=records,new_excluded_third_ids=[r['id'] for r in records],source_sha256={n:sha(ROOT/n) for n in names},scope='Complete staircase necessary-domain rejection for two B3 geometries, with all prefixes transported and all literal letters retained. No numerical F value or alphabet separation.')
    (ROOT/'b3_staircase_inventory.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['records','source_sha256']}),flush=True)
if __name__=='__main__':main()
