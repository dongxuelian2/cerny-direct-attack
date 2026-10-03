"""Generate pair and closed high-rank certificates for image-heredity failures."""
from collections import deque
import json
from pathlib import Path
from direct_attack.near_full_search import pair_data
from direct_attack.cycle_insertion import reset_word


def construct(l):
    n=l+3;a=list(range(n));b=list(range(n))
    for q in range(l):a[q]=(q+1)%l
    a[l],a[l+1]=l+1,l
    b[0],b[1]=l,l+1
    for q in range(2,l):b[q]=q-1
    b[l]=b[l+1]=l+2;b[l+2]=l-1
    return [a,b]


def certificate(rows,V,T):
    n=len(rows[0]);Q=frozenset(range(n));start=frozenset(V);missing=frozenset(T)
    threshold=len(missing);queue=deque([Q]);words={Q:[]}
    while queue:
        S=queue.popleft()
        for a,row in enumerate(rows):
            U=frozenset(row[q] for q in S)
            if len(U)>=threshold and U not in words:words[U]=words[S]+[a];queue.append(U)
    assert start in words and missing not in words
    pairs,g,d=pair_data(rows);c=dict(n=n,rows=rows,port=n-1,pair_potential=d)
    reset,target=reset_word(c)
    return dict(n=n,rows=rows,proper_image=sorted(start),unreachable_subset=sorted(missing),
                reach_word=words[start],threshold=threshold,
                high_rank_vertices=[sorted(Q-S) for S in sorted(words,key=lambda s:(len(s),sorted(s)))],
                pair_potential=d,reset_word=reset,reset_target=target)


def main():
    out=Path('direct_attack/data/image_heredity');out.mkdir(exist_ok=True);records=[]
    for l in list(range(3,21))+[30,50]:
        rows=construct(l);n=l+3;Q=set(range(n));c=certificate(rows,Q-{0},Q-{0,n-1});c['l']=l
        (out/f'n{n}.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
        records.append(dict(n=n,vertices=len(c['high_rank_vertices']),reset_upper=len(c['reset_word'])))
    rows=[[0,0,0,0],[1,2,3,1]];c=certificate(rows,{1,2,3},{1,2})
    (out/'n4.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
    rows=[[1,0,3,2],[1,2,1,3]];c=certificate(rows,{0,2,3},{0,3})
    c.update(unit_defect=True,reset_word=[1,0,1,0,1],reset_target=1,
             discovery=dict(scope='Labeled four-state permutation/unit-defect scan stopped at first failure; no exhaustive count claim.',
                            tested=1015,synchronizing_sc=209))
    (out/'n4_unit.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
    report=dict(records=records,unrestricted_minimum=4,permutation_unit_defect_minimum=4,
                scope='Parameter family with proof; reset words are upper witnesses, not exact thresholds.')
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':main()
