"""Independent ordinary-set policy audits and complete small-alphabet replay."""
from collections import deque
from itertools import combinations, permutations
import hashlib
import json
from pathlib import Path
import time
from direct_attack.ordinary_reverse_policy import profile as ordinary
from direct_attack.audit_sparse_policy import ordinary_forward
from direct_attack.native_sparse_policy import profile as native

ROOT=Path('scripts/direct_attack/data/permutation_units')

def independent_inputs(kind,n):
    U=[]
    for source in range(n):
        for target in range(n):
            if source!=target:
                u=list(range(n));u[source]=target;U.append(u)
    def sets(items,complete):
        sizes=range(1,len(items)+1) if complete else [1,2,3]
        # Generator production order is increasing bit-mask order for complete covers.
        if complete:
            for bits in range(1,2**len(items)):
                yield [items[i] for i in range(len(items)) if bits//2**i%2]
        else:
            for k in sizes:
                for chosen in combinations(items,k):yield list(chosen)
    if kind=='arbitrary':
        for P in sets(list(map(list,permutations(range(n)))),True):
            for choice in sets(U,True):yield P+choice
    else:
        def partitions(total,floor):
            if total==0:yield ()
            for first in range(floor,total+1):
                for rest in partitions(total-first,first):yield (first,)+rest
        for part in partitions(n,1):
            a=[];start=0
            for length in part:
                for q in range(start,start+length):a.append(start+(q-start+1)%length)
                start+=length
            for choice in sets(U,n<=4):yield [a]+choice

def verify(c,all_source=False):
    p=ordinary(c['rows']);assert p is not None
    for key in ['extension','best','worst','forward']:
        assert c[key]=={str(S):v for S,v in p[key].items()},key
    n=len(c['rows'][0]);singles=[1<<q for q in range(n)]
    assert c['reachable']==len(p['forward'])==(1<<n)-1
    assert c['rt']==min(p['forward'][S] for S in singles)
    assert c['best_policy']==min(p['best'][S] for S in singles)
    assert c['worst_policy']==max(p['worst'][S] for S in singles)
    assert c['max_extension']==max(p['extension'].values())
    if all_source:assert ordinary_forward(c['rows'])==p
    return p

def counter_certificate(c):
    p=verify(c,True);rows=c['rows'];Q=frozenset(range(4));mask=lambda S:sum(1<<q for q in S)
    words={Q:[]};queue=[Q]
    for S in queue:
        for x,row in enumerate(rows):
            T=frozenset(row[q] for q in S)
            if T not in words:words[T]=words[S]+[x];queue.append(T)
    pairs=[]
    for S in queue:
        if S==Q:continue
        candidates=[]
        for T in queue:
            if len(T)<=len(S):continue
            W={T:[]};bfs=[T];found=None
            for U in bfs:
                if U<=S:found=W[U];break
                for x,row in enumerate(rows):
                    V=frozenset(row[q] for q in U)
                    if V not in W:W[V]=W[U]+[x];bfs.append(V)
            if found is not None:candidates.append((len(found),T,found))
        e=min(v[0] for v in candidates)
        pairs.append(dict(target=mask(S),extension=e,parents=[dict(source=mask(T),word=w) for d,T,w in candidates if d==e]))
    assert p['forward'][5]==5 and p['best'][5]==6 and p['extension'][5]==2
    phase=next(v for v in pairs if v['target']==5)
    assert phase==dict(target=5,extension=2,parents=[dict(source=7,word=[2,1])])
    assert words[frozenset([2])]==[2,1,2,1,0,2] and p['best'][4]==7
    reset=words[frozenset([2])];S=frozenset([2]);inverse=[mask(S)]
    for x in reversed(reset):
        grows=[y for y,row in enumerate(rows) if len({q for q in Q if row[q] in S})>len(S)]
        # Published immediate-letter greediness holds, despite shortest-phase failure.
        if grows:assert x in grows
        S=frozenset(q for q in Q if rows[x][q] in S);inverse.append(mask(S))
    assert S==Q
    return dict(forward_words={str(mask(S)):w for S,w in words.items()},all_shortest_parents=pairs,
                reset_word=reset,inverse_masks=inverse,immediate_letter_greedy=True,rt=6,P=7,
                minimum_scope='Four states and three letters within arbitrary permutation/unit alphabets; pure-unit controls covered by the forest proof.')

def main():
    start=time.monotonic();summary=json.loads((ROOT/'summary.json').read_text());replays=[];ordinary_count=0
    for r in summary:
        digest=hashlib.sha256();tested=accepted=0;maxe=maxp=maxloss=0
        for rows in independent_inputs(r['kind'],r['n']):
            tested+=1;p=native(rows,True)
            if r['n']<=4:
                o=ordinary(rows);assert (p is None)==(o is None)
                if o is not None:
                    ordinary_count+=1
                    for key in ['extension','best','worst','forward']:assert p[key]==o[key]
            if p is not None:
                accepted+=1
                assert p['reachable']==(1<<r['n'])-1
                if r['kind']=='single':
                    assert p['best']==p['worst']==p['forward']
                    a=rows[0];seen=set();cycles=0
                    for q in range(r['n']):
                        if q in seen:continue
                        cycles+=1
                        while q not in seen:seen.add(q);q=a[q]
                    bound=r['n']-cycles+1
                    assert p['max_extension']<=bound
                    assert p['rt']<=1+(r['n']-2)*bound
                else:assert p['best_policy']==p['rt']
                maxe=max(maxe,p['max_extension']);maxp=max(maxp,p['best_policy'])
                maxloss=max(maxloss,p['worst_policy']-p['best_policy'])
            digest.update(json.dumps([rows,p],sort_keys=True,separators=(',',':')).encode())
        assert (tested,accepted,digest.hexdigest(),maxe,maxp,maxloss)==(r['tested'],r['accepted'],r['sha256'],r['max_e'],r['max_P'],r['max_endpoint_worst_gap'])
        replays.append(dict(kind=r['kind'],n=r['n'],tested=tested,accepted=accepted))
        print(json.dumps(replays[-1]),flush=True)
    samples=json.loads((ROOT/'samples.json').read_text());allsource=0
    for i,c in enumerate(samples):verify(c,i%31==0);allsource+=int(i%31==0)
    c=json.loads((ROOT/'counterexample.json').read_text());certificate=counter_certificate(c)
    rejected=[]
    for key in ['rows','extension','best','worst','forward','rt','best_policy']:
        d=json.loads(json.dumps(c))
        if key=='rows':d[key][2]=[0,1,2,3]
        elif key in ['extension','best','worst','forward']:d[key]['4']+=1
        else:d[key]+=1
        try:verify(d)
        except AssertionError:rejected.append(key)
        else:raise AssertionError('Corruption accepted: '+key)
    (ROOT/'counter_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n',encoding='utf-8')
    result=dict(verified=True,replays=replays,ordinary_small_full_arrays=ordinary_count,ordinary_samples=len(samples),
                all_source_samples=allsource,all_source_counterexample=True,corruptions_rejected=rejected,
                seconds=time.monotonic()-start,single_cycle_sensitive_bound_checked=True,
                scope='All small designated inputs independently enumerated and ordinary-set reverse checked; all larger inputs hash replayed with native scorer; retained larger samples ordinary reverse checked. EVERY accepted single-permutation input checks e<=n-c+1 and rt<=1+(n-2)(n-c+1); all-n claims have a separate paper proof.')
    (ROOT/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result),flush=True)

if __name__=='__main__':main()
