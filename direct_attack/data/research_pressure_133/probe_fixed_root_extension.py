"""EXPLORATORY earlier inline brute-force BFS; not a registered audit."""
import random,json
from collections import deque
from direct_attack.almost_circular_returns import distances

def main():
    rng=random.Random(20261002);tested=controls=maxcost=0
    for n in range(4,11):
        for trial in range(2000):
            alpha=[0,1]+rng.sample(list(range(2,n)),n-2);a=[1]+alpha[1:]
            rem=list(range(n));rem.remove(1);b=[1]+rng.sample(rem,n-1);rows=[a,b]
            p=q=0
            while True:
                p+=1;q=b[q]
                if q==0:break
            if distances(rows,[1,1])[-1] is None:continue
            for U in range(1,(1<<n)-1):
                seen={U};dq=deque([(U,0)]);found=False
                while dq:
                    V,cost=dq.popleft()
                    if V.bit_count()>U.bit_count():found=True;maxcost=max(maxcost,cost);break
                    if cost==n:continue
                    for row in rows:
                        T=sum(1<<q for q in range(n) if V>>row[q]&1)
                        if T not in seen:seen.add(T);dq.append((T,cost+1))
                assert found,(n,alpha,b,U);controls+=1
            tested+=1
    print(json.dumps(dict(tested=tested,subsets=controls,max_extension=maxcost)))

if __name__=='__main__':main()
