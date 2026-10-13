"""Independent full-map class cover, ordinary arrays and constructive words."""
from collections import deque
from itertools import product
from math import gcd
import json
from pathlib import Path
import time
from direct_attack.core import strongly_connected
from direct_attack.ordinary_reverse_policy import profile
from direct_attack.audit_sparse_policy import ordinary_forward


def verify(c):
    n=c['n'];j=c['j'];h=c['h'];rows=c['rows'];assert 1<=h<n and 0<=j<=h
    b=list(range(n));b[h]=0;assert rows==[list(range(1,n))+[j],b] and strongly_connected(rows)
    sync=gcd(n-j,h)==1;assert c['synchronizing']==sync
    if not sync:
        g=gcd(n-j,h)
        assert g>1 and all((rows[0][q]-q-1)%g==0 and (rows[1][q]-q)%g==0 for q in range(n))
        return dict(n=n,j=j,h=h,sync=False)
    p=profile(rows);assert p is not None
    for key in ['extension','best','worst','forward']:assert c[key]=={str(S):v for S,v in p[key].items()}
    if n<=7:
        f=ordinary_forward(rows)
        for key in ['extension','best','worst','forward']:assert f[key]==p[key]
    assert c['rt']==min(p['forward'][1<<q] for q in range(n))==c['best_policy']==min(p['best'][1<<q] for q in range(n))
    assert c['max_extension']==max(p['extension'].values())<=n
    word=c['reset_word'];expected=([1]+[0]*h)*(n-2)+[1] if j==0 else [0]*j+([1]+[0]*h)*(n-j-1)
    assert word==expected and c['rt']<=len(word)<=(n-1)**2
    S=set(range(n))
    for x in word:S={rows[x][q] for q in S}
    assert len(S)==1
    if (n,j,h)==(4,2,3):
        bad=[0]*j+([1]+[0]*h)*(n-j-2)+[1];T=set(range(n))
        for x in bad:T={rows[x][q] for q in T}
        assert len(T)>1 and len(bad)==3<c['rt']==5 # final a^h cannot be trimmed after a tail
    return dict(n=n,j=j,h=h,sync=True,rt=c['rt'],P=c['best_policy'],e=c['max_extension'],all_source=n<=7)


def main():
    started=time.monotonic();root=Path('scripts/direct_attack/data/unit_tail_family');records=[]
    for r in json.loads((root/'summary.json').read_text())['records']:
        records.append(verify(json.loads((root/r['file']).read_text())))
    cover=[]
    for n in range(2,7):
        tested=0;sc=0;sync=0;b=list(range(n));b[-1]=0
        for row in product(range(n),repeat=n):
            tested+=1;connected=strongly_connected([row,b]);orbit=[];seen=set();q=0
            while q not in seen:seen.add(q);orbit.append(q);q=row[q]
            full=len(orbit)==n
            j=orbit.index(q);h=orbit.index(n-1) if n-1 in seen else -1
            assert connected==(full and h>=j)
            if connected:
                sc+=1;assert all(row[orbit[i]]==orbit[i+1] for i in range(n-1)) and row[orbit[-1]]==orbit[j]
                # Ordinary graph closure gives a synchronization test independently of gcd.
                Q=frozenset(range(n));R=[Q];images={Q}
                for S in R:
                    for a in [row,b]:
                        T=frozenset(a[x] for x in S)
                        if T not in images:images.add(T);R.append(T)
                exact=any(len(S)==1 for S in R);assert exact==(gcd(n-j,h)==1);sync+=int(exact)
        cover.append(dict(n=n,tested=tested,sc=sc,sync=sync))
    c=json.loads((root/'n6_j1_h4.json').read_text());rejected=[]
    for key in ['j','reset_word','best']:
        d=json.loads(json.dumps(c))
        if key=='j':d[key]+=1
        elif key=='reset_word':d[key]=d[key][:-1]
        else:d[key]['1']+=1
        try:verify(d)
        except AssertionError:rejected.append(key)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,records=records,cover=cover,corruptions_rejected=rejected,seconds=time.monotonic()-started,
                scope='All 352 SC normal-form parameter cases n2..12; every saved array of 222 sync cases checked by ordinary reverse BFS, n<=7 additionally ALL-SOURCE. Every one of 50068 arbitrary other maps with fixed unit letter n2..6 checked for SC orbit classification and synchronization/gcd agreement. All-n normal form, iff synchronization and reset-square upper bound are paper proofs; e<=n and P=rt remain conjectured beyond finite parameters.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),sync=sum(r['sync'] for r in records),full_map_cover=cover,corruptions_rejected=rejected,seconds=report['seconds'])),flush=True)


if __name__=='__main__':main()
