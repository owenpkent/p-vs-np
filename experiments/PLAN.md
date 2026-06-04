# Proof-architectures plan: testing candidate routes to P vs NP

> The experimental thread's master plan. Analogous to the companion Riemann
> repo's `PROOF_ARCHITECTURES_PLAN.md`. It lays out the candidate proof
> architectures for P vs NP, the wrong-approach detector that disciplines all of
> them (the three barrier theorems), and the per-architecture experiment status.

## The question

Is $\mathsf{P} = \mathsf{NP}$? Equivalently: does every decision problem whose
solutions are verifiable in polynomial time also admit a polynomial-time
decision algorithm? By Cook (1971) and Levin, and the 21 NP-complete problems of
Karp (1972), this is equivalent to asking whether any single NP-complete problem
(SAT, CLIQUE, 3-COLORING, ...) is in $\mathsf{P}$. The official Clay Millennium
Prize statement is by Stephen Cook.

The consensus expectation is $\mathsf{P} \ne \mathsf{NP}$, which would follow
from $\mathsf{NP} \not\subseteq \mathsf{P/poly}$ (a circuit lower bound). No
proof in either direction is known.

## The wrong-approach detector: three barriers

This is the project's structural discipline, the analog of the
Davenport-Heilbronn control in the Riemann repo. Any candidate technique must
evade all three published barrier theorems. The mechanical checker lives in
[`_shared/barriers.py`](_shared/barriers.py).

| Barrier | Reference | Disqualifies |
|---|---|---|
| Relativization | Baker-Gill-Solovay 1975 | techniques valid for every oracle |
| Natural proofs | Razborov-Rudich 1994 | large + constructive lower-bound properties (assuming strong PRGs) |
| Algebrization | Aaronson-Wigderson 2008 | techniques valid under low-degree oracle extensions |

Evading all three is necessary, not sufficient. Williams's 2011
$\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$ is the one technique known to thread
all three.

## Candidate proof architectures

These replace the Riemann repo's four RH architectures.

1. **Circuit complexity / circuit lower bounds.** To separate, prove
   $\mathsf{NP} \not\subseteq \mathsf{P/poly}$. Known unconditional fragments:
   AC0 lower bounds (Furst-Saxe-Sipser, Hastad switching lemma; parity not in
   AC0), monotone circuits (Razborov, clique), ACC0 (Williams 2011:
   $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$), depth-3 and formula-size
   bounds. The gap to general circuits is the central obstruction.
2. **Diagonalization and hierarchy theorems.** Time and space hierarchy theorems
   are proved by diagonalization. The relativization barrier marks the limit of
   pure diagonalization for P vs NP.
3. **Proof complexity.** Propositional proof-system lower bounds (resolution,
   bounded-depth Frege). Ties $\mathsf{NP}$ vs $\mathsf{coNP}$ to the existence
   of short propositional proofs (Cook-Reckhow).
4. **Geometric Complexity Theory (Mulmuley-Sohoni).** Permanent vs determinant
   via representation theory and orbit closures. Note the Burgisser-Ikenmeyer-
   Panova 2016 no-go for occurrence obstructions, which closed the original
   plan A of GCT.
5. **Hardness vs randomness / structural surroundings.** $\mathsf{BPP}$ vs
   $\mathsf{P}$, the PCP theorem, hardness amplification. The landscape that
   constrains and informs the separation question.

## Experiment status

| Architecture | Experiment | Status | Result |
|---|---|---|---|
| Wrong-approach detector | [`_shared/`](_shared/) barrier checker + smoke test | Done | 5/5 smoke tests pass; four canonical techniques' barrier profiles pinned |
| Diagonalization (barrier) | [`relativization/e_bgs_oracle.py`](relativization/) | Runs to completion | BGS diagonalization defeats all 5 modeled poly-time oracle machines; $\mathsf{P}^B \ne \mathsf{NP}^B$ in miniature |
| Circuit complexity | [`circuit_complexity/e_parity_restriction.py`](circuit_complexity/) | Runs to completion | parity is restriction-robust (1856/1856), width-$w$ terms collapse at empirical 0.589 vs exact 0.594 |
| Natural proofs (barrier) | [`natural_proofs/e_largeness_constructivity.py`](natural_proofs/) | Runs to completion | high-sensitivity property is natural (large+constructive); MCSP constructivity is the open crux |
| Hardness landscape | [`sat_phase_transition/e_sat_phase.py`](sat_phase_transition/) | Runs to completion | SAT/UNSAT crossing at $\alpha \approx 4.28$, hardness peak at 4.25, near $\alpha_c \approx 4.267$ |
| Circuit complexity (the hinge) | [`circuit_complexity/e_tc0_sat_savings.py`](circuit_complexity/e_tc0_sat_savings.py) | Runs to completion | models the $\mathsf{TC}^0$ step of the Williams program; CORRECTED (finding 20): the polynomial method does NOT die at threshold gates (it spends probabilistic degree $\Theta(\sqrt{n})$, not approximate degree $\Theta(n)$, and already crosses one threshold layer); reproduces the savings mirage, $2^{m^{0.001}}$ does not beat $m^3$ until $m \approx 10^{4668}$ |
| Algebrization probe | [`_shared/algebrization_probe.py`](_shared/algebrization_probe.py) | Runs to completion | classifies a hardness invariant as algebrizing char-0 trace/rank/volume vs candidate-non-algebrizing mod-2 torsion |
| Circuit complexity (polynomial method) | [`circuit_complexity/e_acc0_polynomial_method.py`](circuit_complexity/e_acc0_polynomial_method.py) | Runs to completion | PARITY has exact $\mathbb{F}_3$ multilinear degree $n$ (top coefficient $\equiv 1 \bmod 3$); low-degree $\mathbb{F}_3$ polynomials cannot match it (best degree-2 agreement 14/16 at $n=4$); the method is natural, disqualified vs $\mathsf{P/poly}$, valid only vs $\mathsf{AC}^0[p]$ |
| Proof complexity (resolution width) | [`proof_complexity/e_resolution_width_php.py`](proof_complexity/e_resolution_width_php.py) | Runs to completion | PHP min refutation width equals the hole count (2 and 3 for the two smallest cases), so the BSW width-size tradeoff is vacuous for PHP (exponent $\approx 0$, Haken needs bottleneck counting); BSW is exponential for constant-width $O(n)$-variable formulas (Tseitin, random k-SAT) |
| GCT (Kronecker coefficients) | [`gct/e_plethysm_kronecker.py`](gct/e_plethysm_kronecker.py) | Runs to completion | computes $S_n$ characters (Murnaghan-Nakayama) and Kronecker coefficients $g(\lambda,\mu,\nu)$ from scratch; verifies orthonormality, hook-length dimensions, and the trivial/sign tensor identities for $n \le 6$. These are the GCT multiplicities, whose positivity is #P-hard to decide |
| Hardness vs randomness (NW PRG) | [`hardness_randomness/e_nisan_wigderson_prg.py`](hardness_randomness/e_nisan_wigderson_prg.py) | Runs to completion | builds the polynomial $(l,k)$-design (size $q$, intersection $\le k$, stretch $q^2 \to q^{k+1}$) and shows NW with an easy $f$ (parity) is distinguishable while a nonlinear $f$ (majority) resists, so the PRG property needs hardness |
| Circuit complexity (monotone) | [`circuit_complexity/e_monotone_clique.py`](circuit_complexity/e_monotone_clique.py) | Runs to completion | constructive Erdos-Rado sunflower extraction (the engine of Razborov's method of approximations), verified on families above the $s!(p-1)^s$ bound; the barrier checker confirms the method is natural, hence monotone-only and blocked against $\mathsf{P/poly}$ |

### The leading-path spine (TC0 / Williams), 2026-06-03/04 (findings 20-30)

A connected sequence of multi-agent passes anatomized the leading path (the Williams
algorithm-to-lower-bound spine toward $\mathsf{NEXP} / \mathsf{NP} \not\subseteq$ dense
$\mathsf{TC}^0$). Each is grounded against primary sources, adversarially audited, and
verifier-checked; no progress on the prize is claimed.

| Architecture | Experiment | Status | Result |
|---|---|---|---|
| Circuit complexity (geometry gap) | [`circuit_complexity/e_threshold_geometry_gap.py`](circuit_complexity/e_threshold_geometry_gap.py) | Runs to completion | Chen 2018 reduces $\mathsf{NEXP} \not\subseteq$ THR-of-THR to a polylog-dimension geometry log-shave (finding 23). The bar is SETH-CONSISTENT and genuinely open; the Boolean-OV shave is a trap (only SYM-of-THR); one route (Thm 1.5.2) would refute SETH |
| Circuit complexity (the log-shave) | [`circuit_complexity/e_maxip_logshave.py`](circuit_complexity/e_maxip_logshave.py) | Runs to completion | the most attackable target, Boolean Max-IP at $d = n^\varepsilon$ (Chen Thm 1.5.1), attacked (finding 24): open, no finer barrier, but every known log-shaver lands ZERO logs; the polylog splits into Coppersmith $\log^2 n$ + the $\Theta(n^2)$ max-extraction |
| Circuit complexity (J1 transfer) | [`circuit_complexity/e_j1_transfer.py`](circuit_complexity/e_j1_transfer.py) | Runs to completion | the $n^3$-machinery transfer does NOT port, for an OPERATION reason (finding 27): AFKLM shaves OR-idempotent detection, Williams a per-entry $(\min,+)$ product; Max-IP is a standard product then one global max. The real frontier is the FUSED-MAX-MM (open, barrier-free) |
| Circuit complexity (fused-max-MM, J1 built) | [`circuit_complexity/e_fused_max_mm.py`](circuit_complexity/e_fused_max_mm.py) | Runs to completion, self-checks pass | the fused-max-MM is BUILT as FOUR candidate fusions (finding 28): moments, spectral / low-rank, count-preserving regularity, sketch / heavy-hitter. All hit ONE shared wall: every fast fusion is a bulk $\ell_2$ / average / moment / spectral / Frobenius statistic, the max is an $\ell_\infty$ / extreme statistic, and unit-resolution argmax localization forces super-quadratic cost or the $n^2$ baseline. Barrier-free reconfirmed; the missing property (extreme-sensitive, worst-case, non-linear aggregation) is named |
| Circuit complexity (wall hardened, J1 attacked) | [`circuit_complexity/e_fused_max_mm_attack.py`](circuit_complexity/e_fused_max_mm_attack.py) | Runs to completion, self-checks pass | a first-principles pass (finding 29) HARDENS the bulk-vs-extreme wall into a single-round cheap-measurement lower bound subsuming the four candidates (separable-linear blind by $\ell_2$-lightness + Price-Woodruff; symmetric blind by the Vandermonde degree-$d$ indicator; spectral blind by equal-spectrum collision) and RELOCATES the escape to adaptive / metric methods. Thresholded Max-IP IS bichromatic closest-pair but its engine decays at $d=n^\varepsilon$; the binding sub-obstruction is worst-case GAPLESSNESS |
| Circuit complexity (wall closed vs adaptive, J1) | [`circuit_complexity/e_fused_max_mm_escape.py`](circuit_complexity/e_fused_max_mm_escape.py) | Runs to completion, self-checks pass | the single-round bound EXTENDS to adaptive multi-round bulk decision trees (finding 30): a Set-Disjointness round-elimination argument ($\Omega(n)$ communication, full-block invariance + sub-block SNR-floor) CLOSES the deterministic+adaptive wall; the metric route is conditionally impossible (doubling dimension $\Theta(n^\varepsilon)$ + exactness); the co-nondeterministic escape wall-survives with the $n^2$ in CERTIFICATE SIZE = nonneg rank = DISJ rectangle-cover = $\Omega(n)$. Residual frontier: derandomize the MA batch-OV certificate into a non-algebrizing co-nd one |
| Natural proofs (the TC0-PRF collision) | [`natural_proofs/e_tc0_prf_collision.py`](natural_proofs/e_tc0_prf_collision.py) | Runs to completion | the PRF collision does NOT doom the Williams route (finding 25): it binds the LARGE-and-constructive alternatives, which is why a non-natural method is needed; the spine is non-natural by non-largeness (Williams 2013). Open only at the NEXP-to-NP descent (non-constructivity) |
| Circuit complexity (descent to NP) | [`circuit_complexity/e_leading_path_descent.py`](circuit_complexity/e_leading_path_descent.py) | Runs to completion | reaching NP is a MULTI-JOINT synthesis, not one missing piece (finding 26): J1 algorithmic (grind), J2 descent (downstream of J1; the NP easy-witness lemma is PROVED), J3 non-constructivity (the BINDING joint, the named locality barrier), J4 composition (no combining theorem) |

Strand-3 (the non-algebrizing-invariant search) was also resolved to TWO sharp no-gos
this round: [`strand3/e_bockstein_forcing.py`](strand3/e_bockstein_forcing.py) (finding 21:
the count-forces-torsion bridge is dead, a count forces only the existence of torsion, a
rank fact that algebrizes) and [`strand3/e_symmetry_route.py`](strand3/e_symmetry_route.py)
(finding 22: the Oliver/Smith symmetry route is also a no-go, its certificate is the
rational $\chi(\mathrm{Fix})$, and its output is a query bound). Both run to completion with
real verified homology / group computation.

## AI-centric methodology

The experiments are organized so that an agent loop (see [`OPERATIONS.md`](../OPERATIONS.md))
can extend them. Each experiment is a runnable module with an honest writeup; new
candidate techniques are encoded as `ProofTechnique` objects and run through the
barrier checker before any deeper investment. The discipline is: a technique that
hits a barrier is not pursued unless the writeup explains exactly how it evades
that barrier (as Williams's does).

## Per-architecture next steps

- **Circuit complexity.** The polynomial-method intuition behind Razborov-Smolensky
  is now reproduced in
  [`circuit_complexity/e_acc0_polynomial_method.py`](circuit_complexity/e_acc0_polynomial_method.py)
  (PARITY needs full $\mathbb{F}_3$ degree, and the method is natural hence
  restricted-class only). The
  $\mathsf{TC}^0$-SAT savings hinge is now modeled in
  [`circuit_complexity/e_tc0_sat_savings.py`](circuit_complexity/e_tc0_sat_savings.py):
  it is the single most-leveraged target, since the polynomial method that beat
  $\mathsf{ACC}^0$ dies at threshold gates (MAJORITY has approximate degree
  $\Theta(n)$, Paturi 1992, so no low-degree approximant) and a combinatorial non-algebrizing $\mathsf{TC}^0$-SAT
  speedup would carry $\mathsf{NEXP} \not\subseteq \mathsf{TC}^0$ along the
  Williams spine.
- **Strategic source for 2026 moves.** The speculative 2050 backward-induction
  dossier ([`../docs/03_research/2050_backward_induction.md`](../docs/03_research/2050_backward_induction.md))
  is a compass-calibration exercise (nine imagined resolution paths,
  adversarially stress-tested, then ranked; narrative-level, none Lean-verified).
  Its convergence finding (graft onto the Williams spine rather than replace it)
  and its identification of the $\mathsf{TC}^0$ step as the attackable-now hinge
  motivate the next moves above.
- **Proof complexity.** Add a resolution-width lower-bound experiment for the
  pigeonhole principle (Haken 1985).
- **GCT.** Add a small permanent-vs-determinant orbit-closure / representation-
  multiplicity computation, with the BIP 2016 no-go documented as the boundary.
- **Hardness vs randomness.** Done: the Nisan-Wigderson pseudorandom-generator demo
  ([`hardness_randomness/e_nisan_wigderson_prg.py`](hardness_randomness/e_nisan_wigderson_prg.py))
  builds the polynomial design and shows the PRG property needs a hard $f$ (easy
  parity is distinguishable, nonlinear majority resists).
