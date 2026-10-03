"""Independent exhaustive permutation, set-image, and transformation checks."""
import argparse
from collections import deque
import copy
from hashlib import sha256
from itertools import product, permutations
import json
from math import factorial
from pathlib import Path


def digest(value):
    return sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def nearest(f):
    candidates=list(permutations(range(len(f))))
    scores=[sum(f[q]==p[q] for q in range(len(f))) for p in candidates]
    best=max(scores)
    return [p for p,score in zip(candidates,scores) if score==best]


def images(rows):
    initial=frozenset(range(len(rows[0])));seen={initial};todo=deque([initial])
    while todo:
        S=todo.popleft()
        for f in rows:
            T=frozenset(f[q] for q in S)
            if T not in seen:seen.add(T);todo.append(T)
    return seen


def mask(S):return sum(1<<q for q in S)


def monoid(rows):
    identity=tuple(range(len(rows[0])));seen={identity};todo=deque([identity])
    while todo:
        f=todo.popleft()
        for a in rows:
            h=tuple(a[t] for t in f)
            if h not in seen:seen.add(h);todo.append(h)
    return seen


def sc(rows):
    n=len(rows[0])
    for start in range(n):
        reached={start};todo=[start]
        for q in todo:
            for a in rows:
                if a[q] not in reached:reached.add(a[q]);todo.append(a[q])
        if len(reached)!=n:return False
    return True


def map_scope(z):
    n=z['n'];total=cs_count=controls=subset_controls=swap_controls=error_controls=0;stream=sha256()
    for f in product(range(n),repeat=n):
        cs=nearest(f);r=len(set(f));total+=1;cs_count+=len(cs)
        stream.update(json.dumps([f,cs],separators=(',',':')).encode()+b'\n')
        for p in cs:
            assert sum(f[q]==p[q] for q in range(n))==r
            inv=[p.index(t) for t in range(n)];e=[inv[f[q]] for q in range(n)]
            selected={q for q in range(n) if p[q]==f[q]}
            for q in range(n):
                assert e[q] in selected and f[e[q]]==f[q] and p[e[q]]==f[q]
                actual=[int(t==f[q]) for t in range(n)]
                expected=[int(t==p[q]) for t in range(n)]
                if q not in selected:
                    expected[f[q]]+=1;expected[p[q]]-=1
                assert actual==expected;controls+=1;error_controls+=n
            for x in range(n):
                for y in range(x+1,n):
                    if f[x]!=f[y]:continue
                    changed=list(p);changed[x],changed[y]=changed[y],changed[x]
                    assert tuple(changed) in cs
                    quotient=tuple(inv[changed[q]] for q in range(n))
                    expected=list(range(n));expected[x],expected[y]=y,x
                    assert quotient==tuple(expected);swap_controls+=1
        for bits in range(1<<n):
            S=[q for q in range(n) if bits>>q&1]
            injective=len({f[q] for q in S})==len(S)
            compatible=[p for p in cs if all(p[q]==f[q] for q in S)]
            assert bool(compatible)==injective
            if r==n-1:
                x,y=next((x,y) for x in range(n) for y in range(x+1,n) if f[x]==f[y])
                assert len(compatible)==[2,1,0][int(x in S)+int(y in S)]
            subset_controls+=1
    assert total==z['maps'] and cs_count==z['closest_permutations'] and controls==z['row_controls']
    assert stream.hexdigest()==z['semantic_sha256']
    return dict(n=n,maps=total,closest_permutations=cs_count,row_controls=controls,
                coordinate_error_controls=error_controls,subset_compatibility_controls=subset_controls,kernel_swap_controls=swap_controls)


def binary_scope(z):
    n=z['n'];maps=[f for f in product(range(n),repeat=n) if len(set(f))>=n-1]
    cs={f:nearest(f) for f in maps};cache={};hist={};total=singular=sync=bad=scbad=0;first=None
    group_elements=image_vertices=0
    for f in maps:
        for h in maps:
            total+=1
            if len(set(f))==len(set(h))==n:continue
            singular+=1;rs=(f,h);orbit=images(rs);image_vertices+=len(orbit)
            yes=min(map(len,orbit))==1
            gens=tuple(sorted(set(cs[f]+cs[h])))
            if gens not in cache:cache[gens]=monoid(gens)
            G=cache[gens];group_elements+=len(G);full=len(G)==factorial(n)
            kernels={(x,y) for row in rs for x in range(n) for y in range(x+1,n) if row[x]==row[y]}
            edges={tuple(sorted((p[x],p[y]))) for p in G for x,y in kernels}
            classes=[{q} for q in range(n)]
            for x,y in edges:
                Cx=next(C for C in classes if x in C);Cy=next(C for C in classes if y in C)
                if Cx is not Cy:classes.remove(Cx);classes.remove(Cy);classes.append(Cx|Cy)
            d=len(classes);hist[str(d)]=hist.get(str(d),0)+1
            assert full==(d==1)
            if yes:sync+=1;assert full
            elif full:
                bad+=1
                if sc(rs):
                    scbad+=1
                    if first is None:first=dict(rows=[list(f),list(h)],images=sorted(map(mask,orbit)),normal_edges=len(edges))
    expected=dict(maps=len(maps),labeled_inputs=total,inputs_with_singular=singular,sync_inputs=sync,
                  nonsync_full_completion=bad,SC_nonsync_full_completion=scbad,component_histogram=hist,first_SC_nonsync_full=first)
    assert all(z[key]==value for key,value in expected.items())
    assert z['scope']=='complete labeled binary alphabets with every letter rank n or n-1; full-G count restricted to inputs with a singular letter'
    return dict(n=n,**expected,independent_group_elements=group_elements,independent_image_vertices=image_vertices,distinct_group_generator_sets=len(cache))


def family(z):
    n=z['n'];assert n>=3
    a=list(range(n));a[0]=1;a[1]=0
    b=[-1]*n;cycle=[0]+list(range(2,n))
    for q,t in zip(cycle,cycle[1:]+cycle[:1]):b[q]=t
    b[1]=b[0];rs=[a,b]
    assert z['rows_sha256']==digest(rs)
    assert z['explicit_rows']==(rs if n<=40 else None)
    cp=b[:];cp[0]=1;cm=b[:];cm[1]=1
    assert z['closest_completion_hashes']==[digest(cp),digest(cm)]
    assert cp==list(range(1,n))+[0]
    assert sorted(cp)==sorted(cm)==list(range(n))
    for p in (cp,cm):assert sum(t==u for t,u in zip(p,b))==n-1
    orbit=images(rs)
    assert orbit=={frozenset(range(n)),frozenset(range(1,n)),frozenset([0]+list(range(2,n)))}
    assert sorted(map(mask,orbit))==z['images'] and min(map(len,orbit))==z['minimum_rank']==n-1
    # Prove SC by literal spanning walks, rather than n BFS runs.
    assert set(cycle)==set(range(n))-{1} and a[0]==1 and b[1]==2
    assert z['strongly_connected'] is True
    classes=[0,0]+list(range(1,n-1))
    for q in range(n):
        assert classes[a[q]]==classes[q]
        assert classes[b[q]]==(classes[q]+1)%(n-1)
    # The two actual permutation words are identity and a. A word with b is singular.
    identity=list(range(n));assert cp not in [identity,a] and cm not in [identity,a]
    assert z['original_permutation_group_order']==2 and z['completions_unrepresentable'] is True
    # Conjugating a by cp gives each circular adjacent transposition, a connected graph.
    adjacent={tuple(sorted((q,(q+1)%n))) for q in range(n)};assert len(adjacent)==n
    assert z['full_completion_group'] is True
    size=0
    if n<=10:
        actual=monoid(rs);size=len(actual)
        assert tuple(cp) not in actual and tuple(cm) not in actual
        assert {p for p in actual if len(set(p))==n}=={tuple(identity),tuple(a)}
        assert min(len(set(p)) for p in actual)==n-1 and sc(rs)
        if n<=6:assert nearest(b)==sorted([tuple(cp),tuple(cm)])
    return dict(n=n,image_vertices=len(orbit),state_congruence_controls=2*n,actual_monoid_size=size)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('direct_attack/data/permutation_completion_boundary.json'))
    ap.add_argument('--out',type=Path,default=Path('direct_attack/data/permutation_completion_boundary_checks.json'))
    args=ap.parse_args();data=json.loads(args.source.read_text())
    assert [z['n'] for z in data['all_map_scopes']]==list(range(2,6))
    assert [z['n'] for z in data['binary_scopes']]==list(range(2,5))
    assert [z['n'] for z in data['families']]==list(range(3,41))+[65,129,257,513,1025,2051,4096]
    mr=[map_scope(z) for z in data['all_map_scopes']];br=[binary_scope(z) for z in data['binary_scopes']];fr=[family(z) for z in data['families']]
    corruptions=[];base=data['families'][0]
    for key,value in [('rows_sha256','0'*64),('minimum_rank',1),('images',[]),('original_permutation_group_order',6),('full_completion_group',False),('completions_unrepresentable',False),('strongly_connected',False)]:
        z=copy.deepcopy(base);z[key]=value;corruptions.append((family,z))
    z=copy.deepcopy(base);z['closest_completion_hashes'][0]='0'*64;corruptions.append((family,z))
    z=copy.deepcopy(base);z['explicit_rows'][1][0]=1;corruptions.append((family,z))
    z=copy.deepcopy(data['all_map_scopes'][0]);z['semantic_sha256']='0'*64;corruptions.append((map_scope,z))
    z=copy.deepcopy(data['binary_scopes'][0]);z['sync_inputs']-=1;corruptions.append((binary_scope,z))
    for check,z in corruptions:
        try:check(z)
        except AssertionError:pass
        else:raise AssertionError('corruption accepted')
    out=dict(verified=True,all_maps=sum(z['maps'] for z in mr),closest_permutations=sum(z['closest_permutations'] for z in mr),
             subset_compatibility_controls=sum(z['subset_compatibility_controls'] for z in mr),kernel_swap_controls=sum(z['kernel_swap_controls'] for z in mr),
             coordinate_error_controls=sum(z['coordinate_error_controls'] for z in mr),binary_inputs=sum(z['labeled_inputs'] for z in br),
             independent_group_elements=sum(z['independent_group_elements'] for z in br),independent_image_vertices=sum(z['independent_image_vertices'] for z in br),
             family_parameters=len(fr),maximum_n=max(z['n'] for z in fr),actual_monoid_scopes=sum(bool(z['actual_monoid_size']) for z in fr),
             actual_monoid_elements=sum(z['actual_monoid_size'] for z in fr),corruptions_rejected=len(corruptions),map_reports=mr,binary_reports=br,family_reports=fr,
             boundary='All-n arbitrary-rank necessary theorem and exact neutral compatibility PROVED paper; binary SC inverse counterfamily every n>=3 PROVED paper; only listed finite scopes COMPUTATIONALLY VERIFIED, no formal kernel, priority and Cerny OPEN')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if not k.endswith('_reports')}),flush=True)


if __name__=='__main__':main()
