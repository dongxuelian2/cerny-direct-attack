# Rank-length inequalities alone still permit a cubic tail

**PROVED (abstract inequality system).** No DFA realizing the profiles below
is claimed. In particular these are NOT counterexamples to Cerny's conjecture.

The rank-length inequalities used here are exactly:

1. lambda_0=0, lambda_1=1, and nonnegative gaps delta_r=lambda_(r+1)-lambda_r.
2. Pin--Frankl: delta_r <= T_r=(r+1)(r+2)/2.
3. The kernel bridge: delta_r <= lambda_r+r+1.
4. The singleton-rich plateau splice: for 1<=r<n/2 and every t with
   delta_t>2r, delta_r <= lambda_t+2r. The terminal infinite gap can be included.

Take n=2m, lambda_r=1 for 1<=r<=m, and thereafter define

    delta_r=min{T_r,lambda_r+r+1},  m<=r<=n-2.

This satisfies all four sets of constraints. Constraints 2 and 3 hold by
construction. Every gap appearing on the left of constraint 4 is zero, so
that constraint holds for every eligible t, not merely the first one.

Yet lambda_(n-1)=(7/48)n^3-O(n^2 log n).

To see this, put t=m^2/2. For r>=m, T_r>=t. While lambda_r<t, its increment
is at least lambda_r, so it reaches t after O(log n) steps. Once it reaches
t, its increment is at least t until it exceeds 2m^2; three further steps
suffice. All remaining T_r are <=2m^2, so every remaining gap equals T_r.
The sum from r=m to n-2 of T_r is (7/48)n^3+O(n^2). Deleting the initial
O(log n) terms costs O(n^2 log n). The constructed profile is bounded above
by this same sum plus 1, giving the stated asymptotic equality.

Therefore a proof using only these rank-length inequalities cannot yield
a subcubic bound. It needs an additional constraint tying the lower-rank
tail to actual fibers, subset geometry, backward expansion, or another
invariant. The point is logical insufficiency of this particular relaxation,
not an impossibility theorem about all rank-profile methods.

Computational checks in abstract_profiles.json verify the stated finite
constraints through n=2000. The construction and asymptotic proof are
independent of those checks.
