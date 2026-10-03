"""Attack choosing the better of exact optimal forward/inverse greedy."""
from collections import Counter
import json
from pathlib import Path
from direct_attack.core import analyze, canonical, strongly_connected
from direct_attack.mine import inputs
from direct_attack.history_dimensions import profile
from direct_attack.check_histories import verify

def main():
    out=Path('direct_attack/data/orientation_greedy'); out.mkdir(parents=True,exist_ok=True)
    summaries=[]
    for n in [3,4,5]:
        counts=Counter(); seen=set(); bad=[]
        mode='exhaustive' if n<=4 else 'first-map-orbits'
        for rows in inputs(n,mode,0,0,2):
            counts['tested']+=1
            if not strongly_connected(rows): continue
            p=analyze(rows)
            if p is None: continue
            counts['sync_cover_occurrences']+=1
            if p['greedy_min'][-1]<=(n-1)**2: continue
            key=canonical(rows)
            if key in seen: continue
            seen.add(key); counts['forward_failing_classes']+=1
            h=profile(key)
            h.update(rt=p['rt'],forward_greedy_best=p['greedy_min'][-1])
            if h['backward_greedy_best']>(n-1)**2:
                bad.append(h); counts['both_failing_classes']+=1
        summaries.append(dict(n=n,mode=mode,counters=dict(counts),violations=bad))
        print(json.dumps(summaries[-1]),flush=True)
    for path in sorted(Path('direct_attack/data/n6_extremal').glob('*.profile.json')):
        p=json.loads(path.read_text()); h=profile(p['rows'])
        if min(p['greedy_min'][-1],h['backward_greedy_best'])<=25: continue
        h.update(rt=p['rt'],forward_greedy_best=p['greedy_min'][-1])
        dest=out/'n6_both_fail.json'; dest.write_text(json.dumps(h,indent=2)+'\n',encoding='utf-8')
        check=verify(dest)
        summaries.append(dict(n=6,status='REFUTED',forward=h['forward_greedy_best'],
                              backward=h['backward_greedy_best'],rt=p['rt'],verified=check['verified']))
    (out/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summaries[-1]),flush=True)

if __name__=='__main__': main()
