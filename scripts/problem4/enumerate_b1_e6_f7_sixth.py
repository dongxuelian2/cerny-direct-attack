"""Complete necessary kernels and G2 individual letters for E6/F7."""
from itertools import combinations,product,permutations
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
K={1,2};P={0,3,5,6,7};KEYS=('preA','preB','preC','preD','preE','preF')
def partitions(X,protected):
    if not X:yield [];return
    q=min(X)
    for old in partitions(X-{q},protected):
        yield [frozenset({q}),*old]
        for i,block in enumerate(old):
            enlarged=block|{q}
            if len(enlarged-K)>1 or enlarged&protected:continue
            yield [*old[:i],enlarged,*old[i+1:]]
def patterns(row,protected):
    groups=[set(row[key]) for key in KEYS];groups.append(set(range(13))-set().union(*groups))
    return [dict(fields=[[sorted(b) for b in part] for part in parts],kernel=[list(e) for e in sorted(
        {e for part in parts for block in part for e in combinations(sorted(block),2)})])
        for parts in product(*[[v for v in partitions(X,protected) if len(v)<=cap] for X,cap in zip(groups,[1,1,2,1,1,1,6])])]
def individual_letters(row):
    Q=set(range(13));U=P|{2};groups=[set(row[key]) for key in KEYS];groups.append(Q-set().union(*groups))
    targets=({3},{0},{1,4},{5},{6},{7},{2,8,9,10,11,12});options=[]
    for X,Y in zip(groups,targets):
        outside=sorted(X-{1});current=[]
        for outputs in permutations(sorted(Y),len(outside)):
            assign=dict(zip(outside,outputs))
            if 1 not in X:current.append(assign);continue
            forbidden={assign[q] for q in outside if q in U}
            for t in sorted(Y-forbidden):current.append(assign|{1:t})
        options.append(current)
    for parts in product(*options):
        row=[-1]*13
        for assign in parts:
            for x,t in assign.items():row[x]=t
        assert all(t>=0 for t in row);yield row
def main():
    parent=json.loads((ROOT/'b1_sixth_inventory.json').read_text(encoding='utf-8'));profiles=[]
    for z in parent['records']:
        if z['E']!=[6] or z['F']!=[7] or z['G'] not in ([2],[1,2],[1,8],[2,4],[1,2,8]):continue
        protected=P|({2} if z['G']==[2] else set())
        rows=[dict(parent_row=i,**{key:row[key] for key in KEYS},patterns=patterns(row,protected)) for i,row in enumerate(z['rows'])]
        pairs=[dict(original_third_rows=p['original_third_rows'],original_fourth_rows=p['original_fourth_rows'],
            original_fifth_rows=p['original_fifth_rows'],rows=[x,y],kernel_pairs=[list(ij) for ij in product(
                range(len(rows[x]['patterns'])),range(len(rows[y]['patterns'])))])
            for p in z['pairs'] for x,y in p['sixth_field_pairs']]
        records=[]
        if z['G']==[2]:
            for i,row in enumerate(z['rows']):
                counts=dict(full_letters=0,permutations=0,C_kernel=0,external_kernel=0);aggregate=0
                for word in individual_letters(row):
                    ker=[e for e in combinations(range(13),2) if word[e[0]]==word[e[1]]]
                    assert len(ker)<=1 and all(1 in e and not set(e)&protected for e in ker)
                    counts['full_letters']+=1;counts['permutations']+=not ker;counts['C_kernel']+=ker==[(1,4)]
                    counts['external_kernel']+=bool(ker and ker[0]!=(1,4))
                    aggregate=(aggregate+int.from_bytes(hashlib.sha256(bytes(word)).digest(),'big'))%(1<<256)
                records.append(dict(row=i,**counts,unordered_row_hash_sum=f'{aggregate:064x}'))
        profiles.append(dict(id=z['id'],G=z['G'],protected=sorted(protected),rows=rows,pairs=pairs,G2_individual_letter_controls=records))
    assert len(profiles)==5
    names=[Path(__file__).name,'b1_sixth_inventory.json','PROOF.md#problem4-b1-e6-f7-g2-exclusion','PROOF.md#problem4-b1-e6-f7-paired-sixth-exclusions']
    result=dict(status='necessary_E6_F7_sixth_kernel_inventory',parameter=[13,9,1],profiles=profiles,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='All original sixth field pairs and kernels; complete individual G2 letters. Necessary over-approximation only, no exclusion or F value asserted by generator.')
    (ROOT/'b1_e6_f7_sixth_kernel_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([dict(G=z['G'],field_pairs=len(z['pairs']),row_patterns=sum(len(r['patterns']) for r in z['rows']),
        kernel_pairs=sum(len(p['kernel_pairs']) for p in z['pairs']),G2_full_letters=sum(v['full_letters'] for v in z['G2_individual_letter_controls'])) for z in profiles]))
if __name__=='__main__':main()
