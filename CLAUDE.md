# CLAUDE.md

Project-specific instructions for Claude Code. Read on every session start. This
file carries both the project's technical context (architectures, conventions,
the barrier discipline) and the human-side context (owner, tech stack, agent
infrastructure).

## What this repo is

A research-and-study project on the P versus NP problem. It contains:
- Layered docs (intuitive, undergraduate, graduate, research) on P, NP, and the
  separation question
- A strategic landscape document (`docs/research_atlas/`) cataloging every known
  proof architecture with its obstructions
- A computational experimental thread (`experiments/`) organized around the
  candidate proof architectures and the three barrier theorems
- A Lean 4 / Mathlib formalization skeleton (`lean/`)

It is **not** a tool or product. It is a research codebase. Output is markdown
documents, numerical experiments, visualizations, and Lean proofs.

## Stance (read this before writing any framing)

The posture of this project is that we are trying to solve P vs NP. It is hard
and the odds are long, but it is a target, not a monument, and nothing here
should be written as if the problem were impossible.

When you document a negative result, frame it as progress. A barrier that rules
out a class of techniques (relativization, natural proofs, algebrization) has
removed a dead branch and sharpened where the real proof must live. Each "this
won't work" is a coordinate that narrows the search.

Avoid fatalistic phrasing ("stuck," "hopeless," "can never"). Prefer the
directional reading: the three barriers are a **compass** saying the proof must
be non-relativizing, non-natural, and non-algebrizing at once. Williams's 2011
result proves such techniques exist. Keep the math exactly as rigorous as it is
(a proved barrier is still a barrier, an open problem is still open). Change the
tone, not the theorems.

## About the owner

The owner is Owen, a wheelchair user with muscular dystrophy.

- **Typing is hard.** Be proactive. Make decisions. Don't ask for confirmation on
  small things.
- **Offer A/B/C choices** when input is needed. One letter is faster than a
  sentence.
- **PowerShell on Windows.** Use PowerShell syntax. Prefer single-line commands.
- **Accessibility matters.** Many of Owen's projects are tools he actually uses.

## START HERE

- **Mindset and philosophy**: [`docs/researcher_mindset.md`](docs/researcher_mindset.md).
  The problem is a target not a monument, we advance a front, negative results are
  coordinates, honesty is the engine. Read this first.
- **Research strategy**: [`docs/research_atlas/README.md`](docs/research_atlas/README.md).
  Comprehensive catalog of all architectures, what is stuck, what is missing.
- **Experiments**: [`experiments/PLAN.md`](experiments/PLAN.md). The test plan
  with current status per architecture.
- **Proof program work**: [`PHASE_STATE.md`](PHASE_STATE.md),
  [`OPERATIONS.md`](OPERATIONS.md).
- **Lean substrate**: [`lean/README.md`](lean/README.md).

## Core conceptual framework

The project is organized around **candidate proof architectures** (from
[`docs/solutions/README.md`](docs/solutions/README.md) and
[`experiments/PLAN.md`](experiments/PLAN.md)):

1. **Circuit complexity** (prove $\mathsf{NP} \not\subseteq \mathsf{P/poly}$):
   AC0, monotone, ACC0 (Williams 2011), formula size.
2. **Diagonalization and hierarchy theorems**: the limit of pure diagonalization
   for P vs NP.
3. **Proof complexity**: propositional proof-system lower bounds; $\mathsf{NP}$ vs
   $\mathsf{coNP}$.
4. **Geometric Complexity Theory** (Mulmuley-Sohoni): permanent vs determinant
   via representation theory; the Burgisser-Ikenmeyer-Panova 2016 no-go.
5. **Hardness vs randomness / structural**: $\mathsf{BPP}$ vs $\mathsf{P}$, the
   PCP theorem, hardness amplification.

## The barrier discipline (the wrong-approach detector)

The three **barrier theorems** are this project's structural sanity check, the
analog of the Davenport-Heilbronn discipline in the companion Riemann repo:

- **Relativization** (Baker-Gill-Solovay 1975): oracles $A, B$ with
  $\mathsf{P}^A = \mathsf{NP}^A$ and $\mathsf{P}^B \ne \mathsf{NP}^B$. A technique
  that relativizes cannot resolve P vs NP.
- **Natural proofs** (Razborov-Rudich 1994): a large + constructive lower-bound
  property cannot exist if strong pseudorandom generators do.
- **Algebrization** (Aaronson-Wigderson 2008): extends relativization to
  low-degree oracle extensions; current techniques algebrize.

Any candidate technique in any architecture must **evade all three**. The
mechanical checker is `experiments/_shared/barriers.py`. Run
`python -m experiments._shared.smoke_test` to verify it (5/5 tests pinning the
barrier profiles of diagonalization, Razborov monotone, arithmetization, and
Williams ACC0).

## Tech stack

- **Language**: Python (primary). Lean 4 (formal verification).
- **Python libraries**: `numpy`, `scipy`, `sympy`, `matplotlib`. The experiments
  deliberately keep dependencies light; the barrier checker and the BGS / parity
  / natural-proofs experiments use the standard library only.
- **Visualization**: manim (3Blue1Brown style). `pip install manim`.
- **Formal verification**: Lean 4 + Mathlib (`lean/` directory, requires `elan`).
- **Docs**: Markdown with LaTeX math (`$...$` inline, `$$...$$` block in files;
  plain Unicode in chat).

## Conventions

- Experiments are runnable modules invoked from the repo root via
  `python -m experiments.<area>.<name>`. Imports use
  `from experiments._shared import ...`.
- Candidate techniques are encoded as `ProofTechnique` objects and run through
  `BarrierChecker` before any deeper investment.
- Plots save as `.png` (gitignored). Numerical results never depend on
  matplotlib being importable.

## Style

- **No em dashes or en dashes** anywhere, in any file. (Global preference. Use
  periods, colons, parentheses, or hyphens instead.) Rewrite the sentence
  instead. Absolute rule.
- Inline math in markdown uses `$...$` for inline, `$$...$$` for display.
- In chat output use Unicode and plain text for math (no KaTeX surface).
- Code: explanatory module-level docstrings, minimal inline comments. Comments
  explain WHY, not WHAT.

## Running things

```powershell
# Smoke test the barrier-checker infrastructure
python -m experiments._shared.smoke_test

# Run an experiment (each is a python module)
python -m experiments.relativization.e_bgs_oracle
python -m experiments.circuit_complexity.e_parity_restriction
python -m experiments.natural_proofs.e_largeness_constructivity
python -m experiments.sat_phase_transition.e_sat_phase

# Build the Lean skeleton (requires elan + lake; skeleton, may not build)
cd lean; lake build
```

## Git commits

```powershell
git add -A; git commit -m "docs: add intuitive explanation"
```

Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`. Never
commit or push without per-action authorization.

## Agent infrastructure (AI-only proof program substrate)

Six agent roles in `.claude/agents/`:

- **SURVEYOR**: literature synthesis + scorecard maintenance.
- **BUILDER**: propose mathematical constructions (definitions, candidate
  techniques, lower-bound attempts).
- **VERIFIER**: translate to Lean 4 / Mathlib and verify.
- **ADVERSARY**: run the three-barrier discipline; counterexample search.
- **SYNTHESIZER**: integrate verified outputs into the project dossier.
- **ORCHESTRATOR**: schedule work; manage compute budget; decide abandonment.

See [`OPERATIONS.md`](OPERATIONS.md) for the full operational guide.

## Known landmarks

- Cook 1971 / Levin: SAT is NP-complete. Karp 1972: 21 NP-complete problems.
- Baker-Gill-Solovay 1975: relativization barrier (oracles both ways).
- Razborov 1985: exponential monotone lower bound for clique.
- Razborov-Rudich 1994: natural-proofs barrier.
- Aaronson-Wigderson 2008: algebrization barrier.
- Williams 2011: $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$ (threads all three
  barriers).
- Random 3-SAT threshold: $\alpha_c \approx 4.267$ (Mertens-Mezard-Zecchina 2006;
  large-$k$ sharp threshold Ding-Sly-Sun 2015).

## When in doubt

- The atlas (`docs/research_atlas/README.md`) is the master reference for what
  has been tried and what is stuck.
- The plan (`experiments/PLAN.md`) is the master reference for the experimental
  thread.
- The three-barrier discipline is the project's structural sanity check. If a
  proposed technique does not explain how it evades all three barriers, it is
  almost certainly insufficient.
