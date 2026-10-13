"""Exact at-most-two-letter coverage of compulsory supplier domains."""
def certificate(active,required):
    if not required or any(not(g&active) for g in required):return None
    patterns=set();bits=active
    while bits:
        bit=bits&-bits;bits-=bit
        patterns.add(sum((1<<j) for j,g in enumerate(required) if g&bit))
    patterns=sorted(patterns);full=(1<<len(required))-1
    for i,a in enumerate(patterns):
        for b in patterns[i:]:
            if a|b==full:return None
    return dict(patterns=patterns,groups=len(required),letters=active.bit_count())
