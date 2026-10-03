"""Layer-entry lower certificates for the completed published family."""
import argparse
from collections import deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from .compress_other_family import transitions


def digest(value):return sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def categories(pair,p):
    x,y=pair
    if y<=2*p:
        J=(x+y)%2==1 and x+y>2*p+1;C=(x+y)%2==1 and x+y==2*p+1
        return dict(badJ=J and pair!=(3,2*p),C=C,H=False,U=False,costC=2*p-2+abs(x-3) if C else None,costH=None)
    if x>2*p:return dict(badJ=False,C=False,H=False,U=False,costC=None,costH=None)
    h=4*p-y;H=(x+h==2*p+1 and (x-h)%2==1) or x==h;U=(x+h==2*p+3 and (x-h)%2==1) or x==h+2
    return dict(badJ=False,C=False,H=H,U=U,costC=None,costH=2*p-1+x if H else None)


def star(rows):
    n=len(rows[0]);seen={(0,q):0 for q in range(1,n)};todo=deque(seen);merge=None
    while todo:
        pair=todo.popleft()
        for row in rows:
            T=tuple(sorted(row[q] for q in pair))
            if T not in seen:seen[T]=seen[pair]+1;todo.append(T)
            if T[0]==T[1] and merge is None:merge=seen[T]
    return dict(minimum=merge,reachable_pairs=len(seen),distinct_pairs=sum(x!=y for x,y in seen))


def record(p):
    rows=transitions(p-2);n=3*p;K=(3,2*p);layers={k:[] for k in ('C','H','U')};counts={k:0 for k in ('controls','C_targets','H_targets','U_entries','K_entries')}
    for pair in combinations(range(n),2):
        s=categories(pair,p)
        for key in layers:
            if s[key]:layers[key].append(pair)
        if s['badJ']:continue
        if pair[0]==0:assert not any(s[k] for k in layers)
        for row in rows:
            T=tuple(sorted(row[q] for q in pair))
            if T[0]==T[1]:continue
            t=categories(T,p);assert not t['badJ']
            if t['C']:
                lower=s['costC'] if s['C'] else min(pair);assert lower+1>=t['costC'];counts['C_targets']+=1
            if t['H']:
                lower=s['costH'] if s['H'] else s['costC'] if s['C'] else min(pair);assert lower+1>=t['costH'];counts['H_targets']+=1
            if t['U'] and not s['U']:assert pair==K;counts['U_entries']+=1
            if T==K:assert s['H'] and s['costH']>=4*p-2;counts['K_entries']+=1
            counts['controls']+=1
    assert categories((4,2*p+1),p)['U']
    word=[1,0]*p+[0,1]*p;pair=[0,2]
    for a in word:pair=[rows[a][q] for q in pair]
    assert pair==[2,2]
    return dict(p=p,n=n,rows_sha256=digest(rows),layer_hashes={k:digest(layers[k]) for k in layers},layer_sizes={k:len(layers[k]) for k in layers},
                transition_counts=counts,lower_bound=4*p,upper_word=word,upper_partner=2,upper_endpoint=2,
                small_forward_star=star(rows) if p<=12 else None)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('direct_attack/data/compress_other_lower_bound.json'));args=ap.parse_args()
    records=[record(p) for p in list(range(3,65))+[100,128,256,512,1024]]
    out=dict(records=records,status='PROVED paper EVERY p>=3, n3p: exact specified-state threshold mu0=4p=4n/3; layered directed-pair certificate lemma; prior charged square reset remains valid. Finite controls separate; no formal kernel, priority and general Cerny OPEN')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(parameters=len(records),maximum_n=max(z['n'] for z in records),pair_edge_controls=sum(z['transition_counts']['controls'] for z in records))),flush=True)


if __name__=='__main__':main()
