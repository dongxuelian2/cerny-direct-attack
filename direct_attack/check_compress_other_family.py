"""Separate ordinary-row/pair audit of the charged public-family witnesses.

Imports neither the generator nor previous research solvers. Finite equality
does not establish the unresolved all-parameter lower-threshold assertion.
"""
from collections import deque
from copy import deepcopy
from pathlib import Path
import argparse
import json


def expected_letters(p):
    n=3*p
    a,b=[],[]
    for i in range(n):
        if i==0: x=0
        elif i<2*p: x=i+1 if i%2 else i-1
        elif i==2*p: x=2*p+1
        elif i==2*p+1: x=3
        elif i%2: x=i-1
        else: x=min(i+1,n-1)
        if i<2*p: y=i+1 if not i%2 else i-1
        elif i==2*p: y=2
        elif i%2: y=min(i+1,n-1)
        else: y=i-1
        a.append(x);b.append(y)
    return a,b


def act(rows,word,states):
    states=list(states)
    for letter in word:
        assert letter in (0,1)
        states=[rows[letter][q] for q in states]
    return states


def strongly_connected(rows):
    n=len(rows[0])
    forward=[set() for _ in range(n)];reverse=[set() for _ in range(n)]
    for row in rows:
        for q,r in enumerate(row):forward[q].add(r);reverse[r].add(q)
    for graph in (forward,reverse):
        seen={0};todo=[0]
        for q in todo:
            for r in graph[q]:
                if r not in seen:seen.add(r);todo.append(r)
        assert len(seen)==n


def independent_pairs(rows):
    n=len(rows[0]);reverse=[[] for _ in range(n*n)]
    distance=[-1]*(n*n);todo=deque()
    for q in range(n):distance[n*q+q]=0;todo.append(n*q+q)
    for q in range(n):
        for r in range(q,n):
            for row in rows:
                x,y=sorted((row[q],row[r]))
                reverse[n*x+y].append(n*q+r)
    while todo:
        target=todo.popleft()
        for source in reverse[target]:
            if distance[source]<0:
                distance[source]=distance[target]+1;todo.append(source)
    assert all(distance[n*q+r]>0 for q in range(n) for r in range(q+1,n))
    # Check every Bellman edge, not just distances from the designated state.
    for q in range(n):
        for r in range(q+1,n):
            next_distances=[]
            for row in rows:
                x,y=sorted((row[q],row[r]));next_distances.append(distance[n*x+y])
            assert distance[n*q+r]==1+min(next_distances)
    return [distance[q] for q in range(n)]


def verify_record(z,check_pairs=True):
    k,p,n=z['k'],z['p'],z['n']
    assert k>=1 and p==k+2 and n==3*p
    a,b=expected_letters(p);rows=[a,b]
    assert rows==z['rows']
    assert len(set(a))==len(set(b))==n-1
    strongly_connected(rows)
    core=[0]+[2*j for j in range(1,p)]+[2*p,1]
    other_core=[0,1]+[2*j+1 for j in range(1,p)]+[2]
    index={q:i for i,q in enumerate(core)};r=p+2
    assert z['core']==core
    assert z['cycle_word']==[1,0]
    assert z['entering_word']==[1,0]*p
    assert z['reflection_word']==[0,1]*p+[0]
    assert z['rooted_word']==z['reflection_word']+[1,0]+z['reflection_word']
    assert set(act(rows,z['entering_word'],range(n)))==set(core)
    assert set(act(rows,[0,1]*p,range(n)))==set(other_core)
    assert {a[q] for q in other_core}==set(core)
    c=act(rows,[1,0],core)
    d=act(rows,z['reflection_word'],core)
    v=act(rows,z['rooted_word'],core)
    assert [index[q] for q in c]==[(i+1)%r for i in range(r)]
    d_positions=[p-i if i<p else p+1 for i in range(r)]
    v_positions=[p+1 if i<2 else i-1 if i<p else p for i in range(r)]
    assert [index[q] for q in d]==d_positions==z['reflection_core_row']
    assert [index[q] for q in v]==v_positions==z['rooted_core_row']
    assert [d_positions[(d_positions[i]+1)%r] for i in range(r)]==v_positions
    roots=[];maximum_height=0
    for start in range(r):
        path=[];q=start
        while q not in path:path.append(q);q=v_positions[q]
        cycle=path[path.index(q):]
        assert cycle==[p]
        maximum_height=max(maximum_height,path.index(p))
    assert maximum_height==p
    image=set(range(r));stages=[r]
    for _ in range(p):image={v_positions[q] for q in image};stages.append(len(image))
    assert image=={p} and stages==z['root_stage_ranks']
    assert z['root_state']==2*p and z['root_power']==p
    original_length=len(z['entering_word'])+z['root_power']*len(z['rooted_word'])
    assert original_length==z['reset_length']==4*p*p+6*p
    assert z['square_slack']==(n-1)**2-original_length==5*(p-3)**2+18*(p-3)+10
    assert z['square_slack']>0
    assert z['q0_upper_word']==[1,0]*p+[0,1]*p
    assert z['q0_upper_partner']==2 and z['q0_upper_length']==4*p
    assert act(rows,z['q0_upper_word'],[0,2])==[2,2]
    # The SOURCE word is one letter longer and starts with another partner.
    printed=[0,1]*p+[0]+[0,1]*p
    assert len(printed)==4*p+1 and act(rows,printed,[0,1])==[2,2]
    literal=0
    if k<=12:
        expanded=z['entering_word']+z['rooted_word']*p
        assert expanded==z['literal_whole_Q_reset_word']
        assert len(expanded)==original_length and set(act(rows,expanded,range(n)))=={2*p}
        literal=original_length
    assert not z['whole_Q_exact_threshold_claim'] and not z['all_n_q0_lower_bound_claim']
    vertices=0
    if 'pair_audit' in z and check_pairs:
        saved=z['pair_audit'];distances=independent_pairs(rows)
        assert distances==saved['q0_distances']
        assert saved['q0_minimum']==min(distances[1:])==4*p
        partner=saved['partner'];word=saved['shortest_pair_word']
        assert partner!=0 and len(word)==distances[partner]
        assert len(set(act(rows,word,[0,partner])))==1
        vertices=n*(n-1)//2
        assert vertices==saved['pair_vertices'] and saved['all_pairs_synchronizing']
    return dict(n=n,k=k,original_reset_length=original_length,root_height=p,
                finite_pair_vertices=vertices,literal_full_reset_length=literal)


def verify_reflected_phase(r,t):
    assert r>=4 and 0<=t<r
    c=[(q+1)%r for q in range(r)]
    d=[r-1 if (t-q)%r==0 else (t-q)%r for q in range(r)]
    # t=0 is deliberately handled by a longer ACTUAL word, not an inverse.
    word=[0,1,0,0,1] if t==0 else [1,0,1]
    v=act([c,d],word,range(r));root=r-1 if t==0 else t
    reverse=[[] for _ in range(r)]
    for q,image in enumerate(v):reverse[image].append(q)
    height={root:0};todo=deque([root])
    while todo:
        for q in reverse[todo.popleft()]:
            if q not in height:
                height[q]=height[v[q]]+1;todo.append(q)
    assert len(height)==r and v[root]==root
    actual=max(height.values());expected=r-1 if t==1 else r-2
    assert actual==expected
    if t==0:
        bad=act([c,d],[1,0,1],range(r))
        assert all(bad[q]!=q for q in range(r))
    return dict(r=r,phase=t,actual_word=word,root=root,exact_root_height=actual)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,default=Path('direct_attack/data/compress_other_family.json'))
    ap.add_argument('--out',type=Path,default=Path('direct_attack/data/compress_other_family_checks.json'))
    args=ap.parse_args();source=json.loads(args.source.read_text())
    expected=list(range(1,65))+[100,128,256,512,1024]
    assert [z['k'] for z in source['records']]==expected
    assert source['scopes']['pair_parameters']==expected[:-2]
    reports=[verify_record(z) for z in source['records']]
    phase_cases=[];phase_count=0;phase_vertices=0
    for r in range(4,201):
        for t in range(r):
            case=verify_reflected_phase(r,t);phase_count+=1;phase_vertices+=r
            if r<=12 or r in (100,200) and t in (0,1,r-1):phase_cases.append(case)
    corruptions=[]
    for field in ('rows','rooted_word','reflection_core_row','reset_length','q0_minimum','root_state'):
        z=deepcopy(source['records'][0])
        if field=='rows':z[field][1][0]=0
        elif field=='rooted_word':z[field][0]^=1
        elif field=='reflection_core_row':z[field][0]=0
        elif field=='q0_minimum':z['pair_audit'][field]+=1
        else:z[field]+=1
        try:verify_record(z)
        except (AssertionError,KeyError):corruptions.append(field)
        else:raise AssertionError('corrupted field accepted: '+field)
    report=dict(verified=True,records=len(reports),reports=reports,
                pair_vertices=sum(r['finite_pair_vertices'] for r in reports),
                literal_full_Q_reset_words=sum(r['literal_full_reset_length']>0 for r in reports),
                literal_full_Q_reset_letters=sum(r['literal_full_reset_length'] for r in reports),
                reflected_phase_controls=phase_count,reflected_phase_vertices=phase_vertices,
                selected_reflected_phases=phase_cases,
                corruptions_rejected=corruptions,
                implementation='independent case rows, original word action, triangular pair array BFS and every Bellman edge',
                status='COMPUTATIONALLY VERIFIED in recorded finite scopes; all-n q0 lower bound OPEN; no formal verification or exact full reset threshold')
    assert report['pair_vertices']==source['scopes']['pair_vertices']
    args.out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('reports','selected_reflected_phases')}),flush=True)


if __name__=='__main__':main()
