"""Uniform binary lower construction at codimension three, n>=10."""
from collections import deque

def pair_word(rows, pair):
    start=frozenset(pair); todo=deque([start]); words={start:""}
    while todo:
        S=todo.popleft()
        if len(S)==1:
            return words[S]
        for letter,row in zip("ab",rows):
            T=frozenset(row[q] for q in S)
            if T not in words:
                words[T]=words[S]+letter; todo.append(T)
    raise ValueError("unmergeable pair")

def construct(n,r):
    L=n-5
    assert L>=5 and 1<=r<=L
    z,v,y,t,c,d=L-1,L,L+1,L+2,L+3,L+4
    a=list(range(n))
    a[z],a[y]=y,z
    a[c],a[d]=d,c
    a[t]=z
    b=list(range(1,L))+[0]+[y,c,v,t,d]
    rows=[a,b]
    S=list(range(L))+[v,t]
    A=list(range(L-1-r,L-1)) if r<L else list(range(L))
    value=min(n-r,9)
    attaining="ababbbaba" if value==9 else "ababa"+"b"*(value-5)
    image=set(range(n)); reset=""
    while len(image)>1:
        word=pair_word(rows,sorted(image)[:2])
        for letter in word:
            image={rows["ab".index(letter)][q] for q in image}
        reset+=word
    return dict(n=n,s=n-3,r=r,alphabet_size=2,rows=rows,S=S,A=A,
                value=value,reaching="abbbabaabb",attaining=attaining,
                reset=reset,source="uniform codimension-three gadget, L=n-5>=5")
