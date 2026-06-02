# State of the proof program (repo-wide)

> A one-page strategic snapshot: where every architecture stands, what wall each
> hit, where the live work is, and the single most-leveraged next move. Companion
> to the operational [`PHASE_STATE.md`](PHASE_STATE.md) and the synthesis surface
> [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md). Last updated: 2026-06-02.

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

## The single most-leveraged next move

**Push the Williams template downward.** The one technique that threads all three
barriers combines a circuit-satisfiability algorithm (better than brute force)
with a non-constructive diagonalization. The research frontier is to (a) find
faster satisfiability algorithms for stronger circuit classes, which by the
Williams connection yield new lower bounds, and (b) understand whether the
non-constructive ingredient can be pushed from $\mathsf{NEXP}$ down to
$\mathsf{NP}$. This is where unconditional progress has actually happened since
2011.

Honest odds: an unconditional resolution of P vs NP from any current program is
very low. The value of the work is that the barriers are now precise enough to
say what a proof must look like, and the partial results (weak-class lower
bounds, the satisfiability-algorithm / lower-bound connection, arithmetic proof
complexity) are contributions in their own right.

## Canonical pointers

- Operational state / next sub-task: [`PHASE_STATE.md`](PHASE_STATE.md)
- Cross-architecture findings: [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md)
- Test plan + per-architecture status: [`experiments/PLAN.md`](experiments/PLAN.md)
- Master research map (all architectures, obstructions): [`docs/research_atlas/README.md`](docs/research_atlas/README.md)
- Operating philosophy: [`docs/researcher_mindset.md`](docs/researcher_mindset.md)
- The research directions: [`docs/03_research/research_directions/`](docs/03_research/research_directions/)
- Lean skeleton + targets: [`lean/README.md`](lean/README.md)
