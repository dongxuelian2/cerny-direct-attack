"""Ternary family with max image extension 2n-1 and rt=P=n+2 for n>=8."""
import json
from pathlib import Path
from direct_attack.native_sparse_policy import profile
from direct_attack.one_fixed_family import construct


def main():
    root=Path('direct_attack/data/adjacent_swap_family');root.mkdir(exist_ok=True);records=[]
    for n in range(4,64):
        L=n-1;c=list(range(n));c[0],c[1]=c[1],c[0];rows=construct(n)+[c];p=profile(rows,True)
        assert p is not None and not p['truncated'];S=(1<<(L-2))|(1<<(L-1));P=(1<<L)|1|(1<<(L-2))
        p.update(target=S,larger_image=P,extension_word=[1]+[0]*(L-1)+[1]+[0,0,2]+[0]*(L-3),
                 reset_word=[1,1]+[0]*(L-1)+[1,1],scope='Paper theorem n>=8: max e=2n-1, rt=P=n+2; smaller n retained as boundary computations.')
        if n>=8:assert p['extension'][S]==p['max_extension']==2*n-1 and p['rt']==p['best_policy']==n+2
        assert p['reachable']==n*n-n+2
        (root/f'n{n}.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8');records.append(dict(n=n,e=p['max_extension'],rt=p['rt'],P=p['best_policy'],R=p['reachable']))
    (root/'summary.json').write_text(json.dumps(dict(records=records),indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(records),max_n=63)))


if __name__=='__main__':main()
