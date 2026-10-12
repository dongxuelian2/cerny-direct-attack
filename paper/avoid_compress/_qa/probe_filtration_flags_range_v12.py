"""Complete graph-quotient flag probe with independent literal/rational checks."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'investigation';sys.path.insert(0,str(ROOT))
from c1_word_staircase_letter_generator import pool
from check_c1_word_staircase import literal_pool
from filtration_quotient_staircase_20261012 import tree
from check_filtration_quotient_staircase_20261012 import check_tree
def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def bindings(d):
    for n,h in d.get('source_sha256',{}).items():assert digest(HERE/n)==h,n
    for n,h in d.get('root_source_sha256',{}).items():assert digest(ROOT/n)==h,n

def main():
    name=sys.argv[1];start=int(sys.argv[2]) if len(sys.argv)>2 else 0;assert start>=0;file=name+'_graph_quotient_scope.json';af=name+'_graph_quotient_transport_audit.json'
    dest=HERE/(name+'_product_supplier_from'+str(start)+'_v12_probe.json');assert not dest.exists()
    scope=read(HERE/file);audit=read(HERE/af);assert audit['status']=='pass';bindings(scope);bindings(audit)
    assert audit['counts']['canonical_prefixes']==len(scope['prefixes']) and audit['rejected_invalid_metadata']==12
    for control in ('supplier_image_controls_audit_20261011.json','supplier_image_horizon_audit_20261011.json','supplier_products_audit_20261012.json','supplier_product_extensions_audit_20261012.json','supplier_triples_v2_audit_20261012.json','supplier_triples_v3_audit_20261012.json','obligatory_supplier_split_audit_20261012.json','obligatory_supplier_split_extended_audit_20261012.json','flag_stabilizer_quotient_audit_20261012.json','candidate967_common_literal_word_cuts_20261012.json','candidate967_real_filtration_audit_20261012.json','candidate967_growth_cover_tree_audit_20261012.json','filtration_pool_exclusion_audit_20261012.json'):
        obj=read(HERE/control);assert obj['status']=='pass';bindings(obj)
    parentpath=HERE/(name+'_inverse_probe.json');parent=read(parentpath)
    z=next(z for z in read(ROOT/'small_first_third_inventory.json')['records'] if z['id']==name)
    B,C,D=map(set,(z['B'],z['C'],z['D']));keep={r['P1_mask']:r for r in parent['records'] if r['reason']=='retained_overapproximation'}
    records=[];counts=Counter();candidate=None
    assert start<len(scope['prefixes'])
    for index in range(start,len(scope['prefixes'])):
        prefix=scope['prefixes'][index]
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
            assert saved is not None;active=saved.pop('active');required=saved.pop('required')
            positions=[i for i in range(len(rows)) if active>>i&1]
            saved['original_letter_indices']=positions
            saved['required_groups']=[[j for j,i in enumerate(positions) if group>>i&1] for group in required]
            assert all(saved['required_groups'])
            saved['rows']=[list(rows[i][0]) for i in positions]
            saved['supplier_flags']=[rows[i][1] for i in positions]
            candidate=dict(prefix=index,P1_mask=prefix['P1_mask'],initial_basis=list(basis),**saved);break
        records.append(dict(index=index,**prefix,letter_count=len(rows),tree=proof,tree_stats=stats,
            rows_sha256=sha256(json.dumps([list(r) for r,f in rows],separators=(',',':')).encode()).hexdigest(),
            flags_sha256=sha256(json.dumps([f for r,f in rows],separators=(',',':')).encode()).hexdigest()))
        counts.update(stats);counts['prefixes']+=1;counts['literal_letters']+=len(rows)
    status='depth11_candidate_not_exclusion' if candidate else ('complete_range_independently_checked_QA_only' if start else 'complete_independently_checked_QA_only')
    if candidate is None:assert len(records)==len(scope['prefixes'])-start
    roots=['c1_word_staircase_letter_generator.py','check_c1_word_staircase.py','basis_column_staircase.py',
        'check_basis_column_staircase.py','BASIS_COLUMN_REACHING_PRUNING.md','basis_column_reaching_audit.json',
        'LOCAL_EQUALITY_FLAG.md','local_equality_flag_audit.json','FEW_GRAPH_FIRST_PAIR_CERTIFICATES.md',
        'small_first_third_inventory.json']
    out=dict(status=status,id=name,parameter=[13,9,1],target_ac=12,counts=dict(counts),prefixes=records,candidate=candidate,
        complete_scope=candidate is None and start==0,complete_range=candidate is None,range_start=start,
        total_native_prefixes=len(scope['prefixes']),candidate_format='dense supplier-group indices',no_authoritative_exclusion=True,no_new_numerical_extremum=True,
        scope='Complete graph quotient and independent literal/rational flag checks. Authoritative adoption still requires immutable packaging and isolated byte-identical regeneration; candidates require all original automaton checks.',
        source_sha256={Path(__file__).name:digest(Path(__file__)),'probe_full_supplier_image_quotient.py':digest(HERE/'probe_full_supplier_image_quotient.py'),file:digest(HERE/file),af:digest(HERE/af),
            parentpath.name:digest(parentpath),'GRAPH_FIRST_TRANSPORTS.md':digest(HERE/'GRAPH_FIRST_TRANSPORTS.md'),
            **{n:digest(HERE/n) for n in ['image_supplier_staircase.py','check_image_supplier_staircase.py',
                'supplier_image_propagation.py','check_supplier_image_propagation.py','SUPPLIER_IMAGE_PROPAGATION.md',
                'supplier_image_controls_audit_20261011.json','supplier_image_horizon_audit_20261011.json',
                'product_supplier_staircase.py','product_supplier_staircase_v2.py','product_supplier_staircase_v3.py','check_product_supplier_staircase.py','supplier_escape_words.py','check_supplier_escape_words.py',
                'SUPPLIER_ESCAPE_WORDS.md','supplier_products_audit_20261012.json','supplier_product_extensions_audit_20261012.json','supplier_escape_words_v2.py','supplier_triples_v2_audit_20261012.json','supplier_escape_words_v3.py','supplier_triples_v3_audit_20261012.json','split_product_supplier_staircase.py','check_split_product_supplier_staircase.py','obligatory_supplier_split.py','check_obligatory_supplier_split.py','OBLIGATORY_SUPPLIER_SPLIT_20261012.md','obligatory_supplier_split_audit_20261012.json','split_product_supplier_staircase_v2.py','obligatory_supplier_split_extended_audit_20261012.json','quotient_split_product_supplier_staircase.py','check_quotient_split_product_supplier_staircase.py','flag_stabilizer_quotient.py','check_flag_stabilizer_quotient.py','FLAG_STABILIZER_QUOTIENT_20261012.md','flag_stabilizer_quotient_audit_20261012.json','filtration_quotient_staircase_20261012.py','check_filtration_quotient_staircase_20261012.py','filtration_pool_exclusion_20261012.py','check_filtration_pool_exclusion_20261012.py','REAL_FILTRATION_POOL_20261012.md','check_candidate967_cover_tree_20261012_v2.py','b2_mixed_candidate967_literal_pool_20261012.json','candidate967_common_literal_word_cuts_20261012.json','candidate967_real_filtration_audit_20261012.json','candidate967_growth_cover_tree_audit_20261012.json','filtration_pool_exclusion_audit_20261012.json']}},
        root_source_sha256={n:digest(ROOT/n) for n in roots})
    with dest.open('w') as output_file:
        json.dump(out,output_file,separators=(',',':'));output_file.write('\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','root_source_sha256','prefixes','candidate')}),flush=True)
if __name__=='__main__':main()
