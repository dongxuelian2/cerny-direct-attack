"""Literal canonical policy chains; no previous policy solver imported."""
from collections import deque
from copy import deepcopy
from pathlib import Path
import json


def preimage(S,a,r):
    n=2*r
    if a==n-1:return (S&((1<<r)-1))|((S&((1<<r)-1))<<r)
    return S^(3<<a) if ((S>>a)^(S>>(a+1)))&1 else S


def weight(S,r):return sum(max(r+1-q,0) for q in range(2*r) if S>>q&1)


def weight_change(S,T,r):
    change=S^T;result=0
    while change:
        bit=change&-change;q=bit.bit_length()-1;change-=bit
        result+=(1 if T&bit else -1)*max(r+1-q,0)
    return result


def doubled(j,r):
    left=1|sum(1<<q for q in range(r-j+1,r))
    return left|(left<<r)


def shortest(S,r):
    n=2*r;full=(1<<n)-1;k=S.bit_count();todo=deque([S]);dist={S:0}
    while todo:
        T=todo.popleft()
        if T==full or (k<r and T.bit_count()>k):return dist[T],len(dist)
        for a in range(n):
            U=preimage(T,a,r)
            if U and U not in dist:dist[U]=dist[T]+1;todo.append(U)
    raise AssertionError()


def record(r):
    n=2*r;full=(1<<n)-1;cost=1;stages=[]
    S=preimage(1,n-1,r);assert S==doubled(1,r);actual=S
    if r==1:return dict(r=r,n=n,cost=1,stages=[],terminal_start=full,terminal_cost=0)
    j=1
    while S.bit_count()<r:
        inverse_letters=list(range(r-j,r))+[n-1]
        T=S
        for a in inverse_letters:T=preimage(T,a,r)
        for a in inverse_letters:actual=preimage(actual,a,r)
        assert T==doubled(j+1,r) and weight(T,r)-weight(S,r)==len(inverse_letters)==j+1
        R=T
        if T.bit_count()>r:
            removed=next(q for q in range(r+1,n) if T>>q&1)
            assert max(r+1-removed,0)==0
            R=T^(1<<removed)
        assert R.bit_count()>S.bit_count() and R.bit_count()<=r and R&~T==0
        assert R&~actual==0
        stages.append(dict(target=S,target_size=S.bit_count(),cost=j+1,parent=R,inverse_letters=inverse_letters))
        cost+=j+1;S=R;j+=1
    assert S.bit_count()==r and S&1 and S>>r&1
    terminal_start=S;terminal_cost=0;terminal_word=[];left=(1<<r)-1
    while S!=full:
        holes=[i for i in range(r) if not S>>i&1]
        assert holes
        i=max(holes);assert i>0
        for a in list(range(i,r))+[n-1]:
            U=preimage(S,a,r);assert weight_change(S,U,r)==1
            actual=preimage(actual,a,r)
            terminal_word.append(a);terminal_cost+=1;S=U
    assert actual==full
    assert terminal_cost==weight(full,r)-weight(terminal_start,r)
    cost+=terminal_cost;assert cost==r*(r+1)//2
    z=dict(r=r,n=n,cost=cost,stages=stages,terminal_start=terminal_start,terminal_cost=terminal_cost,
           terminal_inverse_letters=len(terminal_word),terminal_final=full,
           rt=r*(r+1)//2,global_policy_equals_rt=True)
    if r<=24:z['literal_terminal_inverse_word']=terminal_word
    return z


def verify(z):
    expected=record(z['r']);assert z==expected
    assert z['cost']==z.get('rt',1) and z.get('global_policy_equals_rt',True)


def main():
    data=Path('scripts/direct_attack/data');family=json.loads((data/'transposition_fold_obstruction.json').read_text())
    controls=[record(z['r']) for z in family['records']]
    for z in controls:verify(z)
    exact=[];vertices=0
    for r in range(2,8):
        z=record(r)
        for stage in z['stages']:
            d,count=shortest(stage['target'],r)
            assert d==stage['cost'];vertices+=count
            exact.append(dict(r=r,target_size=stage['target_size'],cost=d,vertices=count))
        d,count=shortest(z['terminal_start'],r)
        assert d==z['terminal_cost'];vertices+=count
        exact.append(dict(r=r,terminal=True,target_size=r,cost=d,vertices=count))
    corruptions=[];base=record(6)
    for field in ('cost','terminal_start','terminal_cost','stages'):
        z=deepcopy(base)
        if field=='stages':z[field][0]['parent']^=1
        else:z[field]-=1
        try:verify(z)
        except AssertionError:corruptions.append(field)
        else:raise AssertionError('accepted corrupted '+field)
    report=dict(verified=True,controls=controls,exact_shortest_phase_scopes=exact,exact_vertices=vertices,
                corruptions_rejected=corruptions,
                status='PROVED paper global P=rt for the entire fold/path family; bounded original-word and phase-BFS audits COMPUTATIONALLY VERIFIED; general policy square and Cerny OPEN; no formal verification')
    (data/'fold_policy_chains_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,controls=len(controls),exact_phase_scopes=len(exact),exact_vertices=vertices,
                          corruptions_rejected=len(corruptions))),flush=True)


if __name__=='__main__':main()
