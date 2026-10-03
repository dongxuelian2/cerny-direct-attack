"""Read no constructor: validate explicit transitions, words, layers and ordinary full arrays."""
from collections import deque
from pathlib import Path
import json
from direct_attack.ordinary_reverse_policy import profile as ordinary

ROOT=Path('direct_attack/data/gonze_bypass')

def main():
    cases=json.loads((ROOT/'cases.json').read_text());records=[]
    for c in cases:
        n=c['n'];a,b,z=c['rows'];Q=frozenset(range(n));m=(n-3)//4;k=(n-5)//2
        assert n>=7 and n%4==3 and c['target']==sorted(Q-{k+1,k+3})
        assert sorted(a)==sorted(b)==list(range(n))
        assert z==[0,2,2,0]+list(range(4,n)) and len(set(z))==n-2
        assert a[:4]==[1,2,3,0] and b[:4]==[5,1,4,3]
        # Direct matching-edge description, independent of the two-state insertion recursion.
        aa=[1,2,3,0]+list(range(4,n));bb=list(range(n));bb[0],bb[5]=5,0;bb[2],bb[4]=4,2
        for start in [4,5]:
            for step,q in enumerate(range(start,n-2,2)):
                r=aa if step%2==0 else bb;r[q],r[q+2]=q+2,q
        assert aa==a and bb==b
        g=[b[a[q]] for q in range(n)];cycle=[];q=0
        while q not in cycle:cycle.append(q);q=g[q]
        assert q==0 and len(cycle)==n and cycle.index(2)==(n+1)//2
        def apply(T,word):
            for i in word:
                assert type(i)==int and 0<=i<3;T=frozenset(c['rows'][i][q] for q in T)
            return T
        word=c['bypass_word'];assert word==[2,0]+[1,0]*m+[2]+[i%2 for i in range(m)]
        T=Q;trajectory=[sorted(T)]
        for i in word:T=apply(T,[i]);trajectory.append(sorted(T))
        assert trajectory==c['bypass_trajectory'] and sorted(T)==c['bypass_target']
        assert len(T)==n-4 and T<=set(c['target']) and len(word)==c['bypass_length']==3*(n+1)//4
        assert apply(Q,c['reset_word'])==frozenset([0])
        assert c['reset_word']==[2,0,1,0,1]*(m+2)+[2,0,1]*(2*m-1)+[2]
        assert len(c['reset_word'])==(11*n-1)//4
        inverse={0};reset=[]
        for phase in c['ordinary_inverse_phases']:
            assert phase['target']==sorted(inverse)
            U={q for q in Q if apply({q},phase['word'])<=inverse}
            assert phase['preimage']==sorted(U) and len(U)>len(inverse)
            inverse=U;reset=phase['word']+reset
        assert inverse==set(Q) and reset==c['reset_word']
        # Unordered-pair BFS for exact reaching; no ordinary-image rank-range constructor import.
        d={frozenset([1,3]):0};queue=deque(d)
        while queue:
            pair=queue.popleft()
            for row in [a,b]:
                U=frozenset(row[q] for q in pair)
                if U not in d:d[U]=d[pair]+1;queue.append(U)
        assert len(d)==n*(n-1)//2
        cost=1+d[Q-frozenset(c['target'])]
        assert cost==c['exact_reaching']==(n*n+5*n)//4-6
        assert len(c['exact_word'])==cost and apply(Q,c['exact_word'])==frozenset(c['target'])
        records.append(dict(n=n,exact_reaching=cost,into_upper=len(word),bypass_rank=n-4,reset_length=len(reset)))
    arrays=json.loads((ROOT/'small_arrays.json').read_text());count=0
    for z in arrays:
        if z['n']>7:continue
        p=ordinary(z['rows']);assert p is not None;count+=1
        for key in ['extension','best','worst','forward']:assert z[key]=={str(S):v for S,v in p[key].items()}
        c=next(c for c in cases if c['n']==z['n']);mask=sum(1<<q for q in c['target'])
        assert z['extension'][str(mask)]==c['bypass_length']
        assert all(int(S).bit_count()!=z['n']-1 for S in z['forward'])
    report=dict(verified=True,records=records,ordinary_all_source_arrays=count,
                general_linear_extension_refutation=False,shortest_into_formula_all_n=False)
    (ROOT/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)

if __name__=='__main__':main()
