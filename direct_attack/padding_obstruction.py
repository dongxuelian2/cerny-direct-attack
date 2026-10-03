"""An infinite reachable corank-two obstruction to a harmonic envelope."""
from collections import deque
import json
from pathlib import Path
from direct_attack.core import analyze, bfs, graph

BASE=[[6,7,1,3,0,5,4,2],[0,4,2,7,5,6,3,4]]

def word_to_subset(rows,start,target):
    g=graph(rows); queue=deque([start]); words={start:[]}
    while queue:
        s=queue.popleft()
        if s==target: return words[s]
        for a,t in enumerate(g[s]):
            if t not in words: words[t]=words[s]+[a]; queue.append(t)
    raise ValueError('unreachable target')

def word_to_state(rows,start,target):
    queue=deque([start]); words={start:[]}
    while queue:
        s=queue.popleft()
        if s==target: return words[s]
        for a,row in enumerate(rows):
            t=row[s]
            if t not in words: words[t]=words[s]+[a]; queue.append(t)
    raise ValueError('unreachable state')

def image(rows,s,word):
    for a in word: s={rows[a][q] for q in s}
    return s

def construct(n):
    assert n>=8 and (n-7)%3
    d=n-7; L=d if d%3==1 else 2*d
    rows=[BASE[0]+list(range(8,n)),BASE[1]+list(range(8,n))]
    if n>8:
        rows[0][3]=8
        for q in range(8,n-1): rows[0][q]=q+1
        rows[0][-1]=3
    def encode(word):
        return [x for a in word for x in ([0]*L if a==0 else [1])]
    p=analyze(BASE); target=next(iter(image(BASE,set(range(8)),p['word'])))
    base_to_zero=p['word']+word_to_state(BASE,target,0)
    V=encode(base_to_zero)
    reset=list(V); current=image(rows,set(range(n)),V)
    assert current=={0}|set(range(8,n))
    while len(current)>1:
        q=min(current-{0}); t=q; j=0
        while t!=3: t=rows[0][t]; j+=1
        phase=[0]*j+[1]+V
        previous=len(current); current=image(rows,current,phase)
        assert len(current)==previous-1 and 0 in current
        reset.extend(phase)
    reach=encode(word_to_subset(BASE,255,123))
    S={q for q in range(n) if q not in [2,7]}
    assert image(rows,set(range(n)),reach)==S
    compression=[0,0,1,0,0,1]
    assert len(image(rows,S,compression))==n-3
    return dict(schema='direct_attack.padding.v1',n=n,rows=rows,start=sorted(S),
                simulation_exponent=L,reach_word=reach,reset_word=reset,
                exact_compression=6,compression_word=compression,
                proposed_harmonic_bound=(3*n+n-4)//(n-3))

def main():
    out=Path('direct_attack/data/padding_obstruction'); out.mkdir(parents=True,exist_ok=True)
    records=[]
    for n in [8,9,11,12,14,15,17,18,20,30,60]:
        c=construct(n)
        (out/f'n{n}.json').write_text(json.dumps(c,separators=(',',':'))+'\n',encoding='utf-8')
        records.append(dict(n=n,exact_compression=6,proposed_bound=c['proposed_harmonic_bound'],
                            reach_length=len(c['reach_word']),reset_length=len(c['reset_word'])))
    (out/'summary.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(records),flush=True)

if __name__=='__main__': main()
