"""Canonical literal conflicts, independently verified without trusting solver status."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    dest=HERE/'candidate967_common_literal_word_cuts_20261012.json';assert not dest.exists()
    pool='b2_mixed_candidate967_literal_pool_20261012.json';p=json.loads((HERE/pool).read_text())['candidate']
    rows=p['rows'];S={q for q in range(13) if p['basis'][0]>>q&1};assert len(rows)==406 and len(S)==9 and 3 in S
    inputs=[('candidate967_alphabet_synthesis_20261012.json','cuts'),
            ('candidate967_alphabet_rank_synthesis_20261012.json','cuts'),
            ('candidate967_second_extra_word_cuts_20261012.json','extra_cuts'),
            ('candidate967_second_alphabet_rank_synthesis_20261012.json','cuts'),
            ('candidate967_common_domains_synthesis_20261012.json','learned')]
    unique={};types={}
    for name,key in inputs:
        for c in json.loads((HERE/name).read_text())[key]:
            w=c['word'];assert all(0<=i<len(rows) for i in w)
            if c['kind']=='short_rank_word':assert 1<=len(w)<=6;T=set(range(13))
            else:assert c['kind']=='unsafe_word' and 1<=len(w)<=11;T=set(S)
            for i in w:T={rows[i][q] for q in T}
            if c['kind']=='short_rank_word':assert len(T)<=9
            else:assert len(T)<9 or 3 not in T
            unique.setdefault(tuple(sorted(set(w))),c)
    keys=sorted(unique,key=lambda k:(len(k),k));clauses=[unique[k] for k in keys]
    for c in clauses:types[c['kind']]=types.get(c['kind'],0)+1
    out=dict(status='pass',literal_pool=406,initial_image=p['basis'][0],distinct_forbidden_alphabets=len(clauses),
        types=types,clauses=clauses,no_geometry_exclusion=True,no_new_numerical_extremum=True,
        scope='Verified literal word cuts only; no supplier-cover or original flag-path conclusion. Solver status is not used.',
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,pool,*[n for n,k in inputs],
            'PROOF.md#problem4-rank-word-compression-pruning-20261012','PROOF.md#problem4-fold-compressibility-premise-20261012']})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('clauses','source_sha256')}),flush=True)
if __name__=='__main__':main()
