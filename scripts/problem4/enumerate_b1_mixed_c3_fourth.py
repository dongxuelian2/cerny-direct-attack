"""Fourth-preimage admission in the fixed disjoint B1/C3/D2 profile."""
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parent
Q=set(range(13)); H={0,1,2}; A={3}; B={4}; C={0,1,5}; D={2,6}; J=set(range(7,13))
WORDS=['ABC','ABD','ACB','ACD','BAC','BAD','BCA','BCD']

def generate():
    old=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    old=next(v for v in old['records'] if v['id']=='b1_out_c5_third6')
    original=[tuple(z) for z in old['binary_profile_pairs']]
    assert original==[(0,7),(1,6),(1,7),(2,5),(2,7),(3,4),(3,5),(3,6),(3,7),(4,7),(5,6),(5,7),(6,7),(7,7)]
    records=[]
    for X in [set(),{0},{2},{0,1},{0,2},{0,1,2}]:
        E=X|{7}; sets=dict(A=A,B=B,C=C,D=D,E=E); rows=[]
        for i,word in enumerate(WORDS):
            for pd in 'ABCDE':
                keys=word+pd; inputs=[sets[k] for k in keys]
                if any(inputs[j]&inputs[k] for j,k in combinations(range(4),2)):continue
                residual=Q-set().union(*inputs)
                capacity=[min(len(v),len(t)) for v,t in zip(inputs+[residual],[A,B,C,D,J])]
                rows.append(dict(base_row=i,preimage_word=keys,capacity=capacity))
        pairs=[]
        for i,j in combinations_with_replacement(range(len(rows)),2):
            x,y=rows[i],rows[j]
            if tuple(sorted((x['base_row'],y['base_row']))) not in original:continue
            if 'E' not in (x['preimage_word'][3],y['preimage_word'][3]):continue
            if any(x['capacity'][k]+y['capacity'][k]<v for k,v in enumerate([1,1,3,2,6])):continue
            pairs.append([i,j])
        forms=[]
        for c,d,hole in product(sorted(C),sorted(D),sorted(J)):
            T=A|B|{c,d}|(J-{hole})
            if len(T&E)==1:forms.append(dict(c=c,d=d,hole=hole))
        admitted=sorted({tuple(sorted((rows[i]['base_row'],rows[j]['base_row']))) for i,j in pairs})
        records.append(dict(E=sorted(E),labelled_orbit_size=6*(2 if len(X&{0,1})==1 else 1),
            rows=rows,binary_fourth_profile_pairs=pairs,original_pairs=[list(z) for z in admitted],
            nine_set_forms=forms,geometric_exclusion='E meets both C and D' if X&{0,1} and 2 in X else None))
    return dict(status='necessary_inventory',parameter=[13,9,1],B=[4],C=[0,1,5],D=[2,6],
        original_pairs=[list(z) for z in original],records=records,
        source_sha256={v:hashlib.sha256((ROOT/v).read_bytes()).hexdigest() for v in
            [Path(__file__).name,'small_first_third_inventory.json']},
        scope='All fourth-preimage fields on the original fourteen binary third-profile pairs. Neither full transition-table enumeration nor an extremum.')

if __name__=='__main__':
    result=generate();(ROOT/'b1_mixed_c3_fourth_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([dict(E=z['E'],rows=len(z['rows']),fourth_pairs=len(z['binary_fourth_profile_pairs']),
        original_pairs=len(z['original_pairs']),forms=len(z['nine_set_forms'])) for z in result['records']]))
