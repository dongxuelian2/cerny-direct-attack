"""Local positive flag trees and deliberately corrupted branch certificates."""
from pathlib import Path
import copy,hashlib,json
from check_c1_word_staircase import literal_pool,check_tree
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    data=read('b2_c5_first_pair_inventory.json');record=next(z for z in read('b1_b2_inverse_union_inventory.json')['records'] if z['id']==data['id'])
    B,C,D=map(set,(data['B'],data['C'],data['D']));cases=[]
    for index in (0,1):
        entry=data['prefixes'][index];c=next(c for c in record['records'] if c['P1_mask']==entry['P1_mask'])
        parent=dict(mandatory=record['mandatory'],required_P3_edges=c['G'],fields=record['fields']);view=dict(extra_pair=None,field_kernel_masks=c['field_kernel_masks'])
        rows,G=literal_pool(parent,view,entry['basis'],B,C,D)
        assert check_tree(rows,entry['basis'],B,C,D,G,entry['tree'])==entry['tree_stats'];cases.append((entry,rows,G))
    mutations=[]
    def alter(label,fn,index=0):
        e,rows,G=cases[index];tree=copy.deepcopy(e['tree']);fn(tree);mutations.append((label,e,rows,G,tree))
    def missing_leaf(node):
        if node['reason']=='missing_required_group':return node
        for child in node.get('children',[]):
            answer=missing_leaf(child['node'])
            if answer is not None:return answer
        return None
    alter('wrong_basis',lambda t:t['basis'].__setitem__(0,t['basis'][0]^1))
    alter('omitted_child',lambda t:t['children'].pop())
    alter('duplicate_child',lambda t:t['children'].append(copy.deepcopy(t['children'][0])))
    alter('wrong_domain_digest',lambda t:t.__setitem__('domain_sha256','0'*64))
    alter('wrong_supplier_size',lambda t:t['required_group_sizes'].__setitem__(0,t['required_group_sizes'][0]+1))
    alter('wrong_missing_group',lambda t:missing_leaf(t).__setitem__('missing_group',(missing_leaf(t)['missing_group']+1)%len(missing_leaf(t)['required_group_sizes'])))
    alter('changed_next_image',lambda t:t['children'][0].__setitem__('next_image',t['children'][0]['next_image']^1))
    alter('false_no_growth',lambda t:t.__setitem__('reason','no_growth'))
    alter('empty_closed_set',lambda t:t.__setitem__('closed_set',[]),1)
    rejected=[]
    for label,e,rows,G,tree in mutations:
        try:check_tree(rows,e['basis'],B,C,D,G,tree)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('Accepted corruption: '+label)
    assert len(rejected)==9
    sources=[Path(__file__).name,'check_c1_word_staircase.py','check_b3_staircase.py','b2_c5_first_pair_inventory.json','b1_b2_inverse_union_inventory.json']
    result=dict(status='pass',positive_flag_controls=2,adversarial_controls_rejected=9,rejected=rejected,source_sha256={n:sha(ROOT/n) for n in sources},scope='Local branch, domain, supplier and closed-set checks only; no F theorem.')
    (ROOT/'b2_c5_first_pair_controls_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}))
if __name__=='__main__':main()
