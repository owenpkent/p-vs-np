# Phase State (operational)

> Read by ORCHESTRATOR at the start of every session. Maintained by SYNTHESIZER.
> Living document.

## Current state (2026-06-02)

**Active mode**: AI-augmented (human owner in the critical path). Transition to
AI-only execution requires infrastructure not yet built (see
[`OPERATIONS.md`](OPERATIONS.md) §7).

**Current phase**: Phase 0 (Foundation). The repository scaffold, the
three-barrier wrong-approach detector, the four runnable experiments, the layered
docs, and the Lean skeleton are in place. The strategic map (research atlas) and
the candidate-architecture catalog are written.

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

## Phase 0 deliverables remaining

- Deeper experiments per architecture: ACC0 / Razborov-Smolensky polynomial
  method, resolution-width lower bound for the pigeonhole principle, a small GCT
  permanent-vs-determinant multiplicity computation, and a Nisan-Wigderson PRG
  demo.
- Lean expansion beyond the skeleton: Mathlib has limited complexity-theory
  coverage, so most targets require either a minimal Mathlib extension or careful
  axiom-flagged reductions.
- Expert verification of the research atlas obstruction claims.

## Architecture status (project level)

- **Circuit complexity (1)**: weak-class lower bounds (AC0, monotone, ACC0)
  demonstrated / catalogued; the gap to general circuits is the central
  obstruction, gated by the natural-proofs barrier.
- **Diagonalization (2)**: the relativization barrier is the documented limit;
  reproduced in miniature.
- **Proof complexity (3)**: catalogued (resolution, bounded-depth Frege; Cook-
  Reckhow tie to $\mathsf{NP}$ vs $\mathsf{coNP}$). No experiment yet.
- **GCT (4)**: catalogued with the Burgisser-Ikenmeyer-Panova 2016 no-go for
  occurrence obstructions. No experiment yet.
- **Hardness vs randomness (5)**: catalogued as the surrounding landscape.

## Recommended next session actions

1. **Add the ACC0 polynomial-method experiment** (Razborov-Smolensky): show that
   $\mathrm{MOD}_2$ has no low-degree polynomial approximation over
   $\mathbb{F}_3$, the algebraic complement of the switching-lemma demo.
2. **Add the resolution-width lower bound** for the pigeonhole principle (Haken
   1985), opening the proof-complexity architecture.
3. **Encode GCT in the barrier checker**: a `ProofTechnique` for the multiplicity-
   obstruction route, with the BIP 2016 no-go documented as the boundary of the
   occurrence-obstruction sub-route.

## Falsifiability triggers

- A claimed separation that turns out to relativize or algebrize: NOT triggered.
- A claimed non-natural property that turns out natural: NOT triggered.
- No progress in N sessions on the live architecture: NOT triggered (Phase 0 just
  established).

## Last verified state

- Smoke test: 5/5 passing (`python -m experiments._shared.smoke_test`).
- All four experiments run to completion under Python 3.11 with numpy/scipy/sympy
  available (the four experiments themselves use only the standard library; the
  SAT plot is optional).
- Git: initial scaffold commit (see commit log).

## Session log (recent)

| Date | Session focus | Key outputs |
|---|---|---|
| 2026-06-02 | Initial scaffold | Repo structure, three-barrier checker + smoke test (5/5), four runnable experiments, layered docs, research atlas, Lean skeleton, agent specs, references. |

## How to update this file

- ORCHESTRATOR: update "Recommended next session actions" at session end.
- SYNTHESIZER: update everything else after agent outputs land.
- Always update "Last verified state" and "Session log".
