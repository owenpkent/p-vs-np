# Overnight orchestrated backlog

> The worklist for the self-paced overnight `/loop`. This is the persistent
> state: each iteration reads this file, advances the top unchecked task, and
> records progress. Companion to [`PHASE_STATE.md`](PHASE_STATE.md),
> [`OPERATIONS.md`](OPERATIONS.md), and [`TODO.md`](TODO.md). Seeded 2026-06-02.

## Loop iteration contract

Each iteration:

1. Read this file. Pick the highest-priority unchecked `[ ]` task whose
   dependencies are met.
2. Execute it to its stated definition of done (BUILD).
3. Verify: run the stated command. It must pass (exit 0, or the stated check).
   If it does not, fix it before committing, or revert and log why.
4. Integrate (SYNTHESIZE): update `experiments/LEARNINGS.md`, the relevant doc,
   and `TODO.md` as the task specifies.
5. Commit with a conventional message (`feat:`, `docs:`, `chore:`).
6. Check the box, append a dated line to the Log at the bottom.
7. When all tasks are checked, stop the loop.

## Honesty guardrails (non-negotiable)

- Never weaken or delete a self-check assertion to make it pass. The self-check
  is the point.
- A candidate technique that hits a barrier is a SUCCESS, recorded as a
  coordinate. It is not a failure to hide or to flag-flip around.
- Never claim a proof of P vs NP or of any open problem. Scope every result
  ("against this restricted class", "conditional on this assumption").
- Run every candidate technique through `experiments/_shared/barriers.py` and,
  where relevant, `experiments/_shared/algebrization_probe.py`.
- House style: no em dashes or en dashes anywhere. `$...$` for math in markdown.
- Each iteration commits, so the morning review is a clean audit trail.

## P1. Reading-notes synthesis (depends on the reading-notes workflow)

For each block below: read the new notes under
`docs/03_research/reading_notes/<topic>/`, synthesize them into a "state of the
art and open cruxes" subsection in the matching research direction, and promote 1
to 3 grounded findings into `experiments/LEARNINGS.md`. Verify: links resolve,
no dashes, claims trace to a cited note.

- [ ] **P1a.** Meta-complexity notes -> `research_directions/02_natural_proofs_evasion.md` deepening + LEARNINGS (the leading path: proved non-constructivity of high $Kt$).
- [ ] **P1b.** Approximate-degree / Williams notes -> `research_directions/01_circuit_lower_bounds.md` deepening + LEARNINGS (the $\mathsf{TC}^0$ hinge, the algorithmic method toward TC0).
- [ ] **P1c.** Algebraic-topology notes -> a new subsection (the strand-3 missing object, Bockstein / Steenrod) in `02` or a short note in the dossier's vicinity + LEARNINGS.
- [ ] **P1d.** GCT, proof-complexity, and stat-physics notes -> `research_directions/04`, `03`, and the SAT-phase-transition writeup respectively + LEARNINGS.

## P2. Experiment backlog (the unbuilt TODO experiments)

Each: a runnable module `experiments/<area>/e_<name>.py` with a docstring, a
`ProofTechnique` barrier-check where relevant, and a `main()` with self-check
asserts. Add a row to `experiments/PLAN.md`, check the TODO box. Verify:
`python -m experiments.<area>.e_<name>` exits 0.

- [ ] **P2a.** `circuit_complexity/e_acc0_polynomial_method.py`: Razborov-Smolensky, $\mathrm{MOD}_2$ has no low-degree approximation over $\mathbb{F}_3$ (degree lower bound in miniature).
- [ ] **P2b.** `proof_complexity/e_resolution_width_php.py`: resolution-width lower bound for the pigeonhole principle (Haken 1985), via the Ben-Sasson-Wigderson width-size relation.
- [ ] **P2c.** `gct/e_plethysm_kronecker.py`: a small plethysm / Kronecker-coefficient computation, with the BIP 2016 occurrence no-go and the DIP 2019 multiplicity result documented as the boundary.
- [ ] **P2d.** `hardness_randomness/e_nisan_wigderson_prg.py`: a Nisan-Wigderson PRG demo connecting circuit hardness to derandomization (combinatorial designs in miniature).
- [ ] **P2e.** `circuit_complexity/e_monotone_clique.py`: Razborov 1985 monotone clique lower bound in miniature (method of approximations), and confirm it is a natural proof via the checker.

## P3. Strand-3 coordinate ledger (the research frontier)

Create `docs/03_research/strand3_ledger.md` if absent. Each iteration: propose
ONE candidate "non-algebrizing invariant a fast algorithm can compute" (toward
the Bockstein bridge), encode it for `algebrization_probe.py` and `barriers.py`,
run both plus a circularity check, and append the verdict to the ledger as a
coordinate (what it rules out, hence where the real object must live). Verify:
the probe and checker run; the ledger entry is honest about the kill.

- [ ] **P3a.** Seed the ledger and add the first 2 candidates (e.g. a Stiefel-Whitney class of the solution complex; a mod-2 Euler-characteristic-with-Steenrod refinement). Most will be killed; that is the deliverable.
- [ ] **P3b.** (recurring) One new candidate per visit until 6 coordinates are logged.

## P4. Lean substrate (slow, durable)

Each iteration: advance `lean/` by wiring one statement to Mathlib or discharging
one placeholder toward a green `lake build`. Verify: `cd lean; lake build`
progresses, or document precisely what blocks it.

- [ ] **P4a.** Audit which `sorry`/placeholder predicates in `lean/PvsNP*.lean` can map to real Mathlib definitions; record findings in `lean/README.md`.
- [ ] **P4b.** Replace one placeholder predicate with a real statement (or document why Mathlib cannot yet support it).

## Log

(The loop appends one dated line per completed task here.)

- 2026-06-02: backlog seeded. Awaiting the reading-notes workflow before P1.
