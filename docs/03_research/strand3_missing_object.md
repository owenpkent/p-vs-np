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
content that survives is mod-2 torsion as a LOCATED OPERATION (Steenrod squares,
Bockstein images $\beta(x) \ne 0$ on a specific $x$) or a non-abelian
fundamental-group class, which characteristic-0 machinery cannot see. Two caveats the
P3c computation makes load-bearing (LEARNINGS finding 21). First, a torsion COUNT does
NOT survive: the existence-of-torsion rank $\dim_{\mathbb{F}_2} H_n - b_n(\mathbb{Q})$
is positive-characteristic and torsion-sensitive yet is a RANK functional, so it
algebrizes like any rank. Only the located OPERATION (which needs the ring / cochain
structure, not a count) is a candidate. Second, "$\beta$ is non-algebrizing" is a
project judgment (no low-degree field analog), NOT a discharged Aaronson-Wigderson
theorem; the probe marks it candidate-only and the claim is formally open.

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
- **A worked precedent exists where $\mathbb{F}_p$ machinery forces a lower bound,
  but its consumed certificate is a RATIONAL count (corrected by P3c)**
  ([Miller](reading_notes/algebraic_topology/miller_2013_evasiveness_topological_fixed_point.md)).
  Kahn-Saks-Sturtevant: a nonevasive monotone graph property gives a collapsible,
  hence $\mathbb{F}_p$-acyclic, simplicial complex; a vertex-transitive group action
  plus the Lefschetz/Oliver fixed-point theorem then forces a contradiction. Precise
  reading (the original "torsion forces a lower bound" gloss overstated it): the chain
  is nonevasive $\Rightarrow$ collapsible $\Rightarrow$ $\mathbb{F}_p$-ACYCLIC (all
  reduced $\mathbb{F}_p$ homology vanishes, a rank fact) $\Rightarrow$ (symmetry +
  Smith theory + Lefschetz) a forced fixed point $\Rightarrow$ contradiction. There is
  NO located nonzero torsion class anywhere: the complex is acyclic, and the consumed
  certificate is the Euler / Lefschetz number $\chi = 1$, a RATIONAL integer which by
  the [algebrization probe](../../experiments/_shared/algebrization_probe.py)'s own
  logic ALGEBRIZES. $\mathbb{F}_p$ is essential but only as the coefficient field that
  makes Smith theory's operator splitting ($\delta = I - F$, $\sigma = \sum F^i$) valid,
  and it enters as ACYCLICITY (a vanishing rank fact), not as a Bockstein / torsion
  class. So this is an $\mathbb{F}_p$-ACYCLICITY-plus-symmetry obstruction whose
  deciding invariant is rational, NOT a mod-$p$ torsion-class certificate. It is the
  Smith-theory / symmetry route (a fixed-point contradiction), which is the reframed
  strand-3 target, not the count-forces-torsion shape. See LEARNINGS finding 21.
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
2. **The symmetry (REFRAMED by gap-2, 2026-06-03: the symmetry is found, but the
   route is a no-go for strand 3).** The symmetry the evasiveness precedent needs is
   NO LONGER missing: it provably EXISTS and is fully explicit.
   $\mathrm{AGL}(1,q) = \mathbb{F}_q \rtimes \mathbb{F}_q^*$ on $q = p^k$ points has the
   exact Oliver $n_G = 0$ shape (translations are a normal elementary-abelian $p$-group
   of order $q$, the quotient is the cyclic $\mathbb{F}_q^*$ of order $q-1$, and the
   action is 2-transitive so the only nonempty invariant graph is $K_q$), verified for
   $q \in \{4,5,8,9\}$ in [`e_symmetry_route.py`](../../experiments/strand3/e_symmetry_route.py);
   the elementary-abelian Cayley translation core (Tseitin) and the Paley translation
   core carry the same shape. What remains missing for those families is the COMPLEX,
   not the symmetry: there is no canonical acyclic property complex on which the action
   bites (the 3-cube clique complex has $H_1 = \mathbb{Z}^5$, $C_5$ is a circle, and
   nonzero translations are fixed-point-free). But the deeper finding is that even
   granting both the symmetry and an acyclic complex, the Smith-theory / fixed-point
   route FAILS both decisive strand-3 questions. (Q1, algebrization) The certificate the
   Lefschetz/Oliver theorem consumes is $\chi(\mathrm{Fix})$, a rational Euler number, in
   EVERY Oliver-number regime (the trichotomy $\{\chi(X^G) - 1\} = n_G \mathbb{Z}$ pins
   the deciding invariant to the integer $\chi(\mathrm{Fix})$, which is
   coefficient-independent, hence a rank functional a low-degree oracle carries), so it
   ALGEBRIZES, generalizing the $\mathbb{F}_p$-acyclicity no-go from KSS to the whole
   Oliver branch. (Q2, circuit vs query) The output is a decision-tree bound
   $D(h) = \binom{n}{2} = O(n^2)$, a query measure on edge slots, never a circuit-size
   bound, and the query-to-circuit bridge is unsupplied. So gap 2 is recorded as a sharp
   NO-GO coordinate. The structurally OPPOSITE FREE $\mathbb{Z}/2$ Borsuk-Ulam route
   (Babson-Kozlov chromatic 2-torsion) is the one that clears Q1 (located
   non-algebrizing torsion), but it fails Q2 (bounds chromatic number). The deeper root,
   surfaced by the audit: in KSS the complex is acyclic BY CONSTRUCTION (the decision
   tree IS the collapsing schedule), so torsion is never produced and the certificate is
   forced to be rational. An invariant computed downstream of an algorithm (cheap,
   strand 1) cannot carry torsion the algorithm did not put there. See LEARNINGS finding
   22 and [`strand3_ledger.md`](strand3_ledger.md) (the ninth coordinate).
3. **The bridge itself (REFRAMED by P3c, 2026-06-03: the count-forces-torsion shape
   is a no-go).** The bridge was originally phrased as a universal-coefficients or
   Bockstein exact sequence in which a char-0 algorithmic count (an Euler
   characteristic or Lefschetz number, strand 1) FORCES a char-2 torsion class to be
   non-vanishing (strand 3). The [`e_bockstein_forcing.py`](../../experiments/strand3/e_bockstein_forcing.py)
   computation (VERIFIER-checked, ADVERSARY-audited) shows this shape cannot work, and
   the reason is a category distinction the original phrasing conflated. The UCT
   relation $\dim_{\mathbb{F}_2} H_n = b_n(\mathbb{Q}) + t_n(2) + t_{n-1}(2)$ lets a
   cheap count force only the EXISTENCE of torsion: a positive integer $t_n + t_{n-1}$,
   itself a difference of two field ranks of the same integer boundary matrices. That
   existence fact is a RANK functional, so a low-degree extension carries it and it
   ALGEBRIZES. It is NOT a LOCATED non-algebrizing class $\beta(x) \ne 0$. The
   decisive witness is the lens-space pair $L(p^2; q)$ vs $L(p; q)$: same mod-$p$ Betti
   and same torsion-count, yet $\beta = 0$ on the order-$p^2$ side and $\beta \ne 0$ on
   the order-$p$ side (Hatcher 3E.3/3E.4). No count distinguishes them; locating the
   class $x$ with $\beta(x) \ne 0$ needs the cup-square / mod-2 ring structure, not a
   number. So no UCT or Bockstein step forces a located $\beta(x) \ne 0$ from a
   rational count, and the existence-output it does force algebrizes. This is recorded
   as a sharp no-go coordinate, not an open slot. The reframed live target is the
   Smith-theory / symmetry route (gap 2), where a structured group action plus an
   acyclicity fact forces a fixed-point contradiction, with the non-algebrizing
   potential carried by the essential use of $\mathbb{F}_p$ coefficients (Smith theory
   is false over $\mathbb{Q}$), not by a count. See LEARNINGS finding 21 and
   [`strand3_ledger.md`](strand3_ledger.md) (rounds 3, two new coordinates).

## What this enables / what remains open

Enables: a precise shopping list for the strand-3 search and the conceptual
companion to the coordinate ledger (`strand3_ledger.md`, built by the overnight
backlog P3). Each candidate invariant should be checked against the
[algebrization probe](../../experiments/_shared/algebrization_probe.py): rational
trace/rank/volume invariants are dead on arrival, and the P3c sharpening adds that
positive-characteristic RANK invariants (the torsion-existence count, $\mathbb{F}_p$
-acyclicity) are dead too; only torsion-valued OPERATIONS (Sq, $\beta$, $\pi_1$)
survive the first filter, and they fail strand 1 (not cheaply computable). Remains
open and REFRAMED: gap 3 (the bridge) is no longer "find the count-forces-torsion
sequence", which P3c records as a no-go. The reframed open targets are gap 2 (a
prime-power-structured symmetry for the Smith-theory / fixed-point route, the route
the one precedent actually uses) and a located non-algebrizing operation that
certifies a bound directly (the Babson-Kozlov 2007 chromatic torsion obstruction is
the closer precedent than KSS). The honest status is that topology provides the
vocabulary and one precedent for the SYMMETRY route, and a sharp no-go for the
count-forces-torsion route, not a finished construction.
