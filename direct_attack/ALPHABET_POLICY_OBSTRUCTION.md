# Image policy can become worse when letters or word shortcuts are added

**REFUTED, state-minimal n=4 over any finite alphabet:** the global policy
P(A)=min_q G_A({q}) need not be nonincreasing under alphabet inclusion.
The failure also occurs when the added transformation is already induced
by an actual word, so the complete monoid and reachable-image family stay
the same. This refutes neither the global policy square target nor Cerny.

## The stronger failure with the monoid unchanged

On Q={0,1,2,3}, take right-action rows

    a=[1,0,0,2], b=[1,2,3,0],
    c=[2,0,1,2]=b^2 a b^3 a.

The equality is equality of transformations on EVERY state. The shortest
word inducing c in {a,b} has length 7, independently checked by complete
individual-transformation BFS. Adding c as a one-step letter preserves
the entire transformation monoid (176 elements, computationally counted)
and image family. Both alphabets are SC synchronizing: b is a full cycle
and aaba resets Q in length 4.

The image family is all 15 nonempty subsets. The triples are rotations of
Qa={0,1,2}; Qaa={0,1} supplies all four adjacent pairs by b rotations;
Qaba={0,2} supplies both diagonal pairs. Q aaba={0}, then b rotations
supply all singletons. This is a paper reachability argument.

Independent set BFS / all-tie recurrence gives:

| Quantity | alphabet {a,b} | alphabet {a,b,c} |
|---|---|---|
| Exact reset threshold | 4 | 4 |
| G({0}),G({1}),G({2}),G({3}) | 4,5,6,7 | 5,6,6,7 |
| Global minimum P | 4 | 5 |
| e({1,2}) | 2 | 1 |
| G({1,2}) | 3 | 4 |

The mechanism is exact. Originally T={0,1,2} is reached from Q by a,
so G(T)=1; its word ab maps T onto {1,2} with cost 2. Hence the old
cost there is 2+1=3. No one-step extension into {1,2} exists originally.
After adding c, T'={0,2,3} maps onto {1,2} in one step. It is the ONLY
larger image qualifying in one step: b preserves cardinality and a maps
every triple to a set containing 0. Thus the policy must take T'.
It has G(T')=3, making the new cost 1+3=4. After one or two letters
the possible proper full-Q images are {0,1,2}, {1,2,3}, {0,1}; none
is contained in T'. The word ab^2 reaches T' in length 3, proving that
top-rank cost. Finally e({0})=1 has only the larger endpoint {1,2},
so G({0}) rises by one. The other singleton values above independently
exclude another initial singleton repairing this increase.

All old exact transport distances weakly decrease: every old word is
still present. On every old image, e_new<=e_old as well. The independent
checker finds 64 strict improvements of exact image-to-image distances,
yet the minimum policy becomes worse. The phase restriction, rather than
failure to improve distances or loss of images, causes the increase.

## A separate failure that adds reachable images

The earlier first failure in the arbitrary-map scan is

    a=[0,0,2,2], b=[1,3,0,2], c=[0,0,2,1].

Its global policy rises from 3 to 4 while rt remains 3. The image family
grows from 9 to all 15 nonempty subsets. The base has no proper reachable
image larger than a pair, whereas the added letter has rank 3. This example
is retained separately; the actual-word example above does not need image
family growth.

## Why four states is minimal: a positive policy theorem

**PROVED on paper.** If a strongly connected synchronizing DFA has no
proper reachable image of size >2, then P(A)=rt(A). Equivalently for n>=3,
every nonpermutation letter has rank <=2. For n=1 the empty word gives 0;
for n=2 a synchronizing DFA has a constant letter and gives 1.

If a constant letter exists, both costs are 1. Otherwise take a shortest
reset w of length L. Its last proper prefix has image U of size 2: a
nonpermutation has already appeared, and a singleton at an earlier prefix
would contradict shortestness. Let the last letter map U to {q}.
Then e({q})=1, with U an allowed larger endpoint. The only image larger
than U is Q, so G(U)=e(U)<=L-1, using the actual prefix word sending Q
into U. Consequently G({q})<=1+G(U)<=L. Every policy constructs a reset
word, giving rt(A)<=P(A), and equality follows. The proof allows arbitrary
alphabet size, inverse cardinality losses and transport into proper subsets.

Every DFA with n<=3 satisfies this image-rank hypothesis. Thus P=rt for
every SC synchronizing DFA in that range, and alphabet inclusion cannot
increase P because it cannot increase rt. This proves the four-state
minimum over ANY alphabet, beyond the small binary augmentation covers.
The n4 word-shortcut example also shows that the rank cap 2 cannot be
replaced by 3 in this policy-optimality theorem. This is a conditional
policy theorem, not a new general synchronization bound.

## Exact evidence and proof boundary

The binary first-map cover at n=2,3, with every extra transformation,
checks 16 and 1593 additions. Restricting additions to the full generated
monoid checks 15 and 899. The n4 scans STOP at the first failure, after
83978 arbitrary and 34227 generated additions; they are not full covers.
Repeated-letter additions are included and harmless; covering counts
overlap and are not unique isomorphism-class counts.

Both complete base/augmented e, best and worst arrays, actual reset words
and phase words are retained. The checker recomputes policies using
ordinary inverse-set BFS, exact set transport using forward BFS, strong
connectivity, the complete 176-element monoids and the actual seven-letter
transformation. Three deliberately corrupted fields are rejected. Negative
search counts use the enumerator, not a second complete enumeration;
state-minimality rests on the paper rank-two theorem. No new Lean result.

The global square policy remains OPEN. Standard letter-deletion arguments
for Cerny use monotonicity of rt. For a hypothetical failure of the POLICY
square bound, deleting a letter can lower P even while synchronization is
preserved. Thus that standard argument alone does not produce an
alphabet-minimal policy failure. This does not alter the valid alphabet
reduction for an actual Cerny counterexample or give a square-bound failure.

There is a valid cost-preserving macro statement. Add finitely many
nonempty actual words as new labels, assigning each its ORIGINAL word
length as positive weight. Every weighted word expands into an old word
of the same total length; conversely every old word remains available.
Thus the monoid, image family, every transport distance, e, the sets of
shortest allowed endpoints, and G are all unchanged. This is a direct
word-expansion observation, not a new synchronization bound. Assigning a
seven-letter word cost 1 changes those distances; the example defeats the
stronger hope that this improvement at least monotonically improves P.
The image-extension framework is known from
[Kisielewicz--Szykula 2016, Section 3.1](https://arxiv.org/pdf/1608.01268).
Priority of these exact policy obstructions and conditional theorem is OPEN.
