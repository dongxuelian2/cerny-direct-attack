"""Independent literal output sets, exact kernels and full graph catalogues."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
from functools import lru_cache
import json,hashlib
ROOT=Path(__file__).resolve().parent
Q,H,A=set(range(13)),{0,1,2},{3}
PAIRS=list(combinations(range(13),2));BITS={e:1<<i for i,e in enumerate(PAIRS)}
allframes=[{3}|set(S) for S in combinations(sorted(Q-A),8)]
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def edges(m):return [e for i,e in enumerate(PAIRS) if m>>i&1]

def graphs(kernels):
    universe=sorted({e for m in kernels for e in edges(m)})
    result=[]
    for size in range(1,5):
        for es in combinations(universe,size):
            mask=sum(BITS[e] for e in es)
            # Exactly the graphs realizable as unions of available kernels.
            cover=0
            for m in kernels:
                if not m&~mask:cover|=m
            if cover==mask:result.append(mask)
    return sorted(result)

def kernel_catalogue(P1):
    E=edges(P1);answer=[]
    for chosen in product((False,True),repeat=len(E)):
        subset={e for e,v in zip(E,chosen) if v};blocks=[{q} for q in range(13)]
        for u,v in subset:
            merged=[b for b in blocks if u in b or v in b]
            blocks=[b for b in blocks if b not in merged]+[set().union(*merged)]
        if subset=={e for b in blocks for e in combinations(sorted(b),2)}:
            answer.append((sum(BITS[e] for e in subset),blocks))
    return answer

def literal_quotas(G,out,Jsize):
    adj=[set() for _ in range(13)]
    for u,v in G:adj[u].add(v);adj[v].add(u)
    quotas={};count=0
    for labels in combinations(range(13),10):
        I=set(labels)
        if any(adj[q]&I for q in I):continue
        complement=sorted(Q-I)
        for size in range(4):
            for extra in combinations(complement,size):
                T=set(extra);available=I|T
                eligible=[q for q in sorted(I) if not adj[q]&available]
                for protected in combinations(eligible,Jsize):
                    L=set(protected);counts=[0]*24;targets=[0]*24
                    for states,col in [(I-L,1),(L,2),(T,3)]:
                        for q in states:
                            i=3*out[q]+col-1;counts[i]+=1;targets[i]|=1<<q
                    entry=quotas.setdefault(tuple(counts),[0]*24)
                    for i,v in enumerate(targets):entry[i]|=v
                    count+=1
    return quotas,count

@lru_cache(None)
def covered_kernel_catalogue(Jtuple):
    J=set(Jtuple);eligible=[e for e in PAIRS if set(e)&H and not set(e)&J];answer=[]
    for size in range(5):
        for chosen in combinations(eligible,size):
            parent=list(range(13))
            def find(q):
                while parent[q]!=q:q=parent[q]
                return q
            for u,v in chosen:parent[find(u)]=find(v)
            components={}
            for q in range(13):components.setdefault(find(q),set()).add(q)
            blocks=list(components.values());full={e for b in blocks for e in combinations(sorted(b),2)}
            if set(chosen)!=full or any(len(b-H)>1 or (len(b)>1 and b&J) for b in blocks):continue
            answer.append((sum(BITS[e] for e in chosen),tuple(frozenset(b) for b in blocks)))
    return tuple(answer)

def verify_native_geometry(z,ns):
    B,C=map(set,(z['B'],z['C']));J=set(ns['mandatory'])
    output=[sum((q in X)<<(2-i) for i,X in enumerate((A,B,C))) for q in range(13)]
    catalog=covered_kernel_catalogue(tuple(sorted(J)))
    for f in ns['fields']:
        labels=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,(f['preA'],f['preB'],f['preC'])))) for q in range(13)]
        expected=[]
        for mask,blocks in catalog:
            if any(len({labels[q] for q in b})>1 for b in blocks):continue
            counts=[sum(labels[min(b)]==a for b in blocks) for a in range(8)]
            if all(counts[a]<=output.count(a) for a in range(8)):expected.append(mask)
        assert sorted(expected)==f['compatible_kernel_masks']
    return len(catalog)

def verify_geometry(data,z,ns):
    name=z['id'];assert data['id']==name and all(data[k]==z[k] for k in ('B','C','D'))
    assert data['fields']==ns['fields'] and data['mandatory']==ns['mandatory']
    native_catalogue_size=verify_native_geometry(z,ns)
    B,C,D=map(set,(z['B'],z['C'],z['D']));J=set(ns['mandatory'])
    assert not J&H and J==set.intersection(*(S for S in allframes if all(len(S&X)==1 for X in (B,C,D))))
    kernels=sorted({m for f in ns['fields'] for m in f['compatible_kernel_masks']})
    expected=graphs(kernels);assert data['unique_kernel_masks']==kernels and [c['P1_mask'] for c in data['records']]==expected and data['global_classes']==len(expected)
    # Verify all D-orbit transports under H,A,B,C-preserving permutations.
    cells=[{q for q in Q-A if tuple(q in X for X in (H,B,C))==sig} for sig in product((False,True),repeat=3)]
    transports=0;closed_transports=0
    for size in range(1,5):
        for item in combinations(sorted(Q-A),size):
            R=set(item)
            if len(R-H)>1 or [len(R&cell) for cell in cells]!=z['cell_signature']:continue
            perm={3:3}
            for cell in cells:perm.update(zip(sorted(cell&D)+sorted(cell-D),sorted(cell&R)+sorted(cell-R)))
            assert set(perm)==set(perm.values())==Q and {perm[q] for q in D}==R and all({perm[q] for q in X}==X for X in (H,A,B,C))
            feasible=[S for S in allframes if all(len(S&X)==1 for X in (B,C,R))]
            assert len(feasible)==z['feasible_nine_sets'] and set.intersection(*feasible)=={perm[q] for q in J}
            for c in data['records']:
                if c['reason']!='maximal_graph_not_SC':continue
                closed={perm[q] for q in c['closed_set']}
                assert closed and closed!=Q
                assert all({perm[q] for q in c['maximal_arrows'][p]}<=closed for p in c['closed_set'])
                closed_transports+=1
            transports+=1
    assert transports==z['labelled_D']==z['orbit_size']
    out=[sum((q in X)<<(2-i) for i,X in enumerate((A,B,C))) for q in range(13)]
    cache={};counts=Counter();colourings=0;tested=0
    for c in data['records']:
        P1=c['P1_mask'];catalog=kernel_catalogue(P1)
        # Independently recover all atom-compatible native kernels in P1.
        atom_masks=[];typed=[]
        for f in ns['fields']:
            ins=[sum((q in X)<<(2-i) for i,X in enumerate(map(set,(f['preA'],f['preB'],f['preC'])))) for q in range(13)]
            local=[];variants=[]
            for m,blocks in catalog:
                if any(len({ins[q] for q in b})>1 or (len(b)>1 and b&J) for b in blocks):continue
                if any(len(b-H)>1 for b in blocks):continue
                capacity=[sum(ins[min(b)]==a for b in blocks) for a in range(8)]
                if any(capacity[a]>out.count(a) for a in range(8)):continue
                local.append(m);variants.append((m,blocks,ins))
            assert sorted(local)==[m for m in f['compatible_kernel_masks'] if not m&~P1]
            atom_masks.append(local);typed.append(variants)
        prelim=[any(set(f[key])==X and atom_masks[i] for i,f in enumerate(ns['fields'])) for key,X in [('preA',B),('preB',C),('preC',D)]]
        if not all(prelim):
            assert c['reason']=='preliminary_missing_supplier' and c['supplier_options']==prelim
            counts[c['reason']]+=1;continue
        G=set(edges(P1))|set(combinations(sorted(C),2))|set(combinations(sorted(D),2));assert c['G']==[list(e) for e in sorted(G)]
        key=tuple(sorted(G))
        if key not in cache:
            cache[key],n=literal_quotas(G,out,len(J));colourings+=n
        quota=cache[key];allowed=[];arrows=[0]*13
        for variants in typed:
            local=[]
            for m,blocks,ins in variants:
                signature=[0]*24;tagged=[]
                for b in blocks:
                    col=2 if b&J else 1 if b-H else 3;i=3*ins[min(b)]+col-1
                    signature[i]+=1;tagged.append((b,i))
                target=quota.get(tuple(signature));tested+=1
                if target is None:continue
                local.append(m)
                for b,i in tagged:
                    for p in b:arrows[p]|=target[i]
            allowed.append(sorted(local))
        assert c['field_kernel_masks']==allowed
        assert c['maximal_arrows']==[[q for q in range(13) if a>>q&1] for a in arrows]
        suppliers=[any(set(f[key])==X and allowed[i] for i,f in enumerate(ns['fields'])) for key,X in [('preA',B),('preB',C),('preC',D)]]
        assert suppliers==c['suppliers']
        if not all(suppliers):assert c['reason']=='missing_supplier' and c['closed_set'] is None
        elif c['reason']=='maximal_graph_not_SC':
            R=set(c['closed_set']);mask=sum(1<<q for q in R)
            assert R and R!=Q and all(not arrows[p]&~mask for p in R)
        else:
            assert c['reason']=='retained_overapproximation' and c['closed_set'] is None
            for root in Q:
                R={root}
                while True:
                    expanded=R|{q for p in R for q in Q if arrows[p]>>q&1}
                    if expanded==R:break
                    R=expanded
                assert R==Q
        counts[c['reason']]+=1
    assert dict(counts)==data['counts']
    return dict(id=name,global_classes=len(expected),counts=dict(counts),literal_output_colourings=colourings,quota_tests=tested,labelled_D_transports=transports,closed_set_transports=closed_transports,native_covered_kernel_catalogue=native_catalogue_size)

def check_inventory(data):
    scope=read('b1_b2_inverse_union_scope.json')
    assert data['status']=='complete_necessary_exclusion_inventory' and data['parameter']==scope['parameter']==[13,9,1]
    for obj in (scope,data):
        for n,h in obj['source_sha256'].items():assert sha(ROOT/n)==h,n
    baseline=read(scope['baseline']);cp=read(scope['checkpoint']);assert sha(ROOT/scope['baseline'])==cp['source_sha256']['active_research.json']
    reports=['three_cover_atom_kernel_audit.json','small_first_third_audit.json','mandatory_core_isolation_audit.json','inverse_clique_letter_controls_audit.json']
    premise_sources=set()
    for n in reports+['three_cover_atom_kernel_inventory.json','small_first_third_inventory.json']:
        obj=read(n)
        if n in reports:assert obj['status']=='pass'
        for f,h in obj['source_sha256'].items():assert sha(ROOT/f)==h,f;premise_sources.add(f)
    required=set(scope['source_sha256'])|set(data['source_sha256'])|premise_sources|{'common_block_profiles_audit.json'}
    for n in required&set(cp['source_sha256']):
        assert sha(ROOT/n)==cp['source_sha256'][n],n
    native={z['id']:z for z in read('three_cover_atom_kernel_inventory.json')['records']};inv={z['id']:z for z in read('small_first_third_inventory.json')['records']}
    assert [z['id'] for z in data['records']]==scope['selected'] and data['geometries']==len(scope['selected'])==25
    j=baseline['joint_fiber_cases'];reports_checked=[];totals=Counter();negative=[]
    for record in data['records']:
        name=record['id'];z=inv[name]
        assert z['joint_id'] not in j['unrestricted_excluded_orbits'] and name not in j['unrestricted_additional_small_first_third_exclusions']
        report=verify_geometry(record,z,native[name]);reports_checked.append(report);totals.update(report['counts'])
        if not report['counts'].get('retained_overapproximation',0):negative.append(name)
        print(json.dumps(report),flush=True)
    assert negative==scope['excluded_geometries']==data['excluded_geometries'] and len(negative)==24
    assert totals['retained_overapproximation']>0 and data['retained_control']==scope['retained_control']
    assert dict(totals)==data['counts'] and sum(z['global_classes'] for z in reports_checked)==data['global_classes']
    cuts={}
    for array in [read('common_block_profiles_audit.json')['profile_cuts'],baseline['two_cover_unique_kernel_profile_cuts'],baseline['two_cover_exact_kernel_profile_cuts'],baseline['three_cover_atom_kernel_profile_cuts']]:
        for z in array:cuts.setdefault(z['id'],set()).update(map(tuple,z['removed_parent_pairs']))
    inv_records=list(inv.values())
    ub=[z for z in inv_records if z['joint_id'] not in j['unrestricted_excluded_orbits'] and z['id'] not in j['unrestricted_additional_small_first_third_exclusions']]
    bb=[z for z in inv_records if z['joint_id'] not in j['binary_excluded_orbits'] and z['id'] not in j['binary_additional_small_first_third_exclusions']]
    profiles=lambda z:set(map(tuple,z['binary_profile_pairs']))-cuts.get(z['id'],set())
    assert (len(ub),len(bb),sum(bool(profiles(z)) for z in bb),sum(len(profiles(z)) for z in bb))==(136,120,105,448)
    ua=[z for z in ub if z['id'] not in negative];ba=[z for z in bb if z['id'] not in negative]
    assert (len(ua),len(ba),sum(bool(profiles(z)) for z in ba),sum(len(profiles(z)) for z in ba))==(112,99,95,437)
    assert {z['joint_id'] for z in ub}=={z['joint_id'] for z in ua}
    assert {z['joint_id'] for z in bb if profiles(z)}=={z['joint_id'] for z in ba if profiles(z)}
    sources={Path(__file__).name,'b1_b2_inverse_union_inventory.json','b1_b2_inverse_union_scope.json','PROOF.md#problem4-b1-b2-inverse-union-exclusion',scope['baseline'],scope['checkpoint'],'common_block_profiles_audit.json','three_cover_atom_kernel_inventory.json','small_first_third_inventory.json',*reports,*premise_sources}
    return dict(status='pass',parameter=[13,9,1],records=reports_checked,geometries=25,global_classes_checked=data['global_classes'],counts=dict(totals),new_excluded_third_ids=negative,retained_control=scope['retained_control'],new_unrestricted_joint_exclusions=[],new_binary_joint_exclusions=[],remaining_unrestricted_geometries=112,remaining_binary_geometries=99,remaining_binary_typed=95,remaining_binary_profiles=437,remaining_binary_joints=18,remaining_unrestricted_joints=20,source_sha256={n:sha(ROOT/n) for n in sorted(sources)},scope=scope['scope'])

def main():
    result=check_inventory(read('b1_b2_inverse_union_inventory.json'))
    (ROOT/'b1_b2_inverse_union_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','source_sha256')}),flush=True)
if __name__=='__main__':main()
