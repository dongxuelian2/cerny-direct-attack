"""Complete graph-quotient flag probe with independent literal/rational checks."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'investigation';sys.path.insert(0,str(ROOT))
from c1_word_staircase_letter_generator import pool
from check_c1_word_staircase import literal_pool
from basis_column_staircase import tree
from check_basis_column_staircase import check_tree
def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def bindings(d):
    for n,h in d.get('source_sha256',{}).items():assert digest(HERE/n)==h,n
    for n,h in d.get('root_source_sha256',{}).items():assert digest(ROOT/n)==h,n

def main():
    name=sys.argv[1];file=name+'_graph_quotient_scope.json';af=name+'_graph_quotient_transport_audit.json'
    dest=HERE/(name+'_graph_quotient_full_probe.json');assert not dest.exists()
    scope=read(HERE/file);audit=read(HERE/af);assert audit['status']=='pass';bindings(scope);bindings(audit)
    assert audit['counts']['canonical_prefixes']==len(scope['prefixes']) and audit['rejected_invalid_metadata']==12
    parentpath=HERE/(name+'_inverse_probe.json');parent=read(parentpath)
    z=next(z for z in read(ROOT/'small_first_third_inventory.json')['records'] if z['id']==name)
    B,C,D=map(set,(z['B'],z['C'],z['D']));keep={r['P1_mask']:r for r in parent['records'] if r['reason']=='retained_overapproximation'}
    records=[];counts=Counter();candidate=None
    for index,prefix in enumerate(scope['prefixes']):
        c=keep[prefix['P1_mask']];p=dict(mandatory=parent['mandatory'],required_P3_edges=c['G'],fields=parent['fields'])
        view=dict(extra_pair=None,field_kernel_masks=c['field_kernel_masks']);basis=tuple(prefix['basis'])
        S,T=[{q for q in range(13) if m>>q&1} for m in basis]
        rows,G=pool(p,view,S,T,B,C,D);independent,H=literal_pool(p,view,basis,B,C,D)
        assert independent==rows and H==G
        print(json.dumps(dict(prefix=index,total=len(scope['prefixes']),letters=len(rows))),flush=True)
        try:
            proof,stats=tree(rows,basis,B,C,D,G)
            assert check_tree(independent,basis,B,C,D,G,proof)==stats
        except AssertionError as error:
            if 'depth-11' not in str(error):raise
            tb=error.__traceback__;saved=None
            while tb:
                local=tb.tb_frame.f_locals
                if tb.tb_frame.f_code.co_name=='visit' and local.get('k')==11:
                    saved=dict(basis=list(local['basis']),active=local['active'],required=list(local['required']))
                tb=tb.tb_next
            assert saved is not None;active=saved.pop('active')
            saved['rows']=[list(row) for k,(row,f) in enumerate(rows) if active>>k&1]
            saved['supplier_flags']=[f for k,(row,f) in enumerate(rows) if active>>k&1]
            candidate=dict(prefix=index,P1_mask=prefix['P1_mask'],initial_basis=list(basis),**saved);break
        records.append(dict(index=index,**prefix,letter_count=len(rows),tree=proof,tree_stats=stats,
            rows_sha256=sha256(json.dumps([list(r) for r,f in rows],separators=(',',':')).encode()).hexdigest(),
            flags_sha256=sha256(json.dumps([f for r,f in rows],separators=(',',':')).encode()).hexdigest()))
        counts.update(stats);counts['prefixes']+=1;counts['literal_letters']+=len(rows)
    status='depth11_candidate_not_exclusion' if candidate else 'complete_independently_checked_QA_only'
    if candidate is None:assert len(records)==len(scope['prefixes'])
    roots=['c1_word_staircase_letter_generator.py','check_c1_word_staircase.py','basis_column_staircase.py',
        'check_basis_column_staircase.py','BASIS_COLUMN_REACHING_PRUNING.md','basis_column_reaching_audit.json',
        'LOCAL_EQUALITY_FLAG.md','local_equality_flag_audit.json','FEW_GRAPH_FIRST_PAIR_CERTIFICATES.md',
        'small_first_third_inventory.json']
    out=dict(status=status,id=name,parameter=[13,9,1],target_ac=12,counts=dict(counts),prefixes=records,candidate=candidate,
        complete_scope=candidate is None,no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        scope='Complete graph quotient and independent literal/rational flag checks. Authoritative adoption still requires immutable packaging and isolated byte-identical regeneration; candidates require all original automaton checks.',
        source_sha256={Path(__file__).name:digest(Path(__file__)),file:digest(HERE/file),af:digest(HERE/af),
            parentpath.name:digest(parentpath),'GRAPH_FIRST_TRANSPORTS.md':digest(HERE/'GRAPH_FIRST_TRANSPORTS.md')},
        root_source_sha256={n:digest(ROOT/n) for n in roots})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','root_source_sha256','prefixes','candidate')}),flush=True)
if __name__=='__main__':main()
