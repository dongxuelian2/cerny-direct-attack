"""Independent ordinary-set full-distance audit of saved rank-three peaks."""
from collections import deque
import json
from pathlib import Path
import time
from direct_attack.audit_sparse_policy import ordinary_forward


def verify(c,rank=3):
    rows=c['rows'];n=len(rows[0]);Q=frozenset(range(n))
    assert sorted(rows[0])==list(range(n)) and len(set(rows[1]))==rank
    for start in Q:
        seen={start};queue=deque([start])
        while queue:
            q=queue.popleft()
            for row in rows:
                if row[q] not in seen:seen.add(row[q]);queue.append(row[q])
        assert seen==Q
    a=ordinary_forward(rows)
    for key in ['extension','best','worst','forward']:
        assert c[key]=={str(S):v for S,v in a[key].items()},key
    assert c['reachable']==len(a['forward']) and c['max_proper_rank']==rank
    assert c['max_extension']==a['extension'][c['extension_start']]==max(a['extension'].values())
    assert c['rt']==min(a['forward'][1<<q] for q in Q)
    assert c['best_policy']==min(a['best'][1<<q] for q in Q)
    assert c['worst_policy']==max(a['worst'][1<<q] for q in Q)
    S=frozenset(q for q in Q if c['extension_start']>>q&1)
    R=[frozenset(q for q in Q if mask>>q&1) for mask in a['forward']]
    predecessor={T:None for T in R if len(T)>len(S)};queue=deque(predecessor)
    while queue:
        T=queue.popleft()
        if T<=S:break
        for label,row in enumerate(rows):
            U=frozenset(row[q] for q in T)
            if U not in predecessor:predecessor[U]=(T,label);queue.append(U)
    else:raise AssertionError('No extension witness')
    word=[];U=T
    while predecessor[U] is not None:
        U,label=predecessor[U];word.append(label)
    word.reverse();assert len(word)==c['max_extension'] and len(U)>len(S)
    return dict(n=n,images=len(R),max_extension=c['max_extension'],rt=c['rt'],P=c['best_policy'],
                target=sorted(S),larger_image=sorted(U),terminal_image=sorted(T),extension_word=word,
                all_entries_checked=True)


def main():
    started=time.monotonic();records=[]
    roots=sorted(Path('direct_attack/data').glob('rank_three_extension_n*'))+sorted(Path('direct_attack/data').glob('rank_bounded_extension_n*'))
    for root in roots:
        summary=json.loads((root/'summary.json').read_text());local=[]
        rank=summary['arguments'].get('rank',3)
        for name in summary['records']:
            c=json.loads((root/name).read_text());r=verify(c,rank);r.update(rank=rank,file=str(root/name).replace('\\','/'));local.append(r)
            print(json.dumps(dict(file=r['file'],verified=True,images=r['images'])),flush=True)
        assert max((r['max_extension'],r['P']) for r in local)==tuple(summary['best'])
        records+=local
    c=json.loads(Path(records[0]['file']).read_text());rejected=[]
    for field in ['extension_start','best_policy','forward']:
        d=json.loads(json.dumps(c))
        if field=='extension_start':d[field]=0
        elif field=='best_policy':d[field]+=1
        else:d[field][str((1<<d['n'])-1)]=1
        try:verify(d)
        except (AssertionError,KeyError):rejected.append(field)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,records=records,corruptions_rejected=rejected,seconds=time.monotonic()-started,
                boundary='Every retained e/G/worst/forward entry uses independent all-source ordinary forward distances. Sampled negative counts are not exhaustive coverage.')
    Path('direct_attack/data/rank_three_independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),all_entries_checked=True,corruptions_rejected=rejected,seconds=report['seconds'])))


if __name__=='__main__':main()
