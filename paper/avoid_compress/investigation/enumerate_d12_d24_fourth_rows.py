"""Complete independent raw rows for all binary D12/D24 fourth fields."""
from pathlib import Path
from itertools import product,permutations,combinations
import hashlib,json,math
ROOT=Path(__file__).resolve().parent;K={1,2}

def literal_rows(f,protected,targets):
    options=[]
    for inputs,outputs in zip(map(set,f['atom_inputs']),map(set,targets)):
        free=sorted(inputs-K);guards=sorted(inputs&K);choices=[]
        for values in permutations(sorted(outputs),len(free)):
            fixed=dict(zip(free,values));blocked={fixed[q] for q in free if q in protected}
            for v in product(sorted(outputs-blocked),repeat=len(guards)):
                choices.append(fixed|dict(zip(guards,v)))
        options.append(choices)
    for parts in product(*options):
        row=[-1]*13
        for part in parts:
            for q,t in part.items():row[q]=t
        assert min(row)>=0;yield tuple(row)

def main():
    parent=json.loads((ROOT/'b1_c14_nonsingleton_fourth_inventory.json').read_text())
    cases=[z for z in parent['records'] if z['D'] in ([1,2],[2,4]) and z['E'] in ([5],[1,5],[2,5])]
    assert len(cases)==6;reports=[];lines=[];digest=hashlib.sha256()
    for z in cases:
        mode=12 if z['D']==[1,2] else 24;em=sum(1<<q for q in z['E'])
        pairs=[xy for p in z['pairs'] for xy in p['fourth_field_pairs']]
        active=sorted({i for xy in pairs for i in xy});pos={i:j for j,i in enumerate(active)}
        targets=[a['targets'] for a in z['target_atoms']];protected=set(z['mandatory_through_seven'])
        forms=sorted(sum(1<<q for q in S) for S in combinations(range(13),9)
                     if 3 in S and all(len(set(S)&X)==1 for X in ({0},{1,4},set(z['D']),set(z['E']))))
        assert len(forms)==z['feasible_nine_sets']<=64
        assert all(all(len({q for q in range(13) if S>>q&1}&set(F))==1 for S in forms) for F in z['additional_covered_fibers'])
        lines.append(f'13 {mode} {em} {len(active)}');lines.append(str(len(targets)))
        for out in targets:lines.append(' '.join(map(str,[len(out),*out])))
        field_counts=[]
        for f,old in enumerate(active):
            row=z['rows'][old];expected=1
            for inp,out in zip(map(set,row['atom_inputs']),targets):
                lines.append(' '.join(map(str,[len(inp),*sorted(inp)])))
                o=len(out);t=len(inp-K);p=len((inp-K)&protected);g=len(inp&K)
                expected*=math.perm(o,t)*(o-p)**g if t<=o else 0
            raw=sorted(literal_rows(row,protected,targets))
            assert len(raw)==expected and all(a<b for a,b in zip(raw,raw[1:]))
            prefix=f'{mode} {em} {f} '
            for r in raw:digest.update((prefix+' '.join(map(str,r))+'\n').encode())
            field_counts.append(dict(field_row=f,original_fourth_field=old,raw_rows=expected))
        remapped=[[pos[x],pos[y]] for x,y in pairs]
        assert len(pairs)==len({tuple(p) for p in pairs})
        lines.append(str(len(remapped)));lines.extend(' '.join(map(str,p)) for p in remapped)
        report=dict(D=z['D'],E=z['E'],mode=mode,E_mask=em,protected=sorted(protected),target_atoms=targets,
            initial_forms=forms,additional_covered_fibers=z['additional_covered_fibers'],active_original_fields=active,
            field_rows=field_counts,original_field_pairs=pairs,normalized_field_pairs=remapped,
            raw_individual_rows=sum(f['raw_rows'] for f in field_counts),
            raw_literal_pair_product=sum(field_counts[x]['raw_rows']*field_counts[y]['raw_rows'] for x,y in remapped))
        reports.append(report);print(json.dumps({k:report[k] for k in ('D','E','raw_individual_rows','raw_literal_pair_product')}),flush=True)
    manifest=('\n'.join(lines)+'\n').encode();(ROOT/'d12_d24_fourth_rows_fields.txt').write_bytes(manifest)
    names=[Path(__file__).name,'D12_D24_ROW_COVER.md','b1_c14_nonsingleton_fourth_inventory.json',
        'b1_c14_nonsingleton_fourth_audit.json','B1_C14_NONSINGLETON_D_FOURTH.md','MANDATORY_CORE_ISOLATION.md',
        'mandatory_core_isolation_audit.json','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    result=dict(status='complete_D12_D24_raw_fourth_field_domain',parameter=[13,9,1],records=reports,
        canonical_raw_rows_sha256=digest.hexdigest(),manifest_sha256=hashlib.sha256(manifest).hexdigest(),
        raw_individual_rows=sum(z['raw_individual_rows'] for z in reports),
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Complete independent raw row domains only. Native independent algorithms check pure/coupled cuts; no exclusion or F value inferred here.')
    (ROOT/'d12_d24_fourth_rows_inventory.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
if __name__=='__main__':main()
