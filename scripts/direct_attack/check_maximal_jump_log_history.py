"""Independent PU rows, charged group words, all shortest jumps and policy audit."""
import argparse
from collections import deque
import copy
from fractions import Fraction
import json
from pathlib import Path


def rank(rows):
    pivots={}
    for values in rows:
        row=list(map(Fraction,values))
        for j,base in sorted(pivots.items()):
            if row[j]:
                c=row[j]
                row=[a-c*b for a,b in zip(row,base)]
        j=next((j for j,a in enumerate(row) if a),None)
        if j is not None:
            c=row[j]
            pivots[j]=[a/c for a in row]
    return len(pivots)


def swaps_for(q,r):
    steps=[]
    def move(value):
        for x,y in steps:
            if value==x: value=y
            elif value==y: value=x
        return value
    if move(q)!=1: steps.append((move(q),1))
    if move(r)!=2: steps.append((move(r),2))
    assert move(q)==1 and move(r)==2
    return steps


def expand_swaps(steps):
    word=[]
    for x,y in steps:
        x,y=sorted((x,y))
        assert x<y
        word += [['t',j] for j in range(x,y)]
        word += [['t',j] for j in range(y-2,x-1,-1)]
    return word


def check(z,full=False,all_words=False):
    d=z['d']; n=2**d-1
    assert d>=3 and z['n']==n
    blocks=[]; cursor=0
    for i in range(d):
        blocks.append(list(range(cursor,cursor+2**i)))
        cursor+=2**i
    assert cursor==n and z['blocks']==[[B[0],B[-1]] for B in blocks]
    index=[None]*n
    for i,B in enumerate(blocks):
        for q in B: index[q]=i
    def inside(k,q): return bool((k>>index[q])&1)
    edge={i:(blocks[i][0],blocks[i][1]) for i in range(1,d)}
    permutations={}
    def permutation(k):
        if k in permutations: return permutations[k]
        i=next(i for i in range(1,d) if (k+1)>>i&1)
        s,t=edge[i]
        domain=[q for q in range(n) if inside(k+1,q) and q!=s]
        target=[q for q in range(n) if inside(k,q)]
        remaining_domain=[q for q in range(n) if not (inside(k+1,q) and q!=s)]
        remaining_target=[q for q in range(n) if not inside(k,q)]
        row=[None]*n
        assert len(domain)==len(target)==k and t in domain
        for x,y in zip(domain,target): row[x]=y
        for x,y in zip(remaining_domain,remaining_target): row[x]=y
        assert set(row)==set(range(n))
        if full: permutations[k]=row
        return row
    def action(label,q):
        if label[0]=='t':
            j=label[1]
            assert 0<=j<n-1
            return j+1 if q==j else j if q==j+1 else q
        if label[0]=='u':
            _,i,orientation=label
            assert 1<=i<d and orientation in (-1,1)
            s,t=edge[i]
            if orientation==-1: s,t=t,s
            return t if q==s else q
        assert label[0]=='p' and 2<=label[1]<n
        return permutation(label[1])[q]
    def apply_word_to_set(image,word):
        for label in word:
            image={action(label,q) for q in image}
        return image
    h=2*n+2*d-5
    assert z['alphabet_symbols']==h and z['all_original_ranks']==[n-1,n]
    assert z['rt_lower']==n-1 and z['rt_upper']==z['policy_upper']==2*n-3
    assert z['endpoint']==2 and z['proper_stages']==n-2
    assert len(z['stages'])==n-1
    assert z['stages'][0]==dict(child='singleton2',parent=2,word=[['u',1,1]],cost=1)
    assert {q for q in range(n) if action(['u',1,1],q)==2}==set(blocks[1])
    phase_controls=0
    for k,stage in enumerate(z['stages'][1:],2):
        assert stage['child']==k and stage['parent']==k+1
        i=next(i for i in range(1,d) if (k+1)>>i&1)
        assert stage['unit_block']==i and stage['word']==[['u',i,1],['p',k]]
        assert stage['cost']==2 and stage['all_shortest_parent_size']==k+1
        row=permutation(k)
        pre={q for q in range(n) if inside(k,row[action(['u',i,1],q)])}
        parent={q for q in range(n) if inside(k+1,q)}
        assert pre==parent and len(pre)==k+1
        for j,(s,t) in edge.items():
            assert inside(k,s)==inside(k,t)
        phase_controls+=n
    # Compose the common full-Q trajectory with the actual pi row at each step.
    assert z['long_reset']==[x for stage in reversed(z['stages']) for x in stage['word']]
    assert z['long_reset_cost']==len(z['long_reset'])==2*n-3
    image=set(range(n))
    for k in range(n-1,1,-1):
        stage=z['stages'][k-1]
        image=apply_word_to_set(image,[stage['word'][0]])
        row=permutation(k)
        image={row[q] for q in image}
        assert image=={q for q in range(n) if inside(k,q)}
    image=apply_word_to_set(image,z['stages'][0]['word'])
    assert image=={2}
    membership_pairs=0; literal_membership_letters=0
    assert len(z['actual_membership'])==n-2
    for k,cert in enumerate(z['actual_membership'],2):
        target={q for q in range(n) if inside(k,q)}
        r=min(target); outside=sorted(set(range(n))-target)
        assert cert['target']==k and cert['root']==r and cert['outside_inputs']==n-k
        cost=0; actual=set(range(n)) if full else None
        for q in outside:
            steps=swaps_for(q,r)
            length=sum(2*abs(x-y)-1 for x,y in steps)
            assert length<=4*n-6
            cost+=2*length+1
            membership_pairs+=1
            if full:
                rho=expand_swaps(steps)
                assert len(rho)==length
                word=rho+[['u',1,1]]+list(reversed(rho))
                assert apply_word_to_set({q},rho)=={1}
                assert apply_word_to_set({r},rho)=={2}
                actual=apply_word_to_set(actual,word)
                literal_membership_letters+=len(word)
        assert cost==cert['charged_cost'] and cost<=(n-k)*(8*n-11)
        # Every rho is a bijection, so the conjugated unit affects exactly q.
        # Distinct outside q inputs and a fixed target root compose onto target.
        assert len(outside)==len(set(outside)) and r not in outside
        if full: assert actual==target
    raw=[[int(inside(k,B[0])) for B in blocks] for k in range(2,n)]
    centered=[[n*v-k for v in row] for k,row in zip(range(2,n),raw)]
    for k,row in zip(range(2,n),raw):
        assert sum(v*len(B) for v,B in zip(row,blocks))==k
    assert rank(raw+[[1]*d])==z['raw_dimension']==d
    assert rank(centered)==z['normalized_dimension']==d-1
    cells=[blocks[0]]
    for B in blocks[1:]: cells.extend(([B[0]],B[1:]))
    assert len(cells)==2*d-1 and all(cells)
    cell_points=[C[0] for C in cells]
    history=[(1,[int(q==2) for q in cell_points])]
    for k in range(2,n):
        history.append((k,[int(inside(k,q)) for q in cell_points]))
        i=next(i for i in range(1,d) if (k+1)>>i&1)
        s=edge[i][0]
        history.append((k,[int(inside(k+1,q) and q!=s) for q in cell_points]))
    assert rank([v for _,v in history]+[[1]*len(cells)])==z['full_history_raw_dimension']==2*d-1
    assert rank([[n*v-k for v in row] for k,row in history])==z['full_history_normalized_dimension']==2*d-2
    for k,row in history:
        assert sum(v*len(C) for v,C in zip(row,cells))==k
    original_rows=0; complete_policy_images=0; two_letter_words=0
    finite_rt=None; finite_P=None
    if full:
        labels=[['t',j] for j in range(n-1)]+[['p',k] for k in range(2,n)]
        labels += [['u',i,sgn] for i in range(1,d) for sgn in (1,-1)]
        assert len(labels)==h
        rows=[[action(label,q) for q in range(n)] for label in labels]
        degrees=[0]*n
        for label,row in zip(labels,rows):
            assert len(set(row))==(n-1 if label[0]=='u' else n)
            for value in row: degrees[value]+=1
        assert degrees==[h]*n
        original_rows=len(rows)
        literal_raw=[[int(inside(k,q)) for q in range(n)] for k in range(2,n)]
        assert rank(literal_raw+[[1]*n])==d
        assert rank([[n*v-k for v in row] for k,row in zip(range(2,n),literal_raw)])==d-1
        point_to_cell={q:j for j,C in enumerate(cells) for q in C}
        full_history=[[row[point_to_cell[q]] for q in range(n)] for _,row in history]
        assert rank(full_history+[[1]*n])==2*d-1
        assert rank([[n*v-k for v in row] for (k,_),row in zip(history,full_history)])==2*d-2
        def inverse(S,row): return sum(1<<q for q in range(n) if S>>row[q]&1)
        def push(S,row): return sum(1<<q for q in {row[r] for r in range(n) if S>>r&1})
        if all_words:
            for k in range(2,n):
                S=sum(1<<q for q in range(n) if inside(k,q))
                assert all(inverse(S,row).bit_count()==k for row in rows)
                winning=[]
                for y in rows:
                    Y=inverse(S,y)
                    for x in rows:
                        T=inverse(Y,x)
                        if T.bit_count()>k:
                            assert T.bit_count()==k+1
                            winning.append(T)
                        two_letter_words+=1
                assert winning
        if n==7:
            Q=(1<<n)-1
            distance={Q:0}; queue=deque([Q])
            while queue:
                S=queue.popleft()
                for row in rows:
                    T=push(S,row)
                    if T not in distance:
                        distance[T]=distance[S]+1; queue.append(T)
            R=set(distance); assert R==set(range(1,1<<n))
            finite_rt=min(distance[1<<q] for q in range(n))
            G={Q:0}; W={Q:0}; extensions={}
            for k in range(n-1,0,-1):
                starts={T for T in R if T.bit_count()>k}
                dist={T:0 for T in starts}; best={T:G[T] for T in starts}; worst={T:W[T] for T in starts}
                queue=deque(starts)
                while queue:
                    T=queue.popleft()
                    for row in rows:
                        U=push(T,row); ell=dist[T]+1
                        if U not in dist:
                            dist[U]=ell; best[U]=best[T]; worst[U]=worst[T]; queue.append(U)
                        elif dist[U]==ell:
                            best[U]=min(best[U],best[T]); worst[U]=max(worst[U],worst[T])
                for S in R:
                    if S.bit_count()!=k: continue
                    contained=[T for T in R if T&S==T]
                    e=min(dist[T] for T in contained)
                    winners=[T for T in contained if dist[T]==e]
                    G[S]=e+min(best[T] for T in winners)
                    W[S]=e+max(worst[T] for T in winners)
                    extensions[S]=e
            for k in range(2,n):
                S=sum(1<<q for q in range(n) if inside(k,q))
                assert extensions[S]==2
            finite_P=min(G[1<<q] for q in range(n))
            assert n-1<=finite_rt<=finite_P<=2*n-3
            complete_policy_images=len(R)
    return dict(d=d,n=n,phase_state_controls=phase_controls,actual_membership_pairs=membership_pairs,
                literal_membership_original_letters=literal_membership_letters,original_rows=original_rows,
                literal_two_letter_words=two_letter_words,complete_policy_images=complete_policy_images,
                raw_dimension=d,normalized_dimension=d-1,common_reset_letters=2*n-3,
                full_history_raw_dimension=2*d-1,full_history_normalized_dimension=2*d-2,
                finite_rt=finite_rt,finite_P=finite_P)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',default='scripts/direct_attack/data/maximal_jump_log_history.json')
    ap.add_argument('--out',default='scripts/direct_attack/data/maximal_jump_log_history_checks.json')
    args=ap.parse_args()
    data=json.loads(Path(args.root).read_text(encoding='utf-8'))
    assert [z['d'] for z in data['records']]==list(range(3,12))
    records=[check(z,full=z['n']<=63,all_words=z['n']<=31) for z in data['records']]
    rejected=[]; witness=data['records'][0]
    for name,change in (
        ('parent',lambda z:z['stages'][1].update(parent=4)),
        ('permutation',lambda z:z['stages'][2].update(word=[['u',1,1],['p',2]])),
        ('phase_cost',lambda z:z['stages'][1].update(cost=1)),
        ('normalized_rank',lambda z:z.update(normalized_dimension=3)),
        ('membership_length',lambda z:z['actual_membership'][0].update(charged_cost=0)),
        ('all_tie_jump',lambda z:z['stages'][1].update(all_shortest_parent_size=5)),
        ('unit_block',lambda z:z['stages'][1].update(unit_block=2)),
        ('full_history_rank',lambda z:z.update(full_history_raw_dimension=z['d'])),
    ):
        bad=copy.deepcopy(witness); change(bad)
        try: check(bad)
        except AssertionError: rejected.append(name)
        else: raise AssertionError('corruption accepted: '+name)
    totals={key:sum(z[key] for z in records) for key in (
        'phase_state_controls','actual_membership_pairs','literal_membership_original_letters',
        'original_rows','literal_two_letter_words','complete_policy_images','common_reset_letters')}
    result=dict(verified=True,status='COMPUTATIONALLY VERIFIED bounded controls; no formal kernel',
                records=records,totals=totals,rejected_corruptions=rejected,
                all_parameter_status='paper log-dimension maximal shortest actual-image jump realization; rt/P only an interval; general Cerny, global policy square and long-phase tradeoff OPEN')
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,parameters=len(records),max_n=records[-1]['n'],
                         totals=totals,rejected_corruptions=rejected)))


if __name__=='__main__': main()
