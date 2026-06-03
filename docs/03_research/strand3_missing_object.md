# The strand-3 missing object: what algebraic topology offers the Bockstein bridge

> A synthesis of the algebraic-topology reading notes toward the one object the
> dossier's braided path is missing. Companion to the
> [2050 dossier](2050_backward_induction.md) (Section 3, the braided path) and to
> the [algebrization probe](../../experiments/_shared/algebrization_probe.py).
> This is a map of what the topology toolkit provides versus what is still missing.
> It is not a construction and it claims nothing about P vs NP.

## The requirement

The dossier's braided path needs one quantity $Q(C, \text{instance})$ that is

- **(strand 1)** nonzero and cheaply certifiable by a faster-than-brute-force
  #SAT-style algorithm on the candidate circuit's gate structure, and
- **(strand 3)** provably NOT reconstructible from any low-degree polynomial
  extension of the oracle (so it does not algebrize).

Every rational trace, rank, or volume invariant proposed for this role algebrizes
(the [algebrization probe](../../experiments/_shared/algebrization_probe.py)
classifies them as such, and finding 9 in
[LEARNINGS](../../experiments/LEARNINGS.md) records why). The only candidate
content that survives is mod-2 torsion (Steenrod squares, Bockstein images) or a
non-abelian fundamental-group class, which characteristic-0 machinery cannot see.

## What the toolkit provides

Synthesized from the [algebraic-topology reading notes](reading_notes/algebraic_topology/).

- **The torsion machinery is exactly the right shape**
  ([Hatcher](reading_notes/algebraic_topology/hatcher_2002_algebraic_topology.md)).
  The universal coefficient theorem (3.1) sends torsion in $H_{n-1}$ into $H^n$,
  and field coefficients (rational homology) erase all torsion, which is why a
  char-0 functional is blind to it. The Bockstein homomorphism $\beta$ (3.E)
  recovers integral torsion from mod-$m$ data, and the first Steenrod square equals
  the mod-2 Bockstein, $Sq^1 = \beta$ (4.L). So the torsion content a rational count
  discards is precisely what the Bockstein and Steenrod operations detect. This is
  the char-0-to-char-2 link the dossier's "Bockstein bridge" names.
- **A worked precedent exists where torsion forces a lower bound**
  ([Miller](reading_notes/algebraic_topology/miller_2013_evasiveness_topological_fixed_point.md)).
  Kahn-Saks-Sturtevant: a nonevasive monotone graph property gives a collapsible,
  hence $\mathbb{F}_p$-acyclic, simplicial complex; a vertex-transitive group action
  plus the Lefschetz/Oliver fixed-point theorem then forces a contradiction. The
  essential ingredient is $\mathbb{F}_p$ (torsion, via Smith theory), NOT rational
  homology. This is a real case of a mod-$p$ torsion obstruction delivering a tight
  complexity lower bound, the template strand 3 wants.
- **A map of which invariants are computable versus torsion-sensitive**
  ([Bjorner](reading_notes/algebraic_topology/bjorner_1995_topological_methods.md)).
  The survey separates the rational, algebrizing-flavored invariants (Euler
  characteristic, $\mathbb{Q}$-Betti numbers, the Mobius function, the
  $\mathbb{Q}$-Lefschetz number) from the torsion-sensitive ones ($\mathbb{Z}/p$
  -acyclicity, Cohen-Macaulayness over $\mathbb{Z}_p$, the $\mathbb{Z}_p$-index),
  with Kahn-Saks-Sturtevant as the documented torsion case. This is the dividing
  line the algebrization probe encodes.

## What is still missing

The literature supplies the tools (Bockstein, Steenrod, Smith theory) and one
template (evasiveness). It does not supply the object. Three concrete gaps:

1. **The explicit complex.** There is no canonical simplicial or cell complex
   attached to $(C, \text{instance})$ whose mod-2 torsion is a hardness certificate.
   The solution-space clustering geometry (the
   [Achlioptas-Coja-Oghlan-Ricci-Tersenghi](reading_notes/stat_physics/achlioptas_cojaoghlan_riccitersenghi_2011_solution_space_geometry.md)
   shattering picture) is the natural candidate substrate, but the complex itself is
   not defined.
2. **The symmetry.** The evasiveness precedent derives its contradiction from a
   vertex-transitive group action. The analogous symmetry for a SAT or circuit
   complex, the one that would make a fixed-point argument bite, is not identified.
3. **The bridge itself.** The dossier's Bockstein bridge requires a
   universal-coefficients or Bockstein exact sequence in which a char-0 algorithmic
   count (an Euler characteristic or Lefschetz number, strand 1) FORCES a char-2
   torsion class to be non-vanishing (strand 3). No such sequence is exhibited for
   any candidate complex. This is the load-bearing missing step.

## What this enables / what remains open

Enables: a precise shopping list for the strand-3 search and the conceptual
companion to the coordinate ledger (`strand3_ledger.md`, built by the overnight
backlog P3). Each candidate invariant should be checked against the
[algebrization probe](../../experiments/_shared/algebrization_probe.py): rational
trace/rank/volume invariants are dead on arrival; only torsion-valued ones survive
the first filter. Remains open: all three gaps above, of which the Bockstein bridge
(gap 3) is the one the dossier itself flags as not existing in 2026. The honest
status is that topology provides the vocabulary and one precedent, not a route.
