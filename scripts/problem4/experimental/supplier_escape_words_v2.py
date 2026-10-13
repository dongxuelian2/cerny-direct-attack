"""Conservative compulsory-group/SC-escape products with literal word proofs."""
from collections import deque
from itertools import combinations,product
from math import prod
def unsafe_word(rows,chosen,S,horizon,size,protected):
    seen={S:()};todo=deque([S])
    while todo:
        m=todo.popleft();word=seen[m]
        if len(word)==horizon:continue
        for i in chosen:
            y=0
            for q in range(len(rows[i])):
                if m>>q&1:y|=1<<rows[i][q]
            if y.bit_count()<size or y&protected!=protected:return list(word+(i,))
            if y not in seen:seen[y]=word+(i,);todo.append(y)
    return None

def certificate(rows,active,required,S,horizon,size,protected,max_active=256,max_products=4096):
    if active.bit_count()>max_active:return None
    domains=[g&active for g in required]
    if not domains or any(not g for g in domains):return None
    forced=sorted({g.bit_length()-1 for g in domains if g.bit_count()==1})
    ids=[i for i in range(len(rows)) if active>>i&1];n=len(rows[0]);cache={}
    forced_mask=sum(1<<i for i in forced)
    def complete_product(lists):
        if prod(map(len,lists))>max_products:return None
        cases=[]
        for choices in product(*lists):
            chosen=tuple(sorted(set(forced)|set(choices)))
            if chosen not in cache:cache[chosen]=unsafe_word(rows,chosen,S,horizon,size,protected)
            word=cache[chosen]
            if word is None:return None
            cases.append(dict(choices=list(choices),word=word))
        return cases
    for degree in (2,3):
        for groups in combinations(range(len(domains)),degree):
            masks=[domains[j] for j in groups]
            if any(m&forced_mask for m in masks) or any(a&b for a,b in combinations(masks,2)):continue
            lists=[[i for i in ids if m>>i&1] for m in masks];cases=complete_product(lists)
            if cases is not None:return dict(kind='suppliers',forced=forced,groups=list(groups),cases=cases)
    for q in range(n):
        if any(rows[i][q]!=q for i in forced):continue
        escape=[i for i in ids if rows[i][q]!=q]
        if not escape:continue
        escape_mask=sum(1<<i for i in escape)
        for j,g in enumerate(domains):
            if g&escape_mask:continue
            supply=[i for i in ids if g>>i&1];cases=complete_product([supply,escape])
            if cases is not None:return dict(kind='SC_escape',state=q,forced=forced,supplier_group=j,cases=cases)
    return None
