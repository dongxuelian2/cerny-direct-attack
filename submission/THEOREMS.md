# Exact Lean theorem inventory

Generated from actual source declarations by `submission/check.py --suite formal`.

Only the ten authoritative modules below are FORMALLY VERIFIED. All hypotheses are part of each statement.


## lean/CertificateCore.lean

SHA-256: `f9cbcd5ab271759ee309919195fb8c84c1f612a3afb20e924ff6a9ba355dd445`


`Orion.potential_along_word`, source line 15, axioms: propext.

```lean
theorem potential_along_word {S A : Type} (step : S → A → S)
    (d : S → Nat) (edge : ∀ s a, d s ≤ d (step s a) + 1)
    (w : List A) (s : S) : d s ≤ w.length + d (run step s w)
```


`Orion.lower_bound`, source line 29, axioms: propext.

```lean
theorem lower_bound {S A : Type} (step : S → A → S) (goal : S → Prop)
    (d : S → Nat) (edge : ∀ s a, d s ≤ d (step s a) + 1)
    (terminal : ∀ s, goal s → d s = 0) (s : S) (w : List A)
    (hgoal : goal (run step s w)) : d s ≤ w.length
```


`Orion.cardinality_limit`, source line 37, axioms: propext.

```lean
theorem cardinality_limit (f : Nat → Nat) (hbase : f 1 = 0)
    (hslope : ∀ k, f (k + 2) ≤ f (k + 1) + 1) :
    ∀ k, f (k + 1) ≤ k
```


## post_baseline/lean_sprint/ResearchCore.lean

SHA-256: `2f5c58ffce695fe35d8efe4db84acbb4f6d0e1e0974e931b3abed0ca65cff884`


`OrionResearch.potential_along_walk`, source line 11, axioms: propext, Quot.sound.

```lean
theorem potential_along_walk {S : Type} {edge : S → S → Prop}
    (p : S → Nat) (edge_bound : ∀ x y, edge x y → p x ≤ p y + 1)
    {x z k} (w : Walk edge x z k) : p x ≤ k + p z
```


`OrionResearch.potential_lower_bound`, source line 18, axioms: propext, Quot.sound.

```lean
theorem potential_lower_bound {S : Type} {edge : S → S → Prop}
    (p : S → Nat) (edge_bound : ∀ x y, edge x y → p x ≤ p y + 1)
    {x z k} (w : Walk edge x z k) (terminal : p z = 0) : p x ≤ k
```


`OrionResearch.quotient_local`, source line 24, axioms: none.

```lean
theorem quotient_local {S A F : Type} (step : S → A → S) (alpha : S → F)
    (p : F → Nat) (h : ∀ s a, p (alpha s) ≤ p (alpha (step s a)) + 1) :
    ∀ x y, QuotientEdge step alpha x y → p x ≤ p y + 1
```


`OrionResearch.monotone_simulation_transfer`, source line 32, axioms: propext, Quot.sound.

```lean
theorem monotone_simulation_transfer {S A F T : Type}
    (step : S → A → S) (alpha : S → F) (view : S → T)
    (small order : T → T → Prop) (p : F → Nat) (d : T → Nat)
    (resolved : ∀ s, p (alpha s) = d (view s))
    (mono : ∀ x y, order x y → d x ≤ d y)
    (edgeCost : ∀ x y, small x y → d x ≤ d y + 1)
    (simulation : ∀ s a, ∃ y, small (view s) y ∧ order y (view (step s a))) :
    ∀ x y, QuotientEdge step alpha x y → p x ≤ p y + 1
```


`OrionResearch.power2_pos`, source line 52, axioms: propext, Quot.sound.

```lean
theorem power2_pos (d : Nat) : 1 ≤ power2 d
```


`OrionResearch.power2_eq`, source line 57, axioms: propext.

```lean
theorem power2_eq (d : Nat) : power2 d = 2^d
```


`OrionResearch.spaced_events`, source line 62, axioms: propext, Quot.sound.

```lean
theorem spaced_events (s : Nat → Nat) (step : ∀ i, s i + 2 ≤ s (i+1)) :
    ∀ i d, s i + 2*d ≤ s (i+d)
```


`OrionResearch.dyadic_release`, source line 72, axioms: propext, Quot.sound.

```lean
theorem dyadic_release (s : Nat → Nat) (r : Nat)
    (release : ∀ i, 1 ≤ i → s i + r ≤ s (2*i)) :
    ∀ d, d*r ≤ s (power2 d)
```


`OrionResearch.genealogy_clock_lower`, source line 84, axioms: propext, Quot.sound.

```lean
theorem genealogy_clock_lower (s : Nat → Nat) (r K d : Nat)
    (step : ∀ i, s i + 2 ≤ s (i+1))
    (release : ∀ i, 1 ≤ i → s i + r ≤ s (2*i))
    (index : power2 d ≤ K) : d*r + 2*(K-power2 d) ≤ s K
```


`OrionResearch.genealogy_word_lower`, source line 94, axioms: propext, Quot.sound.

```lean
theorem genealogy_word_lower (s : Nat → Nat) (r K d totalClock : Nat)
    (step : ∀ i, s i + 2 ≤ s (i+1))
    (release : ∀ i, 1 ≤ i → s i + r ≤ s (2*i))
    (index : power2 d ≤ K) (last : s K ≤ totalClock) :
    K + d*r + 2*(K-power2 d) ≤ K+totalClock
```


`OrionResearch.spaced_events_finite`, source line 103, axioms: propext, Quot.sound.

```lean
theorem spaced_events_finite (s : Nat → Nat) (K : Nat)
    (step : ∀ i, 1 ≤ i → i < K → s i + 2 ≤ s (i+1)) :
    ∀ i d, 1 ≤ i → i+d ≤ K → s i + 2*d ≤ s (i+d)
```


`OrionResearch.dyadic_release_finite`, source line 117, axioms: propext, Quot.sound.

```lean
theorem dyadic_release_finite (s : Nat → Nat) (r K : Nat)
    (release : ∀ i, 1 ≤ i → 2*i ≤ K → s i + r ≤ s (2*i)) :
    ∀ d, power2 d ≤ K → d*r ≤ s (power2 d)
```


`OrionResearch.genealogy_clock_lower_finite`, source line 132, axioms: propext, Quot.sound.

```lean
theorem genealogy_clock_lower_finite (s : Nat → Nat) (r K d : Nat)
    (step : ∀ i, 1 ≤ i → i < K → s i + 2 ≤ s (i+1))
    (release : ∀ i, 1 ≤ i → 2*i ≤ K → s i + r ≤ s (2*i))
    (index : power2 d ≤ K) : d*r + 2*(K-power2 d) ≤ s K
```


`OrionResearch.genealogy_tail_rigidity`, source line 144, axioms: propext, Quot.sound.

```lean
theorem genealogy_tail_rigidity (s : Nat → Nat) (r K d : Nat)
    (step : ∀ i, 1 ≤ i → i < K → s i + 2 ≤ s (i+1))
    (release : ∀ i, 1 ≤ i → 2*i ≤ K → s i + r ≤ s (2*i))
    (index : power2 d ≤ K)
    (optimal : s K ≤ d*r+2*(K-power2 d)) :
    ∀ i, power2 d ≤ i → i ≤ K → s i = d*r+2*(i-power2 d)
```


`OrionResearch.buffer_two_realizable`, source line 163, axioms: propext, Classical.choice, Quot.sound.

```lean
theorem buffer_two_realizable (before now ready input : Nat)
    (bit : input ≤ 1) (change : now = before+input)
    (interlace : now ≤ ready ∧ ready ≤ now+1) :
    input ≤ ready-before ∧ ready-before ≤ 1+input
```


`OrionResearch.sharp_buffer_split`, source line 169, axioms: propext, Quot.sound.

```lean
theorem sharp_buffer_split (h z i ready : Nat) (hh : 1 ≤ h) (hz : 1 ≤ z)
    (parents : i ≤ 2*h-1 ∧ i ≤ h+z) (releaseCount : ready ≤ 2*i+1) :
    ready-(2*h+z-1) ≤ h+1
```


`OrionResearch.sharp_buffer_nonsplit`, source line 175, axioms: propext, Quot.sound.

```lean
theorem sharp_buffer_nonsplit (h z i ready : Nat) (hh : 1 ≤ h)
    (parents : i ≤ 2*h-1 ∧ i ≤ h+z) (releaseCount : ready ≤ 2*i+1) :
    ready-(2*h+z) ≤ h
```


`OrionResearch.sharp_capacity_obstruction`, source line 180, axioms: propext, Quot.sound.

```lean
theorem sharp_capacity_obstruction (h : Nat) (hh : 2 ≤ h) :
    ¬ ((4*h-1)-(3*h-1) ≤ h-1)
```


`OrionResearch.eventually_constant_nat`, source line 183, axioms: propext, Classical.choice, Quot.sound.

```lean
theorem eventually_constant_nat (f : Nat → Nat)
    (mono : ∀ i j, i ≤ j → f j ≤ f i) :
    ∃ N, ∀ n, N ≤ n → f n = f N
```


## post_baseline/lean_sprint/AnchorPotentials.lean

SHA-256: `b4cee113a3998656d31d545ffcefe3d4b597aeed86e35b3b33053f61dfd8dee1`


`OrionAnchors.p2_rotation`, source line 8, axioms: propext, Quot.sound.

```lean
theorem p2_rotation (k : Nat) (u v t : Bool) (hk : 1 ≤ k)
    (valid : bit u + bit v + bit t ≤ k) : p2 k u v ≤ p2 k v t + 1
```


`OrionAnchors.p2_merge`, source line 13, axioms: propext, Quot.sound.

```lean
theorem p2_merge (k : Nat) (u v : Bool) (hk : 1 ≤ k)
    (valid : bit u + bit v ≤ k) :
    p2 k u v ≤ p2 (k-bit (u && v)) (u || v) false + 1
```


`OrionAnchors.p3_rotation`, source line 57, axioms: propext, Quot.sound.

```lean
theorem p3_rotation (k : Nat) (u v w t : Bool) (hk : 1 ≤ k)
    (valid : bit u + bit v + bit w + bit t ≤ k) :
    p3 k u v w ≤ p3 k v w t + 1
```


`OrionAnchors.p3_merge`, source line 64, axioms: propext, Quot.sound.

```lean
theorem p3_merge (k : Nat) (u v w : Bool) (hk : 1 ≤ k)
    (valid : bit u + bit v + bit w ≤ k) :
    p3 k u v w ≤ p3 (k-bit (u && v)) (u || v) false w + 1
```


`OrionAnchors.p3_full_value`, source line 78, axioms: propext, Quot.sound.

```lean
theorem p3_full_value (n : Nat) (hn : 5 ≤ n) : p3 n true true true = 3*n-4
```


## post_baseline/lean_sprint/ThreeAnchorGraph.lean

SHA-256: `96d9461d44ca3d16442e0bcecf51726af7c19518bfb8620b77bc47bf4b1c4a34`


`OrionThreeGraph.rotate_card`, source line 25, axioms: propext, Quot.sound.

```lean
theorem rotate_card (x : Feature) (t : Bool) (valid : bit t ≤ x.hidden) :
    cardinality (rotate x t) = cardinality x
```


`OrionThreeGraph.merge_card`, source line 30, axioms: propext.

```lean
theorem merge_card (x : Feature) :
    cardinality (merge x) = cardinality x - bit (x.u && x.v)
```


`OrionThreeGraph.one_step`, source line 37, axioms: propext, Quot.sound.

```lean
theorem one_step (m : Nat) (x y : Feature) (edge : Edge m x y) :
    potential x ≤ potential y + 1
```


`OrionThreeGraph.full_lower_bound`, source line 54, axioms: propext, Quot.sound.

```lean
theorem full_lower_bound (n : Nat) (hn : 5 ≤ n) (goal : Feature) (length : Nat)
    (walk : Walk (Edge (n-3)) ⟨n-3, true, true, true⟩ goal length)
    (terminal : cardinality goal = 1) : 3*n-4 ≤ length
```


## post_baseline/lean_sprint/Cerny3Checked.lean

SHA-256: `59b4820de7231c0afe4921e3bb425f8793a249939f352e32cb45ec8b4c14e18d`


`Orion.potential_along_word`, source line 16, axioms: propext.

```lean
theorem potential_along_word {S A : Type} (step : S → A → S)
    (d : S → Nat) (edge : ∀ s a, d s ≤ d (step s a) + 1)
    (w : List A) (s : S) : d s ≤ w.length + d (run step s w)
```


`Orion.lower_bound`, source line 30, axioms: propext.

```lean
theorem lower_bound {S A : Type} (step : S → A → S) (goal : S → Prop)
    (d : S → Nat) (edge : ∀ s a, d s ≤ d (step s a) + 1)
    (terminal : ∀ s, goal s → d s = 0) (s : S) (w : List A)
    (hgoal : goal (run step s w)) : d s ≤ w.length
```


`Orion.cardinality_limit`, source line 38, axioms: propext.

```lean
theorem cardinality_limit (f : Nat → Nat) (hbase : f 1 = 0)
    (hslope : ∀ k, f (k + 2) ≤ f (k + 1) + 1) :
    ∀ k, f (k + 1) ≤ k
```


`OrionExample.one_step_fidelity`, source line 80, axioms: propext.

```lean
theorem one_step_fidelity : ∀ (s : State) (a : Bool) (j : Fin 3),
    bitOn (move s a).val j.val =
    (List.finRange 3).any (fun q => bitOn s.val q.val &&
      decide (transition q.val a = j.val))
```


`OrionExample.local_bound`, source line 85, axioms: propext.

```lean
theorem local_bound : ∀ s a, potential s ≤ potential (move s a) + 1
```


`OrionExample.terminal_zero`, source line 87, axioms: none.

```lean
theorem terminal_zero : ∀ s, goal s → potential s = 0
```


`OrionExample.witness_reaches_goal`, source line 93, axioms: propext.

```lean
theorem witness_reaches_goal : goal (run move initial witness)
```


`OrionExample.optimal_subset_path`, source line 97, axioms: propext.

```lean
theorem optimal_subset_path :
    goal (run move initial witness) ∧
    ∀ w : List Bool, goal (run move initial w) → witness.length ≤ w.length
```


## post_baseline/lean_sprint/Cerny4Checked.lean

SHA-256: `5abcbabfd2549273b8e0b58bd40407c19f415d9212bab6db229203caaf075e8c`


`Orion.potential_along_word`, source line 16, axioms: propext.

```lean
theorem potential_along_word {S A : Type} (step : S → A → S)
    (d : S → Nat) (edge : ∀ s a, d s ≤ d (step s a) + 1)
    (w : List A) (s : S) : d s ≤ w.length + d (run step s w)
```


`Orion.lower_bound`, source line 30, axioms: propext.

```lean
theorem lower_bound {S A : Type} (step : S → A → S) (goal : S → Prop)
    (d : S → Nat) (edge : ∀ s a, d s ≤ d (step s a) + 1)
    (terminal : ∀ s, goal s → d s = 0) (s : S) (w : List A)
    (hgoal : goal (run step s w)) : d s ≤ w.length
```


`Orion.cardinality_limit`, source line 38, axioms: propext.

```lean
theorem cardinality_limit (f : Nat → Nat) (hbase : f 1 = 0)
    (hslope : ∀ k, f (k + 2) ≤ f (k + 1) + 1) :
    ∀ k, f (k + 1) ≤ k
```


`OrionExample.one_step_fidelity`, source line 80, axioms: propext.

```lean
theorem one_step_fidelity : ∀ (s : State) (a : Bool) (j : Fin 4),
    bitOn (move s a).val j.val =
    (List.finRange 4).any (fun q => bitOn s.val q.val &&
      decide (transition q.val a = j.val))
```


`OrionExample.local_bound`, source line 85, axioms: propext.

```lean
theorem local_bound : ∀ s a, potential s ≤ potential (move s a) + 1
```


`OrionExample.terminal_zero`, source line 87, axioms: none.

```lean
theorem terminal_zero : ∀ s, goal s → potential s = 0
```


`OrionExample.witness_reaches_goal`, source line 93, axioms: propext.

```lean
theorem witness_reaches_goal : goal (run move initial witness)
```


`OrionExample.optimal_subset_path`, source line 97, axioms: propext.

```lean
theorem optimal_subset_path :
    goal (run move initial witness) ∧
    ∀ w : List Bool, goal (run move initial w) → witness.length ≤ w.length
```


## direct_attack/LayeredPairBarrier.lean

SHA-256: `2c3fa3ced68e0c5e8b230d9977f3bec2ad0492a30b8974a2f817971a6e692a34`


`Orion.DirectAttack.layered_invariants`, source line 42, axioms: propext, Classical.choice, Quot.sound.

```lean
theorem layered_invariants {S : Type u} {edge : S → S → Prop}
    (c : LayeredCertificate edge) (start : S)
    (hindex : c.index start = 0)
    (hC0 : ¬ c.C start) (hH0 : ¬ c.H start)
    (hK0 : ¬ c.K start) (hU0 : ¬ c.U start)
    {q : S} {t : Nat} (path : Walk edge start q t) :
    c.index q ≤ t ∧
    (c.C q → c.phiC q ≤ t) ∧
    (c.H q → c.phiH q ≤ t) ∧
    (c.K q → c.bound ≤ t + 1) ∧
    (c.U q → c.bound ≤ t)
```


`Orion.DirectAttack.first_collapse_cost`, source line 94, axioms: propext, Classical.choice, Quot.sound.

```lean
theorem first_collapse_cost {S : Type u} {edge : S → S → Prop}
    (c : LayeredCertificate edge) (start : S)
    (hindex : c.index start = 0)
    (hC0 : ¬ c.C start) (hH0 : ¬ c.H start)
    (hK0 : ¬ c.K start) (hU0 : ¬ c.U start)
    {q : S} {t : Nat} (path : Walk edge start q t)
    (terminal : c.K q ∨ c.U q) : c.bound ≤ t + 1
```


## direct_attack/KariInverseShrink.lean

SHA-256: `6d82c55ffbb1ba7daf153d24f26f8cb3c1d3ae81e79877025173c3d5eea4b602`


`KariInverseShrink.preMask_bound`, source line 29, axioms: none.

```lean
theorem preMask_bound :
    ∀ S : Fin 64, ∀ letter : Fin 2, preMask letter.val S.val < 64
```


`KariInverseShrink.literal_preimage_correct`, source line 42, axioms: none.

```lean
theorem literal_preimage_correct :
    ∀ S : Fin 64, ∀ letter : Fin 2, ∀ q : Fin 6,
      member (step letter S).val q.val ↔ member S.val (transition letter q)
```


`KariInverseShrink.singleton_bound`, source line 52, axioms: none.

```lean
theorem singleton_bound : ∀ q : Fin 6, 2^q.val < 64
```


`KariInverseShrink.seed_in_cut`, source line 56, axioms: propext, Quot.sound.

```lean
theorem seed_in_cut : ∀ q : Fin 6, (singleton q).val ∈ cut
```


`KariInverseShrink.full_not_in_cut`, source line 58, axioms: propext, Quot.sound.

```lean
theorem full_not_in_cut : ¬ 63 ∈ cut
```


`KariInverseShrink.cut_closed`, source line 60, axioms: propext, Quot.sound.

```lean
theorem cut_closed :
    ∀ S : Fin 64, ∀ letter : Fin 2,
      S.val ∈ cut → card S.val ≤ card (step letter S).val →
      (step letter S).val ∈ cut
```


`KariInverseShrink.run_preserves_cut`, source line 75, axioms: propext, Quot.sound.

```lean
theorem run_preserves_cut (word : List (Fin 2)) :
    ∀ S : Fin 64, S.val ∈ cut → MonotoneRun S word → (run S word).val ∈ cut
```


`KariInverseShrink.no_monotone_inverse_reset`, source line 86, axioms: propext, Quot.sound.

```lean
theorem no_monotone_inverse_reset (q : Fin 6) (word : List (Fin 2))
    (hRun : MonotoneRun (singleton q) word) :
    (run (singleton q) word).val ≠ 63
```


`KariInverseShrink.zero_shrinks_monotone`, source line 100, axioms: propext.

```lean
theorem zero_shrinks_monotone (word : List (Fin 2)) :
    ∀ S : Fin 64, shrinkCount S word = 0 → MonotoneRun S word
```


`KariInverseShrink.reset_needs_shrink`, source line 115, axioms: propext, Quot.sound.

```lean
theorem reset_needs_shrink (q : Fin 6) (word : List (Fin 2))
    (hFull : (run (singleton q) word).val = 63) :
    1 ≤ shrinkCount (singleton q) word
```


`KariInverseShrink.witness_resets`, source line 126, axioms: propext.

```lean
theorem witness_resets : (run (singleton 4) inverseWitness).val = 63
```


`KariInverseShrink.witness_one_shrink`, source line 128, axioms: propext.

```lean
theorem witness_one_shrink : shrinkCount (singleton 4) inverseWitness = 1
```


`KariInverseShrink.witness_cost`, source line 130, axioms: propext.

```lean
theorem witness_cost : inverseWitness.length = 25
```


## direct_attack/KariShrinkProducts.lean

SHA-256: `3ce2361202c7ba27745f9da05492d2251a6d80cc0a58ffa3034a27e5f2fb7e3f`


`KariInverseShrink.preMask_bound`, source line 29, axioms: none.

```lean
theorem preMask_bound :
    ∀ S : Fin 64, ∀ letter : Fin 2, preMask letter.val S.val < 64
```


`KariInverseShrink.literal_preimage_correct`, source line 42, axioms: none.

```lean
theorem literal_preimage_correct :
    ∀ S : Fin 64, ∀ letter : Fin 2, ∀ q : Fin 6,
      member (step letter S).val q.val ↔ member S.val (transition letter q)
```


`KariInverseShrink.singleton_bound`, source line 52, axioms: none.

```lean
theorem singleton_bound : ∀ q : Fin 6, 2^q.val < 64
```


`KariInverseShrink.seed_in_cut`, source line 56, axioms: propext, Quot.sound.

```lean
theorem seed_in_cut : ∀ q : Fin 6, (singleton q).val ∈ cut
```


`KariInverseShrink.full_not_in_cut`, source line 58, axioms: propext, Quot.sound.

```lean
theorem full_not_in_cut : ¬ 63 ∈ cut
```


`KariInverseShrink.cut_closed`, source line 60, axioms: propext, Quot.sound.

```lean
theorem cut_closed :
    ∀ S : Fin 64, ∀ letter : Fin 2,
      S.val ∈ cut → card S.val ≤ card (step letter S).val →
      (step letter S).val ∈ cut
```


`KariInverseShrink.run_preserves_cut`, source line 75, axioms: propext, Quot.sound.

```lean
theorem run_preserves_cut (word : List (Fin 2)) :
    ∀ S : Fin 64, S.val ∈ cut → MonotoneRun S word → (run S word).val ∈ cut
```


`KariInverseShrink.no_monotone_inverse_reset`, source line 86, axioms: propext, Quot.sound.

```lean
theorem no_monotone_inverse_reset (q : Fin 6) (word : List (Fin 2))
    (hRun : MonotoneRun (singleton q) word) :
    (run (singleton q) word).val ≠ 63
```


`KariInverseShrink.zero_shrinks_monotone`, source line 100, axioms: propext.

```lean
theorem zero_shrinks_monotone (word : List (Fin 2)) :
    ∀ S : Fin 64, shrinkCount S word = 0 → MonotoneRun S word
```


`KariInverseShrink.reset_needs_shrink`, source line 115, axioms: propext, Quot.sound.

```lean
theorem reset_needs_shrink (q : Fin 6) (word : List (Fin 2))
    (hFull : (run (singleton q) word).val = 63) :
    1 ≤ shrinkCount (singleton q) word
```


`KariInverseShrink.witness_resets`, source line 126, axioms: propext.

```lean
theorem witness_resets : (run (singleton 4) inverseWitness).val = 63
```


`KariInverseShrink.witness_one_shrink`, source line 128, axioms: propext.

```lean
theorem witness_one_shrink : shrinkCount (singleton 4) inverseWitness = 1
```


`KariInverseShrink.witness_cost`, source line 130, axioms: propext.

```lean
theorem witness_cost : inverseWitness.length = 25
```


`KariProductBase.full_step_bound`, source line 149, axioms: none.

```lean
theorem full_step_bound : ∀ S : Fin 64, ∀ l : Fin 2,
    fullPotential S ≤ 1 + fullPotential (step l S)
```


`KariProductBase.prefix_step_bound`, source line 152, axioms: none.

```lean
theorem prefix_step_bound : ∀ S : Fin 64, ∀ l : Fin 2,
    prefixPotential S ≤ 1 + prefixPotential (step l S)
```


`KariProductBase.mono_step_bound`, source line 155, axioms: none.

```lean
theorem mono_step_bound : ∀ S : Fin 64, ∀ l : Fin 2,
    card S.val ≤ card (step l S).val →
    monoPotential S ≤ 1 + monoPotential (step l S)
```


`KariProductBase.potential_path`, source line 159, axioms: propext, Quot.sound.

```lean
theorem potential_path (p : Fin 64 → Nat)
    (hStep : ∀ S : Fin 64, ∀ l : Fin 2, p S ≤ 1 + p (step l S))
    (word : List (Fin 2)) : ∀ S : Fin 64,
    p S ≤ word.length + p (run S word)
```


`KariProductBase.monotone_potential_path`, source line 172, axioms: propext, Quot.sound.

```lean
theorem monotone_potential_path (word : List (Fin 2)) : ∀ S : Fin 64,
    MonotoneRun S word →
    monoPotential S ≤ word.length + monoPotential (run S word)
```


`KariProductBase.reset_length_lower`, source line 184, axioms: propext, Quot.sound.

```lean
theorem reset_length_lower (q : Fin 6) (word : List (Fin 2))
    (hFull : run (singleton q) word = 63) : 25 ≤ word.length
```


`KariProductBase.to45_length_lower`, source line 193, axioms: propext, Quot.sound.

```lean
theorem to45_length_lower (q : Fin 6) (word : List (Fin 2))
    (hTarget : run (singleton q) word = 45) : 16 ≤ word.length
```


`KariProductBase.mono44_length_lower`, source line 202, axioms: propext, Quot.sound.

```lean
theorem mono44_length_lower (word : List (Fin 2))
    (hMono : MonotoneRun 44 word) (hFull : run 44 word = 63) :
    10 ≤ word.length
```


`KariProductBase.last44_length_lower`, source line 211, axioms: propext, Quot.sound.

```lean
theorem last44_length_lower (q : Fin 6) (lead suffix : List (Fin 2))
    (hPre : run (singleton q) lead = 45)
    (hMono : MonotoneRun 44 suffix) (hPost : run 44 suffix = 63) :
    27 ≤ lead.length + 1 + suffix.length
```


`KariProductBase.co_cut_backward`, source line 219, axioms: propext, Quot.sound.

```lean
theorem co_cut_backward : ∀ S : Fin 64, ∀ l : Fin 2,
    card S.val ≤ card (step l S).val → (step l S).val ∈ coCut →
    S.val ∈ coCut
```


`KariProductBase.run_to_co_cut`, source line 223, axioms: propext, Quot.sound.

```lean
theorem run_to_co_cut (word : List (Fin 2)) : ∀ S : Fin 64,
    MonotoneRun S word → (run S word).val ∈ coCut → S.val ∈ coCut
```


`KariProductBase.last_negative_bridge`, source line 231, axioms: propext, Quot.sound.

```lean
theorem last_negative_bridge : ∀ S : Fin 64, ∀ l : Fin 2,
    card (step l S).val < card S.val → (step l S).val ∈ coCut →
    (S.val = 45 ∧ (step l S).val = 44) ∨
    (S.val = 47 ∧ (step l S).val = 60)
```


`KariProductBase.last_negative_word`, source line 236, axioms: propext, Quot.sound.

```lean
theorem last_negative_word (S : Fin 64) (l : Fin 2) (suffix : List (Fin 2))
    (hNeg : card (step l S).val < card S.val)
    (hMono : MonotoneRun (step l S) suffix)
    (hFull : run (step l S) suffix = 63) :
    (S.val = 45 ∧ (step l S).val = 44) ∨
    (S.val = 47 ∧ (step l S).val = 60)
```


`KariProductBase.one_bridge`, source line 245, axioms: propext, Quot.sound.

```lean
theorem one_bridge : ∀ S : Fin 64, ∀ l : Fin 2,
    S.val ∈ cut → card (step l S).val < card S.val →
    (step l S).val ∈ coCut → S.val = 47 ∧ (step l S).val = 60
```


`KariProductBase.single_negative_word`, source line 249, axioms: propext, Quot.sound.

```lean
theorem single_negative_word (q : Fin 6) (lead suffix : List (Fin 2)) (l : Fin 2)
    (hPre : MonotoneRun (singleton q) lead)
    (hNeg : card (step l (run (singleton q) lead)).val < card (run (singleton q) lead).val)
    (hPost : MonotoneRun (step l (run (singleton q) lead)) suffix)
    (hFull : run (step l (run (singleton q) lead)) suffix = 63) :
    (run (singleton q) lead).val = 47 ∧
    (step l (run (singleton q) lead)).val = 60
```


`KariProductBase.one_phase_witness`, source line 267, axioms: propext.

```lean
theorem one_phase_witness :
    run (singleton 4) onePrefix = 60 ∧ shrinkCount (singleton 4) onePrefix = 1 ∧
    MonotoneRun 60 oneSuffix ∧ run 60 oneSuffix = 63 ∧
    onePrefix.length + oneSuffix.length = 25
```


`KariProductBase.two_phase_witness`, source line 274, axioms: propext.

```lean
theorem two_phase_witness :
    run (singleton 4) twoPrefix = 44 ∧ shrinkCount (singleton 4) twoPrefix = 2 ∧
    MonotoneRun 44 twoSuffix ∧ run 44 twoSuffix = 63 ∧
    twoPrefix.length + twoSuffix.length = 27
```


## direct_attack/ReflectionCoreCut.lean

SHA-256: `5a2df90e8b17785c21270b98a2c7949e4670923b1c774cb4572ead90b4c8727d`


`ReflectionCoreCut.seed`, source line 31, axioms: propext, Quot.sound.

```lean
theorem seed : ([] : List Int) ∈ layer 0
```


`ReflectionCoreCut.letter_in_letters`, source line 35, axioms: propext.

```lean
theorem letter_in_letters : ∀ letter : Fin 2, letter ∈ letters
```


`ReflectionCoreCut.finite_cut_certificate`, source line 41, axioms: propext, Quot.sound.

```lean
theorem finite_cut_certificate : ∀ k : Fin 8, layerOK k.val = true
```


`ReflectionCoreCut.cut_closed`, source line 43, axioms: propext, Quot.sound.

```lean
theorem cut_closed :
    ∀ k : Fin 8, ∀ H ∈ layer k.val, ∀ letter : Fin 2,
      safe H ∧ step letter H ∈ layer (k.val + 1)
```


`ReflectionCoreCut.run_in_layers`, source line 62, axioms: propext, Quot.sound.

```lean
theorem run_in_layers (word : List (Fin 2)) :
    ∀ k H, k + word.length ≤ 8 → H ∈ layer k →
      SafeRun H word ∧ run H word ∈ layer (k + word.length)
```


`ReflectionCoreCut.no_avoid_first_eight`, source line 78, axioms: propext, Quot.sound.

```lean
theorem no_avoid_first_eight (word : List (Fin 2)) (hLength : word.length ≤ 8) :
    SafeRun [] word
```


`ReflectionCoreCut.witness_prefix_holes`, source line 84, axioms: propext.

```lean
theorem witness_prefix_holes : run [] witnessPrefix = [0,1,3]
```


`ReflectionCoreCut.witness_final_unsafe`, source line 86, axioms: propext, Quot.sound.

```lean
theorem witness_final_unsafe : ¬ safe (run [] witnessPrefix)
```


## Excluded archival drafts

`lean/Cerny3.lean` and `lean/Cerny4.lean` fail elaboration and produce `sorryAx` in error recovery. Their proved replacements are the checked copies above. No theorem in either draft is submitted as verified.
