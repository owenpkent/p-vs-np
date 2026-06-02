/-
The Baker-Gill-Solovay relativization barrier (1975).

Relativizing both classes against an oracle `O`, there exist oracles `A` and `B`
with P^A = NP^A and P^B ≠ NP^B. Consequently any proof technique that relativizes
(proves its conclusion for every oracle) cannot decide P vs NP.

This module STATES the barrier. The oracle classes `inP_rel` / `inNP_rel` are
modeled as the relativized analogs of Basic.lean's classes (the decider / verifier
gets oracle access). The two existence statements are documented `sorry` markers:
the PSPACE-collapse oracle and the diagonalization oracle. The finite, runnable
illustration of the diagonalization lives in
`experiments/relativization/e_bgs_oracle.py`.
-/

import PvsNP.Basic

namespace PvsNP

/-- An oracle is a language (a membership predicate on bit strings) the machine
    may query at unit cost. -/
abbrev Oracle := BitString → Bool

/-- Relativized poly-time decider: the decision procedure may call the oracle. -/
structure PolyTimeDeciderRel (O : Oracle) (L : Language) where
  decide : Oracle → BitString → Bool
  polyTime : RunsInPolyTime (decide O)
  correct : ∀ x, decide O x = true ↔ L x

/-- The relativized class P^O. -/
def inP_rel (O : Oracle) (L : Language) : Prop := Nonempty (PolyTimeDeciderRel O L)

/-- The relativized class NP^O (verifier definition, verifier has oracle access).
    VERIFIER target #REL-defn: spell out the oracle-verifier time bound. -/
def inNP_rel (O : Oracle) (L : Language) : Prop :=
  ∃ (V : Oracle → BitString → BitString → Bool) (p : WitnessBound),
    VerifierPolyTime (V O ·) ∧
    ∀ x, L x ↔ ∃ w : BitString, w.length ≤ p x.length ∧ V O x w = true

/-- P^O = NP^O for a fixed oracle. -/
def P_eq_NP_rel (O : Oracle) : Prop := ∀ L : Language, inP_rel O L ↔ inNP_rel O L

/-- BGS, easy oracle: there is an oracle (any PSPACE-complete language) relative
    to which P and NP coincide. VERIFIER target #REL-A: the PSPACE collapse. -/
theorem bgs_oracle_collapse : ∃ A : Oracle, P_eq_NP_rel A := by
  sorry

/-- BGS, separating oracle: there is an oracle relative to which P and NP differ,
    built by diagonalization against an enumeration of poly-time oracle machines.
    VERIFIER target #REL-B: the diagonalization (the finite model is the Python
    experiment). -/
theorem bgs_oracle_separate : ∃ B : Oracle, ¬ P_eq_NP_rel B := by
  sorry

/-- The relativization barrier as a corollary: there is no single answer to
    "P^O = NP^O?" uniform over all oracles, so a relativizing technique cannot
    settle P vs NP. Stated as: the collapse and separation oracles disagree. -/
theorem relativization_barrier :
    (∃ A : Oracle, P_eq_NP_rel A) ∧ (∃ B : Oracle, ¬ P_eq_NP_rel B) :=
  ⟨bgs_oracle_collapse, bgs_oracle_separate⟩

end PvsNP
