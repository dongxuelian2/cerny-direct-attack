"""Independent inclusion lists, policy chains and complete binary n2..5 cover."""
from collections import Counter
import json
from pathlib import Path
import time
from direct_attack.ordinary_reverse_policy import profile
from direct_attack.check_seed_budget import verify as seed_verify
from direct_attack.mine import inputs


def metrics(rows,p):
    Q=frozenset(range(len(rows[0])));R={frozenset(q for q in Q if T>>q&1):v for T,v in p['best'].items()};bylabel={}
    for T in R:
        if len(T)<2:continue
        for x,row in enumerate(rows):
            U=frozenset(row[q] for q in T)
            if len(U)==1:bylabel.setdefault((x,U),[]).append(T)
    maximal={T for Ts in bylabel.values() for T in Ts if not any(T<U for U in Ts)}
    return 1+min(R[T] for T in maximal),sorted(sum(1<<q for q in T) for T in maximal)


def verify(c,words):
    p=profile(c['rows']);assert p is not None
    for key in ['extension','best','worst','forward']:assert c[key]=={str(T):v for T,v in p[key].items()}
    budget,maximal=metrics(c['rows'],p);assert c['inclusion_budget']==budget and c['inclusion_maximal_images']==maximal
    if words:
        seed_verify(c,True);chain=c['inclusion_best_chain'];S=chain['start'];word=[];Q=(1<<c['n'])-1
        def apply(T,w):
            for x in w:T=sum(1<<q for q in {c['rows'][x][r] for r in range(c['n']) if T>>r&1})
            return T
        assert S in maximal
        for phase in chain['phases']:
            T=phase['larger'];assert phase['start']==S and T.bit_count()>S.bit_count()
            assert apply(T,phase['word'])&S==apply(T,phase['word']) and len(phase['word'])==p['extension'][S]
            assert p['best'][S]==len(phase['word'])+p['best'][T]
            word=phase['word']+word;S=T
        assert S==Q and word==chain['word'] and apply(Q,word)&chain['start']==apply(Q,word)
        assert len(word)==p['best'][chain['start']] and chain['reset_word']==word+[chain['merge_letter']]
        assert len(chain['reset_word'])==chain['budget']==budget and apply(Q,chain['reset_word']).bit_count()==1
    if 'antitone_witness' in c:
        w=c['antitone_witness'];S=w['smaller'];T=w['larger'];assert S!=T and S&T==S
        assert p['best'][S]==w['G_smaller']==5 and p['best'][T]==w['G_larger']==6
    return dict(n=c['n'],P=c['best_policy'],Fmax=budget,images=len(p['best']),words=words)


def main():
    root=Path('scripts/direct_attack/data/seed_inclusion');summary=json.loads((root/'summary.json').read_text());started=time.monotonic()
    cases=[dict(file=name,**verify(json.loads((root/name).read_text()),name in summary['certificates'])) for name in summary['certificates']+summary['records']]
    covers=[]
    for n in [2,3,4,5]:
        counts=Counter()
        for rows in inputs(n,'first-map-orbits',0,0,2):
            counts['tested']+=1;p=profile(rows)
            if p is None:continue
            counts['sc_synchronizing']+=1;budget,_=metrics(rows,p)
            if budget>min(p['best'][1<<q] for q in range(n)):counts['inclusion_failures']+=1
        assert not counts['inclusion_failures'];covers.append(dict(n=n,counts=dict(counts)))
    c=json.loads((root/'inclusion_minimum_n5.json').read_text());rejected=[]
    for field in ['inclusion_maximal_images','inclusion_budget','inclusion_best_chain']:
        d=json.loads(json.dumps(c))
        if field=='inclusion_maximal_images':d[field]=d[field][:-1]
        elif field=='inclusion_budget':d[field]-=1
        else:d[field]['reset_word']=d[field]['reset_word'][:-1]
        try:verify(d,True)
        except AssertionError:rejected.append(field)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,cases=cases,binary_covers=covers,corruptions_rejected=rejected,seconds=time.monotonic()-started,
                scope='Every saved array and all inclusion-maximal seed memberships independently checked. Explicit chains also use independent inverse-set checker. Binary n2..5 covers have no inclusion failure; arbitrary-alphabet state minimum n5 follows from paper exclusion at n<=4.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=cases,binary_covers=covers,corruptions_rejected=rejected,seconds=report['seconds'])),flush=True)


if __name__=='__main__':main()
