"""Independent row/set audits; no generator or previous policy solver imports."""
from collections import deque
from copy import deepcopy
import json
from pathlib import Path


def compose(u,v):
    return [v[q] for q in u]


def power(row,m):
    out = list(range(len(row)))
    while m:
        if m&1:
            out = compose(out,row)
        row = compose(row,row)
        m >>= 1
    return out


def literal(word,rows):
    out = list(range(len(next(iter(rows.values())))))
    for x in word:
        out = compose(out,rows[x])
    return out


def image(S,row):
    out = 0
    while S:
        bit = S&-S
        out |= 1 << row[bit.bit_length()-1]
        S -= bit
    return out


def inverse(S,row):
    return sum(1 << q for q,t in enumerate(row) if S>>t&1)


def graph(rows,sources):
    dist = {s:0 for s in sources}
    prev = {}
    todo = deque(sources)
    while todo:
        S = todo.popleft()
        for x,row in rows.items():
            T = image(S,row)
            if T not in dist:
                dist[T] = dist[S]+1
                prev[T] = (S,x)
                todo.append(T)
    return dist,prev


def inverse_distance(T,rows,parents):
    dist = {T:0}
    todo = deque([T])
    while todo:
        S = todo.popleft()
        if any(R&~S == 0 for R in parents):
            return dist[S],len(dist)
        for row in rows.values():
            U = inverse(S,row)
            if U not in dist:
                dist[U] = dist[S]+1
                todo.append(U)
    raise AssertionError('no actual larger-source arrival')


def sc(rows):
    n = len(next(iter(rows.values())))
    edges = [set(row[q] for row in rows.values()) for q in range(n)]
    back = [set() for q in range(n)]
    for q in range(n):
        for t in edges[q]:
            back[t].add(q)
    for adj in (edges,back):
        reached = {0}
        todo = deque([0])
        while todo:
            q = todo.popleft()
            for t in adj[q]-reached:
                reached.add(t)
                todo.append(t)
        assert len(reached) == n


def stall_distances(rows,p):
    """Independent zero/one-cost BFS to the first exceptional a departure."""
    n = 2*p+1
    back = [[] for q in range(n)]
    for x,row in rows.items():
        for q,t in enumerate(row):
            back[t].append((q,int(x=='a')))
    inf = 10**12
    dist = [inf]*n
    dist[2*p] = 0
    todo = deque([2*p])
    while todo:
        t = todo.popleft()
        for q,cost in back[t]:
            if dist[q] > dist[t]+cost:
                dist[q] = dist[t]+cost
                if cost:
                    todo.append(q)
                else:
                    todo.appendleft(q)
    assert dist[p]+1 == p+1
    for i in range(p):
        assert dist[i]+1 == ((p-i)%p)+(p+1)
    return dist


def validate(z):
    p = z['p']
    assert p >= 2
    n, N = 2*p+1, 6*p+3
    rows = z['rows']
    binary = z['binary_rows']
    assert z['n']==n and z['binary_n']==N
    assert set(rows)=={'a','b','c'} and set(binary)=={'0','1'}
    C,D = range(p),range(p,n)
    a = [None]*n
    for cycle in (list(C),list(D)):
        for q,t in zip(cycle,cycle[1:]+cycle[:1]):
            a[q] = t
    b = [q if q<p else (q-p)%p for q in range(n)]
    c = [p if q==0 else 0 if q==p else q for q in range(n)]
    assert rows==dict(a=a,b=b,c=c)
    expected0 = [(q%n)+((q//n+1)%3)*n for q in range(N)]
    xi = [c,b,a]
    expected1 = [xi[q//n][q%n] for q in range(N)]
    assert binary=={'0':expected0,'1':expected1}
    assert len(set(a))==len(set(c))==n and len(set(b))==p
    assert compose(b,b)==b
    assert len(set(binary['0']))==N and len(set(binary['1']))==n
    assert set(binary['1'][:n])==set(range(n))
    full = (1<<n)-1
    for names in (('a','b'),('a','c'),('b','c')):
        restricted,_ = graph({x:rows[x] for x in names},[full])
        assert min(S.bit_count() for S in restricted)>=p
    bfull = (1<<N)-1
    for x in ('0','1'):
        restricted,_ = graph({x:binary[x]},[bfull])
        assert min(S.bit_count() for S in restricted)>1
    sc(rows)
    sc(binary)
    s = p//2
    k = p-s
    A = set(range(s,p)) if p%2==0 else set(range(s))
    T = {q for q in range(n) if b[q] in A}
    assert len(A)==s and len(T)==p
    assert z['s']==s and z['k']==k
    assert z['projected_target']==sorted(A)
    assert z['target']==z['binary_target']==sorted(T)
    pi = [q if q<p else (q-p)%p for q in range(n)]
    for x,row in rows.items():
        for q,t in enumerate(row):
            assert (pi[t]-pi[q])%p == ((1-int(q==2*p))%p if x=='a' else 0)
    # Every letter is injective on C; only c can send a previously
    # unexported original C-identity into D, and only at its one state 0.
    for x,row in rows.items():
        assert len(set(row[q] for q in C))==p
        assert [q for q in C if row[q]>=p] == ([0] if x=='c' else [])
    stall_distances(rows,p)
    amin = (p*p+3*p-2)//2
    assert z['a_lower_bound']==amin
    assert z['c_lower_bound']==k and z['mandatory_b_count']==1
    assert z['image_extension']==amin+k+1
    assert z['binary_image_extension']==3*amin+k+1
    start = min(A)
    base = k*(p+1)
    # Exhaust just the p possible residues after the universal base.
    # This checks the all-word congruence lower argument, not sample words.
    feasible = []
    for t in range(base,base+p):
        i = (start-1-t)%p
        if t >= base+((p-i)%p):
            feasible.append(t)
    assert feasible and min(feasible)==amin
    M = amin-k+1
    assert z['entering_repeated_ca']==k-1 and z['entering_final_a']==M
    enter = compose(b,power(compose(c,a),k-1))
    enter = compose(compose(enter,c),power(a,M))
    assert set(enter)==T
    d = compose(compose(c,power(a,p+1)),b)
    assert [d[q] for q in C]==[0]+[(q+1)%p for q in range(1,p)]
    reset = compose(b,power(d,p-1))
    assert set(reset)=={0}
    assert z['reset_upper_bound']==1+(p+3)*(p-1) <= (n-1)**2
    z0,o = binary['0'],binary['1']
    code_a = compose(power(z0,2),o)
    code_b = compose(z0,o)
    code_c = o
    benter = compose(o,power(compose(code_c,code_a),k-1))
    benter = compose(compose(benter,code_c),power(code_a,M))
    assert set(benter[n:2*n])==T
    actual_target = compose(compose(o,z0),benter)
    assert set(actual_target)==T
    bblock = compose(compose(code_c,power(code_a,p+1)),code_b)
    breset = compose(compose(o,code_b),power(bblock,p-1))
    assert set(breset)=={0}
    assert z['binary_reset_upper_bound']==3+(3*p+6)*(p-1) <= (N-1)**2
    assert z['binary_entering_source_selector']==1
    assert z['binary_actual_target_word_length']==3*amin+k+3
    if p<=16:
        w = 'b'+'ca'*(k-1)+'c'+'a'*M
        r = 'b'+('c'+'a'*(p+1)+'b')*(p-1)
        # Construct codes from actual selector moves, without importing gen.
        code = {'c':'1','b':'01','a':'001'}
        bw = '1'+''.join(code[x] for x in w[1:])
        br = '1'+''.join(code[x] for x in r)
        assert z['literal_entering_word']==w and len(w)==z['image_extension']
        assert z['literal_reset_word']==r and len(r)==z['reset_upper_bound']
        assert z['literal_binary_entering_word']==bw and len(bw)==z['binary_image_extension']
        assert z['literal_binary_actual_target_word']=='10'+bw
        assert z['literal_binary_reset_word']==br and len(br)==z['binary_reset_upper_bound']
        assert set(literal(w,rows))==T and set(literal(r,rows))=={0}
        assert set(literal(bw,binary)[n:2*n])==T
        assert set(literal('10'+bw,binary))==T and set(literal(br,binary))=={0}
    return T


def main():
    data = Path('scripts/direct_attack/data')
    source = json.loads((data/'two_cycle_image_obstruction.json').read_text())
    records = source['records']
    assert [z['p'] for z in records]==list(range(2,65))+[65,100,128,256,512,1024]
    scopes = source['scopes']
    assert scopes['literal_parameters']==list(range(2,17))
    assert scopes['ternary_forward_parameters']==scopes['ternary_inverse_parameters']==list(range(2,10))
    assert scopes['binary_forward_parameters']==list(range(2,9))
    assert scopes['binary_inverse_parameters']==list(range(2,7))
    assert scopes['maximum_ternary_n']==2049 and scopes['maximum_binary_n']==6147
    for z in records:
        validate(z)
    byp = {z['p']:z for z in records}
    forward,backward,bforward,bbackward = [],[],[],[]
    original_images = {}
    for p in source['scopes']['ternary_forward_parameters']:
        z = byp[p]
        n = z['n']
        full = (1<<n)-1
        T = sum(1<<q for q in z['target'])
        dist,prev = graph(z['rows'],[full])
        assert len(dist)==4**p
        assert all(S==full or S.bit_count()<=p for S in dist)
        assert T in dist and min(v for S,v in dist.items() if S&~T==0)==z['image_extension']
        rt = min(v for S,v in dist.items() if S.bit_count()==1)
        assert rt <= z['reset_upper_bound']
        original_images[p] = set(dist)
        forward.append(dict(p=p,n=n,vertices=len(dist),rt=rt,image_extension=z['image_extension']))
    for p in source['scopes']['ternary_inverse_parameters']:
        z = byp[p]
        T = sum(1<<q for q in z['target'])
        value,count = inverse_distance(T,z['rows'],[(1<<z['n'])-1])
        assert value==z['image_extension']
        backward.append(dict(p=p,n=z['n'],vertices=count,image_extension=value))
    for p in source['scopes']['binary_forward_parameters']:
        z = byp[p]
        n,N = z['n'],z['binary_n']
        full = (1<<N)-1
        pure = [((1<<n)-1)<<(i*n) for i in range(3)]
        T = sum(1<<q for q in z['target'])
        dist,_ = graph(z['binary_rows'],[full])
        expected = {full}|{S<<(i*n) for S in original_images[p] for i in range(3)}
        assert set(dist)==expected
        rt = min(v for S,v in dist.items() if S.bit_count()==1)
        assert rt <= z['binary_reset_upper_bound']
        larger = [S for S in dist if S.bit_count()>p]
        assert set(larger)=={full,*pure}
        into,_ = graph(z['binary_rows'],larger)
        assert min(v for S,v in into.items() if S&~T==0)==z['binary_image_extension']
        bforward.append(dict(p=p,n=N,vertices=len(dist),extension_vertices=len(into),rt=rt,
                             image_extension=z['binary_image_extension']))
    for p in source['scopes']['binary_inverse_parameters']:
        z = byp[p]
        n = z['n']
        T = sum(1<<q for q in z['target'])
        pure = [((1<<n)-1)<<(i*n) for i in range(3)]
        value,count = inverse_distance(T,z['binary_rows'],pure)
        assert value==z['binary_image_extension']
        bbackward.append(dict(p=p,n=z['binary_n'],vertices=count,image_extension=value))
    base = byp[6]
    corruptions = []
    edits = [('fold transition',lambda z:z['rows']['b'].__setitem__(2*z['p'],1)),
             ('entering exponent',lambda z:z.__setitem__('entering_final_a',z['entering_final_a']+1)),
             ('ternary extension length',lambda z:z.__setitem__('image_extension',z['image_extension']-1)),
             ('binary extension length',lambda z:z.__setitem__('binary_image_extension',z['binary_image_extension']-1)),
             ('binary selector row',lambda z:z['binary_rows']['1'].__setitem__(0,1)),
             ('target cardinality',lambda z:z['target'].pop()),
             ('reset length',lambda z:z.__setitem__('reset_upper_bound',z['reset_upper_bound']-1))]
    for name,edit in edits:
        damaged = deepcopy(base)
        edit(damaged)
        try:
            validate(damaged)
        except AssertionError:
            corruptions.append(name)
        else:
            raise AssertionError('accepted corruption '+name)
    report = dict(verified=True,controls=len(records),literal_controls=15,
                  ternary_irreducible_controls=len(records),binary_irreducible_controls=len(records),
                  ternary_forward=forward,ternary_inverse=backward,
                  binary_forward=bforward,binary_inverse=bbackward,
                  ternary_forward_vertices=sum(z['vertices'] for z in forward),
                  ternary_inverse_vertices=sum(z['vertices'] for z in backward),
                  binary_forward_vertices=sum(z['vertices'] for z in bforward),
                  binary_extension_forward_vertices=sum(z['extension_vertices'] for z in bforward),
                  binary_inverse_vertices=sum(z['vertices'] for z in bbackward),
                  corruptions_rejected=corruptions,
                  boundary='bounded independent original-row and ordinary-set audits; all-parameter proofs remain paper PROVED; no formal kernel; general Cerny and global policy square OPEN')
    (data/'two_cycle_image_obstruction_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('ternary_forward','ternary_inverse','binary_forward','binary_inverse')}),flush=True)


if __name__ == '__main__':
    main()
