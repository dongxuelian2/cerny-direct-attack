"""Independent finite audit of the arbitrary-n circular image-policy theorem."""
import json
from pathlib import Path
from direct_attack.check_new_image_results import distances
from direct_attack.native_policy import profile


def main():
    out=Path('direct_attack/data/circular_image_policy');out.mkdir(exist_ok=True);records=[]
    for n in range(2,13):
        rows=[[(q+1)%n for q in range(n)],list(range(n-1))+[0]]
        Q,f,reach,e,best,choices,worst=distances(rows,with_worst=True);p=profile(rows,details=True)
        encode=lambda S:sum(1<<q for q in S)
        critical=[]
        for k in range(2,n+1):
            S=frozenset([n-1]+list(range(k-1)));w=([1]+[0]*(n-1))*(n-k);X=Q
            for a in w:X=frozenset(rows[a][q] for q in X)
            assert X==S and best[S]==n*(n-k)
            assert p['best'][encode(S)]==p['worst'][encode(S)]==best[S]==worst[S]
            if k<n:assert e[S]==p['extension'][encode(S)]==n
            critical.append(dict(start=encode(S),size=k,extension=None if k==n else n,policy=best[S],reach_word=w))
        singletons=[]
        for q in range(n):
            S=frozenset([q]);word=([1]+[0]*(n-1))*(n-2)+[1]+[0]*q;X=Q
            for a in word:X=frozenset(rows[a][q] for q in X)
            assert X==S and len(word)==best[S]==(n-1)**2+q
            assert e[S]==p['extension'][1<<q]==q+1
            assert p['best'][1<<q]==p['worst'][1<<q]==best[S]==worst[S]
            assert choices[S][0]==frozenset([0,n-1])
            singletons.append(dict(state=q,extension=e[S],policy=best[S],reset_word=word))
        r=dict(n=n,rows=rows,critical=critical,singletons=singletons,
               mean_sum=sum(best[frozenset([q])] for q in range(n)),square_sum=n*(n-1)**2,verified=True)
        assert r['mean_sum']-r['square_sum']==n*(n-1)//2
        (out/f'n{n}.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
        records.append(dict(n=n,reachable=len(f),best_policy=p['best_policy'],worst_policy=p['worst_policy'],verified=True))
        print(json.dumps(records[-1]),flush=True)
    (out/'summary.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
