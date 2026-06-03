# Direction 1: pushing the Williams program toward P/poly

> The live front. The one technique known to thread all three barriers, and the
> concrete steps to extend it. Companion to
> [`docs/research_atlas/README.md`](../../research_atlas/README.md) Architecture 1.

## The template

Williams (2011) proved $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$ by the
algorithm-to-lower-bound connection: a circuit-satisfiability algorithm for a
class $\mathcal{C}$ that beats brute force (runs in time $2^n / n^{\omega(1)}$ on
$\mathcal{C}$-circuits of $n$ inputs) implies $\mathsf{NEXP} \not\subseteq
\mathcal{C}$. He supplied such an algorithm for $\mathsf{ACC}^0$.

This technique evades all three barriers:

- **Non-relativizing**: it uses the structure of $\mathsf{ACC}^0$ circuits, not a
  black-box machine.
- **Non-natural**: the diagonalization against $\mathsf{NEXP}$ is non-constructive
  (it does not yield an efficiently testable property of truth tables).
- **Non-algebrizing**: it does not go through under low-degree oracle extensions.

Run it through the [barrier checker](../../../experiments/_shared/barriers.py)
(`BARRIERS["williams_acc0"]`): it is the entry that evades all three.

## Milestones

| ID | Milestone | Status |
|---|---|---|
| M1 | Reproduce the algorithm-to-lower-bound connection on paper, with the exact time bound that triggers the lower bound | studied (see "State of the art" below; Williams 2015 / 2021 notes) |
| M2 | Encode the $\mathsf{ACC}^0$ SAT algorithm's structure in a small experiment (the polynomial representation of $\mathsf{ACC}^0$ functions, Beigel-Tarui) | open |
| M3 | Extend toward $\mathsf{TC}^0$ (threshold circuits): the open problem is a non-trivial $\mathsf{TC}^0$ satisfiability algorithm | open, frontier |
| M4 | Bring the hard function from $\mathsf{NEXP}$ down to $\mathsf{NP}$ | open, very hard |

The speculative [2050 backward-induction dossier](../2050_backward_induction.md)
(a strategy exercise, not established mathematics) singles out M3 as THE hinge:
the first rung past $\mathsf{ACC}^0$, where the polynomial method that beat
$\mathsf{ACC}^0$ dies because MAJORITY has approximate degree $\Theta(n)$ (Paturi
1992), so a non-algebrizing combinatorial $\mathsf{TC}^0$-satisfiability speedup is
needed instead. This rung is now modeled in the
[`e_tc0_sat_savings`](../../../experiments/circuit_complexity/e_tc0_sat_savings.py)
experiment.

## State of the art (from the June 2026 reading pass)

Synthesized from the [reading notes](../reading_notes/) on the Williams-method and
approximate-degree sources.

**The spine is barrier-clean, and the first step past $\mathsf{ACC}^0$ is taken.**
[Williams 2015](../reading_notes/williams_method/williams_2015_thinking_algorithmically.md)
states the thesis (a sub-$2^n$ Circuit SAT algorithm implies a lower bound).
[Williams 2013](../reading_notes/williams_method/williams_2013_natural_proofs_vs_derandomization.md)
proves NEXP lower bounds are *equivalent* to constructive useful properties, with
a refinement worth pinning: the method is non-natural by dropping *largeness*, not
constructivity (constructivity is unavoidable). [Murray-Williams 2018](../reading_notes/williams_method/murray_williams_2018_easy_witness_nqp.md)
pushes the hard class down to NQP/NP and lands the first rung past $\mathsf{ACC}^0$:
NQP has no quasi-polynomial $\mathsf{ACC}^0$ circuits with one bottom threshold
layer (ACC of THR). [Chen-Lyu-Williams 2020](../reading_notes/williams_method/chen_lyu_williams_2020_ae_lower_bounds.md)
upgrades these to almost-everywhere and average-case, still stopping at ACC0 o THR.
[Williams 2021](../reading_notes/williams_method/williams_2021_lower_bounds_from_algorithm_design.md)
is the status check, and it names a fourth barrier, *locality*, alongside the
canonical three (corroborating the dossier's implied fourth barrier).

**The wall is genuinely the threshold layer, confirmed from two sides.** (a) By
approximate degree: [Paturi 1992](../reading_notes/approx_degree_tc0/paturi_1992_symmetric_approx_degree.md)
gives MAJORITY approximate degree $\Theta(n)$ (no low-degree approximant), while
[Bun-Thaler 2017](../reading_notes/approx_degree_tc0/bun_thaler_2017_ac0_approx_degree.md)
shows $\mathsf{AC}^0$ already reaches approximate degree $n^{1-\delta}$, so
$\mathsf{AC}^0$ is not the wall, the threshold layer is. (b) By the structure of
the certificates: the [Bun-Thaler 2022 survey](../reading_notes/approx_degree_tc0/bun_thaler_2022_approx_degree_survey.md),
the explicit dual witnesses of [Bun-Thaler 2016](../reading_notes/approx_degree_tc0/bun_thaler_2016_dual_polynomials.md),
and the [Sherstov 2011](../reading_notes/approx_degree_tc0/sherstov_2011_pattern_matrix.md)
pattern-matrix lift are all rational, LP/spectral objects that algebrize, so the
approximate-degree method cannot itself be the non-algebrizing ingredient.
[Kumar 2023](../reading_notes/approx_degree_tc0/kumar_2023_ac0_to_tc0_correlation.md)
and [Kane-Williams 2016](../reading_notes/approx_degree_tc0/kane_williams_2016_threshold_lower_bounds.md)
chart how far the random-restriction toolkit reaches up to the wall (a sharp cliff
at gate balance $\approx n^{1/d}$, and depth-2/3 threshold bounds capped by
$\sqrt{n}$ anti-concentration) without crossing it.

**Open cruxes this exposes.** (1) The M3 hinge is a non-trivial $\mathsf{TC}^0$
(THR-of-THR or MAJ-of-MAJ) satisfiability or CAPP algorithm beating brute force;
Chen-Williams (CCC 2019, in the bibliography) already reduces such an algorithm to
a $\mathsf{TC}^0$ lower bound. (2) The speedup must be combinatorial (a Boolean or
sign-rank collapse), not the polynomial method, since the latter's certificates
algebrize. (3) The locality barrier (Williams 2021) must be threaded, which is the
content of LEARNINGS finding 10.

## Why this is the most-leveraged direction

It is the only architecture where unconditional progress has actually happened
since the barriers were established, and it is barrier-clean by construction. The
gap to P vs NP is enormous (from $\mathsf{ACC}^0$ to $\mathsf{P/poly}$, from
$\mathsf{NEXP}$ to $\mathsf{NP}$), but the direction of travel is correct and the
method is not blocked by a known no-go.

## Honest odds

Resolving P vs NP through this program in the near term is very unlikely. Its
value is that every step (a new satisfiability algorithm, a new lower bound) is a
publishable contribution, and the program is the field's best current guess at
what a real proof would extend.

## What this enables / what remains open

Enables: a barrier-clean target for BUILDER agents and a concrete experiment
(M2). Remains open: the $\mathsf{TC}^0$ satisfiability barrier (M3) is the single
sharpest next obstacle.
