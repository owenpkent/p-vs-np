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

## AI-centric methodology

The experiments are organized so that an agent loop (see [`OPERATIONS.md`](../OPERATIONS.md))
can extend them. Each experiment is a runnable module with an honest writeup; new
candidate techniques are encoded as `ProofTechnique` objects and run through the
barrier checker before any deeper investment. The discipline is: a technique that
hits a barrier is not pursued unless the writeup explains exactly how it evades
that barrier (as Williams's does).

## Per-architecture next steps

- **Circuit complexity.** Extend the restriction demo to ACC0 (mod gates) and
  reproduce the polynomial-method intuition behind Razborov-Smolensky.
- **Proof complexity.** Add a resolution-width lower-bound experiment for the
  pigeonhole principle (Haken 1985).
- **GCT.** Add a small permanent-vs-determinant orbit-closure / representation-
  multiplicity computation, with the BIP 2016 no-go documented as the boundary.
- **Hardness vs randomness.** Add a Nisan-Wigderson pseudorandom-generator demo
  connecting circuit hardness to derandomization.
