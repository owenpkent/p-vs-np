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

1. **Attack the $\mathsf{TC}^0$-SAT hinge (now precisely located).** A 2026-06-03
   multi-agent grounding pass corrected the framing and pinned the target: the first
   threshold rung (ACC-of-THR, one bottom layer) is already climbed (Murray-Williams
   2018), the polynomial method does NOT die at threshold gates (it spends
   probabilistic degree $\Theta(\sqrt{n})$, not approximate degree $\Theta(n)$, and
   crosses one layer via Alman-Chan-Williams 2016), and the open object is a
   satisfiability / CAPP speedup of $2^{n-n^\varepsilon}$ for DENSE depth-2
   THR-of-THR with no subquadratic-bottom restriction (equivalently, the Chen 2018
   log-shaving geometry algorithm). See
   [`docs/03_research/2050_tc0_hinge_grounded.md`](docs/03_research/2050_tc0_hinge_grounded.md)
   and LEARNINGS finding 20. The geometry reduction is now GAP-MAPPED (finding 23,
   subsection 4a, `experiments/circuit_complexity/e_threshold_geometry_gap.py`): the
   THR-of-THR bottleneck is a polylog-dimension log-shave for the EXACT integer
   problems ($Z$-Max-IP, Hopcroft, exact closest/furthest pair), where best-known
   shaves ZERO logs; the single most attackable target is Boolean Max-IP at
   $d = n^\varepsilon$ (Chen Thm 1.5.1), baseline already $n^2\,\mathrm{polylog}$, only
   logs to shave. The bar is SETH-CONSISTENT and genuinely OPEN (a log-shave does not
   refute SETH; Chen disclaims it himself), with exactly one route (Thm 1.5.2, polylog
   Max-IP in $n^{2-\varepsilon}$) being a SETH-refuting barrier to AVOID. The
   Boolean-OV shave is a trap (gives only the weaker SYM-of-THR). Co-equal obstruction
   unchanged: even a successful log-shave only fires the connection; natural-proofs
   evasion stays conditional on the TC0-PRF question (finding 20). Next concrete
   sub-steps: study the Boolean-Max-IP-at-$n^\varepsilon$ log-shave (Thm 1.5.1) as the
   cleanest attackable object, and/or the natural-proofs binding-wall question.
2. **Strand-3: TWO sharp no-go coordinates now; the topology search is nearly
   exhausted.** Two 2026-06-03 multi-agent passes (real homology + group computation,
   adversary-audited, verifier-confirmed) closed both candidate shapes. (a) Finding 21:
   the "cheap count forces a located char-2 torsion class" bridge is a NO-GO (a count
   forces only EXISTENCE of torsion, a rank fact that algebrizes; the located
   $\beta(x) \ne 0$ is not count-forced, lens-space $L(p^2)$ vs $L(p)$ witness;
   `experiments/strand3/e_bockstein_forcing.py`). (b) Finding 22: the Oliver/Smith
   SYMMETRY fixed-point route (gap 2) is ALSO a no-go. The symmetry provably EXISTS
   ($\mathrm{AGL}(1,q)$ has the exact Oliver shape, verified $q \in \{4,5,8,9\}$,
   `experiments/strand3/e_symmetry_route.py`), but its certificate is the rational
   $\chi(\mathrm{Fix})$ (algebrizes, by the Oliver-number trichotomy, across the whole
   branch) and its output is a query bound $D(h) = \binom{n}{2}$, never circuit size.
   Structural root: KSS topology is downstream of the algorithm, so the complex is
   acyclic by construction and the certificate is forced rational. The ONE non-dead
   remainder is the structurally opposite free-$\mathbb{Z}/2$ Borsuk-Ulam route
   (Babson-Kozlov chromatic 2-torsion): it clears Q1 (located non-algebrizing torsion)
   but fails Q2 (bounds chromatic number, no circuit-size bridge) and is open on
   strand 1. Recommendation: do NOT re-attempt the count or Oliver shapes. Either probe
   the Babson-Kozlov route (low odds, the Q2 bridge is the wall), or treat strand 3 as a
   well-mapped dead-end and concentrate on the Williams spine / TC0 hinge (finding 20),
   which is independent of this topology search.
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
  `algebrization_probe`, `strand3.e_ledger`, `strand3.e_bockstein_forcing`,
  `strand3.e_symmetry_route`, and `circuit_complexity.e_threshold_geometry_gap` (the
  strand3 pair needs numpy + sympy). Standard library only elsewhere; plots optional.
- Strand-3 round 3 (2026-06-03): `strand3.e_bockstein_forcing` runs clean
  (VERIFIER-confirmed, real homology cross-validated by Smith normal form vs sympy);
  the algebrization probe gained two char-p RANK fixtures (`torsion_existence_count`,
  `fp_acyclicity`) now pinned as algebrizing; LEARNINGS finding 21 added; findings 9
  and 14 and the two strand-3 docs corrected for the count-forces-torsion no-go.
- Strand-3 gap 2 (2026-06-03): `strand3.e_symmetry_route` runs clean (VERIFIER-confirmed:
  AGL(1,q) Oliver structure + 2-transitivity, the chi(Fix)=1 Smith step, the PHP
  Oliver-failure, all independently re-derived). The Oliver/Smith symmetry route is a
  no-go on both Q1 (certificate is the rational chi, algebrizes) and Q2 (query bound,
  not circuit size); LEARNINGS finding 22 added; the ledger gained a ninth coordinate;
  the missing-object gap-2 reframed. Three builder scratch experiments were consolidated
  to the single `e_symmetry_route.py`.
- Lean: all five `PvsNP/` modules compile against core Lean (documented `sorry`
  targets remain).
- TC0 hinge grounding (2026-06-03): `e_tc0_sat_savings.py` rewritten and still runs
  to exit 0; the corrected note `docs/03_research/2050_tc0_hinge_grounded.md` is in
  place; LEARNINGS finding 20 added and findings 8/11/13 plus the dossier corrected.
- Git: the TC0-hinge-grounding change set (`0baf79c`, `899357f`, `149dcfa`) and the
  strand-3 round-3 change set (`670f7ef`) are committed. The strand-3 gap-2 change set
  is in the working tree, pending commit.

## Session log (recent)

| Date | Session focus | Key outputs |
|---|---|---|
| 2026-06-02 | Initial scaffold | Repo structure, three-barrier checker + smoke test (5/5), four runnable experiments, layered docs, research atlas, Lean skeleton, agent specs, references. |
| 2026-06-02 | 2050 backward-induction dossier | Nine adversarially stress-tested resolution paths; the TC0-hinge and algebrization-probe experiments; curated reading resources (31 sources downloaded). |
| 2026-06-02 | Overnight orchestrated loop (13 tasks) | Reading-notes synthesis into the research directions (LEARNINGS 11-19); five architecture experiments; the strand-3 coordinate ledger; two real Lean bugs fixed (skeleton now compiles against core Lean); MAJORITY approximate-degree correction. |
| 2026-06-03 | Documentation refresh | README, STATE_OF_THE_PROGRAM, and PHASE_STATE updated to current reality; repo-wide no-dash check; pushed. |
| 2026-06-03 | TC0 hinge grounding (multi-agent: 4 surveyors, fact-checkers, builder, adversary, final fact-check) | Corrected the "polynomial method dies at threshold gates" conflation (probabilistic vs approximate degree); located the open frontier as dense depth-2 THR-of-THR; caught 3 synthesis defects (paper-title, gates-vs-wires, over-strong algebrization claim). New note `2050_tc0_hinge_grounded.md`; LEARNINGS finding 20; findings 8/11/13 and the dossier corrected; experiment rewritten, smoke test 5/5. |
| 2026-06-03 | Strand-3 Bockstein bridge (multi-agent: 3 surveys, builder, adversary, verifier) | Verdict NO-GO COORDINATE: a cheap count forces only the EXISTENCE of torsion (a rank fact that algebrizes), never a located $\beta(x)$; lens-space $L(p^2)$ vs $L(p)$ witness. New experiment `strand3/e_bockstein_forcing.py` (real homology, VERIFIER-confirmed); probe gained the third invariant category (char-p rank functionals algebrize too) + two fixtures; LEARNINGS finding 21; findings 9/14 and both strand-3 docs corrected; ledger gained two coordinates (LIVE still 0). Reframed live route: symmetry (Smith-theory fixed point), not count. |
| 2026-06-03 | Strand-3 gap 2, the symmetry route (multi-agent: 3 surveys, builder, adversary, verifier) | Verdict NO-GO COORDINATE on both decisive questions. The symmetry provably EXISTS (AGL(1,q) Oliver structure verified $q \in \{4,5,8,9\}$) but Q1 fails (certificate is the rational $\chi(\mathrm{Fix})$, algebrizes by the Oliver-number trichotomy across the whole branch) and Q2 fails (query bound $\binom{n}{2}$, never circuit size). Structural root: KSS topology is downstream of the algorithm, so the complex is acyclic by construction. New experiment `strand3/e_symmetry_route.py` (group + homology computation, VERIFIER-confirmed; three scratch files consolidated to one); LEARNINGS finding 22; ledger ninth coordinate; gap-2 reframed. Only non-dead strand-3 remainder: the free-$\mathbb{Z}/2$ Babson-Kozlov route (clears Q1, fails Q2). |
| 2026-06-03 | TC0 spine: Chen-2018 fine-grained gap map (multi-agent: 3 surveys, builder, adversary, verifier; primary sources read directly) | FAVORABLE coordinate. The THR-of-THR bottleneck is a polylog-dimension log-shave for the EXACT integer geometry ($Z$-Max-IP, Hopcroft, exact closest/furthest pair), best-known shaves ZERO logs; most attackable = Boolean Max-IP at $d=n^\varepsilon$ (Thm 1.5.1). The bar is SETH-CONSISTENT and OPEN (a log-shave does not refute SETH); exactly one route (Thm 1.5.2) is a SETH-refuting barrier to avoid; the Boolean-OV shave is a trap (only SYM-of-THR). New experiment `circuit_complexity/e_threshold_geometry_gap.py` (gap calculator, VERIFIER-confirmed, all params web-verified verbatim; one scratch file consolidated); LEARNINGS finding 23; note subsection 4a + section-8 upgrade (Chen 2018 verified, companion SETH paper added, unpublished-preprint status confirmed). |

## How to update this file

- ORCHESTRATOR: update "Recommended next session actions" at session end.
- SYNTHESIZER: update everything else after agent outputs land.
- Always update "Last verified state" and "Session log".
