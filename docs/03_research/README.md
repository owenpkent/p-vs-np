# Research level: current approaches and the proof program

Prerequisites: graduate complexity theory (see [`docs/02_graduate/`](../02_graduate/)).
This folder holds the research-grade material: the proof program framing, the
numbered research directions with operational specs, and reading notes on the
reference library.

## Orientation

The strategic picture lives in two places you should read first:

- [`docs/research_atlas/README.md`](../research_atlas/README.md): the master map
  of all candidate architectures and their obstructions.
- [`STATE_OF_THE_PROGRAM.md`](../../STATE_OF_THE_PROGRAM.md): the one-page
  snapshot of where each architecture stands and the single most-leveraged next
  move.
- [`2050_backward_induction.md`](2050_backward_induction.md): the forward-looking,
  speculative strategy document. It runs nine imagined 2050 resolution paths,
  stress-tests each against the three barriers, then ranks them. The leading path
  is meta-complexity riding the Williams spine, and the hinge everything routes
  through is the $\mathsf{TC}^0$ step ($\mathsf{NEXP} \not\subseteq \mathsf{TC}^0$).
  Narrative-level compass calibration, not proven mathematics.

## The proof program in brief

The program treats P vs NP as a target. It is organized around the candidate
architectures (circuit complexity, diagonalization, proof complexity, GCT,
hardness-vs-randomness) and disciplined throughout by the three barrier theorems,
which any candidate technique must evade. The operational mechanics (session
loop, agent roles, the barrier-checker gate) are in
[`OPERATIONS.md`](../../OPERATIONS.md).

The current consensus target is the circuit-lower-bound architecture pushed
through the Williams template: the one known technique that threads all three
barriers. The research directions below are concrete sub-programs.

## Research directions

Numbered specs in [`research_directions/`](research_directions/):

1. [`01_circuit_lower_bounds.md`](research_directions/01_circuit_lower_bounds.md):
   pushing the Williams program from $\mathsf{ACC}^0$ toward $\mathsf{P/poly}$.
2. [`02_natural_proofs_evasion.md`](research_directions/02_natural_proofs_evasion.md):
   constructing or recognizing non-natural lower-bound properties (the MCSP crux).
3. [`03_proof_complexity.md`](research_directions/03_proof_complexity.md): strong
   proof-system lower bounds toward $\mathsf{NP} \ne \mathsf{coNP}$.
4. [`04_geometric_complexity_theory.md`](research_directions/04_geometric_complexity_theory.md):
   multiplicity obstructions after the BIP 2016 occurrence no-go.

## Reading list and notes

[`resources_for_the_leading_path.md`](resources_for_the_leading_path.md) is the
prioritized reading guide: what to read, and in what order, to work on the
dossier's leading path (meta-complexity over the Williams spine, the $\mathsf{TC}^0$
hinge, and the cross-disciplinary missing object). The full bibliography is in
[`references/README.md`](../../references/README.md) (sections 08 to 16 cover the
gap areas the dossier surfaced).

[`reading_notes/`](reading_notes/) holds section-by-section notes on the
reference library. The notes map each source to the directions and findings it
informs.
