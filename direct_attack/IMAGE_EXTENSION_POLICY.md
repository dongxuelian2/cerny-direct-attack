# Shortest image-extension policy: a surviving compatibility target

Status: universal square guarantee **CONJECTURED**, not proved. The finite
checks below are **COMPUTATIONALLY VERIFIED**. No unrestricted reset bound
or Lean result follows. This is distinct from ordinary inverse greedy,
which already fails a square guarantee at four states.

## Precise policy

Let R be the full Q-reachable image family and e(S) the cost from
IMAGE_EXTENSION.md. For proper reachable S, the allowed next images are

    E(S)={T in R: |T|>|S| and exists u, |u|=e(S), Tu subset S}.

All shortest words and all such images are permitted, including proper
reachable subsets of the whole inverse image. Set G(Q)=0 and

    G(S)=e(S)+min_{T in E(S)} G(T).

The minimum policy cost is min_q G({q}). Strong connectivity and
synchronization ensure every singleton is reachable. Cardinality strictly
increases along every policy phase, so the recurrence is acyclic. A chain
starting from a singleton gives an actual reset word by prepending each
phase word, in the correct right-action order.

The open proposal is min_q G({q})<=(n-1)^2 for every strongly connected
synchronizing n-state DFA over any finite alphabet. We do not claim that
every choice of ties satisfies the bound, or that G equals the exact reset
distance. The latter is already false on stored examples (largest saved
gap is 15 among the retained inputs, not a global maximum).
For n=1, G(Q)=0 handles the singleton endpoint without an extension phase.

The unrestricted image-extension conjecture requests a linear e(S) for
every image; this policy target only requests a compatible chain whose
total cost fits the square. Neither implication has been proved from the
other. A local Cn bound with C>=2 would give a different quadratic constant.

## Exact finite evidence

Complete distinct-letter binary coverage at five states checks 146,828
first-map inputs, including 32,588 strongly connected synchronizing inputs.
The maximum minimum policy cost is 16 and no square failure occurs.

At six states, 6,065,150 first-map inputs include 1,122,529 strongly
connected synchronizing inputs. For 1,116,592 the simple sum

    sum_{k=1}^{n-1} max{e(S): S in R, |S|=k}

is <=25 (empty ranks contribute zero). It bounds every policy because
phases strictly increase cardinality and visit each rank at most once.
The remaining 5,937 inputs have their complete all-tie recurrence solved;
their maximum minimum cost is 25. Thus the best policy square guarantee
holds for the complete binary six-state range. These are overlapping
covering counts, not counts of unique isomorphism classes. Repeated-letter
cases reduce to unary and cannot be both strongly connected and
synchronizing at n>=2.

The previously retained six-state extremals of reset thresholds 25,25,23,23
all admit image policies of exactly those lengths. This observation does
not characterize all extremals. For C6 the maximum over initial singletons
costs 30; at a FIXED singleton q both extension-choice extrema equal 25+q.
Thus 30 refutes arbitrary initial-singleton choice, not extension ties
after fixing the best singleton. CIRCULAR_IMAGE_POLICY_THEOREM.md proves
this distinction for every C_n.

Seven/eight-state sampled rank-one-defect neighborhoods have maximum
minimum costs 36 and 49, respectively, with no failure found. These are
only 5,000 and 3,000 proposed mutations. Further alphabet and rank-defect
checks are recorded separately in data/image_extension_policy*/summary.json;
absence of a sampled counterexample proves no general statement.

The four-state exhaustive ternary run checks 2,763,520 distinct-letter
inputs, including 1,825,392 synchronizing strongly connected inputs.
Its rank-sum shortcut covers 1,802,064; the other 23,328 have exact policy
minimum <=9. Binary cases cover repeated letters in a ternary input.
A separate sample of 20,000 six-state ternary inputs has 14,773 SC
synchronizing inputs, all with rank sum <=24. That sample is not a cover.

## Necessary condition for a Cerny counterexample

The explicit policy construction proves rt(A)<=min_q G({q})<=U_image(A),
where U_image is the rank sum above. Hence a strongly connected
counterexample to the square bound must have U_image>(n-1)^2, and in
fact its minimum policy cost must exceed the square. This is an exact
automaton-dependent restriction, not a closed-form general bound. The
complete six-state binary rank-sum test eliminates 1,116,592 of the
1,122,529 SC synchronizing covering inputs before solving exact policies.
No contradiction for unbounded state size has been derived.

## Independent verification and the unresolved proof step

The generator computes transport distances on the actual forward image
graph, allowing Tu to be a proper subset of S. The independent checker
instead performs inverse ordinary-set BFS from each S until the first
preimages containing larger reachable images, collects every shortest
endpoint, and solves the opposite-direction recurrence. Stored explicit
full-Q words agree with the computed minimum policy lengths. Deliberate
reset-word corruption is rejected.

The missing proof is a global compatible-choice bound for G. The local
e(S) can exceed 3n/2, inverse image capacity is not submodular, and G need
not equal optimal reset distance. It is not legitimate to replace the
all-tie minimum by an arbitrary shortest extension or by an unproved rank
potential. The complete computations identify a candidate to attack;
they do not certify its quantifiers for larger n or arbitrary alphabets.

The stronger local G(S)<=n(n-|S|) induction has now failed at binary-minimal
n=5, and capacity-based proper union transfer fails at state-minimal n=3.
See LOCAL_IMAGE_POTENTIAL_OBSTRUCTION.md. These failures leave the global
singleton minimum conjecture open. The restricted permutation-plus-corank-one
binary cover and broader exact searches are recorded in NATIVE_IMAGE_POLICY_AUDIT.md.
