"""All-tie greedy image-extension policies, using forward transport distances."""
from collections import deque
import argparse
import json
from pathlib import Path
from direct_attack.core import bfs,graph
from direct_attack.core import strongly_connected
from direct_attack.mine import inputs


def profile(rows):
    n=len(rows[0]);N=1<<n;g=graph(rows);f=bfs(g,[N-1]);R=[s for s,v in enumerate(f) if v>=0]
    if not any(f[1<<q]>=0 for q in range(n)):return None
    delta={}
    for T in R:
        d=bfs(g,[T]);values=[v if v>=0 else N*N for v in d]
        for S in range(1,N):
            bits=S
            while bits:
                bit=bits & -bits;bits-=bit
                values[S]=min(values[S],values[S^bit])
        delta[T]={S:values[S] for S in R}
    e={S:min(delta[T][S] for T in R if T.bit_count()>S.bit_count()) for S in R if S!=N-1}
    best={N-1:0};worst={N-1:0};choice={}
    for S in sorted(e,key=int.bit_count,reverse=True):
        targets=[T for T in R if T.bit_count()>S.bit_count() and delta[T][S]==e[S]]
        T=min(targets,key=lambda t:best[t]);choice[S]=T
        best[S]=e[S]+best[T];worst[S]=e[S]+max(worst[t] for t in targets)
    singleton=min((1<<q for q in range(n)),key=lambda s:best[s])
    S=singleton;word=[];phases=[]
    while S!=N-1:
        T=choice[S];queue=deque([T]);words={T:[]}
        while queue:
            U=queue.popleft()
            if U & S==U:
                w=words[U];break
            for a,V in enumerate(g[U]):
                if V not in words:words[V]=words[U]+[a];queue.append(V)
        assert len(w)==e[S]
        word=w+word;phases.append(dict(start=S,larger=T,word=w));S=T
    current=N-1
    for a in word:current=g[current][a]
    assert current==singleton and len(word)==best[singleton]
    return dict(n=n,rows=rows,extension=e,best=best,worst=worst,
                best_policy=best[singleton],worst_policy=max(worst[1<<q] for q in range(n)),
                rt=min(f[1<<q] for q in range(n)),reset_word=word,phases=phases)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int)
    ap.add_argument('--mode',choices=['random','exhaustive','first-map-orbits'],default='random')
    ap.add_argument('--count',type=int,default=10000);ap.add_argument('--seed',type=int,default=20260930)
    ap.add_argument('--out',default='direct_attack/data/image_extension_policy')
    args=ap.parse_args();records=[];seen=set();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    paths=list(Path('direct_attack/data').rglob('*.profile.json'))
    paths += [p for r in Path('direct_attack/data').glob('image_extension_*') for p in r.glob('n*_cost*.json')]
    if args.n:
        sources=((str(i),rows) for i,rows in enumerate(inputs(args.n,args.mode,args.count,args.seed,2)))
    else:sources=((str(path),json.loads(path.read_text())['rows']) for path in sorted(paths))
    best_gap=0;worst_excess=0;tested=0;sync=0;witnesses=0;max_policy=0
    for path,rows in sources:
        tested+=1;n=len(rows[0])
        if n>10:continue
        key=tuple(map(tuple,rows))
        if not args.n:
            if key in seen:continue
            seen.add(key)
        if not strongly_connected(rows):continue
        p=profile(rows)
        if p is None:continue
        sync+=1;max_policy=max(max_policy,p['best_policy']);gap=p['best_policy']-p['rt'];excess=p['best_policy']-(n-1)**2
        record=dict(source=str(path),n=n,rt=p['rt'],best_policy=p['best_policy'],worst_policy=p['worst_policy'])
        if not args.n:records.append(record)
        if gap>best_gap or excess>worst_excess:
            best_gap=max(best_gap,gap);worst_excess=max(worst_excess,excess)
            name=f'witness_{witnesses:03d}.json';witnesses+=1
            (out/name).write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(record),flush=True)
    summary=dict(arguments=vars(args),records=records,tested=tested,automata=sync,max_gap=best_gap,
                 max_square_excess=worst_excess,max_policy=max_policy,
                 scope='Complete distinct-letter binary coverage only in exhaustive/first-map-orbits mode; otherwise retained inputs or sampling.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='records'}))


if __name__=='__main__':main()
