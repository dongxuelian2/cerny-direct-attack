"""Complete binary active field rows for D125/E6,E26, with 36/27 masks."""
from pathlib import Path
from itertools import product,permutations,combinations
from collections import Counter
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));K={1,2}
def rows(fields,protected,targets):
    options=[]
    for inputs,outputs in zip(map(set,fields['atom_inputs']),targets):
        outside=sorted(inputs-K);guards=sorted(inputs&K);choices=[]
        for values in permutations(sorted(outputs),len(outside)):
            assign=dict(zip(outside,values));blocked={assign[q] for q in outside if q in protected}
            for assigned in product(sorted(outputs-blocked),repeat=len(guards)):
                choices.append(assign|dict(zip(guards,assigned)))
        options.append(choices)
    for parts in product(*options):
        row=[-1]*13
        for part in parts:
            for q,t in part.items():row[q]=t
        assert min(row)>=0;yield tuple(row)
def single_cut(row,protected):
    power=list(range(13));outside=Q-K
    for depth in range(1,8):
        power=[row[t] for t in power];pre=[set() for _ in Q]
        for q,t in enumerate(power):pre[t].add(q)
        if any(len(X)>1 and X&protected for X in pre):return 'protected_P7_depth'+str(depth)
        if depth<=5 and any(len(X&outside)>1 for X in pre):return 'uncovered_P5_depth'+str(depth)
    return None
def image(S,row):return sum(1<<t for t in {row[q] for q in range(13) if S>>q&1})
def initial_mask(row,forms):
    allowed=set(forms);result=0
    for i,S in enumerate(forms):
        for depth in range(1,12):
            S=image(S,row)
            if S.bit_count()!=9 or not S&(1<<3) or (depth<=7 and S not in allowed):break
        else:result|=1<<i
    return result
def main():
    data=json.loads((ROOT/'b1_c14_nonsingleton_fourth_inventory.json').read_text())
    records=[z for z in data['records'] if z['D']==[1,2,5] and z['E'] in ([6],[2,6])]
    assert len(records)==2;report=[];lines=[];raw_hash=hashlib.sha256();kept_hash=hashlib.sha256()
    for z in records:
        pairs=[xy for p in z['pairs'] for xy in p['fourth_field_pairs']]
        active=sorted({i for xy in pairs for i in xy});positions={old:i for i,old in enumerate(active)}
        selected=[z['rows'][i] for i in active];protected=set(z['mandatory_through_seven'])
        targets=[set(a['targets']) for a in z['target_atoms']];mode=6 if z['E']==[6] else 26;em=sum(1<<q for q in z['E'])
        fibers=({0},{1,4},{1,2,5},set(z['E']))
        forms=sorted(sum(1<<q for q in S) for S in combinations(range(13),9) if 3 in S and all(len(set(S)&X)==1 for X in fibers))
        assert len(forms)==z['feasible_nine_sets'] and len(forms)<=64
        lines.append(f'13 {mode} {em} {len(selected)}');lines.append(str(len(targets)))
        for out in targets:lines.append(' '.join(map(str,[len(out),*sorted(out)])))
        field_reports=[]
        for i,(original,f) in enumerate(zip(active,selected)):
            for inp in f['atom_inputs']:lines.append(' '.join(map(str,[len(inp),*inp])))
            raw=sorted(rows(f,protected,targets));assert len(raw)==len(set(raw));hist=Counter();kept=0
            for row in raw:
                raw_hash.update((' '.join(map(str,[mode,em,i,*row]))+'\n').encode())
                reason=single_cut(row,protected)
                if reason:hist[reason]+=1;continue
                mask=initial_mask(row,forms)
                if not mask:hist['no_single_letter_initial_image']+=1;continue
                kept+=1;hist['kept']+=1
                kept_hash.update((' '.join(map(str,[mode,em,i,mask,*row]))+'\n').encode())
            field_reports.append(dict(field_row=i,original_fourth_field=original,raw_rows=len(raw),kept_rows=kept,counts=dict(sorted(hist.items()))))
        reduced_pairs=[[positions[x],positions[y]] for x,y in pairs]
        assert len(pairs)==len({tuple(xy) for xy in pairs})
        lines.append(str(len(reduced_pairs)));lines.extend(' '.join(map(str,xy)) for xy in reduced_pairs)
        raw_pairs=sum(field_reports[x]['raw_rows']*field_reports[y]['raw_rows'] for x,y in reduced_pairs)
        kept_pairs=sum(field_reports[x]['kept_rows']*field_reports[y]['kept_rows'] for x,y in reduced_pairs)
        report.append(dict(E=z['E'],mode=mode,E_mask=em,protected=sorted(protected),target_atoms=[sorted(X) for X in targets],
            initial_forms=forms,active_original_fields=active,field_rows=field_reports,original_field_pairs=pairs,
            normalized_field_pairs=reduced_pairs,raw_individual_rows=sum(f['raw_rows'] for f in field_reports),
            kept_individual_rows=sum(f['kept_rows'] for f in field_reports),raw_literal_pair_product=raw_pairs,
            kept_literal_pair_product=kept_pairs))
        print(json.dumps(dict(E=z['E'],fields=len(active),raw_rows=report[-1]['raw_individual_rows'],
            kept_rows=report[-1]['kept_individual_rows'],raw_pair_product=raw_pairs,kept_pair_product=kept_pairs)),flush=True)
    manifest=('\n'.join(lines)+'\n').encode();(ROOT/'d125_fourth_rows_fields.txt').write_bytes(manifest)
    names=[Path(__file__).name,'b1_c14_nonsingleton_fourth_inventory.json','b1_c14_nonsingleton_fourth_audit.json',
        'B1_C14_NONSINGLETON_D_FOURTH.md','D125_ROW_NORMALIZATION.md','MANDATORY_CORE_ISOLATION.md',
        'mandatory_core_isolation_audit.json','LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md']
    result=dict(status='complete_D125_active_fourth_literal_rows',parameter=[13,9,1],records=report,
        canonical_raw_rows_sha256=raw_hash.hexdigest(),canonical_kept_rows_sha256=kept_hash.hexdigest(),
        manifest_sha256=hashlib.sha256(manifest).hexdigest(),
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Every actual row in every binary-active fourth field for E6,E26. Empty domains exact; 36/27 literal masks. No coupled exclusion or unrestricted negative or F value.')
    (ROOT/'d125_fourth_rows_inventory.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
if __name__=='__main__':main()
