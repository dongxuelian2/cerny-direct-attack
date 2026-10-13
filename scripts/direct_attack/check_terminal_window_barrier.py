"""Independent original-pair BFS and reachable-image audit of the window barrier."""
from collections import deque
from itertools import combinations
from math import comb
from fractions import Fraction
import json
from pathlib import Path


def rows(n):
    return [list(range(1,n))+[0],list(range(n-1))+[0]]


def distances(n):
    pairs = list(combinations(range(n),2))
    reverse = {p:[] for p in pairs}
    distance, pending = {}, deque()
    transition_rows=rows(n)
    for p in pairs:
        for row in transition_rows:
            q = tuple(sorted({row[x] for x in p}))
            if len(q)==1:
                if p not in distance:
                    distance[p]=1
                    pending.append(p)
            else:
                reverse[q].append(p)
    while pending:
        q=pending.popleft()
        for p in reverse[q]:
            if p not in distance:
                distance[p]=distance[q]+1
                pending.append(p)
    assert len(distance)==len(pairs)
    return distance


def proposed(n):
    result={}
    for r in range(1,n//2+1):
        length=n//2 if 2*r==n else n
        for j in range(length):
            p=tuple(sorted(((r-1-j)%n,(n-1-j)%n)))
            assert p not in result
            result[p]=(r-1)*n+1+j
    return result


def validate(n, annotation, verify_words=False):
    literal=distances(n)
    assert annotation==literal
    assert sorted(literal.values())==list(range(1,comb(n,2)+1))
    letters=0
    transition_rows=rows(n)
    for p,value in annotation.items():
        for row in transition_rows:
            q=tuple(sorted({row[x] for x in p}))
            assert value <= 1+(0 if len(q)==1 else annotation[q])
        if verify_words:
            q=p
            word=[]
            while len(q)>1:
                next_steps=[(a,tuple(sorted({row[x] for x in q})))
                            for a,row in enumerate(transition_rows)]
                a,new_q=next((a,z) for a,z in next_steps
                              if (0 if len(z)==1 else annotation[z])==annotation[q]-1)
                word.append(a)
                q=new_q
            assert len(word)==value
            image=set(p)
            for a in word:
                image={transition_rows[a][x] for x in image}
            assert len(image)==1
            letters+=len(word)
    # All terminal layers, including the endpoint beyond the pair diameter.
    histogram=[0]*(comb(n,2)+1)
    for value in literal.values():
        histogram[value]+=1
    assert histogram[1:]==[1]*comb(n,2)
    for k in range(2,n+1):
        T=comb(n-k+2,2)
        assert min(b+T-min(b,T) for b in (1,T,comb(n,2),comb(n,2)+1))==T
    assert sum(comb(n-k+2,2) for k in range(2,n+1))==comb(n+1,3)
    assert comb(n+1,3)-(n-1)**2==(n-1)*(n-2)*(n-3)//6
    return len(literal),letters


def image_audit(n):
    transition_rows=rows(n)
    initial=frozenset(range(n))
    seen,pending={initial},deque([initial])
    while pending:
        s=pending.popleft()
        for row in transition_rows:
            t=frozenset(row[q] for q in s)
            if t not in seen:
                seen.add(t)
                pending.append(t)
    assert len(seen)==2**n-1
    pair=distances(n)
    worst={k:0 for k in range(2,n+1)}
    for s in seen:
        if len(s)>=2:
            cost=min(pair[p] for p in combinations(sorted(s),2))
            worst[len(s)]=max(worst[len(s)],cost)
    for k in range(2,n+1):
        subset=sorted((j*n)//k for j in range(k))
        cost=min(pair[p] for p in combinations(subset,2))
        assert cost>=n*(n//k-1)+1
        assert worst[k]>=cost
        g,e=divmod(n,k)
        assert worst[k]==g*(n-k+e+1)
        gaps=[g]*(k-e)+[g+1]*e
        attaining=[0]
        for gap in gaps[:-1]:
            attaining.append(attaining[-1]+gap)
        assert min(pair[p] for p in combinations(attaining,2))==worst[k]
    lower=n*sum(n//k for k in range(1,n+1))-2*n*n+2*n-1
    assert sum(worst.values())>=lower
    assert (sum(worst.values())>(n-1)**2)==(n>=4)
    return dict(n=n,reachable_images=len(seen),worst_by_rank=worst,
                rank_sum=sum(worst.values()),spaced_lower_bound=lower,square=(n-1)**2)


def main():
    vertices=word_letters=0
    for n in range(2,251):
        a,b=validate(n,proposed(n),n<=40)
        vertices+=a
        word_letters+=b
    images=[image_audit(n) for n in range(2,17)]
    assert sum(Fraction(1,k) for k in range(1,33))>4
    rejected=0
    for corruption in ('plus','minus','missing'):
        candidate=proposed(8)
        if corruption=='missing':
            del candidate[(0,7)]
        else:
            candidate[(0,7)]+=1 if corruption=='plus' else -1
        try:
            validate(8,candidate)
        except AssertionError:
            rejected+=1
        else:
            raise AssertionError('accepted corrupted pair annotation')
    report=dict(verified=True,state_sizes=[2,250],pair_vertices=vertices,
                independently_simulated_word_letters=word_letters,
                images=images,total_reachable_images=sum(r['reachable_images'] for r in images),
                corruptions_rejected=rejected,
                independent='ordinary original-pair reverse BFS, literal word action and complete ordinary reachable-image BFS',
                scope='finite audits only; all-n exact window and worst-rank barriers have separate paper proofs')
    Path('scripts/direct_attack/data/terminal_window_barrier_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='images'}))


if __name__=='__main__':
    main()
