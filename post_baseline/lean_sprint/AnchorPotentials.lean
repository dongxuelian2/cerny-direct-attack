import Std
namespace OrionAnchors

def bit (u : Bool) : Nat := if u then 1 else 0
def offset2 (u v : Bool) : Nat := if v then (if u then 5 else 4) else 3
def p2 (k : Nat) (u v : Bool) : Nat := if k=1 then 0 else 3*k-offset2 u v

theorem p2_rotation (k : Nat) (u v t : Bool) (hk : 1 ≤ k)
    (valid : bit u + bit v + bit t ≤ k) : p2 k u v ≤ p2 k v t + 1 := by
  cases u <;> cases v <;> cases t <;>
    by_cases h : k=1 <;> simp_all [p2, offset2, bit] <;> omega

theorem p2_merge (k : Nat) (u v : Bool) (hk : 1 ≤ k)
    (valid : bit u + bit v ≤ k) :
    p2 k u v ≤ p2 (k-bit (u && v)) (u || v) false + 1 := by
  cases u <;> cases v <;> by_cases h1 : k=1 <;> by_cases h2 : k=2 <;>
    simp_all [p2, offset2, bit]
  all_goals first | omega | (
    have hp : k-1 ≠ 1 := by omega
    simp [hp]
    omega)

def offset3 : Bool → Bool → Bool → Nat
  | false,false,false => 1
  | false,false,true => 2
  | false,true,false => 1
  | false,true,true => 3
  | true,false,false => 1
  | true,false,true => 2
  | true,true,false => 3
  | true,true,true => 4

def small2 : Bool → Bool → Bool → Nat
  | false,false,false => 4
  | false,false,true => 3
  | false,true,false => 5
  | false,true,true => 2
  | true,false,false => 4
  | true,false,true => 6
  | true,true,false => 1
  | true,true,true => 0

def small3 : Bool → Bool → Bool → Nat
  | false,false,false => 8
  | false,false,true => 7
  | false,true,false => 8
  | false,true,true => 6
  | true,false,false => 8
  | true,false,true => 7
  | true,true,false => 5
  | true,true,true => 6

def p3 (k : Nat) (u v w : Bool) : Nat :=
  if k=1 then 0 else if k=2 then small2 u v w
  else if k=3 then small3 u v w else 3*k-offset3 u v w

theorem p3_rotation (k : Nat) (u v w t : Bool) (hk : 1 ≤ k)
    (valid : bit u + bit v + bit w + bit t ≤ k) :
    p3 k u v w ≤ p3 k v w t + 1 := by
  cases u <;> cases v <;> cases w <;> cases t <;>
    by_cases h1 : k=1 <;> by_cases h2 : k=2 <;> by_cases h3 : k=3 <;>
    simp_all [p3,small2,small3,offset3,bit] <;> omega

theorem p3_merge (k : Nat) (u v w : Bool) (hk : 1 ≤ k)
    (valid : bit u + bit v + bit w ≤ k) :
    p3 k u v w ≤ p3 (k-bit (u && v)) (u || v) false w + 1 := by
  cases u <;> cases v <;> cases w <;>
    by_cases h1 : k=1 <;> by_cases h2 : k=2 <;> by_cases h3 : k=3 <;>
    by_cases h4 : k=4 <;>
    simp_all [p3,small2,small3,offset3,bit]
  all_goals first | omega | (
    have hp1 : k-1 ≠ 1 := by omega
    have hp2 : k-1 ≠ 2 := by omega
    have hp3 : k-1 ≠ 3 := by omega
    simp [hp1,hp2,hp3]
    omega)

theorem p3_full_value (n : Nat) (hn : 5 ≤ n) : p3 n true true true = 3*n-4 := by
  have h1 : n ≠ 1 := by omega
  have h2 : n ≠ 2 := by omega
  have h3 : n ≠ 3 := by omega
  simp [p3,offset3,h1,h2,h3]

end OrionAnchors
#print axioms OrionAnchors.p2_rotation
#print axioms OrionAnchors.p2_merge
#print axioms OrionAnchors.p3_rotation
#print axioms OrionAnchors.p3_merge
#print axioms OrionAnchors.p3_full_value
