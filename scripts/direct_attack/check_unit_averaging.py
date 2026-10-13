"""Independent exact matrix averaging and graph/word/ordinary-array checks."""
from math import prod,lcm
import json
from pathlib import Path
import time
from direct_attack.ordinary_reverse_policy import profile

ROOT=Path('scripts/direct_attack/data/unit_averaging')

def reachability(n,arcs):
    # Independent all-source closure, not the generator's two DFS tests.
    graph=[[] for _ in range(n)]
    for s,t in arcs:graph[s].append(t)
    reach=[]
    for start in range(n):
        seen={start};queue=[start]
        for s in queue:
            for t in graph[s]:
                if t not in seen:seen.add(t);queue.append(t)
        reach.append(seen)
    return reach

def polynomial(c):
    lengths=c['lengths'];n=sum(lengths);coeff=c['coefficients'];K=prod(lengths)
    assert c['n']==n and c['degree']==n-len(lengths)==len(coeff)-1
    assert all(type(x)==int and x>0 for x in coeff) and coeff[0]==coeff[-1]==1 and sum(coeff)==K
    assert c['order']==lcm(*lengths)
    offset=0
    for L in lengths:
        # Independently enumerate basis entries p(B) rather than re-multiply factors.
        for source in range(L):
            counts=[0]*L
            for j,weight in enumerate(coeff):counts[(source+j)%L]+=weight
            assert counts==[K//L]*L and K%L==0
        offset+=L
    assert offset==n

def verify(c,ordinary=True):
    rows=c['rows'];n=len(rows[0]);a=rows[0];assert sorted(a)==list(range(n))
    cycles=[];seen=set()
    for q in range(n):
        if q in seen:continue
        C=[];s=q
        while s not in seen:seen.add(s);C.append(s);s=a[s]
        assert s==q;cycles.append(C)
    assert list(map(len,cycles))==c['lengths'];d=n-len(cycles);assert c['bound']==d+1
    arcs=[]
    for row in rows[1:]:
        changes=[q for q in range(n) if row[q]!=q];assert len(changes)==1
        s=changes[0];arcs.append((s,row[s]))
    full=set()
    for source,target in arcs:
        s,t=source,target
        while (s,t) not in full:full.add((s,t));s,t=a[s],a[t]
    sync=all(len(R)==n for R in reachability(n,full));assert c['synchronizing']==sync
    if not sync:assert c['max_extension'] is None;return False
    prefix=set();current=arcs[:];threshold=None;previous=None
    for j in range(d+1):
        previous=reachability(n,prefix);prefix.update(current)
        if all(len(R)==n for R in reachability(n,prefix)):threshold=j+1;break
        current=[(a[s],a[t]) for s,t in current]
    assert threshold==c['max_extension'] and threshold<=d+1
    # A proper forward-closed set at the preceding prefix gives a maximal-delay
    # non-growth witness by complementing it: no outside-to-inside edge.
    closed=next(R for R in previous if len(R)<n);S=set(range(n))-closed;assert S and len(S)<n
    image=set(S)
    for j in range(threshold):
        grows=[x for x,row in enumerate(rows[1:],1) if len({q for q in range(n) if row[q] in image})>len(S)]
        assert bool(grows)==(j==threshold-1)
        image={q for q in range(n) if a[q] in image}
    if ordinary and n<=8:
        p=profile(rows);assert p is not None and len(p['forward'])==(1<<n)-1
        assert max(p['extension'].values())==threshold
        assert p['best']==p['worst']==p['forward']
        assert min(p['forward'][1<<q] for q in range(n))<=1+(n-2)*(d+1)
    word=c['reset_word'];phases=c['phases_inverse_order'];assert word==[x for phase in reversed(phases) for x in phase]
    S={c['target']}
    for phase in phases:
        assert 1<=len(phase)<=d+1;before=len(S)
        for x in reversed(phase):
            assert 0<=x<len(rows);S={q for q in range(n) if rows[x][q] in S}
        assert len(S)==before+1
    assert S==set(range(n)) and len(phases)==n-1 and len(phases[0])==1
    assert len(word)<=1+(n-2)*(d+1)<=(n-1)**2
    S=set(range(n))
    for x in word:S={rows[x][q] for q in S}
    assert S=={c['target']}
    return True

def main():
    started=time.monotonic();polys=json.loads((ROOT/'polynomials.json').read_text());models=json.loads((ROOT/'models.json').read_text())
    for c in polys:polynomial(c)
    sync=sum(verify(c) for c in models);small=sum(c['synchronizing'] and len(c['rows'][0])<=8 for c in models)
    # Full previously retained single-permutation alphabets, not just the model family.
    samples=json.loads(Path('scripts/direct_attack/data/permutation_units/samples.json').read_text())
    summary=json.loads(Path('scripts/direct_attack/data/permutation_units/summary.json').read_text());indices={i for r in summary if r['kind']=='single' for i in r['samples']}
    for i in indices:
        c=samples[i];n=c['n'];a=c['rows'][0];visited=set();cycles=0
        for q in range(n):
            if q in visited:continue
            cycles+=1
            while q not in visited:visited.add(q);q=a[q]
        assert c['max_extension']<=n-cycles+1 and c['rt']<=1+(n-2)*(n-cycles+1)
    rejected=[]
    good=next(c for c in models if sum(c['lengths'])==6 and c['synchronizing'])
    for key in ['bound','max_extension','reset_word','phases_inverse_order']:
        bad=json.loads(json.dumps(good))
        if key in ['bound','max_extension']:bad[key]+=1
        elif key=='reset_word':bad[key]=bad[key][:-1]
        else:bad[key][0]=[999]
        try:verify(bad,False)
        except AssertionError:rejected.append(key)
        else:raise AssertionError('Corruption accepted')
    bad=json.loads(json.dumps(next(c for c in polys if c['lengths']==[2,3])))
    bad['coefficients'][1]+=1
    try:polynomial(bad)
    except AssertionError:rejected.append('coefficients')
    else:raise AssertionError('Bad polynomial accepted')
    report=dict(verified=True,polynomials=len(polys),models=len(models),sync=sync,ordinary_all_arrays=small,
                previous_single_alphabet_samples=len(indices),corruptions_rejected=rejected,seconds=time.monotonic()-started,
                scope='Every operator entry by independent basis counting; every model prefix graph by ALL-SOURCE closure with a preceding non-growth witness, every explicit inverse phase and reset word; ordinary full arrays n<=8. All-n statements follow the paper proof, not finite extrapolation.')
    assert len(polys)==json.loads((ROOT/'summary.json').read_text())['polynomials']
    (ROOT/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)

if __name__=='__main__':main()
