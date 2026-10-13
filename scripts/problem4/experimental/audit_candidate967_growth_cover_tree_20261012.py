"""Produce a complete finite cover tree from literal word cuts, without SMT."""
from hashlib import sha256
import json,time
from pathlib import Path
from check_candidate967_cover_tree_20261012_v2 import check
HERE=Path(__file__).resolve().parent

def digest(p):return sha256(p.read_bytes()).hexdigest()

def main():
    dest=HERE/'candidate967_growth_cover_tree_audit_20261012.json';assert not dest.exists()
    pool='b2_mixed_candidate967_literal_pool_20261012.json';c=json.loads((HERE/pool).read_text())['candidate']
    rows=c['rows'];filtration_file='candidate967_real_filtration_audit_20261012.json';filtration=json.loads((HERE/filtration_file).read_text());assert filtration['status']=='pass'
    groups=filtration['growth_domains'];N=len(rows);assert N==406 and len(groups)==12
    sources=['candidate967_common_literal_word_cuts_20261012.json']
    dataset=json.loads((HERE/sources[0]).read_text());assert dataset['status']=='pass'
    clauses=dataset['clauses'];keys=[tuple(sorted(set(cut['word']))) for cut in clauses]
    assert len(keys)==len(set(keys))
    negative=[sum(1<<i for i in k) for k in keys];positive=[sum(1<<i for i in g) for g in groups]
    nodes=0;deadline=time.monotonic()+60
    def visit(F,D):
        nonlocal nodes
        nodes+=1
        if time.monotonic()>deadline:raise TimeoutError('Complete finite cover proof not obtained within budget')
        assert not F&D;units=[]
        while True:
            changed=False
            for j,R in enumerate(positive):
                if R&F:continue
                rest=R&~D
                if not rest:return dict(units=units,reason='missing_group',group=j)
                if rest.bit_count()==1:
                    F|=rest;units.append(dict(kind='force',group=j,letter=rest.bit_length()-1));changed=True
            for j,R in enumerate(negative):
                if R&D:continue
                rest=R&~F
                if not rest:return dict(units=units,reason='forbidden_alphabet',clause=j)
                if rest.bit_count()==1:
                    D|=rest;units.append(dict(kind='delete',clause=j,letter=rest.bit_length()-1));changed=True
            if not changed:break
        choices=[((R&~D).bit_count(),j,R&~D) for j,R in enumerate(positive) if not R&F]
        assert choices,'Found a satisfying cover contrary to the independent finite contradiction request'
        _,j,R=min(choices);children=[];prior=0
        for i in range(N):
            if R>>i&1:
                children.append(dict(letter=i,node=visit(F|(1<<i),D|prior)));prior|=1<<i
        return dict(units=units,reason='all_first_suppliers_rejected',group=j,children=children)
    tree=visit(0,0);S={q for q in range(13) if c['basis'][0]>>q&1};counts=check(rows,S,groups,clauses,tree)
    assert counts['nodes']==nodes
    out=dict(status='pass',prefix=967,conditional_pool=N,required_groups=groups,compulsory_group_count=12,distinct_forbidden_alphabets=len(clauses),
        counts=counts,tree=tree,clauses=clauses,complete_saved_pool_cover_exclusion=True,
        complete_original_flag_path_replay=False,complete_geometry_exclusion=False,no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        scope='Finite independently checked cover contradiction for one conditional saved flag. Rank clauses use the existing compressible-subset rank-word bound. No original flag-path replay or whole geometry exclusion.',
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,'check_candidate967_cover_tree_20261012_v2.py',pool,*sources,
            'b2_candidate967_saved_origin_audit_20261012.json','PROOF.md#problem4-rank-word-compression-pruning-20261012',
            'rank_word_compression_audit_20261012.json','PROOF.md#problem4-fold-compressibility-premise-20261012','fold_compressibility_audit_20261012.json',filtration_file,'PROOF.md#problem4-real-filtration-pool-20261012']})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('tree','clauses','source_sha256','required_groups')}),flush=True)
if __name__=='__main__':main()
