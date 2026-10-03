"""Compare every small covered SC synchronizing input with inverse-set BFS."""
import json
from pathlib import Path
from direct_attack.check_new_image_results import distances
from direct_attack.core import strongly_connected
from direct_attack.mine import inputs
from direct_attack.native_policy import profile


def main():
    records=[];encode=lambda S:sum(1<<q for q in S)
    for n in [2,3,4]:
        tested=sc=sync=0
        for rows in inputs(n,'first-map-orbits',0,0,2):
            tested+=1
            if not strongly_connected(rows):continue
            sc+=1;actual=profile(rows,details=True)
            if actual is None:continue
            sync+=1;Q,f,reach,e,best,choices,worst=distances(rows,with_worst=True)
            assert actual['extension']=={encode(S):v for S,v in e.items()}
            assert actual['best']=={encode(S):v for S,v in best.items()}
            assert actual['worst']=={encode(S):v for S,v in worst.items()}
            assert actual['rt']==min(v for S,v in f.items() if len(S)==1)
            assert actual['local_excess']==max(v-n*(n-len(S)) for S,v in best.items() if S!=Q)
        records.append(dict(n=n,tested=tested,sc=sc,synchronizing_sc=sync,verified=True))
    Path('direct_attack/data/native_small_checks.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(records))


if __name__=='__main__':main()
