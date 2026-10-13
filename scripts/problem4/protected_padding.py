"""Binary protected-edge padding at codimension four."""
from collections import deque

def transform(states,word,rows):
    for letter in word:
        states={rows["ab".index(letter)][q] for q in states}
    return set(states)

def reset_word(rows):
    image=set(range(len(rows[0]))); answer=""
    while len(image)>1:
        start=frozenset(sorted(image)[:2]);todo=deque([start]);words={start:""};merge=None
        while todo:
            pair=todo.popleft()
            if len(pair)==1:
                merge=words[pair];break
            for letter,row in zip("ab",rows):
                T=frozenset(row[q] for q in pair)
                if T not in words:
                    words[T]=words[pair]+letter;todo.append(T)
        assert merge is not None
        image=transform(image,merge,rows);answer+=merge
    return answer

def construct(target,r):
    assert target in (10,11)
    k=r-(2 if target==10 else 1)
    assert k>=0
    n=12+k;s=8+k
    a=[0,1,2,4,3,6,7,8,9,10,11,5]+list(range(12,n))
    b=[8,0,1,2,3,6,7,4,9,10,4,11]+list(range(12,n))
    H=list(range(12,n))
    if H:
        b[0]=H[0]
        for q,t in zip(H,H[1:]+[8]):
            b[q]=t
    rows=[a,b]
    e=("a"*6+"b"*s)*3
    reaching="bbb"+e+"aaaa"
    A=[0]+([1] if target==10 else [])+H
    return dict(n=n,s=s,r=r,alphabet_size=2,rows=rows,S=list(range(8))+H,A=A,
                value=target,reaching=reaching,
                attaining="aaaaaababb" if target==10 else "aaaaaabaaab",
                reset=reset_word(rows),source="protected-edge padding, codimension four",
                root_retraction=e,core_cycle_length=s)
