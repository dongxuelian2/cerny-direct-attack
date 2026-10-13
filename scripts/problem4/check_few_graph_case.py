"""Independent full graph, labelled first-pair, literal map and flag check."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse,json
from check_b1_b2_inverse_union import verify_geometry
from check_b3_staircase import permute_mask
from check_c1_word_staircase import literal_pool
from check_basis_column_staircase import check_tree
ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
def digest(path):return sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('id');ap.add_argument('--prefix',type=int);ap.add_argument('--scope',required=True);args=ap.parse_args()
    suffix='' if args.prefix is None else '_prefix'+str(args.prefix)
    scope=read(args.scope)
    assert scope['parameter']==[13,9,1] and scope['target_ac']==12
    file=args.id+'_'+scope['output_tag']+'_inventory'+suffix+'.json';data=read(file)
    for obj in (data,scope):
        for name,h in obj['source_sha256'].items():assert digest(ROOT/name)==h,name
    baseline=read(scope['baseline']);cp=read(scope['checkpoint'])
    assert digest(ROOT/scope['baseline'])==cp['source_sha256']['active_research.json']
    assert baseline['current_auxiliary_audit']==scope['checkpoint']
    for name,h in cp['source_sha256'].items():
        if name in scope['source_sha256'] and name!='active_research.json':
            assert digest(ROOT/name)==h,name
    report=read('basis_column_reaching_audit.json');assert report['status']=='pass'
    for name,h in report['source_sha256'].items():assert digest(ROOT/name)==h,name
    parents=read(scope['parent_domains'])
    for name,h in parents['historical_source_bindings'].items():assert digest(ROOT/name)==h,name
    entry=next(z for z in scope['records'] if z['id']==args.id)
    parent=next(z for z in parents['records'] if z['id']==args.id)
    z=next(z for z in read('small_first_third_inventory.json')['records'] if z['id']==args.id)
    ns=next(z for z in read('three_cover_atom_kernel_inventory.json')['records'] if z['id']==args.id)
    native=verify_geometry(parent,z,ns);assert native==entry['parent_domain']
    B,C,D=map(set,(z['B'],z['C'],z['D']));controls=[{0,1,2},{3},B,C,D,set(parent['mandatory'])]
    keep={c['P1_mask']:c for c in parent['records'] if c['reason']=='retained_overapproximation'}
    assert keep and [c['P1_mask'] for c in entry['classes']]==sorted(keep)
    frames={};expected=[]
    for c in entry['classes']:
        G=set(map(tuple,keep[c['P1_mask']]['G']))
        F=[set(S) for S in combinations(range(13),9) if 3 in S and all(len(set(S)&X)==1 for X in (B,C,D)) and not any(set(e)<=set(S) for e in G)]
        assert c['G']==keep[c['P1_mask']]['G'] and c['frames']==[sorted(S) for S in F]
        frames[c['P1_mask']]=F
        expected.extend((c['P1_mask'],i,j) for i in range(len(F)) for j in range(len(F)) if i!=j)
    assert [(t['P1_mask'],*t['pair']) for t in entry['transports']]==expected
    multiplicities=Counter();perms=set()
    representatives={(p['P1_mask'],tuple(p['basis'])):p for p in entry['prefixes']}
    assert len(representatives)==len(entry['prefixes'])
    for t in entry['transports']:
        p=tuple(t['permutation']);assert set(p)==set(range(13));g=t['P1_mask'];target=t['target_P1'];basis=tuple(t['basis'])
        assert target in keep and permute_mask(g,p)==target
        if p not in perms:
            assert all({p[q] for q in X}==X for X in controls)
            for f in parent['fields']:
                for key in ('preA','preB','preC'):assert {p[q] for q in f[key]}==set(f[key])
                assert sorted(permute_mask(mask,p) for mask in f['compatible_kernel_masks'])==f['compatible_kernel_masks']
            perms.add(p)
        assert {tuple(sorted((p[u],p[v]))) for u,v in keep[g]['G']}==set(map(tuple,keep[target]['G']))
        for old,new in zip(keep[g]['field_kernel_masks'],keep[target]['field_kernel_masks']):assert sorted(permute_mask(mask,p) for mask in old)==new
        assert tuple(sum(1<<p[q] for q in frames[g][i]) for i in t['pair'])==basis and (target,basis) in representatives
        multiplicities[(target,basis)]+=1
    assert set(multiplicities)==set(representatives)
    for key,prefix in representatives.items():assert prefix['multiplicity']==multiplicities[key]
    indices=list(range(len(entry['prefixes']))) if args.prefix is None else [args.prefix]
    assert [p['index'] for p in data['prefixes']]==indices
    total=Counter();maximum=0
    for saved in data['prefixes']:
        index=saved['index'];prefix=entry['prefixes'][index]
        for key in ('P1_mask','basis','multiplicity'):assert saved[key]==prefix[key]
        c=keep[prefix['P1_mask']];p=dict(mandatory=parent['mandatory'],required_P3_edges=c['G'],fields=parent['fields'])
        view=dict(extra_pair=None,field_kernel_masks=c['field_kernel_masks'])
        rows,G=literal_pool(p,view,prefix['basis'],B,C,D)
        assert len(rows)==saved['letter_count']
        assert sha256(json.dumps([list(r) for r,f in rows],separators=(',',':')).encode()).hexdigest()==saved['rows_sha256']
        assert sha256(json.dumps([f for r,f in rows],separators=(',',':')).encode()).hexdigest()==saved['flags_sha256']
        stats=check_tree(rows,prefix['basis'],B,C,D,G,saved['tree']);assert stats==saved['tree_stats']
        total.update(stats);total['prefixes']+=1;total['literal_letters']+=len(rows)
        maximum=max(maximum,max(int(k[6:]) for k,v in stats.items() if k.startswith('depth_') and v))
        if (index+1)%8==0:print(json.dumps(dict(id=args.id,independent_prefix=index+1,total=len(entry['prefixes']))),flush=True)
    assert dict(total)==data['stats']
    status='pass' if args.prefix is None else 'one_prefix_only'
    assert data['status']==('complete_necessary_exclusion_inventory' if args.prefix is None else 'one_prefix_only')
    assert data['new_exclusions']==([args.id] if args.prefix is None else [])
    sources=[Path(__file__).name,file,args.scope,scope['parent_domains'],scope['baseline'],scope['checkpoint'],
             'check_basis_column_staircase.py','check_c1_word_staircase.py','check_b3_staircase.py','check_b1_b2_inverse_union.py',
             'small_first_third_inventory.json','three_cover_atom_kernel_inventory.json','PROOF.md#problem4-basis-column-reaching-pruning',
             'basis_column_reaching_audit.json','PROOF.md#problem4-local-equality-flag','local_equality_flag_audit.json']
    result=dict(status=status,parameter=[13,9,1],id=args.id,global_classes=len(keep),labelled_first_pairs=len(expected),
                canonical_prefixes=len(entry['prefixes']),checked_prefixes=len(data['prefixes']),maximum_basis_depth=maximum,
                tree_counts=dict(total),native_domain= native,new_excluded_third_ids=data['new_exclusions'],
                new_numerical_F_value=False,source_sha256={name:digest(ROOT/name) for name in sources})
    output=ROOT/(args.id+'_'+scope['output_tag']+'_audit'+suffix+'.json');assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)

if __name__=='__main__':main()
