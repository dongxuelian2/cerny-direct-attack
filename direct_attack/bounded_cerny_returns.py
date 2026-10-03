"""Exact paid bounded-return controls for the ordinary Cerny family."""
import heapq,json
from pathlib import Path

def images(row):
    out=[0]*(1<<len(row))
    for S in range(1,len(out)):
        bit=S&-S;out[S]=out[S^bit]|1<<row[bit.bit_length()-1]
    return out

def distances(rows,costs):
    n=len(rows[0]);tables=[images(f) for f in rows];rev=[[] for _ in range(1<<n)]
    for i,table in enumerate(tables):
        for S,T in enumerate(table):rev[T].append((S,costs[i]))
    d=[None]*len(rev);heap=[]
    for S in range(len(rev)):
        if S.bit_count()<=1:d[S]=0;heap.append((0,S))
    heapq.heapify(heap)
    while heap:
        v,T=heapq.heappop(heap)
        if v!=d[T]:continue
        for S,c in rev[T]:
            if d[S] is None or v+c<d[S]:d[S]=v+c;heapq.heappush(heap,(v+c,S))
    return d,tables

def witness(d,tables,costs):
    S=len(d)-1;word=[]
    if d[S] is None:return None
    while S.bit_count()>1:
        for i,table in enumerate(tables):
            T=table[S]
            if d[T] is not None and d[S]==costs[i]+d[T]:word.append(i);S=T;break
        else:raise AssertionError('missing descent')
    return word

def main():
    records=[]
    for n in range(4,15):
        M=n-1;rows=[[1]+list(range(1,n)),list(range(1,n))+[0]]
        original,_=distances(rows,[1,1]);bcount,_=distances(rows,[0,1])
        known=[0]+([1]*M+[0])*(M-1)
        assert original[-1]==M*M and bcount[-1]==M*(M-1)
        caps=[]
        for K in range(1,M+1):
            returns=[]
            for j in range(K+1):
                returns.append([(1 if (q+j)%n==0 else (q+j)%n)-1 for q in range(1,n)])
            costs=list(range(1,K+2));d,tables=distances(returns,costs)
            word=witness(d,tables,costs)
            if K==1:assert d[-1] is None
            elif K<M:assert d[-1]+1>M*M
            else:assert d[-1]+1==M*M
            caps.append(dict(K=K,rows=returns,costs=costs,distances=d,word=word,
                             lower=M*(M-1)+(M*(M-1)+K-1)//K+1))
        records.append(dict(n=n,rows=rows,original_distances=original,b_distances=bcount,
                            known_word=known,caps=caps))
    out=dict(records=records,boundary='Finite ALL subset costs for Cerny n4..14 and ALL return caps1..n-1. Paper every-n b-count lower bound and bounded-return obstruction are separately PROVED, with explicit known-proof attribution and no novelty or formal claim. The general Cerny conjecture remains OPEN.')
    Path('direct_attack/data/bounded_cerny_returns.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(parameters=len(records),caps=sum(len(z['caps']) for z in records),
                         n4_entered_all_three=records[0]['caps'][1]['distances'][-1]+1,
                         cap2_entered_costs=[z['caps'][1]['distances'][-1]+1 for z in records],boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
