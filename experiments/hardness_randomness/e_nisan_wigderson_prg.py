"""Nisan-Wigderson in miniature: combinatorial designs, and why the PRG needs a
hard function.

The Nisan-Wigderson generator turns a hard Boolean function $f: \\{0,1\\}^l \\to
\\{0,1\\}$ into a pseudorandom generator. Fix a combinatorial $(l, k)$-design: sets
$S_1, \\dots, S_m \\subseteq [d]$ with $|S_i| = l$ and $|S_i \\cap S_j| \\le k$ for
$i \\ne j$. The generator is

    NW_f(z) = (f(z|_{S_1}), \\dots, f(z|_{S_m})),   z in {0,1}^d,

stretching $d$ seed bits to $m$ output bits. The theorem (Nisan-Wigderson 1994): if
$f$ cannot be approximated by circuits of size $s$, then $NW_f$ fools circuits of
size $\\approx s$. The proof is a reconstruction argument: a distinguisher for
$NW_f$ yields a small circuit predicting $f$, contradicting hardness. Combined with
Impagliazzo-Wigderson 1997 (if $E$ requires exponential circuits then
$\\mathsf{BPP} = \\mathsf{P}$), hardness gives full derandomization.

This module demonstrates the combinatorial core and the role of hardness:

  1. Build the polynomial $(l, k)$-design over $\\mathbb{F}_q$ (sets indexed by
     degree-$\\le k$ polynomials, $S_p = \\{(x, p(x)) : x \\in \\mathbb{F}_q\\}$),
     and verify $|S_p| = q$ and pairwise intersection $\\le k$ (distinct degree-$k$
     polynomials agree on at most $k$ points). The stretch is $d = q^2$ to
     $m = q^{k+1}$.
  2. Show, honestly, that the PRG property NEEDS a hard $f$: with $f = $ PARITY
     (linear, easy), each output bit is an $\\mathbb{F}_2$-linear function of the
     seed, so once $m > d$ there is a linear dependency among the output bits, and
     the XOR of a fixed set of output bits is identically 0, a perfect distinguisher.
     With a nonlinear $f$ (MAJORITY) the same dependency does NOT make the output
     constant, so the trivial attack fails. Hardness is what blocks the distinguisher.

What is verified here (no overclaiming): the design properties and the stretch are
checked exactly; the parity distinguisher is exhibited explicitly (a guaranteed
linear dependency) and confirmed identically zero on a sample; the nonlinear case is
shown not to collapse under the same attack. The full reconstruction theorem
(distinguisher implies predictor) is stated, not reimplemented.

Run:
    python -m experiments.hardness_randomness.e_nisan_wigderson_prg
"""

from __future__ import annotations

import itertools
import random


def poly_design(q: int, k: int) -> list[tuple[int, ...]]:
    """The Nisan-Wigderson polynomial (l, k)-design over F_q (q prime).

    Each degree-<=k polynomial p over F_q gives the set
    S_p = {(x, p(x)) : x in F_q}, encoded as universe indices x*q + y in [q^2].
    Returns the list of sets (as sorted tuples of indices); there are q^{k+1} of
    them, each of size q, with pairwise intersection <= k.
    """
    sets = []
    for coeffs in itertools.product(range(q), repeat=k + 1):  # a_0 + a_1 x + ... + a_k x^k
        pts = []
        for x in range(q):
            y = 0
            xp = 1
            for a in coeffs:
                y = (y + a * xp) % q
                xp = (xp * x) % q
            pts.append(x * q + y)
        sets.append(tuple(sorted(pts)))
    return sets


def verify_design(sets: list[tuple[int, ...]], q: int, k: int) -> tuple[int, int]:
    """Check |S_i| = q and max pairwise intersection. Returns (m, max_intersection)."""
    for S in sets:
        assert len(S) == q, "each design set must have size q"
    max_int = 0
    for a, b in itertools.combinations(sets, 2):
        inter = len(set(a) & set(b))
        if inter > max_int:
            max_int = inter
    return len(sets), max_int


def find_linear_dependency(vectors: list[int]) -> set[int]:
    """Find a nonempty subset T of the F_2 vectors (given as bitmask ints) whose XOR
    is 0, via Gaussian elimination tracking row combinations. Returns T (indices).
    Guaranteed to exist when len(vectors) exceeds the ambient dimension.
    """
    basis: dict[int, tuple[int, frozenset]] = {}  # pivot bit -> (reduced row, combo)
    for i, v in enumerate(vectors):
        row, combo = v, {i}
        while row:
            pivot = row.bit_length() - 1
            if pivot in basis:
                prow, pcombo = basis[pivot]
                row ^= prow
                combo ^= pcombo  # symmetric difference of index sets
            else:
                basis[pivot] = (row, frozenset(combo))
                break
        if row == 0:
            return set(combo)
    return set()


def restrict(z: int, S: tuple[int, ...]) -> tuple[int, ...]:
    """The bits of seed z (an int) at positions S."""
    return tuple((z >> j) & 1 for j in S)


def f_parity(bits: tuple[int, ...]) -> int:
    return sum(bits) % 2


def f_majority(bits: tuple[int, ...]) -> int:
    return 1 if sum(bits) > len(bits) // 2 else 0


def main() -> int:
    print("=== Nisan-Wigderson in miniature: designs and the role of hardness ===\n")

    print("Polynomial (l, k)-designs over F_q (sets of size q, pairwise intersection <= k):")
    for q, k in [(3, 2), (5, 2)]:
        sets = poly_design(q, k)
        m, max_int = verify_design(sets, q, k)
        d = q * q
        print(f"    q={q}, k={k}: universe d = {d}, sets m = {m} = {q}^{k+1}, "
              f"set size = {q}, max pairwise intersection = {max_int} (<= {k})")
        assert m == q ** (k + 1), "number of sets must be q^(k+1)"
        assert max_int <= k, "pairwise intersection must be at most k"
        assert m > d, "the generator must stretch (m > d) for k >= 2"
    print()

    # Hardness is necessary: parity (easy) gives a distinguishable generator.
    q, k = 5, 2
    sets = poly_design(q, k)
    d = q * q
    # output bit i is the F_2 vector = indicator of S_i (parity is linear)
    indicators = [sum(1 << j for j in S) for S in sets]
    T = find_linear_dependency(indicators)
    assert T, "with m > d there must be a linear dependency among the output bits"
    print(f"PARITY generator (f = XOR): found a linear dependency over {len(T)} output bits.")

    random.seed(20260602)
    sample = [random.getrandbits(d) for _ in range(1000)]

    def xor_over_T(z: int, f) -> int:
        acc = 0
        for i in T:
            acc ^= f(restrict(z, sets[i]))
        return acc

    parity_vals = {xor_over_T(z, f_parity) for z in sample}
    print(f"    XOR of those output bits over the sample: values seen = {sorted(parity_vals)}")
    assert parity_vals == {0}, "parity: the dependent output bits XOR to 0 always (perfect distinguisher)"
    print("    -> identically 0, so NW_parity is perfectly distinguishable from uniform.")
    print()

    # A nonlinear f (majority) does NOT collapse under the same attack.
    maj_vals = {xor_over_T(z, f_majority) for z in sample}
    print(f"MAJORITY generator (f = MAJ, nonlinear): same output bits, XOR values seen = {sorted(maj_vals)}")
    assert maj_vals == {0, 1}, "majority: the same XOR is non-constant, the linear attack fails"
    print("    -> non-constant, so the trivial linear distinguisher does not apply. Hardness blocks it.")
    print()

    print("Hardness-randomness connection (Architecture 5, the structural surroundings):")
    print("  - Nisan-Wigderson 1994: a function hard for size-s circuits yields a PRG fooling")
    print("    size-s circuits, via the design above and a reconstruction argument.")
    print("  - Impagliazzo-Wigderson 1997: if E requires exponential circuits, then BPP = P.")
    print("  - Kabanets-Impagliazzo 2004: derandomizing polynomial identity testing implies")
    print("    circuit lower bounds, so derandomization and lower bounds are entangled.")
    print("  This is not a direct P-vs-NP separation; it constrains and informs the question.")
    print()
    print("Self-check OK: polynomial designs verified (size q, intersection <= k, stretch m > d);")
    print("NW_parity is distinguishable (easy f), NW_majority resists the same attack (hardness")
    print("is necessary for the PRG property).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
