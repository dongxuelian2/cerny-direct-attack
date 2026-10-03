"""Ordinary-set Bellman dual + predecessor primal certificate, without Dijkstra."""
from collections import deque
import json
from pathlib import Path
import time


def verify(c):
    n=c['n'];rows=c['rows'];Q=frozenset(range(n));R=[Q];seen={Q};edges={}
    for S in R:
        children=[]
        for row in rows:
            T=frozenset(row[q] for q in S);children.append(T)
            if T not in seen:seen.add(T);R.append(T)
        edges[S]=children
    mask=lambda S:sum(1<<q for q in S)
    values={S:c['nodes'][str(mask(S))] for S in R}
    assert set(c['nodes'])=={str(mask(S)) for S in R}
    r=max(len(S) for S in R if S!=Q);assert r==c['r'] and len(R)==c['reachable']
    weight=lambda S:max(0,r-max(2,len(S))+1)
    assert values[Q]==dict(area=0,length=0,parent=None)
    for S in R:
        v=values[S];assert type(v['area'])==type(v['length'])==int and v['area']>=0 and v['length']>=0
        for T in edges[S]:
            u=values[T];assert (u['area'],u['length'])<=(v['area']+weight(T),v['length']+1)
        if S!=Q:
            pm,x=v['parent'];P=frozenset(q for q in range(n) if pm>>q&1)
            assert type(pm)==int and 0<pm<(1<<n) and type(x)==int
            assert P in seen and 0<=x<len(rows) and edges[P][x]==S
            assert v['area']==values[P]['area']+weight(S) and v['length']==values[P]['length']+1
    optimum=min((values[S]['area'],values[S]['length']) for S in R if len(S)==1)
    assert optimum==(c['area'],c['length'])
    S=Q;area=0
    for x in c['word']:
        assert type(x)==int and 0<=x<len(rows)
        S=edges[S][x];area+=weight(S)
    assert len(S)==1 and area==c['area'] and len(c['word'])==c['length']
    assert c['budget']==2+(r-1)*n-r*(r+1)//2+area
    # Independent ordinary reverse BFS: every k-subset's true reset distance.
    rev={S:[] for S in R}
    for S in R:
        for T in edges[S]:rev[T].append(S)
    d={S:0 for S in R if len(S)==1};queue=deque(d)
    while queue:
        S=queue.popleft()
        for T in rev[S]:
            if T not in d:d[T]=d[S]+1;queue.append(T)
    assert len(d)==len(R)
    assert rows==[[(q+1)%n for q in range(n)],list(range(n-1))+[0]]
    for S in R:
        if len(S)>=2:assert d[S]>=(len(S)-2)*n+1
    assert d[Q]==(n-1)**2 and len(R)==(1<<n)-1
    assert c['area']==(n-2)*(n*(n-1)//2+1) # finite formula, not an arbitrary-n theorem
    lower=(n-2)*(n*(n-3)//2+2);assert lower<=c['area']
    if n>=3:assert c['budget']>(n-1)**2
    else:assert c['budget']==1
    return dict(n=n,vertices=len(R),edges=len(R)*len(rows),area=area,budget=c['budget'],rt=d[Q])


def main():
    started=time.monotonic();root=Path('direct_attack/data/circular_rank_area');records=[]
    for r in json.loads((root/'summary.json').read_text())['records']:records.append(verify(json.loads((root/r['file']).read_text())))
    c=json.loads((root/'n6.json').read_text());rejected=[]
    for key in ['potential','parent','word','parent_high_bit','negative_word_token']:
        d=json.loads(json.dumps(c))
        if key=='potential':d['nodes']['1']['area']+=1
        elif key=='parent':d['nodes']['1']['parent'][0]=0
        elif key=='word':d['word']=d['word'][:-1]
        elif key=='parent_high_bit':d['nodes']['1']['parent'][0]|=1<<c['n']
        else:d['word'][-1]=-1
        try:verify(d)
        except (AssertionError,KeyError):rejected.append(key)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,records=records,vertices=sum(r['vertices'] for r in records),edges=sum(r['edges'] for r in records),
                corruptions_rejected=rejected,seconds=time.monotonic()-started,
                scope='Every forward area/secondary-length entry verified by ordinary-set Bellman inequalities and acyclic attaining predecessors. Reset word attains minimum over ALL words. Ordinary reverse BFS checks EVERY subset reset-distance lower bound. Exact minimum-area polynomial only finite n2..14; paper separately proves all-n cubic barrier.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(vertices=report['vertices'],edges=report['edges'],cases=len(records),corruptions_rejected=rejected,seconds=report['seconds'])),flush=True)


if __name__=='__main__':main()
