"""Finite reuse of manuscript automata on ALL their reachable images (n<=12).

This enumerates the image semigroups of the supplied families, not all automata.
"""
from collections import deque
import importlib.util
import json
from pathlib import Path
from audit_small import bfs

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('paper_generator',ROOT.parent/'reproducibility'/'generator.py')
gen=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

def move(S,row):return sum(1<<q for q in {row[p] for p in range(len(row)) if S>>p&1})

def run(n):
    upper=lambda s,r:min(n-r,(n-s+2)*(n-s+1)//2)
    best={}
    families=[]
    for r in range(1,n):families.append(('face1',r,gen.face(n,r,1)[0]))
    for r in range(1,n-2):families.append(('face2',r,gen.face(n,r,2)[0]))
    for g in range(2,n):
        for k in range(2,n):
            r=n-k*g-2
            if r>=1:families.append((f'larger_g{g}_k{k}',r,gen.larger(r,g,k)[0]))
    for family,parameter,rows in families:
        full=(1<<n)-1; todo=deque([full]); reach={full:''}; table={}
        while todo:
            S=todo.popleft(); table[S]=[move(S,row) for row in rows]
            for letter,T in zip('ab',table[S]):
                if T not in reach:reach[T]=reach[S]+letter;todo.append(T)
        assert any(S.bit_count()==1 for S in reach)
        for S in reach:
            s=S.bit_count()
            if s<2 or all(best.get((s,r),{}).get('value',0)==upper(s,r) for r in range(1,s)):continue
            comp=n+1; avoid={p:n+1 for p in range(n) if S>>p&1}; queue=deque([S]); dist={S:0}
            while queue:
                T=queue.popleft(); d=dist[T]
                if d>=comp:break
                for U in table[T]:
                    nd=d+1
                    if U.bit_count()<s:comp=min(comp,nd);continue
                    for p in avoid:
                        if not U>>p&1:avoid[p]=min(avoid[p],nd)
                    if U not in dist:dist[U]=nd;queue.append(U)
            scores=sorted(((min(comp,d),p) for p,d in avoid.items()),reverse=True)
            A=[]
            for r in range(1,s):
                value,p=scores[r-1];A.append(p)
                if value>best.get((s,r),{}).get('value',0):
                    best[s,r]=dict(n=n,s=s,r=r,value=value,candidate_bound=upper(s,r),
                                   family=family,parameter=parameter,rows=rows,
                                   S=sorted(p for p in range(n) if S>>p&1),A=sorted(A),reaching=reach[S])
    results=[best[key] for key in sorted(best)]
    for z in results:
        w,_=bfs(z['rows'],z['S'],lambda T:len(T)<z['s'] or not set(z['A'])<=T)
        assert len(w)==z['value'];z['attaining']=w
        reset,_=bfs(z['rows'],range(n),lambda T:len(T)==1);assert reset is not None;z['reset']=reset
    report=dict(n=n,manuscript_family_automata=len(families),exhaustive_all_automata=False,results=results)
    (ROOT/f'reuse_n{n}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(n=n,sharp=sum(z['value']==z['candidate_bound'] for z in results),
                         missing=[(z['s'],z['r'],z['value'],z['candidate_bound']) for z in results if z['value']!=z['candidate_bound']])),flush=True)

if __name__=='__main__':
    for n in range(8,13):run(n)
