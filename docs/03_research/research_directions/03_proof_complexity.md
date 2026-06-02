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
