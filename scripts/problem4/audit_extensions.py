"""Adversarial checks of attempted extensions and finite structured witnesses.

Failures here refute proof attempts, not the conjectural extremal formula.
"""
import json
from pathlib import Path
from audit_small import bfs, strong

ROOT=Path(__file__).resolve().parent

def naive(r,g,M):
    p=r+1;n=p+M;a=list(range(n));b=list(range(n));b[0]=p
    for q in range(1,p):b[q]=q-1
    for j in range(1,M+1):
        q=p+j-1;a[q]=p+j%M
        b[q]=r if j%g==0 else (p+j if j<M else p+g)
    return [a,b],frozenset(range(p+g)),frozenset(range(r))

def check(rows,S,A):
    n=len(rows[0]);S=frozenset(S);A=frozenset(A)
    reaching,_=bfs(rows,range(n),lambda T:T==S)
    reset,_=bfs(rows,range(n),lambda T:len(T)==1)
    attaining,_=bfs(rows,S,lambda T:len(T)<len(S) or not A<=T)
    return dict(strongly_connected=strong(rows),reachable_image=reaching is not None,
                synchronizing=reset is not None,ac=None if attaining is None else len(attaining),
                reaching=reaching,reset=reset,attaining=attaining)

def main():
    failures=[]
    for r,g,M in [(1,3,6),(1,3,8),(1,2,6),(1,4,10)]:
        rows,S,A=naive(r,g,M);result=check(rows,S,A)
        failures.append(dict(r=r,g=g,M=M,n=len(rows[0]),S=sorted(S),A=sorted(A),rows=rows,
                             proposed_ac=M+1,verification=result))
    assert not failures[0]['verification']['synchronizing']
    assert failures[1]['verification']['ac']==8<9
    structured=[]
    for file in sorted(ROOT.glob('structured_n*.json')):
        data=json.loads(file.read_text());n=data['n']
        for z in data['results']:
            S=[q for q in range(n) if z['S_mask']>>q&1]
            A=[q for q in range(n) if z['A_mask']>>q&1]
            result=check(z['rows'],S,A)
            assert result['strongly_connected'] and result['synchronizing'] and result['reachable_image']
            assert result['ac']==z['value']<=z['candidate_bound']
            structured.append(dict(n=n,s=z['s'],r=z['r'],value=z['value'],candidate_bound=z['candidate_bound'],
                                   rows=z['rows'],S=S,A=A,source=file.name,verification=result))
    active=[]
    for file in sorted(ROOT.glob('active_n*.json')):
        z=json.loads(file.read_text());n=z['n']
        S=[q for q in range(n) if z['S_mask']>>q&1];A=[q for q in range(n) if z['A_mask']>>q&1]
        result=check(z['rows'],S,A)
        assert result['strongly_connected'] and result['synchronizing'] and result['reachable_image']
        assert result['ac']==z['value']<=z['candidate_bound']
        active.append(dict(n=n,s=z['s'],r=z['r'],value=z['value'],candidate_bound=z['candidate_bound'],
                          rows=z['rows'],S=S,A=A,source=file.name,verification=result))
    report=dict(status='Conjecture unproved and unrefuted; restricted-search failures are not counterexamples.',
                naive_extensions=failures,structured_certificates=structured,active_certificates=active)
    (ROOT/'extension_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(naive_failures=failures,structured_checked=len(structured),active_checked=len(active))))

if __name__=='__main__':main()
