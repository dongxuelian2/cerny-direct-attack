"""Complete small coverage families, saved flag pools and corruptions."""
from itertools import product,combinations_with_replacement
from hashlib import sha256
from pathlib import Path
import copy,json
from binary_supplier_cover import certificate
from check_binary_supplier_cover import check_certificate
HERE=Path(__file__).resolve().parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    total=negative=positive=0
    for n in range(1,6):
        max_groups=4 if n<=4 else 3
        for k in range(1,max_groups+1):
            for required in product(range(1,1<<n),repeat=k):
                required=list(required);active=(1<<n)-1
                expected=any(all(g&(1<<a|1<<b) for g in required) for a,b in combinations_with_replacement(range(n),2))
                proof=certificate(active,required);assert (proof is None)==expected
                if proof is not None:check_certificate(active,required,proof);negative+=1
                else:positive+=1
                total+=1
    inputs=['b2_mixed_candidate844_literal_pool_20261012.json','b2_mixed_candidate844_second_literal_pool_20261012.json']
    records=[];rejected=[]
    for source in inputs:
        c=json.loads((HERE/source).read_text())['candidate'];active=(1<<len(c['rows']))-1
        required=[sum(1<<i for i in g) for g in c['required_groups']];proof=certificate(active,required)
        assert proof is not None;result=check_certificate(active,required,proof)
        records.append(dict(file=source,result=result,proof=proof))
        for label,change in [('missing pattern',lambda d:d['patterns'].pop()),
                             ('invented covering pattern',lambda d:d['patterns'].append((1<<len(required))-1)),
                             ('wrong group count',lambda d:d.__setitem__('groups',len(required)-1)),
                             ('wrong letter count',lambda d:d.__setitem__('letters',0))]:
            corrupt=copy.deepcopy(proof);change(corrupt)
            try:check_certificate(active,required,corrupt)
            except AssertionError:rejected.append(source+': '+label)
            else:raise AssertionError('Accepted corrupt cover certificate')
    # Deleting possible actual letters must not be confused with a whole-pool cut.
    assert certificate(7,[1,2,4]) is not None
    assert certificate(15,[1|8,2|8,4|8]) is None
    out=dict(status='pass',complete_small_families=total,impossible_binary_families=negative,covering_families=positive,
             maximum_literal_pool=5,maximum_groups=4,records=records,corruptions_rejected=rejected,
             no_geometry_exclusion=True,no_new_numerical_extremum=True,no_alphabet_separation=True,
             source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,'binary_supplier_cover.py','check_binary_supplier_cover.py',
                'BINARY_SUPPLIER_COVER_20261012.md',*inputs]})
    p=HERE/'binary_supplier_cover_audit_20261012.json';assert not p.exists()
    p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('records','source_sha256')}),flush=True)
if __name__=='__main__':main()
