"""Emit a finite powerset-system proof draft, using ordinary decide only."""
from pathlib import Path
from .engine import build_graph
from .check_certificate import check

def export(cert:dict, core_path:Path)->str:
    check(cert)
    if cert['kind']!='exact':
        raise ValueError('Lean exporter currently accepts exact certificates only')
    a=cert['automaton'];n=a['n'];N=1<<n
    if n>5 or len(a['letters'])!=2:
        raise ValueError('Lean draft exporter is limited to binary automata with n <= 5')
    graph=build_graph(a)
    fmt=lambda xs:'['+', '.join(map(str,xs))+']'
    row0=fmt([g[0] for g in graph]);row1=fmt([g[1] for g in graph])
    tr0=fmt(a['transitions'][0]);tr1=fmt(a['transitions'][1])
    d=fmt(cert['potential']);word='['+', '.join('true' if x else 'false' for x in cert['word'])+']'
    target=0
    for letter in cert['word']:
        target=a['transitions'][letter][target]
    # Embedding the core avoids an unbuilt local import in the first-run command.
    return core_path.read_text(encoding='utf-8')+f'''

/- Fixed-instance powerset-system theorem. The final bridge to a reusable
   arbitrary-DFA statement is an explicitly scheduled research task. -/
namespace OrionExample
open Orion
abbrev State := Fin {N}

def transition (q : Nat) (a : Bool) : Nat :=
  (if a then ({tr1} : List Nat) else {tr0}).getD q 0

def move (s : State) (a : Bool) : State :=
  let value := (if a then ({row1} : List Nat) else {row0}).getD s.val 0
  ⟨value % {N}, Nat.mod_lt _ (by decide)⟩

def bitOn (s q : Nat) : Bool := (s / 2 ^ q) % 2 == 1

def goal (s : State) : Prop := ∃ q : Fin {n}, s.val = 2 ^ q.val
def potential (s : State) : Nat := ({d} : List Nat).getD s.val 0
def initial : State := {N-1}
def witness : List Bool := {word}

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

/-- Every table edge agrees with the concrete one-letter subset image. -/
theorem one_step_fidelity : ∀ (s : State) (a : Bool) (j : Fin {n}),
    bitOn (move s a).val j.val =
    (List.finRange {n}).any (fun q => bitOn s.val q.val &&
      decide (transition q.val a = j.val)) := by decide

theorem local_bound : ∀ s a, potential s ≤ potential (move s a) + 1 := by decide

theorem terminal_zero : ∀ s, goal s → potential s = 0 := by
  intro s h
  obtain ⟨q,hq⟩ := h
  have finite : ∀ (s : State) (q : Fin {n}), s.val = 2 ^ q.val → potential s = 0 := by decide
  exact finite s q hq

theorem witness_reaches_goal : goal (run move initial witness) := by
  exact ⟨{target}, by decide⟩

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
'''
