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
| M3 | Survey the MCSP-to-cryptography connections (Hirahara) and map which would, if proved, certify non-naturalness | open |

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

## What this enables / what remains open

Enables: a precise statement of what a $\mathsf{P/poly}$ lower-bound property must
look like, and MCSP as the concrete object to study. Remains open: whether MCSP is
hard, which is itself a major open problem.
