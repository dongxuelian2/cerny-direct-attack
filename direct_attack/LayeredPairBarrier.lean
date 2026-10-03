/-
Soundness of a layered directed-pair lower certificate.
The concrete Figure 3 automaton is NOT instantiated in this file.
All graph and entrance conditions are explicit hypotheses.
-/
import Std

namespace Orion.DirectAttack

universe u

/-- A path containing only noncollapsing original pair edges. -/
inductive Walk {S : Type u} (edge : S → S → Prop) (start : S) :
    S → Nat → Prop where
  | nil : Walk edge start start 0
  | snoc {x y : S} {t : Nat} :
      Walk edge start x t → edge x y → Walk edge start y (t + 1)

/-- The first two layers have paid entrance potentials. The last region
can only be entered through a delayed merging pair. -/
structure LayeredCertificate {S : Type u} (edge : S → S → Prop) where
  index : S → Nat
  C : S → Prop
  H : S → Prop
  K : S → Prop
  U : S → Prop
  phiC : S → Nat
  phiH : S → Nat
  bound : Nat
  indexEdge : ∀ {x y}, edge x y → index y ≤ index x + 1
  cInternal : ∀ {x y}, edge x y → C x → C y → phiC y ≤ phiC x + 1
  cEntrance : ∀ {x y}, edge x y → ¬ C x → C y → phiC y ≤ index x + 1
  hInternal : ∀ {x y}, edge x y → H x → H y → phiH y ≤ phiH x + 1
  hEntranceC : ∀ {x y}, edge x y → ¬ H x → C x → H y →
    phiH y ≤ phiC x + 1
  hEntranceIndex : ∀ {x y}, edge x y → ¬ H x → ¬ C x → H y →
    phiH y ≤ index x + 1
  kEntrance : ∀ {x y}, edge x y → K y → H x ∧ bound ≤ phiH x + 2
  uEntrance : ∀ {x y}, edge x y → ¬ U x → U y → K x

/-- This theorem allows arbitrarily many exits and reentries in each layer. -/
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
    (c.U q → c.bound ≤ t) := by
  classical
  induction path with
  | nil =>
      exact ⟨by omega, fun h => (hC0 h).elim, fun h => (hH0 h).elim,
        fun h => (hK0 h).elim, fun h => (hU0 h).elim⟩
  | @snoc x y t prev step ih =>
      rcases ih with ⟨hi, hC, hH, hK, hU⟩
      refine ⟨?_, ?_, ?_, ?_, ?_⟩
      · have he := c.indexEdge step
        omega
      · intro hy
        by_cases hx : c.C x
        · have he := c.cInternal step hx hy
          have hp := hC hx
          omega
        · have he := c.cEntrance step hx hy
          omega
      · intro hy
        by_cases hx : c.H x
        · have he := c.hInternal step hx hy
          have hp := hH hx
          omega
        · by_cases hcx : c.C x
          · have he := c.hEntranceC step hx hcx hy
            have hp := hC hcx
            omega
          · have he := c.hEntranceIndex step hx hcx hy
            omega
      · intro hy
        rcases c.kEntrance step hy with ⟨hx, hb⟩
        have hp := hH hx
        omega
      · intro hy
        by_cases hx : c.U x
        · have hp := hU hx
          omega
        · have hp := hK (c.uEntrance step hx hy)
          omega

/-- If every first-collapse source belongs to K or U, its final letter
costs at least the requested bound. -/
theorem first_collapse_cost {S : Type u} {edge : S → S → Prop}
    (c : LayeredCertificate edge) (start : S)
    (hindex : c.index start = 0)
    (hC0 : ¬ c.C start) (hH0 : ¬ c.H start)
    (hK0 : ¬ c.K start) (hU0 : ¬ c.U start)
    {q : S} {t : Nat} (path : Walk edge start q t)
    (terminal : c.K q ∨ c.U q) : c.bound ≤ t + 1 := by
  have hi := layered_invariants c start hindex hC0 hH0 hK0 hU0 path
  rcases terminal with hK | hU
  · exact hi.2.2.2.1 hK
  · have hb := hi.2.2.2.2 hU
    omega

end Orion.DirectAttack

#print axioms Orion.DirectAttack.layered_invariants
#print axioms Orion.DirectAttack.first_collapse_cost
