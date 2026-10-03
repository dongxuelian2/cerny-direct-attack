"""Independent pair Bellman solver, unary-cycle controls and retained-certificate audit."""
import argparse
from collections import Counter
import copy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def pair_distances(rows,n):
    pairs=[(p,q) for p in range(n) for q in range(p+1,n)]
    d={pair:None for pair in pairs};rounds=0
    while True:
        changed=False
        for p,q in pairs:
            candidates=[]
            for f in rows:
                x,y=sorted((f[p],f[q]))
                value=0 if x==y else d[x,y]
                if value is not None:candidates.append(value+1)
            v=min(candidates) if candidates else None
            if v is not None and (d[p,q] is None or v<d[p,q]):d[p,q]=v;changed=True
        rounds+=1
        if not changed:break
        assert rounds<=len(pairs)+1
    return d


def mu_profile(d,n):
    out=[]
    for q in range(n):
        finite=[v for pair,v in d.items() if q in pair and v is not None]
        out.append(min(finite) if finite else None)
    return out


def strong(rows,n):
    for source in range(n):
        seen={source};old=set()
        while old!=seen:
            old=set(seen);seen.update(f[q] for f in rows for q in old)
        if len(seen)!=n:return False
    return True


def audit_family(z):
    n=z['n'];m=n-1;p=z['marked_state'];rows=z['rows'];assert n>=3 and p==m and len(rows)==3
    assert rows[0]==[(q+1)%m for q in range(m)]+[p]
    assert rows[1]==[q if q<m-1 else 0 for q in range(m)]+[p]
    assert rows[2]==[n//2 if q!=p else 0 for q in range(n)]
    image=list(range(n))
    for a in z['word']:image=[rows[a][q] for q in image]
    assert z['word']==[2,2] and z['word_length']==len(z['word'])==2
    assert len(set(image))==1 and z['reset_square']==image
    for f in rows:assert all(f[p]!=f[q] for q in range(m))
    assert z['compress_with_another_threshold']==2
    return n*2


def height_controls(z):
    assert z['maximum_n']==5;h=sha256();maps=controls=0
    for n in range(2,6):
        for row in product(range(n),repeat=n):
            maps+=1;power=list(range(n))
            for _ in range(n):power=[row[q] for q in power]
            cycle=set(power)
            for q in range(n):
                if q in cycle:continue
                v=q;height=0
                while v not in cycle:v=row[v];height+=1
                candidates=[]
                for p in cycle:
                    r=p
                    for _ in range(height):r=row[r]
                    if r==v:candidates.append(p)
                assert len(candidates)==1 and 1<=height<=n-1
                partner=candidates[0];assert partner!=q
                h.update(json.dumps([n,list(row),q,height,partner],separators=(',',':')).encode()+b'\n');controls+=1
    assert z['maps']==maps and z['noncyclic_state_controls']==controls and z['semantic_sha256']==h.hexdigest()
    return maps,controls


def all_small_alphabets():
    n=3;maps=list(product(range(n),repeat=n));cases=stars=finite=sync=0;hist=Counter();stream=sha256()
    for k in range(4):
        for rows in product(maps,repeat=k):
            d=pair_distances(rows,n);profile=mu_profile(d,n);cases+=1;sync+=all(v is not None for v in d.values())
            for q,mu in enumerate(profile):
                stars+=1
                if mu is None:continue
                finite+=1;assert mu<=(n-1)*(n-2)//2+1
                start=next(pair for pair,v in d.items() if q in pair and v==mu);path=[];pair=start;word=[]
                while pair[0]!=pair[1]:
                    path.append(pair);value=d[pair]
                    for a,f in enumerate(rows):
                        image=tuple(sorted((f[pair[0]],f[pair[1]])))
                        next_value=0 if image[0]==image[1] else d[image]
                        if next_value is not None and next_value==value-1:word.append(a);pair=image;break
                    else:raise AssertionError('no Bellman descent')
                assert len(path)==len(word)==mu and len(set(path))==mu
                assert all(q not in pair for pair in path[1:])
                excluded={pair for pair in d if q in pair and pair!=start}
                assert not excluded.intersection(path) and len(path)+len(excluded)<=n*(n-1)//2
                hist[mu]+=1
            stream.update(json.dumps([k,rows,profile],separators=(',',':')).encode()+b'\n')
    assert cases==20440
    return dict(n=3,alphabet_sizes=[0,1,2,3],ordered_alphabets=cases,star_controls=stars,compressible_marked_states=finite,
                synchronizing_alphabets=sync,mu_histogram={str(k):hist[k] for k in sorted(hist)},semantic_sha256=stream.hexdigest())


def audit_native_case(z,strong_expected):
    n=z['n'];rows=z['SC_rows'] if strong_expected else z['nonSC_rows'];claim=z['max_SC'] if strong_expected else z['max_nonSC']
    assert len(rows)==2 and all(len(f)==n and all(0<=x<n for x in f) for f in rows)
    assert strong(rows,n)==strong_expected
    d=pair_distances(rows,n);assert all(v is not None for v in d.values())
    profile=mu_profile(d,n);assert max(profile)==claim
    assert all(v<=(n-1)*(n-2)//2+1 for v in profile)
    return dict(n=n,strong=strong_expected,profile=profile,maximum_mu=claim,pair_vertices=len(d))


def audit_pressure(z):
    n,m,q=z['n'],z['core'],z['q'];rows=z['rows'];assert 0<m<n and q==m
    assert len(rows)==2 and all(len(f)==n and all(0<=v<n for v in f) for f in rows)
    assert all(rows[a][p]<m for a in range(2) for p in range(m))
    if z['mode']==0:
        expected=[[(p+1)%m for p in range(m)],[p if p<m-1 else 0 for p in range(m)]]
    else:
        assert m%3==0 and m>=9;p=m//3;expected=[list(range(m)),list(range(m))]
        for j in range(1,2*p):expected[0][j]=j+1 if j%2 else j-1
        for j in range(2*p):expected[1][j]=j-1 if j%2 else j+1
        expected[0][2*p]=2*p+1;expected[0][2*p+1]=3;expected[1][2*p]=2
        for j in range(2*p+2,m-1,2):expected[0][j],expected[0][j+1]=j+1,j
        for j in range(2*p+1,m-1,2):expected[1][j],expected[1][j+1]=j+1,j
    assert [f[:m] for f in rows]==expected and strong(expected,m)
    core_d=pair_distances(expected,m);assert all(v is not None for v in core_d.values())
    assert not strong(rows,n)
    d=pair_distances(rows,n);assert all(v is not None for v in d.values())
    profile=mu_profile(d,n);assert profile[q]==z['maximum_mu']<=n-1
    return dict(n=n,core=m,mode=z['mode'],q=q,mu=profile[q],pair_vertices=len(d))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,default=Path('direct_attack/data/compress_other_non_sc_boundary.json'));ap.add_argument('--out',type=Path,default=Path('direct_attack/data/compress_other_non_sc_boundary_checks.json'));args=ap.parse_args()
    data=json.loads(args.data.read_text(encoding='utf-8'));assert [z['n'] for z in data['family']]==list(range(3,65))+[101,257,1024,2049]
    actions=sum(audit_family(z) for z in data['family']);maps,heights=height_controls(data['noncyclic_controls']);small=all_small_alphabets()
    root=Path('direct_attack/data/research_pressure_126');native=[]
    for n in range(2,8):
        z=json.loads((root/f'compress_other_n{n}.json').read_text());assert z['n']==n and z['map_count']==n**n and z['tested']==z['first_map_orbits']*(n**n-1)
        assert sum(z['histogram'].values())==z['synchronizing'] and z['completed_planned_cover']
        native.extend(audit_native_case(z,s) for s in (False,True))
    pressure=json.loads((root/'nonterminal_mu_pressure_corrected.json').read_text());assert pressure['budget_each']==1000000 and pressure['seed']==20261002 and len(pressure['profiles'])==12
    retained=[audit_pressure(z) for z in pressure['profiles']]
    extremal={'n':4,'SC_rows':[[0,0,3,2],[2,0,1,3]],'max_SC':4};e=audit_native_case(extremal,True);assert e['profile'][3]==4
    counter=pair_distances([[1,2,0,0]],4);assert mu_profile(counter,4)[0] is None
    corruptions=[]
    for field,value in [('marked_state',0),('word',[2]),('word_length',3),('compress_with_another_threshold',100),('reset_square',[0]*3),('rows',[[0]*3]*3)]:
        z=copy.deepcopy(data['family'][0]);z[field]=value
        try:audit_family(z)
        except AssertionError:corruptions.append(field)
        else:raise AssertionError('accepted family corruption '+field)
    z=copy.deepcopy(extremal);z['max_SC']=5
    try:audit_native_case(z,True)
    except AssertionError:corruptions.append('native maximum')
    else:raise AssertionError('accepted native maximum')
    z=copy.deepcopy(pressure['profiles'][3]);z['rows'][1][0]=z['core']-1
    try:audit_pressure(z)
    except AssertionError:corruptions.append('wrong Figure3 core')
    else:raise AssertionError('accepted wrong core')
    out=dict(verified=True,family_parameters=len(data['family']),literal_transition_controls=actions,unary_maps=maps,noncyclic_height_controls=heights,all_small_alphabets=small,
             native_extremal_certificates=native,retained_mutation_certificates=retained,corruptions_rejected=corruptions,
             boundary='Independent exact finite controls and retained positive certificates only. Native full-cover negative searches and mutation searches remain EXPLORATORY; no upgrade of their completeness. General paper pair-star bound and noncyclic lemma are PROVED, not formal; literal Proposition7 construction REFUTED, existential claim OPEN here, general Cerny OPEN.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(verified=True,family_parameters=out['family_parameters'],unary_maps=maps,noncyclic_height_controls=heights,small_alphabets=small,retained_certificates=len(native)+len(retained),corruptions=len(corruptions))),flush=True)


if __name__=='__main__':main()
