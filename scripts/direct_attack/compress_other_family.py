"""Literal diagram-completed public family and charged rooted-word witnesses.

This generator does not assert the unproved all-parameter lower threshold.
"""
from collections import deque
from pathlib import Path
import argparse
import json

SOURCE_URL = 'https://arxiv.org/pdf/2608.24245v1'
SOURCE_PDF_SHA256 = '62fcce9693c7e44f209f65c95939c48a08d5cf035627ffe67f56b7da59889208'


def transitions(k):
    assert k >= 1
    p, n = k+2, 3*(k+2)
    a, b = list(range(n)), list(range(n))
    for i in range(1, 2*p):
        a[i] = i+1 if i % 2 else i-1
    for i in range(2*p):
        b[i] = i+1 if not i % 2 else i-1
    a[2*p], a[2*p+1], b[2*p] = 2*p+1, 3, 2
    for i in range(2*p+2, n-1, 2):
        a[i], a[i+1] = i+1, i
    for i in range(2*p+1, n-1, 2):
        b[i], b[i+1] = i+1, i
    return [a, b]


def row_action(rows, word, states=None):
    result = list(range(len(rows[0]))) if states is None else list(states)
    for a in word:
        result = [rows[a][q] for q in result]
    return result


def pair_report(rows):
    n = len(rows[0])
    pairs = [(q,r) for q in range(n) for r in range(q+1,n)]
    index = {pair:i for i,pair in enumerate(pairs)}
    reverse, distance, choice = [[] for _ in pairs], [-1]*len(pairs), [-1]*len(pairs)
    todo = deque()
    for i,(q,r) in enumerate(pairs):
        for a,row in enumerate(rows):
            x,y = sorted((row[q],row[r]))
            if x == y:
                if distance[i] < 0:
                    distance[i], choice[i] = 1, a
                    todo.append(i)
            else:
                reverse[index[x,y]].append((i,a))
    while todo:
        i = todo.popleft()
        for j,a in reverse[i]:
            if distance[j] < 0:
                distance[j], choice[j] = distance[i]+1, a
                todo.append(j)
    assert all(d > 0 for d in distance)
    q0 = [0]+[distance[index[0,q]] for q in range(1,n)]
    partner = min(range(1,n), key=lambda q:q0[q])
    pair, word = (0,partner), []
    while pair[0] != pair[1]:
        i = index[pair]
        a = choice[i]
        word.append(a)
        pair = tuple(sorted(rows[a][q] for q in pair))
    return dict(pair_vertices=len(pairs), all_pairs_synchronizing=True,
                q0_distances=q0, q0_minimum=min(q0[1:]), partner=partner,
                shortest_pair_word=word)


def record(k, full_pairs=True):
    rows, p = transitions(k), k+2
    n, r = len(rows[0]), p+2
    core = [0]+list(range(2,2*p,2))+[2*p,1]
    c, entering, d = [1,0], [1,0]*p, [0,1]*p+[0]
    v = d+c+d
    c_row = row_action(rows,c,core)
    d_row = row_action(rows,d,core)
    v_row = row_action(rows,v,core)
    index = {q:i for i,q in enumerate(core)}
    expected_d = list(range(p,0,-1))+[p+1,p+1]
    expected_v = [p+1,p+1]+list(range(1,p-1))+[p,p]
    assert [index[q] for q in c_row] == list(range(1,r))+[0]
    assert [index[q] for q in d_row] == expected_d
    assert [index[q] for q in v_row] == expected_v
    assert set(row_action(rows,entering)) == set(core)
    image, stages = set(core), [r]
    for _ in range(p):
        image = {v_row[index[q]] for q in image}
        stages.append(len(image))
    assert image == {2*p}
    z = [1,0]*p+[0,1]*p
    assert row_action(rows,z,[0,2]) == [2,2]
    result = dict(k=k,p=p,n=n,rows=rows,core=core,entering_word=entering,
                  cycle_word=c,reflection_word=d,rooted_word=v,root_power=p,
                  reflection_core_row=expected_d,rooted_core_row=expected_v,
                  root_state=2*p,root_stage_ranks=stages,
                  reset_length=len(entering)+p*len(v),
                  square_slack=(n-1)**2-(len(entering)+p*len(v)),
                  q0_upper_word=z,q0_upper_partner=2,q0_upper_length=len(z),
                  whole_Q_exact_threshold_claim=False,all_n_q0_lower_bound_claim=False)
    if k <= 12:
        word = entering+v*p
        assert set(row_action(rows,word)) == {2*p}
        result['literal_whole_Q_reset_word'] = word
    if full_pairs:
        result['pair_audit'] = pair_report(rows)
        assert result['pair_audit']['q0_minimum'] == 4*p
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/compress_other_family.json'))
    args = ap.parse_args()
    pair_parameters = list(range(1,65))+[100,128,256]
    large_parameters = [512,1024]
    records = [record(k) for k in pair_parameters]+[record(k,False) for k in large_parameters]
    report = dict(verified=True,source=dict(url=SOURCE_URL,pdf_sha256=SOURCE_PDF_SHA256,
                  interpretation='Figure 3 completion; b(0)=1 and final matching cases explicit'),
                  arguments=dict(out=str(args.out)),records=records,
                  scopes=dict(core_witnesses=len(records),pair_parameters=pair_parameters,
                              large_macro_parameters=large_parameters,
                              pair_vertices=sum(z['pair_audit']['pair_vertices'] for z in records if 'pair_audit' in z),
                              literal_full_reset_parameters=list(range(1,13))),
                  status='PROVED paper synchronization/square witness; bounded equality COMPUTATIONALLY VERIFIED; all-n q0 lower bound OPEN; no formal verification')
    args.out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,**report['scopes'])),flush=True)


if __name__ == '__main__':
    main()
