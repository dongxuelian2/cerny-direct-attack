"""Display capped pair distances to look for a uniform proof invariant."""
from alphabet_check import pair_distances,bfs
from two_block_probe import construct

def main():
    for p,t in ((5,3),(6,4),(7,5)):
        rows,S,_,_,_=construct(p,t);d=pair_distances(rows);n=len(rows[0]);L=3*t+2
        print("p,t,cap",p,t,L)
        labels=[f"p{i}" for i in range(p)]+[f"u{i}" for i in range(1,2*t+2)]
        print("   "," ".join(f"{q:>3}" for q in labels))
        for q in range(n):
            print(f"{labels[q]:>3}"," ".join(f"{(0 if q==v else min(d[tuple(sorted((q,v)))],L)):>3}" for v in range(n)))
        w,_=bfs(rows,S,lambda T:len(T)<len(S))
        print("compression",w)
        w,_=bfs(rows,S,lambda T:0 not in T)
        print("root avoidance",w)

if __name__=="__main__":main()
