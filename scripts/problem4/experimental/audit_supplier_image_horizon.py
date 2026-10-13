"""Extra controls isolate the horizon premise and improvement of seed depths."""
from hashlib import sha256
import json
from pathlib import Path
from audit_supplier_image_controls import callback
from supplier_image_propagation import propagate_images
from check_supplier_image_propagation import replay_images
HERE=Path(__file__).resolve().parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    rows=[(0,1,3,2),(0,3,1,2),(0,1,2,1)];S=7;T=11;R=[3]
    a,steps,known=propagate_images(callback(rows,3,1),7,R,{S:0},1)
    assert a==7 and known[T]==1 and all(r['kind']!='delete' for r in steps)
    assert replay_images(rows,7,R,{S:0},1,3,1,steps)==(a,known)
    a,steps,known=propagate_images(callback(rows,3,1),7,R,{S:0,T:2},3)
    assert a==3 and known[T]==1 and any(r['kind']=='force' and r['target']==T and r['target_depth']==1 for r in steps)
    assert replay_images(rows,7,R,{S:0,T:2},3,3,1,steps)==(a,known)
    # Every fact apart from using a source at the horizon is correct here.
    horizon_step=[dict(kind='delete',source=T,source_depth=2,removed_hex='0x4')]
    try:replay_images(rows,7,R,{S:0,T:2},2,3,1,horizon_step)
    except AssertionError:pass
    else:raise AssertionError('Accepted safety beyond the supplied horizon')
    empty_group_step=[dict(kind='force',source=S,source_depth=0,group=0,target=T,target_depth=1)]
    try:replay_images(rows,7,[0],{S:0},2,3,1,empty_group_step)
    except AssertionError:pass
    else:raise AssertionError('Accepted an empty existential supplier premise')
    out=dict(status='pass',horizon_one_keeps_three_letters=True,improved_existing_seed_depth=[2,1],
        valid_depth_premise_at_horizon_rejected=True,empty_required_group_rejected=True,
        no_geometry_exclusion=True,no_new_numerical_extremum=True,
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,'audit_supplier_image_controls.py',
            'supplier_image_propagation.py','check_supplier_image_propagation.py','PROOF.md#problem4-supplier-image-propagation']})
    dest=HERE/'supplier_image_horizon_audit_20261011.json';assert not dest.exists()
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
