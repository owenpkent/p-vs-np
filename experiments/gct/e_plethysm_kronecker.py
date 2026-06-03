"""Kronecker coefficients from scratch: the multiplicities the GCT program compares.

The Kronecker coefficient g(lambda, mu, nu) is the multiplicity of the irreducible
S_nu in the tensor product S_lambda (x) S_mu of two irreducible representations of
the symmetric group S_n. By character theory it is

    g(lambda, mu, nu) = (1/n!) sum_{sigma in S_n} chi_lambda(sigma) chi_mu(sigma) chi_nu(sigma),

which (grouping by conjugacy class, i.e. by cycle type) is a finite sum over
partitions of n. This module computes the S_n irreducible characters by the
Murnaghan-Nakayama rule (rim-hook removal via the beta-set / abacus), assembles the
character table, and computes Kronecker coefficients, with strong correctness checks.

Why this is the GCT object. Mulmuley-Sohoni reduce the GCT multiplicities that would
separate the permanent from the determinant to rectangular Kronecker coefficients.
Deciding positivity of Kronecker coefficients is #P-hard (Ikenmeyer-Mulmuley-Walter
2017), which is exactly why the multiplicity-obstruction program is stuck on
computation. Burgisser-Ikenmeyer-Panova 2016 closed the OCCURRENCE route (the
relevant coefficients are nonzero on both sides), and Dorfler-Ikenmeyer-Panova 2019
showed multiplicity obstructions are strictly stronger than occurrence obstructions.
This module is the concrete, checkable arithmetic those boundary results are about.
Companion barrier self-check: e_multiplicity_obstruction.py.

What is verified here (no overclaiming): the character table is orthonormal, the
dimensions match the hook-length formula and sum of squares is n!, and the computed
Kronecker coefficients are nonnegative integers, fully symmetric in the three
partitions, and satisfy g(lambda, (n), nu) = [lambda = nu] (tensoring with the
trivial representation) and g(lambda, (1^n), nu) = [conjugate(lambda) = nu]
(tensoring with the sign representation). No claim about GCT separation is made.

Run:
    python -m experiments.gct.e_plethysm_kronecker
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from math import factorial


def partitions(n: int, max_part: int | None = None) -> list[tuple[int, ...]]:
    """All integer partitions of n as weakly decreasing tuples (descending)."""
    if max_part is None:
        max_part = n
    if n == 0:
        return [()]
    out: list[tuple[int, ...]] = []
    for first in range(min(n, max_part), 0, -1):
        for rest in partitions(n - first, first):
            out.append((first,) + rest)
    return out


def conjugate(lam: tuple[int, ...]) -> tuple[int, ...]:
    """Conjugate (transpose) partition."""
    if not lam:
        return ()
    return tuple(sum(1 for p in lam if p >= j) for j in range(1, lam[0] + 1))


def z_class(mu: tuple[int, ...]) -> int:
    """The centralizer order z_mu = prod_i i^{m_i} m_i!, so class size = n!/z_mu."""
    c = Counter(mu)
    z = 1
    for part, mult in c.items():
        z *= (part ** mult) * factorial(mult)
    return z


def _border_strip_removals(lam: tuple[int, ...], k: int) -> list[tuple[tuple[int, ...], int]]:
    """All ways to remove a border strip (rim hook) of size k from lam, via the
    beta-set: replace a bead beta_i by beta_i - k when that slot is empty. Returns
    (resulting partition, height) pairs, where height = number of beads jumped.
    """
    lam = tuple(x for x in lam if x > 0)
    R = len(lam)
    if R == 0:
        return []
    beta = [lam[i] + (R - 1 - i) for i in range(R)]  # distinct, strictly decreasing
    beta_set = set(beta)
    out: list[tuple[tuple[int, ...], int]] = []
    for i in range(R):
        target = beta[i] - k
        if target < 0 or target in beta_set:
            continue
        height = sum(1 for j in range(R) if j != i and target < beta[j] < beta[i])
        new_beta = sorted(beta[:i] + [target] + beta[i + 1:], reverse=True)
        new_lam = tuple(new_beta[t] - (R - 1 - t) for t in range(R))
        out.append((tuple(x for x in new_lam if x > 0), height))
    return out


@lru_cache(maxsize=None)
def character(lam: tuple[int, ...], mu: tuple[int, ...]) -> int:
    """Irreducible character chi_lam evaluated at cycle type mu (Murnaghan-Nakayama).
    Both lam and mu are partitions of the same n, given in descending order.
    """
    if not mu:
        return 1 if not lam else 0
    k = mu[0]
    rest = mu[1:]
    total = 0
    for new_lam, height in _border_strip_removals(lam, k):
        total += (-1) ** height * character(new_lam, rest)
    return total


def hook_length_dim(lam: tuple[int, ...], n: int) -> int:
    """Number of standard Young tableaux of shape lam (the irrep dimension), by the
    hook-length formula n! / prod(hooks)."""
    lam = tuple(x for x in lam if x > 0)
    if not lam:
        return 1
    cols = conjugate(lam)
    prod = 1
    for i in range(len(lam)):
        for j in range(lam[i]):
            arm = lam[i] - (j + 1)
            leg = cols[j] - (i + 1)
            prod *= (arm + leg + 1)
    return factorial(n) // prod


def kronecker(lam, mu, nu, n: int) -> int:
    """Kronecker coefficient g(lam, mu, nu) via the character inner product."""
    total = 0
    for cyc in partitions(n):
        size = factorial(n) // z_class(cyc)
        total += size * character(lam, cyc) * character(mu, cyc) * character(nu, cyc)
    assert total % factorial(n) == 0, "Kronecker coefficient must be an integer"
    return total // factorial(n)


def main() -> int:
    print("=== Kronecker coefficients from scratch (the GCT multiplicities) ===\n")

    # Character-table checks for several n.
    for n in (3, 4, 5, 6):
        parts = partitions(n)
        # orthonormality: sum_classes |class| chi_a(c) chi_b(c) = n! [a = b]
        for a in parts:
            for b in parts:
                s = sum((factorial(n) // z_class(c)) * character(a, c) * character(b, c) for c in parts)
                expected = factorial(n) if a == b else 0
                assert s == expected, f"orthonormality failed n={n}, {a},{b}: {s} != {expected}"
        # dimensions: chi_lam(1^n) = hook-length dim; sum of squares = n!
        ones = tuple([1] * n)
        dims = {lam: character(lam, ones) for lam in parts}
        for lam in parts:
            assert dims[lam] == hook_length_dim(lam, n), f"dim mismatch n={n}, {lam}"
        assert sum(d * d for d in dims.values()) == factorial(n), f"sum of squares != n! at n={n}"
        print(f"n={n}: {len(parts)} irreducibles, character table orthonormal, "
              f"sum(dim^2) = {sum(d*d for d in dims.values())} = {n}!")
    print()

    # Kronecker coefficients and their structural identities, for n = 4 and 5.
    for n in (4, 5):
        parts = partitions(n)
        trivial = (n,)
        sign = tuple([1] * n)
        for lam in parts:
            for mu in parts:
                for nu in parts:
                    g = kronecker(lam, mu, nu, n)
                    assert g >= 0, f"negative Kronecker coefficient g({lam},{mu},{nu})={g}"
                    # full symmetry in the three partitions
                    assert g == kronecker(mu, lam, nu, n) == kronecker(lam, nu, mu, n), \
                        f"Kronecker symmetry failed at {lam},{mu},{nu}"
            # tensoring with the trivial rep is the identity
            for nu in parts:
                assert kronecker(lam, trivial, nu, n) == (1 if lam == nu else 0), \
                    f"trivial-tensor identity failed at {lam},{nu}"
            # tensoring with the sign rep transposes
            for nu in parts:
                assert kronecker(lam, sign, nu, n) == (1 if conjugate(lam) == nu else 0), \
                    f"sign-tensor identity failed at {lam},{nu}"
        print(f"n={n}: all {len(parts)**3} Kronecker coefficients are nonnegative integers, "
              f"fully symmetric, and pass the trivial/sign tensor identities.")
    print()

    # A small explicit table for n = 5: g(lambda, mu, nu) for a fixed nu, to exhibit
    # the multiplicities the GCT program would compare.
    n = 5
    parts = partitions(n)
    nu = (3, 2)
    print(f"Sample n=5 Kronecker coefficients g(lambda, mu, (3,2)) (the multiplicity of S_(3,2)):")
    interesting = [(4, 1), (3, 2), (3, 1, 1), (2, 2, 1)]
    header = "  lambda\\mu  | " + "  ".join(f"{str(mu):>10}" for mu in interesting)
    print(header)
    for lam in interesting:
        row = "  ".join(f"{kronecker(lam, mu, nu, n):>10}" for mu in interesting)
        print(f"  {str(lam):>10} | {row}")
    print()

    print("GCT bearing: these Kronecker coefficients are the multiplicities the")
    print("multiplicity-obstruction program compares (Mulmuley-Sohoni reduce the GCT")
    print("coefficients to rectangular Kronecker coefficients). Deciding their positivity")
    print("is #P-hard (Ikenmeyer-Mulmuley-Walter 2017), which is why GCT is stuck on")
    print("computation. BIP 2016 closed occurrence obstructions; DIP 2019 showed")
    print("multiplicity obstructions are strictly stronger. See e_multiplicity_obstruction.py.")
    print()
    print("Self-check OK: characters orthonormal, dimensions match hook lengths, and")
    print("Kronecker coefficients are nonnegative integers with all the required identities.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
