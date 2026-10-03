"""Independent integer row-orbit and exact rational-mixture checker."""
from collections import deque
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path

def word_images(rows,w):
    images=[]
    for start in range(len(rows[0])):
        q=start
        for letter in w:assert letter in (0,1);q=rows[letter][q]
        images.append(q)
    return images

def move(v,f):
    out=[0]*len(v)
    for q,x in enumerate(v):out[f[q]]+=x
    return tuple(out)

def orbit(fs):
    n=len(fs[0]);initial=(1,)*n;dist={initial:0};todo=deque([initial]);edges=0
    while todo:
        v=todo.popleft()
        for f in fs:
            u=move(v,f);edges+=1
            if u not in dist:dist[u]=dist[v]+1;todo.append(u)
    return dist,edges

def check(data):
    assert [z['n'] for z in data['records']]==list(range(4,65))+[127,257]
    states=edges=short_rows=supported_words=particle_letters=permutation_rows=0;checks=[]
    for z in data['records']:
        n=z['n'];fs=z['rows'];assert len(fs)==2 and all(len(f)==n for f in fs)
        # Verify transitions by local graph roles, independently of the
        # generator's concatenated array construction.
        for q in range(n):
            assert fs[0][q]==(0 if q==0 else (q+1 if q<n-1 else 1))
            assert fs[1][q]==(1 if q in (0,n-1) else 0)
        N=n-2;K=n+(n+1)//2-1;L=K-1
        assert (z['N'],z['K'],z['lower_cap'])==(N,K,L)
        phi=z['separator_phi'];assert len(phi)==n
        for q in range(n):assert phi[q]==(N if q==0 else (-2 if q>=(n+1)//2 else 0))
        margin=-sum(phi);assert margin==z['strict_margin']==(1 if n%2 else 2)
        dist,ec=orbit(fs);states+=len(dist);edges+=ec
        assert len(dist)==(2*n if n==4 else 3*n-1)
        wanted={(1,)*n:0}
        for j in range(1,n):
            for mass,expected in ((2,j),(N,j+1)):
                row=[0]*n;row[0]=n-mass;row[j]=mass;row=tuple(row)
                wanted[row]=min(wanted.get(row,expected),expected)
            row=tuple(n if q==j else 0 for q in range(n));wanted[row]=n+j-1
        wanted[tuple(n if q==0 else 0 for q in range(n))]=n+1
        assert dist==wanted
        for row,cost in dist.items():
            if cost>L:continue
            if row==(1,)*n:permutation_rows+=1;continue
            assert sum((row[q]-1)*phi[q] for q in range(n))>=margin;short_rows+=1
        rt=min(cost for row,cost in dist.items() if sum(x>0 for x in row)==1)
        assert rt==z['exact_reset_threshold']==n and len(z['reset'])==n
        assert len(set(word_images(fs,z['reset'])))==1;particle_letters+=n*len(z['reset'])
        summass=Fraction(0);average=[Fraction(0)]*n;maps=[]
        for e in z['support']:
            weight=Fraction(*e['weight']);assert weight>0 and len(e['word'])<=K
            f=word_images(fs,e['word']);counts=[0]*n
            for p in f:counts[p]+=1
            assert counts==e['row_counts'] and len(set(f))<n
            if e['kind']=='B':
                assert e['word']==[1,1]+[0]*(e['j']-1)
            else:
                assert e['kind']=='R' and e['word']==[1]+[0]*(n-2)+[1]+[0]*(e['j']-1)
            summass+=weight;average=[x+weight*y for x,y in zip(average,counts)];maps.append(f)
            particle_letters+=n*len(e['word']);supported_words+=1
        assert summass==1 and average==[1]*n and max(len(e['word']) for e in z['support'])==K
        assert any(len(set(f))==1 for f in maps)
        for start in range(n):
            reached={start};todo=[start]
            for q in todo:
                for f in maps:
                    if f[q] not in reached:reached.add(f[q]);todo.append(f[q])
            assert len(reached)==n
        checks.append(dict(n=n,closed_row_orbit=len(dist),all_parameter_scope='finite original-row closure only',exact_rt=rt,exact_stationary_maximum_cost=K))
    return dict(verified=True,parameters=len(checks),maximum_n=257,closed_row_vertices=states,closure_edges=edges,
                all_short_singular_row_classes=short_rows,permutation_row_classes=permutation_rows,supported_words=supported_words,
                literal_particle_letter_controls=particle_letters,checks=checks,
                boundary='Independent exact complete full-Q ROW orbit closure and Bellman shortest costs in63 retained parameters, covering ALL words in each fixed family input. Exact separator and rational stationary mixture, literal reset and support SC/sync. All-n theorem separately PROVED paper, not formal or all-parameter computational proof. General Cerny OPEN; only universal maximum support n bridge refuted.')

def main():
    data=json.loads(Path('direct_attack/data/weak_stationary_linear_cost.json').read_text());out=check(data);rejected=[]
    for mode in range(8):
        bad=deepcopy(data);z=bad['records'][0]
        if mode==0:z['rows'][1][0]=0
        if mode==1:z['K']-=1
        if mode==2:z['separator_phi'][0]+=1
        if mode==3:z['support'][0]['weight'][0]+=1
        if mode==4:z['support'][0]['row_counts'][0]+=1
        if mode==5:z['reset'].pop()
        if mode==6:z['exact_reset_threshold']+=1
        if mode==7:z['support'].pop()
        try:check(bad)
        except (AssertionError,KeyError,ValueError):rejected.append(mode)
        else:raise AssertionError('corruption accepted')
    out['corruptions_rejected']=rejected
    Path('direct_attack/data/weak_stationary_linear_cost_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='checks'}),flush=True)

if __name__=='__main__':main()
