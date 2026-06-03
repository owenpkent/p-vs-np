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
| M1 | Reproduce the algorithm-to-lower-bound connection on paper, with the exact time bound that triggers the lower bound | open (study target) |
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
