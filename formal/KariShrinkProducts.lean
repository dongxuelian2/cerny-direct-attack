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


namespace KariProductBase
open KariInverseShrink

def fullPotential (S : Fin 64) : Nat :=
  ([1000, 28, 26, 24, 26, 22, 18, 16, 27, 19, 20, 18, 18, 14, 12, 10, 25, 20, 17, 16, 17, 14, 9, 8, 19, 11, 12, 11, 11, 6, 4, 3, 27, 23, 22, 22, 18, 17, 14, 14, 19, 15, 14, 14, 10, 10, 6, 6, 21, 15, 16, 15, 13, 9, 9, 8, 13, 7, 8, 7, 5, 2, 1, 0] : List Nat)[S.val]!

def prefixPotential (S : Fin 64) : Nat :=
  ([1000, 19, 17, 15, 17, 13, 11, 9, 18, 9, 11, 9, 11, 4, 8, 6, 16, 13, 7, 6, 10, 7, 8, 7, 10, 10, 2, 1, 7, 7, 8, 12, 18, 14, 13, 13, 8, 8, 4, 4, 12, 5, 7, 5, 9, 0, 8, 10, 12, 8, 7, 6, 3, 5, 2, 12, 6, 6, 7, 11, 9, 11, 13, 1000] : List Nat)[S.val]!

def monoPotential (S : Fin 64) : Nat :=
  ([1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 9, 8, 1000, 11, 1000, 1000, 1000, 6, 4, 3, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 10, 1000, 6, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 7, 1000, 1000, 5, 2, 1, 0] : List Nat)[S.val]!

def coCut : List Nat := [22, 23, 25, 29, 30, 31, 44, 46, 57, 60, 61, 62, 63]

theorem full_step_bound : ∀ S : Fin 64, ∀ l : Fin 2,
    fullPotential S ≤ 1 + fullPotential (step l S) := by decide

theorem prefix_step_bound : ∀ S : Fin 64, ∀ l : Fin 2,
    prefixPotential S ≤ 1 + prefixPotential (step l S) := by decide

theorem mono_step_bound : ∀ S : Fin 64, ∀ l : Fin 2,
    card S.val ≤ card (step l S).val →
    monoPotential S ≤ 1 + monoPotential (step l S) := by decide

theorem potential_path (p : Fin 64 → Nat)
    (hStep : ∀ S : Fin 64, ∀ l : Fin 2, p S ≤ 1 + p (step l S))
    (word : List (Fin 2)) : ∀ S : Fin 64,
    p S ≤ word.length + p (run S word) := by
  induction word with
  | nil => intro S; simp [run]
  | cons l rest ih =>
    intro S
    have h1 := hStep S l
    have h2 := ih (step l S)
    simp only [List.length_cons, run]
    omega

theorem monotone_potential_path (word : List (Fin 2)) : ∀ S : Fin 64,
    MonotoneRun S word →
    monoPotential S ≤ word.length + monoPotential (run S word) := by
  induction word with
  | nil => intro S _; simp [run]
  | cons l rest ih =>
    intro S h
    have h1 := mono_step_bound S l h.1
    have h2 := ih (step l S) h.2
    simp only [List.length_cons, run]
    omega

theorem reset_length_lower (q : Fin 6) (word : List (Fin 2))
    (hFull : run (singleton q) word = 63) : 25 ≤ word.length := by
  have hSeeds : ∀ t : Fin 6, 25 ≤ fullPotential (singleton t) := by decide
  have hSeed := hSeeds q
  have hEnd : fullPotential (63 : Fin 64) = 0 := by decide
  have h := potential_path fullPotential full_step_bound word (singleton q)
  rw [hFull, hEnd] at h
  omega

theorem to45_length_lower (q : Fin 6) (word : List (Fin 2))
    (hTarget : run (singleton q) word = 45) : 16 ≤ word.length := by
  have hSeeds : ∀ t : Fin 6, 16 ≤ prefixPotential (singleton t) := by decide
  have hSeed := hSeeds q
  have hEnd : prefixPotential (45 : Fin 64) = 0 := by decide
  have h := potential_path prefixPotential prefix_step_bound word (singleton q)
  rw [hTarget, hEnd] at h
  omega

theorem mono44_length_lower (word : List (Fin 2))
    (hMono : MonotoneRun 44 word) (hFull : run 44 word = 63) :
    10 ≤ word.length := by
  have hStart : monoPotential (44 : Fin 64) = 10 := by decide
  have hEnd : monoPotential (63 : Fin 64) = 0 := by decide
  have h := monotone_potential_path word 44 hMono
  rw [hStart, hFull, hEnd] at h
  omega

theorem last44_length_lower (q : Fin 6) (lead suffix : List (Fin 2))
    (hPre : run (singleton q) lead = 45)
    (hMono : MonotoneRun 44 suffix) (hPost : run 44 suffix = 63) :
    27 ≤ lead.length + 1 + suffix.length := by
  have h1 := to45_length_lower q lead hPre
  have h2 := mono44_length_lower suffix hMono hPost
  omega

theorem co_cut_backward : ∀ S : Fin 64, ∀ l : Fin 2,
    card S.val ≤ card (step l S).val → (step l S).val ∈ coCut →
    S.val ∈ coCut := by decide

theorem run_to_co_cut (word : List (Fin 2)) : ∀ S : Fin 64,
    MonotoneRun S word → (run S word).val ∈ coCut → S.val ∈ coCut := by
  induction word with
  | nil => intro S _ h; exact h
  | cons l rest ih =>
    intro S hMono hEnd
    exact co_cut_backward S l hMono.1 (ih (step l S) hMono.2 hEnd)

theorem last_negative_bridge : ∀ S : Fin 64, ∀ l : Fin 2,
    card (step l S).val < card S.val → (step l S).val ∈ coCut →
    (S.val = 45 ∧ (step l S).val = 44) ∨
    (S.val = 47 ∧ (step l S).val = 60) := by decide

theorem last_negative_word (S : Fin 64) (l : Fin 2) (suffix : List (Fin 2))
    (hNeg : card (step l S).val < card S.val)
    (hMono : MonotoneRun (step l S) suffix)
    (hFull : run (step l S) suffix = 63) :
    (S.val = 45 ∧ (step l S).val = 44) ∨
    (S.val = 47 ∧ (step l S).val = 60) := by
  have hEnd : (run (step l S) suffix).val ∈ coCut := by rw [hFull]; decide
  exact last_negative_bridge S l hNeg (run_to_co_cut suffix (step l S) hMono hEnd)

theorem one_bridge : ∀ S : Fin 64, ∀ l : Fin 2,
    S.val ∈ cut → card (step l S).val < card S.val →
    (step l S).val ∈ coCut → S.val = 47 ∧ (step l S).val = 60 := by decide

theorem single_negative_word (q : Fin 6) (lead suffix : List (Fin 2)) (l : Fin 2)
    (hPre : MonotoneRun (singleton q) lead)
    (hNeg : card (step l (run (singleton q) lead)).val < card (run (singleton q) lead).val)
    (hPost : MonotoneRun (step l (run (singleton q) lead)) suffix)
    (hFull : run (step l (run (singleton q) lead)) suffix = 63) :
    (run (singleton q) lead).val = 47 ∧
    (step l (run (singleton q) lead)).val = 60 := by
  have hBefore := run_preserves_cut lead (singleton q) (seed_in_cut q) hPre
  have hEnd : (run (step l (run (singleton q) lead)) suffix).val ∈ coCut := by
    rw [hFull]; decide
  have hAfter := run_to_co_cut suffix (step l (run (singleton q) lead)) hPost hEnd
  exact one_bridge (run (singleton q) lead) l hBefore hNeg hAfter

def onePrefix : List (Fin 2) := [0,1,1,0,1,0,1,1,0,1,1,0,1,0,0,1,1,0,1,0]
def oneSuffix : List (Fin 2) := [1,0,1,1,0]
def twoPrefix : List (Fin 2) := [0,1,1,0,1,0,0,1,1,0,1,1,0,1,0,1,0]
def twoSuffix : List (Fin 2) := [1,0,1,1,0,1,0,1,1,0]

theorem one_phase_witness :
    run (singleton 4) onePrefix = 60 ∧ shrinkCount (singleton 4) onePrefix = 1 ∧
    MonotoneRun 60 oneSuffix ∧ run 60 oneSuffix = 63 ∧
    onePrefix.length + oneSuffix.length = 25 := by
  simp only [MonotoneRun, onePrefix, oneSuffix]
  decide

theorem two_phase_witness :
    run (singleton 4) twoPrefix = 44 ∧ shrinkCount (singleton 4) twoPrefix = 2 ∧
    MonotoneRun 44 twoSuffix ∧ run 44 twoSuffix = 63 ∧
    twoPrefix.length + twoSuffix.length = 27 := by
  simp only [MonotoneRun, twoPrefix, twoSuffix]
  decide

end KariProductBase

#print axioms KariInverseShrink.literal_preimage_correct
#print axioms KariInverseShrink.reset_needs_shrink
#print axioms KariProductBase.reset_length_lower
#print axioms KariProductBase.to45_length_lower
#print axioms KariProductBase.mono44_length_lower
#print axioms KariProductBase.last44_length_lower
#print axioms KariProductBase.last_negative_word
#print axioms KariProductBase.single_negative_word
#print axioms KariProductBase.one_phase_witness
#print axioms KariProductBase.two_phase_witness
