"""Independent original-label and decreasing-cycle-distance certificate audit."""
from collections import deque
from copy import deepcopy
from itertools import permutations
import json
from pathlib import Path

def act(rows,w,q):
    for i in w:assert type(i) is int and 0<=i<len(rows);q=rows[i][q]
    return q

def pre(rows,w,U):return {q for q in range(len(rows[0])) if act(rows,w,q) in U}

def strongly_connected(rows):
    n=len(rows[0]);adj=[set(f[q] for f in rows) for q in range(n)];back=[set() for _ in range(n)]
    for q in range(n):
        for p in adj[q]:back[p].add(q)
    for edges in (adj,back):
        seen={0};todo=[0]
        for q in todo:
            for p in edges[q]:
                if p not in seen:seen.add(p);todo.append(p)
        if len(seen)!=n:return False
    return True

def geometry(rows):
    n=len(rows[0]);b=rows[1];remaining=set(range(n));C=[]
    while remaining:
        q=min(remaining);orbit=[];p=q
        while p not in orbit:orbit.append(p);p=b[p]
        assert p==q;remaining-=set(orbit);C.append(set(orbit))
    index={q:i for i,Z in enumerate(C) for q in Z};root=index[0];adj=[set() for _ in C]
    for f in rows:
        for q,p in enumerate(f):adj[index[q]].add(index[p])
    d=[None]*len(C);d[root]=0;todo=deque([root])
    while todo:
        I=todo.popleft()
        for J in sorted(adj[I]):
            if d[J] is None:d[J]=d[I]+1;todo.append(J)
    return C,index,root,d

def hypotheses(rows,C,root):
    n=len(rows[0]);assert n>=2 and len(rows)>=2 and rows[1][0]==1 and sorted(rows[1])==list(range(n))
    R=C[root];singular=[]
    for i,f in enumerate(rows):
        assert len(f)==n and all(type(q) is int and 0<=q<n for q in f)
        if len(set(f))==n:assert {f[q] for q in R}==R
        else:
            assert f[0]==f[1]==1 and sorted(f[1:])==list(range(1,n))
            singular.append(i)
    assert 0 in singular
    return singular

def extension(rows,e,C,index,root,d):
    n=len(rows[0]);U={q for q in range(n) if e['U']>>q&1};original=set(U);R=C[root];assert 0<len(U)<n
    trace=e['trace'];word=[];chosen=set();paid=0;letters=0;last=None
    for t in trace:
        assert len(U&R) in (0,len(R));value=bool(U&R)
        targets=[J for J,Z in enumerate(C) if any((q in U)!=value for q in Z)]
        minimum=min(d[J] for J in targets);J=t['cycle'];assert J in targets and d[J]==minimum>0
        assert J not in chosen;chosen.add(J)
        if last is not None:assert minimum<last
        last=minimum
        letter,x,y,k=t['letter'],t['x'],t['y'],t['rotation']
        assert t['distance']==minimum and rows[letter][x]==y and index[y]==J and d[index[x]]==minimum-1
        assert 0<=k<len(C[J]) and (x in U)==value
        assert (act(rows,[1]*k,y) in U)!=value
        block=[letter]+[1]*k;new=pre(rows,block,U);letters+=n*len(block)
        assert len(new)==len(U) and (x in new)!=value
        assert (0 in new)==(1 in new)==value
        U=new;word=block+word;paid+=len(block)
        if len(U&R) in (0,len(R)):
            assert bool(U&R)==value
            now=min(d[J] for J,Z in enumerate(C) if any((q in U)!=value for q in Z));assert now<minimum
    assert paid<=sum(len(C[J]) for J in chosen)<=n-len(R)
    assert 0<len(U&R)<len(R)
    k=e['growth_rotation'];assert 0<=k<len(R)
    assert act(rows,[1]*k,0) not in U and act(rows,[1]*k,1) in U
    block=[0]+[1]*k;new=pre(rows,block,U);letters+=n*len(block);word=block+word
    assert len(new)==len(original)+1 and e['word']==word and len(word)<=n
    assert pre(rows,word,original)==new;letters+=n*len(word)
    return letters,len(trace),paid,len(word)

def counter_check(z):
    rows=z['rows'];assert rows==[[2,2,1,3],[1,3,2,0]] and z['U']==11
    assert strongly_connected(rows) and rows[0][1]!=1
    d=z['distances'];assert len(d)==16 and d[15]==0;edges=0
    for S,value in enumerate(d):
        assert value is None or type(value) is int and value>=0
        if S==15:continue
        choices=[]
        U={q for q in range(4) if S>>q&1}
        for i in range(2):
            T=sum(1<<q for q in pre(rows,[i],U));edges+=1
            if d[T] is not None:choices.append(1+d[T])
        assert value==(min(choices) if choices else None)
    assert d[11]==6 and len(z['word'])==6 and pre(rows,z['word'],{0,1,3})==set(range(4))
    return edges

def check(data):
    records=data['records'];assert len(records)==219;complete={n:set() for n in range(2,6)}
    controls=letters=sync=depth=singinputs=0;rootfull=rootempty=mixed=0;multicycle=0
    for z in records:
        rows=z['rows'];n=len(rows[0]);C,index,root,d=geometry(rows);hypotheses(rows,C,root)
        if z['mode']=='complete binary n2..5':
            assert n in complete and len(rows)==2;key=tuple(tuple(f) for f in rows);assert key not in complete[n];complete[n].add(key)
        good=strongly_connected(rows);assert z['SC']==good
        if not good:assert 'extensions' not in z;continue
        assert all(v is not None for v in d);sync+=1
        if len(C)>1:multicycle+=1
        if len(rows)>2:singinputs+=1
        extensions=z['extensions'];masks=[e['U'] for e in extensions];assert len(masks)==len(set(masks))
        if n<=10:assert masks==list(range(1,(1<<n)-1)) and z['subset_scope']=='ALL nonempty proper subsets'
        else:assert z['subset_scope'].startswith('retained deterministic sampled')
        for e in extensions:
            assert 0<e['U']<(1<<n)-1
            U={q for q in range(n) if e['U']>>q&1};p=len(U&C[root])
            rootempty+=p==0;rootfull+=p==len(C[root]);mixed+=0<p<len(C[root])
            work,h,paid,cost=extension(rows,e,C,index,root,d);letters+=work;depth=max(depth,h);controls+=1
        factors=z['reset_factors'];assert len(factors)==n-1 and factors[0]==[0]
        U={1};word=[]
        for j,w in enumerate(factors):
            if j==0:assert w==[0]
            else:assert 0<len(w)<=n
            U=pre(rows,w,U);word=w+word;assert len(U)==j+2;letters+=n*len(w)
        assert U==set(range(n)) and z['reset_word']==word and len(word)<=(n-1)**2
        assert len({act(rows,word,q) for q in range(n)})==1;letters+=n*len(word)
    for n,seen in complete.items():
        expected={(tuple([1,1]+list(tail)),tuple([1]+list(rem))) for tail in permutations(range(2,n)) for rem in permutations([q for q in range(n) if q!=1])}
        assert seen==expected
    edges=counter_check(data['counter'])
    return dict(verified=True,inputs=len(records),complete_binary_inputs=sum(len(v) for v in complete.values()),SC_inputs=sync,
                multicycle_permutation_inputs=multicycle,multiple_letter_inputs=singinputs,subset_controls=controls,
                root_empty_controls=rootempty,root_full_controls=rootfull,root_mixed_controls=mixed,max_paid_preparation_depth=depth,
                literal_particle_letter_controls=letters,counter_bellman_edges=edges,counter_min_extension=6,
                boundary='Independent complete binary n2..5 coverage, original-label witnesses for ALL proper subsets of retained n<=10 inputs, sampled larger/multiple-letter controls, strict cycle-distance descent and distinct-cycle cost budget, compatible full reset expansions. Paper arbitrary-n theorem separately PROVED, not FORMALLY VERIFIED or a novelty claim. Dropping fixed-root n-extensibility REFUTED at n4. General Cerny OPEN.')

def main():
    data=json.loads(Path('direct_attack/data/fixed_root_cycle_extension.json').read_text());out=check(data);rejected=[]
    for mode in range(8):
        bad=deepcopy(data);z=bad['records'][0]
        if mode==0:z['rows'][0][1]=0
        if mode==1:z['rows'][1][0]=0
        if mode==2:z['extensions'][0]['word'].pop()
        if mode==3:z['extensions'][0]['growth_rotation']=0
        if mode==4:z['reset_word'].pop()
        if mode==5:bad['records'].pop()
        if mode==6:bad['counter']['distances'][11]=4
        if mode==7:z['SC']=False
        try:check(bad)
        except (AssertionError,KeyError,ValueError,TypeError):rejected.append(mode)
        else:raise AssertionError('corruption accepted')
    out['corruptions_rejected']=rejected
    Path('direct_attack/data/fixed_root_cycle_extension_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
