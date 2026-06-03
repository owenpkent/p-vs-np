"""The TC0 hinge: a satisfiability-savings model for the Williams program's
first rung past ACC0.

The 2050 backward-induction dossier (docs/03_research/2050_backward_induction.md)
identifies a single load-bearing milestone on the leading path to
P != NP: the late-2030s step where the algorithm-to-lower-bound connection
(Williams 2011) climbs from ACC0 to TC0 (threshold circuits). Every surviving
P != NP scenario routes through that connection, and in 2026 the connection is
stuck at exactly one wall. The Razborov-Smolensky polynomial method, which
powered the ACC0 / AC0[p] bounds, provably stops at threshold gates: MAJORITY has
no low-degree polynomial representation (its approximate degree is Theta(sqrt n),
Paturi 1992), so the low-degree-approximation budget that beats ACC0 blows up at
TC0.

This module pins the hinge as a runnable, checkable object. It does two things.

  1. Barrier audit of two candidate routes to a TC0-SAT speedup:
       - the naive "extend the polynomial method to TC0" route, which is caught
         by the natural-proofs barrier (the method of low-degree approximation is
         large + constructive) and which does not even apply at threshold gates;
       - the candidate "Boolean-rank-collapse" combinatorial speedup fed through
         the Williams template, which (if it exists) threads all three barriers
         exactly as Williams's ACC0 argument does. Its `algebrizes=False` is the
         load-bearing claim: the speedup must be genuinely combinatorial, not the
         arithmetizing polynomial method.

  2. A savings-reality-check reproducing the dossier's numerical coordinate: a
     savings factor of the form 2^{n^eps} for tiny eps is asymptotically
     "superpolynomial" yet a mirage at any feasible scale, while a genuinely
     strong savings (2^{n / polylog n}) dominates a polynomial bar at human
     scale. The Williams connection needs the latter, not the former.

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

# The naive route: try to push Razborov-Smolensky's low-degree polynomial method
# from ACC0 up to TC0. It is a natural proof (large + constructive: the method
# certifies hardness by a property of the function's low-degree approximability,
# which holds for a constant fraction of functions and is poly(2^n)-testable).
# It also does not relativize (it opens the circuit), and it is the arithmetizing
# object, so it algebrizes. The decisive fact, however, is structural: the method
# requires a low-degree polynomial approximation that simply does not exist for
# threshold gates, so it cannot reach TC0 even before the barrier bites.
tc0_polynomial_method = ProofTechnique(
    name="TC0-SAT via the polynomial method (Razborov-Smolensky pushed to threshold gates)",
    relativizes=False,
    natural_largeness=True,
    natural_constructivity=True,
    algebrizes=True,
    notes=(
        "Natural (large + constructive) and algebrizing. Independently, it does not "
        "even apply: MAJORITY has approximate degree Theta(sqrt n) (Paturi 1992), so "
        "the low-degree-approximation budget that beats ACC0 blows up at TC0. This is "
        "the wall the Williams program hits at the first rung past ACC0."
    ),
)

# The candidate winning route: a combinatorial faster-than-brute-force
# satisfiability / circuit-analysis algorithm for TC0 (working name
# "Boolean-rank collapse"), fed through the Williams algorithm-to-lower-bound
# connection. If such an algorithm exists, the resulting lower bound threads all
# three barriers exactly as Williams's ACC0 proof does: non-relativizing (the
# algorithm opens the gate structure), non-natural (the diagonalization is
# non-constructive and function-specific, not a large property), and
# non-algebrizing (the speedup is combinatorial, not a low-degree polynomial
# functional). The algebrizes=False flag is the load-bearing claim.
tc0_sat_boolean_rank = ProofTechnique(
    name="TC0-SAT via a combinatorial Boolean-rank-collapse speedup (Williams template)",
    relativizes=False,
    natural_largeness=False,
    natural_constructivity=False,
    algebrizes=False,
    notes=(
        "The honest target for the late-2030s hinge: a non-trivial TC0 satisfiability "
        "algorithm beating brute force by a genuinely superpolynomial factor, fed "
        "through the Williams connection to yield NEXP not in TC0. Load-bearing claim: "
        "the speedup must be combinatorial (a Boolean / sign-rank collapse), NOT the "
        "polynomial method, or it algebrizes and the algebrization evasion fails. This "
        "is asserted here, not proved: it is the open problem the hinge names."
    ),
)


# --------------------------------------------------------------------------
# Part 2: the savings-reality-check.
# --------------------------------------------------------------------------
#
# Brute-force circuit-SAT on m inputs costs 2^m (times poly). A useful algorithm
# costs 2^m / savings(m). For the Williams connection to fire, savings(m) must be
# superpolynomial in m, i.e. m^{omega(1)}. We compare three quantities, all in
# log10 to avoid astronomical overflow, against a modest polynomial bar m^c.

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
    print("[Naive route] push the polynomial method from ACC0 up to TC0:")
    naive = checker.check(tc0_polynomial_method)
    print(naive.report())
    print()
    print("[Candidate winning route] combinatorial Boolean-rank-collapse SAT algorithm:")
    cand = checker.check(tc0_sat_boolean_rank)
    print(cand.report())
    print()
    print("[Reference] Williams 2011 NEXP not in ACC0 (the proof-of-concept it must imitate):")
    print(checker.check(BARRIERS["williams_acc0"]).report())
    print()

    # The structural fact that makes TC0 the wall, stated numerically.
    print("Structural wall: approximate degree of MAJORITY on n bits is Theta(sqrt n).")
    for n in (100, 10_000, 1_000_000):
        print(f"    n = {n:>9,}:  ~sqrt(n) = {math.isqrt(n):>5}  (the low-degree budget that beats ACC0 cannot reach this)")
    print()

    print("=== Part 2: the savings-reality-check ===\n")
    print("Williams connection needs savings(m) = m^{omega(1)} that DOMINATES the 2^m")
    print("truth-table work at feasible scale. All values below are log10.\n")
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

    # ---- self-checks pinning the dossier's coordinates ----
    assert naive.hits_natural_proofs, "polynomial-method route must hit the natural-proofs barrier"
    assert not naive.evades_all, "polynomial-method route must be disqualified"
    assert cand.evades_all, "the combinatorial candidate must evade all three (necessary, not sufficient)"

    # Mirage: 2^{m^0.001} does not beat m^3 anywhere near feasible scale (10^300).
    assert not savings_table()[3].tiny_beats_bar, "2^(m^0.001) must NOT beat m^3 at m=10^300"
    assert cross_tiny > 1000.0, "the tiny-eps savings crossover must be astronomically large"
    # Genuine: 2^{m/polylog} beats m^3 by m = 10^30 (well within reach of the model).
    assert savings_table()[1].genuine_beats_bar, "2^(m/polylog) must beat m^3 by m=10^30"
    assert cross_genuine < 30.0, "the genuine savings must cross at a feasible scale"

    print("Self-check OK: polynomial-method route disqualified; combinatorial candidate")
    print("evades all three; tiny-eps savings is a mirage, genuine savings is feasible.")
    print("The hinge is the existence of the combinatorial TC0-SAT speedup. It is open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
