"""Independent full-letter and pair-graph audit of the E6/F2 exclusion.

Enumerates kernels first, then injections of quotient blocks, instead
of the generator's outside1 assignments. Imports no generator.
"""
from itertools import combinations,product,permutations
from collections import deque
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={1,4};D={5};E={6};F={2};U=A|B|D|E|F
def independent_fields(n):
    return [list(map(sorted,groups)) for groups in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E),(A,B,C,D,E,F))
        if sum(map(len,groups))==len(set().union(*groups))]
def independent_letters(n,row):
    Q=set(range(n));groups=[set(X) for X in row];groups.append(Q-set().union(*groups))
    targets=(A,B,C,D,E,Q-A-B-C-D-E)
    for kernel in [None]+[(1,q) for q in sorted(Q-U-{1})]:
        if kernel and not any(set(kernel)<=X for X in groups):continue
        options=[];possible=True
        for X,Y in zip(groups,targets):
            blocks=[(q,) for q in sorted(X) if not kernel or q not in kernel]
            if kernel and set(kernel)<=X:blocks.append(kernel)
            blocks.sort()
            if len(blocks)>len(Y):possible=False;break
            options.append([(blocks,values) for values in permutations(sorted(Y),len(blocks))])
        if not possible:continue
        for assignment in product(*options):
            word=[-1]*n
            for blocks,values in assignment:
                for block,t in zip(blocks,values):
                    for q in block:word[q]=t
            assert all(t>=0 for t in word)
            yield word,kernel
def pair_levels(rows):
    n=len(rows[0]);pairs=set(combinations(range(n),2))
    reached={p for p in pairs if any(row[p[0]]==row[p[1]] for row in rows)};first=set(reached)
    second=first|{p for p in pairs if any(tuple(sorted((row[p[0]],row[p[1]]))) in first for row in rows)}
    while True:
        extended=reached|{p for p in pairs if any(tuple(sorted((row[p[0]],row[p[1]]))) in reached for row in rows)}
        if extended==reached:break
        reached=extended
    return first,second,reached
def small_pair_graph_controls():
    # Arbitrary star graphs, all independent (n-1)-sets, no field premises.
    graphs=0;tested_sets=0
    for n in range(3,9):
        for c in range(n):
            outside=[q for q in range(n) if q!=c]
            for count in range(2,n):
                for neighbors in combinations(outside,count):
                    independent=[]
                    for omitted in range(n):
                        tested_sets+=1;X=set(range(n))-{omitted}
                        if not any({c,q}<=X for q in neighbors):independent.append(omitted)
                    assert independent==[c];graphs+=1
    rows=[[1,2,0],[0,2,2]];first,second,allpairs=pair_levels(rows)
    assert first=={(1,2)} and second=={(0,1),(1,2)} and len(allpairs)==3
    for start in range(3):
        reached={start};todo=deque([start])
        while todo:
            for row in rows:
                q=row[todo[0]]
                if q not in reached:reached.add(q);todo.append(q)
            todo.popleft()
        assert len(reached)==3
    return dict(arbitrary_star_graphs=graphs,independent_n_minus_one_sets_tested=tested_sets,
        one_point_P2_cover_admission_control=dict(rows=rows,P1=[[1,2]],P2=[[0,1],[1,2]],
            cover=[1],strongly_connected=True,synchronizing=True,scope='Three-state control, not the E6/F2 thirteen-state branch or an equality claim.'))
def letter_control(n,expected):
    Q=set(range(n));records=[];aggregate=0;mod=1<<256;counts=dict(graph_witnesses=0,
        singleton_protected_witnesses=0,C_swap_or_collapse_witnesses=0,proper_incoming1=0,absent1=0)
    literal_rows=independent_fields(n);assert len(literal_rows)==32
    for fields in literal_rows:
        total=0;perm=0;c_kernel=0;ordinary=0
        for word,kernel in independent_letters(n,fields):
            total+=1;perm+=kernel is None;c_kernel+=kernel==(1,4);ordinary+=kernel is not None and kernel!=(1,4)
            aggregate=(aggregate+int.from_bytes(hashlib.sha256(bytes(word)).digest(),'big'))%mod
            immediate={p for p in combinations(range(n),2) if word[p[0]]==word[p[1]]}
            assert immediate==(set() if kernel is None else {kernel})
            assert all(1 in p and not set(p)&U for p in immediate)
            assert len({word[q] for q in Q-{1}})==n-1 and len(set(word))>=n-1
            preC={q for q,t in enumerate(word) if t in C}
            assert preC in (A,B,C,D)
            inverseG={p for p in combinations(range(n),2) if set((word[p[0]],word[p[1]]))==C}
            assert inverseG<={(1,4)}
            pre1={q for q,t in enumerate(word) if t==1}
            counts['proper_incoming1']+=pre1=={1};counts['absent1']+=not pre1
            for q in range(7,n):
                # Independent graph proof: if outside1 maps onto a set
                # containing1, at least one of edges14,1q has two
                # distinct outside1 predecessors. The corresponding
                # C-merger or assumed R merges them on the next step.
                image={word[x] for x in Q-{1}}
                if 1 in image:
                    edge=next(e for e in ((1,4),(1,q)) if set(e)<=image)
                    p=tuple(next(x for x in Q-{1} if word[x]==t) for t in edge)
                    assert p[0]!=p[1] and 1 not in p
                    merger=list(range(n));merger[edge[0]]=merger[edge[1]]
                    assert merger[word[p[0]]]==merger[word[p[1]]]
                    counts['graph_witnesses']+=1
                if not pre1 or pre1=={1}:continue
                assert q in word
                x=next(x for x,t in enumerate(word) if t==q)
                if len(preC)==1:
                    u=next(iter(preC));assert u in (0,3,5) and word[u]==1 and 4 not in word
                    p=(u,x);assert u in U and u!=x
                    counts['singleton_protected_witnesses']+=1
                else:
                    assert preC==C and word[4]==1 and x not in C
                    if word[1]==4:assert len(set(word))==n
                    else:assert word[1]==1 and 4 not in word
                    p=(4,x);assert 1 not in p
                    counts['C_swap_or_collapse_witnesses']+=1
                assert {word[p[0]],word[p[1]]}=={1,q}
                merger=list(range(n));merger[1]=q
                assert merger[word[p[0]]]==merger[word[p[1]]]
        records.append(dict(fields=fields,full_letters=total,permutations=perm,C_kernel=c_kernel,ordinary_kernel=ordinary))
    reconstructed=dict(n=n,templates=len(records),full_letters=sum(x['full_letters'] for x in records),
        permutations=sum(x['permutations'] for x in records),C_kernel=sum(x['C_kernel'] for x in records),
        ordinary_kernel=sum(x['ordinary_kernel'] for x in records),unordered_row_hash_sum=f'{aggregate:064x}',records=records)
    assert reconstructed==expected
    if n==13:
        z=next(z for z in json.loads((ROOT/'b1_fifth_inventory.json').read_text(encoding='utf-8'))['records'] if z['E']==[6] and z['F']==[2])
        assert sorted([row[key] for key in ('preA','preB','preC','preD','preE')] for row in z['rows'])==sorted(literal_rows)
    return dict(n=n,complete_individual_letters=reconstructed['full_letters'],all_known_preimage_templates=32,
        permutations=reconstructed['permutations'],C_kernel_letters=reconstructed['C_kernel'],
        ordinary_kernel_letters=reconstructed['ordinary_kernel'],proof_controls=counts,
        unordered_row_hash_sum=reconstructed['unordered_row_hash_sum'])
def main():
    inv=json.loads((ROOT/'b1_e6_f2_letters.json').read_text(encoding='utf-8'))
    checks=[letter_control(z['n'],z) for z in inv['controls']]
    small=small_pair_graph_controls()
    for name,digest in inv['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    names=[Path(__file__).name,'enumerate_b1_e6_f2_letters.py','b1_e6_f2_letters.json','PROOF.md#problem4-b1-e6-f2-exclusion',
        'PROOF.md#problem4-b1-fifth-entrance','b1_fifth_inventory.json','b1_fifth_audit.json','PROOF.md#problem4-b1-partial-cover-fourth',
        'PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    result=dict(status='pass',parameter=[13,9,1],alphabet='arbitrary finite',excluded_fifth=[2],fourth=[6],
        complete_individual_letter_controls=checks,independent_pair_graph_controls=small,
        correct_isolation_depth=2,uses_one_point_P3_floor=False,removed_binary_fifth_field_pairs=122,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete conditional E6/F2 exclusion for every finite alphabet. Two symbolic proofs with full individual-letter controls. No full thirteen-state transition-pair scan, whole E6 exclusion, F value or alphabet separation.')
    (ROOT/'b1_e6_f2_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in result.items() if key!='source_sha256'}))
if __name__=='__main__':main()
