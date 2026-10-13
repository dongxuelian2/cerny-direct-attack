"""Actual positive controls, full candidate split and adversarial corruptions."""
from hashlib import sha256
import copy,json
from pathlib import Path
from obligatory_supplier_split import certificate
from check_obligatory_supplier_split import check_certificate
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    source='b2_mixed_candidate844_second_literal_pool_20261012.json'
    c=json.loads((HERE/source).read_text())['candidate'];rows=c['rows'];R=[sum(1<<i for i in g) for g in c['required_groups']]
    active=(1<<len(rows))-1;proof=certificate(rows,active,R,c['basis'],11,9,8,max_choices=16)
    assert proof and proof['group']==4
    result=check_certificate(rows,active,R,c['basis'],11,9,8,proof);assert result==dict(branches=8,words=10240)
    rejected=[]
    def reject(name,mutate):
        d=copy.deepcopy(proof);mutate(d)
        try:check_certificate(rows,active,R,c['basis'],11,9,8,d)
        except (AssertionError,KeyError):rejected.append(name);return
        raise AssertionError('Accepted corrupted split: '+name)
    reject('missing branch',lambda d:d['branches'].pop())
    reject('duplicate branch',lambda d:d['branches'].append(d['branches'][0]))
    reject('wrong split group',lambda d:d.__setitem__('group',2))
    reject('unjustified forced letter',lambda d:d['branches'][0].__setitem__('letter',0))
    reject('altered remaining pool',lambda d:d['branches'][0].__setitem__('remaining_hex','0x0'))
    reject('invented depth',lambda d:d['branches'][0]['known'][0].__setitem__(1,0))
    reject('missing product tuple',lambda d:d['branches'][0]['product']['cases'].pop())
    reject('empty unsafe word',lambda d:d['branches'][0]['product']['cases'][0].__setitem__('word',[]))
    positives=0
    for z in json.loads((ROOT/'frontier_certificates.json').read_text())['certificates']:
        if z['n']>5 or z['value']<2:continue
        actual=z['rows'];n=z['n'];S=set(z['S']);A=set(z['A']);h=min(3,z['value']-1)
        reached={frozenset(S)}
        for depth in range(h):
            nxt={frozenset(row[q] for q in T) for T in reached for row in actual}
            assert all(len(T)==len(S) and A<=T for T in nxt);reached|=nxt
        assert certificate(actual,3,[3],[sum(1<<q for q in S)],h,len(S),sum(1<<q for q in A)) is None
        positives+=1
    assert positives
    out=dict(status='pass',prefix=844,proof=proof,complete_split=result,positive_actual_horizon_controls=positives,
             corruptions_rejected=rejected,no_geometry_exclusion=True,no_new_numerical_extremum=True,
             source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,source,'obligatory_supplier_split.py','check_obligatory_supplier_split.py',
                  'supplier_image_propagation.py','check_supplier_image_propagation.py','supplier_escape_words_v3.py','check_supplier_escape_words.py',
                  'PROOF.md#problem4-obligatory-supplier-split-20261012','PROOF.md#problem4-supplier-image-propagation','PROOF.md#problem4-supplier-escape-words']},
             root_source_sha256={'frontier_certificates.json':digest(ROOT/'frontier_certificates.json')})
    p=HERE/'obligatory_supplier_split_extended_audit_20261012.json';assert not p.exists()
    p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('proof','source_sha256','root_source_sha256')}),flush=True)
if __name__=='__main__':main()
