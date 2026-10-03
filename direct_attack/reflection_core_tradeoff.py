"""Integer-hole certificate and paid witnesses for the reflection core family."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def main():
    layers=[{()}]
    for length in range(8):
        new=set()
        for H0 in layers[-1]:
            H=set(H0);assert not {0,1}<=H
            new.add(tuple(sorted({1}|{1-h for h in H if h not in (0,1)})))
            new.add(tuple(h+1 for h in H0))
        layers.append(new)
    records=[]
    for M in list(range(3,81))+[127,256,512,1024,2048]:
        a=[M,M]+[M+1-q for q in range(2,M)]+[0];b=list(range(1,M))+[0,M]
        v3=[0]+[1]*(M-2)+[0]+[1]*(M-1)+[0]
        coeff=[0]+[2]+[1]*(M-2)
        records.append(dict(M=M,rows=[a,b],three_a_word=v3,three_a_support_coefficients=coeff,
                            short_avoid_word=[0,1,0,0,1,0,1,1,0] if M>=5 else None,
                            short_support_coefficients=[0]+[3 if j==M-2 else 2 for j in range(1,M)] if M>=5 else None,
                            reset_word=[0,1,0,1,1]*(M-2)+[0,1,0,1]))
    out=dict(abstract_hole_layers=[sorted([list(H) for H in layer]) for layer in layers],records=records,
             status='PROVED paper all M>=5: ordinary root avoidance9 but exact minimum three-a avoiding cost2M; positive-original-a stationary maximum cost restricted to its optimal max singular count3 equals2M, unrestricted support has cost<=max(9,M+1). All M>=3 original reset<=5M-6. Integer depth8 cut transfers to M>=17, small M5..16 all words<=8 checked independently. Not a general Cerny proof, formal or novelty claim.')
    (ROOT/'direct_attack/data/reflection_core_tradeoff.json').write_text(json.dumps(out,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(inputs=len(records),integer_hole_layers=[len(z) for z in layers],scope=out['status'])),flush=True)

if __name__=='__main__':main()
