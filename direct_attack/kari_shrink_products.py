"""Coordinate products: unavoidable inverse decreases and exact cost/loss tradeoff."""
from collections import deque
from hashlib import sha256
from heapq import heappop,heappush
import json
from pathlib import Path
from direct_attack.kari_inverse_shrink import ROWS,pred

ROOT=Path(__file__).resolve().parents[1]

def distance(target,monotone=False):
    reverse=[[] for _ in range(64)]
    for S in range(64):
        for i,f in enumerate(ROWS):
            T=pred(S,f)
            if not monotone or T.bit_count()>=S.bit_count():reverse[T].append(S)
    out=[None]*64;out[target]=0;todo=deque([target])
    while todo:
        T=todo.popleft()
        for S in reverse[T]:
            if out[S] is None:out[S]=out[T]+1;todo.append(S)
    return out

def route(S,target,d,monotone=False):
    word=[]
    while S!=target:
        for i,f in enumerate(ROWS):
            T=pred(S,f)
            if d[T] is not None and d[S]==d[T]+1 and (not monotone or T.bit_count()>=S.bit_count()):
                word.append(i);S=T;break
        else:raise AssertionError('route absent')
    return word

def execute(d,blocks,phases):
    masks=[16]*d;card=1;maxloss=shrinks=cost=0;labels=[]
    for c,phase in blocks:
        for i in phases[phase]:
            old=masks[c].bit_count();T=pred(masks[c],ROWS[i]);new=T.bit_count();assert old and new
            nextcard=card//old*new;maxloss=max(maxloss,card-nextcard);shrinks+=nextcard<card
            card=nextcard;masks[c]=T;cost+=1;labels.append(2*c+i)
    assert masks==[63]*d and card==6**d
    return dict(cost=cost,shrinks=shrinks,maxloss=maxloss,final_card=card,
                inverse_word_sha256=sha256(json.dumps(labels,separators=(',',':')).encode()).hexdigest())

def rectangle_d2():
    cardinal=lambda S:(S%64).bit_count()*(S//64).bit_count()
    reverse=[[] for _ in range(4096)]
    for S in range(4096):
        x,y=S%64,S//64
        for c in range(2):
            for i,f in enumerate(ROWS):
                T=pred(x,f)+64*y if c==0 else x+64*pred(y,f)
                reverse[T].append((S,max(0,cardinal(S)-cardinal(T))))
    out={}
    for cap in (None,2,3,4):
        d=[None]*4096;d[4095]=0;todo=deque([4095])
        while todo:
            T=todo.popleft()
            for S,loss in reverse[T]:
                if (cap is None or loss<=cap) and d[S] is None:d[S]=d[T]+1;todo.append(S)
        out['ordinary' if cap is None else 'cap'+str(cap)]=d
    lex=[None]*4096;lex[4095]=(0,0);heap=[(0,0,4095)]
    while heap:
        shrinks,cost,T=heappop(heap)
        if lex[T]!=(shrinks,cost):continue
        for S,loss in reverse[T]:
            if loss>3:continue
            z=(shrinks+int(loss>0),cost+1)
            if lex[S] is None or z<lex[S]:lex[S]=z;heappush(heap,(*z,S))
    out['cap3_lex']=lex
    seeds=[(1<<q)+64*(1<<r) for q in range(6) for r in range(6)]
    assert min(out['ordinary'][S] for S in seeds)==50
    assert all(out['cap2'][S] is None for S in seeds)
    assert min(out['cap3'][S] for S in seeds if out['cap3'][S] is not None)==52
    assert min(out['cap4'][S] for S in seeds if out['cap4'][S] is not None)==50
    assert min(lex[S] for S in seeds if lex[S] is not None)==(3,52)
    return out

def main():
    old=json.loads((ROOT/'direct_attack/data/kari_inverse_shrink.json').read_text())
    inverse=list(reversed(old['word']));S=16;neg=[]
    for j,i in enumerate(inverse):
        T=pred(S,ROWS[i])
        if T.bit_count()<S.bit_count():neg.append(j)
        S=T
    assert neg==[19]
    to45=distance(45);full=distance(63);mono=distance(63,True)
    assert to45[16]==min(to45[1<<q] for q in range(6))==16 and mono[44]==10
    phases=dict(one_pre=inverse[:20],one_post=inverse[20:],
                two_pre=route(16,45,to45)+[0],two_post=route(44,63,mono,True))
    C=[S for S in range(64) if mono[S] is not None]
    bridge=[dict(S=S,T=pred(S,f),letter=i) for S in range(64) for i,f in enumerate(ROWS)
            if pred(S,f) in C and pred(S,f).bit_count()<S.bit_count()]
    records=[]
    for d in list(range(1,17))+[32,63,127,257]:
        short=[[c,'one_pre'] for c in range(d)]+[[c,'one_post'] for c in range(d)]
        loss=[[c,'two_pre'] for c in range(d-1)]+[[d-1,'one_pre']]+[[c,'two_post'] for c in range(d-1)]+[[d-1,'one_post']]
        records.append(dict(d=d,n=6**d,alphabet=2*d,shortest_blocks=short,minimax_blocks=loss,
                            shortest=execute(d,short,phases),minimax=execute(d,loss,phases),
                            literal_all_states=d<=4))
    out=dict(rows=ROWS,forward_cut=old['cut'],co_cut=C,last_negative_bridges=bridge,
             inverse_full_distances=full,to45_distances=to45,monotone_full_distances=mono,
             mono_suffixes=[dict(S=S,word=route(S,63,mono,True)) for S in C],
             seed=4,phases=phases,records=records,rectangle_d2=rectangle_d2(),
             boundary='PROVED paper ALL d>=1, independent-coordinate product n=6^d/alphabet2d: exact minimum inverse-shrink count d, ordinary rt25d, minimum maximum absolute inverse loss3^(d-1), optimum length among that loss policy27d-2 and minimum shrink count2d-1, optimum maximum loss among ordinary-shortest resets4^(d-1). Literal base all-word facts/bounds are Lean verified separately; arbitrary-d product lifting is paper, not formal. No novelty, fixed alphabet, corank-one or general Cerny proof claim.')
    (ROOT/'direct_attack/data/kari_shrink_products.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(parameters=len(records),literal_parameters=4,last_negative_bridges=bridge,
                         base_costs={k:len(v) for k,v in phases.items()},boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
