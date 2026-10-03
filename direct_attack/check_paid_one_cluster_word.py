"""Independent literal checker; imports no research generator or solver."""
from collections import deque
from copy import deepcopy
import json
from pathlib import Path

def run(rows,word,q):
    for letter in word:
        assert type(letter) is int and 0<=letter<len(rows)
        q=rows[letter][q]
    return q

def graph(f):
    n=len(f);indegree=[0]*n
    for x in f:indegree[x]+=1
    todo=deque(q for q in range(n) if not indegree[q]);cyclic=set(range(n))
    while todo:
        q=todo.popleft();cyclic.remove(q);p=f[q];indegree[p]-=1
        if not indegree[p]:todo.append(p)
    cycles=[];unread=set(cyclic)
    while unread:
        q=min(unread);C=[];p=q
        while p not in C:C.append(p);unread.remove(p);p=f[p]
        assert p==q;cycles.append(sorted(C))
    ell=0
    for q in range(n):
        steps=0
        while q not in cyclic:q=f[q];steps+=1;assert steps<n
        ell=max(ell,steps)
    return sorted(cycles),ell

def limits(n,s,m,ell):
    if m==1:return None,None,s*ell
    t=n-m;h=(t+ell-1)//ell if ell else 0
    E=max((r+1)+s*(m+min(t,ell*r)-r-1) for r in range(n-1))
    assert E==s*(n-1)+1-(s-1)*h
    B=t+1+2*s*ell+(m-2)*(E+s*ell)
    assert B==s*((m-1)*(n-1)+m*ell)-(s-1)*(n-1+(m-2)*h)
    return h,E,B

def inverse(rows,w,S):return sum(1<<q for q in range(len(rows[0])) if S>>run(rows,w,q)&1)

def distances(rows):
    n=len(rows[0]);reverse=[[] for _ in range(1<<n)]
    for S in range(1<<n):
        for f in rows:
            T=0
            for q in range(n):
                if S>>q&1:T|=1<<f[q]
            reverse[T].append(S)
    d=[None]*(1<<n);todo=deque()
    for S in range(1<<n):
        if S.bit_count()<=1:d[S]=0;todo.append(S)
    while todo:
        T=todo.popleft()
        for S in reverse[T]:
            if d[S] is None:d[S]=d[T]+1;todo.append(S)
    return d

def check(data):
    assert len(data['cases'])==293 and len(data['obstructions'])==2
    extension_count=state_letters=macro_controls=0;qualifying=all_multi=0
    for z in data['cases']:
        rows=z['rows'];n=len(rows[0]);assert n>=2 and all(len(f)==n and all(type(x) is int and 0<=x<n for x in f) for f in rows)
        v=z['v'];assert v;s=len(v);f=[run(rows,v,q) for q in range(n)];macro_controls+=n*s
        assert f==z['macro_row'];cycles,ell=graph(f);assert len(cycles)==1
        C=sum(1<<q for q in cycles[0]);m=len(cycles[0]);assert cycles[0]==z['cycle'] and m==z['m'] and ell==z['ell']
        h,E,B=limits(n,s,m,ell);assert (h,E,B)==(z['h'],z['E'],z['B'])
        suffix=v*ell;entries={}
        for e in z['extensions']:
            S=e['S'];assert S not in entries and S and S&C==S and S!=C
            assert len(e['prefix'])<=E
            w=e['prefix']+suffix;T=inverse(rows,w,S)&C;state_letters+=n*len(w)
            assert T==e['T'] and T.bit_count()>S.bit_count();entries[S]=e;extension_count+=1
        if m==1:assert not entries and z['initial'] is None;expected_reset=suffix
        else:
            assert set(entries)=={S for S in range(1,1<<n) if S&C==S and S!=C}
            initial=z['initial'];q=initial['q'];assert q in cycles[0]
            assert len(initial['prefix'])<=n-m+1 and initial['S']==1<<q
            assert initial['T']==inverse(rows,initial['prefix']+suffix,1<<q)&C
            assert initial['T'].bit_count()>=2
            for key in ('S','prefix','T'):assert initial[key]==entries[1<<q][key]
            word=initial['prefix']+suffix;S=initial['T'];chain=initial['extension_chain'];assert len(chain)<=m-2
            for oldS in chain:
                assert oldS==S and S!=C;e=entries[S];word=e['prefix']+suffix+word;S=e['T']
            assert S==C;expected_reset=suffix+word
        assert expected_reset==z['reset'] and len(expected_reset)<=B
        assert len({run(rows,expected_reset,q) for q in range(n)})==1
        state_letters+=n*len(expected_reset)
        qualifying+=B<=(n-1)**2
        all_multi+=all(len(graph(f)[0])>=2 for f in rows)
    short_words=0;thresholds=[]
    for z in data['obstructions']:
        rows=z['rows'];n=len(rows[0]);square=(n-1)**2;cap=square//2;assert z['cap']==cap
        assert all(len(graph(f)[0])>1 for f in rows)
        for start in range(n):
            reach={start};todo=[start]
            for q in todo:
                for f in rows:
                    if f[q] not in reach:reach.add(f[q]);todo.append(f[q])
            assert len(reach)==n
        lookup={tuple(e['word']):e for e in z['all_short_words']};assert len(lookup)==len(z['all_short_words'])==2**(cap+1)-1
        todo=[()];best=None
        for w in todo:
            assert w in lookup;e=lookup[w];f=[run(rows,w,q) for q in range(n)];state_letters+=n*len(w)
            cycles,ell=graph(f);assert f==e['row'] and cycles==sorted(e['cycles']) and ell==e['ell']
            if len(cycles)==1 and len(set(f))>1:
                m=len(cycles[0]);B=limits(n,len(w),m,ell)[2];assert B==e['B'] and B>square
                item=dict(B=B,word=list(w),m=m,ell=ell)
                if best is None or (B,list(w))<(best['B'],best['word']):best=item
            else:assert 'B' not in e
            if len(w)<cap:todo.extend([w+(0,),w+(1,)])
        assert best==z['best'];short_words+=len(todo)
        # Check the algebra giving the universal long-word cutoff, for all
        # possible one-cycle parameters at these n, not just observed rows.
        for m in range(1,n+1):
            for ell in range(n-m+1):
                if (m==n)!=(ell==0):continue
                if m==1:
                    if ell<2:continue
                    assert (cap+1)*ell>square
                else:
                    if ell:
                        h=(n-m+ell-1)//ell;D=(m-2)*(n-1-h)+m*ell
                    else:D=(n-1)*(n-2)
                    assert D>=2 and limits(n,cap+1,m,ell)[2]>square
        d=distances(rows);rt=d[-1];assert rt==len(z['reset']) and rt in (8,13)
        assert len({run(rows,z['reset'],q) for q in range(n)})==1
        thresholds.append(dict(n=n,rt=rt,best_short_formula=best['B'],all_subset_distances=d))
    return dict(verified=True,cases=len(data['cases']),cycle_extensions=extension_count,macro_state_letter_controls=macro_controls,
                literal_state_letter_controls=state_letters,obstruction_words=short_words,qualifying_formula_cases=qualifying,
                cases_with_every_original_letter_multicycle=all_multi,thresholds=thresholds,
                boundary='Independent finite original-word macro, ALL cycle-subset paid extensions, literal common reset controls and ALL short-word bridge obstructions at n4/n5. Paper all-parameter conditional refinement not formal. This refutes the worst-case NONCONSTANT FORMULA bridge only, not all one-cluster-word strategies. General Cerny OPEN.')

def main():
    data=json.loads(Path('direct_attack/data/paid_one_cluster_word.json').read_text());out=check(data);rejected=[]
    for mode in range(8):
        bad=deepcopy(data);z=bad['cases'][0]
        if mode==0:z['v']=[]
        if mode==1:z['macro_row'][0]=(z['macro_row'][0]+1)%len(z['macro_row'])
        if mode==2:z['ell']+=1
        if mode==3:z['E']+=1
        if mode==4:z['extensions'][0]['prefix']=[]
        if mode==5:z['reset']=[]
        if mode==6:bad['obstructions'][0]['all_short_words'].pop()
        if mode==7:bad['obstructions'][1]['reset'].pop()
        try:check(bad)
        except (AssertionError,KeyError,ValueError):rejected.append(mode)
        else:raise AssertionError('corruption accepted')
    out['corruptions_rejected']=rejected
    Path('direct_attack/data/paid_one_cluster_word_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='thresholds'}),flush=True)

if __name__=='__main__':main()
