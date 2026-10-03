"""Original shrinking-return reset program, not an all-word lower proof."""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path
from direct_attack.compress_other_family import transitions


def digest(value):return sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def act(rows,word,states):
    current=list(states)
    for a in word:current=[rows[a][q] for q in current]
    return current


def program(p):
    return [1,0]*p+[0,1]*(p-1)+[0]*4+[1,0]*(p-2)+sum(([0]+[1,0]*j for j in range(2*p-2,p-1,-1)),[])+[0,1]*p


def full_subsets(rows):
    n=len(rows[0]);Q=(1<<n)-1;distance={Q:0};todo=deque([Q]);minimum=None
    while todo:
        S=todo.popleft()
        if S.bit_count()==1:minimum=min(minimum,distance[S]) if minimum is not None else distance[S]
        for f in rows:
            T=0;rest=S
            while rest:b=rest&-rest;rest-=b;T|=1<<f[b.bit_length()-1]
            if T not in distance:distance[T]=distance[S]+1;todo.append(T)
    return dict(rt=minimum,reachable_images=len(distance))


def record(p):
    rs=transitions(p-2);n=3*p;R=list(range(0,2*p+1,2))+[1];r=p+2;ids={q:i for i,q in enumerate(R)}
    preparation=[1,0]*p+[0,1]*(p-1)+[0]*4+[1,0]*(p-2)
    prepared=sorted({ids[q] for q in act(rs,preparation,range(n))})
    assert prepared==list(range(p-1))+[p,p+1]
    base=act(rs,[0]+[1,0]*p,R);returns=[];current=base
    for j in range(p,2*p-1):
        row=[ids[q] for q in current];assert row==[(j-i)%r if i<p else (j+1)%r for i in range(r)]
        returns.append(row);current=act(rs,[1,0],current)
    reflection=[ids[q] for q in act(rs,[0]*3+[1,0]*(p-2),R)]
    assert reflection==[(p-2-i)%r for i in range(r)]
    S=set(prepared);chain=[sorted(S)]
    for row in returns[::-1]:S={row[i] for i in S};chain.append(sorted(S))
    assert S=={p,p+1} and act(rs,[0,1]*p,[R[i] for i in sorted(S)])==[2,2]
    literal=program(p) if p<=24 else None
    if literal is not None:assert len(literal)==3*p*p+4*p-1 and set(act(rs,literal,range(n)))=={2}
    small=full_subsets(rs) if p<=7 else None
    if small:assert small['rt']==3*p*p+4*p-1
    return dict(p=p,n=n,rows_sha256=digest(rs),core_states=R,prepared_image_positions=prepared,
                returns_sha256=digest(returns),reflection_sha256=digest(reflection),shrinking_chain_sha256=digest(chain),
                reflection_original_length=2*p-1,preparation_original_length=6*p-2,
                reset_original_length=3*p*p+4*p-1,reset_endpoint=2,literal_word=literal,small_full_subset_scope=small,
                status='PROVED paper reset upper for EVERY p>=3; all-p exact ordinary threshold CONJECTURED')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('direct_attack/data/compress_other_short_reset.json'));args=ap.parse_args()
    records=[record(p) for p in list(range(3,65))+[100,128,256,512,1024]]
    out=dict(records=records,boundary='PROVED paper EVERY p>=3 reset upper3p^2+4p-1 and ACTUAL reflection a^3(ba)^(p-2) on core R, all original word costs paid. Exact all-p ordinary reset threshold CONJECTURED; specified-state4p proof unchanged. Only finite recorded scopes COMPUTATIONALLY VERIFIED; priority and general Cerny OPEN; no formal instantiation.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(parameters=len(records),maximum_n=max(z['n'] for z in records),small=[z['small_full_subset_scope'] for z in records if z['small_full_subset_scope']],boundary=out['boundary'])),flush=True)


if __name__=='__main__':main()
