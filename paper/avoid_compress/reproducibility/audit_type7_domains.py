"""Literal finite controls for every uniform type-7 domain reduction.

Uses actual image complements, not the structural action formula. The
symbolic proof is in TYPE7_EARLY_EXCLUSION.md; finite controls do not replace it.
"""
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
reports = []
for n in (6, 7):
    Q = set(range(n)); C = set(range(5))
    rows = json.loads((ROOT / f'early_alphabet_pool_n{n}.json').read_text())['records'][7]['letters']
    holes = [frozenset(h) for h in combinations(range(n), 3)
             if all(set(h) & e for e in ({0, 1}, {2, 3}, {2, 4}))]
    ix = {h: i for i, h in enumerate(holes)}
    aa = {}
    for f in rows:
        aa[tuple(f)] = [ix.get(frozenset(Q - {f[q] for q in Q - h}), -1)
                        if len({f[q] for q in Q - h}) == n - 3 else -1 for h in holes]
    def domain(alphabet, length):
        d = set(range(len(holes)))
        for _ in range(length):
            d = {i for i in range(len(holes)) if all(a[i] in d for a in alphabet)}
        return {holes[i] for i in d}
    def hs(*triples):
        return set(map(frozenset, triples))
    counts = {}; maxima = {}; equality_counts = {}
    reduced = []; special_checks = 0; B4_checks = 0
    for f in rows:
        perm = len(set(f)) == n
        missing = None if perm else next(q for q in Q if q not in f)
        # Verify the structural templates independently against the full rows.
        if perm:
            assert ({f[0], f[1]} == {0, 1} and
                    ({f[2], f[3]} == {2, 3} or {f[2], f[4]} == {2, 3})) or (
                        {f[0], f[1]} == {2, 3} and {f[2], f[3]} == {0, 1})
        elif missing < 2:
            assert f[0] == f[1] and f[0] in ({1 - missing} | (Q - {0, 1, 2, 3}))
            assert {f[2], f[3]} == {2, 3} or {f[2], f[4]} == {2, 3}
        else:
            assert missing < 4 and f[0] == f[1]
            assert {f[2], f[3]} == {0, 1}
            assert f[0] in ({5 - missing} | (Q - {0, 1, 2, 3}))
        if f[2] == 3 or missing == 3:
            d = domain([aa[tuple(f)]], 1)
            if f[2] == 3:
                if perm:
                    t = {f[2], f[4]} == {2, 3}; free = f[3] if t else f[4]
                    if free == 4:
                        expected = hs((0,2,3),(1,2,3),(0,2,4),(1,2,4),(0,3,4),(1,3,4))
                    else:
                        v = next(q for q in Q if f[q] == 4); assert v >= 5
                        core = ((0,2,4),(1,2,4)) if t else ((0,2,3),(1,2,3))
                        expected = hs(*core,(0,3,4),(1,3,4),(0,2,v),(1,2,v))
                    assert d == expected
                else:
                    c = f[0]; t = {f[2], f[4]} == {2, 3}; free = f[3] if t else f[4]
                    assert len(d) == 6 - int(c == 4)
                    if c != 4:
                        if free == 4:
                            expected = hs((0,2,3),(1,2,3),(0,2,4),(1,2,4),(0,3,4),(1,3,4))
                        else:
                            v = next(q for q in Q if f[q] == 4); assert v >= 5
                            core = ((0,2,4),(1,2,4)) if t else ((0,2,3),(1,2,3))
                            expected = hs(*core,(0,3,4),(1,3,4),(0,2,v),(1,2,v))
                        assert d == expected
            else:
                c, h = f[0], f[4]; A = int(c in (2,4)); B = int(h in (2,4))
                assert len(d) == 4 - A + 2 * B
                if len(d) == 6:
                    v = next(q for q in Q if f[q] in ({2,4} - {h})); assert v >= 5
                    assert d == hs((0,2,4),(1,2,4),(0,3,4),(1,3,4),(0,2,v),(1,2,v))
            special_checks += 1; continue
        isB = perm and {f[0], f[1]} == {2, 3}
        if isB and f[f[2]] == 3:
            # Both orientations are equivalent under the kernel endpoint swap.
            b = f if f[0] == 2 else [f[1], f[0], 1-f[2], 1-f[3], *f[4:]]
            assert b[:4] == [2,3,1,0]
            # Test the normalized actual transformation directly.
            if tuple(b) not in aa:
                aa[tuple(b)] = [ix.get(frozenset(Q-{b[q] for q in Q-h}),-1) for h in holes]
            d = domain([aa[tuple(b)]],2); a = b[4]
            if a == 4:
                assert d == hs((0,2,3),(0,2,4),(1,2,4),(0,3,4),(1,3,4))
            else:
                v = next(q for q in Q if b[q] == 4)
                expected = hs((0,2,3),(0,3,4))
                if a == v: expected |= hs((0,2,4))
                else:
                    w = next(q for q in Q if b[q] == v); assert w >= 5
                    expected |= hs((0,2,w))
                assert d == expected
            B4_checks += 1; continue
        reduced.append(f)
    # No B: every remaining letter preserves the entire two-center family.
    familyI = {h for h in holes if 2 in h and h & {0,1}}
    family02 = {frozenset((0,2,x)) for x in Q-{0,2}}
    noB_checks = 0; keeper_checks = 0
    for g in reduced:
        if len(set(g)) == n and {g[0],g[1]} == {2,3}: continue
        assert all(aa[tuple(g)][ix[H]] >= 0 and holes[aa[tuple(g)][ix[H]]] in familyI for H in familyI)
        noB_checks += 1
    B2 = [f for f in reduced if f[:4] == [2,3,0,1]]
    for b in B2:
        a = b[4]; closed = a == 4; v = next(q for q in Q if b[q] == 4)
        base = domain([aa[tuple(b)]],2)
        if closed:
            assert base == family02 | hs((1,2,4),(0,3,4),(1,3,4))
        else:
            extra = hs((1,2,v))
            if a == v: extra |= hs((0,3,4))

            assert base == family02 | extra, (n,b,v,base,family02|extra)
        for g in reduced:
            perm = len(set(g)) == n
            missing = None if perm else next(q for q in Q if q not in g)
            keeper = ({g[0],g[2]} if perm else {missing,g[2]}) == {0,2}
            if keeper:
                assert all(aa[tuple(g)][ix[H]] >= 0 and holes[aa[tuple(g)][ix[H]]] in family02 for H in family02)
                keeper_checks += 1; continue
            d = domain([aa[tuple(b)],aa[tuple(g)]],2)
            part = d if closed else d & family02
            nc = sum(h <= C for h in part); no = sum(not h <= C for h in part)
            assert nc + no == len(part)
            assert closed or len(d-family02)<=2
            if perm:
                h = g[4]
                if {g[0],g[1]} == {2,3}: key = 'P_B'
                elif {g[2],g[3]} == {2,3}: key = 'P_A'
                else: key = 'P_T'; h = g[3]
                H = int(h == (4 if closed else v)); H4 = int(h == 4)
                if closed: bound = ((1+3*H4,1-H4) if key == 'P_B' else (1+4*H4,1-H4))
                else: bound = ((0,1-H4) if key == 'P_B' else (1+H,1-H))
            else:
                c = g[0]
                key = 'V' if missing == 2 else ('U_A' if {g[2],g[3]} == {2,3} else 'U_T')
                h = g[3] if key == 'U_T' else g[4]
                if key == 'V':
                    A = int(c == (4 if closed else v)); H = int(h == (4 if closed else v))
                    bound = (3+A+2*H,1-A-H) if closed else (1+A+H,1-A-H)
                else:
                    targets = {0,4} if closed else {0,v}
                    A = int(c in targets); H = int(h in targets)
                    if closed:
                        bound = (A+(4 if key=='U_A' else 3)*int(h==4)+(2 if key=='U_A' else 1)*int(h==0),2-A-H)
                    else: bound = (A+H,2-A-H)
            assert nc <= bound[0] and no <= bound[1], (n,b,g,key,d,bound,nc,no)
            assert sum(bound) <= (5 if closed else 2), (n,key,bound)
            assert len(d)<=(5 if closed else 4)
            name = ('closed_' if closed else 'mixing_')+key
            counts[name] = counts.get(name,0)+1; maxima[name] = max(maxima.get(name,0),len(d))
            if len(d) == 5:
                assert closed
                if key == 'P_A': expected = hs((0,1,2),(0,2,4),(1,2,4),(0,3,4),(1,3,4)); eq='C_A'
                elif key == 'P_T': expected = hs((0,1,2),(0,2,3),(1,2,4),(0,3,4),(1,3,4)); eq='C_T'
                elif key == 'V': expected = hs((0,2,3),(0,2,4),(1,2,4),(0,3,4),(1,3,4)); eq='C_V'
                else:
                    assert key=='U_A' and h==4
                    expected = hs((0,2,4),(1,2,4),(0,3,4),(1,3,4))
                    if c in (0,4): expected |= hs((0,1,2)); eq='C_A'
                    else:
                        w = next(q for q in Q if g[q]==0); assert w>=5
                        expected |= hs((0,2,w)); eq='D_w'
                assert d == expected, (b,g,d,expected)
                equality_counts[eq] = equality_counts.get(eq,0)+1
    reports.append(dict(n=n,compatible_letters=len(rows),special_domain_checks=special_checks,
                        B_four_cycle_checks=B4_checks,reduced_letters=len(reduced),normalized_B_two_cycles=len(B2),
                        no_B_invariant_checks=noB_checks,keeper_checks=keeper_checks,
                        breaker_checks=sum(counts.values()),cases=counts,maxima=maxima,equality_domains=equality_counts))

py = json.loads((ROOT/'type7_reduced_actions.json').read_text())
cpp = json.loads((ROOT/'type7_actions_independent.json').read_text())
assert py['status'] == cpp['status'] == 'pass'
for a,b in zip(py['records'],cpp['records'],strict=True):
    assert a['name']==b['name'] and a['profiles']==b['profiles']
    assert a['profile_count']==b['profile_count'] and a['distance_vectors']==b['distance_vectors']
    assert [c['distance_vector'] for c in a['candidates']]==b['candidate_vectors']
    assert b['all_candidates_core_closed']
result = dict(status='pass',reports=reports,all_seven_profiles_flags_vectors_match=True,
              scope='Finite controls and independent projection comparison, accompanying the uniform proof.')
(ROOT/'type7_domain_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
