"""Complete small scheduling enumeration and large-buffer witness verification."""
from uniform_construction import clocks
import json
from pathlib import Path


def schedules(r):
    latest=clocks(r)
    K=r+1
    L=(r-1).bit_length()-1
    p=1<<L
    C=L*r-2*p
    def extend(prefix):
        i=len(prefix)+1
        if i>K:
            yield prefix
            return
        lower=prefix[-1]+2 if prefix else 0
        if i>=2:
            lower=max(lower,prefix[i//2-1]+r+i%2)
        fixed=(i&(i-1)==0 and i<=p) or i>=p
        choices=[C+2*i if i>=p else (i.bit_length()-1)*r] if fixed else range(lower,latest[i-1]+1)
        for t in choices:
            if lower<=t<=latest[i-1]:
                yield from extend(prefix+[t])
    yield from extend([])


def witness(r,s,m):
    assert m>=r+2
    core_end=s[-1]
    events=set(s+[core_end+2*i for i in range(1,m-1)])
    end=core_end+2*(m-2)
    full=(1<<r)-1
    j,x=0,1
    for t in range(end+1):
        if t:
            u=int(t in events)
            assert u<=j<=m-1+u,(r,m,s,t,j,u)
            j=j-u+(x>>(r-1))
            x=((x<<1)&full)|u
        if t in events:
            assert x&3==1,(r,m,s,t,x&3)
            x|=2
    assert (j,x)==(m,full),(r,m,s,j,x)


def accepted(r,s,m):
    # Complete reverse graph propagation: unpaired inputs are allowed.
    A=s[-1]
    events=set(s+[A+2*i for i in range(1,m-1)])
    full=(1<<r)-1
    states={(0,1)}
    for t in range(A+2*(m-2)+1):
        if t:
            candidates=set()
            for j,x in states:
                for u in (0,1):
                    if u<=j<=m-1+u:
                        candidates.add((j-u+(x>>(r-1)),((x<<1)&full)|u))
            states=candidates
        if t in events:
            states={(j,x|2) for j,x in states if x&3==1}
        if not states:
            return False
    return (m,full) in states


def main():
    total=0
    rows=[]
    for r in range(2,17):
        count=0
        accepted_counts=[0]*(r+1)
        for s in schedules(r):
            witness(r,s,r+2)
            witness(r,s,r+5)
            count+=1
            for m in range(2,r+3):
                accepted_counts[m-2]+=accepted(r,s,m)
        total+=count
        assert all(a<=b for a,b in zip(accepted_counts,accepted_counts[1:]))
        assert accepted_counts[-1]==count
        M=accepted_counts.index(count)+2
        rows.append(dict(r=r,W=count,capacities=list(range(2,r+3)),
                         accepted_counts=accepted_counts,minimum_stabilization=M,
                         status='COMPUTATIONALLY VERIFIED complete finite language enumeration'))
        print('r',r,'W',count,'M',M,'counts',accepted_counts,flush=True)
    print('Total schedules with both guaranteed-capacity witnesses:',total)
    Path('post_baseline/sprint_results/optimal_languages_r2_16.json').write_text(
        json.dumps(rows,indent=2)+'\n',encoding='utf-8',newline='\n')


if __name__=='__main__':
    main()
