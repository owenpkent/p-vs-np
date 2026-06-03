# Phase State (operational)

> Read by ORCHESTRATOR at the start of every session. Maintained by SYNTHESIZER.
> Living document.

## Current state (2026-06-03)

**Active mode**: AI-augmented (human owner in the critical path). Transition to
AI-only execution requires infrastructure not yet built (see
[`OPERATIONS.md`](OPERATIONS.md) §7).

**Current phase**: Phase 0 (Foundation) complete, plus a first research pass. The
scaffold, the three-barrier detector, the layered docs, the research atlas, and the
Lean skeleton are in place. Since then: the 2050 backward-induction dossier, 31
grounded reading notes synthesized into the research directions, a per-architecture
experiment suite (the Phase-0 demos plus Razborov-Smolensky, pigeonhole resolution
width, Kronecker coefficients, Nisan-Wigderson, monotone clique, and the TC0-SAT
hinge), the strand-3 coordinate ledger, and a Lean skeleton that now compiles against
core Lean. See [`STATE_OF_THE_PROGRAM.md`](STATE_OF_THE_PROGRAM.md) "Recent progress".

## Phase 0 deliverables done

- Three-barrier checker (`experiments/_shared/barriers.py`) with the canonical
  technique library and a 5/5 smoke test.
- Four runnable experiments, each with an honest writeup:
  - relativization: BGS oracle diagonalization defeats all modeled poly-time
    oracle machines ($\mathsf{P}^B \ne \mathsf{NP}^B$ in miniature).
  - circuit complexity: Hastad switching-lemma parity demo (parity is
    restriction-robust; width-$w$ terms collapse at the exact predicted rate).
  - natural proofs: largeness + constructivity check; MCSP localized as the
    constructivity crux.
  - SAT phase transition: crossing at $\alpha \approx 4.28$, hardness peak at
    4.25, near $\alpha_c \approx 4.267$.
- Layered docs (intuitive, undergraduate, graduate, research).
- Research atlas cataloging all candidate architectures and their obstructions.
- Solutions catalog and implications docs.
- Lean 4 skeleton with typed statements and documented `sorry` markers (Basic,
  SAT, CookLevin, Relativization, CircuitLowerBounds).
- Reference bibliography of real papers and books.
- Agent role specifications in `.claude/agents/`.

## Deliverables remaining

- The per-architecture experiments (Razborov-Smolensky, pigeonhole resolution width,
  GCT Kronecker computation, Nisan-Wigderson) are DONE. The genuine open work is now
  the mathematics they point at, not more scaffolding: the TC0-SAT speedup (the
  hinge), the strand-3 forcing Bockstein bridge, and the Lean `sorry` targets.
- Lean: the skeleton compiles against core Lean; the documented `sorry` targets
  (#CL, #REL, #CKT) are the open mathematics. Mathlib has no cost/poly-time class to
  wire to, so they need new development rather than a lemma lookup.
- Expert verification of the research atlas obstruction claims and the reading-note
  syntheses (all AI-produced, none externally reviewed).

## Architecture status (project level)

- **Circuit complexity (1)**: weak-class lower bounds (AC0, monotone, ACC0)
  demonstrated / catalogued; the gap to general circuits is the central
  obstruction, gated by the natural-proofs barrier.
- **Diagonalization (2)**: the relativization barrier is the documented limit;
  reproduced in miniature.
- **Proof complexity (3)**: catalogued (resolution, bounded-depth Frege; Cook-
  Reckhow tie to $\mathsf{NP}$ vs $\mathsf{coNP}$). Experiment: pigeonhole resolution
  width (the BSW width-size tradeoff is vacuous for PHP; Haken needs bottleneck
  counting).
- **GCT (4)**: catalogued with the Burgisser-Ikenmeyer-Panova 2016 no-go for
  occurrence obstructions. Experiments: the multiplicity-obstruction barrier check
  and a from-scratch Kronecker-coefficient computation; DIP 2019 shows multiplicity
  obstructions are strictly stronger.
- **Hardness vs randomness (5)**: catalogued as the surrounding landscape.

## Recommended next session actions

1. **Attack the $\mathsf{TC}^0$-SAT hinge.** A non-trivial threshold-circuit
   satisfiability / CAPP algorithm beating brute force, fed through the Williams
   connection, is the single most-leveraged target (modeled in
   `circuit_complexity/e_tc0_sat_savings.py`). The speedup must be combinatorial,
   not the polynomial method, which dies at threshold gates.
2. **Specify the strand-3 forcing bridge.** The coordinate ledger shows no invariant
   clears both strands; the object worth building is a Bockstein / universal-
   coefficients sequence forcing a mod-2 torsion class nonzero from a cheap count.
3. **Discharge a Lean `sorry`** or seek external review of the atlas obstruction
   claims and reading-note syntheses. These are verification, not new scaffolding.

## Falsifiability triggers

- A claimed separation that turns out to relativize or algebrize: NOT triggered.
- A claimed non-natural property that turns out natural: NOT triggered.
- No progress in N sessions on the live architecture: NOT triggered (Phase 0 just
  established).

## Last verified state (2026-06-03)

- Smoke test: 5/5 passing (`python -m experiments._shared.smoke_test`).
- All experiment modules run to completion (re-verified 2026-06-03): the Phase-0
  four plus `e_tc0_sat_savings`, `e_acc0_polynomial_method`, `e_monotone_clique`,
  `e_resolution_width_php`, `e_plethysm_kronecker`, `e_nisan_wigderson_prg`,
  `algebrization_probe`, and `strand3.e_ledger`. Standard library only; plots optional.
- Lean: all five `PvsNP/` modules compile against core Lean (documented `sorry`
  targets remain).
- Git: 17 commits since the scaffold; working tree clean.

## Session log (recent)

| Date | Session focus | Key outputs |
|---|---|---|
| 2026-06-02 | Initial scaffold | Repo structure, three-barrier checker + smoke test (5/5), four runnable experiments, layered docs, research atlas, Lean skeleton, agent specs, references. |
| 2026-06-02 | 2050 backward-induction dossier | Nine adversarially stress-tested resolution paths; the TC0-hinge and algebrization-probe experiments; curated reading resources (31 sources downloaded). |
| 2026-06-02 | Overnight orchestrated loop (13 tasks) | Reading-notes synthesis into the research directions (LEARNINGS 11-19); five architecture experiments; the strand-3 coordinate ledger; two real Lean bugs fixed (skeleton now compiles against core Lean); MAJORITY approximate-degree correction. |
| 2026-06-03 | Documentation refresh | README, STATE_OF_THE_PROGRAM, and PHASE_STATE updated to current reality; repo-wide no-dash check; pushed. |

## How to update this file

- ORCHESTRATOR: update "Recommended next session actions" at session end.
- SYNTHESIZER: update everything else after agent outputs land.
- Always update "Last verified state" and "Session log".
