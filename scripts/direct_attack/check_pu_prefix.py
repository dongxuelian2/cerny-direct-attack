"""Independent Bellman checks, reverse cut BFS, tuple groups and ordinary image BFS."""
from itertools import combinations
from pathlib import Path
import copy
import json
from direct_attack.ordinary_reverse_policy import profile as ordinary

ROOT=Path('scripts/direct_attack/data/pu_prefix')

def reach(n,arcs,start):
    seen={start};queue=[start]
    for q in queue:
        for s,t in arcs:
            if s==q and t not in seen:seen.add(t);queue.append(t)
    return seen

def verify(c):
    rows=c['rows'];n=c['n'];assert all(len(a)==n for a in rows)
    P=[];seeds={}
    for i,a in enumerate(rows):
        assert all(0<=q<n for q in a)
        if len(set(a))==n:P.append(i)
        else:
            changed=[q for q in range(n) if a[q]!=q];assert len(changed)==1
            s=changed[0];seeds[i]=(s,a[s])
    assert seeds
    records={(r['source'],r['target']):r for r in c['pairs']}
    assert len(records)==len(c['pairs'])==c['pair_vertices']
    for r in records.values():
        s,t=r['source'],r['target'];d=r['distance'];assert s!=t and 0<=s<n and 0<=t<n and type(d)==int and d>=0
        assert r['origin'] in seeds
        if r['parent'] is None:assert d==0 and (s,t)==seeds[r['origin']]
        else:
            pair,i=r['parent'];pair=tuple(pair);assert i in P
            assert pair in records and records[pair]['distance']==d-1 and records[pair]['origin']==r['origin']
            assert (rows[i][pair[0]],rows[i][pair[1]])==(s,t)
        for i in P:
            pair=rows[i][s],rows[i][t]
            assert pair in records and records[pair]['distance']<=d+1
    for pair in seeds.values():assert records[pair]['distance']==0
    unseen=set(range(n));orbits=[]
    while unseen:
        q=min(unseen);C=reach(n,[(s,rows[i][s]) for s in range(n) for i in P],q)
        orbits.append(sorted(C));unseen-=C
    assert c['group_orbits']==orbits
    assert c['commuting']==all(rows[i][rows[j][q]]==rows[j][rows[i][q]] for i in P for j in P for q in range(n))
    E=c['max_extension'];early={pair for pair,r in records.items() if r['distance']+1<E}
    final={pair for pair,r in records.items() if r['distance']+1<=E}
    assert all(len(reach(n,final,q))==n for q in range(n))
    S=set(c['target']);outside=set(range(n))-S;assert S and outside
    assert all(not(s in outside and t in S) for s,t in early)
    word=c['extension_word'];assert len(word)==E and all(i in P or i in seeds for i in word)
    T=set()
    for q in range(n):
        x=q
        for i in word:x=rows[i][x]
        if x in S:T.add(q)
    assert T==set(c['larger_preimage']) and len(T)==len(S)+1
    return records

def verify_cover(c):
    n=c['n'];assert n in [2,3,4] and c['basis_cap']==(1 if n==2 else 3)
    ps=list(map(tuple,c['permutations']));identity=tuple(range(n))
    assert len(ps)==__import__('math').factorial(n) and len(set(ps))==len(ps)
    assert all(sorted(p)==list(range(n)) for p in ps)
    nonid=[i for i,p in enumerate(ps) if p!=identity];cache={}
    def group(B):
        key=tuple(B)
        if key not in cache:
            G={identity}
            while True:
                H=G|{tuple(ps[p][g[q]] for q in range(n)) for g in G for p in B}
                if H==G:break
                G=H
            cache[key]=G
        return cache[key]
    if n==4:
        expected=set(combinations(nonid,4));assert len(expected)==8855
        got=set()
        for r in c['quadruple_redundancy']:
            B=tuple(r['basis']);assert B in expected and B not in got;got.add(B)
            p=r['removable'];assert p in B and ps[p] in group(tuple(q for q in B if q!=p))
        assert got==expected
    else:assert not c['quadruple_redundancy']
    bases=[]
    for size in range(1,c['basis_cap']+1):
        for B in combinations(nonid,size):
            if all(ps[p] not in group(tuple(q for q in B if q!=p)) for p in B):bases.append(B)
    assert len(bases)==c['bases'];expected={(B,k) for B in bases for k in range(1,n)};got=set()
    if n==3:assert all(len(B)<=2 for B in bases)
    for r in c['cuts']:
        B=tuple(r['basis']);k=r['cut_size'];assert (B,k) in expected and (B,k) not in got;got.add((B,k))
        # Reverse ordered-pair BFS from the entire entering cut, unlike the generator's per-seed forward BFS.
        d={(s,t):0 for s in range(k,n) for t in range(k)};queue=list(d)
        inverses=[tuple(ps[p].index(q) for q in range(n)) for p in B]
        for s,t in queue:
            if d[s,t]==n-1:continue
            for inv in inverses:
                pair=inv[s],inv[t]
                if pair not in d:d[pair]=d[s,t]+1;queue.append(pair)
        safe={(s,t) for s in range(n) for t in range(n) if s!=t and (s,t) not in d}
        assert safe==set(map(tuple,r['safe_units']))
        arcs={(g[s],g[t]) for g in group(B) for s,t in safe}
        R=set(r['closed_vertices']);assert R and len(R)<n
        assert all(s not in R or t in R for s,t in arcs)
    assert got==expected
    return dict(n=n,bases=len(bases),cuts=len(got),quadruples=len(c['quadruple_redundancy']))

def main():
    family=json.loads((ROOT/'families.json').read_text());samples=json.loads((ROOT/'retained_samples.json').read_text())
    arrays=json.loads((ROOT/'small_arrays.json').read_text());paircount=0;ordinary_count=0
    for c in family+[s['certificate'] for s in samples]:paircount+=len(verify(c))
    for c in family:
        n=c['n'];assert n%2 and n>=5 and c['max_extension']==n+1 and c['pair_vertices']==n*(n-1)
        S=set(c['designated_target']);records=verify(c)
        assert S=={0}|set(range(3,n-1,2))
        assert min(r['distance']+1 for (s,t),r in records.items() if s not in S and t in S)==n+1
        x,y=0,n-1
        for i in c['designated_word'][1:]:x,y=c['rows'][i][x],c['rows'][i][y]
        assert x not in S and y in S and len(c['designated_word'])==n+1
    for z in arrays:
        if z['n']>9:continue
        o=ordinary(z['rows']);assert o is not None;ordinary_count+=1
        for key in ['extension','best','worst','forward']:assert z[key]=={str(S):v for S,v in o[key].items()}
        assert len(o['forward'])==(1<<z['n'])-1 and max(o['extension'].values())==z['n']+1
    for sample in samples:
        c=sample['certificate']
        if c['n']<=4:
            o=ordinary(c['rows']);assert max(o['extension'].values())==c['max_extension'];ordinary_count+=1
    raw_covers=json.loads((ROOT/'small_covers.json').read_text());assert [c['n'] for c in raw_covers]==[2,3,4]
    covers=[verify_cover(c) for c in raw_covers]
    corruptions=[]
    for mode in range(6):
        c=copy.deepcopy(family[0])
        if mode==0:c['pairs'][0]['distance']=1
        elif mode==1:c['pairs'].pop()
        elif mode==2:c['max_extension']-=1
        elif mode==3:c['larger_preimage'].pop()
        elif mode==4:c['extension_word'].pop()
        else:c['target']=list(range(c['n']))
        try:verify(c)
        except (AssertionError,KeyError,ValueError):corruptions.append(mode)
        else:raise AssertionError('Accepted corruption '+str(mode))
    report=dict(verified=True,pair_records=paircount,certificates=len(family)+len(samples),ordinary_full_arrays=ordinary_count,
                covers=covers,corruptions_rejected=corruptions,minimum_scope='Every PU alphabet, n<=4; n5 violates e<=n; no minimum for unrestricted DFA.')
    (ROOT/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)

if __name__=='__main__':main()
