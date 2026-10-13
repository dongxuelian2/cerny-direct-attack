"""Seal a NEW residual graph failure, and a literal unrestricted weighted minimum."""
from collections import deque
from pathlib import Path
import json
from .order_two_three_a_barrier import pair_reset

ROOT=Path(__file__).resolve().parents[2]


def main():
    source=ROOT/'scripts/direct_attack/data/weighted_late_block_M24_sample1000000_seed2026100331.counter.json'
    candidate=json.loads(source.read_text());a=candidate['a'];M=candidate['M'];h=candidate['h']
    assert M==24 and h==2
    F=[a,list(range(1,M))+[0,M]];S=(1<<M)|sum(1<<q for q in range(M) if q%2==0)
    mass=lambda U:U.bit_count()+(U>>M&1)
    D={S:0};parents={};todo=deque([S]);goal=None
    while todo:
        U=todo.popleft()
        if mass(U)>mass(S):goal=U;break
        for c,row in enumerate(F):
            V=sum(1<<q for q,x in enumerate(row) if U>>x&1)
            if V not in D:D[V]=D[U]+1;parents[V]=(U,c);todo.append(V)
        assert len(D)<=2000000,'INCOMPLETE cap: no lower-bound assertion'
    assert goal is not None
    word=[];V=goal
    while V!=S:V,c=parents[V];word.append(c)
    assert D[goal]==9
    three=[0]+[1]*10+[0]+[1]*11+[0,1]
    data=dict(rows=F,subset=S,triangular_h=h,minimum=D[goal],word=word,target=goal,
        cut=sorted([U,d] for U,d in D.items() if d<D[goal]),three_a_minimum=25,
        three_a_word=three,reset_word=pair_reset(F),native_counter_path=source.relative_to(ROOT).as_posix())
    (ROOT/'scripts/direct_attack/data/weighted_graph_automaticity_barrier.json').write_text(
        json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(n=M+1,weighted_minimum=9,three_a_minimum=25,cut_vertices=len(data['cut']),
        reset_cost=len(data['reset_word']),automatic_graph='REFUTED',weighted_M_extension='OPEN',general_Cerny='OPEN')))


if __name__=='__main__':main()
