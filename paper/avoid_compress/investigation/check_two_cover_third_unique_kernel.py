"""Literal mandatory families, atom rank bounds and all global kernel classes."""
from pathlib import Path
from itertools import product,combinations
import json,hashlib
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};H={0,1,2}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    premise_names=['small_first_third_audit.json','two_cover_unique_immediate_pair_audit.json','mandatory_core_isolation_audit.json']
    for n in premise_names:
        z=read(n);assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f
    inv=read('small_first_third_inventory.json');allS=[set(S) for S in combinations(range(13),9) if 3 in S]
    result=[];whole=[];binary=[];fields=classes=0
    for z in inv['records']:
        B,C,D=map(set,(z['B'],z['C'],z['D']))
        forms=[S for S in allS if all(len(S&X)==1 for X in (B,C,D))]
        assert len(forms)==z['feasible_nine_sets'];protected=set.intersection(*forms);K=H-protected
        if len(K)!=2:continue
        target={sig:{q for q in Q if tuple(int(q in X) for X in (A,B,C))==sig} for sig in product((0,1),repeat=3)}
        ranks=[];forced=[]
        for f in z['rows']:
            pre=list(map(set,(f['preA'],f['preB'],f['preC'])))
            inp={sig:{q for q in Q if tuple(int(q in X) for X in pre)==sig} for sig in target}
            assert all(not inp[sig] or target[sig] for sig in target)
            caps=[min(len(inp[sig]),len(target[sig])) for sig in target]
            kernels={p for sig in target if len(target[sig])==1 for p in combinations(sorted(inp[sig]),2)}
            assert caps==f['cell_capacity'] and kernels==set(map(tuple,f['forced_pairs']))
            ranks.append(sum(caps));forced.append(kernels);fields+=1
        choices=[]
        for e in combinations(range(13),2):
            if not set(e)&K or set(e)&protected:continue
            good=[i for i in range(len(z['rows'])) if ranks[i]>=12 and forced[i]<={e}]
            suppliers=[any(set(z['rows'][i][key])==X for i in good)
                       for key,X in [('preA',B),('preB',C),('preC',D)]]
            choices.append(dict(pair=list(e),retained_rows=good,suppliers=suppliers));classes+=1
        excluded=not any(all(c['suppliers']) for c in choices)
        bad=[p for p in z['binary_profile_pairs'] if min(ranks[i] for i in p)<12 or len(set().union(*(forced[i] for i in p)))>1]
        if excluded:whole.append(z['id'])
        if bad:binary.append(dict(id=z['id'],removed_parent_pairs=bad))
        result.append(dict(id=z['id'],mandatory=sorted(protected),residual_P5_cover=sorted(K),
                           maximum_letter_ranks=ranks,global_kernel_classes=choices,arbitrary_alphabet_excluded=excluded,
                           bad_binary_pairs=bad))
    names=[Path(__file__).name,'TWO_COVER_THIRD_UNIQUE_KERNEL_CUTS.md','small_first_third_inventory.json',*premise_names,
           'TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md','MANDATORY_CORE_ISOLATION.md','SMALL_FIRST_THIRD_ADMISSION.md',
           'THIRD_ENTRANCE_SPACE.md','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    report=dict(status='pass',parameter=[13,9,1],two_cover_geometries=len(result),exact_fields_reconstructed=fields,
                global_kernel_classes_checked=classes,all_inventory_unrestricted_excluded_ids=whole,
                all_inventory_binary_pair_cuts=binary,records=result,
                source_sha256={n:sha(ROOT/n) for n in names},
                scope='Necessary unique-kernel/rank/supplier cuts only on explicit two-state P5 cover records. Current counts require separate historical accounting.')
    (ROOT/'two_cover_third_unique_kernel_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','records','all_inventory_binary_pair_cuts')}),flush=True)
if __name__=='__main__':main()
