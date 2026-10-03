"""Find exact pair-distance matrices supporting distinct reset thresholds."""
from itertools import combinations,permutations
from pathlib import Path
import json
from direct_attack.core import analyze,canonical,certificate,enrich,public,strongly_connected
from direct_attack.mine import inputs
from src.check_certificate import check

def pair_key(p):
    n=p['n']
    result=None
    relabel=None
    # p maps new indices to old ones for this key.
    for order in permutations(range(n)):
        values=tuple(p['distance'][(1<<order[i])|(1<<order[j])] for i,j in combinations(range(n),2))
        if result is None or values<result: result,relabel=values,order
    return result,relabel

def move(p,order):
    inverse={old:new for new,old in enumerate(order)}
    rows=[[inverse[row[old]] for old in order] for row in p['rows']]
    return analyze(rows)

def main():
    out=Path('direct_attack/data/pair_information')
    out.mkdir(parents=True,exist_ok=True)
    results=[]
    for n in [3,4]:
        seen,groups=set(),{}
        sync_classes=0
        best=None
        for rows in inputs(n,'exhaustive',0,0,2):
            if not strongly_connected(rows): continue
            canon=canonical(rows)
            if canon in seen: continue
            seen.add(canon)
            p=analyze(canon)
            if p is None: continue
            sync_classes+=1
            key,order=pair_key(p)
            if key not in groups: groups[key]=[p,order,p,order]
            old=groups[key]
            if p['rt']<old[0]['rt']: old[0],old[1]=p,order
            if p['rt']>old[2]['rt']: old[2],old[3]=p,order
            gap=old[2]['rt']-old[0]['rt']
            if gap and (best is None or gap>best[0]): best=(gap,key,*old)
        record=dict(n=n,pair_matrices=len(groups),sync_classes=sync_classes,max_reset_difference=0 if best is None else best[0])
        if best:
            gap,key,low,ol,high,oh=best
            low,high=move(low,ol),move(high,oh)
            assert all(low['distance'][s]==high['distance'][s] for s in range(1,1<<n) if s.bit_count()==2)
            record.update(pair_distance_upper_triangle=key,low_rt=low['rt'],high_rt=high['rt'],low_rows=low['rows'],high_rows=high['rows'])
            for label,p in [('low',low),('high',high)]:
                cert=certificate(p)
                check(cert)
                name=f'n{n}_{label}'
                (out/(name+'.certificate.json')).write_text(json.dumps(cert,indent=2)+'\n',encoding='utf-8')
                (out/(name+'.profile.json')).write_text(json.dumps({**public(p),**enrich(p)},indent=2)+'\n',encoding='utf-8')
        results.append(record)
    (out/'summary.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results))

if __name__=='__main__': main()
