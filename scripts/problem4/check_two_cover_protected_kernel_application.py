"""Literal third-entrance premises for the uniform one-count kernel obstruction."""
from pathlib import Path
from itertools import combinations
import json,hashlib
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};H={0,1,2}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    reports=['two_cover_protected_kernel_graph_audit.json','two_cover_third_exact_kernel_audit.json',
             'small_first_third_audit.json','mandatory_core_isolation_audit.json']
    for n in reports:
        z=read(n);assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f
    inv=read('small_first_third_inventory.json')['records'];allS=[set(S) for S in combinations(range(13),9) if 3 in S]
    records=[];whole=[]
    for z in inv:
        B,C,D=map(set,(z['B'],z['C'],z['D']))
        forms=[S for S in allS if all(len(S&X)==1 for X in (B,C,D))]
        protected=set.intersection(*forms);K=H-protected
        if len(K)!=2:continue
        if len(B)==2:E=B;target=3;key='preA';depth=10
        elif len(B)==1 and len(C)==2:E=C;target=next(iter(B));key='preB';depth=9
        elif len(B)==len(C)==1 and len(D)==2:E=D;target=next(iter(C));key='preC';depth=8
        else:continue
        assert target not in E and depth>=5 and all(len(S&E)==1 for S in forms)
        assert any(set(f[key])==E for f in z['rows'])
        records.append(dict(id=z['id'],B=z['B'],C=z['C'],D=z['D'],mandatory=sorted(protected),
                            residual_P5_cover=sorted(K),kernel=sorted(E),supplier_key=key,supplier_target=target,
                            one_count_prefix=depth,m=4,compression_lower_bound=12,required_prefix=5,
                            conservative_compression_threshold=12))
        whole.append(z['id'])
    names=[Path(__file__).name,'PROOF.md#problem4-two-cover-protected-kernel-obstruction',*reports,
           'small_first_third_inventory.json','PROOF.md#problem4-two-cover-unique-immediate-pair',
           'PROOF.md#problem4-mandatory-core-isolation','PROOF.md#problem4-small-first-third-admission','PROOF.md#problem4-third-entrance-space',
           'PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-second-entrance-fiber','PROOF.md#problem4-local-equality-flag']
    report=dict(status='pass',parameter=[13,9,1],all_inventory_unrestricted_excluded_ids=whole,
                all_inventory_binary_excluded_ids=whole,records=records,
                source_sha256={n:sha(ROOT/n) for n in names},
                scope='Uniform obstruction applied to explicit two-cover pair-entrance records only; current newly removed counts require historical accounting.')
    (ROOT/'two_cover_protected_kernel_application_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','records')}),flush=True)
if __name__=='__main__':main()
