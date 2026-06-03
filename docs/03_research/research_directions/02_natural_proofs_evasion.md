# Direction 2: evading the natural-proofs barrier

> The MCSP crux. To prove a $\mathsf{P/poly}$ circuit lower bound, the
> lower-bound property must be non-natural. This direction is about constructing
> or recognizing such properties. Companion to the
> [natural_proofs experiment](../../../experiments/natural_proofs/).

## The constraint

Razborov-Rudich: a *useful* property that is both *large* (holds for a constant
or $1/\mathrm{poly}(2^n)$ fraction of functions) and *constructive* (decidable in
$\mathrm{poly}(2^n)$ time) breaks strong pseudorandom generators, which are
believed to exist. So a $\mathsf{P/poly}$ lower bound needs a property that is
either:

- **non-constructive** (cannot be tested in $\mathrm{poly}(2^n)$ time), or
- **non-large** (specific to the target function, true of few functions), while
  remaining useful.

## The MCSP localization

The [experiment](../../../experiments/natural_proofs/) shows that the property a
real lower bound wants, "minimum circuit size $> s$," is large below the Shannon
counting bound and that its constructivity is exactly the Minimum Circuit Size
Problem (MCSP): given a truth table and a size $s$, is there a circuit of size
$\le s$? MCSP's complexity is open. So for this property, naturalness reduces to a
single question: is MCSP easy?

- If MCSP $\in \mathsf{P}$, the property is natural and the barrier bites.
- If MCSP is hard, the property is non-constructive and the barrier is evaded.

Recent work (Hirahara, and Allender-Hirahara) connects MCSP to one-way functions,
average-case complexity, and learning, making MCSP a hub object. Its hardness is
plausible but unproven.

## Milestones

| ID | Milestone | Status |
|---|---|---|
| M1 | Reproduce the largeness measurement for "circuit size $> s$" across small $n$ (extend the experiment to compute exact min circuit size for $n \le 4$) | open |
| M2 | Encode the MCSP-as-constructivity-crux as a `ProofTechnique` and confirm the checker flags the natural vs non-natural branch correctly | partial (the experiment narrates it; encode it) |
| M3 | Survey the MCSP-to-cryptography connections (Hirahara) and map which would, if proved, certify non-naturalness | done (see "Meta-complexity: state of the art" below, from the reading-notes pass) |

## How Williams's technique evades this

Williams's diagonalization against $\mathsf{NEXP}$ does not produce a property of
truth tables at all; it is non-constructive in a strong sense. This is the
existence proof that the non-constructive branch is reachable. Direction 1 and
Direction 2 are two views of the same escape.

## Pointer: the dossier's leading path and the anti-algebrization probe

The speculative [2050 backward-induction dossier](../2050_backward_induction.md)
(a strategy exercise, not proven mathematics) ranks meta-complexity as its leading
path, and it uses meta-complexity as the non-natural device in a sharper form than
the open MCSP question above: a *proved* (not assumed) non-constructivity of "this
truth table has high $Kt$," grafted onto the Williams algorithm-to-lower-bound
spine. Same escape route, with the non-constructivity discharged rather than
conjectured.

The dossier also surfaces a related anti-algebrization question: is a candidate
hardness invariant reconstructible from a low-degree oracle extension? That is now
operationalized in the
[algebrization_probe experiment](../../../experiments/_shared/algebrization_probe.py),
which classifies a proposed invariant as "algebrizes" (characteristic-0
trace/rank/volume functional) or "candidate-non-algebrizing" (mod-2 torsion or
non-abelian, e.g. Steenrod / Bockstein / $\pi_1$). A non-natural property that also
clears this probe is the kind of object the dossier's braided path is missing.

## Meta-complexity: state of the art (from the June 2026 reading pass)

Synthesized from the [reading notes](../reading_notes/) on the meta-complexity
sources. MCSP and time-bounded Kolmogorov complexity have become a hub tying
circuit lower bounds, cryptography, learning, and pseudorandomness together.

- **The natural-proofs hinge is exact.** [Kabanets-Cai 2000](../reading_notes/meta_complexity/kabanets_cai_2000_mcsp.md)
  named MCSP and proved MCSP $\in \mathsf{P/poly}$ implies no strong PRG.
  [Santhanam 2020](../reading_notes/meta_complexity/santhanam_2020_pseudorandomness_mcsp.md)
  sharpened this: a natural property IS a zero-error average-case algorithm for
  MCSP, and MCSP average-case hardness is *equivalent* to succinct pseudorandomness.
  So "evade natural proofs" and "MCSP is average-case hard" are the same statement.
- **Cryptography is now characterized by meta-complexity.**
  [Liu-Pass 2020](../reading_notes/meta_complexity/liu_pass_2020_owf_kolmogorov.md):
  one-way functions exist iff $Kt$ is mildly average-case hard (the first natural
  problem capturing private-key crypto). [Hirahara 2023](../reading_notes/meta_complexity/hirahara_2023_capturing_owf.md):
  assuming $\mathsf{NP} \not\subseteq \text{i.o.}\mathsf{P/poly}$, OWFs exist iff
  approximating distributional $K^{poly}$ is NP-hard, a worst-case characterization.
- **Worst-case to average-case bridges exist within NP.**
  [Hirahara 2018](../reading_notes/meta_complexity/hirahara_2018_w2a_within_np.md)
  gives a non-black-box W2A reduction for approximating $Kt$ (GapMINKT). The
  certificate embeds the solver's own code, which escapes the Bogdanov-Trevisan
  $\mathsf{coNP/poly}$ placement.
- **Restricted MCSP is NP-hard, non-relativizingly.**
  [Hirahara 2022](../reading_notes/meta_complexity/hirahara_2022_learning_partial_mcsp.md)
  proves the first non-relativizing NP-hardness of learning programs (MINLT) and of
  the partial-function variants (MCSP\*, MKTP\*, MINKT\*). [Allender 2020](../reading_notes/meta_complexity/allender_2020_circuit_minimization.md)
  is the map of the whole landscape and the open-problem list.

## The open cruxes meta-complexity still faces

1. **Exact MCSP NP-hardness under deterministic reductions** remains open. The
   foothold is partial: randomized reductions and partial-function variants
   (Hirahara 2022), not yet exact single-output MCSP under deterministic poly-time
   reductions.
2. **Non-black-box does not mean non-relativizing.** This is the load-bearing
   honest catch from the reading pass. Hirahara 2018 states (its Section 1.7) that
   its W2A reduction still *relativizes*. So the meta-complexity device supplies
   the non-naturalness (a proved, not assumed, non-constructivity of high $Kt$),
   but the non-relativizing and non-algebrizing content must come from elsewhere.
   This is exactly the dossier's repair: graft meta-complexity onto the Williams
   spine, which provides the non-relativizing, non-algebrizing diagonalization. The
   W2A local-list-decoding core arithmetizes and cannot be the barrier-clearing
   ingredient on its own.
3. **Closing the loop unconditionally** (removing the cryptographic and i.o.
   hypotheses) is the gap between the current conditional characterizations and an
   unconditional lower bound.

## What this enables / what remains open

Enables: a precise statement of what a $\mathsf{P/poly}$ lower-bound property must
look like, MCSP as the concrete object to study, and (from the reading pass) a map
of which meta-complexity results are non-relativizing versus merely non-black-box.
Remains open: whether exact MCSP is hard, and whether the non-relativizing /
non-algebrizing content can be supplied by the Williams spine as the leading path
proposes. Both are major open problems.
