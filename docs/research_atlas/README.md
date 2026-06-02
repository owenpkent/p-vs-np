# Research Atlas: the master map of P-vs-NP proof architectures and their obstructions

> The strategic landscape document. Every serious architecture for resolving P
> vs NP, what it would prove, what it has achieved, and the wall (barrier or
> open problem) it meets. Start here for the strategic picture. Companion to
> [`STATE_OF_THE_PROGRAM.md`](../../STATE_OF_THE_PROGRAM.md) and the
> [experiments plan](../../experiments/PLAN.md).

## How to read this atlas

For each architecture we give: the goal (what statement would settle P vs NP),
the state of the art, and the obstruction. The obstructions are mostly the three
barrier theorems (relativization, natural proofs, algebrization) plus
architecture-specific no-go results. The barriers are coordinates, not verdicts:
they tell us what a winning technique must look like.

## Architecture 1: circuit lower bounds

**Goal.** Prove $\mathsf{NP} \not\subseteq \mathsf{P/poly}$ (some NP problem has
no polynomial-size circuits). Since $\mathsf{P} \subseteq \mathsf{P/poly}$, this
implies $\mathsf{P} \ne \mathsf{NP}$.

**State of the art.** Unconditional lower bounds against restricted classes:

| Class | Lower bound | Technique |
|---|---|---|
| $\mathsf{AC}^0$ | PARITY needs size $2^{\Omega(n^{1/(d-1)})}$ | switching lemma (Hastad 1986) |
| $\mathsf{AC}^0[p]$, $p$ prime | $\mathrm{MOD}_q$, MAJORITY exponential | polynomial method (Razborov 1987, Smolensky 1987) |
| monotone | CLIQUE exponential | method of approximations (Razborov 1985) |
| $\mathsf{ACC}^0$ | $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$ | SAT algorithm + diagonalization (Williams 2011) |

**Obstruction.** The natural-proofs barrier. The switching-lemma and
approximation methods are *natural* (large + constructive); they work only
because their target classes (AC0, monotone) do not contain pseudorandom
generators. Against $\mathsf{P/poly}$, which does contain cryptography, a natural
property cannot prove a lower bound (Razborov-Rudich 1994). A P/poly separation
needs a non-natural property. See [natural_proofs experiment](../../experiments/natural_proofs/).

**Where the live work is.** The Williams program: better circuit-satisfiability
algorithms yield new lower bounds via the algorithm-to-lower-bound connection.
This is non-natural (non-constructive diagonalization), non-relativizing, and
non-algebrizing. Pushing it from $\mathsf{ACC}^0$ to $\mathsf{TC}^0$ /
$\mathsf{NC}^1$ / $\mathsf{P/poly}$ and from $\mathsf{NEXP}$ to $\mathsf{NP}$ is
the open frontier.

## Architecture 2: diagonalization and hierarchy theorems

**Goal.** Separate $\mathsf{P}$ from $\mathsf{NP}$ by a diagonalization argument,
as the time/space hierarchy theorems separate $\mathsf{P}$ from $\mathsf{EXP}$.

**State of the art.** Hierarchy theorems are proved and tight. Diagonalization is
the backbone of computability and of the hierarchy separations.

**Obstruction.** The relativization barrier (Baker-Gill-Solovay 1975).
Diagonalization relativizes, and there are oracles forcing P vs NP both ways, so
pure diagonalization cannot resolve it. See
[relativization experiment](../../experiments/relativization/).

**Where the live work is.** Non-relativizing diagonalization, as in the Williams
program (Architecture 1). Diagonalization is not dead; it is one ingredient that
must be combined with a non-relativizing component.

## Architecture 3: proof complexity

**Goal.** Prove $\mathsf{NP} \ne \mathsf{coNP}$ (which would imply
$\mathsf{P} \ne \mathsf{NP}$) by showing some propositional proof system has no
polynomial-size proofs of all tautologies. By Cook-Reckhow (1979),
$\mathsf{NP} = \mathsf{coNP}$ iff there is a proof system in which every tautology
has a polynomial-size proof. Proving super-polynomial lower bounds for *every*
proof system would give $\mathsf{NP} \ne \mathsf{coNP}$.

**State of the art.** Strong lower bounds for weak systems:

- Resolution: exponential lower bounds for the pigeonhole principle (Haken 1985)
  and random CNFs (Chvatal-Szemeredi 1988).
- Bounded-depth Frege: exponential lower bounds (Ajtai 1994; Pitassi-Beame-Impagliazzo;
  Krajicek-Pudlak-Woods), closely tied to the AC0 switching lemma.

**Obstruction.** The gap to *strong* systems (Frege, extended Frege, Frege with
counting axioms) is wide open. No super-polynomial lower bound is known for Frege.
The feasible-interpolation technique that powers many proof-complexity lower
bounds is itself blocked for strong systems (under cryptographic assumptions,
Krajicek-Pudlak; Bonet-Pitassi-Raz 2000), an analog of the natural-proofs
barrier inside proof complexity.

**Where the live work is.** Lower bounds for intermediate systems (cutting
planes, polynomial calculus, Sum-of-Squares), and the deep connection between
proof complexity, circuit complexity, and bounded arithmetic.

## Architecture 4: Geometric Complexity Theory (GCT)

**Goal.** Separate the permanent from the determinant (an algebraic analog of
$\mathsf{VNP} \ne \mathsf{VP}$, the Valiant 1979 algebraic version of P vs NP) by
showing the orbit closure of the permanent is not contained in that of a
polynomial-size determinant. Mulmuley and Sohoni proposed detecting this via
*representation-theoretic obstructions*: irreducible representations appearing in
the coordinate ring of one orbit closure but not the other.

**State of the art.** A rich program connecting complexity to algebraic geometry
and representation theory (plethysm coefficients, Kronecker coefficients). It is
conjecturally non-natural, which is its main appeal as a route past
Razborov-Rudich.

**Obstruction.** Burgisser, Ikenmeyer and Panova (2016) proved that *occurrence
obstructions* (the original GCT plan, where an irreducible appears in one ring
and not the other) cannot prove the permanent-vs-determinant separation: the
relevant multiplicities are nonzero on both sides. This closed plan A.

**Where the live work is.** *Multiplicity obstructions* (comparing the
multiplicities, not just occurrence) remain open but require strictly harder
representation-theoretic computations. Whether GCT can deliver a separation is
genuinely open; the partial results (advances in computing plethysm and
Kronecker coefficients) are valuable independently.

## Architecture 5: hardness versus randomness (the surrounding landscape)

**Goal.** Not a direct route to P vs NP, but the structural surroundings that
constrain and inform it.

**State of the art.**
- $\mathsf{BPP} \subseteq \mathsf{P/poly}$ (Adleman); circuit lower bounds imply
  derandomization (Nisan-Wigderson 1994; Impagliazzo-Wigderson 1997: if $\mathsf{E}$
  needs exponential circuits then $\mathsf{BPP} = \mathsf{P}$).
- The PCP theorem (Arora-Safra; Arora-Lund-Motwani-Sudan-Szegedy 1998) recharacterizes
  $\mathsf{NP}$ via probabilistically checkable proofs and underpins hardness of
  approximation.
- Kabanets-Impagliazzo (2004): derandomizing polynomial identity testing implies
  circuit lower bounds, linking the two programs.

**Obstruction / role.** This architecture mostly tells us that the programs are
entangled: progress on lower bounds and on derandomization are two sides of one
coin. It does not by itself separate P from NP.

## The cross-cutting picture

Every architecture either runs into a barrier (relativization for
diagonalization; natural proofs for combinatorial circuit lower bounds;
feasible-interpolation blockage for strong proof systems; the occurrence-obstruction
no-go for GCT) or is open at exactly the structural step the barriers say it must
be. The barriers are not five separate dead ends; they are one statement seen
from several angles: a winning technique must engage the exact structure of an
NP-complete problem in a way that is non-relativizing, non-natural, and
non-algebrizing. That is the compass. See
[`docs/researcher_mindset.md`](../researcher_mindset.md).

## Pointers

- Per-architecture experiments: [`experiments/PLAN.md`](../../experiments/PLAN.md)
- Cross-architecture findings: [`experiments/LEARNINGS.md`](../../experiments/LEARNINGS.md)
- Known approaches and why each is stuck: [`docs/solutions/`](../solutions/)
- Research directions with operational specs: [`docs/03_research/research_directions/`](../03_research/research_directions/)
