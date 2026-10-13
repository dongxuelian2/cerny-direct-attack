"""Bounded fixed-first-letter SAT scans; no negative theorem is inferred."""
import argparse
import json
from pathlib import Path
from synthesize_pair_cover import solve

def partitions(n,least=1):
    if not n:yield ();return
    for k in range(least,n+1):
        for tail in partitions(n-k,k):yield (k,)+tail

def first_maps(n,m):
    records=[]
    for h in range(1,m+1):
        for L in range(1,n-h+1):
            for parts in partitions(n-h-L):
                row=list(range(n))
                for q in range(h+L-1):row[q]=q+1
                row[h+L-1]=h;base=h+L
                for k in parts:
                    for q in range(k):row[base+q]=base+(q+1)%k
                    base+=k
                records.append(dict(h=h,L=L,parts=parts,first=row,active=sum(row[q]!=q for q in range(n))))
    return sorted(records,key=lambda z:(-z['active'],-z['L'],z['h'],z['parts']))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('n',type=int);ap.add_argument('s',type=int);ap.add_argument('target',type=int)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--start',type=int,default=0);ap.add_argument('--count',type=int,default=20)
    ap.add_argument('--timeout-ms',type=int,default=3000);ap.add_argument('--iterations',type=int,default=8)
    args=ap.parse_args();cases=first_maps(args.n,args.n-args.s);records=[]
    for i in range(args.start,min(len(cases),args.start+args.count)):
        case=cases[i];result=solve(case['first'],args.s,args.target,args.timeout_ms,args.iterations)
        records.append(dict(index=i,**case,result=result))
        args.out.write_text(json.dumps(dict(n=args.n,s=args.s,target=args.target,total_first_classes=len(cases),
                                           scope='Bounded solver calls; not a completed negative cover.',records=records),indent=2)+'\n',encoding='utf-8')
        print(json.dumps(dict(index=i,h=case['h'],L=case['L'],parts=case['parts'],status=result['status'],iterations=result['iterations'],seconds=result['seconds'],
                              protected=(result['witness'] or {}).get('protected'))),flush=True)
        if result['witness']:break

if __name__=='__main__':main()
