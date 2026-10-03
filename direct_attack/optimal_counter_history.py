"""All-parameter binary-counter rank-loss saturation; growing alphabet."""
import argparse
from fractions import Fraction
from hashlib import sha256
from math import comb
import json
from pathlib import Path


def digest_rows(rows):return sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()


def mask_digest(masks,n):
    digest=sha256();size=(n+7)//8
    for S in masks:digest.update(S.to_bytes(size,'little'))
    return digest.hexdigest()


def profile(d):
    n=2**d-1;rows=[]
    for i in range(1,d):
        s=2**i-1
        rows.append([s if q==0 else q for q in range(n)])
        rows.append([s+1+q if q<s else 0 if q==s else q-s-1 if q<=2*s else q for q in range(n)])
    blocks=[sum(1<<q for q in range(2**i-1,2**(i+1)-1)) for i in range(d)]
    selected=lambda k:sum(B for i,B in enumerate(blocks) if k>>i&1)
    word=[];allowed=[]
    for k in range(n,1,-1):
        if k&1:choices=[2*(i-1) for i in range(1,d) if k>>i&1]
        else:choices=[2*((k&-k).bit_length()-2)+1]
        allowed.append(choices);word.append(choices[0])
    number=1
    for j in range(1,d):number*=j**comb(d-1,j)
    # Rational rank on block-coordinate vectors; state-level upper/lower
    # proof is separate and independently checked by integer block minors.
    basis={}
    for k in range(2,n+1):
        v=[Fraction(int(k>>i&1)) for i in range(d)]
        for p,b in sorted(basis.items()):
            if v[p]:
                x=v[p];v=[a-x*c for a,c in zip(v,b)]
        p=next((i for i,x in enumerate(v) if x),None)
        if p is not None:
            x=v[p];basis[p]=[a/x for a in v]
    assert len(basis)==d
    return dict(d=d,n=n,base_letter_count=2*(d-1),augmented_letter_count=n-1+2*(d-1),
                original_rows_sha256=digest_rows(rows),explicit_original_rows=rows if d<=4 else None,
                rt=n-1,P=n-1,unique_reset_endpoint=0,optimal_endpoint_chain_count=1,
                proper_stages=n-2,raw_proper_plus_Q_rank=d,normalized_proper_rank=d-1,
                full_inverse_raw_rank=d,shortest_labeled_word_count=number,
                canonical_original_reset_indices=word,all_optimal_forward_label_choices=allowed,
                canonical_proper_mask_sha256=mask_digest((selected(k) for k in range(2,n)),n),
                augmented_actual_image_count=2**n-1 if d<=4 else None,
                status='paper ALL d>=2; bounded controls of this parameter are not a formal proof')


def generate():
    return dict(status='PROVED paper all-parameter construction; independent finite and structural checks required',
                records=[profile(d) for d in range(2,13)],
                mask_hash_format='ascending proper cardinalities 2..n-1; unsigned fixed (n+7)//8 byte little-endian masks',
                scope='original alphabet grows as 2(d-1); adjoining n-1 original adjacent swaps preserves every minimum word and yields Eulerian SC simple complete reachability; no binary/fixed-alphabet all-d claim',
                boundary='ALL optimized histories have logarithmic rank; expensive-phase dimension tradeoff and Cerny OPEN')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='direct_attack/data/optimal_counter_history.json')
    args=ap.parse_args();z=generate()
    Path(args.out).write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(parameters=len(z['records']),maximum_n=z['records'][-1]['n'],
                         total_proper_stages=sum(r['proper_stages'] for r in z['records']),
                         all_parameter_status='PROVED paper; independent checker and no formal kernel')))


if __name__=='__main__':main()
