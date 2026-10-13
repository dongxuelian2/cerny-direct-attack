"""Complete individual rows for E26/F7 seventh survivors."""
from pathlib import Path
from itertools import product,permutations,combinations
from collections import Counter
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));K={1,2}

def rows(fields,protected,targets):
    groups=list(map(set,fields['atom_inputs']));options=[]
    for inputs,outputs in zip(groups,targets):
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
        assert all(t>=0 for t in row);yield tuple(row)

def single_letter_cut(row,protected):
    protected_mask=sum(1<<q for q in protected);outside_mask=sum(1<<q for q in Q-K)
    power=list(range(13))
    for depth in range(1,8):
        power=[row[t] for t in power];pre=[0]*13
        for q,t in enumerate(power):pre[t]|=1<<q
        if any(x.bit_count()>1 and x&protected_mask for x in pre):
            return 'protected_P7',depth
        if depth<=5 and any((x&outside_mask).bit_count()>1 for x in pre):
            return 'uncovered_P5',depth
    return None,None

def image(S,row):return sum(1<<t for t in {row[q] for q in range(13) if S>>q&1})

def single_initial_masks(row,forms):
    allowed=set(forms);mask=0
    for i,initial in enumerate(forms):
        state=initial
        for depth in range(1,12):
            state=image(state,row)
            if state.bit_count()!=9 or not state&(1<<3) or (depth<=4 and state not in allowed):break
        else:mask|=1<<i
    return mask

def manifest(records):
    lines=[]
    for z in records:
        code=8 if z['G']==[8] else (18 if z['G']==[1,8] else 28);hm=sum(1<<q for q in z['H'])
        lines.append(f"13 {code} {hm} {len(z['rows'])}")
        lines.append(str(len(z['target_atoms'])))
        for atom in z['target_atoms']:lines.append(' '.join(map(str,[len(atom['targets']),*atom['targets']])))
        for row in z['rows']:
            for inputs in row['atom_inputs']:lines.append(' '.join(map(str,[len(inputs),*inputs])))
        pairs=[xy for p in z['pairs'] for xy in p['seventh_field_pairs']]
        assert len(pairs)==len({tuple(xy) for xy in pairs})
        lines.append(str(len(pairs)));lines.extend(' '.join(map(str,xy)) for xy in pairs)
    return '\n'.join(lines)+'\n'

def main():
    parent=json.loads((ROOT/'b1_e26_f7_seventh_inventory.json').read_text())
    records=[z for z in parent['records'] if any(p['seventh_field_pairs'] for p in z['pairs'])]
    assert [(z['G'],z['H']) for z in records]==[([8],[9]),([8],[1,9]),([8],[2,9]),([1,8],[9]),([2,8],[9]),([2,8],[1,8]),([2,8],[1,9])]
    report=[];dump_hash=hashlib.sha256();kept_hash=hashlib.sha256()
    for z in records:
        protected=set(z['mandatory_through_four']);targets=[set(t['targets']) for t in z['target_atoms']]
        assert protected>={0,3,5,7} and not protected&{2,6}
        fibers=({0},{1,4},{5},{2,6},{7},set(z['G']),set(z['H']))
        forms=[sum(1<<q for q in S) for S in combinations(range(13),9)
            if 3 in S and all(len(set(S)&X)==1 for X in fibers)]
        forms.sort();assert len(forms)==z['feasible_nine_sets']
        code=8 if z['G']==[8] else (18 if z['G']==[1,8] else 28);hm=sum(1<<q for q in z['H'])
        rows_report=[];hist=Counter();raw_total=kept_total=0
        for i,fields in enumerate(z['rows']):
            raw=sorted(rows(fields,protected,targets));assert len(raw)==len(set(raw))
            kept_count=0;counts=Counter()
            for row in raw:
                dump_hash.update((' '.join(map(str,[code,hm,i,*row]))+'\n').encode())
                reason,depth=single_letter_cut(row,protected)
                if reason:counts[f'{reason}_depth{depth}']+=1;continue
                initial_mask=single_initial_masks(row,forms)
                if not initial_mask:counts['no_single_letter_initial_image']+=1;continue
                kept_count+=1;counts['kept']+=1
                kept_hash.update((' '.join(map(str,[code,hm,i,initial_mask,*row]))+'\n').encode())
            raw_total+=len(raw);kept_total+=kept_count;hist.update(counts)
            rows_report.append(dict(field_row=i,raw_rows=len(raw),counts=dict(sorted(counts.items())),kept_rows=kept_count))
        pairs=[xy for p in z['pairs'] for xy in p['seventh_field_pairs']]
        raw_pairs=sum(rows_report[x]['raw_rows']*rows_report[y]['raw_rows'] for x,y in pairs)
        kept_pairs=sum(rows_report[x]['kept_rows']*rows_report[y]['kept_rows'] for x,y in pairs)
        report.append(dict(G=z['G'],H=z['H'],protected=sorted(protected),target_atoms=[sorted(t) for t in targets],
            initial_forms=forms,field_rows=rows_report,raw_individual_rows=raw_total,kept_individual_rows=kept_total,
            counts=dict(sorted(hist.items())),original_field_pairs=pairs,raw_normalized_row_pairs=raw_pairs,
            kept_normalized_row_pairs=kept_pairs))
        print(json.dumps(dict(G=z['G'],H=z['H'],raw_rows=raw_total,kept_rows=kept_total,raw_pairs=raw_pairs,
            kept_pairs=kept_pairs,counts=dict(hist))),flush=True)
    data=manifest(records).encode();(ROOT/'b1_e26_f7_seventh_rows_fields.txt').write_bytes(data)
    names=[Path(__file__).name,'b1_e26_f7_seventh_inventory.json','b1_e26_f7_seventh_audit.json',
        'PROOF.md#problem4-b1-e26-f7-seventh','PROOF.md#problem4-mandatory-core-isolation','mandatory_core_isolation_audit.json',
        'PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    result=dict(status='complete_E26_F7_seventh_individual_necessary_row_domain',parameter=[13,9,1],E=[2,6],
        alphabet='binary',records=report,canonical_raw_rows_sha256=dump_hash.hexdigest(),canonical_kept_rows_sha256=kept_hash.hexdigest(),
        manifest_sha256=hashlib.sha256(data).hexdigest(),
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Every individual K-covered mandatory-protected row in all seven typed seventh survivors. Exact overlap atoms and every single-letter initial mask. No coupled-row exclusion or model or extremal F value.')
    (ROOT/'b1_e26_f7_seventh_rows_inventory.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
if __name__=='__main__':main()
