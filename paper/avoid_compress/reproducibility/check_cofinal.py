"""Independent finite audit of the cofinal extension; standard library only.

Transitions are rebuilt from a core cycle and external paths, rather than
copying the generator's piecewise index formula. Exact ac uses set BFS.
"""
from collections import defaultdict, deque
import json
from pathlib import Path
from cofinal_family import construct, expand, reset_word
from subset_bfs import bfs, strong

ROOT=Path(__file__).resolve().parent

def image(states,row):return {row[q] for q in states}

def apply(states,word,rows):
    out=set(states)
    for letter in word:out=image(out,rows['ab'.index(letter)])
    return out

def rebuild(r,g,M):
    h=1+(M-1)%g;p=r+1;n=p+M
    P=list(range(p));U=list(range(p,n));a=list(range(n));b=[None]*n
    # One path through the transient points into a cyclic tail.
    for source,target in zip(U,U[1:]):a[source]=target
    a[U[-1]]=U[h]
    core=[0]+U[h-1:g]+U[:h-1]+list(range(r,0,-1))
    for source,target in zip(core,core[1:]+core[:1]):b[source]=target
    # Ordinary external chains run to the protected-state entrance.
    for q in U[g:-1]:
        offset=q-U[h-1]
        b[q]=r if offset%g==g-1 else q+1
    b[U[-1]]=U[h+g-1]
    assert None not in b
    return [a,b],core

def distances(graph,start):
    dist={q:0 for q in start};todo=deque(start)
    while todo:
        q=todo.popleft()
        for t in graph[q]:
            if t not in dist:dist[t]=dist[q]+1;todo.append(t)
    return dist

def audit(z):
    r,g,M,h,n,s=[z[k] for k in ('r','g','M','h','n','s')];rows=z['rows'];S=set(z['S']);A=set(z['A']);p=r+1
    rebuilt,core=rebuild(r,g,M);assert rows==rebuilt and set(core)==S
    assert strong(rows)
    assert apply(range(n),expand(z['reaching']),rows)==S
    cell=[q if q<p else p+((q-p+1-h-1)%g) for q in range(n)]
    # Colors 1..g use coordinates p..p+g-1.
    Ta=list(range(s));Tb=list(range(s))
    for j in range(g):Ta[p+j]=p+(j+1)%g
    cell_cycle=[0,p+g-1]+list(range(p,p+g-1))+list(range(r,0,-1))
    for source,target in zip(cell_cycle,cell_cycle[1:]+cell_cycle[:1]):Tb[source]=target
    errors=[]
    for letter,(row,T) in enumerate(zip(rows,[Ta,Tb])):
        for q in range(n):
            delta=[0]*s;delta[cell[row[q]]]+=1;delta[T[cell[q]]]-=1
            if any(delta):errors.append((letter,q,delta))
    correction=[0]*s;correction[p+g-1]=1;correction[p]=-1
    assert errors==[(1,n-1,correction)]
    fibres=[]
    for row in rows:
        fibre=defaultdict(list)
        for q,t in enumerate(row):fibre[t].append(q)
        fibres.append([v for v in fibre.values() if len(v)>1])
    assert fibres[0]==[[p+h-1,n-1]]
    assert len(fibres[1])==1 and all(cell[q]==p+g-2 for q in fibres[1][0])
    assert n-1 not in rows[1]
    a_to_h=[q for q,t in enumerate(rows[0]) if t==p+h-1]
    a_to_M=[q for q,t in enumerate(rows[0]) if t==n-1]
    assert a_to_M==[n-2]
    assert a_to_h==([] if h==1 else [p+h-2])
    assert all(cell[q]==p+g-2 for q in a_to_h+a_to_M)
    graph=[[row[q] for row in rows] for q in range(n)]
    assert distances(graph,S)[n-1]==M-g
    cell_graph=[[Ta[q],Tb[q]] for q in range(s)]
    assert distances(cell_graph,[p+g-1])[p+g-2]==g-1
    assert min(distances(cell_graph,[p])[q] for q in A)==g
    unit_word=expand(z['unit'])
    expected=list(range(n));expected[p+h-1]=0
    for q in S:assert apply([q],unit_word,rows)=={expected[q]}
    reset=reset_word(z);assert len(reset)==z['reset_length'] and len(apply(range(n),reset,rows))==1
    attaining=expand(z['attaining']);end=apply(S,attaining,rows)
    assert len(attaining)==M+1 and r-1 not in end
    exact,graph=bfs(rows,S,lambda T:len(T)<s or not A<=T)
    assert len(exact)==M+1
    return dict(r=r,g=g,M=M,h=h,n=n,s=s,ac=len(exact),rows=rows,S=sorted(S),A=sorted(A),
                reaching=expand(z['reaching']),attaining=attaining,reset=reset,
                safe_bfs_vertices=sum(len(w)<M+1 for w in graph.values()),
                sole_error={'letter':'b','source':n-1,'positive_color':g,'negative_color':1},
                unit_word=unit_word)

def main():
    scope={(r,g,M) for g in range(2,9) for M in range(2*g+1,4*g+2) for r in (1,2,5)}
    scope|={(r,2,M) for M in range(5,25) for r in range(1,6)}
    records=[]
    for params in sorted(scope,key=lambda t:(t[0]+t[2]+1,t)):
        records.append(audit(construct(*params)))
    report=dict(status='Finite checks passed. Uniform proof is a separate obligation.',records=records,
                count=len(records),maximum_n=max(z['n'] for z in records),
                bfs_vertices=sum(z['safe_bfs_vertices'] for z in records))
    (ROOT/'cofinal_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','count','maximum_n','bfs_vertices')}))
    print(json.dumps(next(z for z in records if (z['n'],z['s'],len(z['A']))==(10,4,1))))

if __name__=='__main__':main()
