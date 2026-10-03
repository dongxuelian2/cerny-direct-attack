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


/- Fixed-instance powerset-system theorem. The final bridge to a reusable
   arbitrary-DFA statement is an explicitly scheduled research task. -/
namespace OrionExample
open Orion
abbrev State := Fin 16

def transition (q : Nat) (a : Bool) : Nat :=
  (if a then ([0, 1, 2, 0] : List Nat) else [1, 2, 3, 0]).getD q 0

def move (s : State) (a : Bool) : State :=
  let value := (if a then ([0, 1, 2, 3, 4, 5, 6, 7, 1, 1, 3, 3, 5, 5, 7, 7] : List Nat) else [0, 2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13, 15]).getD s.val 0
  ⟨value % 16, Nat.mod_lt _ (by decide)⟩

def bitOn (s q : Nat) : Bool := (s / 2 ^ q) % 2 == 1

def goal (s : State) : Prop := ∃ q : Fin 4, s.val = 2 ^ q.val
instance (s : State) : Decidable (goal s) := inferInstanceAs (Decidable (∃ q : Fin 4, s.val = 2 ^ q.val))
def potential (s : State) : Nat := ([0, 0, 0, 4, 0, 6, 3, 8, 0, 1, 5, 5, 2, 6, 7, 9] : List Nat).getD s.val 0
def initial : State := 15
def witness : List Bool := [true, false, false, false, true, false, false, false, true]

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

/-- Every table edge agrees with the concrete one-letter subset image. -/
theorem one_step_fidelity : ∀ (s : State) (a : Bool) (j : Fin 4),
    bitOn (move s a).val j.val =
    (List.finRange 4).any (fun q => bitOn s.val q.val &&
      decide (transition q.val a = j.val)) := by decide

theorem local_bound : ∀ s a, potential s ≤ potential (move s a) + 1 := by decide

theorem terminal_zero : ∀ s, goal s → potential s = 0 := by decide

theorem witness_reaches_goal : goal (run move initial witness) := by decide

/-- Exact minimum word length in this explicitly defined powerset system. -/
theorem optimal_subset_path :
    goal (run move initial witness) ∧
    ∀ w : List Bool, goal (run move initial w) → witness.length ≤ w.length := by
  constructor
  · exact witness_reaches_goal
  · intro w hw
    have h := lower_bound move goal potential local_bound terminal_zero initial w hw
    simpa [potential, initial, witness] using h

end OrionExample
#print axioms OrionExample.one_step_fidelity
#print axioms OrionExample.optimal_subset_path
