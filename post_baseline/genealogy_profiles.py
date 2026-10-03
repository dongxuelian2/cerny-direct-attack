"""A deliberately relaxed binary genealogy lower-bound experiment.

Tree edges cost r or r+1 in nonmerging time. Ignore collisions and ignore
the stronger endpoint-0 condition. Enumerate all cost multisets for small r.
"""
from functools import lru_cache


def profiles(r, max_leaves):
    @lru_cache(None)
    def f(n):
        if n==1:
            return {(0,)}
        out=set()
        for left in range(1,n):
            for a in f(left):
                for b in f(n-left):
                    out.add(tuple(sorted([x+r+1 for x in a]+[x+r for x in b])))
        return out
    return f(max_leaves)


def main():
    for r in range(2,9):
        offsets=[1,1]+list(range(2,r+2))
        best=min((max(x-y for x,y in zip(p,offsets)),p)
                 for p in profiles(r,r+2))
        h=(r-1).bit_length()
        expected=(h+1)*r-(1<<h)+2
        print(r,'relaxed nonmerge time',best[0],'conjectured',expected,
              'profile',best[1],flush=True)
    for r in range(2,9):
        candidates=tagged_profiles(r,r+2)
        offsets=[1,1]+list(range(2,r+1))
        best=10**9
        for a,b in candidates:
            for side,part in enumerate((a,b)):
                for w in part:
                    rest=sorted(a+b)
                    rest.remove(w)
                    lower=max(w-(r+1 if side==0 else 0),
                              max(x-y for x,y in zip(rest,offsets)))
                    best=min(best,lower)
        print('tagged',r,'bound',best,'profiles',len(candidates),flush=True)


def tagged_profiles(r,leaves):
    @lru_cache(None)
    def f(n):
        if n==1:
            return {((0,),())}
        out=set()
        for left in range(1,n):
            for aa,ab in f(left):
                for ba,bb in f(n-left):
                    if left==1:
                        la,lb=(r+1,),()
                    else:
                        la,lb=tuple(x+r+1 for x in aa),tuple(x+r+1 for x in ab)
                    if n-left==1:
                        ra,rb=(),(r,)
                    else:
                        ra,rb=tuple(x+r for x in ba),tuple(x+r for x in bb)
                    out.add((tuple(sorted(la+ra)),tuple(sorted(lb+rb))))
        return out
    return f(leaves)


if __name__=='__main__':
    main()
