"""Complete literal finite audit of the short-rooted-word counterexample."""
from collections import deque
from copy import deepcopy
from itertools import product
from pathlib import Path
import json


def action(rows,word):
    result=list(range(len(rows[0])))
    for a in word:result=[rows[a][q] for q in result]
    return result


def power(row,t):
    result=list(range(len(row)))
    for _ in range(t):result=[row[q] for q in result]
    return result


def verify(z):
    rows=z['rows'];assert rows==[[0,0,1,3],[3,1,3,2]]
    short={};words=0
    for length in range(5):
        for word in product(range(2),repeat=length):
            row=action(rows,word);words+=1
            assert len(set(power(row,4)))>1
            key=tuple(row)
            if key not in short:short[key]=list(word)
    actions=[dict(row=list(row),word=word,fourth_power=power(row,4)) for row,word in short.items()]
    assert words==31 and len(actions)==22 and actions==z['short_actions']
    assert z['words_checked']==words and z['distinct_short_transformations']==len(actions)
    power_cases=0
    for prefix in rows:
        for length in range(5):
            for word in product(range(2),repeat=length):
                row=power(action(rows,word),2)
                assert len({row[q] for q in prefix})>1
                power_cases+=1
    assert z['one_letter_power_cases']==power_cases==62
    assert z['one_letter_power_template_refuted'] is True
    v=z['rooted_word'];row=action(rows,v)
    assert v==[0,0,1,0,1] and row==z['rooted_row']==[2,2,2,1]
    assert len(v)==z['minimum_rooted_length']==5
    assert len(set(row))==2 and power(row,2)==[2]*4
    assert z['root_height']==2 and z['root_state']==2
    reset=z['reset_word'];assert reset==[0,0,1,0,1,0,0]
    assert len(set(action(rows,reset)))==1
    # Ordinary full actual-image closure, with complete shortest distances.
    initial=frozenset(range(4));dist={initial:0};todo=deque([initial])
    while todo:
        S=todo.popleft()
        for row in rows:
            T=frozenset(row[q] for q in S)
            if T not in dist:dist[T]=dist[S]+1;todo.append(T)
    assert min(d for S,d in dist.items() if len(S)==1)==z['rt']==len(reset)==7
    for start in range(4):
        seen={start};todo=deque([start])
        while todo:
            q=todo.popleft()
            for row in rows:
                r=row[q]
                if r not in seen:seen.add(r);todo.append(r)
        assert len(seen)==4
    return len(dist)


def main():
    rows=[[0,0,1,3],[3,1,3,2]];short={}
    for length in range(5):
        for word in product(range(2),repeat=length):
            row=tuple(action(rows,word))
            if row not in short:short[row]=list(word)
    z=dict(rows=rows,minimum_rooted_length=5,rooted_word=[0,0,1,0,1],rooted_row=[2,2,2,1],root_state=2,root_height=2,
           reset_word=[0,0,1,0,1,0,0],rt=7,words_checked=31,distinct_short_transformations=22,
           one_letter_power_cases=62,one_letter_power_template_refuted=True,
           short_actions=[dict(row=list(row),word=word,fourth_power=power(row,4)) for row,word in short.items()])
    vertices=verify(z);corruptions=[]
    for field in ('minimum_rooted_length','rooted_row','short_actions','root_height','one_letter_power_template_refuted'):
        bad=deepcopy(z)
        if field=='rooted_row':bad[field][3]=2
        elif field=='short_actions':bad[field].pop()
        elif field=='one_letter_power_template_refuted':bad[field]=False
        else:bad[field]-=1
        try:verify(bad)
        except AssertionError:corruptions.append(field)
        else:raise AssertionError('accepted corrupted '+field)
    report=dict(verified=True,witness=z,actual_image_vertices=vertices,corruptions_rejected=corruptions,
                scope='complete original words through four for one SC binary synchronizing DFA; no minimum-state claim',
                status='short-rooted-word length<=n and one-letter short-power square template REFUTED; bounded claims COMPUTATIONALLY VERIFIED; no Cerny counterexample or formal verification')
    Path('direct_attack/data/short_rooted_word_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='witness'}),flush=True)


if __name__=='__main__':main()
