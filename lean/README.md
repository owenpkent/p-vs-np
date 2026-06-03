# Lean 4 / Mathlib formalization of the P vs NP proof program

> Formal verification stack for the proof program. See
> [`../OPERATIONS.md`](../OPERATIONS.md) §4 for context.
>
> **Goal**: state the central objects and theorems of the P-vs-NP landscape
> (P, NP, SAT, Cook-Levin, the relativization barrier, the circuit-lower-bound
> route, and the `P_neq_NP` goal) as typed Lean declarations, so that future work
> can discharge the documented `sorry` markers into real proofs.

## Status

**Skeleton. NOT expected to build without further work.** Mathlib's
complexity-theory coverage is thin as of 2026 (there is no canonical Turing-
machine cost model wired for poly-time class definitions, no SAT, no Cook-Levin,
no P/poly). So this skeleton uses lightweight self-contained models: a
`Language` is a predicate on bit strings, "runs in polynomial time" is an abstract
`Prop` field (the first VERIFIER target), and circuits / CNF formulas are real
inductive types with real evaluation.

What this buys: the STATEMENTS are precise and typed, and several structural
lemmas are actually proved (no `sorry`): `inP_subset_inNP`, `empty_cnf_satisfiable`,
`empty_clause_unsat`, `reduction_preserves_P`, `cook_levin` (from its two parts),
`P_eq_NP_iff_SAT_in_P` (modulo the Cook-Levin inputs), `relativization_barrier`
(from its two oracle existence statements), and
`NP_not_subset_Ppoly_implies_P_neq_NP`. The genuinely hard mathematics is isolated
into a small number of named `sorry` targets below.

## Build

```powershell
cd lean
lake build
```

First-time setup needs `lake update` (downloads prebuilt Mathlib oleans). Because
this is a skeleton, a green build is not a current goal; the value is the typed
statement surface.

## Structure

```
lean/
├── lakefile.lean              # Lake build configuration (package PvsNP)
├── lean-toolchain             # Lean version pin (v4.13.0, matching the zeta repo)
├── PvsNP.lean                 # Main module: imports all sub-modules
└── PvsNP/
    ├── Basic.lean             # Language, poly-time decider/verifier, P, NP, P_eq_NP, P_neq_NP
    ├── SAT.lean               # Literal/Clause/CNF, evaluation, Satisfiable, SAT as a Language
    ├── CookLevin.lean         # Reductions, NP-hardness, NP-completeness, SAT NP-complete, P=NP iff SAT in P
    ├── Relativization.lean    # Oracle classes, BGS collapse + separation oracles, the barrier
    └── CircuitLowerBounds.lean# Circuits, P/poly, P ⊆ P/poly, NP ⊄ P/poly ⇒ P ≠ NP
```

## VERIFIER target IDs

Each `sorry` (and each abstract placeholder) carries an ID for tracking.

| ID | Module | What it asks for |
|---|---|---|
| #TM-1 | Basic.lean | Replace `RunsInPolyTime` placeholder with a real cost model + explicit polynomial bound for a one-argument decider. |
| #TM-2 | Basic.lean | Same for `VerifierPolyTime` (two-argument verifier). |
| #TM-3 | Basic.lean | Pin `WitnessBound` to an actual polynomial. |
| #SAT-enc | SAT.lean | A concrete length-polynomial CNF encode/decode pair (so SAT is a genuine `Language`). |
| #CL-1 | CookLevin.lean | `sat_in_NP`: SAT ∈ NP (needs #SAT-enc + the assignment-size bound). |
| #CL-2 | CookLevin.lean | `sat_NP_hard`: the Cook-Levin tableau construction. The mathematical core; needs the real cost model. |
| #CL-3 | CookLevin.lean | `reduction_preserves_P`: the genuine "polynomial composes with polynomial" step (currently trivial under the placeholder time bound). |
| #REL-defn | Relativization.lean | Spell out the oracle-verifier time bound for `inNP_rel`. |
| #REL-A | Relativization.lean | `bgs_oracle_collapse`: a PSPACE-complete oracle gives P^A = NP^A. |
| #REL-B | Relativization.lean | `bgs_oracle_separate`: the diagonalization oracle with P^B ≠ NP^B (finite model in the Python experiment). |
| #CKT-size | CircuitLowerBounds.lean | Replace `PolySize` placeholder with an explicit polynomial size bound. |
| #CKT-enc | CircuitLowerBounds.lean | The `BitString → (Nat → Bool)` input bridge `DecidesLang` relies on. |
| #CKT-P | CircuitLowerBounds.lean | `inP_subset_inPpoly`: the tableau-to-circuit construction (P ⊆ P/poly). |
| #CKT-goal | CircuitLowerBounds.lean | `SAT_not_in_Ppoly_implies_P_neq_NP`: the separation goal via the circuit route. The open problem. |

## Mathlib coverage gaps

As of 2026, Mathlib does NOT have: a Turing-machine cost model wired for
complexity classes, SAT / CNF complexity, Cook-Levin, P/poly, or the barrier
theorems. For each target, a VERIFIER agent should either propose a minimal
Mathlib extension to contribute back, or reduce the claim to existing Mathlib
lemmas with any extra axioms flagged.

## Mathlib mapping audit and build status (2026-06-02)

From the overnight P4a audit (toolchain present: Lean 4.13.0, Lake 5.0.0).

- **The skeleton is Mathlib-free.** The lakefile `require`s Mathlib, but no module
  imports it: every `PvsNP/*.lean` uses only core Lean (`List`, `Bool`, `Nat`,
  `Prop`). So `lake build` would fetch and build gigabytes of Mathlib for nothing.
  The modules compile against core Lean directly. Recommendation: build standalone
  (drop or comment the unused Mathlib `require`) until a target genuinely imports
  Mathlib, and reinstate it only then.
- **Per-module compile status (bare `lean`, no Mathlib), dependency order:**
  - `Basic.lean`: compiles cleanly, 0 `sorry` (the foundational classes and
    `inP_subset_inNP` are fully proved).
  - `SAT.lean`: a real compile error (not a documented `sorry`), now a P4b target.
    At line 65, `([] : Clause).eval a` resolves to the nonexistent `List.eval`
    because `Clause` is a reducible abbreviation for `List Literal`, so dot notation
    uses the `List` head. Fix: call `Clause.eval ([] : Clause) a` explicitly (or make
    `Clause` a structure). `CNF.eval` (line 40) avoids this only because its binder
    is annotated `Clause`.
  - `CookLevin.lean`, `Relativization.lean`, `CircuitLowerBounds.lean`: not yet
    reached, pending the SAT fix.
- **Per-target Mathlib mapping.** The statement surface needs no Mathlib; core Lean
  suffices. Mathlib's `Computability` namespace has Turing machines (`Turing.TM0/1/2`),
  partial recursive functions, and encodings, but NO time-bounded cost model or
  complexity classes, so #TM-1/2/3, #CL-1/2/3, #REL-*, and #CKT-* remain genuine
  gaps requiring new development rather than a lemma lookup. The external
  [lean-dojo/LeanMillenniumPrizeProblems](https://github.com/lean-dojo/LeanMillenniumPrizeProblems)
  repo is the closest existing Lean 4 statement surface for P, NP, poly-time
  reductions, and NP-completeness to diff against (it parameterizes over the missing
  cost model rather than axiomatizing it).
- **Conclusion.** The near-term win is a standalone (Mathlib-free) green build once
  the `SAT.lean` error is fixed; the Mathlib dependency should be deferred until a
  target genuinely imports it.

## How agents use this

- **BUILDER**: writes mathematical definitions in `PvsNP/`.
- **VERIFIER**: picks a target ID and converts the `sorry` (or placeholder) to a
  real proof / real definition.
- **ADVERSARY**: stress-tests proposed statements (does a claimed lemma secretly
  assume what it should prove?).
- **SYNTHESIZER**: maintains this README and the target table.

## Cross-references

- [`../experiments/PLAN.md`](../experiments/PLAN.md): the experimental thread.
- [`../experiments/relativization/`](../experiments/relativization/): the finite
  BGS diagonalization that #REL-B formalizes in the limit.
- [`../docs/research_atlas/README.md`](../docs/research_atlas/README.md): the
  architectures these statements serve.
