"""Stricter ordinary-set checker and corruptions of the finite cover proof."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from check_candidate967_cover_tree_20261012_v2 import check
HERE=Path(__file__).resolve().parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    dest=HERE/'candidate967_growth_cover_adversarial_audit_20261012.json';assert not dest.exists()
    saved='candidate967_growth_cover_tree_audit_20261012.json';pool='b2_mixed_candidate967_literal_pool_20261012.json'
    d=json.loads((HERE/saved).read_text());c=json.loads((HERE/pool).read_text())['candidate']
    assert d['status']=='pass' and d['complete_saved_pool_cover_exclusion'] and not d['complete_geometry_exclusion']
    rows=c['rows'];groups=d['required_groups'];assert groups==json.loads((HERE/'candidate967_real_filtration_audit_20261012.json').read_text())['growth_domains'];S={q for q in range(13) if c['basis'][0]>>q&1}
    assert check(rows,S,groups,d['clauses'],d['tree'])==d['counts']
    rejected=[]
    def test(label,change):
        clauses=deepcopy(d['clauses']);tree=deepcopy(d['tree']);other=dict(rows=rows,S=set(S),groups=deepcopy(groups))
        change(clauses,tree,other)
        try:check(other['rows'],other['S'],other['groups'],clauses,tree)
        except (AssertionError,KeyError):rejected.append(label)
        else:raise AssertionError('Accepted false cover certificate: '+label)
    test('missing first-supplier branch',lambda a,t,o:t['children'].pop())
    test('duplicate first-supplier branch',lambda a,t,o:t['children'].append(deepcopy(t['children'][0])))
    test('false empty required group terminal',lambda a,t,o:t.update(reason='missing_group',group=0))
    test('empty literal cut word',lambda a,t,o:a[0].update(word=[]))
    test('invented letter in cut word',lambda a,t,o:a[0].update(word=[len(rows)]))
    def too_long(a,t,o):
        z=next(z for z in a if z['kind']=='short_rank_word');z['word']=z['word']*7
    test('rank word beyond length six',too_long)
    def bad_unit(a,t,o):
        todo=[t]
        while todo:
            v=todo.pop()
            if v['units']:v['units'][0]['letter']=len(rows);return
            todo.extend(x['node'] for x in v.get('children',[]))
        raise AssertionError('No unit control exists')
    test('invalid unit propagation letter',bad_unit)
    test('empty compulsory domain',lambda a,t,o:o['groups'].__setitem__(0,[]))
    test('wrong initial image cardinality',lambda a,t,o:o['S'].remove(next(q for q in S if q!=3)))
    test('missing protected state',lambda a,t,o:o['S'].remove(3))
    out=dict(status='pass',prefix=967,conditional_pool=406,counts=d['counts'],distinct_forbidden_alphabets=len(d['clauses']),
        corruptions_rejected=rejected,complete_saved_pool_cover_exclusion=True,complete_original_flag_path_replay=False,
        no_geometry_exclusion=True,no_new_numerical_extremum=True,
        scope='Stricter finite saved-pool cover replay only; no complete native flag path or whole geometry exclusion.',
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,'check_candidate967_cover_tree_20261012_v2.py',saved,pool,'candidate967_real_filtration_audit_20261012.json','PROOF.md#problem4-real-filtration-pool-20261012']})
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
