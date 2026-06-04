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
   evasion stays conditional on the TC0-PRF question (finding 20). The Max-IP-at-$n^\varepsilon$
   log-shave is now ATTACKED (finding 24, subsection 4b,
   `experiments/circuit_complexity/e_maxip_logshave.py`): it is genuinely OPEN with NO
   finer barrier, but every known log-shaver lands ZERO logs at $d=n^\varepsilon$ (the
   polynomial method gives only a constant; four-Russians is the wrong semiring;
   rectangular MM IS the baseline and its $\log^2 n$ is intrinsic). The polylog splits
   into the Coppersmith $\log^2 n$ overhead and the $\Theta(n^2)$ max-extraction, so a
   shave must compute the max WITHOUT enumerating all $n^2$ pairs; a threshold-sweep
   micro-idea was tried and FAILS (cost-increasing). Target-widened: a
   co-nondeterministic log-shave suffices (Chen Remarks 2.7/4.2, project inference).
   The natural-proofs "binding wall" question is now RESOLVED (finding 25,
   `experiments/natural_proofs/e_tc0_prf_collision.py`): the PRF collision does NOT doom
   the Williams route. It binds the LARGE-and-constructive (combinatorial) ALTERNATIVES,
   which is precisely WHY a non-natural method is needed; the Williams spine is
   non-natural by dropping LARGENESS not constructivity (Williams 2013), so the collision
   is silent on it. The earlier "binding constraint" framing was too pessimistic and was
   corrected across the atlas / STATE / note / finding 20. The residual open locus is the
   NEXP-to-NP descent, where the escape flips from non-largeness to non-constructivity
   (the meta-complexity high-Kt device), which against TC0 is open. So the genuine open
   obstructions on the leading path are (a) the ALGORITHMIC one (the dense THR-of-THR
   SAT / Max-IP log-shave), (b) the not-yet-assessable algebrization flag, and (c) the
   descent's non-constructivity. The descent is now MAPPED (finding 26,
   `experiments/circuit_complexity/e_leading_path_descent.py`): reaching NP is a MULTI-JOINT
   synthesis (four open joints), not one missing piece. J1 ALGORITHMIC (the log-shave, a
   GRIND, attackable now); J2 DESCENT (the algorithm+diagonalization scale, downstream of
   J1; the NP easy-witness lemma is already PROVED by Murray-Williams 2018, correcting the
   dossier A2 "circular descent" kill); J3 NON-CONSTRUCTIVITY (the BINDING joint, blocked by
   the NAMED LOCALITY BARRIER: deciding MCSP is capped at AC0[p] and cannot reach TC0
   because MAJORITY and NC1 reduce to MCSP-oracle circuits, Golovnev et al ICALP 2019 /
   CHOPRS JACM 2022); J4 COMPOSITION (no combining theorem; the W2A core relativizes). Next
   concrete sub-steps: J1 is the most-attackable joint, and its frontier is now SHARPENED
   (finding 27, `experiments/circuit_complexity/e_j1_transfer.py`): the "transfer the
   $n^3$-scale machinery" angle does NOT port, for an OPERATION reason (AFKLM shaves
   OR-idempotent triangle detection, Williams a per-entry $(\min,+)$ product; Max-IP is a
   standard product then ONE global max over output indices, neither operation). The real
   J1 frontier is the FUSED-MAX-MM (compute the global max of a small-range $(+,\times)$
   product fused into rectangular MM, without materializing the $n^2$ entries), which is
   OPEN, SETH-consistent, and barrier-free, with NO known fused product touching it. The
   structural novelty must be max-extraction-without-enumeration. The binding joint J3 is a
   published no-go (locality), so the strategic question there is whether non-local hardness
   magnification (the dossier's unbuilt 2044-2047 object) can be designed to defeat it.
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
  `strand3.e_symmetry_route`, `circuit_complexity.e_threshold_geometry_gap`,
  `circuit_complexity.e_maxip_logshave`, `natural_proofs.e_tc0_prf_collision`,
  `circuit_complexity.e_leading_path_descent`, and `circuit_complexity.e_j1_transfer` (the
  strand3 pair needs numpy + sympy; the Max-IP experiments need numpy). Standard library
  only elsewhere; plots optional.
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
| 2026-06-04 | TC0 spine: attack J1, the n^3-machinery transfer (multi-agent: 3 surveys, builder ledger, adversary, verifier; all completed) | The transfer does NOT port, for an OPERATION reason (not scale): AFKLM 2024 shaves OR-idempotent triangle detection (discards the counts the max needs); Williams 2014 shaves a per-entry $(\min,+)$ product; Max-IP is a standard product then ONE global max over output indices. Sharpens finding 24's "wrong scale" labels to "wrong operation". The real frontier is the FUSED-MAX-MM (open, SETH-consistent, barrier-free; no known fused product touches it at the log-shave scale). Micro-idea (small-range block pre-filter) tried and FAILS worst-case. New experiment `circuit_complexity/e_j1_transfer.py` (VERIFIER high, ADVERSARY sound, params web-confirmed verbatim; two scratch experiments consolidated); LEARNINGS finding 27. No progress on the prize claimed. |
| 2026-06-03 | TC0 spine: the leading-path descent to NP (multi-agent: 3 surveys [2 failed StructuredOutput], builder ledger, adversary, verifier) | The descent to NP is a MULTI-JOINT synthesis (four open joints), not one missing piece. J1 algorithmic (the log-shave, a grind); J2 descent (algorithm+diagonalization scale, downstream of J1; the NP easy-witness lemma is PROVED, Murray-Williams 2018, correcting the dossier A2 "circular" kill); J3 non-constructivity (the BINDING joint, blocked by the NAMED LOCALITY barrier, Golovnev et al ICALP 2019 / CHOPRS JACM 2022: MCSP capped at AC0[p], cannot reach TC0); J4 composition (no combining theorem, W2A core relativizes). New experiment `circuit_complexity/e_leading_path_descent.py` (descent ledger, VERIFIER high, claims web-confirmed verbatim); LEARNINGS finding 26; STATE most-leveraged-move refreshed. |
| 2026-06-03 | TC0 spine: the natural-proofs binding-wall question (multi-agent: 3 surveys, builder, adversary, verifier; synth agent failed, recovered from journal + hand-authored) | CORRECTS the project's own framing. The TC0-PRF collision does NOT doom the Williams route: it binds the LARGE-and-constructive ALTERNATIVES (which is WHY a non-natural method is needed); the Williams spine is non-natural by dropping LARGENESS not constructivity (Williams 2013, confirmed verbatim). Verdict SUBTLE/EVADED: evaded at the NEXP-level bound, open at the NEXP-to-NP descent (escape flips to non-constructivity). Fixed a real bug in the core `barriers.py` williams_acc0 fixture (natural_constructivity False->True; smoke stays 5/5). New experiment `natural_proofs/e_tc0_prf_collision.py`; LEARNINGS finding 25; "binding constraint" corrected across atlas / STATE / note section 6 / finding 20. VERIFIER high, every claim web-confirmed verbatim. |
| 2026-06-03 | TC0 spine: attack the Max-IP-at-$n^\varepsilon$ log-shave (multi-agent: 3 surveys, builder, adversary, verifier; Chen 2018 read pp.1-21) | Sharp HONEST negative coordinate (the intended outcome). The target is genuinely OPEN with NO finer barrier (the "hardness of shaving logs" theorems provably do not cover Max-IP), but every known log-shaver lands ZERO logs at $d=n^\varepsilon$. The polylog splits into the intrinsic Coppersmith $\log^2 n$ and the $\Theta(n^2)$ max-extraction; a shave must avoid enumerating the $n^2$ pairs. Threshold-sweep micro-idea tried and FAILS (cost-increasing). Target-widened to co-nondeterministic (Chen Remarks 2.7/4.2). Most-promising angle: transfer $n^3$-scale all-logs machinery down to the $n^2$-scale count-then-max product. New experiment `circuit_complexity/e_maxip_logshave.py` (VERIFIER-confirmed; two scratch experiments consolidated); LEARNINGS finding 24; note subsection 4b; two NEEDS-BODY-VERIFICATION flags cleared. No progress on the prize claimed. |

## How to update this file

- ORCHESTRATOR: update "Recommended next session actions" at session end.
- SYNTHESIZER: update everything else after agent outputs land.
- Always update "Last verified state" and "Session log".
