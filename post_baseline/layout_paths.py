"""Concrete subset enumeration with witnesses for arbitrary information layouts."""
import argparse
from collections import deque
import json
from pathlib import Path


def solve(n,hidden):
    full=(1<<n)-1
    observed=full^sum(1<<q for q in hidden)
    def feature(s):
        return (s.bit_count(),s&observed)
    reverse={}
    witness={}
    for s in range(1,full+1):
        source=feature(s)
        for letter,image in [('a',((s<<1)&full)|(s>>(n-1))),
                             ('b',(s&((1<<(n-1))-1))|(s>>(n-1)))]:
            target=feature(image)
            reverse.setdefault(target,set()).add(source)
            witness.setdefault((source,target),(letter,s,image))
    d={feature(1<<q):0 for q in range(n)}
    queue=deque(d)
    successor={}
    while queue:
        target=queue.popleft()
        for source in sorted(reverse[target]):
            if source not in d:
                d[source]=d[target]+1
                successor[source]=target
                queue.append(source)
    start=feature(full)
    states=[start]
    steps=[]
    while d[states[-1]]:
        source=states[-1]
        target=successor[source]
        letter,s,image=witness[source,target]
        assert feature(s)==source and feature(image)==target
        steps.append(dict(letter=letter,witness_subset=s,image=image))
        states.append(target)
    return dict(n=n,hidden=sorted(hidden),B=d[start],states=states,steps=steps,
                method='complete concrete subset enumeration')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--n',type=int,default=8)
    p.add_argument('--hidden',type=int,nargs='+',default=[1,7])
    p.add_argument('--out')
    args=p.parse_args()
    assert len(set(args.hidden))==len(args.hidden)
    assert all(0<=q<args.n for q in args.hidden)
    data=solve(args.n,args.hidden)
    if args.out:
        Path(args.out).write_text(json.dumps(data,separators=(',',':'))+'\n',
                                  encoding='utf-8',newline='\n')
    print('B',data['B'],'word',''.join(x['letter'] for x in data['steps']))
    for (k,x),step in zip(data['states'],data['steps']+[{}]):
        print(k,format(x,f'0{args.n}b'),step.get('letter','goal'))


if __name__=='__main__':
    main()
