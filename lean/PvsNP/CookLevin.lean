/-
The Cook-Levin theorem: SAT is NP-complete (Cook 1971; Levin independently).

NP-hardness is defined via polynomial-time many-one reductions. SAT NP-complete
means: SAT is in NP, and every NP language reduces to SAT in polynomial time.
The headline corollary is the project's central reformulation:

    P = NP  iff  SAT ∈ P.

The statements are precise; the proofs are documented `sorry` markers, since the
Cook-Levin construction (encoding a polynomial-time verifier's computation
tableau as a CNF) requires the real cost model that Basic.lean leaves abstract.
-/

import PvsNP.Basic
import PvsNP.SAT

namespace PvsNP

/-- A polynomial-time many-one reduction from `A` to `B`: a polynomial-time
    computable `f` with `A x ↔ B (f x)`. -/
structure PolyReduction (A B : Language) where
  f : BitString → BitString
  polyTime : RunsInPolyTime f
  correct : ∀ x, A x ↔ B (f x)

/-- `B` is NP-hard: every NP language reduces to it in polynomial time. -/
def NPHard (B : Language) : Prop :=
  ∀ A : Language, inNP A → Nonempty (PolyReduction A B)

/-- `B` is NP-complete: NP-hard and in NP. -/
def NPComplete (B : Language) : Prop := NPHard B ∧ inNP B

/-- SAT is in NP: a satisfying assignment (encoded) is a polynomial-size witness
    the verifier can check by evaluating the CNF. VERIFIER target #CL-1: needs the
    witness encoding (#SAT-enc) and the polynomial bound on assignment size. -/
theorem sat_in_NP : inNP SAT := by
  sorry

/-- Cook-Levin: SAT is NP-hard. VERIFIER target #CL-2: the tableau construction
    encoding an arbitrary NP verifier's accepting computation as a CNF. This is
    the mathematical core and needs the real cost model. -/
theorem sat_NP_hard : NPHard SAT := by
  sorry

/-- Cook-Levin: SAT is NP-complete. -/
theorem cook_levin : NPComplete SAT :=
  ⟨sat_NP_hard, sat_in_NP⟩

/-- The reduction is transitive: if `A ≤ₚ B` and `B ∈ P` then `A ∈ P`. The proof
    composes the reduction with `B`'s decider; trivial time bounds in the skeleton
    make the content the correctness equivalence. VERIFIER target #CL-3 supplies
    the genuine "polynomial composes with polynomial" step. -/
theorem reduction_preserves_P {A B : Language}
    (r : PolyReduction A B) (hB : inP B) : inP A := by
  obtain ⟨D⟩ := hB
  refine ⟨{ decide := fun x => D.decide (r.f x), polyTime := trivial, correct := ?_ }⟩
  intro x
  rw [D.correct (r.f x)]
  exact (r.correct x).symm

/-- The central reformulation: P = NP iff SAT ∈ P.

    Forward: if P = NP then SAT ∈ NP gives SAT ∈ P. Backward: if SAT ∈ P, then
    every NP language reduces to SAT and so is in P (and P ⊆ NP always), giving
    P = NP. The backward direction uses `sat_NP_hard` and `reduction_preserves_P`;
    it is stated and reduced here, with the NP-hardness input as the documented
    Cook-Levin target #CL-2. -/
theorem P_eq_NP_iff_SAT_in_P : P_eq_NP ↔ inP SAT := by
  constructor
  · intro h
    exact (h SAT).mpr sat_in_NP
  · intro hSAT
    intro L
    constructor
    · intro hL; exact inP_subset_inNP L hL
    · intro hL
      obtain ⟨r⟩ := sat_NP_hard L hL
      exact reduction_preserves_P r hSAT

end PvsNP
