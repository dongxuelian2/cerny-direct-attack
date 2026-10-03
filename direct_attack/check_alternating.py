"""Independent ordinary-set image and inverse-distance audit of alternating layers."""
from collections import deque
import json
from pathlib import Path


def apply(rows,S,w):
    for a in w:S=frozenset(rows[a][q] for q in S)
    return S


def inverse_distance(rows,S):
    n=len(rows[0]);Q=frozenset(range(n));E=frozenset(range(0,n,2))
    templates=[frozenset((q+r)%n for q in E) for r in range(n)]
    queue=deque([S]);dist={S:0};counts=[];current_depth=-1
    while queue:
        X=queue.popleft();d=dist[X]
        if d!=current_depth:counts.append(0);current_depth=d
        counts[-1]+=1
        if any(T<=X for T in templates):return d,len(dist),counts
        for row in rows:
            Y=frozenset(q for q in Q if row[q] in X)
            if Y not in dist:dist[Y]=d+1;queue.append(Y)
    raise AssertionError('No reachable larger image')


def main():
    records=[];cross=[];structure=[];extension_constructions=[];capacity_cases=[]
    for path in sorted(Path('direct_attack/data/alternating_frame_layer').glob('n*.json')):
        c=json.loads(path.read_text());n=c['n'];m=(n-1)//2;rows=c['rows'];Q=frozenset(range(n))
        S=frozenset(q for q in Q if c['start']>>q&1);T=frozenset(q for q in Q if c['larger_image']>>q&1)
        assert len(S)==m and len(T)==m+1
        assert apply(rows,Q,c['reach_word'])==S
        assert apply(rows,T,c['word'])<=S and len(c['word'])==c['max_cost']
        d,vertices,levels=inverse_distance(rows,S);assert d==c['max_cost']
        records.append(dict(file=str(path),n=n,cost=d,vertices=vertices,levels=levels,verified=True))
        print(json.dumps({k:v for k,v in records[-1].items() if k!='levels'}),flush=True)
        other=Path('direct_attack/data/alternating_extension_layer',f'n{n}.json')
        if other.exists():
            a=json.loads(other.read_text());assert a['costs']==c['costs'] and a['max_cost']==d
            assert a['rows']==rows
            AS=frozenset(q for q in Q if a['start']>>q&1)
            goal=frozenset(q for q in Q if a['goal_preimage']>>q&1)
            assert apply(rows,Q,a['reach_word'])==AS
            assert apply(rows,goal,a['word'])<=AS and len(a['word'])==d
            assert any(frozenset((q+r)%n for q in range(0,n,2))<=goal for r in range(n))
            cross.append(dict(n=n,all_rank_entries=len(c['costs']),verified=True))
        if n>=11:
            E=sum(1<<q for q in range(0,n,2));base=E^(1<<(n-3));r=n-5
            target=((base<<r)| (base>>(n-r))) & ((1<<n)-1)
            assert dict(c['costs'])[target]==2*n-4
        if n<=15:
            queue=deque([Q]);R={Q}
            while queue:
                X=queue.popleft()
                for row in rows:
                    Y=frozenset(row[q] for q in X)
                    if Y not in R:R.add(Y);queue.append(Y)
            E=frozenset(range(0,n,2));expected={Q}
            for r in range(n):
                V=[(q+r)%n for q in E]
                for mask in range(1,1<<len(V)):expected.add(frozenset(V[i] for i in range(len(V)) if mask>>i&1))
            assert R==expected
            middle={sum(1<<q for q in X) for X in R if len(X)==m}
            assert middle==set(dict(c['costs'])) and len(middle)==m*n
            structure.append(dict(n=n,reachable_images=len(R),verified=True))
            templates=[frozenset((q+r)%n for q in E) for r in range(n)]
            if n<=11:
                for mask in range(1<<n):
                    X=frozenset(q for q in Q if mask>>q&1)
                    actual=max((len(T) for T in R if T<=X),default=0)
                    formula=n if X==Q else max(len(X&W) for W in templates)
                    assert actual==formula
                capacity_cases.append(dict(n=n,all_subsets=1<<n,verified=True))
            V=templates[1];constructed=0
            for X in R-{Q}:
                r=next(r for r,W in enumerate(templates) if X<=W)
                X0=frozenset((q-r)%n for q in X)
                if X0==E:T=Q;u=[0]
                else:
                    h=next(h for h in sorted(E) if h not in X0 and (h+2)%(n+1) in X0)
                    u=[0] if h==n-1 else [0]+[1]*(h+2)+[0]
                    T=frozenset(q for q in V if apply(rows,frozenset([q]),u)<=X0)
                    assert T in R and len(T)==len(X)+1
                word=u+[1]*r
                assert T in R and len(T)>len(X) and apply(rows,T,word)==X and len(word)<=2*n
                constructed+=1
            extension_constructions.append(dict(n=n,all_proper_images=constructed,verified=True))
    report=dict(peaks=records,complete_layer_cross_checks=cross,image_structure=structure,
                extension_constructions=extension_constructions,capacity_cases=capacity_cases)
    Path('direct_attack/data/alternating_independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(peaks=len(records),complete_layer_cross_checks=len(cross),structure_cases=len(structure),verified=True)))


if __name__=='__main__':main()
