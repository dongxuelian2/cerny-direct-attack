"""Literal labelled core/frame controls and exact singleton Boolean boundary."""
from pathlib import Path
from itertools import combinations,product
import json,hashlib
ROOT=Path(__file__).resolve().parent
Q=set(range(13))
def main():
    for n in ['two_cover_protected_kernel_graph_audit.json','local_equality_flag_audit.json','mandatory_core_isolation_audit.json']:
        z=json.loads((ROOT/n).read_text())
        if n=='local_equality_flag_audit.json':
            assert z['status']=='all_exact_controls_passed'
            assert hashlib.sha256((ROOT/'check_local_equality_flag.py').read_bytes()).hexdigest()==z['source_sha256']
        else:
            assert z['status']=='pass'
            for f,h in z['source_sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    boolean=[]
    for l in (4,5,6,7):
        rows=[]
        for c0,*v in product((0,1),repeat=l+1):
            if (8-l)*c0+sum(v)==1:rows.append((c0,*v))
        if l<=6:assert len(rows)==l and all(r[0]==0 and sum(r[1:])==1 for r in rows)
        else:assert len(rows)==8 and (1,*([0]*7)) in rows
        boolean.append(dict(outside_singletons=l,one_count_boolean_columns=len(rows),ordinary_complement_admitted=l==7))
    seven=0
    for core in combinations(range(13),7):
        C=set(core)
        for e in combinations(sorted(Q-C),2):
            for p in sorted(Q-C-set(e)):
                frames=[C|{p,q} for q in e]
                assert all(len(S)==9 for S in frames) and len({frozenset(S) for S in frames})==2
                assert set.intersection(*frames)==C|{p} and all(len(S&set(e))==1 for S in frames)
                # Two distinct fixed-size rows have linear rank exactly two.
                assert any((q in frames[0])!=(q in frames[1]) for q in Q);seven+=1
    assert seven==102960
    eight=fibers=0
    for core in combinations(range(13),8):
        C=set(core)
        for variables in combinations(sorted(Q-C),4):
            frames=[C|{q} for q in variables]
            masks=[sum(1<<q for q in S) for S in frames]
            allowed=[];count=0
            for mask in range(1<<13):
                if not all((mask&F).bit_count()==1 for F in masks):continue
                R={q for q in Q if mask>>q&1};count+=1
                if R&C:
                    if len(R)>1:continue # immediate collision incident to a protected core point
                elif len(R)>=3:continue # multiple immediate pairs, contrary to unique P1
                allowed.append(R)
            assert count==18 and {frozenset(R) for R in allowed}=={frozenset({q}) for q in C}
            eight+=1;fibers+=count
    assert eight==6435 and fibers==115830
    names=[Path(__file__).name,'PROOF.md#problem4-singleton-third-chain-unrestricted-exclusion',
           'PROOF.md#problem4-two-cover-protected-kernel-obstruction','two_cover_protected_kernel_graph_audit.json',
           'PROOF.md#problem4-local-equality-flag','local_equality_flag_audit.json','check_local_equality_flag.py','PROOF.md#problem4-mandatory-core-isolation',
           'mandatory_core_isolation_audit.json','PROOF.md#problem4-two-cover-unique-immediate-pair','PROOF.md#problem4-compression-cover-floor']
    result=dict(status='pass',parameter=[13,9,1],seven_core_pair_singleton_placements=seven,
                eight_core_four_variable_families=eight,all_masks_per_family=8192,
                literal_one_count_fibers=fibers,Boolean_controls=boolean,
                source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
                scope='Literal complete labelled controls for seven/eight-core span obstructions. No F maximum or general common-fiber assertion.')
    (ROOT/'singleton_core_span_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
