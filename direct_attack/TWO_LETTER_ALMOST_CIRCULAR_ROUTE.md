# An actual return model for a two-letter almost-circular product

Date: 2026-10-02. Normal form below **PROVED (paper, elementary)**,
with no novelty or formal-verification claim. Its general square cost
consequence is **OPEN**. This is a next-route note, not a Cerny proof.
Do not conflate a completed permutation with an available original word.

Later FIXED_ROOT_CYCLE_EXTENSION.md proves the ORIGINAL square for
the entire subclass A(1)=1, by a direct paid n-extension construction.
It does not require the almost-circular product in its broader theorem.
The root-moving case A(1)!=1 remains OPEN at the square; removing that
condition from n-extensibility is independently REFUTED already at n4.

Consider a synchronizing binary n-state DFA, n>=3, with original letters
a,b. Assume b is a permutation, a has rank n-1 and level1, and ab has
one cycle of size n-1 and level1. The hypothesis on a's level is explicit;
a longer original tail is outside this normal form. Write r for a's
unique omitted image state, S=Q minus{r}. Since a has level1, a restricted
to S is a permutation A; a's unique collision pair is{r,s} for some s in S.

The image of ab omits b(r). Because ab has one tail vertex and level1,
its omitted state is one member of its unique collision pair. b is
injective, so that pair is still{r,s}. Hence b(r) is r or s. If b(r)=r,
both original letters preserve S and act as permutations on S, making
synchronization impossible. Therefore

    b(r)=s,       C=Q minus{s}=S b.

Complete a to a permutation abar by fixing r and agreeing with a on S.
Then a=u_(r->s) abar. Put G=abar b. G(r)=s, while G(s)=(ab)(s)=(ab)(r).
Every other transition of G agrees with ab. Thus G is obtained from ab's
cycle C by inserting s immediately after r, and is a FULL n-cycle.
This proves an exact transformation normal form. It does NOT make abar
or G available at cost1, or at any known small original cost.

Actual original returns to S are instead

    A = a|S,          cost1, a permutation;
    c = (b a)|S,      cost2, a full (n-1)-cycle;
    f = (b b a)|S,    cost3, rank n-2=|S|-1 on S.

The WHOLE-Q transformation bba still has rank n-1, since b is a
permutation. Its smaller rank above is explicitly the restriction to S.

The full cycle c follows by conjugating ab|C through the bijection b:S->C.
Every b^j a returns S into S, since the last a sends ALL Q into S. To
prove f's rank, note that b^2 S omits b(s). A loses rank on that image
unless its omitted state is r or s. b(s) cannot equal s, by injectivity
and b(r)=s. If b(s)=r, the b-cycle containing r has length2. Then after
the first a, b only toggles the omitted state r/s, while every subsequent
a returns an (n-1)-set omitting r and is injective on it. All words retain
rank at least n-1, contradicting synchronization. Thus b(s) lies outside
{r,s}; both collision points are present in b^2 S, and f has rank |S|-1.

The FULL original return monoid is circular via c and synchronizes because
an original reset followed by a is a return. Initially synchronization of
the chosen c/f subalphabet was left open. The quotient lifting argument
below now proves it. A or other b^j a returns nevertheless can be essential
for a SMALL PAID COST. Connected cycle translates of one kernel pair are
only a sufficient synchronization test; further f images cannot be ignored.
The proved information is an ACTUAL cheap full cycle plus an ACTUAL
cheap singular return, with all labels paid; neither a formal inverse of
A nor the completed G may be used as a free original operation.

For the retained n6/rt25 example

    a=[0,1,2,4,3,3], b=[1,3,5,0,2,4],

r5,s4,S={0,1,2,3,4}. It satisfies the normal-form hypotheses. The exact
cycle-entry pressure already found ab, cost2, level1, cycle size5,
followed by an original cycle reset of cost23, for a whole reset of25.
The cycle C is not invariant under every original letter; C a=S differs
from C. The return model keeps track of this movement rather than treating
C as an invariant five-state original DFA. These are retained finite
observations, not a new all-parameter cost theorem.

The unresolved task is to prove ONE paid reset of the return monoid on
S with cost at most (n-1)^2-1, then prepend the actual entering a. An
unweighted circular theorem on |S| states does not supply this because
c/f have costs2/3 and other returns may be longer. The generic macro
bound in PAID_ONE_CLUSTER_WORD_BOUND.md still approaches twice the square
here. A useful next step would exploit the relations forced by a,b and
G's completed cycle while keeping only actual return labels and their
costs. This class is a plausible intermediate route, not a universal
reduction: arbitrary potential Cerny counterexamples need not have an
almost-circular two-letter product or a level1 original singular letter.

## Chosen c/f synchronization: a quotient lifts back to the original DFA

This qualitative equivalence is **PROVED paper**, using the established
all-corank<=1 permutation-quotient theorem in
CORANK_ONE_STABILITY_QUOTIENT.md. Relabel the completed G-cycle as
0,1,...,M, M=n-1, with r0,s1. Then abar fixes0 and acts as a permutation
A on S={1,...,M}; a=u_(0->1) abar, b=abar^-1 G. Let H be the full cycle
1,...,M on S. Conjugation by A is ONLY a relabeling, never a paid word.
It transforms the actual return c into H and f into F, where

    P=H A^-1 H is a permutation of S,
    F(q)=P(q) for q!=M, and F(M)=1.

Put t=H^-1(A(M)). P(t)=1. If t=M, equivalently A(M)=1, then b swaps0/1,
and both original and return automata are nonsynchronizing, as shown above.
Otherwise F has unique kernel{M,t}, omitted image P(M), and rank M-1.

Suppose the circular all-corank<=1 return DFA{H,F} is nonsynchronizing.
Its established stable minimum-rank quotient is a nontrivial permutation
quotient. Since H is a full cycle, its classes are the residue classes
modulo some d>1 dividing M, all of equal size. F preserves those classes
and induces a permutation rho; its kernel points M,t have the same class0.
For every other class, P=F maps that whole class bijectively onto its
rho-image class. Since P is a permutation, its remaining images of class0
fill precisely the remaining rho(0) class. Thus P induces the SAME rho.
Consequently A=H P^-1 H also preserves the residue classes and induces a
permutation pi. A(M)=H(t) has class1, so pi(0)=1 modulo d.

Extend this partition to Q by putting the extra state0 into class1.
Original a preserves it: on S it induces pi, and a(0)=A(1) has class
pi(1), as required. Original b induces

    sigma(k)=pi^-1(k)+1 modulo d.

For core states, this follows from b=abar^-1 G. Its only exceptional
core transition, where abar^-1(q)=M and G sends M to0, has source
class pi(0)=1, and sigma(1)=1, exactly the assigned class of state0.
Also b(0)=1 has class1, consistent with sigma(1)=1. Thus the original
DFA has a nontrivial permutation quotient and cannot synchronize.
Contraposition proves that original synchronization forces chosen c/f
synchronization. The converse holds by entering S with original a and
expanding a c/f reset literally. This is a qualitative equivalence,
not a bound on its word cost.

## The paid c/f-only square shortcut fails at the retained n6 example

On its S={0,1,2,3,4}, the actual rows are

    c=[1,4,3,0,2], cost2; f=[4,0,3,1,3], cost3;
    A=[0,1,2,4,3], cost1.

The exact weighted reset cost using ONLY c/f is25. Prepending the entering
original a makes26, ABOVE the square25. Adding the actual A return gives
exact cost24, with entering a giving25. Thus synchronization of the two
cheap returns does not suffice for the proposed paid square certificate;
retaining other cheap original returns is essential even at six states.
This is a **REFUTED c/f-only method shortcut**, not a Cerny counterexample.
The finite weighted shortest costs are checked by complete subset Bellman
certificates, independently of discovery Dijkstra. The all-n cost theorem
for the full return monoid is still OPEN. No FORMALLY VERIFIED claim.

Completed finite independent audit:ALL872 normal-form permutations n3..7,
685 synchronizing inputs,277020 positive-cost subset Bellman edge controls
and173987 literal particle/letter controls. The entered c/f-only budget
exceeds the square in100 finite inputs, including the exact n6 obstruction.
Eight corruptions are rejected. This finite scope is COMPUTATIONALLY
VERIFIED, not an all-parameter computational or formal proof. Registry
130/211 preserves129 prior records and appends ONE checker; no full130
rerun. Native builds remain8. The all-n synchronization equivalence is
PROVED paper; the full-return paid square theorem remains OPEN.
The subsequent BOUNDED_CERNY_RETURNS_OBSTRUCTION.md refutes the fixed
THREE-return square shortcut as well: on ordinary Cerny n4 it costs11
after entering, above9. Indeed, for EVERY n>=4 the entire return pool
b^j a capped by j<n-1 must exceed the square. The all-length return
monoid and the class's general original-alphabet square bound remain
OPEN. The qualitative synchronization equivalence above is unchanged.
