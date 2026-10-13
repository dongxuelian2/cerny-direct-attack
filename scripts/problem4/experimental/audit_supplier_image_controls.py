"""Exhaustive small controls and adversarial literal certificate tests."""
from collections import Counter,deque
import copy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from supplier_image_propagation import propagate_images
from check_supplier_image_propagation import literal_image,replay_images
HERE=Path(__file__).resolve().parent

def digest(p):return sha256(p.read_bytes()).hexdigest()
def callback(rows,size,protected):
    memo={}
    def images(m):
        if m not in memo:
            outputs={}
            for i,row in enumerate(rows):
                y=0
                for q in range(len(row)):
                    if m>>q&1:y|=1<<row[q]
                if y.bit_count()==size and y&protected==protected:outputs[y]=outputs.get(y,0)|(1<<i)
            memo[m]=outputs
        return memo[m]
    return images

def reachable(letters,S,H):
    known={S:0};todo=deque([S])
    while todo:
        m=todo.popleft();d=known[m]
        if d==H:continue
        for row in letters:
            y=literal_image(row,m)
            if y not in known:known[y]=d+1;todo.append(y)
    return known

def main():
    counts=Counter();domains=[]
    for n in (2,3):
        rows=list(product(range(n),repeat=n));allletters=(1<<len(rows))-1;local=Counter()
        for ai,a in enumerate(rows):
            for bi,b in enumerate(rows):
                local['ordered_binary_assignments']+=1
                for S in range(1,1<<n):
                    size=S.bit_count()
                    if size<2:continue
                    R=[sum(1<<j for j,row in enumerate(rows) if literal_image(row,S)==literal_image(actual,S)) for actual in (a,b)]
                    for A in range(1,1<<n):
                        if A==S or A&~S:continue
                        for horizon in (1,2,3):
                            known=reachable((a,b),S,horizon)
                            if any(m.bit_count()!=size or m&A!=A for m in known):continue
                            local['safe_instances']+=1
                            active,steps,forced=propagate_images(callback(rows,size,A),allletters,R,{S:0},horizon)
                            checked,checked_known=replay_images(rows,allletters,R,{S:0},horizon,size,A,steps)
                            assert (checked,checked_known)==(active,forced)
                            assert active>>ai&1 and active>>bi&1
                            assert all(m in known and known[m]<=d for m,d in forced.items())
                            local['proof_steps']+=len(steps);local['literal_letters_deleted']+=len(rows)-active.bit_count()
                            local['forced_images']+=len(forced)-1
        domains.append(dict(n=n,alphabet_size=2,**local));counts.update(local)
    rows=[(0,1,3,2),(0,3,1,2),(0,1,2,1)];S=7;A=1;R=[3];initial=7
    active,steps,known=propagate_images(callback(rows,3,A),initial,R,{S:0},2)
    assert active==3 and known[11]==1 and R[0].bit_count()==2
    assert replay_images(rows,initial,R,{S:0},2,3,A,steps)==(active,known)
    forced=next(i for i,r in enumerate(steps) if r['kind']=='force')
    deleted=next(i for i,r in enumerate(steps) if r['kind']=='delete')
    rejected=[]
    def reject(label,mutate):
        d=copy.deepcopy(steps);mutate(d)
        try:replay_images(rows,initial,R,{S:0},2,3,A,d)
        except (AssertionError,KeyError):rejected.append(label);return
        raise AssertionError('Accepted corrupted propagation certificate: '+label)
    reject('unknown source',lambda d:d[forced].__setitem__('source',8))
    reject('incorrect source depth',lambda d:d[forced].__setitem__('source_depth',1))
    reject('invalid required group',lambda d:d[forced].__setitem__('group',1))
    reject('wrong unanimous image',lambda d:d[forced].__setitem__('target',7))
    reject('shortened target depth',lambda d:d[forced].__setitem__('target_depth',0))
    reject('deleting an actual safe letter',lambda d:d[deleted].__setitem__('removed_hex','0x5'))
    reject('omitted unsafe letter',lambda d:d[deleted].__setitem__('removed_hex','0x0'))
    reject('using a horizon image to delete',lambda d:d[deleted].__setitem__('source_depth',2))
    def row_bad_group():
        d=copy.deepcopy(steps)
        try:replay_images(rows,initial,[4],{S:0},2,3,A,d)
        except AssertionError:return
        raise AssertionError('Accepted a nonunanimous supplier replacement')
    row_bad_group();rejected.append('nonunanimous supplier replacement')
    out=dict(status='pass',domains=domains,totals=dict(counts),nonunique_supplier_control=dict(required_group_size=2,
        actual_letters_retained=2,decoy_letter_deleted=1,forced_image=11,forced_depth=1),
        rejected_corruptions=rejected,adversarial_corruptions_rejected=len(rejected),
        no_geometry_exclusion=True,no_new_numerical_extremum=True,
        scope='Finite controls of the separately proved supplier-image rules; no extrapolation to extremal values.',
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,'supplier_image_propagation.py','check_supplier_image_propagation.py','PROOF.md#problem4-supplier-image-propagation']})
    dest=HERE/'supplier_image_controls_audit_20261011.json';assert not dest.exists()
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()
