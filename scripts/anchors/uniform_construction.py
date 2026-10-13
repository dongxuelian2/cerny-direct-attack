"""Uniform, search-free exact witness for every r>=2, capacity2.

Paper proof: PROOF.md#anchors-all-parameter-proof. No solver/dependency required.
"""
import argparse
import json
from pathlib import Path


def clocks(r):
    assert r>=2
    L=(r-1).bit_length()-1
    C=L*r-(1<<(L+1))
    return [C+min((1<<(d+1))*i-d*r for d in range(r.bit_length()+1))
            for i in range(1,r+2)]


def reverse_witness(r):
    events=clocks(r)
    full=(1<<r)-1
    j,x=0,1
    states=[(j,x)]
    labels=[]
    eventset=set(events)
    for t in range(events[-1]+1):
        if t:
            u=int(t in eventset)
            assert u<=j<=1+u,(r,t,j,u)
            out=x>>(r-1)
            j=j-u+out
            x=((x<<1)&full)|u
            states.append((j,x))
            labels.append('a')
        if t in eventset:
            assert x&3==1
            x|=2
            states.append((j,x))
            labels.append('b')
    assert (j,x)==(2,full)
    return states,labels


def forward_witness(r,m=2):
    assert m>=2
    rev,labels=reverse_witness(r)
    states=list(reversed(rev))
    labels=list(reversed(labels))
    # Prefix baa padding in forward direction if hidden capacity exceeds2.
    full=(1<<r)-1
    prefix=[(m,full)]
    for j in range(m,2,-1):
        prefix.extend([(j,full&~2),(j,(full&~2)>>1|(1<<(r-1))),
                       (j-1,full)])
    return prefix[:-1]+states, ['b','a','a']*(m-2)+labels


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--r',type=int,default=33)
    p.add_argument('--m',type=int,default=2)
    p.add_argument('--out')
    args=p.parse_args()
    states,labels=forward_witness(args.r,args.m)
    h=(args.r-1).bit_length()
    value=3*(args.r+args.m)+(h-1)*args.r-(1<<h)-3
    assert len(labels)==value
    data={'r':args.r,'m':args.m,'n':args.r+args.m,'length':value,
          'clocks':clocks(args.r),'states':states,'labels':labels,
          'method':'uniform formula; no search'}
    if args.out:
        Path(args.out).write_text(json.dumps(data,separators=(',',':'))+'\n',
                                encoding='utf-8',newline='\n')
    print({k:v for k,v in data.items() if k not in ('states','labels','clocks')})


if __name__=='__main__':
    main()
