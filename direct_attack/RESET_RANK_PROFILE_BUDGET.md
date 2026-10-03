# Reset rank trajectories bound every shortest-image seed policy

**PROVED on paper**, elementary deduction; priority OPEN. Let A be any
strongly connected synchronizing DFA with n>=2 and finite alphabet.
Let r=max{|T|:T a proper actual image}. For ANY existing reset word w
of length ell, write rho_t=|Q w[1:t]|, 0<=t<=ell, so rho_0=n and
rho_ell=1. For 1<=k<=r define

    t_k=max{t:rho_t>k},       L_k=ell-t_k.

The prefix image U_k=Q w[1:t_k] is actual and has size >k. The remaining
suffix of length L_k resets it to the same endpoint as w. In the state
graph, a shortest walk from that endpoint to any k-set S has length at
most n-k: before its first entry it visits distinct vertices outside S.
Concatenating these words transports U_k into S (in fact into a singleton
inside S). Thus for EVERY actual proper S of size k,

    e(S)<=L_k+n-k.

No condition on the prefix image containing S, exact arrival rank, or
the reset being shortest is imposed. The source size is strictly larger
than k. This is exactly the actual-image condition needed by e.

Every initial one-letter seed has extension cost 1. Each subsequent
extension phase strictly increases parent cardinality, so its target
ranks belong to {2,...,r} and each is visited at most once. Q is the
zero-cost endpoint. ALL seeds and ALL subsequent shortest-word/parent
ties consequently satisfy

    W({h})<=B(w)=1+sum_(k=2)^r(L_k+n-k).

If the initial merge source is Q, the remaining sum is empty and the
cost is one; bounding it by B(w) is valid. For r=1 the displayed sum
is empty and B=1, covering n2. The n1 case remains rt=P=0 separately.

## The rank-area identity and counterexample restriction

Cardinality never increases along a word. Therefore i>t_k precisely
when rho_i<=k, and double-counting yields

    area_r(w)=sum_(k=2)^r L_k
             =sum_(i=1)^ell max(0,r-max(2,rho_i)+1);
    B(w)=2+(r-1)n-r(r+1)/2+area_r(w).

Since L_k<=ell, this improves the previous reset-length budget rank by
rank, and can cover instances with ell>(n+1)/2. A failure of the global
policy square NECESSARILY satisfies, for EVERY reset word w,

    area_r(w)>(n-1)^2-[2+(r-1)n-r(r+1)/2].

For r=n-1 this is area_r(w)>(n-2)(n+1)/2. An actual SC Cerny counterexample
must obey the same condition since rt<=P. The reverse implication for rt
is not claimed. Short rank tails can exclude a policy counterexample
even when the total reset length exceeds the previous sufficient regime.

These are bounds given a reset witness and its trajectory, not an
n-only upper bound or an efficient general procedure for obtaining a
short reset. A long plateau contributes differently depending on its
rank; it is the summed area, not total length alone, that enters this
deduction. Neither a quadratic nor a subcubic general reset bound follows.

## Adversarial verification

check_first_drop independently constructs the ordinary actual-image graph
and ALL-SOURCE distances on its full finite corpus. It reconstructs a
shortest reset path on the BFS-level DAG, favoring a small area, then
directly verifies the word, every prefix rank, both expressions for the
area, EVERY local e inequality, and EVERY one-letter seed's worst tail.
The saved extra witnesses have rt>(n+1)/2 but B(w)<=(n-1)^2; their actual
words, ranks and bounds are retained in data/rank_profile_budget_cases.json.
No exhaustive priority or Lean verification is claimed.

The initial rank-profile checkpoint tested 8276 inputs (3658 accepted). All 43774 proper
image bounds and 5760 seed budgets pass. The trajectory refinement lowers
the previous rank-sum bound in 1000 accepted cases; it certifies the
square in 330 cases where that previous rank-sum bound exceeds the square,
and in 428 cases outside the simpler ell<=(n+1)/2 regime. Those two
comparisons are kept separate. In total 2711 accepted cases meet the new
sufficient condition. These are finite overlapping input counts.

For example n4, a=[0,0,0,3], d=[1,3,2,2], has shortest reset ddd and
rank trajectory (4,3,2,1). Here r=3, L_2=2,L_3=3, area=5, B=9;
the previous rank-dependent length bound was 10. The example is SC but
not irreducibly synchronizing, and is not presented as a minimal
counterexample rigidity witness.

The later CIRCULAR_RANK_AREA_BARRIER.md proves that on every C_n,n>=3,
NO choice of reset word can make this budget meet the square. Optimizing
over arbitrary words gives cubic leading growth. Therefore this valid
conditional bound cannot by itself become a universal square proof.
