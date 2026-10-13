from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
"""Equality-flag engine with proved full-prefix column restrictions.

No depth-12 safety is used. Surviving depth-11 flags abort as candidates.
All indices in column deletions refer to the unfiltered sorted letter pool.
"""
from supplier_image_propagation import propagate_images
from obligatory_supplier_split import certificate as split_certificate
from supplier_escape_words_v3 import certificate as product_certificate
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from enumerate_b3_staircase import rref, contains
from enumerate_b3_staircase_first import closure
from enumerate_c1_word_staircase import propagate_words


def column_premises(basis):
    columns=[sum(((row>>q)&1)<<i for i,row in enumerate(basis)) for q in range(13)]
    groups={}
    for q,c in enumerate(columns): groups.setdefault(c,[]).append(q)
    return dict(zero=groups.get(0,[]), one=groups.get((1<<len(basis))-1,[]),
                equal=[v for c,v in sorted(groups.items()) if len(v)>1])


def tree(rows,basis0,B,C,D,G):
    n=len(rows);literals=[r for r,f in rows];stats=Counter();inputs={};spans={};pair_masks={}
    masks9=[sum(1<<q for q in S) for S in combinations(range(13),9) if 3 in S]
    sets={m:{q for q in range(13) if m>>q&1} for m in masks9}
    groups=[sum(1<<i for i,(r,f) in enumerate(rows) if f>>j&1) for j in range(4)]
    arrows=[[sum(1<<i for i,(r,f) in enumerate(rows) if r[p]==q) for q in range(13)] for p in range(13)]
    G=set(map(tuple,G))

    def digest(domain): return sha256(domain.to_bytes((n+7)//8,'little')).hexdigest()

    def images(m):
        if m not in inputs:
            source=[q for q in range(13) if m>>q&1];answer={}
            for i,row in enumerate(literals):
                output=sum(1<<q for q in {row[p] for p in source})
                if output.bit_count()==9 and output>>3&1: answer[output]=answer.get(output,0)|(1<<i)
            inputs[m]=answer
        return inputs[m]

    def span(basis):
        key=rref(basis)
        if key not in spans: spans[key]=frozenset(m for m in masks9 if contains(key,m))
        return key,spans[key]

    def safe(m,depth):
        S=sets[m]
        return (depth>10 or len(S&B)==1) and (depth>9 or len(S&C)==1) and (depth>8 or len(S&D)==1) and (depth>8 or not any(set(e)<=S for e in G))

    def column_filter(basis,active):
        premises=column_premises(basis);before=active
        record=dict(**premises,before_size=before.bit_count(),before_sha256=digest(before))
        if not premises['zero']:
            constraints=set()
            for block in premises['equal']: constraints.update(combinations(block,2))
            for j in premises['one']: constraints.update(tuple(sorted((j,q))) for q in range(13) if q!=j)
            for p,q in sorted(constraints):
                if (p,q) not in pair_masks:
                    allowed=0
                    for i,row in enumerate(literals):
                        u,v=sorted((row[p],row[q]))
                        if u!=v and (u,v) not in G: allowed|=1<<i
                    pair_masks[(p,q)]=allowed
                active &= pair_masks[(p,q)]
        removed=before & ~active
        record.update(deleted=[i for i in range(n) if removed>>i&1],
                      after_size=active.bit_count(),after_sha256=digest(active))
        return active,record

    def visit(basis,active,required):
        k=len(basis)-1
        assert k<=11
        rank,current=span(basis);assert len(rank)==len(basis)
        stats['nodes']+=1;stats['depth_'+str(k)]+=1
        mapping=images(basis[-1]) if k<11 else {}
        valid={m:g&active for m,g in mapping.items() if g&active and safe(m,k+1)}
        if k<11:
            safeletters=0
            for g in valid.values():safeletters|=g
            active &= safeletters
        active,image_steps,image_known=propagate_images(images,active,required,{m:i for i,m in enumerate(basis)},11)
        stats['image_propagation_calls']+=1;stats['image_propagation_steps']+=len(image_steps)
        stats['image_deletions']+=sum(int(r['removed_hex'],16).bit_count() for r in image_steps if r['kind']=='delete')
        stats['image_forcings']+=sum(r['kind']=='force' for r in image_steps)
        valid={m:g&active for m,g in valid.items() if g&active}
        col=None
        if k>=4:
            active,col=column_filter(basis,active);stats['column_nodes']+=1
            stats['column_deletions']+=len(col['deleted'])
            valid={m:g&active for m,g in valid.items() if g&active}
        rounds=[];forced_bad=False
        if not(col and col['zero']) and k>=3 and active.bit_count()<=10000:
            active,rounds,forced_bad=propagate_words(literals,basis0[0],active,required,stats)
            valid={m:g&active for m,g in valid.items() if g&active}
        product_proof=None
        if not forced_bad and not(col and col['zero']):
            product_proof=product_certificate(literals,active,required,basis0[0],11,9,1<<3)
        stats['product_cuts']+=int(product_proof is not None)
        stats['product_words']+=len(product_proof['cases']) if product_proof else 0
        node=dict(product_words=product_proof,basis=basis,depth=k,image_propagation=image_steps,forced_image_depths=[[m,d] for m,d in sorted(image_known.items())],column_pruning=col,word_propagation=rounds,
                  domain_size=active.bit_count(),domain_sha256=digest(active),
                  required_group_sizes=[(g&active).bit_count() for g in required])
        if product_proof is not None:
            node.update(reason='obligatory_word_products');stats['obligatory_word_products']+=1;return node
        if col and col['zero']:
            node.update(reason='zero_prefix_column',zero_state=col['zero'][0]);stats['zero_prefix_column']+=1;return node
        if forced_bad:
            node.update(reason='forced_short_word');stats['forced_short_word']+=1;return node
        missing=next((i for i,g in enumerate(required) if not(g&active)),None)
        if missing is not None:
            node.update(reason='missing_required_group',missing_group=missing);stats['missing_required_group']+=1;return node
        adj=[sum(1<<q for q in range(13) if arrows[p][q]&active) for p in range(13)]
        closed=closure(adj)
        if closed is not None:
            node.update(reason='maximal_graph_not_SC',closed_set=[q for q in range(13) if closed>>q&1]);stats['maximal_graph_not_SC']+=1;return node
        split=split_certificate(literals,active,required,basis,11,9,1<<3,max_choices=16) if k==11 else None
        if split is not None:
            node.update(reason="obligatory_supplier_split",supplier_split=split)
            stats["supplier_split_cuts"]+=1
            stats["supplier_split_branches"]+=len(split["branches"])
            stats["supplier_split_words"]+=sum(len(r.get("product",{}).get("cases",[])) for r in split["branches"])
            return node
        # At depth11 test only proved constraints on the existing flag.
        # Never map its last basis row and require safety at depth12.
        assert k<11,'A surviving depth-11 flag is a candidate, not an exclusion'
        choices=sorted((m,g) for m,g in valid.items() if m not in current)
        if not choices:
            node.update(reason='no_growth');stats['no_growth']+=1;return node
        children=[]
        for m,group in choices:
            _,allowed=span(basis+[m]);following=0
            for out,g in valid.items():
                if out in allowed:following|=g
            children.append(dict(next_image=m,node=visit(basis+[m],active&following,required+[group])))
        node.update(reason='all_children_rejected',children=children);stats['internal_nodes']+=1;return node

    result=visit(list(basis0),(1<<n)-1,groups)
    return result,dict(stats)
