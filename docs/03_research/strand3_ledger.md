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

## The ledger (round 1)

| Candidate | strand 3 | strand 1 | status | coordinate |
|---|---|---|---|---|
| Euler characteristic $\chi$ of the SAT solution complex | algebrizes | cheap (alternating face count) | DEAD (strand 3) | a cheap rational count is exactly what algebrizes; $\chi$ cannot be the non-algebrizing object. |
| Stiefel-Whitney class $w_i$ of the solution complex | candidate-non-algebrizing | no (needs the mod-2 cohomology ring) | OPEN (strand-1 gap) | a genuine mod-2 torsion class clears strand 3, but no #SAT-style algorithm is known to compute it cheaply. |
| Steenrod-square refinement $Sq^k$ of the mod-2 cohomology | candidate-non-algebrizing | no (acts on cochains) | OPEN (strand-1 gap) | the Steenrod operation is non-algebrizing, but it is not a count; the cochain-level structure is what is missing on strand 1. |

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
is the place to add candidates. Each new candidate should be encoded as an
`InvariantProfile` for the probe, given a strand-1 judgment and a circularity check,
and appended here as a coordinate. Targets worth testing next: a fundamental-group
class $\pi_1$ of the solution nerve, a Bockstein image $\beta(x)$ paired with the
rational count that would force it, and a discrete-Morse / persistent count that is
cheap yet retains torsion after collapse.
