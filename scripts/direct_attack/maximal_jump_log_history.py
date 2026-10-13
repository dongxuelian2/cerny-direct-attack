"""Sparse original PU alphabet realizing maximal shortest log-rank histories."""
import argparse
import json
from pathlib import Path


def swap_value(q, x, y):
    return y if q == x else x if q == y else q


def conjugator(q, r):
    assert q != r
    a, b = q, r
    steps = []
    if a != 1:
        steps.append([a,1])
        a,b = swap_value(a,a,1),swap_value(b,a,1)
    if b != 2:
        steps.append([b,2])
        a,b = swap_value(a,b,2),swap_value(b,b,2)
    assert (a,b) == (1,2)
    return steps


def record(d):
    n = 2**d-1
    blocks = [[2**i-1,2**(i+1)-2] for i in range(d)]
    def inside(k,q):
        return bool(k & (1 << ((q+1).bit_length()-1)))
    stages = [dict(child='singleton2',parent=2,word=[['u',1,1]],cost=1)]
    for k in range(2,n):
        i = next(i for i in range(1,d) if (k+1)>>i&1)
        stages.append(dict(child=k,parent=k+1,unit_block=i,
                           word=[['u',i,1],['p',k]],cost=2,
                           all_shortest_parent_size=k+1))
    membership = []
    for k in range(2,n):
        root = next(q for q in range(n) if inside(k,q))
        cost = 0
        for q in range(n):
            if not inside(k,q):
                steps = conjugator(q,root)
                cost += 2*sum(2*abs(x-y)-1 for x,y in steps)+1
        membership.append(dict(target=k,root=root,charged_cost=cost,
                               outside_inputs=n-k,word='increasing outside q, expanded rho(q,r) u1+ inverse(rho(q,r))'))
    word = [label for stage in reversed(stages) for label in stage['word']]
    return dict(d=d,n=n,blocks=blocks,alphabet_symbols=2*n+2*d-5,
                stages=stages,actual_membership=membership,long_reset=word,
                long_reset_cost=2*n-3,endpoint=2,rt_lower=n-1,rt_upper=2*n-3,
                policy_upper=2*n-3,raw_dimension=d,normalized_dimension=d-1,
                full_history_raw_dimension=2*d-1,full_history_normalized_dimension=2*d-2,
                proper_stages=n-2,all_original_ranks=[n-1,n])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='scripts/direct_attack/data/maximal_jump_log_history.json')
    args=ap.parse_args()
    records=[record(d) for d in range(3,12)]
    data=dict(status='COMPUTATIONAL certificate; all-d paper proof separate',
              definition='PROOF.md#direct-attack-maximal-jump-log-history',records=records,
              scope=dict(parameters=len(records),max_n=records[-1]['n']))
    Path(args.out).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data['scope']))


if __name__=='__main__': main()
