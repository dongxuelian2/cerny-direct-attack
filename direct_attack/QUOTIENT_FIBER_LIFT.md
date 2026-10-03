# A bounded-fiber quotient lift

**PROVED (elementary conditional bound); priority OPEN.** This is a
necessary-condition result for a state-minimal counterexample, not an
unrestricted proof of the Cerny conjecture. Words act on the right.

Let A be a synchronizing n-state DFA and let theta be a congruence with
classes C_1,...,C_m, where 1<m<n. Assume its quotient admits a reset word
of length at most B. Set

    M(theta) = sum_i (2^|C_i| - |C_i| - 1).

Then

    rt(A) <= B + M(theta).                                      (1)

Indeed, a quotient reset word u puts Qu inside one theta-class. Every
subsequent image of Qu remains inside one theta-class: this is precisely
congruence compatibility. The directed subset graph on the non-singleton
subsets contained in individual classes has M(theta) vertices. Since A is
synchronizing, Qu has a path to a singleton. A shortest such path repeats
no non-singleton subset and hence uses at most M(theta) letters. This
proves (1). It does not assume that Qu equals its containing class, that
individual classes are invariant, or that A is strongly connected.

For a state-minimal hypothetical counterexample, the smaller synchronizing
quotient obeys the square, so B=(m-1)^2 is available. Thus every nontrivial
congruence of such a counterexample must satisfy

    M(theta) > (n-1)^2 - (m-1)^2
             = (n-m)(n+m-2).                                   (2)

## Rank-truncated lift in the strongly connected case

Suppose A is also strongly connected, so its quotient is strongly
connected. For h>=1 define

    V_h(theta) = sum_i sum_(k=2)^min(h,|C_i|) binom(|C_i|,k).

Let u be ANY quotient reset word ending in class C_t. Choose a class C_j
and a shortest quotient-state path v from C_t to C_j, of length d(t,j)
at most m-1. The actual image Quv lies in C_j and has rank at most
h=|C_j|. All later ranks are at most h, and all images stay inside a
single congruence class. A shortest residual path to a singleton repeats
no eligible non-singleton subset. Therefore

    rt(A) <= |u| + d(t,j) + V_|C_j|(theta).                 (3)

One may minimize over j and over quotient reset words u. In particular,
if the quotient has a reset word of length at most B and s is its
smallest class size, then

    rt(A) <= B + (m-1) + V_s(theta).                        (4)

The transport cost is explicitly charged. It is zero if u already ends
in a smallest class. For the n=4 counterexample below, V_2=2 and u=b
ends in such a class, so (3) gives 1+0+2=3, exactly its reset threshold.
The coarser (4) would give 4; (1) also gives the exact 3.

For s=1, (4) is strictly below (n-1)^2 whenever m>=2 and
B<=(m-1)^2. For s=2 put d=n-m>=1. Then

    V_2 = sum_i binom(|C_i|,2)
        <= (n/2) sum_i(|C_i|-1) = nd/2.

Subtracting the upper estimate (4) from the square leaves at least

    d(n/2+m-2) - (m-1).

Since n>=m+1 and m>=2, the parenthesis is at least 3(m-1)/2;
the remainder is therefore positive. This independently reconstructs
the qualitative published 1/2-class lift. No priority claim is made.

## Pair-truncated lift and three-state fibers

Put P(theta)=sum_i binom(|C_i|,2). Every unordered pair initially inside
one congruence class stays inside some class until it merges. Because A
is synchronizing, a shortest merger path exists; it cannot repeat any of
the P(theta) nonmerged pairs. Its length is at most P(theta). From any
subset of rank at most h inside a class, merge an arbitrary pair and
repeat. Rank never increases, so at most h-1 mergers suffice. Using the
same quotient reset word and charged class transport as (3) proves

    rt(A) <= |u| + d(t,j) + (|C_j|-1) P(theta).            (5)

One should take the minimum of (1), (3), and (5), not sum their costs.
For class sizes (4,7), (5) gives 1+1+3(6+21)=83, strictly below the
square 100. The full-subset count and (4) do not settle this profile.

In fact, (5) strictly lifts the square whenever the smallest class has
size three. For m=2, let the other class have size t>=3. A quotient reset
costs at most one, class transport at most one, and P=3+binom(t,2).
The resulting upper bound is t^2-t+8, while (n-1)^2=(t+2)^2;
their difference is 5t-4>0. For m>=3, put d=n-m and note that every
class then has size at least three, so d>=2m. Since
P<=nd/2, the difference between the square and (5)'s coarse estimate
with |u|<=(m-1)^2, d(t,j)<=m-1 is at least

    d(m-2) - (m-1) >= 2m(m-2)-(m-1) > 0.

Thus **a state-minimal counterexample cannot have ANY congruence class
of size at most three**: sizes one and two follow from (4), and size
three from (5). The same strict conditional result applies to a
square-extremal automaton whenever its quotient obeys the square.
The conclusion still leaves simple automata and larger-fiber quotients.

This is a computable rigidity condition on the entire fiber-size profile.
In particular, if all classes have sizes between 3 and 6, (2) is impossible.
For m=2, direct checking of the ten unordered pairs of sizes in {3,4,5,6}
shows M <= (n-1)^2-1; the closest cases are (3,6), with 61<=63, and
(6,6), with 114<=120. For m>=3, each summand satisfies

    2^s-s-1 <= (s-1)(n+m-2),  3<=s<=6.

To see this, n>=3m. If s<=5, n+m-2>=10 and the largest ratio
(2^s-s-1)/(s-1) is 26/4. If s=6, n>=3m+3,
so n+m-2>=13>57/5. Summing proves the inequality.

Rodaro--Venturi, Proposition 3.1, already proves the qualitative 1/2-class
lift. Since a state-minimal counterexample is strongly connected,
combining the independent (4) argument with (2) gives: **every
nontrivial congruence of a state-minimal
counterexample has a class of at least seven states.** This is only a
necessary condition; simple automata have no nontrivial congruence.
The pair bound (5) above gives the stronger independent restriction that
*each* class has at least four states.

There is a sharper distinction when theta has at least three classes.
If all classes have sizes 3..7 and m=3 or 4, the 105 unordered size
profiles satisfy (2)'s opposite inequality by direct integer enumeration.
For m>=5, put d=n-m. If no class has size 7, each summand of M is at most
(57/5)(s-1), while n+m-2>=4m-2>=18. If some class has size 7, every
summand is at most 20(s-1), while n>=3m+4 implies
n+m-2>=4m+2>=22. Hence (2) is impossible for every m>=3.
Combining again with the self-contained 1/2-class result: **a nontrivial
congruence of a state-minimal counterexample has a class of size at least
seven if m=2, and at least eight if m>=3.**

The counted inequalities are in fact strict. For m=2, class sizes 3..6,
the smallest square slack after subtracting M is 2, at (3,6). For m=3,4,
sizes 3..7, the smallest is 8, at (3,7,7). The m>=5 inequalities above
also have strict slack. Rodaro--Venturi's 1/2-class proof is strict for
n>=3. Consequently, if a strongly connected synchronizing A has a
nontrivial congruence whose quotient obeys the square, then A cannot be
*square-extremal* when its largest class is at most six; with m>=3 the
threshold is seven. The qualifier about the quotient is essential here.

The full-subset count (1) alone stops at seven: the profile (3,7) has
M=124 and square slack 80. But (4) uses only V_3=4+56=60 and gives
rt(A)<=1+1+60=62<81 if its two-state quotient obeys the square and A is
strongly connected; (5) sharpens that upper bound to 50. Formula (5)
also excludes (4,7) with bound 83<100. Thus a two-class congruence with
maximum class size seven in a state-minimal counterexample must have its
other class of size at least five. A failure of a counting criterion is not an automaton
violating the square. The new bound and corollary are not
claimed to be new in the literature. They refine the repository's earlier
blanket warning that quotient synchronization has an uncontrolled tail.

The frozen 20260930 sample contains 230 synchronizing two-class lifts over
all ten unordered profiles with sizes 3..6. An independent reverse-subset
Bellman checker verifies each complete DFA, its quotient action, reset
distance, post-quotient tail and both inequalities; it also enumerates
all 5440 ordered profiles of three through six classes in this size range,
plus the 105 unordered m=3,4 profiles with class sizes 3..7.
These checks audit the statement and its arithmetic, but do not replace
the general proof or exhaust the automata in any class.

Primary context: [Rodaro--Venturi, *The hereditariness problem for the
Cerny conjecture*, Proposition 3.1 and Section 3](https://arxiv.org/pdf/2509.17992).

## A stronger additive lift fails at the smallest possible state size

**REFUTED:** the tempting assertion

    rt(A) <= rt(A/theta) + (max_i |C_i|-1)^2

even for strongly connected synchronizing A. At n=4 take

    a=[2,3,0,1], b=[1,0,0,0],
    C_0={0,1}, C_1={2,3}.

The quotient has a swapping letter a and a constant letter b, so its reset
threshold is 1. On Q, b yields {0,1}; a sends this set to {2,3}; then b
merges it. The word bab resets in three letters. No word of length at most
two resets: a preserves Q, b gives {0,1}, and both a and b preserve its
cardinality at the next step. Thus rt(A)=3>1+(2-1)^2=2. A is strongly
connected: from 0, b reaches 1, a reaches 2, and ba reaches 3.
The residual set must *move to another fiber* before it can merge.

This is state-minimal over arbitrary alphabets within the stated SC class.
At n=2 there is no proper nontrivial congruence. At n=3 such a congruence
has classes of sizes 2 and 1. The quotient is a strongly connected
two-state synchronizing DFA and therefore has a one-letter reset. If it
lands in the singleton class, it resets A. If it lands in the doubleton,
strong connectivity of the two-state quotient gives a one-letter move to
the singleton class, so A resets in at most two letters. That is the
proposed additive bound for max class size two. A complete unary/binary/
ternary n=3 scan independently checks 3714 qualifying ordered alphabet/
congruence designations with no violation; the all-alphabet minimum rests
on the preceding short proof.

The counterexample does not challenge (1): here M=2, so its valid bound
is rt(A)<=1+2=3, attained exactly. This shows why the proof counts
non-singleton subsets in *every* congruence class.
