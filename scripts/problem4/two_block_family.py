"""Uniform binary two-block witnesses, original-letter certificates only."""
from collections import deque
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def apply(states,word,rows):
    for letter in word:states={rows["ab".index(letter)][q] for q in states}
    return set(states)

def reset_word(rows):
    image=set(range(len(rows[0])));answer=[]
    while len(image)>1:
        first=frozenset(sorted(image)[:2]);queue=deque([first]);words={first:""}
        while queue:
            pair=queue.popleft()
            if len(pair)==1:
                word=words[pair];break
            for letter,row in zip("ab",rows):
                T=frozenset(row[q] for q in pair)
                if T not in words:words[T]=words[pair]+letter;queue.append(T)
        else:raise AssertionError("nonmergeable pair")
        image=apply(image,word,rows);answer.append(word)
    return "".join(answer)

def construct(p,t,r):
    assert t>=2 and 1<=r<=p-3
    n=p+2*t+1;s=p+t
    a=list(range(n));a[p-2],a[p-1]=p-1,p-2
    U=list(range(p,n))
    for q,v in zip(U,U[1:]+U[:1]):a[q]=v
    b=list(range(n));b[0]=p+t
    for q in range(1,p):b[q]=q-1
    for j in range(2*t):b[p+j]=p-1 if j in (t-1,2*t-1) else p+j+1
    rows=[a,b];S=list(range(s));A=list(range(r))
    e=("a"*(2*t)+"b"*s)*t
    reaching="b"*t+e+"a"*(t+1)
    value=min(n-r,3*t+2)
    attaining=("a"*(2*t)+"ba"+"b"*(p-r-1) if n-r<=3*t+2
               else "a"*(2*t)+"b"+"a"*t+"b")
    return dict(p=p,t=t,n=n,s=s,r=r,rows=rows,S=S,A=A,value=value,
                reaching=reaching,attaining=attaining,reset=reset_word(rows),
                retraction=e,source="Uniform two-block construction")

def main():
    parameters={(p,t,r) for t in range(2,10) for p in range(4,t+5)
                for r in range(1,p-2)}
    parameters.update((p,t,r) for p,t,r in ((4,20,1),(24,20,1),(24,20,21),
                                          (34,15,1),(34,15,31),(8,4,3)))
    records=[construct(p,t,r) for p,t,r in sorted(parameters,key=lambda z:(z[1],z[0],z[2]))]
    data=dict(records=records,instances=len(records),maximum_n=max(z["n"] for z in records),
              scope="Finite implementation certificates for the uniform proof in PROOF.md#problem4-two-block-proof and the manuscript.")
    (ROOT/"two_block_certificates.json").write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps({key:data[key] for key in ("instances","maximum_n")}))

if __name__=="__main__":main()
