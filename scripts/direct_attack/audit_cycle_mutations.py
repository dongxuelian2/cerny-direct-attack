"""Reject deliberate corruption of the newly stored independent certificates."""
from copy import deepcopy
import json
from pathlib import Path
from direct_attack.check_cycle_insertion import verify as verify_lift
from direct_attack.check_near_full import verify as verify_base


def main():
    base = json.loads(Path('scripts/direct_attack/data/near_full_n12_r3/protected_witness.json').read_text())
    lifted = json.loads(Path('scripts/direct_attack/data/cycle_insertion/n16.json').read_text())
    mutations = []
    for name, change in [
        ('pair_potential', lambda c: c['pair_potential'].__setitem__(1, c['pair_potential'][1]+1)),
        ('protected_port', lambda c: c.__setitem__('port', 11)),
        ('reach_word', lambda c: c.__setitem__('reach_word', [])),
        ('compression_word', lambda c: c.__setitem__('compression_word', [])),
    ]:
        c = deepcopy(base); change(c)
        try: verify_base(c)
        except AssertionError: mutations.append(dict(name='base_'+name, rejected=True))
        else: raise AssertionError('accepted corrupted base '+name)
    for name, change in [
        ('reset_word', lambda c: c.__setitem__('reset_word', [])),
        ('reach_word', lambda c: c.__setitem__('reach_word', [])),
        ('simulation_exponent', lambda c: c.__setitem__('simulation_exponent', 1)),
        ('compression_cost', lambda c: c.__setitem__('exact_compression', 8)),
    ]:
        c = deepcopy(lifted); change(c)
        try: verify_lift(c, base)
        except AssertionError: mutations.append(dict(name='lift_'+name, rejected=True))
        else: raise AssertionError('accepted corrupted lift '+name)
    Path('scripts/direct_attack/data/cycle_mutation_checks.json').write_text(json.dumps(mutations, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(mutations=len(mutations), all_rejected=True)))


if __name__ == '__main__': main()
