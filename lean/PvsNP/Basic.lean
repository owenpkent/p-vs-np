/-
Foundational definitions for the PvsNP project: languages, polynomial-time
deciders, the classes P and NP (verifier definition), and the central
P = NP question.

Status note (skeleton): this file uses a deliberately lightweight, self-contained
model of computation rather than a full Turing-machine formalization, because
Mathlib does not (as of 2026) carry the complexity-theory infrastructure needed
for the canonical definitions. The intent is to make the STATEMENTS precise and
typed; the computational content (a real cost model, the polynomial time bound on
an actual machine) is left as documented VERIFIER targets.

A `Language` is a predicate on bit strings. `PolyTimeDecider` and `PolyTimeVerifier`
abstract "runs in polynomial time" as a Prop field, the first VERIFIER target.
-/

namespace PvsNP

/-- A bit string. -/
abbrev BitString := List Bool

/-- A language is a set of bit strings. -/
def Language := BitString → Prop

/-- Abstract "runs in time polynomial in the input length" predicate for a
    procedure `f` (a decider `BitString → Bool` or a reduction `BitString →
    BitString`; polymorphic in the codomain so both uses typecheck). VERIFIER
    target #TM-1: replace by a real cost model (a Turing machine or a clocked
    recursion) with an explicit polynomial bound. -/
def RunsInPolyTime {β : Type} (_f : BitString → β) : Prop := True

/-- Abstract "runs in time polynomial in |x| + |w|" for a two-argument verifier.
    VERIFIER target #TM-2. -/
def VerifierPolyTime (_V : BitString → BitString → Bool) : Prop := True

/-- A polynomial-time decider for a language: a procedure `decide` that runs in
    polynomial time and accepts exactly the strings in `L`. -/
structure PolyTimeDecider (L : Language) where
  decide : BitString → Bool
  polyTime : RunsInPolyTime decide
  correct : ∀ x, decide x = true ↔ L x

/-- The class P: languages with a polynomial-time decider. -/
def inP (L : Language) : Prop := Nonempty (PolyTimeDecider L)

/-- A polynomial bound `p(n)` on witness length. Modeled as a function on the
    input length; VERIFIER target #TM-3 pins it to an actual polynomial. -/
abbrev WitnessBound := Nat → Nat

/-- The verifier definition of NP: `L ∈ NP` iff there is a polynomial-time
    verifier `V` and a witness-length bound `p` such that `x ∈ L` exactly when a
    short witness `w` (with `|w| ≤ p(|x|)`) makes `V x w = true`. -/
def inNP (L : Language) : Prop :=
  ∃ (V : BitString → BitString → Bool) (p : WitnessBound),
    VerifierPolyTime V ∧
    ∀ x, L x ↔ ∃ w : BitString, w.length ≤ p x.length ∧ V x w = true

/-- P is contained in NP: a decider is a verifier that ignores its witness.
    The proof is structural once `RunsInPolyTime` / `VerifierPolyTime` are real;
    here both are `True`, so the time-bound obligations are trivially met and the
    content is the equivalence `decide x = true ↔ L x`. -/
theorem inP_subset_inNP (L : Language) (h : inP L) : inNP L := by
  obtain ⟨D⟩ := h
  refine ⟨(fun x _ => D.decide x), (fun _ => 0), trivial, ?_⟩
  intro x
  constructor
  · intro hx
    exact ⟨[], by simp, (D.correct x).mpr hx⟩
  · rintro ⟨w, _, hw⟩
    exact (D.correct x).mp hw

/-- The Riemann-Prize-level statement: P = NP, as equality of the two classes
    (as predicates on languages). -/
def P_eq_NP : Prop := ∀ L : Language, inP L ↔ inNP L

/-- The expected answer: P ≠ NP. This is the goal of the separation program. -/
def P_neq_NP : Prop := ¬ P_eq_NP

end PvsNP
