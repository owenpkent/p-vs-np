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
For the existing results this is non-relativizing, non-natural, and non-algebrizing.
The threshold frontier is now located precisely (see
[`../03_research/2050_tc0_hinge_grounded.md`](../03_research/2050_tc0_hinge_grounded.md)):
the first threshold rung is already climbed ($\mathsf{NQP} \not\subseteq$ ACC-of-THR,
Murray-Williams 2018), and the open object is a satisfiability speedup for DENSE
depth-2 THR-of-THR, not "$\mathsf{TC}^0$" in the abstract. A caution, corrected in
June 2026 (LEARNINGS finding 25, after an over-pessimistic earlier phrasing): at dense
poly-size $\mathsf{TC}^0$ the PRF collision (likely PRFs in $\mathsf{TC}^0$: ACW 2016;
Naor-Reingold JACM 2004; Miles-Viola candidate JACM 2015; Chen-Tell 2019) rules out any
LARGE-and-constructive (combinatorial / correlation / approximate-degree) lower-bound
property. That binds the natural ALTERNATIVES, and it is precisely WHY a non-natural
method is required, not an obstruction to the Williams route: Razborov-Rudich needs
large AND constructive, and the Williams spine is non-natural by dropping LARGENESS, not
constructivity (Williams 2013: constructivity is unavoidable, the useful property is
non-large), so a genuinely non-large Williams-style proof does NOT collide with the PRF.
Natural proofs on the leading path: CONDITIONALLY EVADED via non-largeness at the
NEXP-level bound. The genuine open obstructions are the ALGORITHMIC one (the dense
THR-of-THR SAT / Max-IP log-shave, findings 20/23/24, sharpened to the fused-max-MM,
BUILT as four candidate fusions sharing one bulk-vs-extreme wall, then that wall HARDENED into a
single-round cheap-measurement lower bound, then CLOSED against deterministic + adaptive bulk and
metric methods, leaving a co-nondeterministic certificate as the last opening, blocked by a
triple-lock (UPIT/NSETH, algebrization, prAM-circularity), NOT the Set-Disjointness SDPT (Chen's
reduction is single-instance); the seam closes for the full-block case via a sufficient-statistic
collapse with the sub-block a named open lemma, findings 27/28/29/30/31/32), the
not-yet-assessable
algebrization flag, and the $\mathsf{NEXP}$-to-$\mathsf{NP}$ descent, where the escape
mechanism must flip from non-largeness to NON-CONSTRUCTIVITY (the meta-complexity
high-Kt device, which is large) and that non-constructivity against $\mathsf{TC}^0$ is
open. Pushing on to $\mathsf{NC}^1$ / $\mathsf{P/poly}$ and to $\mathsf{NP}$ remains the
longer-range frontier.

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
[`docs/researcher_mindset.md`](../researcher_mindset.md). A speculative
backward-induction exercise (the [2050 dossier](../03_research/2050_backward_induction.md))
ranks resolution paths and finds the strongest converge on the Williams spine
(Architecture 1), with the missing object specified as a non-algebrizing
invariant a fast algorithm can compute (the strand-1-vs-strand-3 target). The
"Bockstein bridge" sub-target (a cheap rational count forcing a located char-2
torsion class) is now a NO-GO COORDINATE (LEARNINGS finding 21, 2026-06-03): a
cheap count forces only the EXISTENCE of torsion, a rank fact that algebrizes,
never a located $\beta(x) \ne 0$. The reframed live route is the Smith-theory /
symmetry fixed-point route, not a count.

## Pointers

- Per-architecture experiments: [`experiments/PLAN.md`](../../experiments/PLAN.md)
- Cross-architecture findings: [`experiments/LEARNINGS.md`](../../experiments/LEARNINGS.md)
- Known approaches and why each is stuck: [`docs/solutions/`](../solutions/)
- Research directions with operational specs: [`docs/03_research/research_directions/`](../03_research/research_directions/)
- Speculative strategy exercise: [2050 backward-induction dossier](../03_research/2050_backward_induction.md) ranks nine imagined resolution paths against the three barriers (narrative-level, none Lean-verified) and names the late-2030s $\mathsf{TC}^0$ hinge of the Williams program as the milestone everything routes through. Companion experiments: [`e_tc0_sat_savings.py`](../../experiments/circuit_complexity/e_tc0_sat_savings.py) models the $\mathsf{TC}^0$ hinge and the savings-mirage coordinate; [`algebrization_probe.py`](../../experiments/_shared/algebrization_probe.py) classifies a proposed hardness invariant as algebrizing or candidate-non-algebrizing.
