"""Finite original-word controls of the paid one-cluster theorem."""
from collections import deque
from itertools import product
import json
from pathlib import Path

def action(rows,w):
    f=list(range(len(rows[0])))
    for letter in w:f=[rows[letter][q] for q in f]
    return f

def profile(f):
    cycles=[];ell=0
    for q in range(len(f)):
        path=[];x=q
        while x not in path:path.append(x);x=f[x]
        j=path.index(x);C=frozenset(path[j:]);ell=max(ell,j)
        if C not in cycles:cycles.append(C)
    return cycles,ell

def budget(n,s,m,ell):
    if m==1:return None,None,s*ell
    t=n-m;h=(t+ell-1)//ell if ell else 0
    E=s*(n-1)+1-(s-1)*h
    B=t+1+m*s*ell+(m-2)*E
    assert E==1+s*(m-1)+max(s*min(t,ell*r)-(s-1)*r for r in range(n-1))
    return h,E,B

def pre(S,f):return sum(1<<q for q,p in enumerate(f) if S>>p&1)

def extension(rows,C,S,suffix):
    terminal=action(rows,suffix);start=pre(S,terminal)
    seen={start:()};todo=deque([start])
    while todo:
        T=todo.popleft();w=seen[T]
        if (T&C).bit_count()>S.bit_count():return dict(S=S,prefix=list(w),T=T&C)
        for letter,f in enumerate(rows):
            U=pre(T,f)
            if U not in seen:seen[U]=(letter,)+w;todo.append(U)
    raise AssertionError('synchronizing original alphabet must extend')

def certificate(rows,v):
    n=len(rows[0]);f=action(rows,v);cycles,ell=profile(f);assert len(cycles)==1
    cycle=sorted(cycles[0]);C=sum(1<<q for q in cycle);m=len(cycle);s=len(v)
    h,E,B=budget(n,s,m,ell);suffix=v*ell;extensions=[];initial=None
    if m==1:reset=suffix
    else:
        for S in range(1,1<<n):
            if S&C!=S or S==C:continue
            z=extension(rows,C,S,suffix);assert len(z['prefix'])<=E;extensions.append(z)
        for q in cycle:
            z=next(z for z in extensions if z['S']==1<<q)
            if initial is None or (len(z['prefix']),q)<(len(initial['prefix']),initial['q']):initial=dict(q=q,**z)
        assert len(initial['prefix'])<=n-m+1
        word=initial['prefix']+suffix;S=initial['T'];factors=[]
        while S!=C:
            z=next(z for z in extensions if z['S']==S);factor=z['prefix']+suffix;factors.append(z['S']);word=factor+word;S=z['T']
        reset=suffix+word
        initial['extension_chain']=factors
    assert len(set(action(rows,reset)))==1 and len(reset)<=B
    return dict(rows=rows,v=v,macro_row=f,cycle=cycle,m=m,ell=ell,h=h,E=E,B=B,extensions=extensions,initial=initial,reset=reset)

def bases():
    old=json.loads(Path('scripts/direct_attack/data/one_cluster_annular_controls.json').read_text())
    for c in old['cases']:yield 'fixed_seed/'+str(c['case']),c['rows']
    yield 'bridge_n4',[[0,2,1,1],[2,1,3,0]]
    yield 'bridge_n5',[[0,0,1,3,4],[3,1,3,4,2]]
    yield 'old_rooted_n4',[[0,0,1,3],[3,1,3,2]]
    for n in range(2,10):yield 'circular/'+str(n),[list(range(1,n))+[0],list(range(n-1))+[0]]

def macros(rows):
    selected={};seen=set()
    for length in range(1,5):
        for w in product(range(len(rows)),repeat=length):
            v=list(w);f=action(rows,v)
            if tuple(f) in seen:continue
            seen.add(tuple(f));cycles,ell=profile(f)
            if len(cycles)!=1:continue
            key=(len(cycles[0]),ell,length)
            if key not in selected:selected[key]=v
    return list(selected.values())

def obstruction(rows,known_reset):
    n=len(rows[0]);cap=(n-1)**2//2;words=[];best=None
    for length in range(cap+1):
        for w in product(range(len(rows)),repeat=length):
            f=action(rows,w);cs,ell=profile(f);record=dict(word=list(w),row=f,cycles=[sorted(C) for C in cs],ell=ell)
            if len(cs)==1 and len(set(f))>1:
                m=len(cs[0]);B=budget(n,length,m,ell)[2];record['B']=B
                assert B>(n-1)**2
                if best is None or (B,list(w))<(best['B'],best['word']):best=dict(B=B,word=list(w),m=m,ell=ell)
            words.append(record)
    assert len(set(action(rows,known_reset)))==1
    return dict(rows=rows,cap=cap,all_short_words=words,best=best,reset=known_reset)

def main():
    records=[]
    for label,rows in bases():
        for v in macros(rows):
            z=certificate(rows,v);z['source']=label;records.append(z)
    # The n5 witness is longer than the default macro selection range.
    z=certificate([[0,0,1,3,4],[3,1,3,4,2]],[0,0,1,0,1,0,0]);z['source']='bridge_n5/best';records.append(z)
    boundaries=[obstruction([[0,2,1,1],[2,1,3,0]],[0,1,0,1,1,0,1,0]),
                obstruction([[0,0,1,3,4],[3,1,3,4,2]],[0,0,1,0,1,0,0,1,0,1,1,0,0])]
    out=dict(cases=records,obstructions=boundaries,boundary='Finite actual original-word macro controls only. Paper conditional cost refinement PROVED separately, no novelty or formal verification; worst-case NONCONSTANT formula bridge refuted at n4/n5, general Cerny OPEN.')
    Path('scripts/direct_attack/data/paid_one_cluster_word.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),cycle_extensions=sum(len(z['extensions']) for z in records),obstruction_words=sum(len(z['all_short_words']) for z in boundaries),boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
