"""Independent ordinary-set coverage checks, including repeated letters."""
from itertools import combinations_with_replacement
def check_certificate(active,required,proof):
    assert active>=0 and required and all(g&active for g in required)
    indices={i for i in range(active.bit_length()) if active&(1<<i)}
    domains=[{i for i in indices if g&(1<<i)} for g in required]
    patterns={frozenset(j for j,g in enumerate(domains) if i in g) for i in indices}
    literal=sorted(sum(1<<j for j in p) for p in patterns)
    assert proof['patterns']==literal and proof['groups']==len(domains) and proof['letters']==len(indices)
    universe=set(range(len(domains)))
    assert all(a|b!=universe for a,b in combinations_with_replacement(patterns,2))
    return dict(patterns=len(patterns),groups=len(domains),letters=len(indices))
