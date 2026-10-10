"""Independent positive controls and exact scope ledger for restricted searches.

The negative covers a stated construction family only; no global upper follows.
"""
from pathlib import Path
import hashlib
import json
from math import factorial
from alphabet_check import bfs, certificate, pair_distances, strong, verify

ROOT=Path(__file__).resolve().parent


def main():
    records=[]
    for name,expected in [('odd_core_sanitized_control_n11.json',9),
                          ('odd_core_proved_pruning_n13.json',11),
                          ('odd_core_corank2_n13.json',10),
                          ('odd_core_corank3_n13.json',9),
                          ('odd_core_corank2_sanitized_n11.json',8),
                          ('odd_core_corank3_sanitized_n11.json',5)]:
        data=json.loads((ROOT/name).read_text(encoding='utf-8'))
        assert data.get('best',data.get('best_retained'))==expected
        z=certificate(data['rows'],data['S'],1)
        if z is not None:
            assert z['value']==expected and verify(z)
        else:
            # Native searches deliberately include unreachable subsets.
            # This sanitizer control is not a manuscript lower witness.
            assert name=='odd_core_corank3_sanitized_n11.json'
            reaching,_=bfs(data['rows'],range(data['n']),lambda U:U==frozenset(data['S']))
            assert reaching is None and strong(data['rows'])
            assert len(pair_distances(data['rows']))==data['n']*(data['n']-1)//2
        word,_=bfs(data['rows'],data['S'],lambda U:len(U)<data['s'] or not set(data['A'])<=U)
        assert word is not None and len(word)==expected
        if data['n']==13 and 'involutions' in data:
            assert data['involutions']==604800  # legacy counter name: base permutations
            assert data['redirected_maps']==33868800
            assert data['b_cycle_types']==15 and data['arbitrary_core_permutations']
            assert data['subset_tests']==79722860
        if 'a_corank' in data:
            k=2*data['m'];rank=k-data['a_corank']
            partitions=[]
            def enumerate_partitions(prefix,maximum):
                if len(prefix)==k:
                    if maximum+1==rank and sum(prefix.count(i)*(prefix.count(i)-1)//2 for i in range(rank))<=4:
                        partitions.append(tuple(prefix))
                    return
                for group in range(min(maximum+1,rank-1)+1):
                    enumerate_partitions(prefix+[group],max(maximum,group))
            enumerate_partitions([0],0)
            assert len(partitions)*data['b_cycle_types']==data['kernel_partitions']
            assert len(partitions)*data['b_cycle_types']*factorial(k)//factorial(k-rank)==data['maps']
        records.append(dict(file=name,report_sha256=hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),
                            witness=z,reachable_image=z is not None,
                            local_value=expected,ordinary_bfs_verified=True))
    result=dict(status='restricted_search_positive_controls_verified',records=records,
                source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
                               ('probe_odd_core.cpp','probe_odd_core_higher.cpp','alphabet_check.py')},
                checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                controls='n11 ASan/UBSan controls and n13 independently verified best witnesses; higher-corank partition and assignment counts checked independently',
                scope='Identity on long-cycle interior, outputs confined to active core, permutation b, initial S containing the entire long cycle. Coranks one through three at n13. Includes unreachable initial sets. No general negative theorem.',
                legacy_counter='involutions counts base involutions or base permutations according to arbitrary_core_permutations',
                corrected_negative_authority=['odd_core_proved_pruning_n13.json','odd_core_corank2_n13.json','odd_core_corank3_n13.json'],
                retracted_negative_records=['odd_core_permutations_n13.json'],
                admitted_pruning='P1<=4 and cover(P4)<=3 only, plus proved equality flags in higher-corank n13 runs; no higher-layer edge-count caps')
    (ROOT/'odd_core_search_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],local_values=[z['local_value'] for z in records],
                         reachable_witnesses=sum(z['reachable_image'] for z in records))))


if __name__=='__main__':
    main()
