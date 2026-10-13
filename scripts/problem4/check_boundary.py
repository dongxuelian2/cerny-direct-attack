"""Ordinary-set audit of the M=2g boundary extension, including reset macros."""
from pathlib import Path
import json
from cofinal_family import boundary
from check_cofinal import apply, distances
from subset_bfs import bfs,strong

ROOT=Path(__file__).resolve().parent

def audit(z):
    r,g,M,n,s=[z[k] for k in ('r','g','M','n','s')];p=r+1;rows=z['rows'];S=set(z['S']);A=set(z['A'])
    B=set(range(p))|set(range(p+g-1,p+2*g-1));root=n-1;E=B|{root}
    # Independent cycle/path reconstruction, including the transient block.
    U=list(range(p,n));rebuilt=[list(range(n)),[None]*n]
    for source,target in zip(U,U[1:]+U[:1]):rebuilt[0][source]=target
    core=[0]+U[g-1:2*g-1]+list(range(r,0,-1))
    for source,target in zip(core,core[1:]+core[:1]):rebuilt[1][source]=target
    for source in U[:g-1]:rebuilt[1][source]=r if source==U[g-2] else source+1
    rebuilt[1][root]=root
    assert rebuilt==rows
    assert strong(rows)
    assert apply(range(n),'b'*(g+1),rows)==E
    assert apply(range(n),z['reaching_word'],rows)==S
    cell=list(range(p))+[p+(j%g) for j in range(2*g)]
    Ta=list(range(s));Tb=list(range(s))
    for j in range(g):Ta[p+j]=p+(j+1)%g
    cycle=[0,p+g-1]+list(range(p,p+g-1))+list(range(r,0,-1))
    for source,target in zip(cycle,cycle[1:]+cycle[:1]):Tb[source]=target
    errors=[]
    for letter,(row,T) in enumerate(zip(rows,[Ta,Tb])):
        for q in range(n):
            delta=[0]*s;delta[cell[row[q]]]+=1;delta[T[cell[q]]]-=1
            if any(delta):errors.append((letter,q,delta))
    correction=[0]*s;correction[p+g-1]=1;correction[p]=-1
    assert errors==[(1,root,correction)]
    assert distances([[row[q] for row in rows] for q in range(n)],S)[root]==g
    cell_graph=[[Ta[q],Tb[q]] for q in range(s)]
    assert distances(cell_graph,[p+g-1])[p+g-2]==g-1
    assert min(distances(cell_graph,[p])[q] for q in A)==g
    expected_d={q:q for q in E}
    expected_d[p+g-1]=p+2*g-2;expected_d[p+g]=root;expected_d[root]=p+2*g-2
    for j in range(2,g):expected_d[p+g+j-1]=p+g+j-2
    d='a'*(g-1)+'b'*s
    for q,t in expected_d.items():assert apply([q],d,rows)=={t}
    for q in E:assert apply([q],z['root_unit'],rows)==({root} if q==p+g-1 else {q})
    assert len(apply(range(n),z['reset_word'],rows))==1
    assert r-1 not in apply(S,z['attaining_word'],rows)
    attaining,graph=bfs(rows,S,lambda T:len(T)<s or not A<=T)
    assert len(attaining)==M+1
    return dict(z,value=M+1,safe_bfs_vertices=sum(len(w)<M+1 for w in graph.values()))

def main():
    records=[audit(boundary(r,g)) for g in range(2,13) for r in (1,2,5)]
    out=dict(status='Finite boundary checks passed; uniform proof separate.',records=records,
             count=len(records),maximum_n=max(z['n'] for z in records),
             bfs_vertices=sum(z['safe_bfs_vertices'] for z in records))
    (ROOT/'boundary_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:out[k] for k in ('status','count','maximum_n','bfs_vertices')}))

if __name__=='__main__':main()
