"""Literal alphabet transports, native mid-flag control and damaged certificates."""
from collections import deque
from itertools import product,combinations_with_replacement
from hashlib import sha256
from pathlib import Path
import copy,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'investigation';sys.path.insert(0,str(ROOT))
from flag_stabilizer_quotient import quotient
from check_flag_stabilizer_quotient import check_quotient
from c1_word_staircase_letter_generator import pool
from check_c1_word_staircase import literal_pool
from enumerate_b3_staircase import rref,contains
from check_b3_staircase import rat_rref,rat_contains

def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def image(row,mask):return sum(1<<q for q in {row[p] for p in range(len(row)) if mask>>p&1})
def conjugate(row,p):
    new=[None]*len(p)
    for q,t in enumerate(row):new[p[q]]=p[t]
    return new
def apply(S,word,rows):
    S=set(S)
    for a in word:S={rows[a][q] for q in S}
    return S
def closure(rows,start):
    todo=deque([frozenset(start)]);seen={frozenset(start):0}
    while todo:
        S=todo.popleft()
        for row in rows:
            T=frozenset(row[q] for q in S)
            if T not in seen:seen[T]=seen[S]+1;todo.append(T)
    return seen
def strong(rows):
    for q in range(len(rows[0])):
        work=[q];seen={q}
        for p in work:
            for row in rows:
                if row[p] not in seen:seen.add(row[p]);work.append(row[p])
        if len(seen)<len(rows[0]):return False
    return True

def main():
    rows=list(product(range(4),repeat=4));active=(1<<256)-1;required=[active];basis=[3];fixed={0,1};known={3:0};choices=[5,9]
    proof=quotient(rows,active,required,basis,fixed,set(),known,choices)
    assert proof and check_quotient(rows,active,required,basis,fixed,set(),known,choices,proof)==dict(choices=2,representatives=1,omitted=1,generators=1)
    p=proof['generators'][0]['permutation'];assert p==[0,1,3,2]
    words=[w for h in range(4) for w in product(range(2),repeat=h)]
    alphabets=word_checks=qualitative=actual_witnesses=0;separate_failure=None
    for a,b in combinations_with_replacement(range(256),2):
        original=[rows[a],rows[b]];transported=[conjugate(row,p) for row in original];alphabets+=1
        for w in words:
            before=apply({0,1},w,original);after=apply({0,1},w,transported)
            assert after=={p[q] for q in before};word_checks+=1
            assert (len(before)<2 or 0 not in before)==(len(after)<2 or 0 not in after)
        if alphabets%31==0:
            before=closure(original,range(4));after=closure(transported,range(4))
            assert after=={frozenset(p[q] for q in S):d for S,d in before.items()}
            assert strong(original)==strong(transported);qualitative+=1
            if strong(original) and any(len(T)==1 for T in before) and frozenset({0,1}) in before:actual_witnesses+=1
        if separate_failure is None:
            wrong=[conjugate(original[0],p),list(original[1])]
            for w in words:
                if apply({0,1},w,wrong)!={p[q] for q in apply({0,1},w,original)}:
                    separate_failure=dict(rows=[list(row) for row in original],word=list(w));break
    assert alphabets==32896 and word_checks==493440 and actual_witnesses and separate_failure
    rejected=[]
    def reject(label,mutate):
        d=copy.deepcopy(proof);mutate(d)
        try:check_quotient(rows,active,required,basis,fixed,set(),known,choices,d)
        except (AssertionError,KeyError):rejected.append(label);return
        raise AssertionError('Accepted corrupted transport: '+label)
    reject('nonbijective generator',lambda d:d['generators'][0]['permutation'].__setitem__(2,2))
    reject('wrong fixed states',lambda d:d.__setitem__('fixed_states',[0]))
    reject('basis not preserved',lambda d:d['generators'][0].__setitem__('permutation',[2,1,0,3]))
    reject('wrong row transport digest',lambda d:d['generators'][0].__setitem__('active_row_transport_sha256','0'*64))
    reject('missing child',lambda d:d['transports'].pop())
    reject('duplicate child',lambda d:d['transports'].append(d['transports'][0]))
    reject('wrong representative',lambda d:d['transports'][1].__setitem__('representative',9))
    reject('missing transport step',lambda d:d['transports'][1].__setitem__('steps',[]))
    reject('invalid transport generator',lambda d:d['transports'][1].__setitem__('steps',[1]))
    reject('missing representative',lambda d:d.__setitem__('representatives',[]))
    # A true row bijection is insufficient when a required domain is not fixed.
    k=next(i for i,row in enumerate(rows) if tuple(conjugate(row,p))!=row)
    try:check_quotient(rows,active,[1<<k],basis,fixed,set(),known,choices,proof)
    except AssertionError:rejected.append('unpreserved required singleton')
    else:raise AssertionError('Ignored an obligatory-domain premise')
    try:check_quotient(rows,active,required,basis,fixed,{(0,2)},known,choices,proof)
    except AssertionError:rejected.append('unpreserved premise graph')
    else:raise AssertionError('Ignored a premise graph')
    scope_name='b2_mixed_c4_third2_graph_quotient_scope.json';parent_name='b2_mixed_c4_third2_inverse_probe.json'
    parent=read(HERE/parent_name);prefix=read(HERE/scope_name)['prefixes'][844]
    old=next(c for c in parent['records'] if c['P1_mask']==prefix['P1_mask'] and c['reason']=='retained_overapproximation')
    B,C,D=map(set,[parent[k] for k in ('B','C','D')]);S,T=[{q for q in range(13) if m>>q&1} for m in prefix['basis']]
    args=dict(mandatory=parent['mandatory'],required_P3_edges=old['G'],fields=parent['fields']);view=dict(extra_pair=None,field_kernel_masks=old['field_kernel_masks'])
    labelled,G=pool(args,view,S,T,B,C,D);literal,H=literal_pool(args,view,prefix['basis'],B,C,D);assert literal==labelled and G==H
    native_rows=[r for r,f in literal];native_basis=read(HERE/'b2_mixed_candidate844_literal_pool_20261012.json')['candidate']['basis'][:4]
    spans=[rref(native_basis[:i+2]) for i in range(3)];rational=[rat_rref(native_basis[:i+2]) for i in range(3)]
    cached={}
    def good(m):
        X={q for q in range(13) if m>>q&1}
        return len(X)==9 and 3 in X and all(len(X&Y)==1 for Y in (B,C,D)) and not any(set(e)<=X for e in G)
    def allowed(i,m):
        key=(i,m)
        if key not in cached:
            ans=contains(spans[i],m);assert ans==rat_contains(rational[i],m);cached[key]=ans
        return cached[key]
    native_active=0
    for j,row in enumerate(native_rows):
        if all(good(image(row,m)) and (i==3 or allowed(i,image(row,m))) for i,m in enumerate(native_basis)):native_active|=1<<j
    R=[sum(1<<i for i,(r,f) in enumerate(literal) if f>>j&1) for j in range(4)]
    for i in (1,2):R.append(sum(1<<j for j,row in enumerate(native_rows) if image(row,native_basis[i])==native_basis[i+1]))
    current=rref(native_basis);Cnext=sorted({image(row,native_basis[-1]) for j,row in enumerate(native_rows) if native_active>>j&1 and not contains(current,image(row,native_basis[-1]))})
    pins=set(range(7))|B|C|D|{q for e in G for q in e};K={m:i for i,m in enumerate(native_basis)}
    native_proof=quotient(native_rows,native_active,R,native_basis,pins,G,K,Cnext)
    assert native_proof
    native_result=check_quotient(native_rows,native_active,R,native_basis,pins,G,K,Cnext,native_proof)
    assert native_active.bit_count()==16272 and native_result==dict(choices=18,representatives=6,omitted=12,generators=3)
    out=dict(status='pass',complete_four_state_binary_alphabets=alphabets,short_word_transport_checks=word_checks,
             full_subset_graph_controls=qualitative,actual_SC_sync_reachable_controls=actual_witnesses,
             separate_letter_conjugation_countercontrol=separate_failure,corruptions_rejected=rejected,
             native_partial_flag_control=dict(prefix=844,basis=native_basis,active_letters=16272,result=native_result,proof=native_proof),
             complete_native_flag_path_replay=False,no_geometry_exclusion=True,no_new_numerical_extremum=True,
             source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,'flag_stabilizer_quotient.py','check_flag_stabilizer_quotient.py',
                 'FLAG_STABILIZER_QUOTIENT_20261012.md',scope_name,parent_name,'b2_mixed_candidate844_literal_pool_20261012.json']},
             root_source_sha256={n:digest(ROOT/n) for n in ['c1_word_staircase_letter_generator.py','check_c1_word_staircase.py',
                 'enumerate_b3_staircase.py','check_b3_staircase.py','enumerate_b3_staircase_first.py']})
    dest=HERE/'flag_stabilizer_quotient_audit_20261012.json';assert not dest.exists()
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','root_source_sha256','native_partial_flag_control')}),flush=True)
if __name__=='__main__':main()
