"""Explicit best/worst chains for seed normal-form obstruction certificates."""
from collections import deque
import json
from pathlib import Path
from direct_attack.image_extension_policy import profile as ordinary_creator
from direct_attack.native_sparse_policy import profile


def decorate(c,include_inclusion=False):
    rows=c['rows'];n=len(rows[0]);Q=(1<<n)-1
    def step(S,a):return sum(1<<r for r in {rows[a][q] for q in range(n) if S>>q&1})
    reach={Q:[]};queue=deque([Q])
    while queue:
        T=queue.popleft()
        for a in range(len(rows)):
            U=step(T,a)
            if U not in reach:reach[U]=reach[T]+[a];queue.append(U)
    merged=[]
    for T in reach:
        if T.bit_count()<2:continue
        labels=[dict(letter=a,target=step(T,a)) for a in range(len(rows)) if step(T,a).bit_count()==1]
        if labels:merged.append(dict(image=T,size=T.bit_count(),labels=labels,reach_word=reach[T],G=c['best'][T],W=c['worst'][T]))
    metrics=profile(rows,seed_budget=True);assert metrics is not None and not metrics['truncated']
    for key in ['best_policy','worst_policy','rt']:assert metrics[key]==c[key]
    def transport(T,S,cost):
        words={T:[]};queue=deque([T])
        while queue:
            U=queue.popleft()
            if U&S==U:assert len(words[U])==cost;return words[U]
            if len(words[U])==cost:continue
            for a in range(len(rows)):
                V=step(U,a)
                if V not in words:words[V]=words[U]+[a];queue.append(V)
        return None
    def chain(start,key):
        S=start;word=[];phases=[]
        while S!=Q:
            cost=c['extension'][S];tail=c[key][S]-cost
            for T in sorted(reach):
                if T.bit_count()<=S.bit_count() or c[key][T]!=tail:continue
                w=transport(T,S,cost)
                if w is not None:break
            else:raise AssertionError('No exact policy parent')
            assert step(T,w[0]).bit_count()<=S.bit_count()
            word=w+word;phases.append(dict(start=S,larger=T,word=w));S=T
        return dict(start=start,key=key,word=word,phases=phases)
    def seed_chain(targets,key):
        m=min(targets,key=lambda m:c[key][m['image']]) if key=='best' else max(targets,key=lambda m:c[key][m['image']])
        out=chain(m['image'],key);label=m['labels'][0];out.update(merged_image=m['image'],merge_letter=label['letter'],target=label['target'])
        out['reset_word']=out['word']+[label['letter']];out['budget']=len(out['reset_word']);return out
    maximum=[m for m in merged if m['size']==metrics['kappa']]
    c.update(seed_budget=metrics,one_letter_images=merged,
             seed_best_chain=seed_chain(merged,'best'),anchor_best_chain=seed_chain(maximum,'best'),
             anchor_worst_chain=seed_chain(maximum,'worst'),seed_worst_chain=seed_chain(merged,'worst'))
    assert c['seed_best_chain']['budget']==metrics['seed_best']==c['best_policy']
    assert c['anchor_best_chain']['budget']==metrics['anchor_best'] and c['anchor_worst_chain']['budget']==metrics['anchor_worst']
    if include_inclusion:
        maximal=set()
        for m in merged:
            for label in m['labels']:
                group=[u for u in merged if label in u['labels']]
                if not any(m['image']!=u['image'] and m['image']&u['image']==m['image'] for u in group):
                    maximal.add(m['image'])
        c['inclusion_maximal_images']=sorted(maximal)
        c['inclusion_best_chain']=seed_chain([m for m in merged if m['image'] in maximal],'best')
        c['inclusion_budget']=c['inclusion_best_chain']['budget']
    return c


def main():
    root=Path('scripts/direct_attack/data/seed_budget_obstructions');root.mkdir(exist_ok=True)
    cases=[('arbitrary_minimum_n4',[[0,0,0,3],[3,0,1,2],[3,0,1,3]]),
           ('binary_minimum_n5',[[0,0,0,0,1],[4,1,1,2,3]]),
           ('worst_ties_binary_n6',[[0,1,2,4,3,3],[1,3,5,0,2,4]])]
    records=[]
    for name,rows in cases:
        c=decorate(ordinary_creator(rows));(root/(name+'.json')).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
        records.append(dict(file=name+'.json',n=c['n'],P=c['best_policy'],F=c['seed_budget']['seed_best'],Fk=c['seed_budget']['anchor_best'],Wk=c['seed_budget']['anchor_worst'],rt=c['rt']))
    (root/'summary.json').write_text(json.dumps(dict(records=records),indent=2)+'\n',encoding='utf-8');print(json.dumps(records))


if __name__=='__main__':main()
