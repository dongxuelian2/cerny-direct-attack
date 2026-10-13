"""Independent literal row balance, complete scope and compatible-word audit."""
from copy import deepcopy
from math import factorial
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]

def col(f):
    out=[0]*len(f)
    for q in f:out[q]+=1
    return out

def preimage(S,f):
    out=0
    for q in range(len(f)):
        if (S//(2**f[q]))%2:out+=2**q
    return out

def trace(rows,S,word):
    out=[S]
    for i in reversed(word):
        assert type(i) is int and 0<=i<len(rows);S=preimage(S,rows[i]);out.append(S)
    return out

def cycles(f):
    visited=set();count=0
    for q in range(len(f)):
        if q in visited:continue
        path=set();p=q
        while p not in path and p not in visited:path.add(p);p=f[p]
        count+=p in path;visited|=path
    return count

def strong(rows):
    n=len(rows[0])
    for q in range(n):
        visited={q};todo=[q]
        for p in todo:
            for f in rows:
                if f[p] not in visited:visited.add(f[p]);todo.append(f[p])
        if len(visited)!=n:return False
    return True

def extension(rows,e,corr,cap,balancing=None):
    n=len(rows[0]);U=e['U'];assert type(U) is int and 0<U<2**n-1
    w=e['change_word'];assert 1<=len(w)<=n-1
    t=trace(rows,U,w);k=U.bit_count();assert all(S.bit_count()==k for S in t[:-1]) and t[-1].bit_count()!=k
    delta=t[-1].bit_count()-k;assert e['negative']==(delta<0)
    f=w[0]
    if balancing is None:
        assert f in corr;expected=w if delta>0 else [f]+corr[f]+w[1:];assert e['word']==expected
    else:
        assert f in balancing;expected=e['word']
        if delta>0:assert expected==w
        else:assert len(expected)==len(w)+1 and expected[0]==f and expected[2:]==w[1:] and balancing[f]['beta'].get(str(expected[1]),0)>0
    assert len(expected)<=cap
    out=trace(rows,U,expected);assert out[-1].bit_count()>k
    if balancing is None:assert out[-1].bit_count()==k+abs(delta)
    return out[-1],n*(len(w)+len(expected)),int(delta<0),all(y.bit_count()>=x.bit_count() for x,y in zip(out,out[1:]))

def check(data):
    records=data['records'];assert len(records)==430
    complete={n:set() for n in range(2,6)};samples={n:0 for n in range(6,13)};special=set()
    rich=set();pair_edges=particles=subsets=negative=mono=sync=multidefect=multicluster=singcorr=high_indegree=0
    max_change=max_extension=0
    for z in records:
        rows=z['rows'];n=len(rows[0]);assert n>=2 and rows and all(len(f)==n and all(type(q) is int and 0<=q<n for q in f) for f in rows)
        c=[col(f) for f in rows];sing={i for i,x in enumerate(c) if x!=[1]*n}
        cor={int(i):j for i,j in z['correctors'].items()};assert set(cor)<=sing and sing
        bal={int(i):v for i,v in z['balancing'].items()};assert set(bal)==sing
        for i,v in bal.items():
            alpha=v['alpha'];beta={int(j):t for j,t in v['beta'].items()}
            assert type(alpha) is int and alpha>0 and beta and all(type(t) is int and t>=0 and 0<=j<len(rows) for j,t in beta.items())
            total=[alpha*(x-1) for x in c[i]]
            for j,t in beta.items():
                comp=col([rows[j][rows[i][q]] for q in range(n)])
                total=[x+t*(y-1) for x,y in zip(total,comp)]
            assert total==[0]*n
        for i,j in cor.items():
            assert type(j) is int and 0<=j<len(rows)
            counts=col([rows[j][rows[i][q]] for q in range(n)])
            assert all(c[i][q]+counts[q]==2 for q in range(n));assert max(c[i])==2
            singcorr+=j in sing
        d=z['pair_distances'];assert len(d)==n*n
        for x in range(n):
            for y in range(n):
                value=d[n*x+y];assert value is None or type(value) is int and value>=0
                if x==y:assert value==0;continue
                candidates=[]
                for f in rows:
                    pair_edges+=1;v=d[n*f[x]+f[y]]
                    if v is not None:candidates.append(v+1)
                assert value==(min(candidates) if candidates else None)
        good=all(v is not None for v in d);assert type(z['SYNC']) is bool and z['SYNC']==good
        if z['mode']=='complete binary n2..5':
            assert 2<=n<=5 and len(rows)==2 and c[0]==[0,2]+[1]*(n-2)
            assert rows[1][:2]==[1,0] and sorted(rows[1][2:])==list(range(2,n))
            sig=tuple(tuple(f) for f in rows);assert sig not in complete[n];complete[n].add(sig)
        elif z['mode']=='sampled two-singular/four-letter':
            assert 6<=n<=12 and len(rows)==4 and good;samples[n]+=1
        elif z['mode']=='retained high-indegree convex balancing':
            assert n in (4,8,16,32,64) and n not in rich;rich.add(n)
            assert len(rows)==n and not cor and max(c[0])>=3 and good
            power=n.bit_length()-1;f=list(range(n))
            for q in [2**k for k in range(power)]:f[q]=0
            assert rows==[f]+[[q^v for q in range(n)] for v in range(1,n)]
        else:
            assert z['mode'] in {'retained all-original-multicluster','retained all-singular correctors'} and z['mode'] not in special
            special.add(z['mode']);assert good
            if z['mode']=='retained all-original-multicluster':assert rows==[[0,0,2,2,4,4],[1,0,3,2,5,4],[2,1,3,4,0,5]]
            else:assert rows==[[1,1,2],[0,0,2],[0,2,2],[0,1,1]] and sing==set(range(4))
        if not good:
            assert 'extensions' not in z and 'reset_word' not in z;continue
        sync+=1;assert strong(rows);high_indegree+=any(max(x)>=3 for x in c)
        multidefect+=any(len(set(f))<=n-2 for f in rows);multicluster+=all(cycles(f)>=2 for f in rows)
        corr={i:[j] for i,j in cor.items()};seen=set()
        for e in z['extensions']:
            assert e['U'] not in seen;seen.add(e['U']);S,p,neg,mon=extension(rows,e,corr,n,bal)
            subsets+=1;particles+=p;negative+=neg;mono+=mon
            max_change=max(max_change,len(e['change_word']));max_extension=max(max_extension,len(e['word']))
        if n<=10:
            assert z['subset_scope']=='ALL proper nonempty subsets' and seen==set(range(1,2**n-1))
        else:assert z['subset_scope']=='64 retained deterministic sampled subsets' and len(seen)==64
        factors=z['reset_factors'];assert factors and len(factors[0])==1
        i=factors[0][0];target=z['target'];assert 0<=target<n and c[i][target]>=2
        S=trace(rows,2**target,factors[0])[-1];assert S.bit_count()>=2;word=factors[0]
        M=max(max(x) for x in c);assert S.bit_count()==M
        for w in factors[1:]:
            assert 1<=len(w)<=n;T=trace(rows,S,w)[-1];assert T.bit_count()>S.bit_count();S=T;word=w+word
        assert S==2**n-1 and word==z['reset_word'] and len(word)<=1+n*(n-2)
        assert len(word)<=1+n*(n-M)
        particles+=n*len(word)
        for q in range(n):
            for i in word:q=rows[i][q]
            assert q==target
        particles+=n*len(word)
    assert all(len(complete[n])==factorial(n)*factorial(n-2)//2 for n in complete)
    assert sum(map(len,complete.values()))==388 and all(v==5 for v in samples.values()) and len(special)==2
    assert rich=={4,8,16,32,64}
    z=data['counter'];rows=z['rows'];assert rows==[[1,1,3,2,4],[4,2,0,3,1]] and z['U']==3 and z['corrector_word']==[1,1]
    first=col(rows[0]);f=rows[0]
    for i in z['corrector_word']:f=[rows[i][p] for p in f]
    assert all(x+y==2 for x,y in zip(first,col(f)))
    assert all(any(x+y!=2 for x,y in zip(first,col([g[p] for p in rows[0]]))) for g in rows)
    counter_edges=0;d=z['extension_distances'];assert len(d)==32
    for S,value in enumerate(d):
        if S.bit_count()>2:assert value==0;continue
        candidates=[]
        for f in rows:
            counter_edges+=1;T=preimage(S,f)
            if d[T] is not None:candidates.append(1+d[T])
        assert value==(min(candidates) if candidates else None)
    assert d[3]==6 and len(z['extension_word'])==6 and trace(rows,3,z['extension_word'])[-1].bit_count()>2
    out,p,neg,mon=extension(rows,z['flipped_change'],{0:[1,1]},6);assert neg and len(z['flipped_change']['change_word'])==4 and len(z['flipped_change']['word'])==6
    row_edges=row_controls=0
    family=data['cerny_reversal'];assert [z['n'] for z in family]==list(range(2,17))+[31,63,127,257]
    for z in family:
        n=z['n'];f=[1,1]+list(range(2,n));b=list(range(1,n))+[0];d=z['distances'];assert len(d)==n*n and d[n]==0
        for P in range(n):
            for Q in range(n):
                value=d[n*P+Q]
                if P==Q:assert value is None;continue
                assert type(value) is int and value>=0
                if P==1 and Q==0:continue
                weights=[1]*n;weights[P]=0;weights[Q]=2;candidates=[]
                for g in (f,b):
                    counts=[0]*n
                    for q,c in enumerate(weights):counts[g[q]]+=c;row_controls+=1
                    if counts.count(0)!=1 or counts.count(2)!=1 or max(counts)>2:continue
                    T=n*counts.index(0)+counts.index(2);row_edges+=1
                    assert d[T] is not None;candidates.append(1+d[T])
                assert value==min(candidates)
        u=z['corrector_word'];assert u==[1,0]*(n-2)+[1] and len(u)==d[1]==2*n-3
        actual=f[:]
        for i in u:actual=[(f,b)[i][q] for q in actual];row_controls+=n
        assert all(x+y==2 for x,y in zip(col(f),col(actual)))
    return dict(verified=True,inputs=430,complete_binary=388,SYNC=sync,multidefect_SYNC=multidefect,all_original_multicluster_SYNC=multicluster,
                nonpermutation_correctors=singcorr,subset_witnesses=subsets,negative_changes_flipped=negative,monotone_literal_witnesses=mono,
                high_indegree_balanced_SYNC=high_indegree,
                max_short_change=max_change,max_extension=max_extension,pair_bellman_edges=pair_edges,literal_particle_letters=particles,
                counter_bellman_edges=counter_edges,paid_counter_extension=6,
                cerny_reversal_parameters=len(family),cerny_reversal_bellman_edges=row_edges,cerny_reversal_literal_weighted_controls=row_controls,
                boundary='Independent positive integer defect balance, complete388 binary n2..5,35 multi-defect samples plus2 explicit controls and5 high-indegree balanced translation controls; proper-subset witnesses and ONE paid max-indegree-seeded square checked. Existing n5 cost2 corrector stage6 reused;19 complete retained Cerny row graphs certify suffix2n-3 through n257. Arbitrary-n positive class/reversal-cost results PROVED paper, no novelty/formal/general Cerny proof.')

def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/original_defect_reversal.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    for mode in range(10):
        bad=deepcopy(data)
        if mode==0:bad['records'].pop()
        if mode==1:bad['records'][-1]['balancing']['0']['alpha']=2
        if mode==2:bad['records'][0]['pair_distances'][1]=0
        if mode==3:bad['records'][0]['extensions'].pop()
        if mode==4:bad['records'][0]['extensions'][0]['negative']=not bad['records'][0]['extensions'][0]['negative']
        if mode==5:bad['records'][0]['extensions'][0]['word'].pop()
        if mode==6:bad['records'][0]['reset_word'].pop()
        if mode==7:bad['counter']['corrector_word']=[1]
        if mode==8:bad['counter']['extension_distances'][3]=5
        if mode==9:bad['cerny_reversal'][0]['distances'][1]=0
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError('accepted corruption')
    out['corruptions_rejected']=rejected
    (ROOT/'scripts/direct_attack/data/original_defect_reversal_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
