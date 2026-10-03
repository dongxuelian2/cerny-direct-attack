"""Constant-seven-letter shortcut family; exact formulas are not inferred."""
import argparse
import json
from pathlib import Path
import time
from direct_attack.native_complete_policy import profile


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--max-n',type=int,default=20)
    ap.add_argument('--out',default='direct_attack/data/shortcut_family');args=ap.parse_args();assert 4<=args.max_n<=22
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);records=[];controls=[]
    for n in range(4,args.max_n+1):
        rows=[[1,0,0]+list(range(2,n-1)),[(q+1)%n for q in range(n)]]
        word=[1,1,0,1,1,1,0];extra=list(range(n))
        for a in word:extra=[rows[a][q] for q in extra]
        started=time.monotonic();base=profile(rows,'singletons');augmented=profile(rows+[extra],'singletons')
        assert base is not None and augmented is not None
        c=dict(n=n,base=base,augmented=augmented,extra_word=word,reset_word=[0]*(n-2)+[1,0],
               seconds=time.monotonic()-started,scope='Exact full-cube native result; arbitrary-parameter exact P formula remains conjectured.')
        assert base['best_policy']==base['rt']==augmented['rt']==n
        if n!=5:assert augmented['best_policy']>=n+1
        (out/f'n{n}.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
        r=dict(n=n,base_policy=n,augmented_policy=augmented['best_policy'],rt=n,seconds=c['seconds'])
        records.append(r);print(json.dumps(r),flush=True)
        if n<=12:
            scaled_word=[1,1,0]+[1]*(n-1)+[0];scaled=list(range(n))
            for a in scaled_word:scaled=[rows[a][q] for q in scaled]
            control=profile(rows+[scaled],'singletons');assert control is not None
            controls.append(dict(n=n,extra_word=scaled_word,profile=control))
    (out/'summary.json').write_text(json.dumps(dict(arguments=vars(args),records=records,scaled_controls=controls),indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
