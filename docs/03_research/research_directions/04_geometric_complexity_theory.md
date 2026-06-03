# Direction 4: Geometric Complexity Theory after the occurrence no-go

> Separate permanent from determinant via representation-theoretic obstructions.
> The original occurrence-obstruction plan is closed; multiplicity obstructions
> remain open. Companion to
> [`docs/research_atlas/README.md`](../../research_atlas/README.md) Architecture 4.

## The algebraic version of P vs NP

Valiant (1979) defined algebraic complexity classes $\mathsf{VP}$ (polynomials
with small arithmetic circuits, e.g. the determinant $\det_n$) and $\mathsf{VNP}$
(an algebraic analog of $\mathsf{NP}$, with the permanent $\mathrm{per}_n$ as its
complete problem). $\mathsf{VP} \ne \mathsf{VNP}$ is the algebraic P-vs-NP and is
considered a necessary milestone. Concretely: the determinantal complexity of the
permanent, the smallest $m$ with $\mathrm{per}_n$ a projection of $\det_m$, is
conjectured super-polynomial (best lower bound is quadratic, Mignon-Ressayre
2004).

## The GCT approach (Mulmuley-Sohoni)

Attach to each polynomial its orbit closure under the general linear group. The
coordinate rings of these orbit closures are $\mathrm{GL}$-representations.
Mulmuley-Sohoni proposed separating $\mathrm{per}_n$ from $\det_m$ by finding an
**obstruction**: an irreducible representation that appears in the coordinate ring
of one orbit closure but not the other. This was conjecturally non-natural (it
does not fit the Razborov-Rudich large+constructive template), which is its
appeal.

## The 2016 no-go

Burgisser, Ikenmeyer and Panova (2016) proved that **occurrence obstructions**
(an irreducible occurring in one ring and not the other) cannot prove the
permanent-versus-determinant separation: for the relevant partitions the
multiplicities are nonzero on both sides, so occurrence alone cannot distinguish
them. This closed the original concrete plan ("plan A") of GCT.

## What remains open

- **Multiplicity obstructions**: compare the *multiplicities* (how many times an
  irreducible appears), not just occurrence. This is not ruled out, but it
  requires computing plethysm coefficients and Kronecker coefficients, which are
  themselves hard (Kronecker coefficients are #P-hard to compute in general,
  Ikenmeyer-Mulmuley-Walter).
- Whether GCT can deliver any separation is genuinely open. The partial results
  (advances in symmetric-function and representation-theory computations) are
  valuable independently of P vs NP.
- **Sign coordinate (from the speculative 2050 backward-induction exercise,
  [`../2050_backward_induction.md`](../2050_backward_induction.md)):** that
  narrative-level strategy dossier (not verified mathematics) sharpens the
  reading of BIP 2016. In the padded regime BIP gives multiplicity
  *domination*, $\mathrm{mult}_{\text{perm}} \le \mathrm{mult}_{\text{det}}$,
  which is the opposite sign of what a separation needs, and padding is exactly
  the lever BIP weaponized. So a live GCT route must either avoid padding or use
  a containment-monotone quantity (dimension or codimension) rather than a raw
  multiplicity comparison.

## State of the art (from the June 2026 reading pass)

Synthesized from the [GCT reading notes](../reading_notes/gct_rep_theory/).

- [Burgisser 2015](../reading_notes/gct_rep_theory/burgisser_2015_permanent_determinant_kronecker.md)
  lays out the occurrence-obstruction program (Mulmuley-Sohoni reduce GCT
  coefficients to rectangular Kronecker coefficients) and reports its 2016
  collapse: plethysm positivity forces Kronecker and GCT-coefficient positivity in
  the obstruction-shape regime (Ikenmeyer-Panova; BIP), ruling out the occurrence
  route.
- [Dorfler-Ikenmeyer-Panova 2019](../reading_notes/gct_rep_theory/dorfler_ikenmeyer_panova_2019_multiplicity_obstructions.md)
  is the reason the program is still alive: for the Chow variety versus the higher
  Veronese secant, the partition $\lambda = (n^2-2, n, 2)$ is a multiplicity
  obstruction (multiplicity gap exactly 1) where no occurrence obstruction can
  separate for any $k$. So multiplicity obstructions are provably strictly stronger
  than occurrence obstructions, in a model case.
- [Grochow 2015](../reading_notes/gct_rep_theory/grochow_2015_unifying_lower_bounds_gct.md)
  connects this to strand 3: most classical lower bounds (Nisan-Wigderson partial
  derivatives, Razborov-Smolensky) already build a GCT separating module that is a
  rank, minor, or degree functional, hence algebrizes. The multiplicity obstruction
  is the one quantity in the GCT frame that is NOT the rank of an explicit matrix,
  making it the natural GCT candidate for the dossier's missing non-algebrizing
  invariant (see [`strand3_missing_object.md`](../strand3_missing_object.md)).

This sharpens M2: the live target is a multiplicity comparison, and the model
separation to study is Chow versus Veronese secant (DIP 2019), not padded
perm-versus-det, which is exactly the padding BIP weaponized.

## Milestones

| ID | Milestone | Status |
|---|---|---|
| M1 | Reproduce the Mignon-Ressayre quadratic lower bound on determinantal complexity of the permanent (small $n$, explicit Hessian rank computation) | open, scoped |
| M2 | Compute small plethysm / Kronecker coefficients and check the BIP 2016 multiplicity-nonzero phenomenon on a small partition | done (Kronecker coefficients computed from scratch via Murnaghan-Nakayama in [`gct/e_plethysm_kronecker.py`](../../../experiments/gct/e_plethysm_kronecker.py), verified for $n \le 6$; the DIP 2019 Chow vs Veronese case is the model obstruction to target next) |
| M3 | Encode the occurrence vs multiplicity distinction so the barrier checker treats occurrence obstructions as a closed sub-route and multiplicity obstructions as open | open |

## Barrier status

GCT's appeal is that it is conjecturally non-natural, so it is a candidate route
past Razborov-Rudich. It does not obviously relativize or algebrize (it is an
algebraic-geometry argument, not a black-box or low-degree-oracle one). The
occurrence no-go is an architecture-specific obstruction, not one of the three
general barriers.

## What this enables / what remains open

Enables: a fourth architecture that is plausibly barrier-clean, with concrete
small computations to attempt (M1, M2). Remains open: whether multiplicity
obstructions exist, gated by the hardness of computing the relevant coefficients.
