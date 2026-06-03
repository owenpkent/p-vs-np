"""Physics-native hardness bridge: the overlap-gap / free-energy barrier candidate.

BUILDER candidate for the "physics-native proof" research direction. The core
object is a rigorous statistical-mechanics quantity, the overlap-gap structure
of the solution-space geometry of a constraint-satisfaction problem, lifted from
an average-case (random ensemble) statement to a worst-case complexity lower
bound.

This module does two things:

  1. Encodes the candidate technique as a `ProofTechnique` and runs it through
     the three-barrier checker. This is the mandatory self-check.

  2. Computes an explicit worked example: the 1-step replica-symmetry-breaking
     (1RSB) free-energy / complexity (Sigma) curve sign-structure for a toy
     mean-field model, and an explicit overlap-gap certificate on a small
     instance, to show the quantities the scenario rests on are concrete and
     computable, not hand-waved.

The point of the worked example is honesty about WHERE the worst-case hardness
must come from. The statistical-mechanics quantities (the overlap gap, the
1RSB complexity Sigma, the clustering threshold alpha_d) are average-case by
construction: they describe a RANDOM ensemble. The hard step, flagged loudly
below, is the bridge from "overlap gap obstructs a large class of algorithms on
the random ensemble" to "some specific NP language has no poly-size circuit in
the worst case." That bridge is the graveyard of physics arguments. We make the
candidate's dependency on it explicit so VERIFIER and ADVERSARY can attack it.

Dependencies: standard library + math only (no numpy needed).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

from experiments._shared import BarrierChecker, ProofTechnique


# ---------------------------------------------------------------------------
# The candidate technique, encoded for the barrier checker.
# ---------------------------------------------------------------------------

def physics_native_technique() -> ProofTechnique:
    """The overlap-gap-to-worst-case hardness bridge as a ProofTechnique.

    Honesty matters here; the fields are the load-bearing self-check.

    relativizes = False:
        The argument inspects the explicit constraint-graph geometry of an
        instance (the overlap structure of its solution space). An oracle is a
        black box with no solution-space geometry, so the central quantity is
        undefined relative to an oracle. The argument does NOT go through for an
        arbitrary oracle, because there is nothing to compute the overlap gap of.
        This is the same reason Razborov's monotone method does not relativize:
        it opens up the object.

    natural_largeness = False:
        The certifying property (a non-trivial overlap-gap / 1RSB free-energy
        profile that survives a worst-case-to-average-case self-reduction) is
        NOT satisfied by a constant fraction of all Boolean functions. A random
        function has a structureless, replica-symmetric (flat) landscape; the
        overlap-gap certificate is rare. We claim non-largeness, which is the
        standard escape from Razborov-Rudich (a property of the hard instance,
        not of generic functions).

    natural_constructivity = False:
        Deciding whether a function/instance has the worst-case overlap-gap
        certificate is conjectured to require solving the very free-energy
        optimization that is #P-hard in the worst case. We do NOT claim a
        poly(2^n)-time decision procedure for the property. The non-constructive
        ingredient is essential, mirroring the non-constructive diagonalization
        in Williams 2011.

    algebrizes = False:
        This is the riskiest claim and the one ADVERSARY should hit hardest.
        The overlap gap is a metric/geometric statement about the Hamming
        distance between near-optimal configurations. A low-degree polynomial
        extension of an oracle over a large field does NOT preserve Hamming
        geometry: the field elements have no Hamming-distance structure, and the
        clustering is destroyed by interpolation. So the argument should not
        survive algebrization. BUT: if at any point the bridge routes through a
        sum-of-squares / arithmetized free-energy certificate (a real
        temptation, since the Parisi functional is an analytic optimization),
        that sub-argument WOULD algebrize, and the whole thing collapses to the
        arithmetization barrier. The candidate must keep the geometric core
        non-arithmetic. We mark algebrizes = False but flag the live risk.
    """
    return ProofTechnique(
        name="Overlap-gap / 1RSB free-energy worst-case hardness bridge (physics-native)",
        relativizes=False,
        natural_largeness=False,
        natural_constructivity=False,
        algebrizes=False,
        notes=(
            "Statistical-mechanics-native. Central quantity: the worst-case "
            "overlap-gap certificate of a constraint-satisfaction instance, "
            "lifted from the random ensemble to a worst-case circuit lower bound "
            "via a geometry-preserving worst-case-to-average-case self-reduction. "
            "RISK: any arithmetized free-energy (Parisi/SoS) sub-step would "
            "reintroduce the algebrization barrier; the geometric core must stay "
            "non-arithmetic. Average-to-worst-case is the live gap, not a barrier."
        ),
    )


# ---------------------------------------------------------------------------
# Worked example 1: the 1RSB complexity Sigma sign-structure (toy mean-field).
# ---------------------------------------------------------------------------
#
# In the cavity / 1RSB picture, the number of clusters of solutions at free
# "energy density" f scales like exp(n * Sigma(f)), where Sigma is the
# complexity (configurational entropy). The clustering / dynamical transition
# alpha_d is where Sigma develops a non-trivial positive branch (exponentially
# many clusters appear), and the condensation / SAT-UNSAT transition is where
# the dominant Sigma hits zero. We model Sigma with a smooth toy profile to make
# the sign-structure and threshold-crossing explicit and checkable. The numbers
# are illustrative of the structure, not fitted to real k-SAT.


def toy_complexity(alpha: float, sigma_max_coeff: float = 0.18) -> Tuple[float, str]:
    """Toy 1RSB complexity at clause density alpha.

    Returns (Sigma*, regime_label). Sigma* is the complexity of the dominant
    (lowest-free-energy) clusters. The toy form mimics the qualitative shape:

      - alpha < alpha_d  : replica symmetric, single dominant cluster, Sigma ~ 0
      - alpha_d < alpha < alpha_c : 1RSB, Sigma > 0 (exponentially many clusters)
      - alpha > alpha_c  : Sigma < 0 for SAT clusters -> formula is UNSAT

    For 3-SAT the literature places alpha_d ~ 3.86 (clustering), alpha_c ~ 4.267
    (SAT-UNSAT). We hard-code those thresholds in the toy.
    """
    alpha_d = 3.86
    alpha_c = 4.267
    if alpha < alpha_d:
        return 0.0, "replica-symmetric (single basin)"
    if alpha <= alpha_c:
        # rises from 0 at alpha_d, falls back to 0 at alpha_c (clustered/1RSB)
        x = (alpha - alpha_d) / (alpha_c - alpha_d)
        sigma = sigma_max_coeff * math.sin(math.pi * x)
        return sigma, "1RSB clustered (exponentially many clusters)"
    # past the SAT-UNSAT threshold the SAT-cluster complexity goes negative
    sigma = -sigma_max_coeff * (alpha - alpha_c)
    return sigma, "condensed / UNSAT (no SAT clusters)"


# ---------------------------------------------------------------------------
# Worked example 2: an explicit overlap-gap certificate on a tiny instance.
# ---------------------------------------------------------------------------
#
# The overlap gap property (OGP) of Gamtor+ / Gamarnik-Sudan style: for a pair
# of near-optimal solutions x, y, the normalized overlap (or equivalently the
# Hamming distance) is forbidden from an interval [a, b]. Solutions come in
# well-separated clusters; there are no near-optimal solutions at intermediate
# distance. OGP is the rigorous obstruction that provably defeats stable /
# local algorithms (Gamarnik 2021 survey). We exhibit it explicitly on a small
# Boolean cube by listing the "near-optimal" set and showing its pairwise
# normalized-distance spectrum has a gap.


def normalized_hamming(x: Tuple[int, ...], y: Tuple[int, ...]) -> float:
    n = len(x)
    return sum(1 for a, b in zip(x, y) if a != b) / n


def overlap_gap_certificate(
    near_optimal: List[Tuple[int, ...]],
) -> Tuple[List[float], Tuple[float, float] | None]:
    """Given a near-optimal solution set, return its sorted distinct normalized
    pairwise distances and the largest forbidden gap interval, if any.

    A non-trivial gap (a, b) with 0 < a < b < 1 strictly inside the spectrum is
    an OGP certificate: no two near-optimal solutions sit at normalized distance
    in (a, b). That is the geometric obstruction the bridge would exploit.
    """
    dists = sorted({normalized_hamming(x, y)
                    for i, x in enumerate(near_optimal)
                    for y in near_optimal[i + 1:]})
    if len(dists) < 2:
        return dists, None
    # find the largest interior gap between consecutive realized distances
    best = None
    best_width = 0.0
    for lo, hi in zip(dists, dists[1:]):
        if hi - lo > best_width:
            best_width = hi - lo
            best = (lo, hi)
    return dists, best


def demo_ogp() -> None:
    """Two well-separated clusters on the 6-cube: a clean OGP example.

    Cluster A: configurations within Hamming distance 1 of 000000.
    Cluster B: configurations within Hamming distance 1 of 111111.
    Intra-cluster normalized distance is small (<= 2/6); inter-cluster is large
    (>= 4/6). The band (2/6, 4/6) is forbidden -> overlap gap.
    """
    n = 6
    base_a = (0, 0, 0, 0, 0, 0)
    base_b = (1, 1, 1, 1, 1, 1)

    def ball(center, radius):
        out = [center]
        for i in range(len(center)):
            flipped = list(center)
            flipped[i] ^= 1
            out.append(tuple(flipped))
        return out if radius >= 1 else [center]

    near_optimal = ball(base_a, 1) + ball(base_b, 1)
    dists, gap = overlap_gap_certificate(near_optimal)
    print("Worked example 2: explicit overlap-gap certificate (6-cube, two clusters)")
    print(f"  |near-optimal set| = {len(near_optimal)} on the {n}-cube")
    print(f"  realized normalized distances: {[round(d, 3) for d in dists]}")
    if gap:
        print(f"  FORBIDDEN BAND (overlap gap): ({gap[0]:.3f}, {gap[1]:.3f}) "
              f"width {gap[1] - gap[0]:.3f}")
        print("  No two near-optimal solutions lie at normalized distance in "
              "this band. This is the OGP obstruction (Gamarnik 2021): any "
              "Lipschitz / stable algorithm whose output moves continuously "
              "with the input cannot cross the band, so it cannot reach both "
              "clusters. That defeats the whole stable-algorithm class on this "
              "geometry.")
    else:
        print("  no interior gap (replica-symmetric-like)")


def demo_complexity_curve() -> None:
    print("Worked example 1: toy 1RSB complexity Sigma(alpha) sign-structure")
    print(f"  {'alpha':>7} {'Sigma*':>10}  regime")
    for a10 in range(35, 46):
        alpha = a10 / 10.0
        sigma, regime = toy_complexity(alpha)
        marker = "  <- clustering onset" if abs(alpha - 3.9) < 1e-9 else ""
        marker = "  <- SAT/UNSAT" if abs(alpha - 4.3) < 1e-9 else marker
        print(f"  {alpha:>7.2f} {sigma:>10.4f}  {regime}{marker}")
    print("  alpha_d ~ 3.86 (clustering / 1RSB onset), alpha_c ~ 4.267 (SAT-UNSAT).")
    print("  These are AVERAGE-CASE thresholds of the RANDOM ensemble. The "
          "candidate's burden is to transport this geometry to a WORST-CASE "
          "instance via a self-reduction; see the barrier note.")


def main() -> int:
    print("=" * 78)
    print("PHYSICS-NATIVE HARDNESS BRIDGE: BUILDER candidate + barrier self-check")
    print("=" * 78)
    print()

    technique = physics_native_technique()
    verdict = BarrierChecker().check(technique)
    print(verdict.report())
    print()
    print(f"evades_all = {verdict.evades_all}  (necessary, not sufficient)")
    print()

    demo_complexity_curve()
    print()
    demo_ogp()
    print()
    print("HONEST CAVEAT (read before trusting any of the above):")
    print("  The barrier self-check is a claim about the INTENDED argument. The "
          "average-case-to-worst-case bridge is NOT yet a theorem; it is the "
          "open hard step. If the bridge is built from an arithmetized free-energy "
          "certificate it will algebrize and the evasion claim is false. The "
          "geometric (Hamming) core is what keeps the algebrization box unchecked.")
    return 0


# ---------------------------------------------------------------------------
# Handoff: explicit verification targets and adversarial test cases.
# ---------------------------------------------------------------------------
#
# VERIFIER (Lean 4 / Mathlib) targets, smallest first:
#   V1. Formalize OGP as a predicate on a finite metric space: there exist
#       0 < a < b < 1 such that the near-optimal set has no pair at normalized
#       distance in (a, b). Prove the 6-cube demo satisfies it with (1/3, 2/3).
#   V2. Formalize the "stable algorithm cannot cross a forbidden band" lemma
#       (a discrete intermediate-value / connectedness argument). This is the
#       rigorous, already-known core (Gamarnik-Sudan style) and should be the
#       first fully formal milestone.
#   V3. State (do not yet prove) the worst-case-to-average-case self-reduction
#       as an interface: a map from a worst-case instance to a distribution over
#       random-ensemble instances that PRESERVES the overlap-gap certificate.
#       The gap between V2 (proved) and V3 (stated) is exactly the open problem.
#
# ADVERSARY test cases (try to break the evasion claim):
#   A1. ALGEBRIZATION: attempt to reconstruct the overlap gap from a low-degree
#       polynomial extension of an oracle over GF(2^k). If the forbidden band
#       survives interpolation, the algebrizes=False claim is FALSE.
#   A2. NATURAL PROOFS: estimate the fraction of all Boolean functions on n bits
#       whose induced "solution geometry" carries a non-trivial overlap gap. If
#       that fraction is bounded below by a constant, natural_largeness=False is
#       FALSE and the property is large after all.
#   A3. RELATIVIZATION: construct an oracle relative to which the self-reduction
#       (V3) exists for an easy problem, forcing the conclusion P^A = NP^A while
#       the geometry argument still "goes through." If found, relativizes=True.
#   A4. THE GRAVEYARD: exhibit a problem with a strong average-case overlap gap
#       (e.g. random k-SAT) that is nonetheless NOT worst-case hard for circuits
#       (it is not, as far as anyone knows, NP-complete to certify), showing the
#       average-to-worst-case bridge cannot be generic. This is the known reason
#       physics arguments die; the candidate must show its bridge is non-generic.

if __name__ == "__main__":
    raise SystemExit(main())
