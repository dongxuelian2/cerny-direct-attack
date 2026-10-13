"""Independent permutation coverage, quotient, holes, rows, and avoidance Bellman audit."""
from copy import deepcopy
from math import factorial,gcd
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]

def literal(F,w):
    assert isinstance(w,list) and all(type(i) is int and i in (0,1) for i in w)
    state=list(range(len(F[0])));holes=[]
    for i in w:
        state=[F[i][p] for p in state]
        if i==0:holes.append(sorted(set(range(len(state)))-set(state)))
    return state,holes

def model(F,M,d):
    a,b=F;L=M-d;assert len(a)==len(b)==M+1 and a[M]==0 and a[0]==a[L]==M
    rest=[q for q in range(M) if q not in (0,L)];assert sorted(a[q] for q in rest)==rest
    assert b==list(range(1,M))+[0,M]
    return a,b,rest

def independently_four_pool(a):
    M=len(a)-1;L=M//2;domain=[q for q in range(M) if q not in (0,L)];options=[]
    for p in domain:
        x=a[p];q=next(q for q in domain if a[q]==(x+L)%M)
        difference=(q-p)%M
        if difference==L:continue
        z=next(z for z in domain if a[z]==(L+difference)%M)
        j=(z-L)%M;h=(p-L)%M;k=(-x)%M
        options.append([j+h+k+4,x,j,h,k])
    return sorted(options)

def verify_four(F,code):
    M=len(F[0])-1;L=M//2;cost,x,j,h,k=code
    assert 0<x<M and x!=L and all(0<=v<M for v in (j,h,k)) and cost==j+h+k+4
    w=[0]+[1]*j+[0]+[1]*h+[0]+[1]*k+[0];state,H=literal(F,w)
    assert len(w)==cost and w.count(0)==4 and cost<=3*M+1
    a=F[0];z=(L+j)%M;p=(L+h)%M;q=(a[z]+h)%M
    assert a[p]==x and a[q]==(x+L)%M
    assert H==[[L],sorted([L,a[z]]),sorted([L,x,(x+L)%M]),sorted([M,L,a[(L-x)%M]])]
    assert M not in state and len(set(state))==M-2
    return state,w

def stationary_rotations(F,v,letter_count):
    M=len(F[0])-1;av,_=literal(F,[0]);vv,_=literal(F,v)
    assert v.count(0)==letter_count and M not in vv
    row=[0]*(M+1)
    for j in range(M):
        for states in (av,vv):
            for q in states:row[(q+j)%M if q<M else M]+=1
    assert row==[2*M]*(M+1)
    return M*2

def forward(U,f):
    return sum(1<<p for p in {f[q] for q in range(len(f)) if U>>q&1})

def check_avoid(z,expected=None):
    F=z['rows'];n=len(F[0]);N=1<<n;D=z['distances'];assert len(D)==N;edges=0
    for U,d in enumerate(D):
        assert d is None or type(d) is int and d>=0
        if U<N//2:assert d==0
        else:
            values=[D[forward(U,f)] for f in F];finite=[x for x in values if x is not None]
            assert d==(1+min(finite) if finite else None);edges+=2
    state,_=literal(F,z['word']);image=sum(1<<p for p in set(state))
    assert image==z['image']<N//2 and len(z['word'])==D[N-1]
    if expected is not None:assert D[N-1]==expected
    return edges

def check(data):
    seen={M:set() for M in [2,4,6,8,10]};sync=quotients=particles=support_words=0;max_reset=0;max_four={M:0 for M in seen}
    for z in data['records']:
        M=z['M'];assert M in seen;L=M//2;rest=[q for q in range(M) if q not in (0,L)];A=z['permutation']
        assert sorted(A)==rest and tuple(A) not in seen[M];seen[M].add(tuple(A))
        a=list(range(M+1));a[M]=0;a[0]=a[L]=M
        for q,p in zip(rest,A):a[q]=p
        F=[a,list(range(1,M))+[0,M]];pool=independently_four_pool(a)
        if not pool:
            assert z['four_a_preparation'] is None and z['reset_word'] is None
            phi=[None]*L;phi[0]=0
            for q in rest:
                h=q%L;k=a[q]%L
                if phi[h] is None:phi[h]=k
                else:assert phi[h]==k
            assert sorted(phi)==list(range(L))
            quotient_a=[L]+phi[1:]+[0];quotient_b=[(h+1)%L for h in range(L)]+[L]
            assert sorted(quotient_a)==sorted(quotient_b)==list(range(L+1));quotients+=1
        else:
            assert z['four_a_preparation']==pool[0];states,v=verify_four(F,pool[0]);max_four[M]=max(max_four[M],len(v))
            w=z['reset_word'];states,_=literal(F,w);assert len(set(states))==1 and len(w)<=M*M
            max_reset=max(max_reset,len(w));sync+=1;particles+=(M+1)*(len(v)+len(w))
            support_words+=stationary_rotations(F,v,4)
    assert all(len(seen[M])==factorial(M-2) for M in seen)
    assert len(data['records'])==41067 and sync==40624 and quotients==443
    controls=data['three_a_controls'];expected={(M,d) for M in range(3,16) for d in range(1,M) if M//gcd(M,d)>=3}
    assert len(controls)==len(expected) and {(z['M'],z['d']) for z in controls}==expected
    for z in controls:
        M=z['M'];d=z['d'];a,b,rest=model(z['rows'],M,d);L=M-d;p=next(p for p in rest if a[p]==2*L%M);j=(p-L)%M
        v=z['preparation'];assert v==[0]+[1]*j+[0]+[1]*d+[0] and len(v)<=2*M
        states,H=literal([a,b],v);assert set(states)==set(range(M))-{L} and H==[[L],sorted([L,2*L%M]),sorted([M,L])]
        support_words+=stationary_rotations([a,b],v,3);particles+=(M+1)*len(v)
    family=data['family_controls'];assert [z['L'] for z in family]==list(range(7,31))+[63,127,256]
    for z in family:
        L=z['L'];M=2*L;a,b,rest=model(z['rows'],M,L)
        required={1:L+2,L+1:1,L-2:L+1,M-2:2,2:L+3,L+2:3,L-1:L-3,M-1:M-3}
        assert all(a[q]==p for q,p in required.items())
        assert all((a[h+L]-a[h])%M==L for h in range(1,L) if h not in (1,L-2))
        pool=independently_four_pool(a);assert z['four_a_pool']==pool and len(pool)==4
        assert [p[0] for p in pool]==[2*M+2,2*M+2,2*M+3,2*M+3]
        for code in pool:verify_four([a,b],code)
        support_words+=stationary_rotations([a,b],[0]+[1]*pool[0][2]+[0]+[1]*pool[0][3]+[0]+[1]*pool[0][4]+[0],4)
    z=data['n_plus_two_boundary'];assert z['rows']==[[4,4,3,2,0],[1,2,3,0,4]];edges=check_avoid(z,8)
    total=[0]*5
    for word,weight in z['stationary_support']:
        assert type(weight) is int and weight>0 and len(word)<=8;states,_=literal(z['rows'],word)
        for q in range(5):total[q]+=weight*(states.count(q)-1)
    assert total==[0]*5 and z['stationary_support'][0]==[[0],1] and max(len(w) for w,c in z['stationary_support'])==8
    z=data['four_a_tradeoff'];assert z['rows']==[[6,1,5,6,2,4,0],[1,2,3,4,5,0,6]];edges+=check_avoid(z,9)
    assert z['word'].count(0)==5 and independently_four_pool(z['rows'][0])[0][0]==13
    z=data['family_boundary'];assert z['rows']==family[0]['rows'];edges+=check_avoid(z)
    return dict(verified=True,complete_order_two_inputs=41067,synchronizing=sync,permutation_quotients=quotients,
                literal_particle_controls=particles,stationary_rotated_word_controls=support_words,
                three_a_controls=len(controls),infinite_family_controls=len(family),max_literal_reset=max_reset,max_minimum_four_a_cost=max_four,
                avoidance_bellman_edges=edges,family_base_minimum_avoid=z['distances'][-1],
                status='PROVED paper all-n model synchronization classification and min avoiding/support singular count3/4, explicit paid bounds, infinite minimum FOUR-a avoid cost2n; not general minimum original cost. Complete finite permutation scope COMPUTATIONALLY VERIFIED. Exact n5 avoid/positive-original stationary cost8 refutes broader n+2 metric; coprime support cost<=max(avoid_cost,n) PROVED paper. General mixed-core square/Cerny OPEN, no formal/priority claim.')

def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/moving_root_order_two.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    z=data['n_plus_two_boundary']
    for mode in range(6):
        bad=deepcopy(z)
        if mode==0:bad['distances'][-1]=7
        if mode==1:bad['word'].pop()
        if mode==2:bad['image']=31
        if mode==3:bad['rows'][0][2]=2
        if mode==4:bad['distances'][0]=1
        if mode==5:bad['distances'].pop()
        try:check_avoid(bad,8)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError(('accepted boundary corruption',mode))
    # Local hole/endpoint corruptions; completeness was checked separately above.
    record=next(z for z in data['records'] if z['four_a_preparation'] is not None);M=record['M'];L=M//2;rest=[q for q in range(M) if q not in (0,L)];a=list(range(M+1));a[M]=0;a[0]=a[L]=M
    for q,p in zip(rest,record['permutation']):a[q]=p
    for mode in range(6,10):
        code=list(record['four_a_preparation']);code[mode-6]=(code[mode-6]+1)%M
        try:verify_four([a,list(range(1,M))+[0,M]],code)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError(('accepted hole corruption',mode))
    out['corruptions_rejected']=rejected
    (ROOT/'scripts/direct_attack/data/moving_root_order_two_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
