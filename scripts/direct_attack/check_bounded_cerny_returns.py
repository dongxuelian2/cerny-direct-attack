"""Independent literal edges, lower potentials, and reset-witness controls."""
from copy import deepcopy
import json
from pathlib import Path

def img(S,f):
    T=0
    for q,p in enumerate(f):
        if S>>q&1:T|=1<<p
    return T

def bellman(rows,costs,d):
    assert len(d)==1<<len(rows[0]);edges=0
    for S,value in enumerate(d):
        assert value is None or type(value) is int and value>=0
        if S.bit_count()<=1:assert value==0;continue
        choices=[]
        for f,c in zip(rows,costs):
            T=img(S,f);edges+=1
            if d[T] is not None:choices.append(c+d[T])
        assert value==(min(choices) if choices else None)
    return edges

def lower_potential(rows,costs,d):
    # Zero-cost a edges prevent a uniqueness claim for Bellman equations.
    # Edge inequalities alone telescope to a certified lower bound; a
    # separate literal reset word attains the whole-set value.
    assert len(d)==1<<len(rows[0]);edges=0
    for S,value in enumerate(d):
        assert type(value) is int and value>=0
        if S.bit_count()<=1:assert value==0
        for f,c in zip(rows,costs):assert value<=c+d[img(S,f)];edges+=1
    return edges

def literal(rows,w):
    endpoints=[]
    for q in range(len(rows[0])):
        for i in w:assert 0<=i<len(rows);q=rows[i][q]
        endpoints.append(q)
    assert len(set(endpoints))==1
    return len(rows[0])*len(w)

def check(data):
    records=data['records'];assert [z['n'] for z in records]==list(range(4,15))
    edges=zero_edges=letters=capcases=finitefail=0
    for z in records:
        n=z['n'];M=n-1;rows=z['rows'];assert rows==[[1]+list(range(1,n)),list(range(1,n))+[0]]
        edges+=bellman(rows,[1,1],z['original_distances'])
        zero_edges+=lower_potential(rows,[0,1],z['b_distances'])
        known=z['known_word'];assert known==[0]+([1]*M+[0])*(M-1)
        assert len(known)==M*M and known.count(1)==M*(M-1)
        assert z['original_distances'][-1]==len(known) and z['b_distances'][-1]==known.count(1)
        letters+=literal(rows,known)
        assert [c['K'] for c in z['caps']]==list(range(1,M+1))
        for c in z['caps']:
            K=c['K'];costs=c['costs'];returned=c['rows'];assert costs==list(range(1,K+2))
            assert len(returned)==K+1
            for j,f in enumerate(returned):
                assert f==[(1 if (q+j)%n==0 else (q+j)%n)-1 for q in range(1,n)]
            edges+=bellman(returned,costs,c['distances']);w=c['word'];v=c['distances'][-1]
            assert c['lower']==M*(M-1)+(M*(M-1)+K-1)//K+1
            if v is None:assert w is None and K==1
            else:
                assert w is not None and sum(costs[i] for i in w)==v
                letters+=literal(returned,w);expanded=[0]
                for j in w:expanded.extend([1]*j+[0])
                assert len(expanded)==v+1 and expanded.count(1)>=M*(M-1)
                assert len(expanded)>=c['lower'];letters+=literal(rows,expanded)
                if K<M:assert v+1>M*M;finitefail+=1
                else:assert v+1==M*M
            capcases+=1
    assert records[0]['caps'][1]['distances'][-1]==10
    return dict(verified=True,parameters=len(records),caps=capcases,finite_entered_square_failures=finitefail,
                positive_cost_bellman_edges=edges,zero_cost_lower_potential_edges=zero_edges,
                literal_particle_letter_controls=letters,n4_entered_all_three=11,
                boundary='ALL finite subset Bellman costs n4..14/caps1..n-1, independent original-word expansion, and zero-cost telescoping b-count lower potentials. The all-n obstruction is PROVED paper separately, without novelty or formal claim. General Cerny OPEN.')

def main():
    data=json.loads(Path('scripts/direct_attack/data/bounded_cerny_returns.json').read_text());out=check(data);rejected=[]
    for mode in range(8):
        bad=deepcopy(data);z=bad['records'][0];c=z['caps'][1]
        if mode==0:z['rows'][0][0]=0
        if mode==1:z['b_distances'][-1]+=1
        if mode==2:c['distances'][-1]=8
        if mode==3:c['costs'][2]=2
        if mode==4:c['word'].pop()
        if mode==5:c['rows'][2][2]=1
        if mode==6:z['caps'].pop()
        if mode==7:c['lower']-=1
        try:check(bad)
        except (AssertionError,KeyError,ValueError):rejected.append(mode)
        else:raise AssertionError('accepted corruption')
    out['corruptions_rejected']=rejected
    Path('scripts/direct_attack/data/bounded_cerny_returns_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
