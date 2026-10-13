"""Independent original-row controls and complete reverse subset distances."""
import argparse
from collections import deque
import copy
from hashlib import sha256
import json
from pathlib import Path


def digest(value):return sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def rows(p):
    n=3*p;a=list(range(n));b=list(range(n))
    for q in range(1,2*p,2):a[q],a[q+1]=q+1,q
    for q in range(0,2*p,2):b[q],b[q+1]=q+1,q
    a[2*p]=2*p+1;a[2*p+1]=3;b[2*p]=2
    for q in range(2*p+2,n-1,2):a[q],a[q+1]=q+1,q
    for q in range(2*p+1,n-1,2):b[q],b[q+1]=q+1,q
    return [a,b]


def original_apply(rs,w,states):
    current=list(states)
    for a in w:
        for i,q in enumerate(current):current[i]=rs[a][q]
    return current


def subset_reverse(rs):
    n=len(rs[0]);Q=frozenset(range(n));images={Q};todo=[Q];pred={Q:[]};edges=0
    while todo:
        S=todo.pop()
        for f in rs:
            T=frozenset(f[q] for q in S);edges+=1
            if T not in images:images.add(T);todo.append(T);pred[T]=[]
            pred[T].append(S)
    distance={S:0 for S in images if len(S)==1};todo=deque(distance)
    while todo:
        T=todo.popleft()
        for S in pred[T]:
            if S not in distance:distance[S]=distance[T]+1;todo.append(S)
    assert len(distance)==len(images)
    return dict(rt=distance[Q],reachable_images=len(images)),edges


def verify(z):
    p=z['p'];assert p>=3;n=3*p;rs=rows(p);R=[0]+list(range(2,2*p+1,2))+[1];r=len(R);ids={q:i for i,q in enumerate(R)}
    assert z['n']==n and z['rows_sha256']==digest(rs) and z['core_states']==R
    for f in rs:assert len(set(f))==n-1
    c=[rs[0][rs[1][q]] for q in R]
    assert c==R[1:]+R[:1]
    prefix=[1,0]*p+[0,1]*(p-1)+[0]*4+[1,0]*(p-2)
    assert z['preparation_original_length']==len(prefix)==6*p-2
    prepared=sorted({ids[q] for q in original_apply(rs,prefix,range(n))})
    assert prepared==z['prepared_image_positions']==list(range(p-1))+[p,p+1]
    base=original_apply(rs,[0]+[1,0]*p,R);returns=[];current=base
    controls=n*len(prefix)+r*(2*p+1)+2*r
    for j in range(p,2*p-1):
        image=[ids[q] for q in current]
        assert image==[(j-i)%r for i in range(p)]+[(j+1)%r]*2
        returns.append(image)
        current=[rs[0][rs[1][q]] for q in current];controls+=2*r
    assert z['returns_sha256']==digest(returns)
    hword=[0,0,0]+[1,0]*(p-2);reflection=[ids[q] for q in original_apply(rs,hword,R)]
    controls+=r*len(hword)
    assert z['reflection_original_length']==len(hword)==2*p-1
    assert reflection==[(p-2-i)%r for i in range(r)] and z['reflection_sha256']==digest(reflection)
    S=set(prepared);chain=[sorted(S)]
    for t in range(p-2,-1,-1):
        assert S==set(range(t+1))|{p,p+1}
        S={returns[t][i] for i in S};expected=set(range(t))|{p,p+1}
        assert S==expected;chain.append(sorted(S))
    assert digest(chain)==z['shrinking_chain_sha256'] and S=={p,p+1}
    final=original_apply(rs,[0,1]*p,[R[p],R[p+1]]);controls+=4*p
    assert final==[2,2] and z['reset_endpoint']==2
    length=len(prefix)+sum(2*j+1 for j in range(p,2*p-1))+2*p
    assert z['reset_original_length']==length==3*p*p+4*p-1
    assert length<(n-1)**2
    literal=0
    if p<=24:
        w=prefix[:]
        for t in range(p-2,-1,-1):w += [0]+[1,0]*(p+t)
        w += [0,1]*p
        assert z['literal_word']==w and len(w)==length
        assert original_apply(rs,w,range(n))==[2]*n;literal=n*length
    else:assert z['literal_word'] is None
    small=None;edges=0
    if p<=7:
        small,edges=subset_reverse(rs);assert small==z['small_full_subset_scope'] and small['rt']==length
    else:assert z['small_full_subset_scope'] is None
    return dict(p=p,n=n,original_macro_state_letter_controls=controls,literal_reset_state_letter_controls=literal,
                small_full_forward_reverse_scope=small,small_complete_subset_edges=edges)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('scripts/direct_attack/data/compress_other_short_reset.json'))
    ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/compress_other_short_reset_checks.json'));args=ap.parse_args();data=json.loads(args.source.read_text(encoding='utf-8'))
    assert [z['p'] for z in data['records']]==list(range(3,65))+[100,128,256,512,1024]
    reports=[verify(z) for z in data['records']];base=data['records'][0];mutations=[]
    for key,val in [('rows_sha256','0'*64),('prepared_image_positions',[0,1,2,3]),('returns_sha256','0'*64),('reflection_sha256','0'*64),('shrinking_chain_sha256','0'*64),('reflection_original_length',4),('reset_original_length',37),('reset_endpoint',0),('literal_word',[0]*38)]:
        z=copy.deepcopy(base);z[key]=val;mutations.append(z)
    z=copy.deepcopy(base);z['small_full_subset_scope']['rt']=37;mutations.append(z)
    for z in mutations:
        try:verify(z)
        except AssertionError:pass
        else:raise AssertionError('corruption accepted')
    out=dict(verified=True,parameters=len(reports),maximum_n=max(z['n'] for z in reports),
             original_macro_state_letter_controls=sum(z['original_macro_state_letter_controls'] for z in reports),literal_reset_state_letter_controls=sum(z['literal_reset_state_letter_controls'] for z in reports),
             small_forward_reverse_subset_scopes=sum(z['small_full_forward_reverse_scope'] is not None for z in reports),
             small_complete_subset_vertices=sum(z['small_full_forward_reverse_scope']['reachable_images'] for z in reports if z['small_full_forward_reverse_scope']),
             small_complete_subset_edges=sum(z['small_complete_subset_edges'] for z in reports),corruptions_rejected=len(mutations),reports=reports,
             boundary='PROVED paper EVERY p>=3 actual reflection return and reset upper3p^2+4p-1. Finite small ordinary equality only COMPUTATIONALLY VERIFIED; all-p exact rt remains CONJECTURED, priority and general Cerny OPEN, no formal family proof.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='reports'}),flush=True)


if __name__=='__main__':main()
