"""Literal independent verification of every branch in a compulsory-domain split."""
from check_supplier_image_propagation import replay_images
from check_supplier_escape_words import check_certificate as check_product

def check_certificate(rows,active,required,basis,horizon,size,protected,proof):
    j=proof['group'];assert 0<=j<len(required)
    assert required and all(g&active for g in required)
    choices={i for i in range(len(rows)) if (required[j]&active)>>i&1};assert len(choices)>=2
    seen=set();words=0
    for branch in proof['branches']:
        a=branch['letter'];assert a in choices and a not in seen;seen.add(a)
        req=required+[1<<a]
        remaining,known=replay_images(rows,active,req,{m:i for i,m in enumerate(basis)},horizon,size,protected,branch['image_steps'])
        assert branch['known']==[[m,d] for m,d in sorted(known.items())]
        assert branch['remaining_hex']==hex(remaining)
        if branch['reason']=='missing_group':
            k=branch['missing_group'];assert 0<=k<len(req) and not(req[k]&remaining)
        else:
            assert branch['reason']=='word_product'
            words+=check_product(rows,remaining,req,basis[0],horizon,size,protected,branch['product'])
    assert seen==choices
    return dict(branches=len(seen),words=words)
