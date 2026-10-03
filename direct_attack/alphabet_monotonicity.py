"""Attack global image-policy monotonicity under alphabet/word-shortcut additions."""
import argparse
from collections import deque
from itertools import product
import json
from pathlib import Path
import time
from direct_attack.mine import inputs
from direct_attack.native_policy import profile as fast
from direct_attack.image_extension_policy import profile as certificate


def monoid_words(rows):
    identity=tuple(range(len(rows[0])));words={identity:[]};queue=deque([identity])
    while queue:
        transformation=queue.popleft()
        for a,row in enumerate(rows):
            following=tuple(row[q] for q in transformation)
            if following not in words:
                words[following]=words[transformation]+[a];queue.append(following)
    return words


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--kind',choices=['arbitrary','semigroup'],required=True);ap.add_argument('--out',required=True)
    args=ap.parse_args();assert 2<=args.n<=4
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);started=time.monotonic()
    counts=dict(binary_inputs=0,synchronizing_sc_bases=0,augmentation_tests=0)
    witness=None
    for rows in inputs(args.n,'first-map-orbits',0,0,2):
        counts['binary_inputs']+=1;base=fast(rows)
        if base is None:continue
        counts['synchronizing_sc_bases']+=1
        words=monoid_words(rows) if args.kind=='semigroup' else None
        extras=words.items() if words is not None else ((extra,None) for extra in product(range(args.n),repeat=args.n))
        for extra,word in extras:
            augmented_rows=[list(row) for row in rows]+[list(extra)]
            augmented=fast(augmented_rows);assert augmented is not None
            counts['augmentation_tests']+=1
            if augmented['best_policy']<=base['best_policy']:continue
            base_rows=[list(row) for row in rows]
            for name,case in [('base',base_rows),('augmented',augmented_rows)]:
                c=certificate(case);reference=base if name=='base' else augmented
                assert c['best_policy']==reference['best_policy'] and c['rt']==reference['rt']
                (out/(name+'.json')).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
            witness=dict(n=args.n,kind=args.kind,base_policy=base['best_policy'],augmented_policy=augmented['best_policy'],
                         base_rt=base['rt'],augmented_rt=augmented['rt'],extra_word=word,
                         base_monoid_size=len(words) if words is not None else None)
            break
        if witness is not None:break
    report=dict(arguments=vars(args),counts=counts,first_failure=witness,seconds=time.monotonic()-started,
                scope='Binary first-map cover and all extra maps/generated transformations; n4 stops at first failure. Counts overlap.',
                complete=witness is None)
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
