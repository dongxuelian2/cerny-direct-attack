"""Positive and adversarial controls for literal forced-word inference."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,hashlib
from check_c1_word_staircase import replay_words
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(domain):return hashlib.sha256(bytes([domain])).hexdigest()
def main():
    identity=list(range(13));g=identity.copy();g[0]=1;h=identity.copy();h[2]=1;rows=[(tuple(r),0) for r in [identity,g,h]];S=sum(1<<q for q in range(9));required=[1,6]
    record=dict(before_size=3,before_sha256=digest(7),singleton_premises=[[0,0]],deletions=[dict(letter=1,word=[1]),dict(letter=2,word=[2])],after_size=1,after_sha256=digest(1))
    stats=Counter();active,bad=replay_words(rows,S,7,required,[record],stats);assert active==1 and not bad and not(active&required[1]) and dict(stats)==dict(word_rounds=1,word_deletions=2)
    forced=dict(before_size=2,before_sha256=digest(3),singleton_premises=[[0,0],[1,1]],deletions=[],forced_bad_word=[1],after_size=2,after_sha256=digest(3))
    stats=Counter();active,bad=replay_words(rows,S,3,[1,2],[forced],stats);assert active==3 and bad and dict(stats)==dict(word_rounds=1)
    variants=[]
    x=deepcopy(record);x['singleton_premises']=[[0,1]];variants.append(x)
    x=deepcopy(record);x['deletions'][0]['word']=[];variants.append(x)
    x=deepcopy(record);x['deletions'][0]['word']=[1]*12;variants.append(x)
    x=deepcopy(record);x['deletions'][0]['word']=[0];variants.append(x)
    x=deepcopy(record);x['deletions'][0]['word']=[99];variants.append(x)
    x=deepcopy(record);x['deletions'][0]['letter']=0;variants.append(x)
    x=deepcopy(record);x['after_sha256']=digest(7);variants.append(x)
    for i,variant in enumerate(variants):
        try:replay_words(rows,S,7,required,[variant],Counter())
        except AssertionError:pass
        else:raise AssertionError('invalid proof accepted: '+str(i))
    result=dict(status='pass',positive_controls=2,adversarial_controls_rejected=len(variants),source_sha256={n:sha(ROOT/n) for n in [Path(__file__).name,'check_c1_word_staircase.py','PROOF.md#problem4-c1-word-staircase-exclusion']},scope='Literal singleton-domain inference, bad-word set composition and invalid-proof rejection controls. No geometry or F value follows from these controls alone.')
    (ROOT/'c1_word_controls_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
