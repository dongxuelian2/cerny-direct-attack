"""Integer elimination and independent Fraction replay of all literal actions."""
from functools import lru_cache
from hashlib import sha256
from math import gcd
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'investigation';sys.path.insert(0,str(ROOT))
from check_b3_staircase import rat_rref,rat_contains
def digest(p):return sha256(p.read_bytes()).hexdigest()
def integer_rank(matrix):
    M=[list(row) for row in matrix];rank=0
    for col in range(13):
        p=next((j for j in range(rank,len(M)) if M[j][col]),None)
        if p is None:continue
        M[rank],M[p]=M[p],M[rank];pivot=M[rank][col]
        for j in range(rank+1,len(M)):
            q=M[j][col]
            if not q:continue
            M[j]=[pivot*x-q*y for x,y in zip(M[j],M[rank])]
            common=0
            for x in M[j]:common=gcd(common,abs(x))
            if common:M[j]=[x//common for x in M[j]]
        rank+=1
    return rank
def main():
    dest=HERE/'candidate967_real_filtration_audit_20261012.json';assert not dest.exists()
    source='b2_mixed_candidate967_literal_pool_20261012.json';p=json.loads((HERE/source).read_text())['candidate']
    rows=p['rows'];basis=p['basis'];assert len(rows)==406 and len(basis)==12
    assert len(set(map(tuple,rows)))==406 and all(len(r)==13 and set(r)<=set(range(13)) for r in rows)
    vectors=[[int(bool(m&(1<<q))) for q in range(13)] for m in basis]
    assert all(sum(v)==9 and v[3]==1 for v in vectors)
    dimensions=[integer_rank(vectors[:i+1]) for i in range(12)];assert dimensions==list(range(1,13))
    rational=[rat_rref(basis[:i+1]) for i in range(12)];assert list(map(len,rational))==dimensions
    @lru_cache(maxsize=None)
    def member(i,y):return integer_rank(vectors[:i+1]+[list(y)])==i+1
    growth=[[] for _ in range(12)];steps=0
    for j,row in enumerate(rows):
        for i,v in enumerate(vectors):
            y=[0]*13
            for q in range(13):y[row[q]]+=v[q]
            assert sum(y)==9
            if i<11:
                assert set(y)<={0,1} and y[3]==1
                m=sum(1<<q for q in range(13) if y[q]);inside=member(i,tuple(y))
                assert member(i+1,tuple(y)) and rat_contains(rational[i+1],m)
                assert inside==rat_contains(rational[i],m);steps+=1
                if not inside:growth[i].append(j)
            elif y[3]!=1:growth[i].append(j)
    diagnostic='candidate967_filtration_diagnostic_20261012.json';old=json.loads((HERE/diagnostic).read_text())
    assert growth==old['growth_domains'] and all(growth) and steps==4466
    out=dict(status='pass',pool=406,basis=basis,initial_image=basis[0],prefix_dimensions=dimensions,
        exact_integer_and_rational_action_checks=steps,growth_domains=growth,growth_sizes=list(map(len,growth)),
        complete_finite_pool_filtration=True,depth_twelve_safety_required=False,
        no_geometry_exclusion=True,no_new_numerical_extremum=True,
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,source,diagnostic,'REAL_FILTRATION_POOL_20261012.md']},
        root_source_sha256={'check_b3_staircase.py':digest(ROOT/'check_b3_staircase.py')})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('growth_domains','source_sha256','root_source_sha256','basis')}),flush=True)
if __name__=='__main__':main()
