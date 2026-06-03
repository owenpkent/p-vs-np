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
> coordinates). Relates to LEARNINGS finding 9.

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

## The ledger (rounds 1 and 2, six coordinates)

| Candidate | strand 3 | strand 1 | status | coordinate |
|---|---|---|---|---|
| Euler characteristic $\chi$ of the SAT solution complex | algebrizes | cheap (alternating face count) | DEAD (strand 3) | a cheap rational count is exactly what algebrizes; $\chi$ cannot be the non-algebrizing object. |
| Stiefel-Whitney class $w_i$ of the solution complex | candidate-non-algebrizing | no (needs the mod-2 cohomology ring) | OPEN (strand-1 gap) | a genuine mod-2 torsion class clears strand 3, but no #SAT-style algorithm is known to compute it cheaply. |
| Steenrod-square refinement $Sq^k$ of the mod-2 cohomology | candidate-non-algebrizing | no (acts on cochains) | OPEN (strand-1 gap) | the Steenrod operation is non-algebrizing, but it is not a count; the cochain-level structure is what is missing on strand 1. |
| Fundamental-group class $\pi_1$ of the solution nerve | candidate-non-algebrizing | no (needs the loop structure) | OPEN (strand-1 gap) | a non-abelian class clears strand 3, but it is not a count either; same strand-1 gap as the cohomological candidates. |
| Bockstein image $\beta(x)$ of a mod-2 class | candidate-non-algebrizing | no ($\beta$ alone is not a count) | OPEN (strand-1 gap) | the closest single piece to the bridge: the LIVE object is not $\beta(x)$ alone but a rational count that FORCES $\beta(x) \ne 0$ via a Bockstein sequence. |
| Persistent mod-2 homology barcode (discrete-Morse computable) | algebrizes | cheap (Morse collapse + persistence) | DEAD (strand 3) | the sharpest coordinate: even a cheap, torsion-AWARE computation algebrizes if it outputs ranks/Betti numbers. You need the cohomology OPERATION (Sq, $\beta$), not the ranks. |

LIVE candidates: 0.

## The coordinate this round records

The two strands have not been met by one object. The non-algebrizing candidates
(Stiefel-Whitney, Steenrod) all fail strand 1 because they need ring or cochain
structure, not a count, and the one cheap count tried ($\chi$) algebrizes because it
is a characteristic-0 rational functional. This is exactly the Bockstein-bridge gap
the dossier names: the missing step is a universal-coefficients or Bockstein exact
sequence in which a characteristic-0 algorithmic count (which a #SAT algorithm can
produce, strand 1) FORCES a characteristic-2 torsion class to be non-vanishing
(non-algebrizing, strand 3). Until such a sequence is exhibited for an explicit
solution complex, every candidate sits on one side of the gap.

The narrowing: the search should not look for a new cheap count (those algebrize),
nor for a new torsion class in isolation (those fail strand 1). It should look for
the BRIDGE: a forcing relation between a cheap count and a torsion class on the same
complex. That is the one object worth building.

## Next rounds

The driver [`experiments/strand3/e_ledger.py`](../../experiments/strand3/e_ledger.py)
is the place to add candidates, each encoded as an `InvariantProfile` for the probe
with a strand-1 judgment and a circularity check. The round-2 targets (a $\pi_1$
class, a Bockstein image, a discrete-Morse persistent count) are now logged above,
and they sharpened the gap rather than closing it: every torsion-valued candidate is
OPEN (no cheap count) and every cheap count (including the torsion-aware persistent
barcode) is DEAD (it outputs ranks, which algebrize).

The decisive next object is therefore not another invariant on one side. It is the
FORCING relation itself: a universal-coefficients or Bockstein exact sequence, on an
explicit solution complex, in which a cheap rational count (one a #SAT-style
algorithm can produce) forces a mod-2 torsion class to be non-vanishing. That single
construction would turn a DEAD-or-OPEN row into a LIVE one. It is the dossier's stated
missing tool, and the six coordinates above pin exactly why nothing short of it works.
