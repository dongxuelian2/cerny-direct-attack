# Even the unique globally shortest binary reset can have dependent indicators

Date: 2026-10-01. **PROVED (paper)** with a separate
**COMPUTATIONALLY VERIFIED** finite certificate. No **FORMALLY VERIFIED**
claim. Priority is **OPEN**. General Cerny and global policy square remain
**OPEN**. No positive-fraction dimension or long-phase tradeoff refutation.

The immediately preceding n5 audit refuted independent OPTIMAL locally
shortest actual-image policies, but its two witnesses still had independent
NONGREEDY shortest reset words. We continued and now refute that weaker
existence repair as well, using a new simple strongly connected binary
example. The distinction about those earlier witnesses remains correct.

## The exact automaton and a paper uniqueness proof

On Q={0,1,2,3,4}, use ORIGINAL letters

    a=(2,1,1,4,3), b=(3,0,1,1,2).

Both have rank four. The only collision of a is {1,2}, with image 1
and missing state 0. The only collision of b is {2,3}, with image 1
and missing state 4. Thus any original letter decreases the size of
ANY current subset by at most one, giving rt>=4. Literally

    Q --a--> {1,2,3,4} --b--> {0,1,2}
      --a--> {1,2} --a--> {1}.

Hence rt=4. Moreover **abaa is the UNIQUE shortest original reset word**.
Indeed the full inverse history of any length-four reset must increase
by exactly one at EVERY letter, from singleton to Q. The only possible
first growths are:

| Current target | Inverse letter | Larger full preimage |
|---|---|---|
| {1} | a | {1,2} |
| {1} | b | {2,3} |

Neither letter grows {2,3}: both inverse preimages are {0,4}.
From {1,2}, a gives {0,1,2}, while b gives {2,3,4}. Neither letter
grows {2,3,4}: a gives {0,3,4} and b gives {0,4}. From {0,1,2},
a does not grow and b gives {1,2,3,4}. Only a grows that four-set to
Q; b does not. Thus the ONLY all-growing inverse label sequence is
a,a,b,a, equivalent to the original forward word abaa. This argument
covers every reset endpoint and every original length-four word.

The automaton is strongly connected. From 0 one reaches 2 by a, 1 by
ab, 3 by b and 4 by ba. Conversely 1 reaches 0 by b, 2 by bb,
3 by bb, and 4 by bbb. Both unary subalphabets are nonsynchronizing:
a has the fixed state 1 and the separate cycle (3,4); b has the
three-cycle (0,3,1). Thus both original letters are necessary.

## No nontrivial state congruence

Every distinct pair can be taken to {1,2} without collapsing it:

| Pair | Original word |
|---|---|
| 0,1 | a |
| 0,2 | a |
| 0,3 | ab |
| 0,4 | aaba |
| 1,2 | empty |
| 1,3 | ba |
| 1,4 | ba |
| 2,3 | aba |
| 2,4 | b |
| 3,4 | b |

These ten words are literal finite certificates. Any nontrivial
congruence therefore identifies 1 and 2. Applying b identifies 0 and
1; applying b to 0 and 1 adds 3; applying a to 0 and 3 adds 4.
The congruence is universal. The DFA is consequently simple. This is
state congruence simplicity, with no stronger semigroup assertion.

## The dependence survives every optimization of the reset word

In state masks the unique inverse growth history is

    2 -> 6 -> 7 -> 30 -> 31.

All its proper stages are ACTUAL images: forward prefixes of abaa give
Q,30,7,6,2. Every reverse stage has exact actual-image local e=1,
since a zero-cost transport from a larger set is impossible. Hence the
same chain is an optimal compatible image policy, with P=rt=4. Any
cost-four policy must compose to abaa and start at its reset endpoint.
Each successive target on its inverse path has e=1, and an original
inverse letter can grow by only one, so its actual larger parent equals
that full preimage. This forces every cut and the same endpoint chain.

The three proper growth indicators obey

    chi_6 + chi_31 = chi_7 + chi_30.

Raw rank after adjoining Q is three; normalized rank is two. Even
adjoining the initial singleton, and counting ALL letter-level intermediate
preimages, gives raw rank only four for five vectors. There are no
non-growth intermediates here: each phase is one ORIGINAL letter.

Thus existence of a fully independent proper record-growth history among
globally shortest original reset words is **REFUTED**, including simple
SC irreducibly synchronizing binary inputs with rt=n-1. Allowing locally
longer phases cannot change the unique shortest original word. This
strengthens D3's policy obstruction and does not use a greedy choice.

Five states are minimal for this PROPER-STAGE assertion over ANY finite
alphabet: at n<=4 there are at most two proper record-growth sets, of
strictly increasing sizes. Two distinct proper indicators together with
Q can be dependent only if the two sets are complements. The only
two-stage case at n4 has sizes two and three, summing to five, so that
cannot happen. The exact Boolean proof is also given in
OPTIMAL_PHASE_INDEPENDENCE_REFUTATION.md. It applies equally to the
unrestricted record-growth convention with temporary shrinking.

## Counting the initial singleton is a different question

A separate SC binary n3 control has

    a=(1,0,0), b=(1,2,1).

Its unique shortest word is ba, of length two. Both letters have rank
two, so no one-letter reset exists. The only growing inverse path to
Q is {0} --a^-1--> {1,2} --b^-1--> Q. These THREE full-history vectors
obey chi_{0}+chi_{1,2}=chi_Q and have raw rank two. Its ONE proper
stage has normalized rank one and is independent. This is NOT a
three-state counterexample to the proper-stage assertion above.

At n2 a synchronizing DFA must contain a constant original letter,
because every other nonconstant transformation is a permutation. A
shortest reset then has length one and its singleton/Q indicators are
independent. Thus the full-history assertion INCLUDING the initial
singleton already has a state-minimal n3 failure. The two conventions
must not be silently interchanged.

## Independent verification and research boundary

`shortest_binary_independence.py` uses forward subset BFS, exhaustive
original words and rational Gaussian ranks. `check_shortest_binary_independence.py`
imports neither it nor another policy checker. It enumerates ALL +1
inverse growth branches (11/6 tree vertices), using the paper rank-defect
lower bound to make this exhaustive for shortest words. It also runs
EACH original state literally through ALL 16/4 original words at the
two lower bounds. All 76 letter/subset rank-defect controls, six ranks
by integer Leibniz determinant minors, all actual images (19/6), SC
paths and the ten simplicity pair words are verified independently.
Seven deliberate corruptions are rejected.

This is check105 / regeneration189. The previous104-check record is
preserved verbatim; only the new generator, replay and checker continue.
No full105 rerun or formal kernel. The proof is a small exact obstruction
to a quantified dimension assertion, not an asymptotic reset lower bound.
Positive-fraction guarantees for optimized histories, dimension versus
EXPENSIVE-phase costs, and general quadratic compatibility remain OPEN.
The informal 2026 dimension question is not declared wholly settled.
