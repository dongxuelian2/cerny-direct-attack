"""Bijective, graph-preserving corruptions test the actual protection checks."""
import copy
from hashlib import sha256
import json
from pathlib import Path
from check_graph_quotient_scope import verify,move_edges,ROOT
HERE=Path(__file__).resolve().parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    name='b1_out_c3_third10';file=name+'_graph_quotient_scope.json';scope=read(HERE/file)
    parent=read(HERE/(name+'_inverse_probe.json'))
    z=next(z for z in read(ROOT/'small_first_third_inventory.json')['records'] if z['id']==name)
    tests=[]
    for output,label in ((3,'protected singleton'),(4,'first entrance singleton')):
        d=copy.deepcopy(scope);r=d['raw_classes'][0];p=r['permutation']
        i,j=p.index(output),p.index(12);p[i],p[j]=p[j],p[i]
        assert set(p)==set(range(13)) and move_edges(r['P1_mask'],p)==r['target_P1']
        try:verify(d,parent,z)
        except AssertionError:tests.append(label);continue
        raise AssertionError('Accepted a graph-preserving violation of '+label)
    out=dict(status='pass',rejected_bijective_graph_preserving_corruptions=tests,no_new_numerical_extremum=True,
        scope='Two adversarial tests of the actual protection checker; both preserve bijectivity and the P1 graph.',
        source_sha256={Path(__file__).name:digest(Path(__file__)),'check_graph_quotient_scope.py':digest(HERE/'check_graph_quotient_scope.py'),
            file:digest(HERE/file),name+'_inverse_probe.json':digest(HERE/(name+'_inverse_probe.json'))},
        root_source_sha256={'small_first_third_inventory.json':digest(ROOT/'small_first_third_inventory.json')})
    dest=HERE/(name+'_graph_transport_protection_audit.json');assert not dest.exists()
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','root_source_sha256')}),flush=True)
if __name__=='__main__':main()
