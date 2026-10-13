"""Independent finite/boundary controls for the uniform common-block proof."""
from pathlib import Path
from itertools import permutations,combinations,product
from collections import deque
import hashlib,json
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def reverse_dist(rows):
    n=len(rows[0]);pairs=list(combinations(range(n),2));back={p:[] for p in pairs};d={};todo=deque()
    for p in pairs:
        for row in rows:
            out=tuple(sorted({row[q] for q in p}))
            if len(out)==1:
                if p not in d:d[p]=1;todo.append(p)
            else:back[out].append(p)
    while todo:
        p=todo.popleft()
        for prev in back[p]:
            if prev not in d:d[prev]=d[p]+1;todo.append(prev)
    return d

def forward_merges(rows,pair):
    todo=deque([frozenset(pair)]);d={frozenset(pair):0}
    while todo:
        p=todo.popleft()
        if len(p)==1:return d[p]
        for row in rows:
            out=frozenset(row[q] for q in p)
            if out not in d:d[out]=d[p]+1;todo.append(out)
    return None

def apply(S,word,rows):
    for c in word:S={rows[ord(c)-97][q] for q in S}
    return S

def main():
    records=[];models=separate=0
    for n in range(3,7):
        for d in range(2,n):
            D=set(range(d));C=n-1;outside=list(range(d,n));targets=list(range(n-1))
            rows=[];raw=0
            for values in permutations(targets,len(outside)):
                raw+=1;row=tuple([C]*d+list(values))
                if sum(row[q] in D for q in range(n))<=1:rows.append(row)
            expected={p:1 for p in combinations(range(d),2)}
            for alpha in (2,3):
                checked=0;controls=0
                for alphabet in product(rows,repeat=alpha):
                    dist=reverse_dist(alphabet);assert dist==expected
                    if checked<64:
                        for pair in combinations(range(n),2):assert forward_merges(alphabet,pair)==dist.get(pair)
                        controls+=1
                    checked+=1
                assert checked==len(rows)**alpha
                records.append(dict(n=n,D_size=d,alphabet_size=alpha,complete_raw_individual_rows=raw,
                    necessary_retained_rows=len(rows),complete_ordered_alphabets=checked,
                    separately_checked_forward_alphabets=controls,only_D_clique_merges=True))
                models+=checked;separate+=controls
    boundary=[dict(rows=[[2,2,3,3]],D=[0,1],c=2,K=[0],omitted='P2 cover',reset='aa'),
        dict(rows=[[0,0,1]],D=[0,1],c=0,K=[0,1],omitted='c outside D',reset='aa'),
        dict(rows=[[2,2,0],[1,2,0]],D=[0,1],c=2,K=[0,1],omitted='all letters have same preimage',reset='aba')]
    for z in boundary:
        rows=z['rows'];D=set(z['D']);K=set(z['K']);n=len(rows[0]);c=z['c'];dist=reverse_dist(rows)
        assert K<=D and len(D)<n and len(apply(set(range(n)),z['reset'],rows))==1
        common=all({q for q in range(n) if row[q]==c}==D for row in rows)
        cover=all(set(p)&K for p,v in dist.items() if v<=2)
        assert ((common,c not in D,cover)==(True,True,False) if z['omitted']=='P2 cover'
            else (common,c not in D,cover)==(True,False,True) if z['omitted']=='c outside D'
            else (common,c not in D,cover)==(False,True,True))
    names=[Path(__file__).name,'PROOF.md#problem4-common-collapsing-block-trap']
    result=dict(status='pass',uniform_proof='PROOF.md#problem4-common-collapsing-block-trap',
        complete_finite_ordered_alphabets=models,separately_checked_forward_alphabets=separate,
        finite_controls=records,essential_hypothesis_boundary_controls=boundary,
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Uniform conditional non-synchronization lemma for arbitrary alphabets; complete finite controls supplement the proof. No global F value or numerical alphabet separation.')
    (ROOT/'common_collapsing_block_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','finite_controls','essential_hypothesis_boundary_controls')}),flush=True)
if __name__=='__main__':main()
