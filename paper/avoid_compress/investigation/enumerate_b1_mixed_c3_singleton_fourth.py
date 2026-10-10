"""Complete kernel admission on the 41 singleton fourth-field pairs."""
from itertools import combinations, product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
H={0,1,2}; A={3}; B={4}; C={0,1,5}; D={2,6}; E={7}

def partitions(X):
    if not X:yield [];return
    q=min(X)
    for old in partitions(X-{q}):
        yield [frozenset({q}),*old]
        if q in {3,4}:continue
        for i,block in enumerate(old):
            if block&{3,4} or len((set(block)|{q})-H)>1:continue
            yield [*old[:i],block|{q},*old[i+1:]]

def kernel(blocks):return {tuple(z) for b in blocks for z in combinations(sorted(b),2)}

def row_patterns(n,word):
    Q=set(range(n));J=set(range(7,n));sets=dict(A=A,B=B,C=C,D=D,E=E)
    inputs=[sets[k] for k in word];inputs.append(Q-set().union(*inputs))
    sizes=[1,1,3,2,len(J)];choices=[]
    for X,cap in zip(inputs,sizes):
        choices.append([p for p in partitions(X) if len(p)<=cap and len(kernel(p))<=4])
    result=[]
    for fields in product(*choices):
        K=set().union(*(kernel(p) for p in fields))
        if len(K)>4:continue
        blocks=[sorted(b) for field in fields for b in field]
        result.append(dict(fields=[[sorted(b) for b in p] for p in fields],kernel=[list(p) for p in sorted(K)]))
    return result

def inventory(n=13):
    old=json.loads((ROOT/'b1_mixed_c3_fourth_inventory.json').read_text(encoding='utf-8'))['records'][0]
    assert old['E']==[7] and len(old['binary_fourth_profile_pairs'])==41
    rows=[]
    for row in old['rows']:
        rows.append(dict(base_row=row['base_row'],word=row['preimage_word'],patterns=row_patterns(n,row['preimage_word'])))
    pairs=[]
    for x,y in old['binary_fourth_profile_pairs']:
        xy=[]
        for i,j in product(range(len(rows[x]['patterns'])),range(len(rows[y]['patterns']))):
            left,right=rows[x]['patterns'][i],rows[y]['patterns'][j]
            K={tuple(p) for p in left['kernel']+right['kernel']}
            if len(K)>4:continue
            if any(len(left['fields'][k])+len(right['fields'][k])<cap for k,cap in enumerate([1,1,3,2,n-7])):continue
            xy.append([i,j])
        pairs.append(dict(rows=[x,y],kernel_pairs=xy))
    return dict(status='necessary_kernel_inventory',n=n,parameter=[13,9,1],rows=rows,pairs=pairs,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
            [Path(__file__).name,'b1_mixed_c3_fourth_inventory.json']},
        scope='Complete immediate-kernel admission with necessary target capacities. No transition-table enumeration or F value.')

if __name__=='__main__':
    result=inventory();(ROOT/'b1_mixed_c3_singleton_fourth_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],fourth_pairs=len(result['pairs']),row_kernel_patterns=sum(len(v['patterns']) for v in result['rows']),
        compatible_kernel_pairs=sum(len(v['kernel_pairs']) for v in result['pairs']))))
