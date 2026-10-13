"""Entire active literal pool inclusion in one audited real-flag exclusion."""
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
POOL='b2_mixed_candidate967_literal_pool_20261012.json'
FLAG='candidate967_real_filtration_audit_20261012.json'
COVER='candidate967_growth_cover_tree_audit_20261012.json'
@lru_cache(maxsize=1)
def saved():
    p=json.loads((HERE/POOL).read_text())['candidate'];f=json.loads((HERE/FLAG).read_text());c=json.loads((HERE/COVER).read_text())
    assert f['status']==c['status']=='pass' and f['basis']==p['basis']
    assert c['required_groups']==f['growth_domains'] and c['complete_saved_pool_cover_exclusion']
    index={tuple(r):i for i,r in enumerate(p['rows'])};assert len(index)==len(p['rows'])==406
    return p,index,{n:sha256((HERE/n).read_bytes()).hexdigest() for n in (POOL,FLAG,COVER)}
def certificate(rows,active,S):
    p,index,hashes=saved()
    if S!=p['basis'][0] or not active or active.bit_count()>406:return None
    assert active>=0 and active.bit_length()<=len(rows)
    transport=[];bits=active
    while bits:
        bit=bits&-bits;bits-=bit;i=bit.bit_length()-1;j=index.get(tuple(rows[i]))
        if j is None:return None
        transport.append([i,j])
    if len({j for i,j in transport})!=len(transport):return None
    return dict(kind='real_filtration_pool_exclusion',initial_image=S,
        saved_pool=POOL,filtration=FLAG,growth_cover=COVER,artifact_sha256=hashes,transport=transport)
