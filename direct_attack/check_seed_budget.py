"""Inverse-set independent policy checks and complete words for seed obstructions/peaks."""
from collections import deque
import argparse
import json
from pathlib import Path
import time
from direct_attack.check_image_policy import verify as inverse_verify
from direct_attack.audit_sparse_policy import ordinary_forward
from direct_attack.ordinary_reverse_policy import profile as ordinary_reverse


def verify(c,words=False):
    rows=c['rows'];n=c['n'];Q=frozenset(range(n));mask=lambda T:sum(1<<q for q in T)
    def apply(T,w):
        for a in w:T=frozenset(rows[a][q] for q in T)
        return T
    method='ordinary_all_source_forward' if len(c['best'])<=200 else 'ordinary_per_target_reverse'
    p=ordinary_forward(rows) if method=='ordinary_all_source_forward' else ordinary_reverse(rows)
    for key in ['extension','best','worst']:assert c[key]=={str(T):v for T,v in p[key].items()}
    if 'forward' in c:assert c['forward']=={str(T):v for T,v in p['forward'].items()}
    R={frozenset(q for q in range(n) if T>>q&1) for T in p['best']}
    merged={T:[a for a in range(len(rows)) if len(apply(T,[a]))==1] for T in R if len(T)>1}
    merged={T:labels for T,labels in merged.items() if labels};kappa=max(map(len,merged))
    expected=dict(kappa=kappa,seed_best=1+min(p['best'][mask(T)] for T in merged),
        anchor_best=1+min(p['best'][mask(T)] for T in merged if len(T)==kappa),
        anchor_worst=1+max(p['worst'][mask(T)] for T in merged if len(T)==kappa))
    for key,value in expected.items():assert c['seed_budget'][key]==value
    assert expected['seed_best']==c['best_policy']==min(p['best'][1<<q] for q in range(n))
    assert c['rt']==min(p['forward'][1<<q] for q in range(n))
    if words:
        inverse_verify(c)
        assert {m['image'] for m in c['one_letter_images']}=={mask(T) for T in merged}
        for m in c['one_letter_images']:
            T=frozenset(q for q in range(n) if m['image']>>q&1)
            assert apply(Q,m['reach_word'])==T and m['size']==len(T)
            assert m['labels']==[dict(letter=a,target=mask(apply(T,[a]))) for a in merged[T]]
            assert m['G']==p['best'][mask(T)] and m['W']==p['worst'][mask(T)]
        for key in ['seed_best_chain','anchor_best_chain','anchor_worst_chain','seed_worst_chain']:
            chain=c[key];T=frozenset(q for q in range(n) if chain['merged_image']>>q&1);assert T in merged
            if key.startswith('anchor_'):assert len(T)==kappa
            S=T;word=[];valuekey=chain['key']
            for phase in chain['phases']:
                A=frozenset(q for q in range(n) if phase['start']>>q&1);B=frozenset(q for q in range(n) if phase['larger']>>q&1)
                assert A==S and B in R and len(B)>len(A)
                assert len(phase['word'])==p['extension'][mask(A)] and apply(B,phase['word'])<=A
                assert len(apply(B,phase['word'][:1]))<=len(A)
                assert p[valuekey][mask(A)]==len(phase['word'])+p[valuekey][mask(B)]
                word=phase['word']+word;S=B
            assert S==Q and word==chain['word'] and apply(Q,word)<=T
            assert len(word)==p[valuekey][mask(T)]
            assert chain['merge_letter'] in merged[T]
            assert chain['reset_word']==word+[chain['merge_letter']] and len(chain['reset_word'])==chain['budget']
            assert apply(Q,chain['reset_word'])==frozenset(q for q in range(n) if chain['target']>>q&1)
        assert c['seed_best_chain']['budget']==expected['seed_best']
        assert c['anchor_best_chain']['budget']==expected['anchor_best'] and c['anchor_worst_chain']['budget']==expected['anchor_worst']
    return dict(n=n,images=len(R),rt=c['rt'],P=c['best_policy'],**expected,words_checked=words,method=method)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',default='independent_checks.json');args=ap.parse_args()
    assert Path(args.out).name==args.out and args.out.endswith('.json')
    started=time.monotonic();records=[];root=Path('direct_attack/data/seed_budget_obstructions')
    for path in sorted(root.glob('*.json')):
        if path.name=='summary.json' or path.name.endswith('checks.json'):continue
        records.append(dict(file=str(path),**verify(json.loads(path.read_text()),True)))
    for folder in sorted(Path('direct_attack/data').glob('seed_budget_*')):
        if not (folder/'summary.json').exists() or folder.name=='seed_budget_obstructions':continue
        for name in json.loads((folder/'summary.json').read_text())['records']:
            records.append(dict(file=str(folder/name),**verify(json.loads((folder/name).read_text()))))
    c=json.loads((root/'worst_ties_binary_n6.json').read_text());assert c['seed_worst_chain']['budget']==26 and c['best_policy']==25
    rejected=[]
    for field in ['seed_budget','one_letter_images','anchor_worst_chain']:
        d=json.loads(json.dumps(c))
        if field=='seed_budget':d[field]['kappa']+=1
        elif field=='one_letter_images':d[field][0]['reach_word']=d[field][0]['reach_word'][:-1]
        else:d[field]['reset_word']=d[field]['reset_word'][:-1]
        try:verify(d,True)
        except AssertionError:rejected.append(field)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,records=records,corruptions_rejected=rejected,seconds=time.monotonic()-started,
        boundary='Every retained e/G/W array and seed metric independently recomputed: small graphs use ordinary all-source forward BFS; larger ones use a separate reverse BFS for EACH containment target on the ordinary full image graph. Three obstruction files additionally have inverse-set policy verification, all actual seed reach words and concrete best/worst chains.')
    (root/args.out).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(records),corruptions_rejected=rejected,seconds=report['seconds'],methods={m:sum(r['method']==m for r in records) for m in sorted({r['method'] for r in records})})))


if __name__=='__main__':main()
