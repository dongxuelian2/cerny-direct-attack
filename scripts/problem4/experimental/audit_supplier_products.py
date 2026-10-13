"""Positive controls and complete adversarial checks of word-product certificates."""
from hashlib import sha256
from itertools import product
import copy,json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;sys.path.insert(0,str(ROOT))
from supplier_escape_words import certificate
from check_supplier_escape_words import check_certificate
def digest(p):return sha256(p.read_bytes()).hexdigest()
def literal_image(row,S):return {row[q] for q in S}
def main():
    source='b2_mixed_c4_third2_supplier_image_from638_v2_probe.json';c=json.loads((HERE/source).read_text())['candidate']
    rows=c['rows'];R=[sum(1<<i for i in g) for g in c['required_groups']];active=(1<<len(rows))-1
    proof=certificate(rows,active,R,c['basis'][0],11,9,8);assert proof is not None
    assert proof['kind']=='suppliers' and proof['groups']==[2,5]
    assert check_certificate(rows,active,R,c['basis'][0],11,9,8,proof)==1152
    bad=[]
    def reject(label,mutate):
        d=copy.deepcopy(proof);mutate(d)
        try:check_certificate(rows,active,R,c['basis'][0],11,9,8,d)
        except (AssertionError,KeyError):bad.append(label);return
        raise AssertionError('Accepted a corrupted product certificate: '+label)
    reject('missing combination',lambda d:d['cases'].pop())
    reject('duplicate combination',lambda d:d['cases'].append(d['cases'][0]))
    reject('wrong domains',lambda d:d.__setitem__('groups',[0,5]))
    reject('missing forced premise',lambda d:d.__setitem__('forced',[]))
    reject('empty word',lambda d:d['cases'][0].__setitem__('word',[]))
    reject('beyond horizon',lambda d:d['cases'][0].__setitem__('word',[66]*12))
    reject('wrong tuple',lambda d:d['cases'][0]['choices'].__setitem__(0,66))
    def foreign(d):
        allowed={66}|set(d['cases'][0]['choices']);i=next(i for i in range(len(rows)) if i not in allowed)
        d['cases'][0]['word'][0]=i
    reject('unjustified letter',foreign)
    frontier=json.loads((ROOT/'frontier_certificates.json').read_text())['certificates'];positive=0
    for z in frontier:
        n=z['n']
        if n>4 or z['value']<2:continue
        allrows=list(product(range(n),repeat=n));index={r:i for i,r in enumerate(allrows)}
        ident=index[tuple(range(n))];S=set(z['S']);mask=sum(1<<q for q in S);A=sum(1<<q for q in z['A']);h=min(3,z['value']-1)
        actual=z['rows']+[list(range(n))]
        # Ordinary-set BFS independently verifies the claimed control horizon.
        reached={frozenset(S)}
        for d in range(h):
            following={frozenset(literal_image(row,T)) for T in reached for row in actual}
            assert all(len(T)==len(S) and set(z['A'])<=T for T in following);reached|=following
        for row in z['rows']:
            for q in range(n):
                if row[q]!=q:continue
                target=literal_image(row,S)
                group=sum(1<<i for i,r in enumerate(allrows) if r[q]==q and literal_image(r,S)==target)
                assert group>>index[tuple(row)]&1
                answer=certificate(allrows,(1<<len(allrows))-1,[1<<ident,group],mask,h,len(S),A)
                assert answer is None;positive+=1
    assert positive>0
    out=dict(status='pass',positive_actual_horizon_controls=positive,complete_candidate_product=1152,
        product_kind=proof['kind'],groups=proof['groups'],proof=proof,rejected_corruptions=bad,adversarial_corruptions_rejected=len(bad),
        no_geometry_exclusion=True,no_new_numerical_extremum=True,
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,'supplier_escape_words.py','check_supplier_escape_words.py',
            'PROOF.md#problem4-supplier-escape-words',source]},root_source_sha256={'frontier_certificates.json':digest(ROOT/'frontier_certificates.json')})
    dest=HERE/'supplier_products_audit_20261012.json';assert not dest.exists()
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('proof','source_sha256','root_source_sha256')}),flush=True)
if __name__=='__main__':main()
