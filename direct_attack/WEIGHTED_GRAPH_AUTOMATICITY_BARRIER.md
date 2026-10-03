# A residual graph can fail while the actual extension is short

2026-10-03. **REFUTED:** automatic strong connectivity of the original
triangular-power/three-a residual graph in WEIGHTED_GRAPH_SQUARE.md.
The sufficient theorem and its prime-half-core corollary remain valid.
General weighted M-extension, ordinary RP and Cerny remain OPEN.
All literal controls below are COMPUTATIONALLY VERIFIED, not formal.

The new synchronizing n25 input is

    a=[24,2,9,4,11,5,18,10,3,8,1,13,
       24,14,21,16,23,17,6,22,15,20,7,19,0],
    b=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,0,24].

Let S be the root plus all EVEN core states, mask22369621, ordinary
size13 and weighted mass14. Its triangular gcd is h2. The COMPLETE
original residual graph of words a b^j a b^k a b^s of cost<=24 has
exactly these nonloop edges on even/odd/root labels:

    root -> even, root -> odd, even -> root.

The odd vertex cannot reach either other vertex. The selected set
{even,root} has no entering edge. The 792 original triangular words
also have mass difference0 on S. Thus the former automaticity conjecture
is objectively false, including a synchronization premise.

This is NOT a weighted M-extension counterexample. The unrestricted
minimum is9, attained by

    a b a^2 b a^2 b a.

The actual inverse target is mask29684111, mass15, and still contains
the root. Consequently the ordinary ROOT-POSITIVE minimum also is9.
An independent sparse cut has373 vertices and378 checked closure edges;
all words of length<=8 fail even the weaker weighted goal. The literal
witness attains it. A separate actual reset of length119 proves the
input is synchronizing and itself satisfies square576.

The exact weighted minimum among ALL words with at mostTHREE a is25,
attained by a b^10 a b^11 a b. The independent check exhausts1152
canonical three-a forms and52 zero/one/two-a controls; eight three-a
forms succeed. No implicit root-retention restriction is used for
this weighted lower bound.

The finite pool a b^j a^k b^s with ACTUAL total cost<=24 has minimum15
on this S (529 checked canonical forms). The original triangular pool
had insisted on j+k<=L so that every L-shift was affordable. Permitting
the shorter final period-two tail recovers an upper word; it does not
prove that this enlarged pool works for all inputs.

## Provenance and next mathematical obstacle

The new late-block/strict-low-output native pressure found this row
after81619 accepted mixed proposals at M24, stopping immediately.
Six other parameter streams ran1000000 proposals each. All6081619
proposal counts remain EXPLORATORY. Only their six retained PASS peaks
and this counter receive independent literal checks; empty larger
retained scopes are not absence theorems. The counter is rechecked
without importing its generator, and six corruptions are rejected.

Old captures reporting automatic connectivity as CONJECTURED/OPEN
are historical checkpoints. This later literal REFUTATION supersedes
that status while preserving the successful finite M12 criteria and
every proved sufficient square theorem.

A possible continuation is to use the ACTUAL period of the target when
charging final b shifts, rather than reserving all L rotations. The
inverse-class and early-mix shortcuts remain false. Neither the new
pool nor a complete general weighted extension proof is asserted here.
