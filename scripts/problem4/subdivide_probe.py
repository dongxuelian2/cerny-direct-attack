"""Finite edge-subdivision probes, with full ordinary-set checks of positives."""
import json
from pathlib import Path
from audit_small import bfs,strong
from synthesize_safe import nonmergeable_pairs

ROOT=Path(__file__).resolve().parent

def main():
    base=json.loads((ROOT/'formula_certificates.json').read_text())['certificates']
    records=[];tested=0
    requests={(10,7,2),(11,7,1),(11,8,1),(11,8,2),(11,8,3)}
    for z in base:
      for add_s,add_a in ((False,False),(True,False),(True,True)):
        n=z['n']+1;s=z['s']+add_s;r=z['r']+add_a
        if (n,s,r) not in requests:continue
        target=min(n-r,(n-s+2)*(n-s+1)//2)
        S=set(z['S'])|({n-1} if add_s else set());A=set(z['A'])|({n-1} if add_a else set())
        for first in range(-1,n-1):
            for second in range(-1,n-1):
                if first<0 and second<0:continue
                rows=[list(row)+[n-1] for row in z['rows']]
                for i,q in enumerate((first,second)):
                    if q>=0:rows[i][n-1]=rows[i][q];rows[i][q]=n-1
                tested+=1
                if not strong(rows) or nonmergeable_pairs(rows):continue
                attaining,_=bfs(rows,S,lambda T:len(T)<len(S) or not A<=T)
                if len(attaining)<target:continue
                reaching,_=bfs(rows,range(n),lambda T:T==S)
                if reaching is None:continue
                reset,_=bfs(rows,range(n),lambda T:len(T)==1)
                records.append(dict(n=n,s=len(S),r=len(A),value=len(attaining),rows=rows,S=sorted(S),A=sorted(A),
                                    reaching=reaching,attaining=attaining,reset=reset,source=f"subdivision of checked ({z['n']},{z['s']},{z['r']}) witness"))
    out=dict(tested=tested,scope='Only single-edge subdivisions in each letter, or a new fixed point for that letter.',certificates=records)
    (ROOT/'subdivide_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(tested=tested,certificates=len(records),triples=sorted({(z['n'],z['s'],z['r']) for z in records}))))

if __name__=='__main__':main()
