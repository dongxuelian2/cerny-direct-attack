from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'investigation'))
"""Independent literal pair filtering, Fraction spans and certificate replay.

Does not import the generator or its column-premise routine.
"""
from check_supplier_image_propagation import replay_images
from check_obligatory_supplier_split import check_certificate as check_split
from check_supplier_escape_words import check_certificate as check_product
from collections import Counter
from hashlib import sha256
from itertools import combinations
from check_b3_staircase import rat_rref,rat_contains
from check_c1_word_staircase import replay_words


def verify_column_step(rows,basis,G,active,record):
    n=len(rows)
    def digest(domain):return sha256(domain.to_bytes((n+7)//8,'little')).hexdigest()
    columns=[tuple(bool(row&(1<<q)) for row in basis) for q in range(13)]
    zeros=[q for q in range(13) if not any(columns[q])]
    ones=[q for q in range(13) if all(columns[q])]
    grouped={}
    for q,column in enumerate(columns):grouped.setdefault(column,[]).append(q)
    # Generator orders classes by little-endian column bitmask; reproduce
    # the order from literal tuples, not by importing its routine.
    equal=[grouped[c] for c in sorted(grouped,key=lambda x:sum(int(v)*2**i for i,v in enumerate(x))) if len(grouped[c])>1]
    assert record['zero']==zeros and record['one']==ones and record['equal']==equal
    assert record['before_size']==active.bit_count() and record['before_sha256']==digest(active)
    removed=[]
    if not zeros:
        for i,(row,flags) in enumerate(rows):
            if not(active>>i&1):continue
            invalid=False
            for p,q in combinations(range(13),2):
                if columns[p]!=columns[q] and p not in ones and q not in ones:continue
                image=tuple(sorted((row[p],row[q])))
                if image[0]==image[1] or image in G:
                    invalid=True;break
            if invalid:removed.append(i)
    assert record['deleted']==removed
    for i in removed:active &= ~(1<<i)
    assert record['after_size']==active.bit_count() and record['after_sha256']==digest(active)
    return active


def check_tree(rows,basis0,B,C,D,G,saved):
    n=len(rows);literals=[r for r,f in rows];stats=Counter();images={};spans={};G=set(map(tuple,G))
    masks=[sum(1<<q for q in S) for S in combinations(range(13),9) if 3 in S]
    def digest(domain):return sha256(domain.to_bytes((n+7)//8,'little')).hexdigest()
    def mapping(m):
        if m not in images:
            source={q for q in range(13) if m>>q&1};answer={}
            for i,(row,flags) in enumerate(rows):
                successor={row[q] for q in source}
                if len(successor)==9 and 3 in successor:
                    mask=sum(1<<q for q in successor);answer[mask]=answer.get(mask,0)|(1<<i)
            images[m]=answer
        return images[m]
    def span(basis):
        key=rat_rref(basis);assert len(key)==len(basis)
        if key not in spans:spans[key]={m for m in masks if rat_contains(key,m)}
        return spans[key]
    def safe(m,depth):
        S={q for q in range(13) if m>>q&1}
        return (depth>10 or len(S&B)==1) and (depth>9 or len(S&C)==1) and (depth>8 or len(S&D)==1) and (depth>8 or not any(set(e)<=S for e in G))
    def visit(basis,active,required,node):
        k=len(basis)-1;assert k<=11;current=span(basis)
        stats['nodes']+=1;stats['depth_'+str(k)]+=1
        valid={m:g&active for m,g in (mapping(basis[-1]).items() if k<11 else []) if g&active and safe(m,k+1)}
        if k<11:
            permitted=0
            for g in valid.values():permitted|=g
            active &= permitted
        active,image_known=replay_images(literals,active,required,{m:i for i,m in enumerate(basis)},11,9,1<<3,node['image_propagation'])
        assert node['forced_image_depths']==[[m,d] for m,d in sorted(image_known.items())]
        stats['image_propagation_calls']+=1;stats['image_propagation_steps']+=len(node['image_propagation'])
        for record in node['image_propagation']:
            if record['kind']=='delete':stats['image_deletions']+=int(record['removed_hex'],16).bit_count()
            else:stats['image_forcings']+=1
        # Zero counts remain present, as in the generator.
        stats['image_deletions']+=0;stats['image_forcings']+=0
        valid={m:g&active for m,g in valid.items() if g&active}
        if k>=4:
            assert node['column_pruning'] is not None
            active=verify_column_step(rows,basis,G,active,node['column_pruning'])
            stats['column_nodes']+=1;stats['column_deletions']+=len(node['column_pruning']['deleted'])
            valid={m:g&active for m,g in valid.items() if g&active}
        else:assert node['column_pruning'] is None
        if node['word_propagation']:assert k>=3 and active.bit_count()<=10000
        active,forced_bad=replay_words(rows,basis0[0],active,required,node['word_propagation'],stats)
        valid={m:g&active for m,g in valid.items() if g&active}
        assert node['basis']==basis and node['depth']==k and node['domain_size']==active.bit_count()
        assert node['domain_sha256']==digest(active)
        sizes=[(g&active).bit_count() for g in required];assert node['required_group_sizes']==sizes
        product_proof=node['product_words'];stats['product_cuts']+=int(product_proof is not None)
        stats['product_words']+=len(product_proof['cases']) if product_proof else 0
        if product_proof is not None:
            assert not forced_bad and not(node['column_pruning'] and node['column_pruning']['zero'])
            assert node['reason']=='obligatory_word_products'
            assert check_product(literals,active,required,basis0[0],11,9,1<<3,product_proof)==len(product_proof['cases'])
            stats['obligatory_word_products']+=1;return
        col=node['column_pruning']
        if col and col['zero']:
            assert not node['word_propagation'] and node['reason']=='zero_prefix_column' and node['zero_state']==col['zero'][0]
            stats['zero_prefix_column']+=1;return
        if forced_bad:
            assert node['reason']=='forced_short_word';stats['forced_short_word']+=1;return
        missing=next((i for i,size in enumerate(sizes) if not size),None)
        if missing is not None:
            assert node['reason']=='missing_required_group' and node['missing_group']==missing
            stats['missing_required_group']+=1;return
        adjacency=[set() for _ in range(13)]
        for i,(row,flags) in enumerate(rows):
            if active>>i&1:
                for p,q in enumerate(row):adjacency[p].add(q)
        if node['reason']=='maximal_graph_not_SC':
            R=set(node['closed_set']);assert R and len(R)<13 and all(adjacency[p]<=R for p in R)
            stats['maximal_graph_not_SC']+=1;return
        for initial in range(13):
            reached={initial};work=[initial]
            for p in work:
                for q in adjacency[p]-reached:reached.add(q);work.append(q)
            assert len(reached)==13
        if node['reason']=='obligatory_supplier_split':
            assert k==11
            result=check_split(literals,active,required,basis,11,9,1<<3,node['supplier_split'])
            stats['supplier_split_cuts']+=1
            stats['supplier_split_branches']+=result['branches']
            stats['supplier_split_words']+=result['words'];return
        assert k<11,'Surviving depth11 flag cannot be rejected'
        choices=sorted(m for m in valid if m not in current)
        if not choices:assert node['reason']=='no_growth';stats['no_growth']+=1;return
        assert node['reason']=='all_children_rejected' and [z['next_image'] for z in node['children']]==choices
        for m,child in zip(choices,node['children']):
            allowed=span(basis+[m]);following=0
            for out,g in valid.items():
                if out in allowed:following|=g
            visit(basis+[m],active&following,required+[valid[m]],child['node'])
        stats['internal_nodes']+=1
    required=[sum(1<<i for i,(row,flags) in enumerate(rows) if flags>>j&1) for j in range(4)]
    visit(list(basis0),(1<<n)-1,required,saved)
    return dict(stats)
