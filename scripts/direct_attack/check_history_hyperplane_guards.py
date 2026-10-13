"""Independent positive-weight vertex reconstruction and graph component audit."""
import argparse,copy,json,math
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations,combinations_with_replacement,product
from pathlib import Path

def digest(z):return sha256(json.dumps(z,separators=(',',':')).encode()).hexdigest()

def exact_rank(vertices,n):
    # Column elimination on an n-by-|V| rational matrix, rather than the generator's row update.
    matrix=[[Fraction(v>>q&1) for v in vertices] for q in range(n)];r=0
    for j in range(len(vertices)):
        i=next((i for i in range(r,n) if matrix[i][j]),None)
        if i is None:continue
        matrix[r],matrix[i]=matrix[i],matrix[r];pivot=matrix[r][j]
        matrix[r]=[x/pivot for x in matrix[r]]
        for i in range(r+1,n):
            a=matrix[i][j]
            if a:matrix[i]=[x-a*y for x,y in zip(matrix[i],matrix[r])]
        r+=1
        if r==n:break
    return r

def check_plane(z):
    aa=z['normal'];n=len(aa);assert n==z['n'] and sum(aa)==0 and math.gcd(*aa)==1
    support=[q for q,a in enumerate(aa) if a];free=[q for q,a in enumerate(aa) if not a]
    assert len(support)==z['support'] and len(free)==z['singletons']>=1
    target=-sum(a for a in aa if a<0);weights=[abs(aa[q]) for q in support]
    patterns=[]
    for bits in product((0,1),repeat=len(support)):
        if sum(a*b for a,b in zip(weights,bits))!=target:continue
        mask=sum((b if aa[q]>0 else 1-b)<<q for q,b in zip(support,bits));patterns.append(mask)
    vertices=sorted(mask+sum(b<<q for q,b in zip(free,bits)) for mask in patterns for bits in product((0,1),repeat=len(free)))
    assert len(set(vertices))==len(vertices)==z['vertices'] and digest(vertices)==z['vertices_sha256']
    r=exact_rank(vertices,n);assert r==z['boolean_span_rank'] and ((1<<n)-1) in vertices
    # Every weight level is an antichain. Independently check every comparable pair on the support.
    subsets=[sum(b<<i for i,b in enumerate(bits)) for bits in product((0,1),repeat=len(support)) if sum(a*b for a,b in zip(weights,bits))==target]
    assert all(x&y!=x for x in subsets for y in subsets if x!=y)
    if r==n-1:
        bound=len(vertices)-len(free)-1;assert z['history_count_bound']==bound
        s=len(support)
        if s==2:assert sorted(aa[q] for q in support)==[-1,1]
        elif s==4:
            assert sorted(aa[q] for q in support)==[-1,-1,1,1]
            assert len(vertices)==6*2**len(free) and bound==6*2**len(free)-len(free)-1
        else:
            assert s>=5 and len(patterns)<=math.comb(s,s//2)
            assert bound<=5*2**(n-4)-2<=3*2**(n-3)-n+3
            if n==6:assert len(vertices)<=16 and bound<=14
    else:assert 'history_count_bound' not in z
    return len(vertices)

def components(d,edges):
    adjacency=[[] for _ in range(d)]
    for p,q in edges:adjacency[p].append(q);adjacency[q].append(p)
    colors={};blocks=[]
    for root in range(d):
        if root in colors:continue
        colors[root]=0;todo=[root];part=[]
        while todo:
            p=todo.pop();part.append(p)
            for q in adjacency[p]:
                if q in colors:
                    if colors[p]==colors[q]:return None
                else:colors[q]=1-colors[p];todo.append(q)
        blocks.append(part)
    return colors,blocks

def check_graphs(z):
    d=z['d'];ee=list(combinations(range(d),2));stream=sha256();profiles=0;hist=Counter();bip=0;binary=0
    for code in range(1,2**len(ee)):
        edges=[e for i,e in enumerate(ee) if code>>i&1];answer=components(d,edges);forbidden=[]
        if answer is not None:
            colors,blocks=answer;bip+=1
            for flips in product((0,1),repeat=len(blocks)):
                forbidden.append(sum((colors[q]^bit)<<q for bit,block in zip(flips,blocks) for q in block))
            assert len(set(forbidden))==len(forbidden)==2**len(blocks)
        tmask=sum(1<<q for q in range(d) if (1<<q) in forbidden)
        F=len(forbidden);stream.update(json.dumps([code,F,tmask],separators=(',',':')).encode()+b'\n')
        binary+=len(edges)<=2
        for C in range(1,2**d):
            unused=(C&tmask).bit_count();allowed=C.bit_count()-unused
            if not allowed:continue
            B=2**d-F-allowed-1;hist[B]+=1;profiles+=1
            assert B<=2**d-C.bit_count()-1
            if len(edges)<=2:
                assert answer is not None
                if len(edges)==1:assert B<=2**(d-1)-C.bit_count()+1
                else:assert B<=3*2**(d-2)-C.bit_count()
    assert z['nonempty_graphs']==2**len(ee)-1 and z['bipartite_graphs']==bip and z['binary_graphs']==binary
    assert z['admissible_singleton_profiles']==profiles and z['length_bound_histogram']=={str(k):hist[k] for k in sorted(hist)}
    assert z['semantic_sha256']==stream.hexdigest()
    return profiles

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,default=Path('scripts/direct_attack/data/history_hyperplane_guards.json'));ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/history_hyperplane_guards_checks.json'));args=ap.parse_args()
    data=json.loads(args.data.read_text(encoding='utf-8'))
    expected=[]
    for s in range(2,9):
        expected.extend(list(aa)+[0] for aa in combinations_with_replacement((-3,-2,-1,1,2,3),s) if sum(aa)==0 and math.gcd(*aa)==1)
    assert [z['normal'] for z in data['normal_models']]==expected
    assert [z['n'] for z in data['balanced_models']]==list(range(5,16)) and [z['d'] for z in data['guard_graphs']]==list(range(2,7))
    normal_vertices=sum(check_plane(z) for z in data['normal_models']);balanced_vertices=sum(check_plane(z) for z in data['balanced_models'])
    profiles=sum(check_graphs(z) for z in data['guard_graphs'])
    assert [a[0] for a in data['arithmetic']]==list(range(4,65));density=0
    for d,a,b in data['arithmetic']:
        assert a==6*2**(d-3)-(d-3)-1 and b==5*2**(d-3)-2 and a-b==2**(d-3)-d+4>0
        for s in range(5,d+1):assert Fraction(math.comb(s,s//2),2**s)<=Fraction(5,16);density+=1
    corruptions=[]
    for section,field,value,checker in [('normal_models','vertices',0,check_plane),('normal_models','boolean_span_rank',0,check_plane),('normal_models','singletons',0,check_plane),
                                      ('balanced_models','normal',[1,-1,1,-1,1],check_plane),('balanced_models','history_count_bound',0,check_plane),
                                      ('guard_graphs','bipartite_graphs',0,check_graphs),('guard_graphs','admissible_singleton_profiles',1,check_graphs),('guard_graphs','semantic_sha256','0'*64,check_graphs)]:
        z=copy.deepcopy(data[section][0]);z[field]=value
        try:checker(z)
        except AssertionError:corruptions.append(section+'_'+field)
        else:raise AssertionError('accepted corruption '+field)
    out=dict(verified=True,integer_normal_models=len(expected),boolean_spanning_normal_models=sum(z['boolean_span_rank']==z['n']-1 for z in data['normal_models']),
             normal_boolean_vertices=normal_vertices,balanced_models=len(data['balanced_models']),balanced_boolean_vertices=balanced_vertices,
             nonempty_guard_graphs=sum(z['nonempty_graphs'] for z in data['guard_graphs']),admissible_singleton_profiles=profiles,
             middle_layer_density_controls=density,length_comparisons=len(data['arithmetic']),corruptions_rejected=corruptions,
             boundary='independent exact finite real-space and graph controls only; not all real normals, all automata, or formal verification. General Cerny and unrestricted ALL/SOME full-history cost/rank remain OPEN. Separate near-critical prefilter/search is outside this checker and remains EXPLORATORY.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
