# Strand-3 coordinate ledger

> A running ledger of candidate invariants for the dossier's missing object, each
> run through the two strands and recorded as a coordinate. The object must be both
> strand 1 (cheaply computable by a faster-than-brute-force #SAT-style algorithm)
> and strand 3 (provably not reconstructible from a low-degree oracle extension, so
> it does not algebrize). Companion to
> [`strand3_missing_object.md`](strand3_missing_object.md) (the algebraic-topology
> toolkit) and the driver
> [`experiments/strand3/e_ledger.py`](../../experiments/strand3/e_ledger.py), which
> runs the [algebrization probe](../../experiments/_shared/algebrization_probe.py)
> and pins the classifications. A candidate that fails a strand is a SUCCESS recorded
> as a coordinate, not a failure to hide (the project stance: negative results are
> coordinates). Relates to LEARNINGS findings 9 and 21. Round 3 (finding 21) records
> a sharp no-go: the "count forces a located torsion class" bridge cannot supply
> non-algebrizing content, because a cheap count forces only the EXISTENCE of torsion
> (a rank fact that algebrizes), never a located $\beta(x) \ne 0$.

## How a candidate is scored

- **strand 3** (the probe): `algebrizes` if it is a characteristic-0 trace, rank, or
  volume functional (a low-degree oracle extension reconstructs it);
  `candidate-non-algebrizing` if it is a positive-characteristic torsion or
  non-abelian quantity (Steenrod, Bockstein, $\pi_1$) the rational machinery is blind
  to.
- **strand 1**: is it cheaply computable by a faster-than-brute-force #SAT-style
  algorithm on the instance, or does it need ring / cochain structure a count does
  not give?
- **circularity**: does defining or computing it secretly assume a lower bound?
- **status**: DEAD (strand 3) if it algebrizes; OPEN (strand-1 gap) if non-algebrizing
  but not cheaply computable; LIVE if it clears both (the object the dossier says
  does not yet exist).

## The ledger (rounds 1, 2, and 3; eight coordinates)

| Candidate | strand 3 | strand 1 | status | coordinate |
|---|---|---|---|---|
| Euler characteristic $\chi$ of the SAT solution complex | algebrizes | cheap (alternating face count) | DEAD (strand 3) | a cheap rational count is exactly what algebrizes; $\chi$ cannot be the non-algebrizing object. Sharper: $\chi$ is provably coefficient-INDEPENDENT ($\chi$ over $\mathbb{Q}$ equals $\chi$ over $\mathbb{F}_2$), so the UCT torsion terms telescope and cancel in the alternating sum. $\chi$ is the unique count structurally BLIND to torsion, not just an algebrizing near-miss (verified on the $\mathbb{Z} \xrightarrow{2} \mathbb{Z}$ toy, P3c). |
| Stiefel-Whitney class $w_i$ of the solution complex | candidate-non-algebrizing | no (needs the mod-2 cohomology ring) | OPEN (strand-1 gap) | a genuine mod-2 torsion class clears strand 3, but no #SAT-style algorithm is known to compute it cheaply. |
| Steenrod-square refinement $Sq^k$ of the mod-2 cohomology | candidate-non-algebrizing | no (acts on cochains) | OPEN (strand-1 gap) | the Steenrod operation is non-algebrizing, but it is not a count; the cochain-level structure is what is missing on strand 1. |
| Fundamental-group class $\pi_1$ of the solution nerve | candidate-non-algebrizing | no (needs the loop structure) | OPEN (strand-1 gap) | a non-abelian class clears strand 3, but it is not a count either; same strand-1 gap as the cohomological candidates. |
| Bockstein image $\beta(x)$ of a mod-2 class | candidate-non-algebrizing (candidate-only; not a discharged A-W theorem) | no ($\beta$ alone is not a count, and no count FORCES it) | OPEN (strand-1 gap), reframed by P3c | a LOCATED non-algebrizing OPERATION, but NOT count-forced. The P3c no-go (below) shows no cheap count can force $\beta(x) \ne 0$ on a specific $x$: the lens-space pair $L(p^2)$ vs $L(p)$ has equal Betti and equal torsion-count yet $\beta = 0$ on one and $\beta \ne 0$ on the other. Locating $x$ needs the cup-square / ring data, not a number. |
| Persistent mod-2 homology barcode (discrete-Morse computable) | algebrizes | cheap (Morse collapse + persistence) | DEAD (strand 3) | the sharpest cheap-count coordinate: even a cheap, torsion-AWARE computation algebrizes if it outputs ranks/Betti numbers. You need the cohomology OPERATION (Sq, $\beta$), not the ranks. |
| Existence-of-torsion count $\dim_{\mathbb{F}_2} H_n - b_n(\mathbb{Q})$ (the UCT Betti gap) | algebrizes | cheap (two field ranks of the same boundary matrices) | DEAD (strand 3), the decisive new coordinate | NEW (P3c). This is the actual OUTPUT of the UCT forcing $\dim_{\mathbb{F}_2} H_n = b_n(\mathbb{Q}) + t_n(2) + t_{n-1}(2)$. It is torsion-SENSITIVE yet a RANK functional (a difference of two field ranks of the same integer boundary matrices), so a low-degree extension carries it and it ALGEBRIZES. This is the cleanest statement of the no-go: a cheap count forces only the EXISTENCE of torsion, and existence is a rank fact that algebrizes. Verified on RP^2, Klein bottle, the $\mathbb{Z} \xrightarrow{2} \mathbb{Z}$ toy. |
| $\mathbb{F}_p$-acyclicity / Smith-theory rank fact (the KSS/Oliver engine) | algebrizes | cheap in principle (vanishing of field ranks), but the KSS complex is exponential | DEAD (strand 3), third category | NEW (P3c). The one worked precedent (Kahn-Saks-Sturtevant evasiveness) forces via $\mathbb{F}_p$-ACYCLICITY (all reduced $\mathbb{F}_p$ homology vanishes), a positive-characteristic but RANK functional, fed to a Lefschetz/Oliver fixed-point theorem whose consumed certificate is the rational Euler number $\chi = 1$. No located torsion class appears. This is the third category the probe's char-0/char-p binary misses: positive characteristic, torsion-FLAVORED coefficient choice, yet a rank functional, hence still algebrizing. The non-algebrizing load in KSS is carried by SYMMETRY plus acyclicity, not by a count being intrinsically hard. |

LIVE candidates: 0. The two new P3c coordinates make the no-go explicit rather than implicit: the only thing a cheap count forces (existence of torsion) is a rank fact that algebrizes, and the only non-algebrizing object ($\beta(x)$ located) is not count-forced.

## The coordinate this round records (P3c: the bridge is reframed, and the count-forces-torsion shape is a no-go)

Round 3 (the [`e_bockstein_forcing.py`](../../experiments/strand3/e_bockstein_forcing.py)
computation, VERIFIER-checked, ADVERSARY-audited) turns the declarative ledger into
real homology and lands a sharper, honest result: the bridge as originally phrased,
a cheap rational count FORCES a located char-2 torsion class to be non-vanishing, is a
NO-GO. The reason is a category distinction the earlier rounds conflated.

- A cheap count can force only the EXISTENCE of torsion, never a LOCATED class.
  The universal coefficient theorem gives $\dim_{\mathbb{F}_2} H_n =
  b_n(\mathbb{Q}) + t_n(2) + t_{n-1}(2)$, so a mod-2 Betti number exceeding the
  rational Betti number forces $t_n + t_{n-1} \ge 1$, i.e. "some 2-torsion exists."
  But BOTH inputs are ranks (field dimensions of the same integer boundary matrices)
  and the output is the integer $t_n + t_{n-1}$, itself a rank functional. A
  low-degree oracle extension carries the rational chain data, hence every field
  rank, so by Aaronson-Wigderson the existence-of-torsion fact ALGEBRIZES. Forcing
  existence buys nothing for strand 3.
- The LOCATED operation $\beta(x) \ne 0$ on a specific class $x$ is the only
  non-algebrizing candidate, and it is NOT count-forced. The decisive witness is the
  lens-space pair $L(p^2; q)$ vs $L(p; q)$ (at $p = 2$, a $\mathbb{Z}/4$ summand vs a
  $\mathbb{Z}/2$ summand in the same degree): same mod-$p$ Betti, same cheap
  torsion-count, yet $\beta = 0$ on the order-$p^2$ side and $\beta \ne 0$ on the
  order-$p$ side (Hatcher 3E.3/3E.4). No count can distinguish them; the located
  operation can. Identifying which $x$ has $\beta(x) \ne 0$ needs the cup-square /
  mod-2 ring structure, which is not a #SAT-style number.

So the named bridge collapses to two halves, neither LIVE: count-forces-existence
(true but algebrizing) or count-forces-located-$\beta(x)$ (false, the lens-space
no-go). The one worked precedent does not rescue the original shape either: in
Kahn-Saks-Sturtevant evasiveness the consumed certificate is the rational Euler /
Lefschetz number $\chi = 1$, which by the probe's own logic ALGEBRIZES; $\mathbb{F}_p$
enters only as the coefficient field that makes Smith theory's operator splitting
($\delta = I - F$, $\sigma = \sum F^i$) valid, and it enters as ACYCLICITY (a
vanishing rank fact), not as a located torsion class.

The narrowing (the reframed target): do not look for a cheap count forcing a torsion
class. Look instead at the route the precedent actually uses, the Smith-theory /
symmetry route: a structured group action plus an acyclicity/structure fact forcing a
FIXED-POINT contradiction. The non-algebrizing potential there lives in the
$\mathbb{F}_p$-coefficient essentiality (Smith theory is false over $\mathbb{Q}$), and
the genuinely located non-algebrizing operations ($\beta$, $Sq^1$, $\pi_1$) remain
OPEN on strand 1 (not cheaply computable), not refuted. The closer precedent for a
LOCATED torsion class certifying a bound directly (not count-forced) is Babson-Kozlov
chromatic lower bounds, where integral 2-torsion in $H^*(\mathrm{Hom}(C_{2r+1}, K_n);
\mathbb{Z})$ for even $n$ obstructs a coloring; that is the right precedent to study,
and it too lacks a cheap-count forcing (the torsion is the primary, hard-to-compute
object).

## Next rounds

The driver [`experiments/strand3/e_ledger.py`](../../experiments/strand3/e_ledger.py)
is the place to add declarative candidates; the round-3 computation
[`experiments/strand3/e_bockstein_forcing.py`](../../experiments/strand3/e_bockstein_forcing.py)
is the place to add real homology. Rounds 1 and 2 logged the declarative candidates;
round 3 computed real homology on RP^2, the Klein bottle, S^2, the Moebius band, the
$\mathbb{Z} \xrightarrow{2} \mathbb{Z}$ toy, the Lovasz complex $N(K_4)$, and small
SAT Vietoris-Rips complexes (all cross-validated by SNF, VERIFIER-confirmed).

The decisive next object is NO LONGER "the forcing relation count-forces-torsion":
P3c records that as a no-go (a cheap count forces only existence of torsion, a rank
fact that algebrizes; the located $\beta(x)$ is not count-forced, by the lens-space
witness). The reframed live targets, in priority order:

1. Close gap 2 (the symmetry) on the Smith-theory route, not the count route. The
   working precedent forces via a structured transitive group action plus acyclicity,
   producing a fixed-point contradiction. The structural obstruction P3c surfaces: a
   generic SAT/circuit instance lacks the prime-power transitive automorphism Oliver's
   theorem needs (the builder confirmed the literal-flip stabilizer is generically
   trivial). The target is an instance family with a canonical prime-power-structured
   symmetry, or a proof that none exists (itself a coordinate).
2. Find a LOCATED non-algebrizing object that certifies a bound DIRECTLY, the way
   Babson-Kozlov 2007 uses integral 2-torsion in $H^*(\mathrm{Hom}(C_{2r+1}, K_n))$ to
   obstruct a coloring. This is a closer precedent than KSS because the certificate IS
   a torsion class, not an Euler number. The open strand-1 question stays: is it
   cheaply computable? It is not yet, but it is not count-forced either, so it sidesteps
   the P3c no-go.
3. Discharge, or refute, the claim that $\beta$ is non-algebrizing with an actual
   Aaronson-Wigderson model (an oracle and a low-degree extension). The probe marks it
   candidate-only; this is still open, and it is the one piece whose non-algebrization
   would actually be load-bearing if a non-count route ever forced it.

The earlier "build the count-forces-torsion bridge" instruction is retired. The six
prior coordinates plus the two new ones pin why that shape cannot supply
non-algebrizing content.
