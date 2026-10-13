import Std
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
namespace ReflectionCoreCut

def layers : List (List (List Int)) := [[[]],[[],[1]],[[],[1],[2]],[[],[-1,1],[1],[2],[3]],[[],[-2,1],[-1,1],[0,2],[1],[1,2],[2],[3],[4]],[[],[-3,1],[-2,1],[-1,1],[-1,2],[0,2],[1],[1,2],[1,3],[2],[2,3],[3],[4],[5]],[[],[-4,1],[-3,1],[-2,-1,1],[-2,1],[-2,2],[-1,1],[-1,1,2],[-1,2],[0,2],[0,3],[1],[1,2],[1,3],[1,4],[2],[2,3],[2,4],[3],[3,4],[4],[5],[6]],[[],[-5,1],[-4,1],[-3,-2,1],[-3,-1,1],[-3,1],[-3,2],[-2,-1,1],[-2,1],[-2,2],[-1,0,2],[-1,1],[-1,1,2],[-1,1,3],[-1,2],[-1,3],[0,2],[0,2,3],[0,3],[1],[1,2],[1,2,3],[1,3],[1,4],[1,5],[2],[2,3],[2,4],[2,5],[3],[3,4],[3,5],[4],[4,5],[5],[6],[7]],[[],[-6,1],[-5,1],[-4,-3,1],[-4,-2,1],[-4,-1,1],[-4,1],[-4,2],[-3,-2,1],[-3,-1,1],[-3,1],[-3,2],[-2,-1,1],[-2,-1,2],[-2,0,2],[-2,1],[-2,1,2],[-2,2],[-2,3],[-1,0,2],[-1,1],[-1,1,2],[-1,1,3],[-1,1,4],[-1,2],[-1,3],[0,1,3],[0,2],[0,2,3],[0,2,4],[0,3],[0,4],[1],[1,2],[1,2,3],[1,2,4],[1,3],[1,3,4],[1,4],[1,5],[1,6],[2],[2,3],[2,3,4],[2,4],[2,5],[2,6],[3],[3,4],[3,5],[3,6],[4],[4,5],[4,6],[5],[5,6],[6],[7],[8]]]

def layer (k : Nat) : List (List Int) := layers[k]!

def safe (H : List Int) : Prop := ¬ (0 ∈ H ∧ 1 ∈ H)

instance (H : List Int) : Decidable (safe H) :=
  inferInstanceAs (Decidable (¬ (0 ∈ H ∧ 1 ∈ H)))

def insertUnique (q : Int) : List Int → List Int
  | [] => [q]
  | h :: rest =>
    if q = h then h :: rest
    else if q < h then q :: h :: rest
    else h :: insertUnique q rest

def canonical : List Int → List Int
  | [] => []
  | h :: rest => insertUnique h (canonical rest)

def step (letter : Fin 2) (H : List Int) : List Int :=
  if letter.val = 0 then
    canonical (1 :: ((H.filter (fun q => q != 0 && q != 1)).map (fun q => 1 - q)))
  else H.map (fun q => q + 1)

theorem seed : ([] : List Int) ∈ layer 0 := by decide

def letters : List (Fin 2) := [0,1]

theorem letter_in_letters : ∀ letter : Fin 2, letter ∈ letters := by decide

def layerOK (k : Nat) : Bool :=
  (layer k).all (fun H => decide (safe H) &&
    letters.all (fun letter => (layer (k+1)).contains (step letter H)))

theorem finite_cut_certificate : ∀ k : Fin 8, layerOK k.val = true := by decide

theorem cut_closed :
    ∀ k : Fin 8, ∀ H ∈ layer k.val, ∀ letter : Fin 2,
      safe H ∧ step letter H ∈ layer (k.val + 1) := by
  intro k H hH letter
  have h := List.all_eq_true.mp (finite_cut_certificate k) H hH
  change (decide (safe H) && letters.all (fun letter =>
    (layer (k.val+1)).contains (step letter H))) = true at h
  rw [Bool.and_eq_true] at h
  have hNext := List.all_eq_true.mp h.2 letter (letter_in_letters letter)
  exact ⟨of_decide_eq_true h.1,List.contains_iff_mem.mp hNext⟩

def run (H : List Int) : List (Fin 2) → List Int
  | [] => H
  | letter :: rest => run (step letter H) rest

def SafeRun (H : List Int) : List (Fin 2) → Prop
  | [] => True
  | letter :: rest => safe H ∧ SafeRun (step letter H) rest

theorem run_in_layers (word : List (Fin 2)) :
    ∀ k H, k + word.length ≤ 8 → H ∈ layer k →
      SafeRun H word ∧ run H word ∈ layer (k + word.length) := by
  induction word with
  | nil =>
    intro k H _ hH
    exact ⟨True.intro, by simpa [run] using hH⟩
  | cons letter rest ih =>
    intro k H hLength hH
    have hk : k < 8 := by simp only [List.length_cons] at hLength; omega
    have hStep := cut_closed ⟨k,hk⟩ H hH letter
    have hRest : k + 1 + rest.length ≤ 8 := by simp only [List.length_cons] at hLength; omega
    have h := ih (k+1) (step letter H) hRest hStep.2
    refine ⟨⟨hStep.1,h.1⟩, ?_⟩
    simpa [run,List.length_cons,Nat.add_assoc,Nat.add_comm,Nat.add_left_comm] using h.2

theorem no_avoid_first_eight (word : List (Fin 2)) (hLength : word.length ≤ 8) :
    SafeRun [] word := by
  exact (run_in_layers word 0 [] (by simpa using hLength) seed).1

def witnessPrefix : List (Fin 2) := [0,1,0,0,1,0,1,1]

theorem witness_prefix_holes : run [] witnessPrefix = [0,1,3] := by decide

theorem witness_final_unsafe : ¬ safe (run [] witnessPrefix) := by decide

#print axioms cut_closed
#print axioms run_in_layers
#print axioms no_avoid_first_eight
#print axioms witness_prefix_holes
#print axioms witness_final_unsafe
end ReflectionCoreCut
