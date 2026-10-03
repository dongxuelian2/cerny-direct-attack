"""Emit a separate post-release literal Lean cut; no old formal file is edited."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TEMPLATE = r'''import Std
set_option maxRecDepth 20000
set_option maxHeartbeats 100000000
namespace OrderTwoThreeABarrier

abbrev State := Fin 25
abbrev Letter := Fin 2
abbrev Subset := State → Bool

def states : List State := [STATES]
def letters : List Letter := [0,1]
def rows : List (List State) := ROWS
def transition (letter : Letter) (q : State) : State := rows[letter.val]![q.val]!
def membership (S : Nat) (q : State) : Bool := decide ((S / 2^q.val) % 2 = 1)
def pre (S : Subset) (letter : Letter) : Subset := fun q => S (transition letter q)
def cardinality (S : Subset) : Nat := states.foldl (fun total q => total + if S q then 1 else 0) 0
def goal (S : Subset) : Prop := S 24 = true ∧ cardinality S > 17
instance (S : Subset) : Decidable (goal S) := inferInstanceAs (Decidable (_ ∧ _))
def initialMask : Nat := INITIAL
def layers : List (List Nat) := LAYERS
def layer (k : Nat) : List Nat := layers[k]!
def pullMask (letter : Letter) (S : Nat) : Nat :=
  states.foldl (fun total q => total + if membership S (transition letter q) then 2^q.val else 0) 0
def layerOK (k : Nat) : Bool :=
  (layer k).all (fun S => letters.all (fun letter =>
    (layer (k+1)).contains (pullMask letter S) &&
    states.all (fun q => decide (membership (pullMask letter S) q = membership S (transition letter q)))))
def safeLayer (k : Nat) : Bool := (layer k).all (fun S => decide (¬ goal (membership S)))

theorem state_in_states : ∀ q : State, q ∈ states := by decide
theorem letter_in_letters : ∀ letter : Letter, letter ∈ letters := by decide
theorem initial_cardinality : cardinality (membership initialMask) = 17 := by decide
theorem seed : initialMask ∈ layer 0 := by decide
theorem finite_closure : ∀ k : Fin 9, layerOK k.val = true := by decide
theorem finite_safety : ∀ k : Fin 10, safeLayer k.val = true := by decide

theorem cut_closed (k : Fin 9) (S : Nat) (hS : S ∈ layer k.val) (letter : Letter) :
    pullMask letter S ∈ layer (k.val+1) ∧
      pre (membership S) letter = membership (pullMask letter S) := by
  have h := List.all_eq_true.mp (finite_closure k) S hS
  have hletter := List.all_eq_true.mp h letter (letter_in_letters letter)
  rw [Bool.and_eq_true] at hletter
  refine ⟨List.contains_iff_mem.mp hletter.1, ?_⟩
  funext q
  have hq := List.all_eq_true.mp hletter.2 q (state_in_states q)
  exact (of_decide_eq_true hq).symm

theorem cut_safe (k : Fin 10) (S : Nat) (hS : S ∈ layer k.val) :
    ¬ goal (membership S) := by
  exact of_decide_eq_true (List.all_eq_true.mp (finite_safety k) S hS)

def run (S : Nat) : List Letter → Nat
  | [] => S
  | letter :: rest => run (pullMask letter S) rest
def actualRun (S : Subset) : List Letter → Subset
  | [] => S
  | letter :: rest => actualRun (pre S letter) rest

theorem run_in_layers (word : List Letter) :
    ∀ k S, k + word.length ≤ 9 → S ∈ layer k → run S word ∈ layer (k+word.length) := by
  induction word with
  | nil =>
    intro k S _ hS
    simpa [run] using hS
  | cons letter rest ih =>
    intro k S hLength hS
    have hk : k < 9 := by simp only [List.length_cons] at hLength; omega
    have hNext := (cut_closed ⟨k,hk⟩ S hS letter).1
    have hLengthNext : (k+1)+rest.length ≤ 9 := by simp only [List.length_cons] at hLength; omega
    have h := ih (k+1) (pullMask letter S) hLengthNext hNext
    simpa [run, List.length_cons, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using h

theorem literal_run_bridge (word : List Letter) :
    ∀ k S, k + word.length ≤ 9 → S ∈ layer k →
      actualRun (membership S) word = membership (run S word) := by
  induction word with
  | nil => intro k S _ _; rfl
  | cons letter rest ih =>
    intro k S hLength hS
    have hk : k < 9 := by simp only [List.length_cons] at hLength; omega
    have hNext := cut_closed ⟨k,hk⟩ S hS letter
    have hLengthNext : (k+1)+rest.length ≤ 9 := by simp only [List.length_cons] at hLength; omega
    change actualRun (pre (membership S) letter) rest = membership (run (pullMask letter S) rest)
    rw [hNext.2]
    exact ih (k+1) (pullMask letter S) hLengthNext hNext.1

-- ALL words, including arbitrarily many a within the length limit.
-- actualRun processes inverse letters in listed order; the original forward
-- word is its reverse. Universal quantification covers either convention.
theorem every_short_word_fails (word : List Letter) (hLength : word.length ≤ 9) :
    ¬ goal (actualRun (membership initialMask) word) := by
  have hBound : 0+word.length ≤ 9 := by omega
  have hLayer := run_in_layers word 0 initialMask hBound seed
  have hBridge := literal_run_bridge word 0 initialMask hBound seed
  rw [hBridge]
  apply cut_safe ⟨word.length, by omega⟩ (run initialMask word)
  simpa using hLayer

def witness : List Letter := [0,0,0,0,0,0,0,0,1,0]
theorem witness_length : witness.length = 10 := by decide
theorem witness_success : goal (actualRun (membership initialMask) witness) := by decide
theorem ordinary_minimum :
    (∃ word : List Letter, word.length = 10 ∧ goal (actualRun (membership initialMask) word)) ∧
    (∀ word : List Letter, word.length < 10 → ¬ goal (actualRun (membership initialMask) word)) := by
  refine ⟨⟨witness,witness_length,witness_success⟩, ?_⟩
  intro word hLength
  exact every_short_word_fails word (by omega)

#print axioms initial_cardinality
#print axioms finite_closure
#print axioms finite_safety
#print axioms cut_closed
#print axioms literal_run_bridge
#print axioms every_short_word_fails
#print axioms witness_success
#print axioms ordinary_minimum
end OrderTwoThreeABarrier
'''


def main():
    data = json.loads((ROOT/'direct_attack/data/order_two_three_a_barrier.json').read_text(encoding='utf-8'))
    z = data['records'][0]
    source = (TEMPLATE.replace('STATES', ','.join(map(str, range(25))))
              .replace('ROWS', json.dumps(z['rows'], separators=(',', ':')))
              .replace('INITIAL', str(z['subset']))
              .replace('LAYERS', json.dumps(z['ordinary']['cumulative_layers'], separators=(',', ':'))))
    path = ROOT/'direct_attack/post_release/OrderTwoThreeABarrier.lean'
    path.parent.mkdir(exist_ok=True)
    path.write_text(source, encoding='utf-8')
    print(json.dumps(dict(path=str(path), layers=len(z['ordinary']['cumulative_layers']),
                          literal_states=25, scope='literal ordinary minimum 10 only')))


if __name__ == '__main__':
    main()
