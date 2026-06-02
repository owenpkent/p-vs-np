# P versus NP: Deep Study Repo

A multi-level exploration of the P versus NP problem: from intuitive
understanding through undergraduate and graduate complexity theory to the
frontier of current research. Includes a computational experimental thread
organized around the candidate proof architectures and the three barrier
theorems that discipline every one of them.

**Operational substrate**: this repo is also structured as the substrate for an
AI-augmented (and, speculatively, AI-only) proof program for P vs NP. See
[`STATE_OF_THE_PROGRAM.md`](STATE_OF_THE_PROGRAM.md) for a one-page strategic
snapshot, [`OPERATIONS.md`](OPERATIONS.md) for how to operate it,
[`PHASE_STATE.md`](PHASE_STATE.md) for current state, and
[`docs/03_research/`](docs/03_research/) for the proof programs. The repo is a
handoff artifact: it is a research codebase, not a tool or product.

## What's Here

This repo is structured so you can enter at any level and go as deep as you want.

```
p-vs-np/
├── docs/                        # All written explanations
│   ├── 00_intuitive/            # No math required: verifying vs finding
│   ├── 01_undergraduate/        # P, NP, reductions, NP-completeness, Cook-Levin
│   ├── 02_graduate/             # Circuit classes, the three barriers, the polynomial hierarchy
│   ├── 03_research/             # Current approaches; proof programs; numbered directions
│   │   ├── research_directions/ # Research-grade directions with operational specs
│   │   └── reading_notes/       # Notes on the reference library
│   ├── implications/            # Why it matters (crypto, optimization, science, AI)
│   ├── solutions/               # Known approaches and why each is stuck
│   ├── research_atlas/          # Master research map: all architectures + obstructions
│   └── researcher_mindset.md    # The operating philosophy
├── experiments/                 # Computational thread; barrier discipline
│   ├── PLAN.md                  # Test plan + AI-centric methodology
│   ├── LEARNINGS.md             # Cross-architecture findings
│   ├── _shared/                 # ProofTechnique, BarrierChecker control, smoke_test
│   ├── relativization/          # BGS oracle diagonalization (barrier a)
│   ├── circuit_complexity/      # Hastad switching lemma / parity (architecture 1)
│   ├── natural_proofs/          # Largeness + constructivity check (barrier c)
│   └── sat_phase_transition/    # Random 3-SAT threshold + hardness peak (b)
├── references/                  # Bibliography of real papers/books (PDFs gitignored)
├── lean/                        # Lean 4 / Mathlib formal verification (skeleton)
│   ├── lakefile.lean
│   ├── PvsNP.lean               # Main module
│   └── PvsNP/                   # Basic, SAT, CookLevin, Relativization, CircuitLowerBounds
├── .claude/agents/              # Six AI agent role specifications
├── sources/                     # Original PDFs and converted text
├── visualizations/              # manim animation scripts
├── OPERATIONS.md                # How to operate this repo as the proof-program substrate
├── PHASE_STATE.md               # Current operational state (read by ORCHESTRATOR)
└── CLAUDE.md                    # Project + owner context for AI assistants
```

## The Question

**P versus NP** asks:

> Does every decision problem whose solutions can be verified in polynomial time
> also admit a polynomial-time decision algorithm?

Equivalently, is $\mathsf{SAT}$ (or any NP-complete problem) in $\mathsf{P}$? The
problem was crystallized by Cook (1971) and independently Levin, with Karp (1972)
showing 21 natural problems are NP-complete. It is one of the seven Clay
Millennium Prize Problems (worth \$1,000,000); the official statement is by
Stephen Cook. It has been open since 1971. Its resolution would reshape
cryptography, optimization, and our understanding of what efficient computation
can do.

## Stance

We are trying to solve this. That is the posture of the whole repo.

It is hard. The odds against any single program are long, and five decades of
effort by the best complexity theorists alive is the honest baseline. But "hard"
is not "impossible," and this project treats P vs NP as a target, not a monument.

Read every negative result here in that spirit. The three barriers
(relativization, natural proofs, algebrization) each rule out a class of
techniques. That is **progress**: each removes a dead branch and sharpens where
the real proof must live. Each "this won't work" is a coordinate that narrows the
search, not a verdict that the search is hopeless. The barriers together are a
compass: the proof must be non-relativizing, non-natural, and non-algebrizing at
once. Williams's 2011 $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$ proves such
techniques exist. The job is to push them down to $\mathsf{NP}$ versus
$\mathsf{P/poly}$.

## Levels

| Level | Folder | Prerequisites |
|-------|--------|---------------|
| Intuitive | `docs/00_intuitive/` | None, curiosity only |
| Undergraduate | `docs/01_undergraduate/` | Discrete math, basic algorithms |
| Graduate | `docs/02_graduate/` | Algorithms, computability, basic complexity |
| Research | `docs/03_research/` | Graduate complexity theory |
| **Research Atlas** | `docs/research_atlas/` | **Start here for the strategic map** of all architectures, failures, obstructions |

## Experimental thread

See [`experiments/PLAN.md`](experiments/PLAN.md) for the test plan. The candidate
proof architectures (circuit complexity, diagonalization, proof complexity,
Geometric Complexity Theory, hardness-vs-randomness) are disciplined throughout
by the three barrier theorems, which play the role the Davenport-Heilbronn
control plays in the companion Riemann repo. Any candidate technique must evade
all three.

Smoke test:

```powershell
python -m experiments._shared.smoke_test
```

Four experiments run to completion: the BGS relativization diagonalization, the
Hastad switching-lemma parity demo, the natural-proofs largeness/constructivity
check, and the random 3-SAT phase transition.

## Cross-cutting findings

Synthesis lives in [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md). The
dominant meta-finding: the three barriers are one coordinate system, not three
separate walls. Every technique that works on a weak circuit class fails to
generalize for a barrier-shaped reason; the few escapes (ACC0, GCT) are exactly
the techniques that are non-natural, non-relativizing, and non-algebrizing at
once. This is the project's most useful piece of map.

## Status

| Area | Status |
|------|--------|
| Repo structure | Complete |
| Solutions / approach catalog | `docs/solutions/` |
| Research atlas | `docs/research_atlas/` |
| Experiments, Phase 0 infrastructure (barrier checker + smoke test) | Complete (5/5) |
| Experiments, relativization (BGS) | Runs to completion |
| Experiments, circuit complexity (parity restriction) | Runs to completion |
| Experiments, natural proofs (largeness/constructivity) | Runs to completion |
| Experiments, SAT phase transition | Runs to completion |
| Lean 4 / Mathlib formalization | Skeleton with documented `sorry` (need not build) |
| Intuitive / undergraduate / graduate docs | Substantial |
| manim visualizations | One scene (SAT phase transition) |

## Quick Start

```powershell
# Set up environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Smoke test the barrier-checker framework
python -m experiments._shared.smoke_test

# Run an experiment
python -m experiments.sat_phase_transition.e_sat_phase

# manim scene
manim -pql visualizations/01_sat_phase_transition/sat_phase_scene.py SatPhaseTransition
```
