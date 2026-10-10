"""All individual letters of the E6/F2 conditional local model.

No alphabet-size assumptions; no automaton existence or absence
is inferred from this generator. Independent checker uses kernels.
"""
from itertools import product,permutations,combinations
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={1,4};D={5};E={6};F={2};U=A|B|D|E|F
def templates(n):
    Q=set(range(n));targets=(A,B,C,D,E,Q-A-B-C-D-E);rows=[]
    for known in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E),(A,B,C,D,E,F)):
        if sum(map(len,known))!=len(set().union(*known)):continue
        groups=(*known,Q-set().union(*known))
        if any(len(X-{1})>len(Y) for X,Y in zip(groups,targets)):continue
        forced={p for X,Y in zip(groups,targets) if len(Y)==1 for p in combinations(sorted(X),2)}
        if any(1 not in p or set(p)&U for p in forced):continue
        rows.append([sorted(X) for X in known])
    return rows
def letters(n,row):
    Q=set(range(n));groups=[set(X) for X in row];groups.append(Q-set().union(*groups))
    targets=(A,B,C,D,E,Q-A-B-C-D-E);options=[]
    for X,Y in zip(groups,targets):
        outside=sorted(X-{1});opts=[]
        for outputs in permutations(sorted(Y),len(outside)):
            assignment=dict(zip(outside,outputs))
            if 1 not in X:opts.append(assignment);continue
            forbidden={assignment[q] for q in outside if q in U}
            for t in sorted(Y-forbidden):opts.append(assignment|{1:t})
        options.append(opts)
    for parts in product(*options):
        word=[-1]*n
        for part in parts:
            for q,t in part.items():word[q]=t
        assert all(t>=0 for t in word)
        yield word
def control(n):
    rows=templates(n);counts=[];aggregate=0;mod=1<<256
    for row in rows:
        total=0;perm=0;c_kernel=0;ordinary=0
        for word in letters(n,row):
            ker=[p for p in combinations(range(n),2) if word[p[0]]==word[p[1]]]
            assert len(ker)<=1 and all(1 in p and not set(p)&U for p in ker)
            total+=1;perm+=not ker;c_kernel+=ker==[(1,4)];ordinary+=bool(ker and ker[0]!=(1,4))
            aggregate=(aggregate+int.from_bytes(hashlib.sha256(bytes(word)).digest(),'big'))%mod
        counts.append(dict(fields=row,full_letters=total,permutations=perm,C_kernel=c_kernel,ordinary_kernel=ordinary))
    return dict(n=n,templates=len(rows),full_letters=sum(x['full_letters'] for x in counts),
        permutations=sum(x['permutations'] for x in counts),C_kernel=sum(x['C_kernel'] for x in counts),
        ordinary_kernel=sum(x['ordinary_kernel'] for x in counts),unordered_row_hash_sum=f'{aggregate:064x}',records=counts)
def main():
    names=[Path(__file__).name,'B1_E6_F2_EXCLUSION.md','B1_FIFTH_ENTRANCE.md','b1_fifth_inventory.json']
    result=dict(status='complete_individual_letter_controls',parameter=[13,9,1],
        controls=[control(n) for n in (7,8,9,13)],
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='All individual letters respecting the derived singleton P1 cover and protected P1 isolation, with every ordinary output assignment. No transition-pair or full-automaton scan.')
    (ROOT/'b1_e6_f2_letters.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([dict(n=x['n'],templates=x['templates'],full_letters=x['full_letters'],ordinary_kernel=x['ordinary_kernel']) for x in result['controls']]))
if __name__=='__main__':main()
