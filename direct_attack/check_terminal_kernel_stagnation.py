"""Direct word enumeration and ordinary-set audit of component stagnation."""
from collections import deque
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import json


def components(n,edges):
    blocks=[{q} for q in range(n)]
    for p,q in edges:
        first=next(s for s in blocks if p in s)
        second=next(s for s in blocks if q in s)
        if first is not second:
            blocks.remove(first);blocks.remove(second);blocks.append(first|second)
    return sorted([sorted(s) for s in blocks])


def check(z):
    rows=z['rows'];n=4
    assert rows==[[0,0,3,2],[2,0,1,3]]
    pairs=list(combinations(range(n),2));dist={};witness={}
    for length in range(1,6):
        for word in product(range(2),repeat=length):
            row=list(range(n))
            for a in word:row=[rows[a][q] for q in row]
            for pair in pairs:
                if pair not in dist and row[pair[0]]==row[pair[1]]:
                    dist[pair]=length;witness[pair]=list(word)
    assert [dist[p] for p in pairs]==z['pair_distances']==[1,3,4,2,4,5]
    layers=[]
    for b in range(1,6):
        edges=[p for p in pairs if dist[p]<=b]
        layers.append(dict(b=b,edges=[list(p) for p in edges],components=components(n,edges)))
    assert layers==z['layers']
    assert layers[1]['components']==layers[2]['components']!=layers[3]['components']
    seen={frozenset(range(n)):[]};todo=deque(seen)
    while todo:
        source=todo.popleft()
        for a,row in enumerate(rows):
            target=frozenset(row[q] for q in source)
            if target not in seen:seen[target]=seen[source]+[a];todo.append(target)
    rt=min(len(word) for S,word in seen.items() if len(S)==1)
    assert rt==z['rt']==7 and z['connectivity_threshold']==4
    word=z['reset_word'];image=set(range(n))
    for a in word:image={rows[a][q] for q in image}
    assert len(word)==rt and len(image)==1
    # Base SC, separately from synchronization.
    for start in range(n):
        reached={start};todo=deque([start])
        while todo:
            q=todo.popleft()
            for row in rows:
                if row[q] not in reached:reached.add(row[q]);todo.append(row[q])
        assert len(reached)==n
    return len(seen),witness


def main():
    rows=[[0,0,3,2],[2,0,1,3]];pairs=list(combinations(range(4),2));ds=[1,3,4,2,4,5]
    z=dict(rows=rows,pair_distances=ds,rt=7,reset_word=[0,1,1,0,1,1,0],connectivity_threshold=4,
           layers=[dict(b=b,edges=[list(p) for p,d in zip(pairs,ds) if d<=b],
                        components=components(4,[p for p,d in zip(pairs,ds) if d<=b])) for b in range(1,6)])
    vertices,words=check(z);corruptions=[]
    for field in ('pair_distances','layers','rt','reset_word'):
        bad=deepcopy(z)
        if field=='pair_distances':bad[field][2]=3
        elif field=='layers':bad[field][2]['components']=[[0,1,2,3]]
        elif field=='rt':bad[field]-=1
        else:bad[field][0]=1
        try:check(bad)
        except AssertionError:corruptions.append(field)
        else:raise AssertionError('accepted '+field)
    report=dict(verified=True,witness=z,pair_words={str(pair):w for pair,w in words.items()},
                actual_image_vertices=vertices,all_binary_words_through_length=5,
                corruptions_rejected=corruptions,
                state_minimum='four, established on paper for arbitrary synchronizing alphabets',
                scope='exact four-state witness; independent literal-word enumeration and subset closure; no general Cerny counterexample')
    Path('direct_attack/data/terminal_kernel_stagnation_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('witness','pair_words')}),flush=True)


if __name__=='__main__':main()
