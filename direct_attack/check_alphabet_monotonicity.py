"""Independent set-policy and individual-transformation closure audit."""
from collections import deque
from copy import deepcopy
import json
from pathlib import Path
from direct_attack.check_image_policy import verify as policy_verify


def monoid(rows):
    identity=tuple(range(len(rows[0])));distance={identity:0};queue=deque([identity])
    while queue:
        transformation=queue.popleft()
        for row in rows:
            following=tuple(row[q] for q in transformation)
            if following not in distance:distance[following]=distance[transformation]+1;queue.append(following)
    return distance


def set_distances(rows,S):
    distance={S:0};queue=deque([S])
    while queue:
        X=queue.popleft()
        for row in rows:
            Y=frozenset(row[q] for q in X)
            if Y not in distance:distance[Y]=distance[X]+1;queue.append(Y)
    return distance


def connected(rows):
    Q=set(range(len(rows[0])))
    for start in Q:
        seen={start};queue=deque([start])
        while queue:
            q=queue.popleft()
            for row in rows:
                if row[q] not in seen:seen.add(row[q]);queue.append(row[q])
        assert seen==Q


def verify(base,augmented,meta):
    before=policy_verify(base);after=policy_verify(augmented)
    rows=base['rows'];new_rows=augmented['rows'];n=base['n'];Q=frozenset(range(n))
    assert augmented['n']==n and len(new_rows)==len(rows)+1 and new_rows[:-1]==rows
    connected(rows);connected(new_rows)
    assert meta['base_policy']==before['best_policy'] and meta['augmented_policy']==after['best_policy']
    assert meta['base_rt']==before['rt'] and meta['augmented_rt']==after['rt']
    assert after['best_policy']>before['best_policy'] and after['rt']<=before['rt']
    R=set(set_distances(rows,Q));Rnew=set(set_distances(new_rows,Q));assert R<=Rnew
    common=list(base['extension'])
    assert all(augmented['extension'][s]<=base['extension'][s] for s in common)
    increased=[int(s) for s in base['best'] if augmented['best'][s]>base['best'][s]]
    improvements=0
    for S in R:
        d=set_distances(rows,S);dnew=set_distances(new_rows,S)
        assert all(T in dnew and dnew[T]<=v for T,v in d.items())
        improvements+=sum(dnew[T]<v for T,v in d.items())
    size=None;shortcut_length=None
    if meta['kind']=='semigroup':
        word=meta['extra_word'];transformation=tuple(range(n))
        assert all(type(a) is int and 0<=a<len(rows) for a in word)
        for a in word:transformation=tuple(rows[a][q] for q in transformation)
        assert transformation==tuple(new_rows[-1])
        M=monoid(rows);Mnew=monoid(new_rows)
        assert set(M)==set(Mnew) and len(M)==meta['base_monoid_size'] and R==Rnew
        assert M[transformation]==len(word)
        size=len(M);shortcut_length=len(word)
    return dict(n=n,kind=meta['kind'],base_policy=before['best_policy'],augmented_policy=after['best_policy'],
                base_rt=before['rt'],augmented_rt=after['rt'],same_images=R==Rnew,
                monoid_size=size,shortest_shortcut_length=shortcut_length,
                exact_distance_improvements=improvements,increased_policy_images=sorted(increased),verified=True)


def main():
    root=Path('direct_attack/data/alphabet_monotonicity');records=[];complete=[];cases=[]
    for directory in sorted(root.iterdir()):
        if not directory.is_dir():continue
        c=json.loads((directory/'summary.json').read_text())
        if c['first_failure'] is None:
            assert c['complete'];complete.append(dict(file=str(directory/'summary.json'),counts=c['counts']))
            continue
        base=json.loads((directory/'base.json').read_text());augmented=json.loads((directory/'augmented.json').read_text())
        records.append(dict(directory=str(directory),**verify(base,augmented,c['first_failure'])))
        cases.append((base,augmented,c['first_failure']))
    base,augmented,meta=next(case for case in cases if case[2]['kind']=='semigroup')
    rejected=[]
    for field in ['shortcut_word','extra_transformation','global_policy']:
        b=deepcopy(base);a=deepcopy(augmented);m=deepcopy(meta)
        if field=='shortcut_word':m['extra_word']=m['extra_word'][:-1]
        elif field=='extra_transformation':a['rows'][-1][0]=(a['rows'][-1][0]+1)%a['n']
        else:m['augmented_policy']-=1
        try:verify(b,a,m)
        except AssertionError:rejected.append(field)
        else:raise AssertionError('Corruption accepted: '+field)
    report=dict(records=records,complete_binary_runs=complete,corruptions_rejected=rejected,
                negative_count_boundary='Counts copied from generator; independent policy proof and n<=3 paper optimality establish minimality.',verified=True)
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
