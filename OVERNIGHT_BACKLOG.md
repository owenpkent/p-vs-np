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

- [x] **P1a.** Meta-complexity notes -> `research_directions/02_natural_proofs_evasion.md` deepening + LEARNINGS (the leading path: proved non-constructivity of high $Kt$).
- [x] **P1b.** Approximate-degree / Williams notes -> `research_directions/01_circuit_lower_bounds.md` deepening + LEARNINGS (the $\mathsf{TC}^0$ hinge, the algorithmic method toward TC0).
- [x] **P1c.** Algebraic-topology notes -> a new subsection (the strand-3 missing object, Bockstein / Steenrod) in `02` or a short note in the dossier's vicinity + LEARNINGS.
- [x] **P1d.** GCT, proof-complexity, and stat-physics notes -> `research_directions/04`, `03`, and the SAT-phase-transition writeup respectively + LEARNINGS.

## P2. Experiment backlog (the unbuilt TODO experiments)

Each: a runnable module `experiments/<area>/e_<name>.py` with a docstring, a
`ProofTechnique` barrier-check where relevant, and a `main()` with self-check
asserts. Add a row to `experiments/PLAN.md`, check the TODO box. Verify:
`python -m experiments.<area>.e_<name>` exits 0.

- [x] **P2a.** `circuit_complexity/e_acc0_polynomial_method.py`: Razborov-Smolensky, $\mathrm{MOD}_2$ has no low-degree approximation over $\mathbb{F}_3$ (degree lower bound in miniature).
- [x] **P2b.** `proof_complexity/e_resolution_width_php.py`: resolution-width lower bound for the pigeonhole principle (Haken 1985), via the Ben-Sasson-Wigderson width-size relation.
- [x] **P2c.** `gct/e_plethysm_kronecker.py`: a small plethysm / Kronecker-coefficient computation, with the BIP 2016 occurrence no-go and the DIP 2019 multiplicity result documented as the boundary.
- [x] **P2d.** `hardness_randomness/e_nisan_wigderson_prg.py`: a Nisan-Wigderson PRG demo connecting circuit hardness to derandomization (combinatorial designs in miniature).
- [x] **P2e.** `circuit_complexity/e_monotone_clique.py`: Razborov 1985 monotone clique lower bound in miniature (method of approximations), and confirm it is a natural proof via the checker.

## P3. Strand-3 coordinate ledger (the research frontier)

Create `docs/03_research/strand3_ledger.md` if absent. Each iteration: propose
ONE candidate "non-algebrizing invariant a fast algorithm can compute" (toward
the Bockstein bridge), encode it for `algebrization_probe.py` and `barriers.py`,
run both plus a circularity check, and append the verdict to the ledger as a
coordinate (what it rules out, hence where the real object must live). Verify:
the probe and checker run; the ledger entry is honest about the kill.

- [x] **P3a.** Seed the ledger and add the first 2 candidates (e.g. a Stiefel-Whitney class of the solution complex; a mod-2 Euler-characteristic-with-Steenrod refinement). Most will be killed; that is the deliverable.
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
- 2026-06-02: P1a done. Synthesized the 7 meta-complexity notes into a "state of the art" + "open cruxes" section in research direction 02 (M3 marked done), and promoted LEARNINGS finding 12 (meta-complexity is the leading path's engine, but non-black-box is not non-relativizing, so the non-relativizing content must come from the Williams spine).
- 2026-06-02: P1b done. Synthesized the Williams-method + approximate-degree notes into a "state of the art" section in research direction 01 (M1 marked studied), and promoted LEARNINGS finding 13 (the TC0 wall is confirmed from two sides; the method is non-natural by non-largeness, and Williams 2021 names a fourth barrier corroborating finding 10).
- 2026-06-02: P1c done. Created docs/03_research/strand3_missing_object.md synthesizing the algebraic-topology notes (Hatcher Bockstein/Steenrod, Kahn-Saks-Sturtevant torsion precedent, Bjorner's computable-vs-torsion map), linked from the dossier's braided-path section, and promoted LEARNINGS finding 14 (topology gives the words and one precedent for strand 3, not a route; three gaps remain).
- 2026-06-02: P1d done. Added "state of the art" sections to research directions 04 (GCT: multiplicity obstructions strictly stronger, DIP 2019; the candidate non-algebrizing GCT invariant) and 03 (proof complexity: Razborov 1995 unprovability = A6 path; GPW 2017 lifting), and a statistical-physics section to the SAT-phase-transition writeup (clustering + OGP as average-case algorithm-class barriers, not worst-case). Promoted LEARNINGS findings 15, 16, 17. P1 (reading-notes synthesis) complete.
- 2026-06-02: P2a done. Built circuit_complexity/e_acc0_polynomial_method.py (Razborov-Smolensky in miniature): PARITY has exact F_3 multilinear degree n (top coeff 1 mod 3), low-degree F_3 polys cannot match it (best degree-2 agreement 14/16 at n=4), and the barrier checker confirms the polynomial method is natural (disqualified vs P/poly, valid only vs AC0[p]). Runs to exit 0. Added PLAN status row, checked the TODO box.
- 2026-06-02: P2b done. Built proof_complexity/e_resolution_width_php.py: PHP is UNSAT and not refutable below its hole count; min refutation width = hole count (2, 3), so the BSW width-size tradeoff is vacuous for PHP (exponent ~0) and Haken's exponential bound is bottleneck counting, not width. Promoted LEARNINGS finding 18, added PLAN row, marked research direction 03 M1 done, checked the TODO box. Runs to exit 0.
- 2026-06-02: P2c done. Built gct/e_plethysm_kronecker.py: computes S_n irreducible characters (Murnaghan-Nakayama via beta-set rim-hook removal) and Kronecker coefficients g(lam,mu,nu) from scratch; verified orthonormality, hook-length dimensions, sum(dim^2)=n!, and the trivial/sign tensor identities for n<=6 (125 and 343 Kronecker coefficients for n=4,5). These are the GCT multiplicities (#P-hard positivity, Ikenmeyer-Mulmuley-Walter). Added PLAN row, marked direction 04 M2 done, checked the TODO box. Runs to exit 0.
- 2026-06-02: P2d done. Built hardness_randomness/e_nisan_wigderson_prg.py: polynomial (l,k)-designs verified (size q, intersection <= k, stretch q^2 -> q^{k+1}); the PRG needs hardness, with easy f = PARITY distinguishable (linear dependency among output bits XORs to 0) and nonlinear f = MAJORITY resisting the same attack. Promoted LEARNINGS finding 19, added PLAN row + per-arch next step, checked the TODO box. Runs to exit 0. (P2e monotone clique still remains.)
- 2026-06-02: P2e done. Built circuit_complexity/e_monotone_clique.py: constructive Erdos-Rado sunflower extraction (greedy packing + recurse on the link), verified to find p-sunflowers in families above the s!(p-1)^s bound (2-subsets of [5], 3-subsets of [8]); barrier checker confirms Razborov's method of approximations is natural (disqualified vs P/poly, monotone-only; Razborov-Tardos: monotone hardness does not transfer). Added PLAN row, checked the TODO box. Runs to exit 0. P2 (experiment backlog) complete.
- 2026-06-02: P3a done. Seeded docs/03_research/strand3_ledger.md and built experiments/strand3/e_ledger.py: ran three candidate invariants through the algebrization probe + a strand-1 computability judgment + circularity check. Coordinates: Euler characteristic algebrizes (DEAD strand 3); Stiefel-Whitney class and Steenrod-square refinement are non-algebrizing (strand 3 OK) but fail strand 1 (no cheap #SAT count) -> OPEN. No LIVE candidate: the non-algebrizing objects are not cheap counts and the cheap count algebrizes, which is the Bockstein-bridge gap (the search should target the forcing BRIDGE, not a new count or a lone torsion class). Runs to exit 0.
