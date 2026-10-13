"""Exact designated covers of permutation/unit alphabets; no random stopping."""
from itertools import combinations, permutations
import hashlib
import json
from pathlib import Path
from direct_attack.native_sparse_policy import profile
from direct_attack.native_policy import profile as dense

ROOT=Path('scripts/direct_attack/data/permutation_units')

def partitions(n,least=1):
    if n==0:yield []
    for k in range(least,n+1):
        for rest in partitions(n-k,k):yield [k]+rest

def representative(parts):
    row=[];offset=0
    for k in parts:
        row+=list(range(offset+1,offset+k))+[offset];offset+=k
    return row

def units(n):
    result=[]
    for s in range(n):
        for t in range(n):
            if s!=t:
                row=list(range(n));row[s]=t;result.append(row)
    return result

def selections(items,complete):
    if complete:
        for bits in range(1,1<<len(items)):
            yield [v for i,v in enumerate(items) if bits>>i&1]
    else:
        for size in [1,2,3]:
            for choice in combinations(items,size):yield list(choice)

def inputs(kind,n):
    U=units(n)
    if kind=='single':
        for part in partitions(n):
            for choice in selections(U,n<=4):yield [representative(part)]+choice
    else:
        P=list(map(list,permutations(range(n))))
        for choices in selections(P,True):
            for choice in selections(U,True):yield choices+choice

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def main():
    ROOT.mkdir(exist_ok=True);summaries=[];samples=[]
    for kind,ns in [('single',range(2,7)),('arbitrary',range(2,4))]:
        for n in ns:
            tested=accepted=0;digest=hashlib.sha256();maxe=maxp=maxloss=0;chosen={}
            for rows in inputs(kind,n):
                tested+=1;p=profile(rows,True);d=dense(rows,True)
                assert (p is None)==(d is None)
                if p is None:
                    digest.update(canonical([rows,None]));continue
                accepted+=1
                for key in ['extension','best','worst']:assert p[key]==d[key]
                for key in ['rt','best_policy','worst_policy','reachable']:assert p[key]==d[key]
                assert p['reachable']==(1<<n)-1
                if kind=='single':assert p['best']==p['worst']==p['forward'],(rows,p)
                else:assert p['best_policy']==p['rt']
                # Each complete array enters the order-sensitive digest, not just its scalar.
                digest.update(canonical([rows,p]))
                scores=dict(e=p['max_extension'],P=p['best_policy'],loss=p['worst_policy']-p['best_policy'])
                for key,score in scores.items():
                    if key not in chosen or score>chosen[key][0]:chosen[key]=(score,p)
                if accepted%127==1:chosen['sample'+str(accepted)]=(0,p)
                maxe=max(maxe,scores['e']);maxp=max(maxp,scores['P']);maxloss=max(maxloss,scores['loss'])
            sample_indices=[]
            for _,p in chosen.values():
                sample_indices.append(len(samples));samples.append(p)
            r=dict(kind=kind,n=n,tested=tested,accepted=accepted,rejected=tested-accepted,
                   sha256=digest.hexdigest(),max_e=maxe,max_P=maxp,max_endpoint_worst_gap=maxloss,samples=sample_indices,
                   scope='All nonempty unit-letter subsets, all permutation cycle types' if kind=='single' and n<=4 else
                   'All permutation cycle types; unit-letter subsets of sizes 1,2,3' if kind=='single' else
                   'All nonempty subsets of distinct permutations times all nonempty subsets of distinct units',
                   per_input_two_native_kernels=True)
            summaries.append(r);print(json.dumps({k:v for k,v in r.items() if k!='samples'}),flush=True)
    counter=profile([[0,1,3,2],[1,2,0,3],[2,1,2,3]],True)
    assert counter['rt']==6 and counter['best_policy']==7
    (ROOT/'counterexample.json').write_text(json.dumps(counter,indent=2)+'\n',encoding='utf-8')
    (ROOT/'samples.json').write_text(json.dumps(samples,indent=2)+'\n',encoding='utf-8')
    (ROOT/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
