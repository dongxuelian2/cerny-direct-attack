"""Complete two-commuting-permutation/<=3-unit covers n2..5 and n6 refutation."""
from itertools import combinations,permutations
import hashlib
import json
from pathlib import Path
from direct_attack.permutation_units import units
from direct_attack.native_sparse_policy import profile
from direct_attack.native_policy import profile as dense

ROOT=Path('direct_attack/data/commuting_unit_boundary')
ROWS=[[0,1,2,3,5,4],[1,2,3,0,5,4],[4,1,2,3,4,5],[0,1,2,3,1,5]]

def inputs(n):
    Ps=list(map(list,permutations(range(n))))
    for a,b in combinations(Ps,2):
        if all(a[b[q]]==b[a[q]] for q in range(n)):
            for count in range(1,min(3,n*(n-1))+1):
                for chosen in combinations(units(n),count):yield [a,b]+list(chosen)

def main():
    ROOT.mkdir(exist_ok=True);records=[]
    for n in range(2,6):
        tested=accepted=0;digest=hashlib.sha256();hist={}
        for rows in inputs(n):
            tested+=1;p=profile(rows)
            if p is not None:
                accepted+=1;assert p['best_policy']==p['rt'];key=str((p['rt'],p['best_policy'],p['max_extension']))
                hist[key]=hist.get(key,0)+1
            digest.update(json.dumps([rows,p],sort_keys=True,separators=(',',':')).encode())
        r=dict(n=n,tested=tested,accepted=accepted,rejected=tested-accepted,sha256=digest.hexdigest(),histogram=hist)
        records.append(r);print(json.dumps({k:v for k,v in r.items() if k!='histogram'}),flush=True)
    p=profile(ROWS,True);q=dense(ROWS,True)
    for key in ['extension','best','worst','rt','best_policy','reachable']:assert p[key]==q[key]
    assert p['rt']==8 and p['best_policy']==9 and p['reachable']==63
    (ROOT/'counterexample.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
    (ROOT/'summary.json').write_text(json.dumps(dict(records=records,
        scope='Complete designated covers: TWO distinct commuting permutation letters and one to three distinct unitary letters at n2..5. State minimum6 ONLY in this restricted class. The n6 search was adaptive first-refutation exploration, not a complete cover; its old terminal stdout was not persisted and its trial count is not used as a durable result.'),indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
