/-
ORION SyncLab. Proof-source draft, not compiled in the preparation environment.
No extra axioms, proof holes or native_decide are intentionally used.
Compile before describing this source as formally verified.
-/
import Std

namespace Orion

def run {S A : Type} (step : S → A → S) : S → List A → S
  | s, [] => s
  | s, a :: w => run step (step s a) w

/-- Local one-step inequalities imply a bound along every finite word. -/
theorem potential_along_word {S A : Type} (step : S → A → S)
    (d : S → Nat) (edge : ∀ s a, d s ≤ d (step s a) + 1)
    (w : List A) (s : S) : d s ≤ w.length + d (run step s w) := by
  induction w generalizing s with
  | nil => simp [run]
  | cons a w ih =>
    calc
      d s ≤ d (step s a) + 1 := edge s a
      _ ≤ (w.length + d (run step (step s a) w)) + 1 :=
        Nat.add_le_add_right (ih (step s a)) 1
      _ = (a :: w).length + d (run step s (a :: w)) := by
        simp [run, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

/-- Every word reaching a zero-potential goal has length at least d s. -/
theorem lower_bound {S A : Type} (step : S → A → S) (goal : S → Prop)
    (d : S → Nat) (edge : ∀ s a, d s ≤ d (step s a) + 1)
    (terminal : ∀ s, goal s → d s = 0) (s : S) (w : List A)
    (hgoal : goal (run step s w)) : d s ≤ w.length := by
  have h := potential_along_word step d edge w s
  simpa [terminal (run step s w) hgoal] using h

/-- A potential constrained to increase at most one per cardinality level is linear. -/
theorem cardinality_limit (f : Nat → Nat) (hbase : f 1 = 0)
    (hslope : ∀ k, f (k + 2) ≤ f (k + 1) + 1) :
    ∀ k, f (k + 1) ≤ k := by
  intro k
  induction k with
  | zero => simpa [hbase]
  | succ k ih =>
    calc
      f (k + 1 + 1) ≤ f (k + 1) + 1 := hslope k
      _ ≤ k + 1 := Nat.add_le_add_right ih 1

end Orion

#print axioms Orion.potential_along_word
#print axioms Orion.lower_bound
#print axioms Orion.cardinality_limit
