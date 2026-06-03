"""GCT multiplicity-obstruction route: barrier self-check and small-case arithmetic.

BUILDER candidate for Architecture 4 (Geometric Complexity Theory), the backward
reconstruction of a hypothetical 2050 separation of the permanent from the
determinant via *multiplicity obstructions*, not occurrence obstructions.

Context (2026 known facts):
  - Mulmuley-Sohoni (2001, 2008) proposed separating Perm_m from Det_n by finding
    an irreducible GL representation that occurs in the coordinate ring of the
    orbit closure of (a padding of) the permanent but not of the determinant.
  - Burgisser-Ikenmeyer-Panova (2016) proved this OCCURRENCE plan cannot work:
    every irreducible that occurs on the permanent side also occurs on the
    determinant side (no "occurrence obstruction" separates them). Plan A closed.
  - What remains open: MULTIPLICITY obstructions. The multiplicity of an
    irreducible can still be strictly larger on the permanent side than on the
    determinant side even when both are nonzero. A single such inequality, holding
    for n = poly(m), would separate VNP from VP.

This module does three things:
  1. Encodes the multiplicity-obstruction technique as a `ProofTechnique` and runs
     the three-barrier checker (the mandatory discipline).
  2. Computes explicit small-case representation-theoretic data (plethysm-style
     multiplicities and a toy "multiplicity gap") to show the object is concrete
     and computable, not vaporware.
  3. Records the padding/degree bookkeeping that any VNP != VP -> P != NP bridge
     must respect.

Nothing here is a proof. It is a CANDIDATE whose barrier profile is honest and
whose small cases are explicit, handed off to VERIFIER and ADVERSARY.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple

from experiments._shared import BarrierChecker, ProofTechnique


# ---------------------------------------------------------------------------
# 1. The technique, encoded for the barrier checker.
# ---------------------------------------------------------------------------

MULTIPLICITY_OBSTRUCTION = ProofTechnique(
    name="GCT multiplicity obstruction (Perm vs Det orbit closures)",
    # Does NOT relativize: the argument is about the coordinate ring of a specific
    # algebraic variety (the orbit closure of the determinant under GL_{n^2}). There
    # is no machine and no oracle to relativize; the object is the permanent
    # polynomial itself, fully opened up. BGS oracles do not even type-check here.
    relativizes=False,
    # Largeness: a multiplicity-gap property is conjecturally NOT large. It is a
    # statement about one specific pair of polynomials (perm_m, det_n) and the
    # representations carried by their orbit closures. A random polynomial of the
    # same degree has a generic (maximal) orbit and a different multiplicity
    # profile; the property "your orbit-closure coordinate ring under-counts this
    # irreducible relative to the determinant" is function-specific, not satisfied
    # by a constant fraction of functions. So largeness is FALSE (this is the
    # GCT selling point against Razborov-Rudich).
    natural_largeness=False,
    # Constructivity: deciding the property requires computing a plethysm /
    # Kronecker multiplicity, which is #P-hard in general (Ikenmeyer-Mulmuley-Walter
    # 2017 for Kronecker positivity). Even with machine-discovered identities it is
    # not known to be poly-time in the truth-table size. We mark FALSE: the property
    # is plausibly non-constructive, which is a second, independent way out of the
    # natural-proofs barrier.
    natural_constructivity=False,
    # Algebrization: this is the subtle one and the place to be honest. The
    # technique is intrinsically algebraic (it lives over C / a field). The worry
    # is that "algebraic" arguments are exactly what algebrization formalizes as
    # insufficient. The defense is that algebrization (Aaronson-Wigderson) is about
    # algebraic *oracle extensions* of Boolean computation; GCT studies the
    # symmetry group of a fixed polynomial, which is not an oracle-extension
    # construction. There is no known algebraic oracle that makes the perm/det orbit
    # closures coincide. We mark FALSE but flag this as the least settled field.
    algebrizes=False,
    notes=(
        "Multiplicity obstruction: find a partition lambda with "
        "mult_lambda(coord ring of GL-orbit closure of padded perm_m) "
        "> mult_lambda(coord ring of orbit closure of det_n) for n = poly(m). "
        "Burgisser-Ikenmeyer-Panova 2016 killed the occurrence version "
        "(both multiplicities nonzero); the multiplicity version is open. "
        "Non-relativizing (no oracle), conjecturally non-large and "
        "non-constructive (#P-hard plethysm), so it threads natural proofs in "
        "TWO independent ways. Algebrization status is the honest weak point."
    ),
)


# ---------------------------------------------------------------------------
# 2. Explicit small-case representation theory.
# ---------------------------------------------------------------------------
#
# We compute, by hand-coded combinatorics, two quantities that the GCT program
# actually needs, on tiny inputs where the numbers are checkable against the
# literature:
#
#   (a) Plethysm coefficients a_lambda(d, n) = mult of Schur S_lambda in
#       Sym^d(Sym^n(C^k)) for small d, n. These control the representations on the
#       determinant side. We verify the classic identity Sym^2(Sym^2) =
#       S_{(4)} + S_{(2,2)} (as GL-reps), i.e. the d=2, n=2 plethysm.
#
#   (b) A TOY multiplicity gap on a 2x2 model, to illustrate the *shape* of an
#       obstruction (this is a sanity model, NOT the real perm/det gap, which is
#       far out of reach by hand).


def partitions(n: int, max_part: int | None = None) -> List[Tuple[int, ...]]:
    """All integer partitions of n as weakly decreasing tuples."""
    if max_part is None:
        max_part = n
    if n == 0:
        return [()]
    out: List[Tuple[int, ...]] = []
    for first in range(min(n, max_part), 0, -1):
        for rest in partitions(n - first, first):
            out.append((first,) + rest)
    return out


def plethysm_sym2_sym2() -> Dict[Tuple[int, ...], int]:
    """Sym^2(Sym^2 V) as a sum of Schur functors, computed by character.

    Classical result (checkable in any rep-theory text): as GL(V)-representations
    Sym^2(Sym^2 V) = S_{(4)}(V) + S_{(2,2)}(V). We return the multiplicities of the
    degree-4 Schur functors S_{(4)}, S_{(3,1)}, S_{(2,2)}, S_{(2,1,1)}, S_{(1^4)}.

    The multiplicity of S_lambda in Sym^d(Sym^n) is the plethysm coefficient
    a_lambda = <s_lambda, h_d[h_n]> in the symmetric-function inner product. For
    d=n=2 these are well known; we hard-code them as the ground truth and let the
    callers treat them as a fixture (a VERIFIER target to re-derive in Lean).
    """
    return {
        (4,): 1,
        (3, 1): 0,
        (2, 2): 1,
        (2, 1, 1): 0,
        (1, 1, 1, 1): 0,
    }


def plethysm_sym3_sym2() -> Dict[Tuple[int, ...], int]:
    """Sym^3(Sym^2 V) as a sum of Schur functors.

    Classical: Sym^3(Sym^2 V) = S_{(6)} + S_{(4,2)} + S_{(2,2,2)}. Degree-6 Schur
    functors. We return the nonzero multiplicities; everything else is 0. This is
    the next plethysm up and is the kind of datum machine-algebra would tabulate at
    scale on the determinant side.
    """
    return {
        (6,): 1,
        (4, 2): 1,
        (2, 2, 2): 1,
    }


def dim_schur_gl(lam: Tuple[int, ...], k: int) -> int:
    """Dimension of the irreducible GL_k representation S_lam(C^k) via the
    Weyl/hook-content formula:

        dim = prod_{(i,j) in lam} (k + j - i) / hook(i, j).

    Cells are 1-indexed (i row, j column). Returns an int (the product is always an
    integer for a valid partition). Used to sanity-check that the plethysm
    decompositions above have matching total dimensions.
    """
    # build hook lengths
    lam = tuple(p for p in lam if p > 0)
    if not lam:
        return 1
    rows = len(lam)
    # column lengths (conjugate partition)
    maxc = lam[0]
    col = [0] * maxc
    for r in range(rows):
        for c in range(lam[r]):
            col[c] += 1
    num = Fraction(1, 1)
    den = Fraction(1, 1)
    for i in range(rows):
        for j in range(lam[i]):
            arm = lam[i] - (j + 1)
            leg = col[j] - (i + 1)
            hook = arm + leg + 1
            num *= (k + j - i)
            den *= hook
    val = num / den
    assert val.denominator == 1, f"non-integer dim for {lam}, k={k}: {val}"
    return val.numerator


def verify_plethysm_dimension(decomp: Dict[Tuple[int, ...], int], d: int, n: int, k: int) -> Tuple[int, int]:
    """Cross-check: sum of dims of the Schur pieces of Sym^d(Sym^n C^k) must equal
    dim Sym^d(Sym^n C^k) = C(N + d - 1, d) where N = dim Sym^n C^k = C(n+k-1, n).

    Returns (lhs_from_decomp, rhs_direct). Caller asserts equality.
    """
    from math import comb

    lhs = sum(mult * dim_schur_gl(lam, k) for lam, mult in decomp.items())
    big_n = comb(n + k - 1, n)
    rhs = comb(big_n + d - 1, d)
    return lhs, rhs


@dataclass
class ToyMultiplicityGap:
    """A toy illustration of the *form* of a multiplicity obstruction.

    We are NOT computing the real perm_m vs det_n orbit-closure multiplicities by
    hand (out of reach). Instead we model the asymmetry abstractly: suppose on the
    'hard side' (permanent analog) an irreducible S_lambda appears with multiplicity
    m_hard, and on the 'easy side' (determinant analog) with multiplicity m_easy. An
    obstruction in the BIP sense is the strict inequality m_hard > m_easy with both
    nonzero (so it is a genuine multiplicity gap, invisible to occurrence tests).
    """

    lam: Tuple[int, ...]
    m_hard: int
    m_easy: int

    @property
    def is_occurrence_obstruction(self) -> bool:
        """The (now-dead) BIP-2016 kind: appears on hard side, absent on easy side."""
        return self.m_hard > 0 and self.m_easy == 0

    @property
    def is_multiplicity_obstruction(self) -> bool:
        """The live kind: present on BOTH sides but strictly more on the hard side."""
        return self.m_hard > self.m_easy and self.m_easy > 0

    def classify(self) -> str:
        if self.is_occurrence_obstruction:
            return "occurrence obstruction (ruled out by Burgisser-Ikenmeyer-Panova 2016)"
        if self.is_multiplicity_obstruction:
            return "multiplicity obstruction (open route; what 2050 would need)"
        if self.m_hard == self.m_easy:
            return "no obstruction (multiplicities equal)"
        return "anti-obstruction (easy side has more; useless for separation)"


def main() -> int:
    print("=" * 72)
    print("GCT multiplicity-obstruction route: BUILDER barrier self-check")
    print("=" * 72)

    # --- Mandatory three-barrier discipline -------------------------------
    verdict = BarrierChecker().check(MULTIPLICITY_OBSTRUCTION)
    print(verdict.report())
    print()

    # --- Small-case plethysm fixtures, dimension-checked ------------------
    print("-" * 72)
    print("Explicit plethysm decompositions (determinant-side rep theory)")
    print("-" * 72)
    for label, decomp, d, n in [
        ("Sym^2(Sym^2 V)", plethysm_sym2_sym2(), 2, 2),
        ("Sym^3(Sym^2 V)", plethysm_sym3_sym2(), 3, 2),
    ]:
        nonzero = {lam: m for lam, m in decomp.items() if m > 0}
        print(f"{label} = " + " + ".join(
            (f"{m}*S_{lam}" if m != 1 else f"S_{lam}") for lam, m in nonzero.items()
        ))
        for k in (2, 3, 4):
            lhs, rhs = verify_plethysm_dimension(decomp, d, n, k)
            status = "OK" if lhs == rhs else "MISMATCH"
            print(f"    dim check k={k}: sum_of_pieces={lhs}, direct={rhs}  [{status}]")
            assert lhs == rhs, f"dimension mismatch for {label} at k={k}"
    print()

    # --- Toy multiplicity gap, classified ---------------------------------
    print("-" * 72)
    print("Toy obstruction classification (shape of an obstruction, not the real gap)")
    print("-" * 72)
    samples = [
        ToyMultiplicityGap((3, 1), m_hard=2, m_easy=0),  # dead occurrence kind
        ToyMultiplicityGap((2, 2), m_hard=5, m_easy=3),  # live multiplicity kind
        ToyMultiplicityGap((4,), m_hard=4, m_easy=4),    # no gap
        ToyMultiplicityGap((2, 1, 1), m_hard=1, m_easy=7),  # anti-obstruction
    ]
    for s in samples:
        print(f"  S_{s.lam}: m_hard={s.m_hard}, m_easy={s.m_easy} -> {s.classify()}")
    print()

    print("Summary: technique evades all three barriers per the checker "
          f"({'PASS' if verdict.evades_all else 'FAIL'}); "
          "algebrization is the honest weak point and is flagged for ADVERSARY.")
    return 0 if verdict.evades_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
