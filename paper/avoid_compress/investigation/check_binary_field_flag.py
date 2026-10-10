"""Independent F2 prefix-basis controls for every applicable frontier witness."""
from itertools import combinations
import hashlib
import json
from pathlib import Path
from check_local_equality_flag import image
from check_short_pair_span import exact_rank

ROOT=Path(__file__).resolve().parent


def coordinates(mask,basis):
    pivots={}
    for i,source in enumerate(basis):
        current,coeff=source,1<<i
        while current:
            pivot=current.bit_length()-1
            if pivot not in pivots:
                pivots[pivot]=(current,coeff)
                break
            row,c=pivots[pivot]
            current ^= row;coeff ^= c
    current,coeff=mask,0
    while current:
        pivot=current.bit_length()-1
        if pivot not in pivots:
            return None
        row,c=pivots[pivot]
        current ^= row;coeff ^= c
    return coeff


def audit(z):
    n,s,r,t=z['n'],z['s'],z['r'],z['value']
    assert s%2==1 and t==n-r
    rows=z['rows'];initial=sum(1<<q for q in z['S'])
    basis=[initial];word=''
    for depth in range(1,t):
        for ell,row in enumerate(rows):
            mask=image(basis[-1],row)
            if coordinates(mask,basis) is None:
                basis.append(mask);word+='abcdefghijklmnopqrstuvwxyz'[ell]
                break
        else:
            raise AssertionError((z,depth,'prefix plateau'))
        assert basis[-1].bit_count()==s
        assert all(basis[-1]&(1<<q) for q in z['A'])
    assert len(basis)==t
    common=(1<<n)-1
    for mask in basis:common &= mask
    assert common.bit_count()>=r and all(common&(1<<q) for q in z['A'])
    relations=[]
    for i in range(t-1):
        assert exact_rank([[(mask>>q)&1 for q in range(n)] for mask in basis[:i+2]],n)==i+2
        for ell,row in enumerate(rows):
            target=image(basis[i],row)
            coeff=coordinates(target,basis[:i+2])
            assert coeff is not None
            reconstructed=0
            for j,mask in enumerate(basis[:i+2]):
                if coeff&(1<<j):reconstructed ^= mask
            assert reconstructed==target and target.bit_count()==s
            relations.append(dict(i=i,letter=ell,coefficient_mask=coeff))
    return dict(n=n,s=s,r=r,target=t,prefix_word=word,basis_masks=basis,
                common_protected=[q for q in range(n) if common&(1<<q)],relations=relations)


def main():
    frontier=json.loads((ROOT/'frontier_certificates.json').read_text(encoding='utf-8'))['certificates']
    applicable=[z for z in frontier if z['s']%2==1 and z['value']==z['n']-z['r']]
    records=[audit(z) for z in applicable]
    control=json.loads((ROOT/'potential_full_flag_control_n13.json').read_text(encoding='utf-8'))['witness']
    assert control is not None
    records.append(audit(control))
    # The parity requirement is essential to the argument: even-size rows
    # reset to zero in F2. The checker does not apply it to those witnesses.
    assert all(z['s']%2==1 for z in records)
    result=dict(status='all_independent_controls_passed',frontier_controls=len(applicable),
                additional_fixed_control=1,records=records,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='Independent prefix-word and complete XOR-relation checks; no new maximum.')
    (ROOT/'binary_field_flag_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],frontier_controls=len(applicable),additional_fixed_control=1)))


if __name__=='__main__':
    main()
