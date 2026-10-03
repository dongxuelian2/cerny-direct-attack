"""Negative tests for reachable-capacity and greedy-image-policy certificates."""
from copy import deepcopy
import json
from pathlib import Path
from direct_attack.check_image_extension import verify
from direct_attack.check_image_policy import verify as verify_policy


def main():
    c=json.loads(Path('direct_attack/data/image_extension_n5/n5_cost10.json').read_text())
    mutations=[]
    for name,change in [
        ('capacity',lambda x:x['image_capacity'].__setitem__(3,1)),
        ('distance',lambda x:x['preimage_distances']['2'].__setitem__(24,9)),
        ('reachability',lambda x:x['witness'].__setitem__('start_reach_word',[])),
        ('extension_word',lambda x:x['witness'].__setitem__('word',[])),
    ]:
        x=deepcopy(c);change(x)
        try:verify(x)
        except AssertionError:mutations.append(dict(field=name,rejected=True))
        else:raise AssertionError('accepted corruption '+name)
    p=json.loads(Path('direct_attack/data/image_extension_policy/witness_000.json').read_text())
    x=deepcopy(p);x['reset_word']=[]
    try:verify_policy(x)
    except AssertionError:mutations.append(dict(field='policy_reset_word',rejected=True))
    else:raise AssertionError('accepted policy corruption')
    Path('direct_attack/data/image_mutation_checks.json').write_text(json.dumps(mutations,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(mutations=len(mutations),all_rejected=True)))


if __name__=='__main__':main()
