"""Lift a protected selected fixed point to a cycle of fully selected new states."""
from collections import deque
from itertools import combinations
import json
from math import gcd,lcm
from pathlib import Path

def apply(rows,S,word):
    for a in word:S={rows[a][q] for q in S}
    return S

def order(row):
    seen=set();M=1
    for q in range(len(row)):
        if q in seen:continue
        x=q;length=0
        while x not in seen:seen.add(x);x=row[x];length+=1
        M=lcm(M,length)
    return M

def state_word(rows,start,target):
    words={start:[]};queue=deque([start])
    while queue:
        q=queue.popleft()
        if q==target:return words[q]
        for a,row in enumerate(rows):
            t=row[q]
            if t not in words:words[t]=words[q]+[a];queue.append(t)
    raise ValueError('state unreachable')

def reset_word(c):
    n,rows=c['n'],c['rows'];pairs=list(combinations(range(n),2));d=dict(zip(pairs,c['pair_potential'][1:]))
    current=set(range(n));word=[]
    while len(current)>1:
        pair=min(combinations(sorted(current),2),key=lambda p:d[p]);w=[]
        while len(pair)>1:
            cost=d[pair]
            for a,row in enumerate(rows):
                target=tuple(sorted(set(row[q] for q in pair)))
                if (0 if len(target)==1 else d[target])==cost-1:
                    w.append(a);pair=target;break
            else:raise AssertionError('missing pair descent')
        current=apply(rows,current,w);word+=w
    p=c['port'];z=next(q for q in range(n) if q!=p)
    word+=state_word(rows,next(iter(current)),z)
    assert apply(rows,set(range(n)),word)=={z}
    return word,z

def lift(c,extra):
    n0,p=c['n'],c['port'];d=extra+1;M=order(c['rows'][0]);assert gcd(d,M)==1
    n=n0+extra;L=d*(pow(d,-1,M) if M>1 else 1)
    rows=[list(row)+list(range(n0,n)) for row in c['rows']]
    if extra:
        rows[0][p]=n0
        for q in range(n0,n-1):rows[0][q]=q+1
        rows[0][-1]=p
    def encode(word):return [x for a in word for x in ([0]*L if a==0 else [1])]
    W,z=reset_word(c);V=encode(W);word=list(V);current=apply(rows,set(range(n)),V)
    assert current=={z}|set(range(n0,n))
    while len(current)>1:
        q=min(current-{z});j=0
        while q!=p:q=rows[0][q];j+=1
        phase=[0]*j+[1]+V;previous=len(current);current=apply(rows,current,phase)
        assert len(current)==previous-1 and z in current;word+=phase
    S=set(range(n))-set(c['holes']);reach=encode(c['reach_word'])
    assert apply(rows,set(range(n)),reach)==S
    cw=c['compression_word'];assert len(apply(rows,S,cw))<len(S)
    return dict(schema='direct_attack.cycle-insertion.v1',base_n=n0,n=n,port=p,extra=extra,
                old_permutation_order=M,simulation_exponent=L,rows=rows,start=sorted(S),
                exact_compression=c['exact_compression'],compression_word=cw,
                reach_word=reach,reset_word=word,reset_target=z)

def main():
    c=json.loads(Path('direct_attack/data/near_full_n12_r3/protected_witness.json').read_text())
    out=Path('direct_attack/data/cycle_insertion');out.mkdir(parents=True,exist_ok=True);records=[]
    M=order(c['rows'][0])
    for extra in [0,4,6,10,16,22,34,46]:
        assert gcd(extra+1,M)==1
        x=lift(c,extra)
        (out/f'n{x["n"]}.json').write_text(json.dumps(x,separators=(',',':'))+'\n',encoding='utf-8')
        records.append(dict(n=x['n'],exact_compression=x['exact_compression'],
            reset_length=len(x['reset_word']),reach_length=len(x['reach_word']),
            harmonic_coefficient_lower=x['exact_compression']*(x['n']-4)/(4*x['n'])))
    (out/'summary.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8');print(json.dumps(records))

if __name__=='__main__':main()
