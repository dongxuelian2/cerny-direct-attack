"""Independent Fraction filtration, literal conflicts and complete cover replay."""
from functools import lru_cache
from hashlib import sha256
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;sys.path.insert(0,str(ROOT))
from check_b3_staircase import rat_rref,rat_contains
from check_candidate967_cover_tree_20261012_v2 import check as check_cover
@lru_cache(maxsize=1)
def verified_saved():
    pn='b2_mixed_candidate967_literal_pool_20261012.json';fn='candidate967_real_filtration_audit_20261012.json';cn='candidate967_growth_cover_tree_audit_20261012.json'
    p=json.loads((HERE/pn).read_text())['candidate'];f=json.loads((HERE/fn).read_text());c=json.loads((HERE/cn).read_text())
    assert f['status']==c['status']=='pass' and c['complete_saved_pool_cover_exclusion']
    basis=p['basis'];rows=p['rows'];assert len(basis)==12 and len(rows)==406 and len(set(map(tuple,rows)))==406
    assert all(0<=m<8192 and m.bit_count()==9 and m&8 for m in basis)
    assert all(len(row)==13 and set(row)<=set(range(13)) for row in rows)
    spans=[rat_rref(basis[:i+1]) for i in range(12)];assert list(map(len,spans))==list(range(1,13))
    members={}
    def contains(i,m):
        if (i,m) not in members:members[i,m]=rat_contains(spans[i],m)
        return members[i,m]
    growth=[[] for _ in range(12)];checks=0
    for j,row in enumerate(rows):
        for i,m in enumerate(basis):
            source={q for q in range(13) if m&(1<<q)};counts=[sum(row[q]==t for q in source) for t in range(13)]
            assert sum(counts)==9
            if i<11:
                target={row[q] for q in source};assert len(target)==9 and 3 in target
                output=sum(1<<q for q in target);assert contains(i+1,output);checks+=1
                if not contains(i,output):growth[i].append(j)
            elif counts[3]!=1:growth[i].append(j)
    assert checks==4466 and growth==f['growth_domains']==c['required_groups']
    assert f['basis']==basis and f['initial_image']==basis[0] and f['prefix_dimensions']==list(range(1,13))
    S={q for q in range(13) if basis[0]&(1<<q)}
    cover_counts=check_cover(rows,S,growth,c['clauses'],c['tree']);assert cover_counts==c['counts']
    return p,cover_counts,{n:sha256((HERE/n).read_bytes()).hexdigest() for n in (pn,fn,cn)},(pn,fn,cn)
def check_certificate(rows,active,S,record):
    p,counts,hashes,names=verified_saved()
    assert record['kind']=='real_filtration_pool_exclusion' and record['initial_image']==S==p['basis'][0]
    assert [record[k] for k in ('saved_pool','filtration','growth_cover')]==list(names)
    assert record['artifact_sha256']==hashes
    assert 0<active and active.bit_length()<=len(rows)
    ids=[i for i in range(len(rows)) if active&(1<<i)]
    transport=record['transport'];assert [i for i,j in transport]==ids and len({j for i,j in transport})==len(ids)
    for i,j in transport:assert 0<=j<406 and list(rows[i])==p['rows'][j]
    return dict(active_letters=len(ids),filtration_action_checks=4466,cover_nodes=counts['nodes'])
