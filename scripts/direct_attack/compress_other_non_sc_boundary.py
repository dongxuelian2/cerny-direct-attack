"""Exact finite controls for a source-construction error and general pair bounds."""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def family(n):
    assert n >= 3
    m=n-1
    rows=[list(range(1,m))+[0,m],list(range(m))+[m], [n//2]*m+[0]]
    rows[1][m-1]=0
    square=[rows[2][rows[2][q]] for q in range(n)]
    assert square == [n//2]*n
    return dict(n=n,marked_state=m,rows=rows,word=[2,2],word_length=2,
                compress_with_another_threshold=2,reset_square=square)


def heights():
    h=sha256();maps=controls=0
    for n in range(2,6):
        for f in product(range(n),repeat=n):
            maps+=1
            for q in range(n):
                path=[];p=q
                while p not in path:path.append(p);p=f[p]
                height=path.index(p)
                if not height:continue
                cycle=path[height:];target=p
                partner=next(r for r in cycle if iterate(f,r,height)==target)
                assert partner!=q and iterate(f,q,height)==iterate(f,partner,height)
                h.update(json.dumps([n,list(f),q,height,partner],separators=(',',':')).encode()+b'\n');controls+=1
    return dict(maximum_n=5,maps=maps,noncyclic_state_controls=controls,semantic_sha256=h.hexdigest())


def iterate(f,q,k):
    for _ in range(k):q=f[q]
    return q


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/compress_other_non_sc_boundary.json'));args=ap.parse_args()
    ns=list(range(3,65))+[101,257,1024,2049]
    out=dict(source_url='https://arxiv.org/pdf/2608.24245v1',source_pdf_sha256='62fcce9693c7e44f209f65c95939c48a08d5cf035627ffe67f56b7da59889208',source_pdf_zero_based_page=3,
             displayed_construction_status='REFUTED as a quadratic lower-bound construction; c squared resets',existential_proposition_status='OPEN here; NOT refuted by the construction error',
             family=[family(n) for n in ns],noncyclic_controls=heights(),
             boundary='PROVED paper: any compressible marked state has mu<=binom(n-1,2)+1, even without synchronization; a state noncyclic under an original letter has mu<=n-1. The literal Proposition7 construction has mu(p)=2 for ALL n>=3. No general linear mu bound or Cerny proof, no novelty for elementary bounds, no formal verification.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(family_parameters=len(ns),height_controls=out['noncyclic_controls'],boundary=out['boundary'])),flush=True)


if __name__=='__main__':main()
