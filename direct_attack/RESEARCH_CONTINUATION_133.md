# A compatible square via fixed-root cycle routing

Date:2026-10-02. Starting HEAD d16da3b49140209c87f561e7ab5ade3daa3eed97.
Goal ACTIVE, general Cerny OPEN, frozen168ffff unchanged; changes ONLY
direct_attack. Registry132/213 preserves131 earlier check captures
verbatim and appends ONE checker; no full132 rerun; native builds8.

After committing the bounded-short-return obstruction, research moved
to actual original letters. A trial with one transposition away from
the kernel pair yielded a compatible inverse-history construction.
Self-audit widened it: involution, a single transposition and an
almost-circular product are NOT needed. The retained final theorem
is FIXED_ROOT_CYCLE_EXTENSION.md, PROVED paper for arbitrary n/alphabet
under its fixed-common-root conditions. No novelty/formal claim.

There is a permutation b with b(r)=s and root cycle R. Every other
letter either permutes Q while preserving R as a set, or has omitted
r, fixed root s, kernel{r,s} and a permutation on Q\{r}. At least one
singular letter is present. On SC inputs, every nonempty proper subset
extends by EXACTLY one in ORIGINAL cost<=n. With R mixed, align its
0->1 membership boundary and apply a singular original letter, cost
<=|R|. With R empty/full, route an existing/missing point through the
original b-cycle graph. Before root mixing, cardinality change is ZERO.
Its minimum distance strictly decreases, so each selected non-root
cycle is paid once: preparation<=n-|R|. These two costs add to n.

Starting from the original singular preimage of{s}, size2/cost1, the
n-2 actual factors of cost<=n form ONE compatible square reset. Every
underlying edge of this class is on a cycle (the exceptional r->s is
on b's cycle), so its SCCs are closed and any sync input is already SC.
Thus the theorem covers ALL sync inputs of these letter types. In the
earlier almost-circular normal form it proves the square when A(1)=1.

The essential next obstacle is root movement, not cyclic routing alone.
At n4, a=[2,2,1,3],b=[1,3,2,0], U={0,1,3} needs EXACT6>4 to extend.
Here the omitted r0/b-adjacent kernel partner s1 is NOT fixed by a.
The ALL16 subset Bellman certificate and literal length6 word are
independently checked. Ordinary rt9 was already verified by the full
normal-form audit. Thus dropping the root hypothesis is REFUTED for
n-extensibility, not for Cerny or the subclass theorem.

Independent finite controls:219 inputs,ALL159 binary pairs n2..5,
146 SC inputs (94 with multicycle b),21 multiple-letter inputs,
16411 proper subsets, maximum127 paid preparation steps,2247092
literal particle/letter controls,30 counter Bellman edges and eight
rejected corruptions. The checker imports no generator or old solver;
it checks complete finite pair coverage, ALL subsets for retained
n<=10 inputs, sampled larger/deep-chain controls through n257, literal
hypotheses/labels, distinct-cycle charges, strict distance descent,
and one whole compatible reset. COMPUTATIONALLY VERIFIED is finite;
the arbitrary-n theorem is paper, not a finite pattern inference.

Exploratory prior BFS sampled8927 SC valid binary inputs n4..10,
2914082 subset searches, maximum extension10; it is archived separately
as a transcription of actual tool stdout, without claiming independent
negative implementation coverage. It is not used as proof.

Continue research after committing this theorem. The remaining
almost-circular case A(1)!=1 can lose cardinality during root routing;
local n-extension is already false. A compatible amortized compensation
or a different general route remains necessary. General Cerny OPEN.
