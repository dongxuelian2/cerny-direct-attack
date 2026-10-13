"""Independent coprime hypotheses, paid witnesses, and exact seed obstruction."""
from copy import deepcopy
from itertools import permutations
from math import gcd
import json
from pathlib import Path
# These are independent checker routines, not generators/search solvers.
from direct_attack.check_fixed_root_cycle_extension import geometry,strongly_connected,extension,pre,act

def orbit(b):
    C=[];q=0
    while q not in C:C.append(q);q=b[q]
    assert q==0
    return C

def original_bellman(rows,d):
    assert len(d)==1<<len(rows[0]);edges=0
    for S,value in enumerate(d):
        assert type(value) is int and value>=0
        if S.bit_count()<=1:assert value==0;continue
        values=[]
        for f in rows:
            T=0
            for q in range(len(f)):
                if S>>q&1:T|=1<<f[q]
            values.append(1+d[T]);edges+=1
        assert value==min(values)
    S=len(d)-1;w=[]
    while S.bit_count()>1:
        for i,f in enumerate(rows):
            T=0
            for q in range(len(f)):
                if S>>q&1:T|=1<<f[q]
            if d[S]==d[T]+1:S=T;w.append(i);break
    assert len(w)==d[-1] and len({act(rows,w,q) for q in range(len(rows[0]))})==1
    return edges,w

def check(data):
    records=data['records'];assert len(records)==398
    complete={n:set() for n in range(2,6)};sampled={n:0 for n in range(6,11)};sync=controls=letters=nonadjacent=multicycle=depth=0
    for z in records:
        rows=z['rows'];assert len(rows)==2;n=len(rows[0]);a,b=rows
        assert a[:2]==[1,1] and sorted(a[1:])==list(range(1,n)) and sorted(b)==list(range(n))
        R=orbit(b);assert 1 in R;delta=R.index(1);assert z['delta']==delta and gcd(len(R),delta)==1
        if z['mode'].startswith('complete'):
            assert n in complete;key=tuple(tuple(f) for f in rows);assert key not in complete[n];complete[n].add(key)
        else:
            assert z['mode']=='sampled nonadjacent coprime binary' and n in sampled and delta>1
            sampled[n]+=1
        good=strongly_connected(rows);assert good==z['SC']
        if not good:assert 'extensions' not in z;continue
        sync+=1;nonadjacent+=delta>1;C,index,root,d=geometry(rows);multicycle+=len(C)>1
        assert [e['U'] for e in z['extensions']]==list(range(1,(1<<n)-1))
        for e in z['extensions']:
            work,h,paid,cost=extension(rows,e,C,index,root,d);letters+=work;depth=max(depth,h);controls+=1
        factors=z['reset_factors'];assert len(factors)==n-1 and factors[0]==[0];U={1};w=[]
        for j,v in enumerate(factors):
            assert 0<len(v)<=n;U=pre(rows,v,U);w=v+w;assert len(U)==j+2;letters+=n*len(v)
        assert U==set(range(n)) and z['reset_word']==w and len(w)<=(n-1)**2
        assert len({act(rows,w,q) for q in range(n)})==1;letters+=n*len(w)
    for n,seen in complete.items():
        expected=set()
        for tail in permutations(range(2,n)):
            for b in permutations(range(n)):
                R=orbit(b)
                if 1 in R and gcd(len(R),R.index(1))==1:expected.add((tuple([1,1]+list(tail)),tuple(b)))
        assert seen==expected
    assert all(count==10 for count in sampled.values())
    z=data['counter'];rows=z['rows'];assert rows==[[1,1,3,2,4],[4,2,0,3,1]] and z['U']==3
    assert strongly_connected(rows);R=orbit(rows[1]);assert len(R)==4 and R.index(1)==2 and gcd(4,2)==2
    d=z['extension_distances'];assert len(d)==32;edges=0
    for S,value in enumerate(d):
        assert value is None or type(value) is int and value>=0
        if S.bit_count()>2:assert value==0;continue
        U={q for q in range(5) if S>>q&1};values=[]
        for i in range(2):
            T=sum(1<<q for q in pre(rows,[i],U));edges+=1
            if d[T] is not None:values.append(1+d[T])
        assert value==(min(values) if values else None)
    assert d[3]==6 and len(z['extension_word'])==6 and len(pre(rows,z['extension_word'],{0,1}))==3
    ordinary,w=original_bellman(rows,z['original_distances']);assert len(w)==13
    factors=[[0],[0,1,1,1,0,1],[0,1],[0,1,1,1]];U={1};paid=[];assembled=[]
    for factor,expected in zip(factors,({0,1},{0,1,2},{0,1,3,4},set(range(5)))):
        U=pre(rows,factor,U);assert U==expected;paid.append(len(factor));assembled=factor+assembled
    assert paid==[1,6,2,4] and assembled==w
    return dict(verified=True,inputs=len(records),complete_binary_inputs=sum(len(z) for z in complete.values()),SC_inputs=sync,
                nonadjacent_coprime_SC_inputs=nonadjacent,multicycle_b_SC_inputs=multicycle,subset_controls=controls,
                max_preparation_depth=depth,literal_particle_letter_controls=letters,counter_extension_edges=edges,
                counter_original_edges=ordinary,counter_min_seed_extension=6,counter_rt=13,counter_reset_word=w,counter_growth_costs=paid,
                boundary='Independent complete coprime binary n2..5 cover and original literal ALL-subset witnesses on retained inputs through n10, reusing only previously independent checker primitives. Finite exact n5 noncoprime seed extension6>5 and ordinary rt13<16. All-n coprime subclass theorem PROVED paper, not formal or novelty. General Cerny OPEN.')

def main():
    data=json.loads(Path('scripts/direct_attack/data/coprime_root_cycle_extension.json').read_text());out=check(data);rejected=[]
    for mode in range(8):
        bad=deepcopy(data);z=bad['records'][0]
        if mode==0:z['delta']=0
        if mode==1:z['rows'][0][1]=0
        if mode==2:z['extensions'][0]['word'].pop()
        if mode==3:z['reset_word'].pop()
        if mode==4:bad['counter']['extension_distances'][3]=5
        if mode==5:bad['counter']['original_distances'][-1]=16
        if mode==6:bad['records'].pop()
        if mode==7:bad['counter']['extension_word'].pop()
        try:check(bad)
        except (AssertionError,KeyError,ValueError,TypeError):rejected.append(mode)
        else:raise AssertionError('accepted corruption')
    out['corruptions_rejected']=rejected
    Path('scripts/direct_attack/data/coprime_root_cycle_extension_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
