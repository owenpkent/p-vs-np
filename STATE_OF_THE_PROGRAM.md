# State of the proof program (repo-wide)

> A one-page strategic snapshot: where every architecture stands, what wall each
> hit, where the live work is, and the single most-leveraged next move. Companion
> to the operational [`PHASE_STATE.md`](PHASE_STATE.md) and the synthesis surface
> [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md). Last updated: 2026-06-03.

## The thesis in one paragraph

The program does not have a proof of P vs NP and is not close to one. What it has
is a **sharp map of where the proof cannot live**, supplied by three published
barrier theorems, and a **precise specification of what a winning technique must
look like**: non-relativizing, non-natural, and non-algebrizing at once. Most of
the candidate architectures are constrained (not refuted) by one or more
barriers. The one technique known to thread all three (Williams's
$\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$, 2011) proves that such techniques
exist; the open problem is to push it from $\mathsf{ACC}^0$ to $\mathsf{P/poly}$
and from $\mathsf{NEXP}$ to $\mathsf{NP}$. The barriers are a compass, not a
verdict.

## The candidate architectures

| Arch | What it is | Status | The wall (what we learned) |
|---|---|---|---|
| **1. Circuit complexity** | prove $\mathsf{NP} \not\subseteq \mathsf{P/poly}$ via circuit lower bounds | **LIVE** | Real bounds against AC0 (parity), monotone (clique), ACC0 (NEXP). The gap to general circuits is gated by the natural-proofs barrier: a P/poly bound needs a non-natural property. |
| **2. Diagonalization** | hierarchy-theorem-style separation | **Constrained** | Relativizes (Baker-Gill-Solovay 1975), so pure diagonalization cannot resolve P vs NP. Reproduced in miniature in `experiments/relativization/`. |
| **3. Proof complexity** | propositional proof-system lower bounds; $\mathsf{NP}$ vs $\mathsf{coNP}$ | **Open / partial** | Strong lower bounds for weak systems (resolution: Haken 1985); the gap to strong systems (Frege, extended Frege) is wide open and ties to $\mathsf{NP}$ vs $\mathsf{coNP}$ (Cook-Reckhow). |
| **4. Geometric Complexity Theory** | permanent vs determinant via representation theory + orbit closures | **Constrained** | Burgisser-Ikenmeyer-Panova 2016 closed the occurrence-obstruction route. Any continuation needs multiplicity obstructions, a strictly harder computation. |
| **5. Hardness vs randomness** | $\mathsf{BPP}$ vs $\mathsf{P}$, PCP, hardness amplification | **Landscape** | Not a direct route to P vs NP, but the structural surroundings: circuit hardness implies derandomization (Nisan-Wigderson, Impagliazzo-Wigderson). |

Each "constrained" is a coordinate: it tells us the proof is not that kind of
argument, so effort concentrates on the live, structural routes (circuit lower
bounds threading all three barriers; proof complexity for strong systems; GCT
multiplicity obstructions).

## The cross-cutting compass

- **The three barriers compose** (LEARNINGS #1). Clearing one or two is not
  enough. Arithmetization is non-relativizing yet still algebrizes.
- **Naturalness is the default** (LEARNINGS #2). Most combinatorial lower-bound
  techniques are natural; non-naturalness is the rare, expensive ingredient a
  P/poly separation needs.
- **The constructivity crux is MCSP** (LEARNINGS #3). For the property a real
  lower bound wants ("circuit size $> s$"), naturalness reduces to the open
  complexity of the Minimum Circuit Size Problem.
- **Average-case is not worst-case** (LEARNINGS #5). The SAT threshold locates
  random hardness, but P vs NP is a worst-case question.
- **The strong stories converge on the Williams spine** (speculative). A
  backward-induction exercise (nine imagined 2050 resolution paths, stress-tested
  against the three barriers, six died and three were wounded) found that four of
  the kills carry the same repair: graft onto the Williams algorithm-to-lower-bound
  spine instead of replacing it, the one component no adversary could disqualify.
  It also gestures at an implied fourth barrier (a technique fails if its hardness
  certificate is reconstructible across a bounded, low-interaction interface), not
  yet correctly axiomatized. Narrative-level only, none of it is Lean-verified. See
  [`docs/03_research/2050_backward_induction.md`](docs/03_research/2050_backward_induction.md).

## The single most-leveraged next move

**Push the Williams template downward.** The one technique that threads all three
barriers combines a circuit-satisfiability algorithm (better than brute force)
with a non-constructive diagonalization. The research frontier is to (a) find
faster satisfiability algorithms for stronger circuit classes, which by the
Williams connection yield new lower bounds, and (b) understand whether the
non-constructive ingredient can be pushed from $\mathsf{NEXP}$ down to
$\mathsf{NP}$. This is where unconditional progress has actually happened since
2011.

The specific hinge is the threshold step of the Williams program, now grounded
against the primary sources (2026-06-03; see
[`docs/03_research/2050_tc0_hinge_grounded.md`](docs/03_research/2050_tc0_hinge_grounded.md)).
The first threshold rung is already climbed: $\mathsf{NQP} \not\subseteq$ ACC-of-THR
with one bottom threshold layer (Murray-Williams 2018), and one extra threshold layer
is done under a restriction ($\mathsf{E}^{\mathsf{NP}}$ not in AC0[m] of LTF of LTF
with a subquadratic bottom THRESHOLD-GATE count, Alman-Chan-Williams 2016). The
genuine open frontier is the SECOND threshold layer once dense: a satisfiability /
CAPP speedup of $2^{n - n^\varepsilon}$ for general depth-2 THR-of-THR (LTF-of-LTF)
with no subquadratic-bottom restriction, which by the Williams connection yields
$\mathsf{NEXP} \not\subseteq$ poly-size THR-of-THR. Crucially, the earlier slogan
"the polynomial method dies at threshold gates because MAJORITY has approximate
degree $\Theta(n)$" was a conflation: the SAT algorithm spends PROBABILISTIC degree
($\Theta(\sqrt{n})$ for MAJORITY), not approximate degree, and that is exactly why it
already crosses one threshold layer. The barrier profile of the open target is
honest-but-weaker than "evades all three": relativization is genuinely evaded,
natural-proofs evasion is CONDITIONAL on whether dense poly-size $\mathsf{TC}^0$
supports PRFs (ACW 2016 warn it likely does, a co-equal open obstruction), and
algebrization is NOT YET ASSESSABLE (a property of a nonexistent algorithm). This
rung is compute-light and attackable now. The runnable model in
[`experiments/circuit_complexity/e_tc0_sat_savings.py`](experiments/circuit_complexity/e_tc0_sat_savings.py)
encodes the corrected picture; the "Boolean-rank-collapse" placeholder is retired in
favor of its real referents (dense LTF-of-LTF SAT, open; sparse case
Impagliazzo-Paturi-Schneider 2013; the Chen 2018 log-shaving geometry reduction).

Honest odds: an unconditional resolution of P vs NP from any current program is
very low. The value of the work is that the barriers are now precise enough to
say what a proof must look like, and the partial results (weak-class lower
bounds, the satisfiability-algorithm / lower-bound connection, arithmetic proof
complexity) are contributions in their own right.

## Recent progress (TC0 hinge grounding, 2026-06-03)

A multi-agent run (4 surveyors over the threshold-circuit-SAT literature, paired
fact-checkers, a builder synthesis, an adversary audit, and a final fact-check
against primary sources) re-grounded the project's single most-leveraged target. It
corrected a load-bearing error, not just added scaffolding. The "polynomial method
dies at threshold gates" slogan conflated worst-case approximate degree (MAJORITY
$\Theta(n)$, Paturi 1992, which blocks only the correlation route) with probabilistic
degree (MAJORITY $\Theta(\sqrt{n})$, Alman-Williams 2015 / Alman-Chan-Williams 2016,
which the SAT algorithm spends and which already crosses one threshold layer). The
first threshold rung is already climbed (Murray-Williams 2018, NQP not in ACC-of-THR,
verified against ECCC TR17-188), so the open frontier is the dense SECOND threshold
layer (general depth-2 THR-of-THR), not "$\mathsf{NEXP} \not\subseteq \mathsf{TC}^0$"
generically. The adversary caught three real defects in the synthesis before they
landed: a paper-title misattribution (the FOCS 2016 ACW paper is "Polynomial
Representations of Threshold Functions", not the FOCS 2015 Hamming-nearest-neighbors
paper), a gates-vs-wires error (the ACW restriction is on bottom-layer GATES), and an
over-strong barrier claim (algebrization is NOT YET ASSESSABLE for a nonexistent
algorithm, and natural-proofs evasion is conditional on the open TC0-PRF question).
New artifact:
[`docs/03_research/2050_tc0_hinge_grounded.md`](docs/03_research/2050_tc0_hinge_grounded.md);
LEARNINGS gains finding 20 and findings 8/11/13 plus the dossier are corrected;
the experiment [`e_tc0_sat_savings.py`](experiments/circuit_complexity/e_tc0_sat_savings.py)
is rewritten and still runs green (smoke test 5/5). Residual needs-citation items are
listed in the note's section 9 for human review.

## Recent progress (overnight run, 2026-06-02)

An autonomous orchestrated loop ran the experimental and documentation backlog to
completion: 13 tasks, each committed separately (per-task log in
[`OVERNIGHT_BACKLOG.md`](OVERNIGHT_BACKLOG.md); cross-architecture findings 11-19 in
[`experiments/LEARNINGS.md`](experiments/LEARNINGS.md)). It produced research
scaffolding and negative-result coordinates, not breakthroughs. The open mathematics
is exactly as open as before.

Concrete additions, all verified (self-checks pass):

- Five new runnable experiments: the Razborov-Smolensky $\mathbb{F}_3$-degree bound,
  pigeonhole resolution width, Kronecker coefficients computed from scratch
  (Murnaghan-Nakayama), Nisan-Wigderson designs, and the monotone-clique sunflower
  lemma.
- The 31 grounded reading notes synthesized into the four research directions and the
  SAT writeup, plus a strand-3 missing-object synthesis and a coordinate ledger
  ([`docs/03_research/strand3_ledger.md`](docs/03_research/strand3_ledger.md)).
- The Lean skeleton now compiles against core Lean: two real bugs were fixed (a
  `Clause.eval` abbreviation-resolution error and a too-narrow `RunsInPolyTime`), with
  the documented `sorry` targets remaining as the open math.

Three findings worth flagging:

- **A propagated error was corrected.** MAJORITY's approximate degree is $\Theta(n)$,
  not $\Theta(\sqrt{n})$ (that is OR / AND); the correction strengthens the
  $\mathsf{TC}^0$-hinge argument. Grounded reading against primary sources is the
  mechanism that caught it (LEARNINGS #11).
- **The strand-3 search has a sharp coordinate.** No candidate invariant clears both
  strands: every cheap count algebrizes, and every torsion class is not a cheap count.
  So the one object worth building is the forcing Bockstein bridge (a cheap count
  forcing a mod-2 torsion class to be nonzero), not another one-sided invariant.
- **Negative results, recorded as coordinates.** The Ben-Sasson-Wigderson width-size
  tradeoff is vacuous for the pigeonhole principle (Haken's bound needs bottleneck
  counting), and the Nisan-Wigderson generator genuinely needs a hard function. Both
  narrow where the real work must live.

## Canonical pointers

- Operational state / next sub-task: [`PHASE_STATE.md`](PHASE_STATE.md)
- Cross-architecture findings: [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md)
- Test plan + per-architecture status: [`experiments/PLAN.md`](experiments/PLAN.md)
- Master research map (all architectures, obstructions): [`docs/research_atlas/README.md`](docs/research_atlas/README.md)
- Operating philosophy: [`docs/researcher_mindset.md`](docs/researcher_mindset.md)
- The research directions: [`docs/03_research/research_directions/`](docs/03_research/research_directions/)
- Speculative 2050 backward-induction (strategy/compass calibration, not proven math): [`docs/03_research/2050_backward_induction.md`](docs/03_research/2050_backward_induction.md)
- Lean skeleton + targets: [`lean/README.md`](lean/README.md)
