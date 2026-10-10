# Unrestricted B0/C4/D12 fourth exclusions

Assume (n,s,r)=(13,9,1), ac(S,{3})=12, B={0}, C={4}, D={1,2},
and K={1,2} covers P5. The complete fourth classification leaves only
E={5} and E={1,5}, with 8 and 16 labels. There are no additional
covered Boolean companions. Both geometries are impossible for an
arbitrary finite alphabet satisfying strong connectivity and synchronization.
This is a conditional structural exclusion, not a numerical F value.

Write A={3}, H=A union B union C, O=Q-(H union D), and e=5. Exact
columns are preA in {A,B}, preB in {A,B,C}, preC in {A,B,C,D}, and
preD in {A,B,C,D,E}. They are disjoint. Every letter is injective
outside K. Some letter supplies preC=D, and some supplies preD=E.
A preC=D supplier collapses D into C, so {1,2} is in P1.
There are 16 individual fields for E5 and 12 for E15; all are used.

If preD=D, the three preA/preB/preC groups are the H singletons;
the letter permutes H and O and maps D into D. Call it D-preserving.
If preC=D, then preD is a singleton p in H, or (only for E5) {e}.
The O-output group has |O| inputs, all outside K, so the full image
contains O. For p in H, the letter permutes O. For p=e, the O-output
inputs are one H point and O-{e}; this letter need not preserve O.
Every remaining letter has preD=E and the three H singleton columns.
Call these letters T. The inputs O-{e} inject into O, omitting exactly
one hole h; inputs of D outside E also map into O.

## E={e}

Here J=H union {e} is mandatory through seven and isolated in P7.
Choose a preC=D supplier M, with preD(M)={p}, p in J, and put d=pM
in D. For each T, both D inputs map into O. If dT is not the hole h,
some x in O-{e} has xT=dT. Since O is contained in QM, choose q
with qM=x. Then q differs from p and MT merges the pair {p,q} touching
J in two steps. This contradicts isolation. Thus dT=h for every T,
and consequently O is contained in QT for every T.

Every entering letter now has its full image containing O; its exact
preD is a singleton in J. D-preserving letters permute O. The only
possible immediate kernel outside D is a mixed pair {k,x}, k in D,
x in O, under a T letter. Strong connectivity makes every D state
reachable from outside D. At the last entrance the input p is in J;
afterwards only D-preserving letters can keep the path inside D.
Since D has two states, a shortest such suffix u has length at most one.
Thus pLu=k with |Lu|<=2, and O is contained in QLu. Choose q with
qLu=x; then LuT merges {p,q} within three, again contradicting P7
isolation. No arbitrary entering-letter prefix is claimed to preserve O.

So all immediate kernels are inside D. Every letter has preD=D or a
singleton. The closed-merging-block lemma traps every mergeable pair
inside D, ruling out synchronization. This excludes E5.

## E={1,e}

Here J=H is mandatory through seven and isolated in P7. Choose suppliers
M0 with preC=D and T0 with preD=E. Since E meets D, every preC=D
supplier has preD={p} for p in H and permutes O. Both 1 and e map
under T0 into D, which M0 collapses, so {1,e} merges under T0M0.

Every preC=D letter M must send its unique entering p to 2. If pM=1,
choose q in O with qM=e; then MT0M0 merges {p,q} within three.
In particular fix p0 with p0M0=2. No D-preserving letter F can send
2 to 1: such F permutes O, so take x in O with xF=e and q in O
with qM0=x. The word M0FT0M0 would merge {p0,q} within four.

For every T letter, the remaining guard input 2 maps into O. It must
fill the unique hole h of the injection O-{e}->O. Otherwise some
x in O-{e} has xT=2T; choosing q in O with qM0=x makes M0T merge
{p0,q} within two.

No T can send e to 1. If eT=1 and h differs from e, choose
x in O-{e} with xT=e. Then TT0M0 merges the distinct pair {e,x}
entirely outside K within three, contradicting the P5 cover. If instead
h=e, then 2T=e and eT=1. Choose q in O with qM0=e; M0TT0M0
merges {p0,q} within four, contradicting isolation of H.

Now examine every possible predecessor of state 1. A preC=D letter
enters D only at 2. A D-preserving letter cannot send 2 to 1, and its
only D inputs are 1,2. A T letter has preD={1,e}, with e forbidden
from mapping to 1. Thus the only possible predecessor of 1 is 1
itself. This contradicts strong connectivity. This excludes E15.

Both proofs use the full individual field schema and suppliers, not
binary capacity or sampled failures. The E15 argument needs only
the P3 cover and H isolation through four; the accepted stronger
hypotheses imply these. E5 uses synchronization only after the
closed-block case; strongly connected nonsynchronizing controls are
allowed there. Initial-image reachability is not an extra premise
of these conditional obstructions.

Independent controls reconstruct every individual row at n6,7,8,9;
for n6..8 they completely check ordered binary alphabets having both
suppliers, including alphabets where one letter supplies both D and
E. Seeded larger alphabets support but do not prove the paper result.
The checker evaluates each short contradiction word directly and
uses a separate reverse pair BFS. In the E5 closed case it independently
checks that every mergeable pair lies in D. No uint64 initial-family
mask is used: the actual 70-set E5 family is kept as literal Python
sets. No whole third exclusion is recorded until full composition
and transport checks cover both E geometries and all labels.
