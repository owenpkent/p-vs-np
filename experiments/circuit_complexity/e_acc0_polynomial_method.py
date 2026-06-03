"""Razborov-Smolensky in miniature: PARITY has no low-degree polynomial over F_3.

The polynomial method (Razborov 1987, Smolensky 1987) proves that
$\\mathrm{MOD}_2 = \\mathrm{PARITY}$ is not in $\\mathsf{AC}^0[3]$ (constant-depth
circuits with AND/OR/NOT and MOD_3 gates, polynomial size). Two steps:

  1. (easy) Every AC0[3] circuit of size s and depth d is approximated, on a
     (1 - eps) fraction of inputs, by a polynomial over F_3 of degree
     O((log(s/eps))^d). Low depth and size force low degree.
  2. (hard) PARITY agrees with no low-degree F_3 polynomial: any degree-D
     polynomial over F_3 agrees with PARITY on at most a (1/2 + O(D/sqrt(n)))
     fraction of {0,1}^n, so matching PARITY forces D = Omega(sqrt(n)).

Together: a polynomial-size constant-depth AC0[3] circuit would give a low-degree
approximator, contradicting step 2. Hence PARITY is not in AC0[3].

Why this belongs in the project. The polynomial method is a NATURAL proof (large
and constructive), confirmed below via the barrier checker. That is why it
separates only against AC0[p] (which contains no pseudorandom generators), not
against P/poly: against general circuits a natural property would break PRGs
(Razborov-Rudich 1994). It is also exactly why the method dies at threshold gates:
MAJORITY has approximate degree Theta(n) (Paturi 1992), so it has no low-degree
approximant, which is the TC0 hinge modeled in e_tc0_sat_savings.py.

What is demonstrated EXACTLY here (no overclaiming): (a) the exact F_3 multilinear
degree of PARITY is n (proved: the top coefficient is (-1)^{n+1} 2^{n-1}, which is
1 mod 3 for every n), so PARITY needs full degree for EXACT representation over
F_3; (b) a small brute-force search confirms low-degree F_3 polynomials cannot even
match PARITY on all inputs, with the best agreement reported. The Omega(sqrt n)
APPROXIMATION bound (step 2) is the deep theorem; it is stated, not brute-forced,
because enumeration is infeasible at the n where sqrt(n) separates from n.

Run:
    python -m experiments.circuit_complexity.e_acc0_polynomial_method
"""

from __future__ import annotations

import itertools

from experiments._shared import BarrierChecker, ProofTechnique


def parity_values(n: int) -> list[int]:
    """PARITY on {0,1}^n as a list indexed by the integer x in [0, 2^n)."""
    return [bin(x).count("1") % 2 for x in range(2 ** n)]


def f3_multilinear_coeffs(values: list[int], n: int) -> dict[int, int]:
    """Multilinear coefficients over F_3 of f: {0,1}^n -> F_3.

    The unique multilinear polynomial p with p(x) = f(x) on {0,1}^n has
    c_S = sum_{T subseteq S} (-1)^{|S|-|T|} f(1_T) (mod 3), the Mobius inversion,
    indexed by the subset bitmask S (bit i set means coordinate i is in S).
    """
    coeffs: dict[int, int] = {}
    for S in range(2 ** n):
        popS = bin(S).count("1")
        total = 0
        T = S
        while True:  # enumerate all submasks T of S, including S and 0
            sign = -1 if ((popS - bin(T).count("1")) & 1) else 1
            total += sign * values[T]
            if T == 0:
                break
            T = (T - 1) & S
        coeffs[S] = total % 3
    return coeffs


def f3_degree(values: list[int], n: int) -> int:
    """Largest |S| with a nonzero F_3 multilinear coefficient."""
    coeffs = f3_multilinear_coeffs(values, n)
    return max((bin(S).count("1") for S, c in coeffs.items() if c % 3 != 0), default=0)


def best_agreement_degree_d(n: int, d: int, target: list[int]) -> int:
    """Max number of points (out of 2^n) where a degree-<=d F_3 polynomial equals
    target. Brute force over all coefficient vectors in F_3^{D(n,d)}; only feasible
    for small n and d (used here for an illustration, not the asymptotic bound).
    """
    monos = [S for S in range(2 ** n) if bin(S).count("1") <= d]
    npts = 2 ** n
    # active[x] = indices i with monos[i] subseteq x (the monomial evaluates to 1 at x)
    active = [[i for i, S in enumerate(monos) if (S & x) == S] for x in range(npts)]
    best = 0
    for coeffs in itertools.product((0, 1, 2), repeat=len(monos)):
        agree = 0
        for x in range(npts):
            val = 0
            for i in active[x]:
                val += coeffs[i]
            if val % 3 == target[x]:
                agree += 1
        if agree > best:
            best = agree
            if best == npts:
                break
    return best


# The Razborov-Smolensky polynomial method, encoded for the barrier checker. It is
# the same profile as the monotone method already in BARRIERS: non-relativizing
# (it opens the circuit), NATURAL (large + constructive: low-degree approximability
# is a property of a constant fraction of functions and is poly(2^n)-testable),
# non-algebrizing. Its naturalness is exactly why it does not extend to P/poly.
rs_polynomial_method = ProofTechnique(
    name="Razborov-Smolensky polynomial method (AC0[p] lower bounds)",
    relativizes=False,
    natural_largeness=True,
    natural_constructivity=True,
    algebrizes=False,
    notes=(
        "Proves MOD_q / MAJORITY require exponential AC0[p] size via low-degree F_3 "
        "approximation. A natural proof in the Razborov-Rudich sense; it does not "
        "violate the barrier because it bounds only AC0[p], where no pseudorandom "
        "generators are assumed. Against P/poly a natural property would break PRGs, "
        "and the method cannot reach threshold gates (MAJORITY has approximate degree "
        "Theta(n), no low-degree approximant). This is why it is restricted-class only."
    ),
)


def main() -> int:
    print("=== Razborov-Smolensky in miniature: PARITY has no low-degree F_3 polynomial ===\n")

    print("Exact F_3 multilinear degree of PARITY (must equal n):")
    for n in range(2, 9):
        deg = f3_degree(parity_values(n), n)
        print(f"    n = {n}:  F_3 degree = {deg}  (need full degree {n} for exact representation)")
        assert deg == n, f"PARITY F_3 degree should be {n}, got {deg}"
    print()

    print("Best agreement of a degree-<=d F_3 polynomial with PARITY (brute force):")
    for n in (3, 4):
        target = parity_values(n)
        npts = 2 ** n
        for d in range(0, 3):
            best = best_agreement_degree_d(n, d, target)
            tag = "  <- perfect" if best == npts else ""
            print(f"    n = {n}, degree <= {d}:  best agreement = {best}/{npts}{tag}")
            # low degree (d < n) cannot match PARITY on all inputs
            assert best < npts, f"degree-{d} F_3 poly should not match PARITY on all {npts} points"
    print()

    checker = BarrierChecker()
    print("Barrier profile of the polynomial method:")
    verdict = checker.check(rs_polynomial_method)
    print(verdict.report())
    print()
    assert verdict.hits_natural_proofs, "the polynomial method must be flagged natural"
    assert not verdict.evades_all, "a natural method is disqualified against P/poly"

    print("Self-check OK: PARITY needs full F_3 degree n; low-degree F_3 polynomials")
    print("cannot match it; the polynomial method is natural, hence restricted-class")
    print("only (it cannot reach P/poly, and dies at threshold gates).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
