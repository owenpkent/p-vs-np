"""The TC0 hinge: a satisfiability-savings model for the Williams program's
threshold rungs.

The 2050 backward-induction dossier (docs/03_research/2050_backward_induction.md)
identifies a single load-bearing milestone on the leading path to
P != NP: the step where the algorithm-to-lower-bound connection (Williams 2011)
climbs through the threshold-circuit (TC0) ladder. Every surviving P != NP
scenario routes through that connection. The corrected picture, grounded against
the primary sources, is NOT "the polynomial method dies at threshold gates."

What is actually true (corrected 2026-06-03 from the survey/fact-check pass):

  - The ladder has more than one rung and the FIRST threshold rung is already
    climbed. ACC0 with a SINGLE bottom layer of linear threshold gates
    (ACC of THR) is done: Williams 2014 ("New algorithms and lower bounds for
    circuits with linear threshold gates", STOC 2014 / Theory of Computing 14:17
    2018) gives the ACC-of-THR SAT/evaluation algorithm, and Murray-Williams 2018
    ("An Easy Witness Lemma for NP and NQP", STOC 2018) feeds it through a new
    easy-witness lemma to get NQP not in n^(log^k n)-size ACC of THR, upgraded to
    average-case (Chen, FOCS 2019) and almost-everywhere (Chen-Lyu-Williams,
    ~FOCS 2020; exact venue/year to be confirmed).

  - The polynomial method does NOT die at threshold gates. It uses PROBABILISTIC
    degree, not worst-case approximate degree. MAJORITY's probabilistic degree to
    error eps is Theta(sqrt(n log(1/eps))) (Alman-Williams FOCS 2015;
    Alman-Chan-Williams FOCS 2016 Thm 1.1), tight against Razborov-Smolensky 1987,
    which is FAR below its worst-case approximate degree Theta(n) (Paturi 1992).
    Built directly from these probabilistic polynomials, ACW 2016 (Thm 1.8) give a
    deterministic 2^{n - n^eps} SAT algorithm for AC0[m] of LTF of LTF with a
    subquadratic number of bottom-layer linear threshold GATES (n^{2-eps} GATES,
    not wires), climbing one EXTRA threshold layer, and via the Williams connection
    (Cor 1.1) prove E^NP not in that class.

  - The real wall is a DENSITY / DEPTH / ERROR budget, not a flat impossibility.
    Each threshold layer costs ~sqrt(n) probabilistic degree; the ACW construction
    needs a subquadratic bottom threshold-GATE count and bounded threshold depth;
    pushing error below 2^{-n} (to union-bound over all inputs) inflates the
    per-layer degree by log(1/eps). The method stalls when threshold layers become
    both dense and deep. (A separate n^{2-o(1)}-WIRE bound for THR-of-THR exists,
    Chen-Tamaki / ACW; do not conflate that wire bound with the ACW gate bound.) Separately, ACW 2016 warn (after Thm 1.9) that their most powerful
    threshold class "seems likely" to support pseudorandom function candidates, so
    a natural-proofs collision looms exactly where the method would reach dense
    poly-size TC0. The worst-case approximate-degree Theta(n) fact is a real but
    SECOND, independent reason the Razborov-Smolensky low-degree-APPROXIMATION
    (correlation) route is blocked; it is not the resource the SAT algorithm spends.

This module pins the hinge as a runnable, checkable object. It does two things.

  1. Barrier audit of two candidate routes to a deeper threshold-SAT speedup:
       - the naive "prove TC0 lower bounds by low-degree (worst-case)
         approximability" route, caught by the natural-proofs barrier (large +
         constructive). Note this is the correlation/approximate-degree route, NOT
         the probabilistic-polynomial SAT algorithm, which is already non-natural
         the way Williams's ACC0 argument is.
       - the candidate combinatorial speedup for DENSE / DEEP threshold circuits
         (the open frontier object), fed through the Williams template, which (if
         it exists) threads all three barriers as Williams's ACC0 argument does.
         Its `algebrizes=False` is the load-bearing claim.

  2. A savings-reality-check: a savings factor 2^{n^eps} for tiny eps is
     asymptotically "superpolynomial" yet a mirage at feasible scale, while a
     genuinely strong savings (2^{n / polylog n}, the form the ACC and ACW
     algorithms actually achieve, 2^{n - n^eps}) dominates a polynomial bar at
     human scale. Williams 2010 ("Improving Exhaustive Search", STOC 2010 /
     SICOMP 2013) Thm 1.1: ANY superpolynomial savings over the 2^n*poly
     truth-table cost yields NEXP not in P/poly; Thm 1.2: 2^{(1-delta)n} savings
     buys the stronger exponential-size E^NP bound.

Run:
    python -m experiments.circuit_complexity.e_tc0_sat_savings
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from experiments._shared import BarrierChecker, BARRIERS, ProofTechnique


# --------------------------------------------------------------------------
# Part 1: barrier audit of two routes to a TC0-SAT speedup.
# --------------------------------------------------------------------------

# The naive route: prove TC0 lower bounds by WORST-CASE low-degree approximability
# (the correlation / approximate-degree route, the analog of how a generic
# function is certified hard). It is a natural proof (large + constructive: the
# certifying property holds for a constant fraction of functions and is
# poly(2^n)-testable). It does not relativize (it opens the circuit) and it is the
# arithmetizing object, so it algebrizes. The approximate-degree obstruction
# (MAJORITY needs Theta(n), Paturi 1992) blocks THIS route's correlation bounds.
#
# IMPORTANT correction (2026-06-03): this technique is NOT the probabilistic
# polynomial-method SAT algorithm. That algorithm spends PROBABILISTIC degree,
# where MAJORITY is only Theta(sqrt(n log(1/eps))) (Alman-Williams 2015; ACW 2016
# Thm 1.1), and it DOES cross one threshold layer (ACW 2016 Thm 1.8, a 2^{n-n^eps}
# SAT algorithm for AC0[m] of LTF of LTF with a subquadratic n^{2-eps} bottom
# threshold-GATE count). So the "polynomial method cannot represent even one
# threshold gate" framing was wrong; it conflated worst-case approximate degree
# with the probabilistic degree the algorithm actually uses.
tc0_approx_degree_route = ProofTechnique(
    name="TC0 lower bounds via worst-case low-degree approximation (correlation / approximate-degree route)",
    relativizes=False,
    natural_largeness=True,
    natural_constructivity=True,
    algebrizes=True,
    notes=(
        "Natural (large + constructive): that is the PRIMARY, citable disqualifier "
        "(Razborov-Rudich). The further flag algebrizes=True (the dual-polynomial / "
        "pattern-matrix objects being rational LP/spectral functionals) is PROJECT "
        "INFERENCE, not a cited Aaronson-Wigderson theorem; treat it as a modeling "
        "choice, not an established fact. The approximate-degree obstruction (MAJORITY "
        "worst-case approximate degree Theta(n), Paturi 1992; OR/AND only "
        "Theta(sqrt n)) blocks this correlation route specifically. It is NOT the "
        "probabilistic-polynomial SAT algorithm, which spends probabilistic degree "
        "Theta(sqrt n) and crosses one threshold layer (ACW 2016)."
    ),
)

# The candidate winning route: a faster-than-brute-force satisfiability / CAPP
# algorithm for DENSE, DEEPER threshold circuits (the open frontier object, past
# the one-threshold-layer ACW 2016 result), fed through the Williams connection.
# If such an algorithm exists, the resulting lower bound would need the same
# three-barrier profile as Williams's ACC0 proof: non-relativizing (a real
# circuit-SAT speedup must read the gate structure), non-natural (the
# diagonalization drops largeness, function-specific, per Williams 2013), and
# non-algebrizing.
#
# HONESTY NOTE (2026-06-03, from the adversary audit): do NOT equate "combinatorial"
# with "non-algebrizing". ACW 2016's probabilistic-polynomial method is ALGEBRAIC,
# and it already crossed one threshold layer and fired the connection, so "algebraic
# method" and "algebrizes (survives the Aaronson-Wigderson algebraic-oracle game)"
# are different axes. algebrizes=False here is therefore NOT YET ASSESSABLE: it is a
# property of a nonexistent algorithm whose mechanism is undetermined, and no cited
# source establishes it. The flag encodes the NECESSARY target condition (the same
# profile Williams's proof has), not a cleared barrier.
#
# NAMING NOTE (2026-06-03): the earlier working name "Boolean-rank collapse" is a
# project coinage with no published theorem behind it. The honest status: the
# real, citable frontier objects in this neighborhood are (a) a SAT/CAPP speedup
# for dense depth-2 LTF-of-LTF (no nontrivial algorithm is known for the dense
# case; ACW 2016 needs a subquadratic n^{2-eps} bottom threshold-GATE count; the
# sparse cn-wire case is solved by Impagliazzo-Paturi-Schneider FOCS 2013 via
# Vector Domination); equivalently
# (b) "shaving all polylog factors" off a polylog-dimension geometric problem
# (ell_2-Furthest-Pair / Bichromatic-Closest-Pair / Max-IP) per Chen 2018
# (arXiv:1805.10698) Thm 1.1, which would give NEXP not in poly-size THR of THR.
# Sign-rank / dimension complexity is a real object class but provably CANNOT
# crack THR-of-THR alone (a linear-size THR-of-THR circuit can have exponential
# sign-rank), so the hoped-for object must go beyond sign-rank. We keep
# algebrizes=False as the necessary condition, with the object now named by its
# real referents rather than the placeholder.
threshold_sat_combinatorial = ProofTechnique(
    name="Dense/deep-threshold SAT or CAPP via a combinatorial speedup (Williams template)",
    relativizes=False,
    natural_largeness=False,
    natural_constructivity=False,
    algebrizes=False,
    notes=(
        "The honest target for the hinge: a nontrivial SAT/CAPP algorithm for dense "
        "depth-2 LTF-of-LTF (or deeper TC0), beating brute force by 2^{n^eps}, fed "
        "through the Williams connection. Real citable forms: a dense depth-2 "
        "threshold SAT speedup (open; sparse case done by IPS 2013), or a log-shaving "
        "geometry algorithm (Chen 2018 Thm 1.1) yielding NEXP not in poly THR-of-THR. "
        "algebrizes=False is NOT YET ASSESSABLE (a property of a nonexistent "
        "algorithm), not a cleared barrier: it encodes the necessary target profile. "
        "natural_largeness=False is CONDITIONAL: ACW 2016 warn dense poly-size TC0 "
        "likely supports PRF candidates, and if it does, no natural property separates "
        "there, so this evasion fails (a co-equal open obstruction). 'Boolean-rank "
        "collapse' was a placeholder coinage; sign-rank alone provably cannot crack "
        "THR-of-THR."
    ),
)


# --------------------------------------------------------------------------
# Part 2: the savings-reality-check.
# --------------------------------------------------------------------------
#
# Brute-force circuit-SAT on m inputs costs 2^m (times poly). A useful algorithm
# costs 2^m / savings(m). Williams 2010 (STOC 2010 / SICOMP 2013) Thm 1.1: for the
# connection to fire toward NEXP not in P/poly, savings(m) need only be ANY
# superpolynomial factor m^{omega(1)} over the 2^m*poly truth-table cost; Thm 1.2:
# a constant-savings-in-exponent 2^{(1-delta)m} buys the stronger exponential-size
# E^NP bound. The ACC and ACW threshold algorithms achieve 2^{m - m^eps}, the
# 2^{m/polylog}-style "genuine" savings modeled below. We compare three quantities,
# all in log10 to avoid astronomical overflow, against a modest polynomial bar m^c.

def log10_savings_tiny(log10_m: float, eps: float = 0.001) -> float:
    """log10 of a 2^{m^eps} savings factor, given m = 10^{log10_m}.

    Asymptotically superpolynomial for any eps > 0, but the exponent m^eps grows
    glacially: this is the dossier's mirage.
    """
    # m^eps = 10^{eps * log10_m}; savings = 2^{m^eps}; log10 = m^eps * log10(2).
    m_pow_eps = 10.0 ** (eps * log10_m)
    return m_pow_eps * math.log10(2.0)


def log10_savings_genuine(log10_m: float) -> float:
    """log10 of a 2^{m / (log2 m)^2} savings factor, given m = 10^{log10_m}.

    Comfortably superpolynomial and the kind of savings the Williams connection
    actually needs. (log2 m)^2 in the denominator is a mild shave.
    """
    log2_m = log10_m / math.log10(2.0)  # = log2(m)
    if log2_m < 1.0:
        log2_m = 1.0
    exponent = (10.0 ** log10_m) / (log2_m ** 2)  # = m / (log2 m)^2
    return exponent * math.log10(2.0)


def log10_poly_bar(log10_m: float, c: float = 3.0) -> float:
    """log10 of the polynomial bar m^c that a 'real' savings must beat."""
    return c * log10_m


def first_crossover(log10_savings_fn, c: float = 3.0, ceiling: float = 1.0e7) -> float:
    """Smallest log10(m) at which the savings factor exceeds the m^c bar.

    Scans log10(m) and returns the first crossing, or `ceiling` (a stand-in for
    'no feasible-scale crossing') if none is found below it.
    """
    log10_m = 1.0
    step = 1.0
    while log10_m <= ceiling:
        if log10_savings_fn(log10_m) > log10_poly_bar(log10_m, c):
            # refine the crossing to one decimal place for reporting
            lo, hi = log10_m - step, log10_m
            for _ in range(40):
                mid = (lo + hi) / 2.0
                if log10_savings_fn(mid) > log10_poly_bar(mid, c):
                    hi = mid
                else:
                    lo = mid
            return hi
        log10_m += step
    return ceiling


@dataclass
class SavingsRow:
    log10_m: float
    log10_tiny: float
    log10_genuine: float
    log10_bar: float

    @property
    def tiny_beats_bar(self) -> bool:
        return self.log10_tiny > self.log10_bar

    @property
    def genuine_beats_bar(self) -> bool:
        return self.log10_genuine > self.log10_bar


def savings_table(c: float = 3.0) -> list[SavingsRow]:
    # Capped at 10^300: the genuine-savings column grows like m / polylog(m), so
    # 10^1000 would overflow a float. 10^300 is the dossier's reference point and
    # already shows the tiny-eps savings failing by ~900 orders of magnitude.
    scales = [3.0, 30.0, 100.0, 300.0]
    rows = []
    for k in scales:
        rows.append(
            SavingsRow(
                log10_m=k,
                log10_tiny=log10_savings_tiny(k),
                log10_genuine=log10_savings_genuine(k),
                log10_bar=log10_poly_bar(k, c),
            )
        )
    return rows


def main() -> int:
    checker = BarrierChecker()

    print("=== Part 1: the TC0 hinge, barrier audit ===\n")
    print("[Naive route] prove TC0 bounds by worst-case low-degree approximation:")
    naive = checker.check(tc0_approx_degree_route)
    print(naive.report())
    print()
    print("[Candidate winning route] combinatorial dense/deep-threshold SAT speedup:")
    cand = checker.check(threshold_sat_combinatorial)
    print(cand.report())
    print()
    print("[Reference] Williams 2011 NEXP not in ACC0 (the proof-of-concept it must imitate):")
    print(checker.check(BARRIERS["williams_acc0"]).report())
    print()

    # Two DISTINCT obstructions, stated numerically. They live on opposite sides of
    # the hinge and must not be conflated (the prior version conflated them).
    print("Obstruction A (lower-bound / correlation side): WORST-CASE approximate degree")
    print("of MAJORITY is Theta(n) (Paturi 1992); OR/AND only Theta(sqrt n). This blocks the")
    print("low-degree-approximation correlation route, NOT the SAT algorithm.")
    print("Obstruction B (algorithm side): PROBABILISTIC degree of MAJORITY is Theta(sqrt n)")
    print("(Alman-Williams 2015; ACW 2016 Thm 1.1). The SAT algorithm spends THIS, and it")
    print("crosses ONE threshold layer (ACW 2016 Thm 1.8). The wall is density/depth/error budget.")
    print(f"    {'n':>9} | {'approx-deg MAJ ~ n':>18} | {'prob-deg MAJ ~ sqrt(n)':>22} | {'OR/AND ~ sqrt(n)':>16}")
    for n in (100, 10_000, 1_000_000):
        r = math.isqrt(n)
        print(f"    {n:>9,} | {n:>18,} | {r:>22} | {r:>16}")
    print()

    print("=== Part 2: the savings-reality-check ===\n")
    print("Williams 2010 Thm 1.1: ANY superpolynomial savings(m) = m^{omega(1)} over the")
    print("2^m*poly truth-table cost yields NEXP not in P/poly. The mirage below is that a")
    print("2^{m^eps} factor is superpolynomial in the limit yet negligible at any feasible")
    print("scale; the ACC/ACW algorithms instead achieve 2^{m-m^eps}. All values log10.\n")
    header = f"{'log10(m)':>10} | {'log10(2^{m^.001})':>18} | {'log10(2^{m/polylog})':>20} | {'log10(m^3) bar':>14}"
    print(header)
    print("-" * len(header))
    for row in savings_table():
        print(
            f"{row.log10_m:>10.0f} | {row.log10_tiny:>18.3f} | {row.log10_genuine:>20.3e} | {row.log10_bar:>14.0f}"
        )
    print()

    cross_tiny = first_crossover(log10_savings_tiny)
    cross_genuine = first_crossover(log10_savings_genuine)
    print(f"First scale where 2^(m^0.001) beats the m^3 bar : m ~ 10^{cross_tiny:.0f}  (a mirage)")
    print(f"First scale where 2^(m/polylog) beats the m^3 bar: m ~ 10^{cross_genuine:.1f}  (feasible)")
    print()

    # ---- self-checks pinning the corrected coordinates ----
    # NOTE: BarrierChecker is a transparent lookup, not a proof. cand.evades_all
    # records the DECLARED necessary target profile (the same one Williams's proof
    # has); it does NOT certify that the algebrization barrier has been cleared for
    # any actual algorithm. algebrizes=False for the candidate is "not yet
    # assessable" (no such algorithm exists yet); see the HONESTY NOTE above.
    assert naive.hits_natural_proofs, "approximate-degree correlation route must hit natural proofs"
    assert not naive.evades_all, "approximate-degree correlation route must be disqualified"
    assert cand.evades_all, "the combinatorial candidate must match the necessary target profile (declared, not cleared)"

    # Mirage: 2^{m^0.001} does not beat m^3 anywhere near feasible scale (10^300).
    assert not savings_table()[3].tiny_beats_bar, "2^(m^0.001) must NOT beat m^3 at m=10^300"
    assert cross_tiny > 1000.0, "the tiny-eps savings crossover must be astronomically large"
    # Genuine: 2^{m/polylog} beats m^3 by m = 10^30 (well within reach of the model).
    assert savings_table()[1].genuine_beats_bar, "2^(m/polylog) must beat m^3 by m=10^30"
    assert cross_genuine < 30.0, "the genuine savings must cross at a feasible scale"

    print("Self-check OK: the worst-case approximate-degree (correlation) route is")
    print("disqualified by natural proofs; the combinatorial SAT candidate matches the")
    print("necessary target profile (algebrization NOT yet assessable; natural-proofs")
    print("evasion CONDITIONAL on the open TC0-PRF question); tiny-eps savings is a")
    print("mirage, genuine 2^{n-n^eps}-style savings is feasible. CORRECTED hinge: the")
    print("first threshold rung (ACC of THR, one bottom layer) is ALREADY climbed")
    print("(Murray-Williams 2018); the open object is a SAT/CAPP speedup for DENSE")
    print("depth-2 LTF-of-LTF (or deeper TC0). It is open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
