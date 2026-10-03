"""Compare independent inverse rank solver with full forward distances and sets."""
from itertools import combinations
import json
from pathlib import Path
import random
import time
from direct_attack.mine import inputs,maps
from direct_attack.native_policy import profile as forward
from direct_attack.native_complete_policy import profile as inverse
from direct_attack.image_extension_policy import profile as certificate
from direct_attack.check_image_policy import verify as set_verify


def main():
    started=time.monotonic();counts=dict(tested=0,complete=0,incomplete_rejected=0,ordinary_set_policy_checks=0)
    records=[]
    def check(rows,ordinary=False):
        counts['tested']+=1;a=forward(rows,True);b=inverse(rows,True)
        complete=a is not None and a['reachable']==(1<<len(rows[0]))-1
        if not complete:
            assert b is None;counts['incomplete_rejected']+=1;return
        assert b is not None;counts['complete']+=1
        for key in ['extension','best','worst','best_policy','worst_policy','rt','reachable','local_excess','local_start']:
            assert a[key]==b[key],(rows,key,a[key],b[key])
        assert b['unit_defect']==all(len(set(row))>=len(row)-1 for row in rows)
        if ordinary:
            c=json.loads(json.dumps(certificate(rows)));set_verify(c)
            for key in ['extension','best','worst']:
                assert c[key]=={str(S):v for S,v in b[key].items()}
            counts['ordinary_set_policy_checks']+=1
    for n in [2,3,4]:
        before=dict(counts)
        for rows in inputs(n,'first-map-orbits',0,0,2):check(rows,True)
        records.append(dict(scope=f'binary first-map n{n}',counts={key:counts[key]-before[key] for key in counts}))
    before=dict(counts)
    for rows in combinations(maps(3),3):check(rows,True)
    records.append(dict(scope='all distinct-letter ternary n3',counts={key:counts[key]-before[key] for key in counts}))
    rng=random.Random(20261008)
    for n in [6,8,10]:
        before=dict(counts);base=[list(range(n-1))+[0],[(q+1)%n for q in range(n)]]
        for i in range(20):
            if i%4==0:extra=[rng.randrange(n)]*n
            elif i%4==1:extra=list(range(n));rng.shuffle(extra)
            elif i%4==2:
                extra=list(range(n));rng.shuffle(extra);extra[0]=extra[1]
            else:extra=[rng.randrange(n) for _ in range(n)]
            check(base+[extra])
        records.append(dict(scope=f'Cerny with general added map n{n}',counts={key:counts[key]-before[key] for key in counts}))
    n=12;rows=[[1,0,0]+list(range(2,n-1)),[(q+1)%n for q in range(n)]]
    check(rows);extra=list(range(n))
    for a in [1,1,0,1,1,1,0]:extra=[rows[a][q] for q in extra]
    check(rows+[extra])
    full=inverse(rows+[extra],True);small=inverse(rows+[extra],'singletons')
    for prefix,field in [('singleton_extension','extension'),('singleton_best','best'),('singleton_worst','worst')]:
        assert small[prefix]==[full[field][1<<q] for q in range(n)]
    report=dict(counts=counts,records=records,seconds=time.monotonic()-started,all_agreed=True,
                boundary='All binary covers through n4 and ternary n3 have independent ordinary-set checks. Larger cases compare two native algorithms; this is not a larger complete automaton enumeration.')
    Path('direct_attack/data/complete_policy_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
