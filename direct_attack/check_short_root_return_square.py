"""Independent forward particles, exact budgets, complete coverage and Bellman cut."""
from collections import defaultdict,Counter
from copy import deepcopy
from math import gcd,factorial
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def check(data):
    signatures=defaultdict(set)
    for z in data['records']:
        if z['mode']=='complete_new_c_positive_M5..7':
            key=(z['M'],z['L'],z['c']);row=tuple(z['rows'][0]);assert row not in signatures[key];signatures[key].add(row)
    expected={(M,L,c):factorial(M-2) for M in range(5,8) for L in range(1,M) for c in range(1,M) if c!=L and any(0<2*J<M and (L+J)%M not in (c,L) for J in {L,c})}
    assert set(signatures)==set(expected) and all(len(signatures[key])==value for key,value in expected.items())
    stats=Counter();seeds=Counter();cycles=Counter();compensations=Counter()
    def action(F,w):
        assert isinstance(w,list) and all(type(i) is int and i in (0,1) for i in w)
        S=list(range(len(F[0])))
        for i in w:S=[F[i][q] for q in S]
        stats['literal_particle_controls']+=len(F[0])*len(w);return S
    for z in data['records']:
        M=z['M'];n=M+1;L=z['L'];c=z['c'];J=z['J'];a,b=z['rows'];g=gcd(M,L);t=M//g;Q=(1<<n)-1;C=(1<<M)-1
        assert M>=5 and 0<L<M and 0<=c<M and c!=L and a[M]==0 and a[c]==a[L]==M
        assert len(a)==n and {a[q] for q in range(M) if q not in (c,L)}==set(range(M))-{0,L}
        assert b==list(range(1,M))+[0,M] and J in (c,L) and 0<2*J<M and a[(L+J)%M]!=M
        def pre(U,w):return sum(1<<q for q,x in enumerate(action([a,b],w)) if U>>x&1)
        f=[0]+[1]*J+[0];z0=a[(L+J)%M];assert z0==z['z'] and z0 not in (0,L,M)
        image=action([a,b],f);assert image[M]==M
        assert [image.count(q)-1 for q in range(n)]==[int(q==M)+int(q==0)-int(q==L)-int(q==z0) for q in range(n)]
        H=c if J==L else L;p=a.index((H-J)%M);assert p==z['p'] and p not in (c,L) and pre(1<<M,f)==(1<<M)|(1<<p)
        seed=z['seed'];rule=z['seed_rule'];q=z['q'];seeds[rule]+=1
        if p<=M-J-1:assert rule=='three_a' and q is None and seed==[0]+[1]*p+f and len(seed)<=n+1
        elif p!=z0:assert rule=='f_squared' and q is None and seed==f+f
        else:assert rule=='f_shift_f' and q==(2 if p==L+1 else 1) and seed==f+[1]*q+f
        U=pre(1<<M,seed);assert U>>M&1 and U.bit_count()==3;word=seed[:];saved=0;core_sizes=[]
        for e in z['factors']:
            assert e['U']==U and U>>M&1 and U<Q
            core=U&C;core_sizes.append(core.bit_count());whole=all((core>>x&1)==(core>>((x+L)%M)&1) for x in range(M))
            if whole:
                assert e['rule']=='coset';s=e['s'];assert 0<=s<g and not core>>((z0+s)%M)&1
                w=f+[1]*s;assert len(w)<=J+g+1<=M
            else:
                assert e['rule']=='noncoset';j=e['j'];assert 0<=j<M and core>>j&1 and not core>>((j+L)%M)&1
                w=[0]+[1]*j;assert len(w)<=n-1;saved+=1
            V=pre(U,w);assert V>>M&1 and V.bit_count()==U.bit_count()+1
            U=V;word=w+word;stats['literal_root_preserving_extensions']+=1
        N=M-g-1;assert core_sizes==list(range(2,M)) and N==(M-2)-(M-1)//t and saved>=N
        if M%2:assert t>=3 and N>=3 and len(seed)<=n+4
        else:assert N>=2 and len(seed)<=n+3
        assert len(seed)<=n+1+N and U==Q and word==z['reset_word'] and len(word)<=M*M-M+(5 if M%2 else 4)
        assert action([a,b],word)==[M]*n
        if len(seed)>n+1:compensations[len(seed)-(n+1)]+=1
        cyc=z['root_cycle'];assert cyc[0]==M and len(set(cyc))==len(cyc) and all(a[cyc[i]]==cyc[(i+1)%len(cyc)] for i in range(len(cyc)))
        cycles[len(cyc)]+=1;stats['literal_reset_words']+=1
    boundaries=data['order_two_seed_boundaries'];assert len(boundaries)==2
    minima=[]
    for boundary in boundaries:
        F=boundary['rows'];M=len(F[0])-1;n=M+1;N=1<<n;Q=N-1;start=1<<M
        assert F[1]==list(range(1,M))+[0,M] and M in (6,8) and F[0][M]==0 and F[0][0]==F[0][M//2]==M
        edges=[[sum(1<<q for q,x in enumerate(row) if U>>x&1) for row in F] for U in range(N)]
        assert [cert['k'] for cert in boundary['goals']]==[3,4,n]
        for cert in boundary['goals']:
            k=cert['k'];D=cert['distances'];assert len(D)==N
            for U in range(N):
                goal=bool(U>>M&1 and U.bit_count()>=k)
                if goal:assert D[U]==0
                else:
                    ds=[D[V] for V in edges[U] if D[V] is not None];want=1+min(ds) if ds else None
                    assert D[U]==want
                stats['boundary_bellman_edges']+=2
            assert cert['minimum']==D[start]==len(cert['word'])
            V=sum(1<<q for q,x in enumerate(action(F,cert['word'])) if x==M)
            assert V==cert['target'] and V>>M&1 and V.bit_count()>=k
            if k==3:assert cert['minimum']>n+1;minima.append(dict(n=n,minimum_root_seed3=cert['minimum']))
            if k==n:assert V==Q and len(cert['word'])<=M*M
    assert minima==[dict(n=7,minimum_root_seed3=9),dict(n=9,minimum_root_seed3=12)]
    return dict(verified=True,inputs=len(data['records']),complete_new_inputs=sum(expected.values()),maximum_n=max(z['M']+1 for z in data['records']),
                root_cycle_lengths=dict(cycles),seed_rules=dict(seeds),global_seed_compensations=dict(compensations),seed3_refutations=minima,**dict(stats),
                status='PROVED paper ALL M>=5 original rank-one/tail-root/core-cycle model with admissible kernel-return exponent J<M/2; arbitrary root-cycle length and remaining bijection. Every root-preserving extension costs M, giving strict quadratic reset M^2-M+4(even M) / M^2-M+5(odd M). Finite independent words/rows/coverage/Bellman COMPUTATIONALLY VERIFIED; not FORMALLY VERIFIED. General Cerny and c0 opposite-pair order-two all-n square OPEN.')

def main():
    data=json.loads((ROOT/'direct_attack/data/short_root_return_square.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    for mode in range(10):
        bad=deepcopy(data);z=bad['records'][0]
        if mode==0:bad['records'].pop(0)
        if mode==1:bad['records'][1]=deepcopy(z)
        if mode==2:z['rows'][0][z['c']]=0
        if mode==3:z['J']=z['M']
        if mode==4:z['p']=z['L']
        if mode==5:z['seed'].pop()
        if mode==6:z['factors'][0]['U']^=1
        if mode==7:z['reset_word'].pop()
        if mode==8:bad['order_two_seed_boundaries'][0]['goals'][0]['distances'][1<<6]=8
        if mode==9:bad['order_two_seed_boundaries'][1]['goals'][0]['word'].pop()
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError,StopIteration):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected
    (ROOT/'direct_attack/data/short_root_return_square_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
