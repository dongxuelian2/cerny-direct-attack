"""Complete C3 prefix transports and staircase rejection inventories."""
from pathlib import Path
from collections import Counter
import json,hashlib
from enumerate_b3_staircase import tree
from b3_staircase_letter_generator import letters
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(basis,extra,controls):
    cells={}
    for q in range(13):cells.setdefault(tuple(q in X for X in controls),[]).append(q)
    perm={};E=set(extra or [])
    for cell in cells.values():perm.update(zip(sorted(cell,key=lambda q:(q not in E,tuple(q in S for S in basis),q)),sorted(cell)))
    return tuple(sorted(perm[q] for q in E)),tuple(sum(1<<perm[q] for q in S) for S in basis),[perm[q] for q in range(13)]
def main():
    baseline=read('c3_staircase_baseline_state.json');old=read('AUXILIARY_AUDIT_20261010_21.json');assert sha(ROOT/'c3_staircase_baseline_state.json')==old['source_sha256']['active_research.json']
    first={z['id']:z for z in read('c3_staircase_first_inventory.json')['records']};planes=read('c3_staircase_plane_inventory.json');raw={z['id']:z for z in read('b3_inverse_clique_inventory.json')['records']};native={z['id']:z for z in read('b3_third_cover_inventory.json')['records']}
    records=[];total=Counter();expected={'b3_mixed_c3_third1':170,'b3_mixed_c3_third4':166,'b3_mixed_c3_third6':50,'b3_mixed_c3_third9':20}
    for rec in planes['records']:
        name=rec['id'];parent=raw[name];z=native[name];B,C,D=map(set,[z['B'],z['C'],z['D']]);controls=[{0,1,2},{3},B,C,D];orbit={};transports=[]
        for c in rec['classes']:
            frames=next(v['frames'] for v in first[name]['classes'] if v['extra_pair']==c['extra_pair'])
            for si,ti,pp in c['retained']:
                for ri in pp:
                    if ri in (si,ti):continue
                    basis=[set(frames[i]) for i in [si,ti,ri]];em,bm,perm=canonical(basis,c['extra_pair'],controls);plane=sorted(sum(1<<perm[q] for q in frames[i]) for i in pp);key=(em,bm)
                    entry=orbit.setdefault(key,dict(count=0,plane=plane));assert entry['plane']==plane;entry['count']+=1
                    transports.append(dict(extra_pair=c['extra_pair'],indices=[si,ti,ri],plane_indices=pp,canonical_extra=list(em),basis=list(bm),plane=plane,permutation=perm))
        assert len(orbit)==expected[name];entries=[]
        for oi,((em,basis),entry) in enumerate(sorted(orbit.items())):
            c=next(c for c in parent['global_classes'] if tuple(c['extra_pair'] or [])==em);G=set(map(tuple,parent['required_P3_edges']))|({em} if em else set());S,T,R=[{q for q in range(13) if m>>q&1} for m in basis];plane=[{q for q in range(13) if m>>q&1} for m in entry['plane']]
            rows=letters(parent,c,S,T,R,plane,B,C,D);proof,stats=tree(rows,list(basis),B,C,D,G);total.update(stats);total['orbits']+=1;total['literal_letters']+=len(rows)
            rowdigest=hashlib.sha256(json.dumps([list(r) for r,f in rows],separators=(',',':')).encode()).hexdigest();flagdigest=hashlib.sha256(json.dumps([f for r,f in rows],separators=(',',':')).encode()).hexdigest()
            entries.append(dict(extra_pair=list(em),basis=list(basis),plane=entry['plane'],multiplicity=entry['count'],letter_count=len(rows),rows_sha256=rowdigest,flags_sha256=flagdigest,tree=proof,tree_stats=stats))
            if (oi+1)%25==0:print(name,'orbits',oi+1,'/',len(orbit),flush=True)
        records.append(dict(id=name,transports=transports,orbits=entries,geometry_excluded=True));total['prefix_transports']+=len(transports)
    assert total['orbits']==406 and total['prefix_transports']==53790
    names=[Path(__file__).name,'enumerate_b3_staircase.py','b3_staircase_letter_generator.py','enumerate_b3_staircase_first.py','C3_STAIRCASE_EXCLUSION.md','B3_STAIRCASE_FLAG_EXCLUSION.md','c3_staircase_scope.json','c3_staircase_baseline_state.json','AUXILIARY_AUDIT_20261010_21.json','c3_staircase_first_inventory.json','c3_staircase_plane_inventory.json','b3_inverse_clique_inventory.json','b3_third_cover_inventory.json']
    result=dict(status='complete_necessary_exclusion_inventory',parameter=[13,9,1],stats=dict(total),records=records,new_excluded_third_ids=[r['id'] for r in records],source_sha256={n:sha(ROOT/n) for n in names},scope='Complete arbitrary-alphabet C3 staircase exclusions with all companion fields, literal letters, four-vertex planes and actual R choices. No numerical F value or alphabet separation.')
    (ROOT/'c3_staircase_inventory.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['records','source_sha256']}),flush=True)
if __name__=='__main__':main()
