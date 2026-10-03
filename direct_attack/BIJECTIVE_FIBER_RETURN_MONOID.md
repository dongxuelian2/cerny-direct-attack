# Short return monoids with bijective transport between equal classes

Date: 2026-09-30. **PROVED (paper)** under the explicit transport
hypothesis below. Priority is **OPEN**; the finite literature search does
not establish novelty. **COMPUTATIONALLY VERIFIED** applies only to the
saved finite certificates. No **FORMALLY VERIFIED** statement is added.
The unrestricted Cerny conjecture and general congruence hereditariness
remain **OPEN**.

## 1. Entire return monoid, not just a synchronizing basis

Let a DFA have a congruence with m>=2 classes, each of size h>=2.
Make a directed graph J on these classes: include a labeled edge D--a-->E
exactly when the restriction of a from D to E is a BIJECTION. Assume J
is strongly connected. A letter may be bijective on one class and
singular on another; global permutation letters are not required.

Fix a class C. Let p_D be a shortest path in J from C to D, and r_D
a shortest path from D to C; p_C=r_C=epsilon. These word restrictions
are bijections. Form a return alphabet B on C using the actual words

    p_D a r_(Da)             for every class D and letter a,
    p_D r_D                  for every D != C.                 (1)

Duplicates may be removed. There are at most m|Sigma|+m-1 generators.
Every word in (1) is a FIRST return to C: its two shortest routing
paths have no internal visit to C. Let L be the maximum length in
(1). Then L<=2m-1, and

    M(B) = {w restricted to C : Cw subset C}.                  (2)

The right-hand side includes the identity and all word lengths.
Thus B synchronizes iff C can be reset in the original DFA. Neither
strong connectivity of the base DFA nor synchronization is needed
for the monoid equality itself.

Proof. Use p_D as an abstract coordinate bijection C->D. For an
edge D--a-->E, define the coordinate transformation

    f_(D,a)=p_D a p_E^(-1).

Here p_E^(-1) is initially an abstract bijection, not a free word.
The actual loop ell_E=p_E r_E is a permutation of C and is a B
generator (or the identity at E=C). Its inverse belongs to M(B),
because a permutation of a finite set has a positive-power inverse.
The other generator in (1) is

    g_(D,a)=p_D a r_E=f_(D,a) ell_E.

Consequently f_(D,a)=g_(D,a) ell_E^(-1) is in M(B). This argument
uses only transformation membership; it does NOT charge the inverse
as length zero or assert a short original word representing it.

Along any quotient path beginning and ending at C, the successive
coordinate transformations telescope: p_E^(-1)p_E is the identity
on E, and p_C is the identity. Their product is the original word
restricted to C. It lies in M(B). Conversely every generator of B
is an actual C-return word, and concatenations remain C-return
words. This proves (2).

The alphabet is constructible in polynomial time by class-graph BFS
and literal word composition. Enumeration of the full monoid is
used only in the finite audit, not in the construction or proof.

## 2. Conditional square lift and a general minimal-counterexample exclusion

Assume A synchronizes, its quotient has reset threshold R, and H(h)
is ANY proved reset bound for arbitrary h-state DFAs. By (2), B is
an actual synchronizing h-state DFA. Reset the quotient, route its
terminal class to C using J, and reset C using B. This pays the
quotient and class route once, and proves

    rt(A)<=R+dist_J(quotient reset endpoint,C)+L H(h)
          <=R+(m-1)+(2m-1)H(h).                              (3)

If BOTH the quotient and arbitrary h-state DFAs satisfy the square,
the bound is m(m-1)+(2m-1)(h-1)^2. Since n=mh,

    (n-1)^2-[m(m-1)+(2m-1)(h-1)^2]
       =(m-1)[(m-1)h^2+2h-m-2]>0.                          (4)

For h>=2 the bracket is at least 3m-2. This proves a strict lift
for EVERY m,h under those two smaller-state assumptions. A quotient
square assumption ALONE is not asserted to settle all h.

In a state-minimal Cerny counterexample both smaller-state squares
are supplied by minimality. Therefore EVERY uniform nontrivial
congruence in such a counterexample has a NON-strongly-connected
bijective-edge graph J. This all-n restriction is additional to the
earlier growing class-size floor; it includes arbitrarily large h.

In particular, a minimal counterexample cannot have a congruence on
which its permutation letters act transitively. Such transitivity
forces equal class sizes and makes J strongly connected. If the
permutation subgroup is transitive on all states, a minimal
counterexample must be SIMPLE as a DFA. This does not imply that
its permutation subgroup must be primitive: other letters may break
the group's block systems. It does not establish the square for
all automata with transitive permutation subgroups.

## 3. The cutoff 2m-1 is sharp, independently of h

For every m,h>=2 take states (i,j), 0<=i<m, 0<=j<h. Classes are
the fixed-i fibers. Define three letters R,L,c:

    R(i,j)=(i+1,j)                   if i<m-1;
    R(m-1,j)=(m-1,j)                 if j<h-1;
    R(m-1,h-1)=(m-1,0);
    L(i,j)=(max(i-1,0),j);
    c(0,j)=(0,j+1 mod h), c(i,j)=(i,j) if i>0.

The bijective-edge graph contains the two directed paths between all
classes, hence is strongly connected. The whole DFA is SC: move to
class zero using L, choose any fiber coordinate using c, and move
to any class using R without using its terminal loop.

A singular C_0-return must use R at class m-1. Reaching it needs
m-1 letters, the singular step needs one, and returning to zero
needs m-1 more. Thus every first return shorter than 2m-1 is a
permutation. At length 2m-1, R^m L^(m-1) is exactly the adjacent
unit collapse (h-1)->0 on C_0. Together with c it gives the usual
Cerny h-state alphabet. Thus the short return alphabet first
synchronizes at EXACTLY 2m-1. The usual macro square is attained
by this alphabet, although its actual letter costs are unequal.

The original DFA synchronizes: R^m maps ALL states to class m-1
and performs the adjacent collapse. The explicit word

    R^m (L^(m-1) c^(h-1) R^m)^(h-2)                         (5)

resets Q, with length m+(h-2)(2m+h-2). No exact original reset
threshold is claimed. This family also shows why a worst macro
cost times a macro reset length can overcharge the original problem.

## 4. Removing bijective connectivity fails even with uniform classes

For each odd h=2t+1>=3 use two h-classes C and O. Write both with
local indices 0,...,h-1. Define x(q)=0 for q<t or q=h-1, and
x(q)=t otherwise. Let a map C into O by x and cycle O by +1;
let b fix C and map O to C preserving its local index.

This DFA is SC: O cycles, b reaches every member of C, and a
exits C. Its bijective-edge graph has no path C->O.
First returns at C are b and a^(s+1)b, inducing identity and
x followed by the O-cycle shift s. Put B={0,t}, and color q by x(q).
For s=0,...,h-2, B+s has different colors; at s=h-1 both colors
are zero. This follows directly by splitting s into 0..t-1,
t..2t-1, and 2t.

All short nonidentity return images are B+s, 0<=s<=h-2. Applying
any further such return first applies x, so preserves their rank
two and returns them to this same pair family. Therefore the
first-return alphabet through length h is NOT synchronizing.
At length h+1 the shifted pair B+h-1 appears and the length-two
return ab merges it. Thus the exact synchronizing cutoff is h+1,
which equals n-h+1. An actual full reset is

    b a^h b a, of length h+3.                               (6)

Uniform congruences alone therefore admit NO return cutoff depending
only on the number m of classes. These examples refute removal of
the hypothesis of (2); they do not refute Cerny or a stronger class
reset bound such as (h-1)(n-1).

## 5. Verification and subsequent research

bijective_fiber_returns.py tests 3000 deterministic sampled alphabets
with h,m in {2,3,4}: all 3000 short/full return monoids agree;
2166 base DFAs synchronize and 834 do not. This is not a cover.
It retains 48 improving sample records, 30 sharp-cutoff controls,
and 10 nonbijective boundary controls. The exact subset reset
claims for small macro DFAs are checked, not assumed from the sample.

check_bijective_fiber_returns.py independently uses packed deterministic
matrix multiplication and ordinary reverse-subset distances. It
checks all 88 records, the smaller gauge alphabet as well as all
short returns, 17915 return-orbit vertices, 1120 reverse-subset
vertices, every literal lifted word, and four corrupted fields.
The family controls include full-Q resets and separate SC checks.
Neither implementation imports the other's return solver.

The coordinate-change argument is an elementary finite-semigroup
construction. The conditional quotient comparison is the context of
[Rodaro--Venturi](https://arxiv.org/abs/2509.17992), while general
short-return synchronization is proved separately in
SHORT_RETURN_QUOTIENT_LIFT.md. Exact priority of the present monoid
generation statement and exclusion remains OPEN.

The next unresolved cases are uniform congruences without bijective
connectivity, nonuniform classes, and simple automata. The inverse
permutations in section 1 do not give a length estimate outside the
finite macro alphabet; replacing them by inverse singular maps is
invalid. The stronger class-reset proposal from
PROFILE_CLASS_COMPRESSION.md remains OPEN. No universal n-only reset
or image-extension bound follows from the result above.
