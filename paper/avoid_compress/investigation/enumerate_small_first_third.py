"""Geometric and deterministic typed third admission for the B1/B2 frontier.

This is a necessary-condition inventory, never a full automaton search.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import hashlib, json, math

ROOT=Path(__file__).resolve().parent
Q=set(range(13)); A={3}; H={0,1,2}; O=Q-A

def rank(rows):
    work=[[Fraction(x) for x in row] for row in rows]; r=0
    for j in range(len(work[0])):
        p=next((i for i in range(r,len(work)) if work[i][j]),None)
        if p is None: continue
        work[r],work[p]=work[p],work[r]; v=work[r][j]
        work[r]=[x/v for x in work[r]]
        for i in range(r+1,len(work)):
            v=work[i][j]; work[i]=[x-v*y for x,y in zip(work[i],work[r])]
        r+=1
    return r

def coefficients(rows, values):
    work=[[Fraction(x) for x in row]+[Fraction(v)] for row,v in zip(rows,values)]
    for j in range(4):
        p=next(i for i in range(j,4) if work[i][j]); work[j],work[p]=work[p],work[j]
        v=work[j][j]; work[j]=[x/v for x in work[j]]
        for i in range(4):
            if i==j: continue
            v=work[i][j]; work[i]=[x-v*y for x,y in zip(work[i],work[j])]
    return [work[i][-1] for i in range(4)]

def incomparable(x,y): return not x<=y and not y<=x

def covered():
    return [set(z) for size in range(1,5) for z in combinations(sorted(O),size) if len(set(z)-H)<=1]

def fibers(B,C,D):
    cells={key:{q for q in O if (int(q in B),int(q in C),int(q in D))==key}
           for key in product((0,1),repeat=3)}
    keys=[k for k in cells if cells[k]]; rows=[[1,*k] for k in keys]
    basis=next(z for z in combinations(range(len(rows)),4) if rank([rows[i] for i in z])==4)
    answer=[]
    for values in product((0,1),repeat=4):
        coef=coefficients([rows[i] for i in basis],values)
        out=[sum(c*x for c,x in zip(coef,row)) for row in rows]
        if any(x not in (0,1) for x in out) or coef[0]*8+sum(coef[1:])!=1: continue
        R=set().union(*(cells[k] for k,v in zip(keys,out) if v))
        if not R or len(R-H)>1 or any(R!=x and not incomparable(R,x) for x in (B,C,D)): continue
        answer.append(R)
    return answer

def row_profile(B,C,pa,pb,pc):
    outputs={key:{q for q in Q if (int(q in A),int(q in B),int(q in C))==key}
             for key in product((0,1),repeat=3)}
    inputs={key:{q for q in Q if (int(q in pa),int(q in pb),int(q in pc))==key}
            for key in outputs}
    if any(inputs[k] and not outputs[k] for k in inputs): return None
    # Even if both rows use different output labels, these cells cannot
    # have more incoming targets than the number of inputs supplying them.
    capacity=[min(len(inputs[k]),len(outputs[k])) for k in outputs]
    forced=set()
    for k in inputs:
        if len(outputs[k])==1: forced.update(combinations(sorted(inputs[k]),2))
    if len(forced)>4 or any(not set(pair)&H for pair in forced): return None
    return dict(preA=sorted(pa),preB=sorted(pb),preC=sorted(pc),
                cell_capacity=capacity,forced_pairs=[list(z) for z in sorted(forced)])

def typed(B,C,D,allowed):
    rows=[]
    for pa,pb,pc in product((A,B),(A,B,C),[A]+allowed):
        row=row_profile(B,C,pa,pb,pc)
        if row is not None: rows.append(row)
    keys=list(product((0,1),repeat=3))
    output_sizes=[sum((int(q in A),int(q in B),int(q in C))==k for q in Q) for k in keys]
    pairs=[]
    for x,y in combinations_with_replacement(range(len(rows)),2):
        pair=[rows[x],rows[y]]
        if not any(set(v['preA'])==B for v in pair): continue
        if not any(set(v['preB'])==C for v in pair): continue
        if not any(set(v['preC'])==D for v in pair): continue
        if any(pair[0]['cell_capacity'][j]+pair[1]['cell_capacity'][j]<v for j,v in enumerate(output_sizes)): continue
        forced={tuple(z) for v in pair for z in v['forced_pairs']}
        if len(forced)>4: continue
        # The already proved crossing lemma is valid for any overlapping B,C.
        if B&C and any(set(v['preA'])==A and set(v['preC'])==B for v in pair): continue
        pairs.append([x,y])
    return rows,pairs

def main():
    joint=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))
    allD=covered(); allS=[A|set(z) for z in combinations(sorted(O),8)]
    records=[]; summaries={}
    for entry in joint['records']:
        B=set(entry['B']); C=set(entry['C'])
        if len(B)>2: continue
        witnesses=[S for S in allS if len(S&B)==len(S&C)==1]
        cells=[{q for q in O if (int(q in H),int(q in B),int(q in C))==key}
               for key in product((0,1),repeat=3)]
        candidates={}
        for D in allD:
            if len(B|C|D)>6 or not incomparable(D,B) or not incomparable(D,C): continue
            feasible=[S for S in witnesses if len(S&D)==1]
            if not feasible or rank([[1,int(q in B),int(q in C),int(q in D)] for q in sorted(O)])!=4: continue
            signature=tuple(len(D&cell) for cell in cells)
            if signature in candidates: candidates[signature]['labelled_D']+=1; continue
            canonical=set().union(*(set(sorted(cell)[:v]) for cell,v in zip(cells,signature)))
            assert canonical==D
            allowed=fibers(B,C,D); rows,pairs=typed(B,C,D,allowed)
            candidates[signature]=dict(joint_id=entry['id'],B=sorted(B),C=sorted(C),D=sorted(D),
                cell_signature=list(signature),labelled_D=1,
                orbit_size=math.prod(math.comb(len(cell),v) for cell,v in zip(cells,signature)),
                feasible_nine_sets=len(feasible),allowed_preC_fibers=[sorted(R) for R in allowed],
                rows=rows,binary_profile_pairs=pairs)
        for j,z in enumerate(candidates.values(),1):
            assert z['labelled_D']==z['orbit_size'];z['id']=entry['id']+'_third'+str(j);records.append(z)
        summaries[entry['id']]=dict(geometric=len(candidates),labelled=sum(z['labelled_D'] for z in candidates.values()),
            binary_typed=sum(bool(z['binary_profile_pairs']) for z in candidates.values()),
            binary_pairs=sum(len(z['binary_profile_pairs']) for z in candidates.values()))
    result=dict(status='necessary_inventory',parameter=[13,9,1],joint_cases=len(summaries),
        counts=summaries,records=records,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
          [Path(__file__).name,'joint_fiber_orbits.json','THIRD_ENTRANCE_SPACE.md','SECOND_ENTRANCE_FIBER.md',
           'ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md','BINARY_THIRD_ENTRANCE_CROSSING.md']},
        scope='Necessary B1/B2 third-preimage inventory, retaining all same-level Boolean fibers. No full transition search or new extremal value. Independently checked by check_small_first_third.py.')
    (ROOT/'small_first_third_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(joint_cases=len(summaries),geometric=sum(z['geometric'] for z in summaries.values()),
        binary_typed=sum(z['binary_typed'] for z in summaries.values()),
        binary_pairs=sum(z['binary_pairs'] for z in summaries.values()),
        joint_no_binary_profiles=[k for k,v in summaries.items() if not v['binary_typed']],counts=summaries)))

if __name__=='__main__':main()
