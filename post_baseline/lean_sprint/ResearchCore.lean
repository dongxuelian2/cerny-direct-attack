import Std
namespace OrionResearch

def QuotientEdge {S A F : Type} (step : S → A → S) (alpha : S → F)
    (x y : F) : Prop := ∃ s a, alpha s = x ∧ alpha (step s a) = y

inductive Walk {S : Type} (edge : S → S → Prop) : S → S → Nat → Prop
  | nil (x) : Walk edge x x 0
  | cons {x y z k} : edge x y → Walk edge y z k → Walk edge x z (k+1)

theorem potential_along_walk {S : Type} {edge : S → S → Prop}
    (p : S → Nat) (edge_bound : ∀ x y, edge x y → p x ≤ p y + 1)
    {x z k} (w : Walk edge x z k) : p x ≤ k + p z := by
  induction w with
  | nil => simp
  | cons h w ih => have hh := edge_bound _ _ h; omega

theorem potential_lower_bound {S : Type} {edge : S → S → Prop}
    (p : S → Nat) (edge_bound : ∀ x y, edge x y → p x ≤ p y + 1)
    {x z k} (w : Walk edge x z k) (terminal : p z = 0) : p x ≤ k := by
  have h := potential_along_walk p edge_bound w
  omega

theorem quotient_local {S A F : Type} (step : S → A → S) (alpha : S → F)
    (p : F → Nat) (h : ∀ s a, p (alpha s) ≤ p (alpha (step s a)) + 1) :
    ∀ x y, QuotientEdge step alpha x y → p x ≤ p y + 1 := by
  intro x y hedge
  obtain ⟨s, a, hx, hy⟩ := hedge
  simpa [hx,hy] using h s a

/-- Distance transfer only needs an inclusion-type simulation, not commuting maps. -/
theorem monotone_simulation_transfer {S A F T : Type}
    (step : S → A → S) (alpha : S → F) (view : S → T)
    (small order : T → T → Prop) (p : F → Nat) (d : T → Nat)
    (resolved : ∀ s, p (alpha s) = d (view s))
    (mono : ∀ x y, order x y → d x ≤ d y)
    (edgeCost : ∀ x y, small x y → d x ≤ d y + 1)
    (simulation : ∀ s a, ∃ y, small (view s) y ∧ order y (view (step s a))) :
    ∀ x y, QuotientEdge step alpha x y → p x ≤ p y + 1 := by
  apply quotient_local step alpha p
  intro s a
  obtain ⟨y, hsmall, horder⟩ := simulation s a
  have h₁ := edgeCost (view s) y hsmall
  have h₂ := mono y (view (step s a)) horder
  rw [resolved s, resolved (step s a)]
  omega

def power2 : Nat → Nat
  | 0 => 1
  | d+1 => 2 * power2 d

theorem power2_pos (d : Nat) : 1 ≤ power2 d := by
  induction d with
  | zero => decide
  | succ d ih => simp only [power2]; omega

theorem power2_eq (d : Nat) : power2 d = 2^d := by
  induction d with
  | zero => rfl
  | succ d ih => simp [power2, ih, Nat.pow_succ, Nat.mul_comm]

theorem spaced_events (s : Nat → Nat) (step : ∀ i, s i + 2 ≤ s (i+1)) :
    ∀ i d, s i + 2*d ≤ s (i+d) := by
  intro i d
  induction d with
  | zero => simp
  | succ d ih =>
    have h := step (i+d)
    simp only [Nat.mul_succ, Nat.add_assoc] at *
    omega

theorem dyadic_release (s : Nat → Nat) (r : Nat)
    (release : ∀ i, 1 ≤ i → s i + r ≤ s (2*i)) :
    ∀ d, d*r ≤ s (power2 d) := by
  intro d
  induction d with
  | zero => simp
  | succ d ih =>
    have h := release (power2 d) (power2_pos d)
    simp only [power2, Nat.succ_mul] at *
    omega

/-- Hypotheses are the timing lemmas of the paper, not assumed automaton facts. -/
theorem genealogy_clock_lower (s : Nat → Nat) (r K d : Nat)
    (step : ∀ i, s i + 2 ≤ s (i+1))
    (release : ∀ i, 1 ≤ i → s i + r ≤ s (2*i))
    (index : power2 d ≤ K) : d*r + 2*(K-power2 d) ≤ s K := by
  have h₁ := dyadic_release s r release d
  have h₂ := spaced_events s step (power2 d) (K-power2 d)
  have eq : power2 d + (K-power2 d) = K := by omega
  rw [eq] at h₂
  omega

theorem genealogy_word_lower (s : Nat → Nat) (r K d totalClock : Nat)
    (step : ∀ i, s i + 2 ≤ s (i+1))
    (release : ∀ i, 1 ≤ i → s i + r ≤ s (2*i))
    (index : power2 d ≤ K) (last : s K ≤ totalClock) :
    K + d*r + 2*(K-power2 d) ≤ K+totalClock := by
  have h := genealogy_clock_lower s r K d step release index
  omega

/-- Finite hypotheses suffice: no fictitious events beyond the final split. -/
theorem spaced_events_finite (s : Nat → Nat) (K : Nat)
    (step : ∀ i, 1 ≤ i → i < K → s i + 2 ≤ s (i+1)) :
    ∀ i d, 1 ≤ i → i+d ≤ K → s i + 2*d ≤ s (i+d) := by
  intro i d hi
  induction d with
  | zero => intro _; simp
  | succ d ih =>
    intro bound
    have prev : i+d ≤ K := by omega
    have h₁ := ih prev
    have h₂ := step (i+d) (by omega) (by omega)
    simp only [Nat.mul_succ, Nat.add_assoc] at *
    omega

theorem dyadic_release_finite (s : Nat → Nat) (r K : Nat)
    (release : ∀ i, 1 ≤ i → 2*i ≤ K → s i + r ≤ s (2*i)) :
    ∀ d, power2 d ≤ K → d*r ≤ s (power2 d) := by
  intro d
  induction d with
  | zero => intro _; simp
  | succ d ih =>
    intro bound
    have hp := power2_pos d
    have index : power2 d ≤ K := by simp only [power2] at bound; omega
    have h₁ := ih index
    have h₂ := release (power2 d) hp (by simpa only [power2] using bound)
    simp only [power2, Nat.succ_mul] at *
    omega

theorem genealogy_clock_lower_finite (s : Nat → Nat) (r K d : Nat)
    (step : ∀ i, 1 ≤ i → i < K → s i + 2 ≤ s (i+1))
    (release : ∀ i, 1 ≤ i → 2*i ≤ K → s i + r ≤ s (2*i))
    (index : power2 d ≤ K) : d*r + 2*(K-power2 d) ≤ s K := by
  have h₁ := dyadic_release_finite s r K release d index
  have h₂ := spaced_events_finite s K step (power2 d) (K-power2 d)
    (power2_pos d) (by omega)
  have eq : power2 d + (K-power2 d) = K := by omega
  rw [eq] at h₂
  omega

/-- Optimal clock cost forces every event in the dyadic terminal interval. -/
theorem genealogy_tail_rigidity (s : Nat → Nat) (r K d : Nat)
    (step : ∀ i, 1 ≤ i → i < K → s i + 2 ≤ s (i+1))
    (release : ∀ i, 1 ≤ i → 2*i ≤ K → s i + r ≤ s (2*i))
    (index : power2 d ≤ K)
    (optimal : s K ≤ d*r+2*(K-power2 d)) :
    ∀ i, power2 d ≤ i → i ≤ K → s i = d*r+2*(i-power2 d) := by
  intro i hi hK
  have hd := dyadic_release_finite s r K release d index
  have h₁ := spaced_events_finite s K step (power2 d) (i-power2 d)
    (power2_pos d) (by omega)
  have hiPos : 1 ≤ i := by have hp := power2_pos d; omega
  have h₂ := spaced_events_finite s K step i (K-i) hiPos (by omega)
  have eq₁ : power2 d + (i-power2 d) = i := by omega
  have eq₂ : i + (K-i) = K := by omega
  rw [eq₁] at h₁
  rw [eq₂] at h₂
  omega

/-- The exact capacity-two input inequalities, not merely conservation. -/
theorem buffer_two_realizable (before now ready input : Nat)
    (bit : input ≤ 1) (change : now = before+input)
    (interlace : now ≤ ready ∧ ready ≤ now+1) :
    input ≤ ready-before ∧ ready-before ≤ 1+input := by omega

/-- The sharp dyadic buffer estimate at an even offset (a split clock). -/
theorem sharp_buffer_split (h z i ready : Nat) (hh : 1 ≤ h) (hz : 1 ≤ z)
    (parents : i ≤ 2*h-1 ∧ i ≤ h+z) (releaseCount : ready ≤ 2*i+1) :
    ready-(2*h+z-1) ≤ h+1 := by
  by_cases regime : z < h <;> omega

/-- The distinct, one-smaller bound required at an odd offset (input zero). -/
theorem sharp_buffer_nonsplit (h z i ready : Nat) (hh : 1 ≤ h)
    (parents : i ≤ 2*h-1 ∧ i ≤ h+z) (releaseCount : ready ≤ 2*i+1) :
    ready-(2*h+z) ≤ h := by
  by_cases regime : z < h <;> omega

theorem sharp_capacity_obstruction (h : Nat) (hh : 2 ≤ h) :
    ¬ ((4*h-1)-(3*h-1) ≤ h-1) := by omega

theorem eventually_constant_nat (f : Nat → Nat)
    (mono : ∀ i j, i ≤ j → f j ≤ f i) :
    ∃ N, ∀ n, N ≤ n → f n = f N := by
  have aux : ∀ v, ∀ g : Nat → Nat, g 0 = v →
      (∀ i j, i ≤ j → g j ≤ g i) → ∃ N, ∀ n, N ≤ n → g n = g N := by
    intro v
    induction v using Nat.strongRecOn with
    | ind v ih =>
      intro g hv hm
      by_cases constant : ∀ n, g n = v
      · exact ⟨0, fun n _ => by rw [constant n, constant 0]⟩
      · have witness : ∃ k, g k ≠ v := Classical.not_forall.mp constant
        obtain ⟨k, hk⟩ := witness
        have le := hm 0 k (Nat.zero_le k)
        have lt : g k < v := by omega
        obtain ⟨N,hN⟩ := ih (g k) lt (fun n => g (n+k)) (by simp)
          (fun i j hij => hm (i+k) (j+k) (Nat.add_le_add_right hij k))
        refine ⟨N+k, ?_⟩
        intro n hn
        have hn' : N ≤ n-k := by omega
        have eq : n-k+k = n := by omega
        have result := hN (n-k) hn'
        simpa only [eq] using result
  exact aux (f 0) f rfl mono
end OrionResearch

#print axioms OrionResearch.potential_lower_bound
#print axioms OrionResearch.quotient_local
#print axioms OrionResearch.monotone_simulation_transfer
#print axioms OrionResearch.genealogy_clock_lower
#print axioms OrionResearch.genealogy_clock_lower_finite
#print axioms OrionResearch.genealogy_tail_rigidity
#print axioms OrionResearch.buffer_two_realizable
#print axioms OrionResearch.sharp_buffer_split
#print axioms OrionResearch.sharp_buffer_nonsplit
#print axioms OrionResearch.sharp_capacity_obstruction
#print axioms OrionResearch.eventually_constant_nat
