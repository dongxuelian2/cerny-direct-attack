"""Complete prefix trees of one geometry; candidates never become negatives."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import argparse,json
from c1_word_staircase_letter_generator import pool
from basis_column_staircase import tree
ROOT=Path(__file__).resolve().parent

def read(name):return json.loads((ROOT/name).read_text())
def digest(path):return sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('id');ap.add_argument('--prefix',type=int);args=ap.parse_args()
    scope=read('b2_single_scope.json')
    for name,h in scope['source_sha256'].items():assert digest(ROOT/name)==h,name
    record=next(z for z in scope['records'] if z['id']==args.id)
    parent=next(z for z in read('b2_single_parent_domains.json')['records'] if z['id']==args.id)
    classes={c['P1_mask']:c for c in parent['records'] if c['reason']=='retained_overapproximation'}
    selected=list(enumerate(record['prefixes'])) if args.prefix is None else [(args.prefix,record['prefixes'][args.prefix])]
    entries=[];total=Counter();B,C,D=map(set,(record['B'],record['C'],record['D']))
    for index,prefix in selected:
        c=classes[prefix['P1_mask']];p=dict(mandatory=parent['mandatory'],required_P3_edges=c['G'],fields=parent['fields'])
        view=dict(extra_pair=None,field_kernel_masks=c['field_kernel_masks'])
        S,T=[{q for q in range(13) if m>>q&1} for m in prefix['basis']]
        rows,G=pool(p,view,S,T,B,C,D)
        print(json.dumps(dict(id=args.id,prefix=index,total=len(record['prefixes']),literal_letters=len(rows))),flush=True)
        proof,stats=tree(rows,prefix['basis'],B,C,D,G)
        entries.append(dict(index=index,**prefix,letter_count=len(rows),
                       rows_sha256=sha256(json.dumps([list(r) for r,f in rows],separators=(',',':')).encode()).hexdigest(),
                       flags_sha256=sha256(json.dumps([f for r,f in rows],separators=(',',':')).encode()).hexdigest(),
                       tree=proof,tree_stats=stats))
        total.update(stats);total['prefixes']+=1;total['literal_letters']+=len(rows)
    status='complete_necessary_exclusion_inventory' if args.prefix is None else 'one_prefix_only'
    sources=[Path(__file__).name,'b2_single_scope.json','b2_single_parent_domains.json','basis_column_staircase.py',
             'BASIS_COLUMN_REACHING_PRUNING.md','basis_column_reaching_audit.json','c1_word_staircase_letter_generator.py',
             'enumerate_c1_word_staircase.py','enumerate_b3_staircase.py','enumerate_b3_staircase_first.py']
    result=dict(status=status,parameter=[13,9,1],id=args.id,prefixes=entries,stats=dict(total),
                new_exclusions=[args.id] if args.prefix is None else [],
                source_sha256={name:digest(ROOT/name) for name in sources})
    suffix='' if args.prefix is None else '_prefix'+str(args.prefix)
    output=ROOT/(args.id+'_single_inventory'+suffix+'.json');assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=status,id=args.id,stats=dict(total))),flush=True)

if __name__=='__main__':main()
