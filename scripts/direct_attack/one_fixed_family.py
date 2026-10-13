"""One fixed point, one cycle, and a rank-three map: exact e maximum 2n-2."""
import json
from pathlib import Path
from direct_attack.native_sparse_policy import profile


def construct(n,r=None):
    L=n-1;r=L-2 if r is None else r
    assert n>=4 and 1<=r<L
    return [[(q+1)%L for q in range(L)]+[L],[L]*(L-1)+[r,0]]


def main():
    out=Path('scripts/direct_attack/data/one_fixed_family');out.mkdir(exist_ok=True);records=[]
    for n in range(4,64):
        L=n-1;c=profile(construct(n),True);assert c is not None and not c['truncated']
        S=(1<<(L-3))|(1<<(L-1));P=(1<<L)|1|(1<<(L-2))
        c.update(target=S,larger_image=P,extension_word=[1]+[0]*(L-1)+[1]+[0]*(L-1),
                 reset_word=[1,1]+[0]*(L-1)+[1,1],scope='Paper theorem max e=2n-2, rt=P=n+2 for n>=6; n5 is an explicit exception.')
        if n>=6:assert c['extension'][S]==c['max_extension']==2*n-2 and c['rt']==c['best_policy']==n+2
        (out/f'n{n}.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
        records.append(dict(n=n,max_extension=c['max_extension'],rt=c['rt'],P=c['best_policy'],images=c['reachable']))
    (out/'summary.json').write_text(json.dumps(dict(records=records),indent=2)+'\n',encoding='utf-8')
    scan=[]
    for n in [4,5,6,7,8,12,20,40,63]:
        values=[]
        for r in range(1,n-1):
            c=profile(construct(n,r));assert c is not None and not c['truncated']
            values.append([r,c['max_extension'],c['best_policy'],c['rt'],c['reachable']])
        scan.append(dict(n=n,values=values))
    Path('scripts/direct_attack/data/one_fixed_three_image_scan.json').write_text(json.dumps(scan,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(records),scan_parameters=sum(len(c['values']) for c in scan),max_n=63)))


if __name__=='__main__':main()
