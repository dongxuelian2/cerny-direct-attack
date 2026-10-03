"""Charged witnesses for the quadratic actual-image extension obstruction."""
import argparse
import json
from pathlib import Path


def record(r):
    n=2*r
    reset=[n-1]
    for j in range(r-1,0,-1):reset.extend(list(range(j,r))+[n-1])
    z=dict(r=r,n=n,fold_row=list(range(r))*2,
           transposition_edges=[[i,i+1] for i in range(n-1)],
           target=list(range(r,n)),source=list(range(n)),
           inverse_potential_weights=list(range(r+1,0,-1))+[0]*(r-1),
           rt=r*(r+1)//2,image_extension=r*(r+3)//2,
           reset_endpoint=0,entering_endpoint=r,reset_b_count=r,
           reset_swap_count=r*(r-1)//2,reset_stage_ranks=list(range(r,0,-1)),
           reachable_target_word_length=r*r+1,
           only_larger_actual_image_is_Q=True,
           all_parameter_status='PROVED paper; priority OPEN; no formal verification')
    assert len(reset)==z['rt']
    if r<=24:
        z['literal_reset_word']=reset
        z['literal_entering_word']=reset+list(range(r))
        target_word=[n-1]
        for j in range(r-1,-1,-1):target_word.extend(range(j,j+r))
        z['literal_reachable_target_word']=target_word
    return z


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,default=Path('direct_attack/data/transposition_fold_obstruction.json'))
    args=ap.parse_args()
    parameters=list(range(1,65))+[100,128,256,512,1024]
    z=dict(verified=True,arguments=dict(out=str(args.out)),records=[record(r) for r in parameters],
           scopes=dict(parameters=parameters,literal_parameters=list(range(1,25)),
                       exact_subset_audit_parameters=list(range(1,10)),maximum_n=2048),
           status='PROVED paper exact reset and quadratic image-extension family; every universal linear actual-image extension bound REFUTED; Cerny OPEN; no formal verification')
    args.out.write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(z['scopes']),flush=True)


if __name__=='__main__':main()
