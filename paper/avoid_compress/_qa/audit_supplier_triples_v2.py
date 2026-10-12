"""Audit unrestricted bounded triple enumeration; no extremal conclusion."""
from hashlib import sha256
from itertools import product
import copy,json
from pathlib import Path
from supplier_escape_words_v2 import certificate
from check_supplier_escape_words import check_certificate
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'investigation'
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    source='b2_mixed_c4_third2_product_supplier_from640_v3_probe.json'
    c=json.loads((HERE/source).read_text())['candidate'];rows=c['rows']
    R=[sum(1<<i for i in g) for g in c['required_groups']];active=(1<<len(rows))-1
    proof=certificate(rows,active,R,c['basis'][0],11,9,8)
    assert proof['kind']=='suppliers' and proof['groups']==[0,2,5] and proof['forced']==[]
    assert check_certificate(rows,active,R,c['basis'][0],11,9,8,proof)==1536
    rejected=[]
    def reject(label,mutate):
        d=copy.deepcopy(proof);mutate(d)
        try:check_certificate(rows,active,R,c['basis'][0],11,9,8,d)
        except (AssertionError,KeyError):rejected.append(label);return
        raise AssertionError('Accepted corrupted proof: '+label)
    reject('missing tuple',lambda d:d['cases'].pop())
    reject('duplicate tuple',lambda d:d['cases'].append(d['cases'][0]))
    reject('wrong groups',lambda d:d.__setitem__('groups',[0,2,9]))
    reject('invented forced letter',lambda d:d.__setitem__('forced',[72]))
    reject('empty word',lambda d:d['cases'][0].__setitem__('word',[]))
    reject('beyond horizon',lambda d:d['cases'][0].__setitem__('word',[72]*12))
    reject('unjustified letter',lambda d:d['cases'][0]['word'].__setitem__(0,0))
    positives=0
    frontier=json.loads((ROOT/'frontier_certificates.json').read_text())['certificates']
    for z in frontier:
        if z['n']>4 or z['value']<2:continue
        n=z['n'];pool=list(product(range(n),repeat=n));ids={r:i for i,r in enumerate(pool)}
        actual=[ids[tuple(row)] for row in z['rows']];actual.append(ids[tuple(range(n))])
        S=set(z['S']);A=set(z['A']);h=min(3,z['value']-1)
        reached={frozenset(S)}
        for depth in range(h):
            nxt={frozenset(pool[i][q] for q in T) for T in reached for i in actual}
            assert all(len(T)==len(S) and A<=T for T in nxt);reached|=nxt
        # Every compulsory group meets this independently safe actual alphabet.
        groups=[]
        for i in actual:
            target={pool[i][q] for q in S}
            groups.append(sum(1<<j for j,row in enumerate(pool) if {row[q] for q in S}==target))
        assert certificate(pool,(1<<len(pool))-1,groups,sum(1<<q for q in S),h,len(S),sum(1<<q for q in A)) is None
        positives+=1
    assert positives
    out=dict(status='pass',proof=proof,complete_product=1536,positive_actual_horizon_controls=positives,
             corruptions_rejected=rejected,no_geometry_exclusion=True,no_new_numerical_extremum=True,
             source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,'supplier_escape_words_v2.py','check_supplier_escape_words.py',source,'SUPPLIER_ESCAPE_WORDS.md']},
             root_source_sha256={'frontier_certificates.json':digest(ROOT/'frontier_certificates.json')})
    dest=HERE/'supplier_triples_v2_audit_20261012.json';assert not dest.exists()
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('proof','source_sha256','root_source_sha256')}),flush=True)
if __name__=='__main__':main()
