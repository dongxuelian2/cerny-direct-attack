"""Independent ordinary-set checks for each complete conditional product."""
from itertools import product
def check_certificate(rows,active,required,S,horizon,size,protected,record):
    ids={i for i in range(len(rows)) if active&(1<<i)};domains=[{i for i in ids if g&(1<<i)} for g in required]
    assert domains and all(domains)
    forced={next(iter(g)) for g in domains if len(g)==1};assert record['forced']==sorted(forced)
    if record['kind']=='suppliers':
        groups=record['groups'];assert len(groups) in (2,3) and groups==sorted(set(groups))
        assert all(0<=j<len(domains) for j in groups);lists=[domains[j] for j in groups]
    else:
        assert record['kind']=='SC_escape'
        q=record['state'];assert 0<=q<len(rows[0]) and all(rows[i][q]==q for i in forced)
        escape={i for i in ids if rows[i][q]!=q};assert escape
        j=record['supplier_group'];assert 0<=j<len(domains);lists=[domains[j],escape]
    expected=set(product(*lists));seen=set()
    initial={q for q in range(len(rows[0])) if S&(1<<q)};A={q for q in range(len(rows[0])) if protected&(1<<q)}
    assert len(initial)==size and A<=initial
    for case in record['cases']:
        choices=tuple(case['choices']);assert choices in expected and choices not in seen;seen.add(choices)
        word=case['word'];assert 1<=len(word)<=horizon and set(word)<=forced|set(choices)
        image=set(initial)
        for i in word:image={rows[i][p] for p in image}
        assert len(image)<size or not A<=image
    assert seen==expected
    return len(seen)
