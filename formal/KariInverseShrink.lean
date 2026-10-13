import Std

set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

namespace KariInverseShrink

-- The literal six-state rows are a=[4,4,2,3,1,5], b=[1,5,3,4,2,0].
-- A word here is listed in inverse processing order. Preimages of an
-- ordinary original word are processed in reverse letter order.
def bitContribution (S q weight : Nat) : Nat :=
  if (S / 2^q) % 2 = 1 then weight else 0

def card (S : Nat) : Nat :=
  bitContribution S 0 1 + bitContribution S 1 1 +
  bitContribution S 2 1 + bitContribution S 3 1 +
  bitContribution S 4 1 + bitContribution S 5 1

def preMask (letter S : Nat) : Nat :=
  if letter = 0 then
    bitContribution S 4 1 + bitContribution S 4 2 +
    bitContribution S 2 4 + bitContribution S 3 8 +
    bitContribution S 1 16 + bitContribution S 5 32
  else
    bitContribution S 1 1 + bitContribution S 5 2 +
    bitContribution S 3 4 + bitContribution S 4 8 +
    bitContribution S 2 16 + bitContribution S 0 32

theorem preMask_bound :
    ∀ S : Fin 64, ∀ letter : Fin 2, preMask letter.val S.val < 64 := by
  decide

def step (letter : Fin 2) (S : Fin 64) : Fin 64 :=
  ⟨preMask letter.val S.val, preMask_bound S letter⟩

def transition (letter : Fin 2) (q : Fin 6) : Nat :=
  if letter.val = 0 then ([4,4,2,3,1,5] : List Nat)[q.val]!
  else ([1,5,3,4,2,0] : List Nat)[q.val]!

def member (S q : Nat) : Prop := (S / 2^q) % 2 = 1

theorem literal_preimage_correct :
    ∀ S : Fin 64, ∀ letter : Fin 2, ∀ q : Fin 6,
      member (step letter S).val q.val ↔ member S.val (transition letter q) := by
  unfold member
  decide

def cut : List Nat :=
  [1,2,3,4,5,7,8,10,11,12,14,15,16,20,21,24,28,32,
   33,34,35,37,39,42,43,47,48,49,50,51,53,55,56,58,59]

theorem singleton_bound : ∀ q : Fin 6, 2^q.val < 64 := by decide

def singleton (q : Fin 6) : Fin 64 := ⟨2^q.val, singleton_bound q⟩

theorem seed_in_cut : ∀ q : Fin 6, (singleton q).val ∈ cut := by decide

theorem full_not_in_cut : ¬ 63 ∈ cut := by decide

theorem cut_closed :
    ∀ S : Fin 64, ∀ letter : Fin 2,
      S.val ∈ cut → card S.val ≤ card (step letter S).val →
      (step letter S).val ∈ cut := by
  decide

def run (S : Fin 64) : List (Fin 2) → Fin 64
  | [] => S
  | letter :: rest => run (step letter S) rest

def MonotoneRun (S : Fin 64) : List (Fin 2) → Prop
  | [] => True
  | letter :: rest => card S.val ≤ card (step letter S).val ∧
      MonotoneRun (step letter S) rest

theorem run_preserves_cut (word : List (Fin 2)) :
    ∀ S : Fin 64, S.val ∈ cut → MonotoneRun S word → (run S word).val ∈ cut := by
  induction word with
  | nil =>
      intro S hS _
      exact hS
  | cons letter rest ih =>
      intro S hS hRun
      exact ih (step letter S) (cut_closed S letter hS hRun.1) hRun.2

-- Quantifies over ALL lengths, not only words up to the square threshold.
theorem no_monotone_inverse_reset (q : Fin 6) (word : List (Fin 2))
    (hRun : MonotoneRun (singleton q) word) :
    (run (singleton q) word).val ≠ 63 := by
  intro hFull
  have hCut := run_preserves_cut word (singleton q) (seed_in_cut q) hRun
  rw [hFull] at hCut
  exact full_not_in_cut hCut

def shrinkCount (S : Fin 64) : List (Fin 2) → Nat
  | [] => 0
  | letter :: rest =>
      (if card (step letter S).val < card S.val then 1 else 0) +
      shrinkCount (step letter S) rest

theorem zero_shrinks_monotone (word : List (Fin 2)) :
    ∀ S : Fin 64, shrinkCount S word = 0 → MonotoneRun S word := by
  induction word with
  | nil =>
      intro S _
      trivial
  | cons letter rest ih =>
      intro S h
      have hNot : ¬ card (step letter S).val < card S.val := by
        intro hLt
        simp [shrinkCount, hLt] at h
      have hRest : shrinkCount (step letter S) rest = 0 := by
        simpa [shrinkCount, hNot] using h
      exact ⟨Nat.le_of_not_gt hNot, ih (step letter S) hRest⟩

theorem reset_needs_shrink (q : Fin 6) (word : List (Fin 2))
    (hFull : (run (singleton q) word).val = 63) :
    1 ≤ shrinkCount (singleton q) word := by
  by_cases hZero : shrinkCount (singleton q) word = 0
  · exact False.elim
      (no_monotone_inverse_reset q word (zero_shrinks_monotone word (singleton q) hZero) hFull)
  · omega

def inverseWitness : List (Fin 2) :=
  [0,1,1,0,1,0,1,1,0,1,1,0,1,0,0,1,1,0,1,0,1,0,1,1,0]

theorem witness_resets : (run (singleton 4) inverseWitness).val = 63 := by decide

theorem witness_one_shrink : shrinkCount (singleton 4) inverseWitness = 1 := by decide

theorem witness_cost : inverseWitness.length = 25 := by decide

end KariInverseShrink

#print axioms KariInverseShrink.no_monotone_inverse_reset
#print axioms KariInverseShrink.literal_preimage_correct
#print axioms KariInverseShrink.reset_needs_shrink
#print axioms KariInverseShrink.witness_resets
#print axioms KariInverseShrink.witness_one_shrink
#print axioms KariInverseShrink.witness_cost
