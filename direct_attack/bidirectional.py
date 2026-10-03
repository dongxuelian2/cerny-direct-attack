"""Greedy frontiers may meet inside phases; the cost is exact for this policy."""
from collections import deque, Counter
import argparse
import json
from pathlib import Path
from direct_attack.core import analyze, reverse, bfs, public, enrich, certificate, strongly_connected
from src.check_certificate import check
from direct_attack.mine import inputs

def solve(p):
    n=p['n']; full=(1<<n)-1; rows=p['rows']; g=p['graph']; c=p['compression']
    # All forward prefixes that follow a shortest first-drop at every phase.
    gf=[tuple(t for t in g[s] if (t.bit_count()<s.bit_count() and c[s]==1)
              or (t.bit_count()==s.bit_count() and c[t]==c[s]-1))
        if s.bit_count()>=2 else () for s in range(full+1)]
    f=bfs(gf,[full]); fw={full:[]}; queue=deque([full])
    while queue:
        s=queue.popleft()
        for a,t in enumerate(g[s]):
            if t in gf[s] and t not in fw:
                fw[t]=fw[s]+[a]; queue.append(t)
    pg=[tuple(sum(1<<q for q in range(n) if s>>row[q]&1) for row in rows) for s in range(full+1)]
    pr=reverse(pg); macro={}; partial={}; phaseword={}
    for s in range(1,full):
        ds=bfs(pg,[s]); goals=[t for t in range(1,full+1) if t.bit_count()>s.bit_count()]
        e=min(ds[t] for t in goals if ds[t]>=0)
        dg=bfs(pr,goals)
        partial[s]={t:ds[t] for t in range(1,full+1) if ds[t]>=0 and ds[t]+dg[t]==e}
        macro[s]=[t for t in goals if ds[t]==e]
        words={s:[]}; queue=deque([s])
        while queue:
            t=queue.popleft()
            if ds[t]>=e: continue
            for a,u in enumerate(pg[t]):
                if ds[u]==ds[t]+1 and u not in words:
                    words[u]=words[t]+[a]; queue.append(u)
        phaseword[s]=words
    b={1<<q:0 for q in range(n)}; bw={1<<q:[] for q in range(n)}
    for s in sorted(range(1,full),key=lambda s:s.bit_count()):
        if s not in b: continue
        for t in macro[s]:
            word=bw[s]+phaseword[s][t]
            if t not in b or len(word)<b[t]: b[t]=len(word); bw[t]=word
    # Every intermediate node of a shortest inverse phase is a valid suffix.
    bp=dict(b); bpw=dict(bw)
    for s,cost in b.items():
        if s==full: continue
        for t,length in partial[s].items():
            if t not in bp or cost+length<bp[t]:
                bp[t]=cost+length; bpw[t]=bw[s]+phaseword[s][t]
    cost,s,t=min((f[s]+bp[t],s,t) for s in range(1,full+1) if f[s]>=0
                 for t in bp if s&t==s)
    prefix=fw[s]; suffix=list(reversed(bpw[t])); word=prefix+suffix
    assert len(word)==cost>=p['rt']
    image=set(range(n))
    for a in word: image={rows[a][q] for q in image}
    assert len(image)==1
    return dict(cost=cost,prefix=prefix,suffix=suffix,forward_meeting=s,backward_meeting=t,
                forward_greedy_best=p['greedy_min'][-1],backward_greedy_best=b[full])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',default='direct_attack/data')
    ap.add_argument('--n',type=int,default=6)
    ap.add_argument('--random',type=int,default=0)
    ap.add_argument('--out',default='direct_attack/data/bidirectional')
    args=ap.parse_args(); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    candidates=[json.loads(path.read_text())['rows'] for path in Path(args.source).rglob('*.profile.json')]
    candidates+=list(inputs(args.n,'random',args.random,20260928,2))
    seen=set(); counts=Counter(); records=[]; gap=0
    for rows in candidates:
        key=tuple(tuple(r) for r in rows)
        if key in seen: continue
        seen.add(key)
        if not strongly_connected(rows): continue
        p=analyze(rows)
        if p is None: continue
        h=solve(p); counts['sync_inputs']+=1
        counts['square_failures']+=h['cost']>(p['n']-1)**2
        counts['suboptimal']+=h['cost']>p['rt']
        if h['cost']-p['rt']>gap or h['cost']>(p['n']-1)**2:
            gap=max(gap,h['cost']-p['rt'])
            label=f'witness_{len(records):03d}'
            (out/(label+'.policy.json')).write_text(json.dumps(dict(n=p['n'],rows=rows,rt=p['rt'],**h),indent=2)+'\n',encoding='utf-8')
            cert=certificate(p); check(cert)
            (out/(label+'.certificate.json')).write_text(json.dumps(cert,indent=2)+'\n',encoding='utf-8')
            (out/(label+'.profile.json')).write_text(json.dumps({**public(p),**enrich(p)},indent=2)+'\n',encoding='utf-8')
            records.append(dict(label=label,n=p['n'],rt=p['rt'],cost=h['cost']))
    result=dict(arguments=vars(args),counts=dict(counts),maximum_gap=gap,records=records,
                status='REFUTED' if counts['square_failures'] else 'COMPUTATIONALLY VERIFIED IN THIS CORPUS ONLY')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)

if __name__=='__main__': main()
