# Short rooted words and a single-letter power template can fail

Date: 2026-10-01. The proposed short-rooted-word lemma is **REFUTED**
by an exact finite certificate, **COMPUTATIONALLY VERIFIED** with a
separate literal evaluator. No minimum-state, priority, or
**FORMALLY VERIFIED** claim is made. Cerny's conjecture remains **OPEN**.

A transformation is called rooted here if some positive power is
constant. Equivalently its functional graph has exactly one directed
cycle, a fixed point; its height is the largest distance into that root.
This definition does not allow a unique nontrivial cycle to count as
rooted. If a rooted actual word v has height H on Q, v^H resets it,
with ORIGINAL cost H|v|. An entering prefix can reduce the relevant
height, but that prefix must also be paid.

After the reflected-return construction, a tempting generalization was:
every SC synchronizing n-state DFA has a rooted word of length <=n.
This would at least give a universal quadratic reset bound by taking
a power. It is false, even for a binary four-state automaton:

    a=[0,0,1,3],       b=[3,1,3,2].

All 31 literal binary words through length four, INCLUDING the empty
word, give 22 different transformations. None is rooted. The word

    v=a a b a b

has length five and row `[2,2,2,1]`. It is rooted at state 2 with
height exactly two: v itself has rank two, while v^2 is constant.
Thus the exact shortest rooted-word length is five, greater than n.
The enumeration through four is complete, not a truncated semigroup
search, and the positive five-letter witness proves attainability.

The whole DFA is strongly connected and synchronizing. Its actual
reset word

    a a b a b a a

has length seven; ordinary full-image BFS verifies rt=7, below the
square nine. The shortest rooted word's pure power costs ten, whereas
a shorter compatible varying suffix resets. Neither the Cerny square
nor a prefix-plus-rooted-word budget is refuted by this example.

It also refutes a more direct proposed square construction: choose ONE
letter x and an actual word v of length <=n so that x v^(n-2) resets.
Such a certificate would have cost at most 1+n(n-2)=(n-1)^2. On this
four-state DFA, none of the 62 choices (two prefix letters times all
31 words through length four) makes x v^2 constant. This test permits
EVERY v, including transformations with nontrivial cycles; it does not
merely reject v for failing the rooted definition. Thus even that
single-prefix repeated-word template cannot replace a general compatible
schedule. Longer prefixes, longer repeated words, and different suffixes
are outside the refutation. The displayed seven-letter reset remains valid.

The lesson is precise: semigroup synchronization guarantees the
existence of rooted transformations (a reset word already supplies
one), but does not put a rooted word within original length n. A
general proof must control BOTH actual word cost and the height on the
entered image, or use a different compatible sequence. The public
family proof in PUBLISHED_COMPRESS_OTHER_FAMILY.md supplies those
quantities for its explicitly realized return structure only.

check_short_rooted_word.py imports none of the preceding generators or
solvers. It retains every short action, tests rootedness by literal
fourth powers, checks both positive words, recomputes rt/SC, and rejects
five deliberately corrupted fields. The complete certificate is in
data/short_rooted_word_checks.json.
