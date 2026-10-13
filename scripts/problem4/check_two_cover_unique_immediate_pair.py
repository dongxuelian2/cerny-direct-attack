"""Complete n4 compression/cover controls and literal FP two-pair sequences."""
from pathlib import Path
from itertools import product,combinations
import hashlib,json
from check_finite_independent_image_trap import forward_pair,reachable
ROOT=Path(__file__).resolve().parent

def main():
    sequences=0;per_n=[]
    for n in range(4,14):
        Q=set(range(n));pairs=list(combinations(range(n),2));count=0
        for e1 in pairs:
            for e2 in pairs:
                if e1==e2:continue
                x=min(set(e2)-set(e1));y=min(Q-set(e1)-{x});T1=Q-{x,y}
                omitted=sorted(Q-set(e2))[:2];T2=Q-set(omitted)
                assert len(T1)==len(T2)==n-2 and set(e1)<=T1 and not set(e2)<=T1 and set(e2)<=T2
                count+=1
        assert count==len(pairs)*(len(pairs)-1);sequences+=count;per_n.append(dict(n=n,ordered_two_pair_sequences=count))
    pool=list(product(range(4),repeat=4));pairs=list(combinations(range(4),2));tested=multi=compressed=qualified=0;boundary=None
    for rows in product(pool,repeat=2):
        tested+=1;ds={p:forward_pair(p,rows) for p in pairs};P1={p for p,d in ds.items() if d==1}
        if len(P1)>=2:
            multi+=1
            for d in ds.values():
                if d is not None:assert d<=5;compressed+=1
        if all(d is not None for d in ds.values()) and ds[(2,3)]>5:
            qualified+=1;assert len(P1)==1
            assert any(len(S)==1 for S in reachable(set(range(4)),rows))
            if boundary is None:boundary=dict(rows=rows,P1=[list(p) for p in sorted(P1)],outside_K_pair_distance=ds[(2,3)])
    assert tested==65536 and qualified==24
    rows=[(1,2,0),(0,0,0)];K={0,1}
    assert all(set(p)&K for p in combinations(range(3),2))
    assert len([p for p in combinations(range(3),2) if forward_pair(p,rows)==1])==3
    assert any(len(S)==1 for S in reachable(set(range(3)),rows))
    names=[Path(__file__).name,'PROOF.md#problem4-two-cover-unique-immediate-pair','check_finite_independent_image_trap.py','PROOF.md#problem4-binary-obstruction-proof']
    report=dict(status='pass',uniform_state_range='n>=4',alphabet='arbitrary finite',known_refinement_application=True,
        complete_n4_ordered_binary_alphabets=tested,alphabets_with_multiple_immediate_pairs=multi,
        compressible_pairs_checked_against_five_bound=compressed,qualifying_sync_fixed_cover_controls=qualified,
        literal_two_pair_sequences=sequences,sequence_stats=per_n,structural_boundary=boundary,
        n3_essential_boundary=dict(rows=rows,K=sorted(K),outside_K_size=1,immediate_pairs=3,synchronizing=True),
        source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
        scope='Direct credited compression-refinement consequence, complete n4 controls and literal pair-sequence construction. No new F value or priority claim.')
    (ROOT/'two_cover_unique_immediate_pair_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','sequence_stats','structural_boundary')}),flush=True)
if __name__=='__main__':main()
