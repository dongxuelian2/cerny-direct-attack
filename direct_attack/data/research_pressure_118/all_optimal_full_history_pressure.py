"""Explore ALL shortest inverse paths, pruning by exact finite-field subspaces."""
from collections import deque
from fractions import Fraction
import json,time
from pathlib import Path
from direct_attack.compress_other_family import transitions

MOD=1000003

def add_basis(basis,mask,n):
    row=[int(mask>>q&1) for q in range(n)]
    for old in basis:
        p=next(q for q,x in enumerate(old) if x)
        a=row[p]
        if a:row=[(x-a*y)%MOD for x,y in zip(row,old)]
    p=next((q for q,x in enumerate(row) if x),None)
    if p is None:return basis
    z=pow(row[p],MOD-2,MOD);row=tuple(x*z%MOD for x in row)
    result=[]
    for old in basis:
        a=old[p];result.append(tuple((x-a*y)%MOD for x,y in zip(old,row)))
    result.append(row)
    return tuple(sorted(result,key=lambda old:next(q for q,x in enumerate(old) if x)))

def rational_rank(masks,n):
    basis={}
    for mask in masks:
        row=[Fraction(int(mask>>q&1)) for q in range(n)]
        for p,old in sorted(basis.items()):
            if row[p]:z=row[p];row=[x-z*y for x,y in zip(row,old)]
        p=next((q for q,x in enumerate(row) if x),None)
        if p is not None:z=row[p];basis[p]=[x/z for x in row]
    return len(basis)

def analyse(rows,name,deadline):
    n=len(rows[0]);Q=(1<<n)-1;inv=[];pred=[[] for _ in range(Q+1)]
    for a,f in enumerate(rows):
        masks=[sum(1<<q for q,t in enumerate(f) if t==x) for x in range(n)]
        table=[0]*(Q+1)
        for S in range(1,Q+1):b=S&-S;table[S]=table[S^b]|masks[b.bit_length()-1]
        inv.append(table)
        for S,T in enumerate(table):pred[T].append(S)
    dd={Q:0};todo=deque([Q])
    while todo:
        T=todo.popleft()
        for S in pred[T]:
            if S not in dd:dd[S]=dd[T]+1;todo.append(S)
    targets=[1<<q for q in range(n) if (1<<q) in dd]
    if not targets:return dict(name=name,n=n,synchronizing=False)
    rt=min(dd[S] for S in targets);threshold=(rt+n-2)//(n-1);failed=set();nodes=0;cuts=0
    def dfs(S,basis,path,history):
        nonlocal nodes,cuts
        if time.monotonic()>deadline:raise TimeoutError
        nodes+=1
        if len(basis)>threshold:cuts+=1;return None
        if S==Q:
            d=rational_rank(history,n)
            if rt>(n-1)*(d-1):return dict(word=path[::-1],history=history,rank=d,field_rank=len(basis),rt=rt,rows=rows)
            return None
        key=(S,basis)
        if key in failed:return None
        for a,T in enumerate(f[S] for f in inv):
            if dd.get(T)!=dd[S]-1:continue
            answer=dfs(T,add_basis(basis,T,n),path+[a],history+[T])
            if answer is not None:return answer
        failed.add(key)
        return None
    for S in targets:
        if dd[S]!=rt:continue
        basis=add_basis(add_basis((),Q,n),S,n)
        result=dfs(S,basis,[],[S])
        if result:return dict(name=name,n=n,counter=result)
    return dict(name=name,n=n,rt=rt,counter_dimension_threshold=threshold,all_optimal_paths_excluded=True,
                memo_states=len(failed),dfs_nodes=nodes,dimension_prunes=cuts,optimal_targets=sum(dd[S]==rt for S in targets))

def main():
    start=time.monotonic();deadline=start+90;records=[]
    cases=[]
    for n in (4,5,6):
        for p in sorted(Path(f'direct_attack/data/n{n}_extremal').glob('*.certificate.json')):
            z=json.loads(p.read_text(encoding='utf-8'));cases.append((str(p),z['automaton']['transitions']))
    for n in range(3,13):
        a=list(range(1,n))+[0];b=list(range(n));b[-1]=0;cases.append((f'Cerny{n}',[a,b]))
        b=list(range(1,n))+[1];cases.append((f'Wielandt{n}',[a,b]))
    for p in (3,4,5):cases.append((f'completed_public_p{p}',transitions(p-2)))
    for n in (6,8,10,12):
        a=list(range(1,n))+[0];b=list(range(n));b[n//2]=0
        for j in range(1,n//2):
            c=list(range(n));c[0],c[j]=j,0;cases.append((f'antipodal_unit_transposition_n{n}_j{j}',[a,b,c]))
    completed=True
    for name,rs in cases:
        try:z=analyse(rs,name,deadline)
        except TimeoutError:completed=False;print(json.dumps(dict(timeout_case=name)),flush=True);break
        records.append(z);print(json.dumps(z),flush=True)
        if 'counter' in z:break
    out=dict(records=records,completed_planned_cases=completed,planned_cases=len(cases),seconds=time.monotonic()-start,
             modulus=MOD,boundary='exploratory only; ALL-path finite-field pruning is sound for rejecting a rational low-dimension candidate, but not independently audited and no universal cost/dimension claim')
    Path('direct_attack/native_build/all_optimal_full_history_pressure.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(completed=len(records),planned=len(cases),seconds=out['seconds'],counter=any('counter' in z for z in records))),flush=True)

if __name__=='__main__':main()
