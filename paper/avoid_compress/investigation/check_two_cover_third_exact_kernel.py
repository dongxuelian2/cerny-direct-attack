"""Exact letter kernel classes and protected cover-image cuts on third fields."""
from pathlib import Path
from itertools import product,combinations
import json,hashlib
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};H={0,1,2}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    premises=['exact_atom_kernel_compatibility_audit.json','letter_image_short_pair_cover_audit.json',
              'two_cover_third_unique_kernel_audit.json','small_first_third_audit.json',
              'two_cover_unique_immediate_pair_audit.json','mandatory_core_isolation_audit.json']
    for n in premises:
        z=read(n);assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f
    inv=read('small_first_third_inventory.json');allS=[set(S) for S in combinations(range(13),9) if 3 in S]
    previous={z['id']:z for z in read(premises[2])['records']};records=[];whole=[];paircuts=[];fields=classes=0
    for z in inv['records']:
        B,C,D=map(set,(z['B'],z['C'],z['D']))
        forms=[S for S in allS if all(len(S&X)==1 for X in (B,C,D))]
        J=set.intersection(*forms);K=H-J
        if len(K)!=2:continue
        target={sig:{q for q in Q if tuple(int(q in X) for X in (A,B,C))==sig} for sig in product((0,1),repeat=3)}
        candidates=[e for e in combinations(range(13),2) if set(e)&K and not set(e)&J];typed=[]
        for f in z['rows']:
            pre=list(map(set,(f['preA'],f['preB'],f['preC'])))
            inp={sig:{q for q in Q if tuple(int(q in X) for X in pre)==sig} for sig in target}
            guard_targets={q:set().union(*(target[s] for s in inp if q in inp[s])) for q in K}
            permitted=any(guard_targets[q]-J for q in K)
            perm=all(len(inp[s])==len(target[s]) for s in target)
            singular=[]
            for e in candidates:
                atom=next((s for s in inp if set(e)<=inp[s]),None)
                if atom is not None and all(len(inp[s])-int(s==atom)<=len(target[s]) for s in target):singular.append(e)
            typed.append(dict(permutation_possible=perm and permitted,
                              possible_singular_kernels=[list(e) for e in singular] if permitted else [],
                              protected_image_forced=not permitted))
            fields+=1
        kernelclasses=[]
        for e in candidates:
            good=[i for i,f in enumerate(typed) if f['permutation_possible'] or list(e) in f['possible_singular_kernels']]
            singular=[i for i in good if list(e) in typed[i]['possible_singular_kernels']]
            suppliers=[any(set(z['rows'][i][key])==X for i in good)
                       for key,X in [('preA',B),('preB',C),('preC',D)]]
            old=next(c for c in previous[z['id']]['global_kernel_classes'] if c['pair']==list(e))
            assert set(good)<=set(old['retained_rows'])
            kernelclasses.append(dict(pair=list(e),retained_rows=good,singular_rows=singular,suppliers=suppliers));classes+=1
        excluded=not any(all(c['suppliers']) and c['singular_rows'] for c in kernelclasses)
        bad=[p for p in z['binary_profile_pairs'] if not any(set(p)<=set(c['retained_rows']) and set(p)&set(c['singular_rows']) for c in kernelclasses)]
        assert set(map(tuple,previous[z['id']]['bad_binary_pairs']))<=set(map(tuple,bad))
        if excluded:whole.append(z['id'])
        if bad:paircuts.append(dict(id=z['id'],removed_parent_pairs=bad))
        records.append(dict(id=z['id'],mandatory=sorted(J),residual_P5_cover=sorted(K),fields=typed,
                            global_kernel_classes=kernelclasses,arbitrary_alphabet_excluded=excluded,bad_binary_pairs=bad))
    assert (len(records),fields,classes)==(43,311,765)
    names=[Path(__file__).name,'EXACT_ATOM_KERNEL_COMPATIBILITY.md','small_first_third_inventory.json',*premises,
           'LETTER_IMAGE_SHORT_PAIR_COVER.md','TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md',
           'TWO_COVER_THIRD_UNIQUE_KERNEL_CUTS.md','MANDATORY_CORE_ISOLATION.md','SMALL_FIRST_THIRD_ADMISSION.md',
           'THIRD_ENTRANCE_SPACE.md','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    report=dict(status='pass',parameter=[13,9,1],two_cover_geometries=len(records),exact_fields_reconstructed=fields,
                global_kernel_classes_checked=classes,all_inventory_unrestricted_excluded_ids=whole,
                all_inventory_binary_pair_cuts=paircuts,records=records,
                source_sha256={n:sha(ROOT/n) for n in names},
                scope='Exact letter atom/kernel compatibility plus protected-image cover cuts, only on explicit two-cover records. Retained automaton classes are necessary overapproximations.')
    (ROOT/'two_cover_third_exact_kernel_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','records','all_inventory_binary_pair_cuts')}),flush=True)
if __name__=='__main__':main()
