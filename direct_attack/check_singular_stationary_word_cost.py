"""Independent weighted-row propagation and literal support/reset certificates."""
import argparse
from collections import Counter
import copy
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def audit_words(z):
    n=z['n'];assert 2<=n<=16 and z['maximum_word_length']==n-1
    h=[n-2-q if q<n-1 else n-1 for q in range(n)];assert z['potential']==h
    level=[([1]*n,0,False)];hist=Counter();stream=sha256();words=0;strict=0
    for length in range(n):
        following=[]
        for counts,runs,last in level:
            assert sum(counts)==n
            value=sum((counts[q]-1)*h[q] for q in range(n));assert value==-runs
            if runs:assert value<0;strict+=1
            hist[value]+=1;words+=1
            stream.update(json.dumps([length,counts,runs,value],separators=(',',':')).encode()+b'\n')
            if length<n-1:
                following.append(([counts[-1]]+counts[:-1],runs,False))
                folded=counts[:];folded[0]+=folded[-1];folded[-1]=0
                following.append((folded,runs+(not last),True))
        level=following
    assert words==z['words']==(1<<n)-1 and strict==words-n
    assert z['functional_histogram']=={str(k):hist[k] for k in sorted(hist)} and z['semantic_sha256']==stream.hexdigest()
    # Independent ALL suffix paths on the distinguished pair, not full-row recursion.
    states=[(0,n-1,False,0)];pair_controls=0
    for length in range(n-1):
        next_states=[]
        for p,q,first_b,k in states:
            pair_controls+=1;difference=h[p]-h[q]
            if length==0:assert (p,q)==(0,n-1) and difference==-1
            elif first_b:assert p==q and difference==0
            else:assert 1<=k<=n-2 and (p,q)==(k,k-1) and difference==-1
            if length<n-2:
                next_states.append(((p+1)%n,(q+1)%n,first_b,k+1))
                next_states.append((0 if p==n-1 else p,0 if q==n-1 else q,first_b or length==0,k))
        states=next_states
    assert pair_controls==(1<<(n-1))-1
    return words,pair_controls,strict


def literal(fs,word):
    images=list(range(len(fs[0])))
    for a in word:images=[fs[a][p] for p in images]
    return images


def audit_attainment(z):
    n=z['n'];fs=z['rows'];assert fs==[[(q+1)%n for q in range(n)],[q if q<n-1 else 0 for q in range(n)]]
    words=z['support_words'];assert len(words)==n and z['weights_denominator']==n
    total=[[0]*n for _ in range(n)];paid=0
    for k,word in enumerate(words):
        assert word==[1]+[0]*k
        result=literal(fs,word);assert len(set(result))==n-1;paid+=n*len(word)
        for q,r in enumerate(result):total[q][r]+=1
    assert all(x==1 for row in total for x in row)
    assert z['maximum_support_length']==max(map(len,words))==n
    assert sha256(json.dumps(total,separators=(',',':')).encode()).hexdigest()==z['matrix_numerator_sha256']
    assert paid==z['literal_support_letter_controls']==n*n*(n+1)//2
    reset=z['reset_word'];assert reset==([1]+[0]*(n-1))*(n-2)+[1] and len(reset)==z['reset_length']==(n-1)**2
    image=list(range(n));ranks=[]
    for a in reset:image=[fs[a][p] for p in image];ranks.append(len(set(image)))
    assert image==[0]*n and z['reset_image']==[0] and z['reset_rank_history']==ranks
    # Actual b and ba edges alone are strongly connected.
    second=literal(fs,[1,0]);seen=set();p=0
    for _ in range(n):seen.add(p);p=second[p]
    assert seen==set(range(n)) and fs[1][n-1]==0
    # Every singleton occurs in the invariant-space orbit under original a preimages.
    singleton=1;orbit=[]
    for _ in range(n):
        orbit.append(singleton)
        singleton=sum(1<<q for q in range(n) if singleton>>fs[0][q]&1)
    assert set(orbit)=={1<<q for q in range(n)}
    # Weak stationarity has expected-cost infimum0, not the maximum-cost lower bound n.
    expected=[]
    for denominator in (2,3,7,31,1024):
        eps=Fraction(1,denominator)
        for r in range(n):assert (1-eps)+eps*sum(total[q][r] for q in range(n))/n==1
        value=eps*sum(map(len,words))/n;assert value==eps*Fraction(n+1,2)
        expected.append([value.numerator,value.denominator])
    return dict(n=n,paid_support_state_letters=paid,paid_reset_state_letters=n*len(reset),
                matrix_entries=n*n,singleton_orbit=n,expected_cost_controls=expected)


def audit_projected(z):
    n=5;fs=z['rows'];alpha=z['normal']
    assert z['n']==n and alpha==[1,1,-1,-1,0] and z['marked_state']==4 and z['dimension']==4
    assert fs==[[4,0,4,0,0],[1,2,2,1,4],[1,3,3,1,0]]
    assert z['weights_numerators']==[1,1,1] and z['weights_denominator']==3
    cols=[[sum(f[q]==r for q in range(n)) for r in range(n)] for f in fs]
    assert [sum(row[r] for row in cols)-3 for r in range(n)]==alpha
    for f in fs:assert [sum(alpha[q] for q in range(n) if f[q]==r) for r in range(n)]==[0]*n
    for start in range(n):
        seen={start};previous=set()
        while seen!=previous:previous=set(seen);seen.update(f[q] for q in previous for f in fs)
        assert seen==set(range(n))
    reset=z['reset_word'];assert reset==[0,1,0] and literal(fs,reset)==[0]*n and z['reset_threshold']==3
    short_ranks=[]
    for k in range(3):
        for word in product(range(3),repeat=k):
            rank=len(set(literal(fs,word)));assert rank>=2;short_ranks.append(rank)
    assert [row[2] for row in cols]==[0,2,0] and [row[3] for row in cols]==[0,0,2] and [row[4] for row in cols]==[2,1,0]
    forced=[Fraction(0),Fraction(1,2),Fraction(1,2)]
    assert sum(forced)==1 and sum(forced[a]*cols[a][4] for a in range(3))==Fraction(1,2)!=1
    assert z['full_original_stationarity_possible'] is False
    vertices=[];witnesses=[];stationary_controls=0
    for S in range(1<<n):
        if sum(alpha[q] for q in range(n) if S>>q&1):continue
        vertices.append(S)
        preimages=[sum(bool(S>>f[q]&1) for q in range(n)) for f in fs]
        assert sum(preimages)==3*S.bit_count();stationary_controls+=1
        if S in (0,(1<<n)-1):continue
        for k in range(1,4):
            found=False
            for word in product(range(3),repeat=k):
                mapping=literal(fs,word);T=sum(1<<q for q in range(n) if S>>mapping[q]&1)
                assert sum(alpha[q] for q in range(n) if T>>q&1)==0
                if T.bit_count()>S.bit_count():witnesses.append(dict(S=S,word=list(word),T=T));found=True;break
            if found:break
        else:raise AssertionError('no paid projected extension')
    assert len(vertices)==12 and len(witnesses)==10
    return dict(verified=True,dimension=4,boolean_vertices=len(vertices),stationarity_controls=stationary_controls,
                proper_nonempty_extension_witnesses=witnesses,maximum_extension_cost=max(len(z['word']) for z in witnesses),
                all_shorter_reset_words_checked=len(short_ranks),reset_threshold=3,full_original_stationarity_impossible=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,default=Path('direct_attack/data/singular_stationary_word_cost.json'));ap.add_argument('--out',type=Path,default=Path('direct_attack/data/singular_stationary_word_cost_checks.json'));args=ap.parse_args()
    data=json.loads(args.data.read_text(encoding='utf-8'));assert [z['n'] for z in data['short_words']]==list(range(2,17))
    short=[audit_words(z) for z in data['short_words']]
    assert [z['n'] for z in data['attainment']]==list(range(2,33))+[64,127,257]
    positive=[audit_attainment(z) for z in data['attainment']];projected=audit_projected(data['projected_stationary_example']);corruptions=[]
    for field,value in [('words',1),('potential',[0,0]),('maximum_word_length',2),('functional_histogram',{'0':3}),('semantic_sha256','0'*64)]:
        z=copy.deepcopy(data['short_words'][0]);z[field]=value
        try:audit_words(z)
        except AssertionError:corruptions.append(field)
        else:raise AssertionError('accepted '+field)
    for field,value in [('maximum_support_length',1),('matrix_numerator_sha256','0'*64),('reset_length',2),('reset_rank_history',[2]),('support_words',[[1],[1]])]:
        z=copy.deepcopy(data['attainment'][0]);z[field]=value
        try:audit_attainment(z)
        except AssertionError:corruptions.append(field)
        else:raise AssertionError('accepted '+field)
    for field,value in [('normal',[0]*5),('reset_word',[0])]:
        z=copy.deepcopy(data['projected_stationary_example']);z[field]=value
        try:audit_projected(z)
        except AssertionError:corruptions.append('projected '+field)
        else:raise AssertionError('accepted projected '+field)
    out=dict(verified=True,all_literal_words=sum(z[0] for z in short),all_suffix_pair_paths=sum(z[1] for z in short),strictly_separated_singular_words=sum(z[2] for z in short),
             attainment=positive,paid_support_state_letters=sum(z['paid_support_state_letters'] for z in positive),paid_reset_state_letters=sum(z['paid_reset_state_letters'] for z in positive),
             matrix_entries=sum(z['matrix_entries'] for z in positive),projected_stationary_example=projected,corruptions_rejected=corruptions,
             boundary='Independent exact finite original-word weak-stationarity separation, ALL word controls n2..16, support/reset/singleton-orbit certificates through n257. All-n maximum support optimum n is paper PROVED, not formal. No general reset theorem, no expected-cost lower bound or universality of this construction; general Cerny OPEN.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,all_literal_words=out['all_literal_words'],all_suffix_pair_paths=out['all_suffix_pair_paths'],strictly_separated_singular_words=out['strictly_separated_singular_words'],attainment_scopes=len(positive),paid_support_state_letters=out['paid_support_state_letters'],paid_reset_state_letters=out['paid_reset_state_letters'],corruptions=len(corruptions))),flush=True)


if __name__=='__main__':main()
