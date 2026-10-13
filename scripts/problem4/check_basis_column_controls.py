"""Positive actual-letter controls and adversarial column proof records."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
from basis_column_staircase import column_premises
from check_basis_column_staircase import verify_column_step,check_tree
from check_basis_column_reaching import prefix_rows,integer_basis,pairs_forward
from check_c1_word_staircase import literal_pool
ROOT=Path(__file__).resolve().parent

def read(name):return json.loads((ROOT/name).read_text())
def digest(path):return sha256(path.read_bytes()).hexdigest()

def record_step(rows,basis,G,active):
    premise=column_premises(basis);constraints=set()
    for group in premise['equal']:constraints.update(combinations(group,2))
    for j in premise['one']:constraints.update(tuple(sorted((j,q))) for q in range(13) if q!=j)
    allowed=active
    if not premise['zero']:
        for i,(row,flag) in enumerate(rows):
            if allowed>>i&1 and any(row[p]==row[q] or tuple(sorted((row[p],row[q]))) in G for p,q in constraints):
                allowed &= ~(1<<i)
    def hash_mask(m):return sha256(m.to_bytes((len(rows)+7)//8,'little')).hexdigest()
    record=dict(**premise,before_size=active.bit_count(),before_sha256=hash_mask(active),
                deleted=[i for i in range(len(rows)) if active>>i&1 and not allowed>>i&1],
                after_size=allowed.bit_count(),after_sha256=hash_mask(allowed))
    assert verify_column_step(rows,basis,G,active,record)==allowed
    return record

def reject(fn):
    try:fn()
    except (AssertionError,KeyError,ValueError):return 1
    raise AssertionError('Invalid proof accepted')

def main():
    data=read('frontier_certificates.json')['certificates'];positive=[];rejected=0
    for z in data:
        if z['n']!=13:continue
        rows=tuple(map(tuple,z['rows']));S=set(z['S']);basisrows=integer_basis(prefix_rows(rows,S,13-len(S)))
        assert all(set(row)<={0,1} for row in basisrows)
        basis=[sum(x<<q for q,x in enumerate(row)) for row in basisrows]
        distances=pairs_forward(rows);G={pair for pair,d in distances.items() if d<=3}
        literal=[(row,0) for row in rows];record=record_step(literal,basis,G,3)
        assert record['zero']==[] and record['deleted']==[]
        positive.append(dict(parameter=[z[k] for k in ('n','s','r')],basis_rows=len(basis),
                             core_columns=record['one'],equal_classes=record['equal']))
        if len(positive)==1:
            p=record['one'][0];q=next(q for q in range(13) if q!=p)
            bad=list(rows[0]);bad[p]=bad[q]
            literal=literal+[(tuple(bad),0)]
            record=record_step(literal,basis,G,7);assert record['deleted']==[2]
            for key,value in [('zero',[0]),('one',[]),('equal',[]),('deleted',[]),
                              ('deleted',[0,2]),('before_sha256','0'*64),('after_sha256','0'*64)]:
                tamper=deepcopy(record);tamper[key]=value
                rejected+=reject(lambda t=tamper:verify_column_step(literal,basis,G,7,t))
    assert len(positive)==4 and rejected==7
    # Replay one complete existing-scope tree using independently regenerated
    # literal maps, then invalidate its prefix basis and domain digest.
    name='b2_in_c3_third5'
    saved=next(p for p in read(name+'_column_inventory.json')['prefixes'] if p['tree'].get('children'))
    scope=read('b2_column_scope.json');entry=next(z for z in scope['records'] if z['id']==name)
    parent=next(z for z in read('b2_column_parent_domains.json')['records'] if z['id']==name)
    c=next(z for z in parent['records'] if z['P1_mask']==saved['P1_mask'])
    p=dict(mandatory=parent['mandatory'],required_P3_edges=c['G'],fields=parent['fields'])
    view=dict(extra_pair=None,field_kernel_masks=c['field_kernel_masks']);B,C,D=map(set,(entry['B'],entry['C'],entry['D']))
    rows,G=literal_pool(p,view,saved['basis'],B,C,D)
    check=lambda t:check_tree(rows,saved['basis'],B,C,D,G,t)
    assert check(saved['tree'])==saved['tree_stats']
    for key,value in [('basis',[0,0]),('domain_sha256','0'*64),('required_group_sizes',[0])]:
        tamper=deepcopy(saved['tree']);tamper[key]=value;rejected+=reject(lambda t=tamper:check(t))
    tamper=deepcopy(saved['tree']);tamper['children'].pop()
    rejected+=reject(lambda:check(tamper))
    tamper=deepcopy(saved['tree']);tamper.update(reason='maximal_graph_not_SC',closed_set=list(range(13)))
    rejected+=reject(lambda:check(tamper))
    def find_column_node(node):
        if node['column_pruning'] is not None:return node
        for child in node.get('children',[]):
            result=find_column_node(child['node'])
            if result is not None:return result
        return None
    column_fixture=next(p for p in read(name+'_column_inventory.json')['prefixes']
                        if find_column_node(p['tree']) is not None)
    c=next(z for z in parent['records'] if z['P1_mask']==column_fixture['P1_mask'])
    p=dict(mandatory=parent['mandatory'],required_P3_edges=c['G'],fields=parent['fields'])
    view=dict(extra_pair=None,field_kernel_masks=c['field_kernel_masks'])
    fixture_rows,fixture_G=literal_pool(p,view,column_fixture['basis'],B,C,D)
    tamper=deepcopy(column_fixture['tree']);find_column_node(tamper)['column_pruning']['zero']=[0]
    rejected+=reject(lambda:check_tree(fixture_rows,column_fixture['basis'],B,C,D,fixture_G,tamper))
    # Zero-column positive record: report must retain the input domain, so
    # the enclosing tree rejects by the explicit zero-column contradiction.
    zero_basis=[sum(1<<q for q in range(9))];one_row=[(tuple(range(13)),0)]
    zero_record=record_step(one_row,zero_basis,set(),1)
    assert zero_record['zero']==[9,10,11,12] and zero_record['deleted']==[]
    result=dict(status='pass',actual_positive_column_controls=positive,positive_controls=6,
                rejected_invalid_records=rejected,zero_column_record_checked=True,
                source_sha256={name:digest(ROOT/name) for name in [Path(__file__).name,
                  'basis_column_staircase.py','check_basis_column_staircase.py','check_basis_column_reaching.py',
                  'basis_column_reaching_audit.json','frontier_certificates.json','check_c1_word_staircase.py',
                  'b2_column_scope.json','b2_column_parent_domains.json','b2_in_c3_third5_column_inventory.json']})
    (ROOT/'basis_column_controls_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)

if __name__=='__main__':main()
