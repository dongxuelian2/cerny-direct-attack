"""Complete small compulsory-domain splits, each with checked safe-image proofs."""
from supplier_image_propagation import propagate_images
from supplier_escape_words_v3 import certificate as product_certificate

def certificate(rows,active,required,basis,horizon,size,protected,max_active=512,max_choices=4):
    if active.bit_count()>max_active:return None
    groups=[g&active for g in required]
    if not groups or any(not g for g in groups):return None
    options=sorted((g.bit_count(),j,g) for j,g in enumerate(groups) if 2<=g.bit_count()<=max_choices)
    if not options:return None
    _,j,group=options[0];branches=[];cache={}
    def images(m):
        if m not in cache:
            output={}
            for i,row in enumerate(rows):
                y=sum(1<<q for q in {row[p] for p in range(len(row)) if m>>p&1})
                if y.bit_count()==size and y&protected==protected:output[y]=output.get(y,0)|(1<<i)
            cache[m]=output
        return cache[m]
    for a in range(len(rows)):
        if not(group>>a&1):continue
        req=required+[1<<a]
        remaining,steps,known=propagate_images(images,active,req,{m:i for i,m in enumerate(basis)},horizon)
        record=dict(letter=a,image_steps=steps,known=[[m,d] for m,d in sorted(known.items())],remaining_hex=hex(remaining))
        missing=next((i for i,g in enumerate(req) if not(g&remaining)),None)
        if missing is not None:record.update(reason='missing_group',missing_group=missing)
        else:
            proof=product_certificate(rows,remaining,req,basis[0],horizon,size,protected)
            if proof is None:return None
            record.update(reason='word_product',product=proof)
        branches.append(record)
    return dict(group=j,branches=branches)
