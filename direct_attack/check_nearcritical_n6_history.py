"""Independent retained-case ALL shortest-history audit by forward images/minors.

The complete native covering prefilter is deliberately NOT certified here.
"""
import argparse,copy,json
from collections import deque
from fractions import Fraction
from itertools import permutations
from pathlib import Path

def minor(masks):
    # Select six independent Boolean rows by exact elimination; check their determinant separately.
    basis={};indices=[]
    for i,S in enumerate(masks):
        rr=[Fraction(S>>q&1) for q in range(6)]
        for p,row in sorted(basis.items()):
            a=rr[p]
            if a:rr=[x-a*y for x,y in zip(rr,row)]
        p=next((q for q,x in enumerate(rr) if x),None)
        if p is not None:
            z=rr[p];basis[p]=[x/z for x in rr];indices.append(i)
    if len(indices)<6:return None
    chosen=[masks[i] for i in indices[:6]];det=0
    for pp in permutations(range(6)):
        if not all(chosen[i]>>pp[i]&1 for i in range(6)):continue
        inversions=sum(pp[i]>pp[j] for i in range(6) for j in range(i+1,6))
        det+=(-1)**inversions
    assert det
    return dict(independent_history_indices=indices[:6],determinant=det)

def canonical_key(rows):
    keys=[]
    for pp in permutations(range(6)):
        renamed=[]
        for f in rows:
            g=[0]*6
            for q in range(6):g[pp[q]]=pp[f[q]]
            renamed.append(tuple(g))
        keys.append(tuple(sorted(renamed)))
    return min(keys)

def audit_case(z):
    rows=z['rows'];assert len(rows)==2 and all(len(f)==6 and all(0<=t<6 for t in f) for f in rows)
    graph=[]
    for S in range(64):
        targets=[]
        for f in rows:
            image={f[q] for q in range(6) if S>>q&1};targets.append(sum(1<<q for q in image))
        graph.append(targets)
    forward={63:0};queue=deque([63])
    while queue:
        S=queue.popleft()
        for T in graph[S]:
            if T not in forward:forward[T]=forward[S]+1;queue.append(T)
    # A word expands S to Q by inverse images iff its forward Q-image is contained in S.
    distance=[min((v for T,v in forward.items() if T&~S==0),default=10**6) for S in range(64)]
    L=min(distance[1<<q] for q in range(6));assert L==z['analysis']['rt'] and 21<=L<=25
    inv=[[sum(1<<q for q in range(6) if S>>f[q]&1) for S in range(64)] for f in rows]
    cuts=[];nodes=0;edges=0
    def recurse(S,history,path):
        nonlocal nodes,edges
        nodes+=1;certificate=minor([63]+history)
        if certificate is not None:
            cuts.append(dict(inverse_letter_prefix=path,inverse_history=history,**certificate));return
        assert S!=63,'retained case has a proper-rank shortest full history'
        choices=[(a,inv[a][S]) for a in range(2) if distance[inv[a][S]]==distance[S]-1]
        assert choices
        for a,T in choices:
            assert T and T.bit_count()>1 and T not in history;edges+=1
            recurse(T,history+[T],path+[a])
    starts=[1<<q for q in range(6) if distance[1<<q]==L]
    for S in starts:recurse(S,[S],[])
    assert cuts
    return dict(rows=rows,rt=L,optimal_reset_targets=len(starts),full_forward_subset_vertices=len(forward),
                all_subset_letter_controls=128,proper_rank_prefix_nodes=nodes,proper_rank_prefix_edges=edges,full_rank_branch_certificates=cuts,
                maximum_cut_depth=max(len(c['inverse_letter_prefix']) for c in cuts),minimum_minor_absolute_value=min(abs(c['determinant']) for c in cuts),
                all_globally_shortest_full_histories_have_raw_rank6=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,default=Path('direct_attack/data/research_pressure_121/nearcritical_n6_history.analysis.json'));ap.add_argument('--out',type=Path,default=Path('direct_attack/data/nearcritical_n6_history_checks.json'));args=ap.parse_args()
    data=json.loads(args.data.read_text(encoding='utf-8'));cases=data['records'];assert len(cases)==37
    keys=[canonical_key(z['rows']) for z in cases];assert len(set(keys))==37
    records=[audit_case(z) for z in cases]
    corruption=[]
    for name in ('wrong_rt','constant_letter','out_of_range'):
        z=copy.deepcopy(cases[0])
        if name=='wrong_rt':z['analysis']['rt']+=1
        elif name=='constant_letter':z['rows'][0]=[0]*6
        else:z['rows'][0][0]=6
        try:audit_case(z)
        except AssertionError:corruption.append(name)
        else:raise AssertionError('accepted '+name)
    out=dict(verified=True,retained_isomorphism_classes=len(records),all_subset_letter_controls=sum(z['all_subset_letter_controls'] for z in records),
             retained_forward_subset_vertices=sum(z['full_forward_subset_vertices'] for z in records),prefix_nodes=sum(z['proper_rank_prefix_nodes'] for z in records),
             prefix_edges=sum(z['proper_rank_prefix_edges'] for z in records),nonzero_integer_minor_certificates=sum(len(z['full_rank_branch_certificates']) for z in records),
             maximum_cut_depth=max(z['maximum_cut_depth'] for z in records),records=records,corruptions_rejected=corruption,
             boundary='COMPUTATIONALLY VERIFIED: ANY globally shortest full inverse history in EACH of these37 retained binary SC cases has real rank6, by complete forward image distances and ALL optimal prefix branches terminated at a nonzero integer6-minor. The native complete covering prefilter and its class completeness are NOT audited here; their negative coverage remains EXPLORATORY. No arbitrary-alphabet, all-n, formal, or general Cerny proof.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)

if __name__=='__main__':main()
