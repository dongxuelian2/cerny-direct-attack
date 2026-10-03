import ResearchCore
import AnchorPotentials

namespace OrionThreeGraph
open OrionAnchors OrionResearch

structure Feature where
  hidden : Nat
  u : Bool
  v : Bool
  w : Bool

def cardinality (x : Feature) : Nat := x.hidden + bit x.u + bit x.v + bit x.w
def potential (x : Feature) : Nat := p3 (cardinality x) x.u x.v x.w
def rotate (x : Feature) (t : Bool) : Feature :=
  ⟨x.hidden + bit x.u - bit t, x.v, x.w, t⟩
def merge (x : Feature) : Feature := ⟨x.hidden, x.u || x.v, false, x.w⟩

/-- Exact count/window relation; the concrete powerset bridge remains on paper. -/
def Edge (m : Nat) (x y : Feature) : Prop :=
  1 ≤ cardinality x ∧ x.hidden ≤ m ∧
  ((∃ t, bit t ≤ x.hidden ∧ x.hidden ≤ m-1+bit t ∧ y = rotate x t)
    ∨ y = merge x)

theorem rotate_card (x : Feature) (t : Bool) (valid : bit t ≤ x.hidden) :
    cardinality (rotate x t) = cardinality x := by
  simp only [cardinality, rotate]
  omega

theorem merge_card (x : Feature) :
    cardinality (merge x) = cardinality x - bit (x.u && x.v) := by
  cases x with
  | mk j u v w =>
    cases u <;> cases v <;> cases w <;>
      simp [cardinality, merge, bit] <;> omega

theorem one_step (m : Nat) (x y : Feature) (edge : Edge m x y) :
    potential x ≤ potential y + 1 := by
  obtain ⟨hk, _, h⟩ := edge
  rcases h with ⟨t, ht, _, rfl⟩ | rfl
  · have valid : bit x.u + bit x.v + bit x.w + bit t ≤ cardinality x := by
      simp only [cardinality]; omega
    have h := p3_rotation (cardinality x) x.u x.v x.w t hk valid
    unfold potential
    rw [rotate_card x t ht]
    exact h
  · have valid : bit x.u + bit x.v + bit x.w ≤ cardinality x := by
      simp only [cardinality]; omega
    have h := p3_merge (cardinality x) x.u x.v x.w hk valid
    unfold potential
    rw [merge_card]
    exact h

theorem full_lower_bound (n : Nat) (hn : 5 ≤ n) (goal : Feature) (length : Nat)
    (walk : Walk (Edge (n-3)) ⟨n-3, true, true, true⟩ goal length)
    (terminal : cardinality goal = 1) : 3*n-4 ≤ length := by
  have ht : potential goal = 0 := by simp [potential, terminal, p3]
  have bound := potential_lower_bound potential (one_step (n-3)) walk ht
  have card : cardinality ⟨n-3, true, true, true⟩ = n := by
    simp [cardinality, bit]; omega
  have value : potential ⟨n-3, true, true, true⟩ = 3*n-4 := by
    simpa only [potential, card] using p3_full_value n hn
  rwa [value] at bound

end OrionThreeGraph
#print axioms OrionThreeGraph.one_step
#print axioms OrionThreeGraph.full_lower_bound
