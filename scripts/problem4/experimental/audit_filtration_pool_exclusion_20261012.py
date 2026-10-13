"""Controls on full-pool embeddings; no prescribed image-supplier assumptions."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from filtration_pool_exclusion_20261012 import certificate
from check_filtration_pool_exclusion_20261012 import check_certificate
HERE=Path(__file__).resolve().parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    dest=HERE/'filtration_pool_exclusion_audit_20261012.json';assert not dest.exists()
    pn='b2_mixed_candidate967_literal_pool_20261012.json';p=json.loads((HERE/pn).read_text())['candidate']
    rows=p['rows'];active=(1<<len(rows))-1;S=p['basis'][0];base=certificate(rows,active,S);assert base
    result=check_certificate(rows,active,S,base);assert result==dict(active_letters=406,filtration_action_checks=4466,cover_nodes=103)
    positives=[result]
    for r,a in [(list(reversed(rows)),active),(rows,active&~(1<<405))]:
        proof=certificate(r,a,S);assert proof;positives.append(check_certificate(r,a,S,proof))
    rejected=[]
    def test(label,change):
        proof=deepcopy(base);other=dict(rows=deepcopy(rows),active=active,S=S);change(proof,other)
        try:check_certificate(other['rows'],other['active'],other['S'],proof)
        except (AssertionError,KeyError):rejected.append(label)
        else:raise AssertionError('Accepted invalid complete-pool embedding: '+label)
    test('missing active literal',lambda d,o:d['transport'].pop())
    test('duplicated saved image',lambda d,o:d['transport'][1].__setitem__(1,d['transport'][0][1]))
    test('invalid saved index',lambda d,o:d['transport'][0].__setitem__(1,406))
    test('wrong pool digest',lambda d,o:d['artifact_sha256'].__setitem__(pn,'0'*64))
    test('wrong filtration digest',lambda d,o:d['artifact_sha256'].__setitem__('candidate967_real_filtration_audit_20261012.json','0'*64))
    test('wrong cover digest',lambda d,o:d['artifact_sha256'].__setitem__('candidate967_growth_cover_tree_audit_20261012.json','0'*64))
    test('changed literal action',lambda d,o:o['rows'][0].__setitem__(0,(o['rows'][0][0]+1)%13))
    test('wrong initial image',lambda d,o:o.update(S=S^1))
    assert certificate(rows,0,S) is None and certificate(rows,active,S^1) is None
    assert certificate(rows+[[0]*13],(active&~1)|(1<<406),S) is None
    out=dict(status='pass',positive_embeddings=positives,corruptions_rejected=rejected,inapplicable_controls=3,
        fixed_image_supplier_domains_required=False,depth_twelve_safety_required=False,
        complete_original_flag_path_replay=False,no_geometry_exclusion=True,no_new_numerical_extremum=True,
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,'filtration_pool_exclusion_20261012.py',
            'check_filtration_pool_exclusion_20261012.py','PROOF.md#problem4-real-filtration-pool-20261012',pn,
            'candidate967_real_filtration_audit_20261012.json','candidate967_growth_cover_tree_audit_20261012.json',
            'check_candidate967_cover_tree_20261012_v2.py']})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
