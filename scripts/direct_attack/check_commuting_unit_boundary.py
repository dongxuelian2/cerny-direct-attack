"""Independent small cover, hash replay and ALL-SOURCE commuting refutation."""
from itertools import combinations,permutations
from collections import deque
import hashlib,json
from pathlib import Path
from direct_attack.ordinary_reverse_policy import profile as ordinary
from direct_attack.audit_sparse_policy import ordinary_forward
from direct_attack.native_sparse_policy import profile as native
from direct_attack.native_policy import profile as dense

ROOT=Path('scripts/direct_attack/data/commuting_unit_boundary')

def main():
    summary=json.loads((ROOT/'summary.json').read_text());checks=[];ordinary_count=0
    for n in range(2,6):
        tested=accepted=0;digest=hashlib.sha256();hist={};U=[]
        for s in range(n):
            for t in range(n):
                if s!=t:U.append([t if q==s else q for q in range(n)])
        Ps=list(map(list,permutations(range(n))))
        for a,b in combinations(Ps,2):
            if [a[b[q]] for q in range(n)]!=[b[a[q]] for q in range(n)]:continue
            for size in range(1,min(3,len(U))+1):
                for chosen in combinations(U,size):
                    rows=[a,b]+list(chosen);tested+=1;p=native(rows)
                    if n==5:
                        d=dense(rows);assert (p is None)==(d is None)
                        if p is not None:
                            for key in ['rt','best_policy','worst_policy','reachable']:assert p[key]==d[key]
                    if n<=4:
                        o=ordinary(rows);assert (p is None)==(o is None)
                        if o is not None:
                            ordinary_count+=1;assert min(o['best'][1<<q] for q in range(n))==min(o['forward'][1<<q] for q in range(n))
                    if p is not None:
                        accepted+=1;assert p['best_policy']==p['rt'];key=str((p['rt'],p['best_policy'],p['max_extension']))
                        hist[key]=hist.get(key,0)+1
                    digest.update(json.dumps([rows,p],sort_keys=True,separators=(',',':')).encode())
        r=dict(n=n,tested=tested,accepted=accepted,rejected=tested-accepted,sha256=digest.hexdigest(),histogram=hist)
        assert r==next(v for v in summary['records'] if v['n']==n);checks.append({k:v for k,v in r.items() if k!='histogram'})
        print(json.dumps(checks[-1]),flush=True)
    c=json.loads((ROOT/'counterexample.json').read_text());rows=c['rows'];n=c['n'];a,b=rows[:2]
    assert n==6 and all(a[b[q]]==b[a[q]] for q in range(n))
    for row in rows[2:]:assert len([q for q in range(n) if row[q]!=q])==1
    o=ordinary_forward(rows);assert o==ordinary(rows)
    for key in ['extension','best','worst','forward']:assert c[key]=={str(S):v for S,v in o[key].items()}
    assert min(o['forward'][1<<q] for q in range(n))==c['rt']==8
    assert min(o['best'][1<<q] for q in range(n))==c['best_policy']==9
    Q=frozenset(range(n));words={Q:[]};queue=[Q]
    for S in queue:
        for x,row in enumerate(rows):
            T=frozenset(row[q] for q in S)
            if T not in words:words[T]=words[S]+[x];queue.append(T)
    target=min((S for S in words if len(S)==1),key=lambda S:len(words[S]));word=words[target]
    assert len(word)==8;S=set(range(n));trajectory=[sum(1<<q for q in S)]
    for x in word:S={rows[x][q] for q in S};trajectory.append(sum(1<<q for q in S))
    assert len(S)==1
    parents=[];goal=frozenset([0,1,4])
    for source in queue:
        if len(source)<=len(goal):continue
        bfs=[source];paths={source:[]}
        for U in bfs:
            if U<=goal:
                if len(paths[U])==2:parents.append(dict(mask=sum(1<<q for q in source),word=paths[U]))
                break
            for x,row in enumerate(rows):
                V=frozenset(row[q] for q in U)
                if V not in paths:paths[V]=paths[U]+[x];bfs.append(V)
    assert parents==[dict(mask=51,word=[3,0])]
    assert o['extension'][19]==2 and o['best'][51]==5 and o['best'][19]==7 and o['forward'][19]==6
    certificate=dict(rows=rows,rt=8,P=9,reset_word=word,target=list(S)[0],forward_masks=trajectory,
                     singleton_forward=[o['forward'][1<<q] for q in range(n)],singleton_G=[o['best'][1<<q] for q in range(n)],
                     singleton_W=[o['worst'][1<<q] for q in range(n)],critical_target=19,
                     all_critical_winning_parents=parents,minimum_scope=summary['scope'])
    (ROOT/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n',encoding='utf-8')
    report=dict(verified=True,replays=checks,ordinary_small=ordinary_count,two_kernel_n5_inputs=486000,all_source_counterexample=True,
                reset_word=word,rt=8,P=9,scope=summary['scope'])
    (ROOT/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)

if __name__=='__main__':main()
