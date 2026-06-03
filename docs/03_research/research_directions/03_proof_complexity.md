# Direction 3: proof complexity toward NP != coNP

> Prove $\mathsf{NP} \ne \mathsf{coNP}$ (hence $\mathsf{P} \ne \mathsf{NP}$) by
> showing strong propositional proof systems have no short proofs. Companion to
> [`docs/research_atlas/README.md`](../../research_atlas/README.md) Architecture 3.

## The Cook-Reckhow framing

A propositional proof system is a polynomial-time-verifiable way to certify
tautologies. Cook-Reckhow (1979): $\mathsf{NP} = \mathsf{coNP}$ iff some proof
system is *polynomially bounded* (every tautology of size $n$ has a proof of size
$\mathrm{poly}(n)$). To prove $\mathsf{NP} \ne \mathsf{coNP}$ one must show *every*
proof system has tautologies requiring super-polynomial proofs. The program
proceeds system by system, from weak to strong.

## The ladder of systems

| System | Lower bound status |
|---|---|
| Resolution | exponential (Haken 1985, pigeonhole; Chvatal-Szemeredi 1988, random CNF) |
| Polynomial calculus | exponential (Razborov, Impagliazzo-Pudlak-Sgall) |
| Cutting planes | exponential (Pudlak, via interpolation) |
| Bounded-depth Frege | exponential (Ajtai 1994; tied to AC0 switching lemma) |
| Frege | **no super-polynomial lower bound known** |
| Extended Frege | open; tied to circuit lower bounds |

## The obstruction

Feasible interpolation, the technique behind many of the lower bounds above,
provably fails for strong systems under cryptographic assumptions (Bonet-Pitassi-Raz
2000; Krajicek-Pudlak). This is the proof-complexity analog of the natural-proofs
barrier: the soft, generic technique is blocked, so the proof must engage the
specific structure of the strong system.

## State of the art (from the June 2026 reading pass)

Synthesized from the [proof-complexity reading notes](../reading_notes/proof_complexity/).

- [Razborov 1995](../reading_notes/proof_complexity/razborov_1995_unprovability_circuit_lower_bounds.md)
  turns the natural-proofs barrier into a formal unprovability theorem: under a
  strong PRG (hardness $2^{n^\epsilon}$ against circuits), the theory $S_2^2(\alpha)$
  cannot refute "SAT has small circuits" (Corollary 6.5), with an unconditional
  depth-3-with-PARITY case (Theorem 6.1) marking exactly where the cryptographic
  assumption becomes necessary. This is the dossier's A6 independence-from-a-strong-
  arithmetic path in concrete form, and it confirms the A6 caveat that the crypto
  hypothesis is doing the work.
- [Goos-Pitassi-Watson 2017](../reading_notes/proof_complexity/goos_pitassi_watson_2017_lifting_bpp.md)
  is the first BPP-regime query-to-communication lifting theorem: composing any $f$
  with a polynomial-size index gadget makes randomized communication complexity
  equal to randomized decision-tree complexity up to a $\Theta(\log n)$ factor.
  Lifting is the modern engine behind cutting-planes and monotone proof-complexity
  lower bounds.

Cruxes: a super-polynomial Frege lower bound is still open, and the protocol-circuit
duality that lifting exploits is exactly what Bonet-Pitassi-Raz weaponize against
extended Frege. The honest near-term targets are intermediate systems
($\mathsf{AC}^0$-Frege with mod gates) where the duality is not provably blocked,
matching the dossier's A4 repair.

## Milestones

| ID | Milestone | Status |
|---|---|---|
| M1 | Reproduce the resolution-width lower bound for the pigeonhole principle (Haken 1985 via the Ben-Sasson-Wigderson width-size tradeoff) as a runnable experiment | open, scoped in PLAN.md |
| M2 | Connect bounded-depth Frege lower bounds to the AC0 switching lemma already demonstrated in `circuit_complexity/` | open |
| M3 | Survey the Frege lower-bound barrier (feasible interpolation failure) and the bounded-arithmetic connection (Krajicek) | open |

## What this enables / what remains open

Enables: a second, independent route to $\mathsf{P} \ne \mathsf{NP}$ via
$\mathsf{NP} \ne \mathsf{coNP}$, with a concrete first experiment (pigeonhole
resolution width). Remains open: any super-polynomial lower bound for Frege,
which is as hard as the circuit-lower-bound frontier and connected to it.
