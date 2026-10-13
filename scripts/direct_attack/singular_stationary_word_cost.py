"""Exact finite controls of the weaker stationary-support cost obstruction."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


def rows(n):return [list(range(1,n))+[0],list(range(n-1))+[0]]


def short_words(n):
    a,b=rows(n);h=list(range(n-2,-1,-1))+[n-1];level=[(list(range(n)),0,False)];stream=sha256();hist={};words=0
    for length in range(n):
        next_level=[]
        for image,runs,last_b in level:
            value=sum(h[x]-h[q] for q,x in enumerate(image));assert value==-runs
            hist[value]=hist.get(value,0)+1;words+=1
            counts=Counter(image)
            stream.update(json.dumps([length,[counts[q] for q in range(n)],runs,value],separators=(',',':')).encode()+b'\n')
            if length<n-1:
                next_level.append(([a[x] for x in image],runs,False))
                next_level.append(([b[x] for x in image],runs+(not last_b),True))
        level=next_level
    assert words==(1<<n)-1
    return dict(n=n,maximum_word_length=n-1,words=words,potential=h,
                functional_histogram={str(k):hist[k] for k in sorted(hist)},semantic_sha256=stream.hexdigest())


def attainment(n):
    fs=rows(n);summed=[[0]*n for _ in range(n)];words=[]
    for k in range(n):
        word=[1]+[0]*k;image=list(range(n))
        for a in word:image=[fs[a][q] for q in image]
        for q,p in enumerate(image):summed[q][p]+=1
        words.append(word)
    assert all(value==1 for row in summed for value in row)
    reset=([1]+[0]*(n-1))*(n-2)+[1];image=set(range(n));stages=[]
    for a in reset:image={fs[a][q] for q in image};stages.append(len(image))
    assert image=={0} and len(reset)==(n-1)**2
    return dict(n=n,rows=fs,support_words=words,weights_denominator=n,maximum_support_length=n,
                matrix_numerator_sha256=sha256(json.dumps(summed,separators=(',',':')).encode()).hexdigest(),
                literal_support_letter_controls=n*n*(n+1)//2,reset_word=reset,reset_length=len(reset),
                reset_rank_history=stages,reset_image=[0])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/singular_stationary_word_cost.json'));args=ap.parse_args()
    out=dict(short_words=[short_words(n) for n in range(2,17)],attainment=[attainment(n) for n in list(range(2,33))+[64,127,257]],
             projected_stationary_example=dict(n=5,rows=[[4,0,4,0,0],[1,2,2,1,4],[1,3,3,1,0]],normal=[1,1,-1,-1,0],marked_state=4,dimension=4,weights_numerators=[1,1,1],weights_denominator=3,reset_word=[0,1,0],reset_threshold=3,full_original_stationarity_possible=False),
             boundary='PROVED paper ALL n>=2: at costs<=n-1, full-Q stationary nonnegative average cannot positively use ANY singular word in Cerny automata; sharp maximum support cost n with synchronizing support. Weak full-row condition, not required J/n. Expected cost can approach0. No general Cerny proof, no novelty claim, no formal verification.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(short_word_scopes=len(out['short_words']),all_literal_words=sum(z['words'] for z in out['short_words']),attainment_scopes=len(out['attainment']),maximum_attainment_n=257,boundary=out['boundary'])),flush=True)


if __name__=='__main__':main()
