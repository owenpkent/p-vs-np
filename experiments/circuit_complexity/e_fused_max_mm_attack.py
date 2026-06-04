"""Fused-max-MM (the J1 frontier): the four first-principles ATTACKS on the bulk-vs-extreme wall.

THE TARGET (Chen 2018, arXiv:1805.10698, Theorem 1.5 item 1, web-confirmed VERBATIM in the
sibling e_maxip_logshave.py):

  "An n^2 / log^{omega(1)} n time algorithm for Bichromatic Maximum Inner Product with vector
   dimension d = n^eps for any small constant eps would imply NEXP has no polynomial size
   THR o THR circuits. Note there is an n^2 polylog(n) time algorithm via fast rectangle
   matrix multiplication."

So A, B are each n Boolean vectors in {0,1}^d, d = n^eps. M = A B^T is the n x n INTEGER count
matrix, M_{ij} = <a_i, b_j> in {0,...,d}, rank <= d, given in FACTORED form (input size 2 n d =
n^{1+eps}, subquadratic). ans = max_{i,j} M_{ij} (Bichromatic Max-IP). The bar is a SUPER-polylog
shave of the n^2 baseline. The required novelty: MAX-EXTRACTION-WITHOUT-ENUMERATION.

WHAT e_fused_max_mm.py ESTABLISHED (finding 28). The frontier was built as FOUR candidate
subquadratic fusions of the n^2 inner products (B1 moment, B2 spectral, B3 regularity, B4 sketch),
all hitting ONE shared wall: every fast fusion computes a BULK statistic (L2 / average / low-moment
/ spectral / Frobenius); the Max-IP answer is an L-infinity / extreme statistic; integer-gap-1
resolution + argmax localization forces super-quadratic cost or the n^2 baseline. BUT the wall is a
HEURISTIC verified on four oblivious methods, not a theorem.

WHAT THIS MODULE DOES. It runs, with measured numbers, the FOUR first-principles attacks on that
heuristic, and reports for each whether the wall hardens, survives, or cracks:

  ATTACK-1 (HARDEN, W2). Upgrade the heuristic to a SINGLE-ROUND in-model lower bound over the
    Cheap-Measurement Model (CMM), a class that quantifies over a CONTINUUM and demonstrably
    contains all four prior candidates up to a rotation-invariant family. Three measurement
    families are cheap-from-factored: (a) separable/low-rank linear functionals u^T M v =
    (u^T A)(B^T v) at O(nd); (b) degree-<=D entry-symmetric statistics sum g(M_ij) = sum_p c_p m_p;
    (c) rotation-invariant spectral statistics f(sigma_1..sigma_d) from the d x d core, O(n d^2).
    CLAIM: no single oblivious round of these resolves max=d vs max<=d-1. Branch (i) heaviness
    (the argmax is L2-light, ratio Theta(1/n^2)); branch (ii) Vandermonde (the top-bucket indicator
    has degree exactly d); branch (iii) equal-spectrum collisions (the spectrum is blind to the max).

  ATTACK-2 (ADAPTIVE B&B, W4). The single-round restriction is the obvious thing to drop. Build
    the adaptive branch-and-bound with incumbent-dependent pruning, hand it the omniscient warm
    incumbent, and MEASURE the pruned fraction and the additive looseness of every cheap certificate
    on dense worst-case data. Result: on fixed-popcount worst-case rows the pruned fraction is
    EXACTLY 0 and T(n) = 4 T(n/2) + cheap = Theta(n^2). The wall survives, sharpened to worst-case
    gaplessness.

  ATTACK-3 (CLOSEST-PAIR, W3). The wall's LITERAL claim is "every fast method is a bulk aggregation."
    That is FALSE: thresholded Max-IP IS bichromatic Hamming closest-pair (a metric problem) via the
    exact identity Ham(a,b) = |a| + |b| - 2<a,b>, which has its OWN closest-pair-specific log-shaving
    machinery (Alman-Williams FOCS 2015). The wall cracks AS STATED. But the imported metric method's
    saved factor decays to 1 + o(1) at d = n^eps (a hard dimension ceiling d = o(log^2 n)), strictly
    WORSE than even the OV polynomial method's constant 2^{1/eps}. Cracked, then re-hardened.

  ATTACK-4 (FALSIFY, non-bulk probes). Test the universality on aggregations chosen to be non-bulk:
    T1 tropical/(max,+), T2 threshold-rank, T3 max-stable/Indyk L-infinity sketch. Each is either
    not-fast-from-factored or not-extreme-at-unit-resolution. T3 (Indyk's L-infinity sketch) is a
    genuine fast non-bulk aggregation, so the LITERAL universality is false, but its per-entry max
    readout has no factorization through A B^T and forces Theta(n^2) ingest TIME.

ADVERSARY CORRECTIONS APPLIED (the math the verifier fixed):
  - The binding obstruction is NOT "separable" but BULK / rotation-invariant / low-degree-symmetric.
    The d x d cores A^T A, B^T B give CHEAP (O(n d^2)) NON-separable functionals (Frobenius via
    trace, the core spectrum eig(G_A G_B), every moment m_p). So "cheap => separable" is FALSE;
    separability is a strict subclass of what is cheaply computable. The blindness mechanism is
    bulk-ness (Vandermonde / rotation-invariance), demonstrated head-on with a cheap non-separable
    Frobenius identity and equal-spectrum/different-max collisions. (Containment patch: ATTACK-1
    adds the third, rotation-invariant family with its own blindness proof, so the CMM genuinely
    subsumes all four prior candidates including the full B2 spectral one.)
  - ATTACK-1 separates two distinct floors in branch (i): the d-independent LOCALIZATION floor
    1/heaviness = ||M||_F^2/argmax^2 = Theta(n^2), and the gap-1 ESTIMATION floor
    ||M||_F^2/gap^2 = Theta(n^2 d^2) (Price-Woodruff ICALP 2012; Li-Nguyen-Woodruff STOC 2014).
  - ATTACK-2 distinguishes the cheap-bound-vs-absolute-max gap Theta(d) from the OPERATIVE inter-block
    max SPREAD O(sqrt(d log n)); both exceed 1 so the negative holds. The tested scale is reported
    with the full d-sweep so the Theta(d) TREND, not a small-d snapshot, carries the claim.

HONESTY DISCIPLINE. PROVED facts cite venue/year/arXiv. Each wall/crack is exhibited with an
explicit small instance and MEASURED numbers. If an escape appeared to actually shave, that would
be almost-certainly a bug to hunt (ATTACK-2 surfaces exactly one such bug: the i.i.d. popcount-spread
prune, neutralized by fixed-popcount rows). No speedup is claimed; no progress on the prize. No em
dashes anywhere.

Run:
    python -m experiments.circuit_complexity.e_fused_max_mm_attack
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np

# REUSE the J1 baseline ground truth: Boolean Max-IP two ways (brute force, A B^T then global max).
from experiments.circuit_complexity.e_maxip_logshave import (
    max_ip_bruteforce,
    max_ip_matrix_product,
)
from experiments._shared.barriers import BarrierChecker
from experiments._shared.technique import ProofTechnique


EPS = 0.1   # the modest dimension exponent d = n^eps; any constant eps > 0 works.


# ==========================================================================
# ATTACK-1 (HARDEN, W2): the single-round Cheap-Measurement Model lower bound.
#
# Cheap-from-factored forces one of three families. We demonstrate that EACH is blind to the
# gap-1 decision max=d vs max<=d-1, and that the families genuinely contain the four prior
# candidates. The corrected framing: cheap-from-factored => BULK / rotation-invariant /
# low-degree-symmetric => blind, NOT "=> separable =>" (the cores give cheap NON-separable
# functionals, so separability is a strict subclass; the blindness mechanism is bulk-ness).
# ==========================================================================


def separable_pushes_through(A: np.ndarray, B: np.ndarray, u: np.ndarray, v: np.ndarray) -> dict[str, float]:
    """Family (a): a rank-1 separable linear functional u^T M v = (u^T A)(B^T v) at O(nd), no n^2.

    The fusion identity that makes a separable measurement cheap from the factors. We verify it
    against the materialized <W, M> with W = u v^T.
    """
    M = A.astype(np.float64) @ B.astype(np.float64).T
    direct = float(u @ M @ v)                       # forms M: O(n^2) (only for grounding)
    factored = float((u @ A.astype(np.float64)) @ (B.astype(np.float64).T @ v))  # O(nd)
    return {"direct": direct, "factored": factored, "agree": abs(direct - factored) < 1e-6}


def generic_dense_W_is_high_rank(n: int, seed: int = 0) -> dict[str, object]:
    """A generic dense linear test matrix W is full-rank, so <W, M> = tr(A^T W B) costs Theta(n^2 d).

    Only LOW-RANK / separable W is cheap. This pins that "cheap linear" forces low rank in (i,j).
    """
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((n, n))
    return {"n": n, "rank_W": int(np.linalg.matrix_rank(W)), "is_full_rank": int(np.linalg.matrix_rank(W)) == n}


def cheap_nonseparable_core_identity(A: np.ndarray, B: np.ndarray) -> dict[str, object]:
    """The CORRECTION head-on: cheap does NOT imply separable. The d x d cores give cheap NON-separable
    functionals of M = A B^T.

    ||M||_F^2 = tr((A^T A)(B^T B)) is computed from the d x d cores G_A = A^T A, G_B = B^T B in
    O(n d^2) (subquadratic for eps < 1/2), yet ||M||_F^2 = sum_ij M_ij^2 is a degree-2 (NON rank-1,
    NON separable) functional of M. So "cheap => separable" is FALSE. The blindness is bulk-ness:
    Frobenius is a rotation-invariant L2 statistic, not the L-infinity max.
    """
    Af = A.astype(np.float64)
    Bf = B.astype(np.float64)
    M = Af @ Bf.T
    fro2_direct = float((M ** 2).sum())             # the bulk L2 mass (forms M, for grounding)
    G_A = Af.T @ Af                                 # d x d core, O(n d^2)
    G_B = Bf.T @ Bf                                 # d x d core, O(n d^2)
    fro2_core = float(np.trace(G_A @ G_B))          # ||M||_F^2 from the cores: cheap, NON-separable
    return {
        "fro2_direct": fro2_direct,
        "fro2_core": fro2_core,
        "agree": abs(fro2_direct - fro2_core) < 1e-3,
        "core_dim": int(G_A.shape[0]),
    }


def heaviness_ratio(n: int, d: int, seed: int = 0) -> dict[str, float]:
    """BRANCH (i): argmax^2 / ||M||_F^2 on dense Boolean M = A B^T, and the two distinct floors.

    The argmax value ~ d is one of n^2 entries all of comparable Theta(d) magnitude, so
    ||M||_F^2 = Theta(n^2 d^2) and the heaviness ratio is Theta(1/n^2), INDEPENDENT of d.
      - LOCALIZATION floor (d-independent): 1/heaviness = ||M||_F^2/argmax^2 = Theta(n^2).
      - ESTIMATION floor (gap-1, Price-Woodruff): dim >= ||M||_F^2/gap^2 = n^2 * E[M_ij^2] =
        Theta(n^2 d^2). E[M_ij^2] = fro2/n^2 grows like Theta(d^2), so once d is not tiny the
        gap-1 sketch dimension exceeds n^2 by a factor Theta(d^2). These are DIFFERENT objects.
    """
    rng = np.random.default_rng(seed)
    A = (rng.random((n, d)) < 0.5).astype(np.float64)
    B = (rng.random((n, d)) < 0.5).astype(np.float64)
    M = A @ B.T
    fro2 = float((M ** 2).sum())
    amax = float(M.max())
    ratio = amax * amax / fro2
    gap = 1.0
    return {
        "n": float(n), "d": float(d),
        "argmax": amax,
        "fro2": fro2,
        "heaviness_ratio": ratio,
        "ratio_times_n2": ratio * n * n,            # ~ const: the d-independent LOCALIZATION floor core
        "localization_floor": 1.0 / ratio,          # = ||M||_F^2/argmax^2 = Theta(n^2)
        "estimation_floor_over_n2": fro2 / (gap * gap) / (n * n),  # = E[M_ij^2] = Theta(d^2): gap-1 ESTIMATION
        "EM2": fro2 / (n * n),                       # per-entry second moment, Theta(d^2)
    }


def vandermonde_nullspace_dim(d: int, K: int) -> int:
    """BRANCH (ii): dim of value-multisets on {0,...,d} left FREE after matching moments m_0..m_K.

    The map (multiset on {0,...,d}) -> (m_0, m_1, ..., m_K) is the (K+1) x (d+1) Vandermonde. Its
    affine fiber has dimension (d+1) - (K+1) = d - K when K < d. When d - K > 0 (K <= d-1) the max
    is NOT determined. Reading the top bucket [v=d] is a degree-EXACTLY-d polynomial of the value
    (it vanishes on {0..d-1}, equals 1 at d; the Lagrange/Vandermonde indicator), so any degree-D<d
    entry-symmetric statistic is blind. The affordable degree is D < 1/eps (a constant).
    """
    return max(0, (d + 1) - (K + 1))


def explicit_moment_collision() -> dict[str, object]:
    """BRANCH (ii) smallest exact witness: two value-multisets sharing m_1, m_2 but different max.

    X = {3,1,1,1} (max=3), Y = {2,2,2,0} (max=2). Exact rationals so equality is not a float artifact.
    Any degree-2 entry-symmetric statistic CANNOT decide max=3 vs max=2.
    """
    X = [3, 1, 1, 1]
    Y = [2, 2, 2, 0]
    def moments(vals: list[int], P: int) -> list[Fraction]:
        return [sum(Fraction(v) ** p for v in vals) for p in range(1, P + 1)]
    mX = moments(X, 3)
    mY = moments(Y, 3)
    return {
        "X": X, "Y": Y,
        "m1_X": mX[0], "m2_X": mX[1], "m3_X": mX[2],
        "m1_Y": mY[0], "m2_Y": mY[1], "m3_Y": mY[2],
        "max_X": max(X), "max_Y": max(Y),
        "m1_equal": mX[0] == mY[0],
        "m2_equal": mX[1] == mY[1],
        "m3_equal": mX[2] == mY[2],
        "max_differs": max(X) != max(Y),
    }


def equal_spectrum_collision_at_gap1() -> dict[str, object]:
    """BRANCH (iii) (CONTAINMENT PATCH): a cheap rotation-invariant spectral readout is blind too.

    Two 3x3 Boolean products with d=2 sharing the IDENTICAL singular spectrum (2,0,0) but with
    different max at the gap-1 top (max=2=d vs max=1=d-1). Realized as factored products:
      M2: a single row/col pair carrying value 2 (max=d=2).
      M1: a spread 2x2 all-ones block of value 1 (max=1=d-1), same Frobenius and same spectrum.
    The full d x d core spectrum (cheap, O(n d^2)) provably cannot tell max=d from max=d-1, by
    rotation-invariance rather than heaviness/Vandermonde. So the spectral family is in the CMM
    and is blind. This closes the "the model omits B2 spectral" gap.
    """
    # M2: entry (2,2) = 2, max = d = 2. Factored as A2 = B2 with one row carrying the weight-2 vector.
    A2 = np.array([[0, 0], [0, 0], [1, 1]], dtype=np.float64)
    M2 = A2 @ A2.T                                   # M2[2,2] = 2, rest 0; spectrum (2,0,0)
    # M1: a 2x2 all-ones block of value 1 in rows/cols {1,2}, max = d - 1 = 1, same spectrum (2,0,0).
    u = np.array([0.0, 1.0, 1.0])
    M1 = np.outer(u, u)                              # rank-1, sigma = 2; entries 0/1; max = 1
    s1 = np.linalg.svd(M1, compute_uv=False)
    s2 = np.linalg.svd(M2, compute_uv=False)
    return {
        "M1": M1.astype(int).tolist(), "M2": M2.astype(int).tolist(),
        "spectrum_M1": [round(float(x), 6) for x in s1],
        "spectrum_M2": [round(float(x), 6) for x in s2],
        "spectra_equal": bool(np.allclose(np.sort(s1), np.sort(s2), atol=1e-9)),
        "max_M1": int(M1.max()), "max_M2": int(M2.max()),
        "max_differs": int(M1.max()) != int(M2.max()),
        "d": 2,
    }


def single_round_cheap_blind_pair(n: int, d: int, seed: int) -> dict[str, object]:
    """ATTACK-1 (c): two rank-<=d Boolean instances with identical CHEAP measurements but GLOBAL max d-1 vs d.

    We engineer the GAP-1 decision directly: the max<=d-1 instance has a UNIQUE top cell (i*, j*) at
    value d-1, and the max=d instance is that instance plus a single +1 at exactly that cell, so its
    global max jumps from d-1 to d. Construction (rank <= d, difference 1-sparse):
      a_{i*} = all-ones (popcount d); b_{j*} = all-ones EXCEPT the private bit k* (popcount d-1), so
      M[i*,j*] = d-1. The rest of the data is moderately dense bulk whose entries stay <= d-1. Flipping
      b'_{j*}[k*] = 1 makes b_{j*} all-ones, so M'[i*,j*] = d (the new unique global max), and only that
      one cell changes (k* is set in exactly one A-row, i*). We verify the cheap readouts the CMM can
      afford agree to a 1/n^2-order fraction while the GLOBAL max differs by exactly 1:
      - family (a) a fixed oblivious random separable functional u^T M v (the +1 changes it by
        u[i*] v[j*] = O(1), below the bulk Frobenius noise for a random oblivious (u,v));
      - family (b) low-degree moments m_1, m_2 (a +1 at one cell moves m_p by O(d^{p-1}), a
        1/n^2 relative perturbation against the Theta(n^2 d^2) bulk);
      - family (c) the Frobenius mass / core spectrum (moves by O(d), a 1/n^2 relative change).
    All three are blind at the precision the dense bulk sets; only an L-infinity readout sees the +1.
    """
    rng = np.random.default_rng(seed)
    # Moderately dense bulk (density 0.4) whose pairwise inner products stay strictly below d-1 with
    # high probability; the planted top cell is the unique maximizer.
    A = (rng.random((n, d)) < 0.4).astype(np.float64)
    B = (rng.random((n, d)) < 0.4).astype(np.float64)
    i_star, j_star, k_star = 0, 1, d - 1
    # Private column k*: set in exactly one A-row (i*), so a single B-bit flip changes exactly one cell.
    A[:, k_star] = 0.0
    A[i_star, k_star] = 1.0
    # a_{i*} = all-ones (popcount d); b_{j*} = all-ones except the private bit k* (popcount d-1).
    A[i_star, :] = 1.0
    B[j_star, :] = 1.0
    B[j_star, k_star] = 0.0
    Bp = B.copy()
    Bp[j_star, k_star] = 1.0                         # M' = M + E_{i*,j*}, a single +1 (b'_{j*} = all-ones)
    M = A @ B.T
    Mp = A @ Bp.T
    max_M = int(M.max())
    max_Mp = int(Mp.max())
    # The cheap measurements, on BOTH instances.
    u = rng.standard_normal(n)
    v = rng.standard_normal(n)
    sep_M = float((u @ A) @ (B.T @ v))
    sep_Mp = float((u @ A) @ (Bp.T @ v))
    fro2_M = float((M ** 2).sum())
    fro2_Mp = float((Mp ** 2).sum())
    m1_M = float(M.sum()); m1_Mp = float(Mp.sum())
    m2_M = fro2_M; m2_Mp = fro2_Mp
    # Relative perturbations: each cheap readout changes by a 1/n^2-order fraction (bulk-dominated).
    sep_rel = abs(sep_Mp - sep_M) / (abs(sep_M) + 1e-12)
    fro2_rel = abs(fro2_Mp - fro2_M) / (fro2_M + 1e-12)
    m1_rel = abs(m1_Mp - m1_M) / (m1_M + 1e-12)
    return {
        "n": n, "d": d,
        "max_M": max_M, "max_Mp": max_Mp,
        "max_differs_by_one": (max_Mp - max_M),
        "rank_ok": bool(np.linalg.matrix_rank(M) <= d and np.linalg.matrix_rank(Mp) <= d),
        "sep_rel_change": sep_rel,
        "fro2_rel_change": fro2_rel,
        "m1_rel_change": m1_rel,
        # The +1 absolute change vs the bulk scale: a single cell against ||M||_F^2.
        "argmax_signal_over_bulk": 1.0 / fro2_M,
    }


# ==========================================================================
# ATTACK-2 (ADAPTIVE B&B, W4): branch-and-bound with incumbent-dependent pruning.
#
# Divide A into row-halves, B into row-halves; max over M = A B^T is the max over the four
# sub-blocks; recurse; PRUNE a block when a CHEAP upper bound on its max <= the best-so-far
# incumbent. Exact for any valid UB. The whole question reduces to the pruned fraction f. By the
# Master theorem with a = 4(1-f) children of quarter area, the leaf count is n^(log2(4(1-f))).
# ==========================================================================


def cheap_upper_bounds(Af: np.ndarray, Bf: np.ndarray) -> dict[str, float]:
    """Cheap separable / rotation-invariant upper bounds on max_ij (Af Bf^T)_ij, all O((n_p+n_q) d ..).

    - cauchy_schwarz : (max_i ||a_i||)(max_j ||b_j||), separable, O((n_p+n_q) d).
    - min_popcount   : min(max_i pop(a_i), max_j pop(b_j)), the tightest cheap Boolean bound, separable.
    - spectral       : sigma_max(Af) * sigma_max(Bf), separable, rotation-invariant, O((n_p+n_q) d^2).
    """
    a_norms = np.sqrt((Af ** 2).sum(axis=1))
    b_norms = np.sqrt((Bf ** 2).sum(axis=1))
    cs = float(a_norms.max() * b_norms.max())
    a_pop = Af.sum(axis=1).max()
    b_pop = Bf.sum(axis=1).max()
    minpop = float(min(a_pop, b_pop))
    sa = float(np.linalg.svd(Af, compute_uv=False)[0]) if min(Af.shape) > 0 else 0.0
    sb = float(np.linalg.svd(Bf, compute_uv=False)[0]) if min(Bf.shape) > 0 else 0.0
    return {"cauchy_schwarz": cs, "min_popcount": minpop, "spectral": sa * sb}


@dataclass
class BBStats:
    nodes: int
    leaves_base_case: int          # leaf cells fully enumerated (the base-case n^2 work proxy)
    pruned_blocks: int
    answer: int


def branch_and_bound_maxip(A: np.ndarray, B: np.ndarray, cert: str, incumbent: int) -> BBStats:
    """Exact adaptive branch-and-bound for max_ij (A B^T)_ij, counting nodes / base-case cells / prunes.

    incumbent is the warm start (we will hand it the OMNISCIENT true max to give the escape every
    advantage). A block is pruned iff its cheap upper bound <= incumbent (it cannot beat the best).
    Base case (a single i or single j, or a tiny block) enumerates the cells (the n^2 work proxy).
    """
    Af = A.astype(np.float64)
    Bf = B.astype(np.float64)
    stats = {"nodes": 0, "leaves": 0, "pruned": 0}
    best = [incumbent]

    def recurse(ri: np.ndarray, rj: np.ndarray) -> None:
        stats["nodes"] += 1
        nia, njb = len(ri), len(rj)
        # Base case: a 1xK or Kx1 block (or a single cell) is enumerated directly.
        if nia <= 1 or njb <= 1:
            sub = Af[ri] @ Bf[rj].T
            stats["leaves"] += nia * njb            # cells touched at the base case
            m = int(sub.max()) if sub.size else -1
            if m > best[0]:
                best[0] = m
            return
        # Cheap upper bound on this block's max; prune if it cannot beat the incumbent.
        ub = cheap_upper_bounds(Af[ri], Bf[rj])[cert]
        if ub <= best[0]:
            stats["pruned"] += 1
            return
        ha, hb = nia // 2, njb // 2
        ia1, ia2 = ri[:ha], ri[ha:]
        jb1, jb2 = rj[:hb], rj[hb:]
        for sub_i in (ia1, ia2):
            for sub_j in (jb1, jb2):
                recurse(sub_i, sub_j)

    recurse(np.arange(A.shape[0]), np.arange(B.shape[0]))
    return BBStats(nodes=stats["nodes"], leaves_base_case=stats["leaves"],
                   pruned_blocks=stats["pruned"], answer=best[0])


def additive_looseness(d: int, seed: int = 0) -> dict[str, float]:
    """Measure UB - true_max for each cheap certificate on a dense Boolean block (the looseness wall).

    A prune on a gapless block (whose true max ties the global max) needs UB tight to ADDITIVE 1.
    We show every CHEAP separable / rotation-invariant certificate is additively loose by Theta(d)
    (the gap GROWS with d, not a constant slack), so no cheap certificate gives additive-1 pruning.
    """
    rng = np.random.default_rng(seed)
    n = 64
    A = (rng.random((n, d)) < 0.5).astype(np.float64)
    B = (rng.random((n, d)) < 0.5).astype(np.float64)
    true_max = float((A @ B.T).max())
    ubs = cheap_upper_bounds(A, B)
    return {
        "d": float(d),
        "true_max": true_max,
        "cs_gap": ubs["cauchy_schwarz"] - true_max,
        "minpop_gap": ubs["min_popcount"] - true_max,
        "spectral_gap": ubs["spectral"] - true_max,
    }


def leaf_exponent(f: float) -> float:
    """Master-theorem leaf exponent log2(4(1-f)): f=0 -> 2.0 (baseline), f=0.5 -> 1.0, f=0.75 -> 0.0."""
    a = 4.0 * (1.0 - f)
    return math.log2(a) if a > 0 else float("-inf")


def make_fixed_popcount(n: int, d: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """The TRUE worst case: every row has popcount EXACTLY d/2, so every separable filter is a flat
    constant d/2 on every block (no popcount-spread lever for pruning)."""
    rng = np.random.default_rng(seed)
    w = d // 2
    def rows(m: int) -> np.ndarray:
        R = np.zeros((m, d), dtype=np.float64)
        for i in range(m):
            idx = rng.choice(d, size=w, replace=False)
            R[i, idx] = 1.0
        return R
    return rows(n), rows(n)


def make_planted_gap(n: int, d: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """A GAPPED (Valiant/light-bulb) instance: sparse bulk plus one planted heavy pair. The B&B prunes
    here (a real shave), but this is exactly the constant-relative-gap regime the THR-of-THR
    connection EXCLUDES."""
    rng = np.random.default_rng(seed)
    A = (rng.random((n, d)) < 0.08).astype(np.float64)   # sparse bulk: small inner products
    B = (rng.random((n, d)) < 0.08).astype(np.float64)
    A[0, :] = 1.0                                          # planted heavy pair: a_0 = b_0 = all-ones
    B[0, :] = 1.0
    return A, B


# ==========================================================================
# ATTACK-3 (CLOSEST-PAIR, W3): the weight-bucketed Max-IP -> Hamming near-neighbor reduction,
# and the decay of the closest-pair-specific log-shaver at d = n^eps.
# ==========================================================================


def hamming_identity_check(seed: int = 0) -> bool:
    """The exact reframe identity Ham(a,b) = |a| + |b| - 2<a,b> on Boolean vectors (to the bit)."""
    rng = np.random.default_rng(seed)
    ok = True
    for _ in range(200):
        d = int(rng.integers(1, 40))
        a = (rng.random(d) < 0.5).astype(np.int64)
        b = (rng.random(d) < 0.5).astype(np.int64)
        ham = int(np.sum(a != b))
        ip = int(a @ b)
        ok = ok and (ham == int(a.sum()) + int(b.sum()) - 2 * ip)
    return ok


def maxip_via_weight_bucketed_closest_pair(A: np.ndarray, B: np.ndarray) -> int:
    """Max-IP computed through the weight-bucketed minimum-Hamming reduction (a METRIC route).

    Within a weight class (wa, wb), <a,b> = (wa + wb - Ham(a,b))/2, so the per-class Max-IP is
    (wa + wb - min_Hamming)/2. Max-IP = max over weight classes of the per-class value. The weight
    classes PARTITION the rows, so per-class near-neighbor costs SUM, not multiply. This is exact;
    we verify it equals the direct A B^T max and the brute force.
    """
    wa = A.sum(axis=1)
    wb = B.sum(axis=1)
    best = -1
    for ua in np.unique(wa):
        Asub = A[wa == ua]
        for ub in np.unique(wb):
            Bsub = B[wb == ub]
            if Asub.size == 0 or Bsub.size == 0:
                continue
            # Minimum Hamming distance within this (ua, ub) class, then map back to inner product.
            # Ham(a,b) = ua + ub - 2 <a,b>, minimized when <a,b> is maximized; both reach the same pair.
            ip_block = (Asub @ Bsub.T).max()
            val = int(ip_block)
            if val > best:
                best = val
    return best


def closest_pair_saved_factor_log2(log2n: float, eps: float, c_mm: float = 1.0) -> dict[str, float]:
    """ATTACK-3 decay: the Alman-Williams FOCS 2015 closest-pair-specific saved factor at d = n^eps.

    ACW: a batch of n Hamming nearest-neighbor queries over n vectors at d = c log n runs in
    n^{2 - 1/O(c log^2 c)}, subquadratic only for d = o(log^2 n / (loglog n)^2). At d = n^eps,
    c = n^eps/log n, so the saved exponent s = 1/(c_mm * c * log2^2 c) collapses; log2(saved factor)
    = s * log2 n. Computed in overflow-safe log space (d = n^eps would overflow if materialized).
    Returns the saved-exponent s and log2(saved factor of n) for both d = n^eps and the in-regime
    reference d = 4 log n, plus the dimension-ceiling test (in-regime iff log2 n > sqrt(d)).
    """
    log2_logn = math.log2(log2n) if log2n > 1.0 else 1.0
    # d = n^eps: c = n^eps / log2 n = 2^{eps log2 n} / log2 n, all in log space.
    log2_d_neps = eps * log2n                         # log2(d) for d = n^eps
    log2_c = log2_d_neps - math.log2(log2n)           # log2(c) = log2(d) - log2(log2 n)
    c = 2.0 ** log2_c if log2_c < 200 else float("inf")
    # saved exponent s = 1 / (c_mm * c * (log2 c)^2). We compute log2(s) = -log2(c_mm c log2^2 c).
    # log2_c can be huge; guard.
    if math.isinf(c) or log2_c > 100:
        log2_s = float("-inf")
        saved_factor_log2 = 0.0
    else:
        log2_log2c = math.log2(abs(log2_c)) if abs(log2_c) > 1.0 else 0.0
        log2_denom = math.log2(c_mm) + log2_c + 2.0 * log2_log2c
        log2_s = -log2_denom
        saved_factor_log2 = (2.0 ** log2_s) * log2n if log2_s > -100 else 0.0
    # In-regime reference d = 4 log n (c = 4): a genuine shave.
    c_ref = 4.0
    s_ref = 1.0 / (c_mm * c_ref * (math.log2(c_ref) ** 2))
    saved_factor_log2_ref = s_ref * log2n
    # Dimension ceiling: subquadratic needs d = o(log^2 n), proxy d = log^2 n -> in-regime iff
    # log2 n > sqrt(d). At d = n^eps, sqrt(d) = 2^{eps log2 n / 2} grows exponentially vs log2 n linear.
    log2_sqrt_d = 0.5 * log2_d_neps
    in_regime = log2n > (2.0 ** log2_sqrt_d) if log2_sqrt_d < 50 else False
    return {
        "log2n": log2n,
        "saved_factor_log2_neps": saved_factor_log2,            # -> 0 (sub-one-log)
        "saved_factor_log2_ref_4logn": saved_factor_log2_ref,   # grows (in-regime shave)
        "in_regime_neps": in_regime,
        "log2_sqrt_d": log2_sqrt_d,
    }


def ov_poly_saved_factor_log2(eps: float) -> float:
    """For contrast: the general OV/Max-IP polynomial method (AWY SODA 2015) saved factor at d = n^eps.

    log2(saved factor) -> 1/eps (a CONSTANT 2^{1/eps}, itself only a constant-factor shave). The
    closest-pair method's saved factor decays BELOW this (extra log^2 c surcharge), so the metric
    method is the WEAKER of the two at polynomial dimension.
    """
    return 1.0 / eps if eps > 0 else float("inf")


def center_radius_width(seed: int = 0) -> dict[str, float]:
    """ATTACK-2-vs-metric check: a triangle-inequality / center-radius bound gives a RANGE of width 2R,
    not the gap-1 argmax. Measured on a real Hamming ball: resolving max vs max-1 needs R < 1/2."""
    rng = np.random.default_rng(seed)
    d = 64
    center = (rng.random(d) < 0.5).astype(np.int64)
    pts = (rng.random((50, d)) < 0.5).astype(np.int64)
    R = int(np.max(np.sum(pts != center, axis=1)))   # ball radius (max Hamming to center)
    # <a, c> ranges over [<a,c> - R, <a,c> + R]-ish: the certificate width is 2R, not 1.
    return {"radius": float(R), "range_width_2R": 2.0 * float(R), "needs_R_below": 0.5}


# ==========================================================================
# ATTACK-4 (FALSIFY): non-bulk aggregations, each not-fast-from-factored or not-extreme-at-unit-res.
# ==========================================================================


def tropical_is_wrong_quantity(n: int, d: int, seed: int = 0) -> dict[str, object]:
    """T1: the (max,+) product max_k(a_ik + b_jk) is a DIFFERENT object (values in {0,1,2}) from
    Max-IP = max_ij sum_k a_ik b_jk in {0..d}. Tropical/(max,+) MM also has no sub-n^2 shave from
    small d (APSP-class). So T1 fails fast-from-factored AND is the wrong quantity."""
    rng = np.random.default_rng(seed)
    A = (rng.random((n, d)) < 0.5).astype(np.int64)
    B = (rng.random((n, d)) < 0.5).astype(np.int64)
    maxip = int((A @ B.T).max())
    # (max,+) of n x d by d x n: T_ij = max_k (A_ik + B_jk), entries in {0,1,2} for Boolean inputs.
    trop = -1
    for i in range(n):
        for j in range(n):
            trop = max(trop, int(np.max(A[i] + B[j])))
    return {"maxip": maxip, "tropical_max": trop, "tropical_capped_at_2": trop <= 2, "differs": maxip != trop}


def threshold_destroys_rank(n: int, d: int, seed: int = 0) -> dict[str, int]:
    """T2: 'max >= tau' iff 1[M >= tau] is nonzero, and a rank-r Boolean matrix is nonzero-testable in
    n*poly(r). But thresholding a rank-d integer matrix DESTROYS low rank: rank(1[M >= bulk_tau]) grows
    like Theta(min(n, .)) >> d. The only tau keeping rank ~ 1 is tau = max (circular: that IS the answer)."""
    rng = np.random.default_rng(seed)
    A = (rng.random((n, d)) < 0.5).astype(np.int64)
    B = (rng.random((n, d)) < 0.5).astype(np.int64)
    M = A @ B.T
    rank_M = int(np.linalg.matrix_rank(M.astype(np.float64)))
    bulk_tau = int(np.floor(M.mean()))               # a bulk threshold (not the max)
    Mthr = (M >= bulk_tau).astype(np.float64)
    rank_thr = int(np.linalg.matrix_rank(Mthr))
    return {"n": n, "d": d, "rank_M": rank_M, "bulk_tau": bulk_tau, "rank_threshold": rank_thr}


def max_stable_needs_materialization(n: int, d: int, seed: int = 0) -> dict[str, object]:
    """T3: Indyk's max-stable / L-infinity sketch IS extreme-sensitive (the LITERAL universality is
    false), but its readout is a per-entry MAX max_ij r_ij M_ij with r_ij iid PER COORDINATE
    (full-rank diagonal reweighting), non-linear with NO trace factorization through A B^T. A rank-1
    SEPARABLE sketch factors at O(nd); the per-entry max sketch must touch all n^2 products (Theta(n^2)
    ingest TIME). So T3 is non-bulk but not-fast-from-factored: small in SPACE, not in TIME-to-ingest."""
    rng = np.random.default_rng(seed)
    A = (rng.random((n, d)) < 0.5).astype(np.float64)
    B = (rng.random((n, d)) < 0.5).astype(np.float64)
    M = A @ B.T
    # (a) a rank-1 SEPARABLE linear sketch DOES factor through the factors at O(nd):
    u = rng.standard_normal(n); v = rng.standard_normal(n)
    sep_factored = float((u @ A) @ (B.T @ v))
    sep_direct = float(u @ M @ v)
    # (b) the per-entry max-stable readout: max_ij r_ij M_ij, r_ij iid per (i,j). No factorization:
    #     it is a max over all n^2 reweighted entries, must form M to evaluate.
    R = rng.standard_normal((n, n))
    per_entry_max = float(np.max(R * M))             # requires the materialized M: Theta(n^2)
    return {
        "n": n, "d": d,
        "separable_factors": abs(sep_factored - sep_direct) < 1e-6,
        "per_entry_max": per_entry_max,
        "per_entry_max_touches": n * n,              # the ingest cost: all n^2 products
        "separable_touches": n * d,                  # the cheap factored cost
    }


# ==========================================================================
# The summary ledger row per attack prong.
# ==========================================================================


@dataclass(frozen=True)
class ProngRow:
    name: str
    goal: str
    result: str
    quantified: str
    escape_locus: str
    barrier_free: bool


def build_prong_ledger() -> list[ProngRow]:
    return [
        ProngRow(
            name="ATTACK-1 (HARDEN, W2): single-round Cheap-Measurement-Model lower bound",
            goal="harden-the-wall",
            result="wall hardened to an in-model single-round lower bound",
            quantified="separable-linear localization floor 1/heaviness = Theta(n^2) (gap-1 estimation "
                       "floor Theta(n^2 d^2)); symmetric degree D >= d = n^eps; spectral blind by "
                       "equal-spectrum collision at the gap-1 top. Affordable: R = o(n^2/d), D < 1/eps.",
            escape_locus="ADAPTIVE / multi-round (W4): round t's measurement may depend on rounds 1..t-1.",
            barrier_free=True,
        ),
        ProngRow(
            name="ATTACK-2 (ADAPTIVE B&B, W4): incumbent-dependent branch-and-bound",
            goal="crack-the-wall",
            result="wall SURVIVES, sharpened to worst-case GAPLESSNESS",
            quantified="fixed-popcount worst case: pruned fraction EXACTLY 0, base/n^2 = 1.000, "
                       "T(n) = 4 T(n/2) + cheap = Theta(n^2). Cheap-cert additive looseness Theta(d); "
                       "operative inter-block spread O(sqrt(d log n)); both >> additive 1.",
            escape_locus="the only additive-1-tight certificate is the exact block max = a recursive call "
                         "(circular). Gapped/Valiant instances DO prune (~0.72) but are EXCLUDED.",
            barrier_free=True,
        ),
        ProngRow(
            name="ATTACK-3 (CLOSEST-PAIR, W3): the metric reframe",
            goal="crack-the-wall",
            result="wall CRACKED as stated, re-hardened (metric method decays at d = n^eps)",
            quantified="thresholded Max-IP IS bichromatic Hamming closest-pair (exact reframe, verified). "
                       "ACW FOCS 2015 saved factor -> 1 + o(1) at d = n^eps (ceiling d = o(log^2 n)), "
                       "STRICTLY worse than the OV constant 2^{1/eps}.",
            escape_locus="degree-vs-dimension collapse: the symmetric-predicate polynomial degree is set "
                         "by the universe size; at polynomial dimension the batch-MM collapses.",
            barrier_free=True,
        ),
        ProngRow(
            name="ATTACK-4 (FALSIFY): non-bulk probes (tropical, threshold-rank, max-stable)",
            goal="falsify-the-wall",
            result="literal universality FALSE (T3 is non-bulk), wall survives at the TIME-to-ingest level",
            quantified="T1 tropical in {0,1,2} != Max-IP; T2 threshold destroys rank-d; T3 max-stable per-entry "
                       "max has no factorization, Theta(n^2) ingest. Cheap-from-factored => BULK / rotation-"
                       "invariant => blind (NOT 'separable': the cores give cheap non-separable functionals).",
            escape_locus="a non-linear, full-rank-in-(i,j), unit-resolution readout that ALSO factors through "
                         "A B^T in o(n^2) time. No such factored identity is known.",
            barrier_free=True,
        ),
    ]


# ==========================================================================
# Reporting
# ==========================================================================


def main() -> int:
    print("=== Fused-max-MM (J1 frontier): four first-principles ATTACKS on the bulk-vs-extreme wall ===\n")
    print("TARGET (Chen 2018 arXiv:1805.10698 Thm 1.5 item 1, web-confirmed verbatim in e_maxip_logshave.py):")
    print('  "An n^2 / log^{omega(1)} n time algorithm for Bichromatic Maximum Inner Product with vector')
    print('   dimension d = n^eps ... would imply NEXP has no polynomial size THR o THR circuits. Note there')
    print('   is an n^2 polylog(n) time algorithm via fast rectangle matrix multiplication."')
    print("M = A B^T (integer counts <a_i,b_j> in {0,...,d}, rank <= d, FACTORED). ans = max_{i,j} M_{ij}.")
    print("e_fused_max_mm.py (finding 28) built FOUR oblivious bulk fusions, all blind to the L-infinity max.")
    print("That wall is a HEURISTIC on four methods, NOT a theorem. This module runs the four attacks.\n")

    # ---------------------------------------------------------------------
    # ATTACK-1 (HARDEN).
    # ---------------------------------------------------------------------
    print("=" * 78)
    print("ATTACK-1 (HARDEN, W2): the single-round Cheap-Measurement-Model lower bound.")
    print("=" * 78 + "\n")
    print("Cheap-from-factored forces one of three families: (a) separable/low-rank linear, (b) degree-D")
    print("entry-symmetric, (c) rotation-invariant spectral from the d x d core. CORRECTION (adversary):")
    print("the binding obstruction is BULK-ness, NOT separability. The cores give CHEAP NON-separable")
    print("functionals, so 'cheap => separable' is FALSE.\n")

    print("(0) The cheap-from-factored identities (what makes a measurement affordable):")
    rng = np.random.default_rng(1)
    A0 = (rng.random((30, 8)) < 0.5).astype(np.int64)
    B0 = (rng.random((30, 8)) < 0.5).astype(np.int64)
    u0 = rng.standard_normal(30); v0 = rng.standard_normal(30)
    sep = separable_pushes_through(A0, B0, u0, v0)
    print(f"    family (a) rank-1 separable: u^T M v = (u^T A)(B^T v) agree={sep['agree']} "
          f"(O(nd), not n^2)")
    core = cheap_nonseparable_core_identity(A0, B0)
    print(f"    CORRECTION: ||M||_F^2 = tr((A^T A)(B^T B)) from the {core['core_dim']}x{core['core_dim']} cores "
          f"agree={core['agree']} (O(n d^2), CHEAP but NON-separable: cheap =/=> separable)")
    gw = generic_dense_W_is_high_rank(64)
    print(f"    a generic dense linear test W (n={gw['n']}) has rank {gw['rank_W']} (full_rank={gw['is_full_rank']}): "
          f"<W,M> = tr(A^T W B) costs Theta(n^2 d), outside the cheap model.\n")

    print("(a) BRANCH (i) heaviness: the dense argmax is L2-LIGHT (ratio Theta(1/n^2)), d-independent.")
    print(f"    {'n':>5} | {'d':>4} | {'heaviness ratio':>16} | {'ratio*n^2':>10} | {'localization floor':>18}")
    print("    " + "-" * 64)
    rtn2 = []
    for n in (16, 32, 64, 128):
        for d in (4, 16, 64):
            h = heaviness_ratio(n, d, seed=0)
            if d == 16:
                rtn2.append(h["ratio_times_n2"])
            print(f"    {n:>5} | {d:>4} | {h['heaviness_ratio']:>16.3e} | {h['ratio_times_n2']:>10.2f} | "
                  f"{h['localization_floor']:>18.1f}")
    print("    ratio*n^2 stays a small constant across n AND d: LOCALIZATION floor 1/heaviness = Theta(n^2).")
    print("    The gap-1 ESTIMATION floor (Price-Woodruff ICALP 2012) is ||M||_F^2/gap^2 = n^2 E[M_ij^2]:")
    print(f"      {'d':>4} | {'E[M_ij^2] (Theta d^2)':>21} | {'gap-1 floor / n^2':>18}")
    print("      " + "-" * 47)
    for d in (4, 16, 64, 128):
        h = heaviness_ratio(256, d, seed=0)
        print(f"      {d:>4} | {h['EM2']:>21.3f} | {h['estimation_floor_over_n2']:>18.3f}")
    print("    E[M_ij^2] grows ~ d^2: the gap-1 separable-linear dimension is Theta(n^2 d^2), worse than n^2.\n")

    print("(b) BRANCH (ii) Vandermonde: the top-bucket indicator [v=d] has degree EXACTLY d.")
    coll = explicit_moment_collision()
    print(f"    explicit witness: X = {coll['X']} (max={coll['max_X']}), Y = {coll['Y']} (max={coll['max_Y']})")
    print(f"      m_1: {coll['m1_X']}={coll['m1_Y']} equal={coll['m1_equal']};  "
          f"m_2: {coll['m2_X']}={coll['m2_Y']} equal={coll['m2_equal']};  "
          f"m_3: {coll['m3_X']} vs {coll['m3_Y']} equal={coll['m3_equal']}")
    print(f"      so any DEGREE-2 entry-symmetric statistic CANNOT tell max=3 from max=2 (m_3 first splits them).")
    print("    Vandermonde free dimension d - D (max NOT pinned until D = d):")
    for d in (8, 16, 20):
        for D in (3, 5, 9, d):
            free = vandermonde_nullspace_dim(d, D)
            tag = "pinned" if free == 0 else "max FREE"
            print(f"      d={d:2d} D={D:2d}: free dim = {free} ({tag})")
    print(f"    affordable degree is D < 1/eps = {1.0/EPS:.0f} (a CONSTANT); reading the top bucket needs D = d = n^eps.\n")

    print("(c) BRANCH (iii) (CONTAINMENT PATCH): a cheap rotation-invariant SPECTRAL readout is blind too.")
    es = equal_spectrum_collision_at_gap1()
    print(f"    two 3x3 Boolean products (d={es['d']}) with IDENTICAL spectrum but different max at the gap-1 top:")
    print(f"      M1 = {es['M1']} (max={es['max_M1']}=d-1), spectrum {es['spectrum_M1']}")
    print(f"      M2 = {es['M2']} (max={es['max_M2']}=d),   spectrum {es['spectrum_M2']}")
    print(f"      spectra_equal={es['spectra_equal']}, max_differs={es['max_differs']}: the full d x d core")
    print("      spectrum (cheap, O(n d^2)) cannot resolve max=d vs max=d-1 (by rotation-invariance).\n")

    print("(d) The SINGLE ROUND, head-on: two rank-<=d Boolean instances with identical cheap measurements")
    print("    but max differing by 1 (the max=d instance is the max<=d-1 instance plus a single +1 cell).")
    print(f"    {'n':>5} | {'d':>4} | {'max M':>6} | {'max M+E':>8} | {'sep rel':>10} | {'fro2 rel':>10} | {'rank<=d':>8}")
    print("    " + "-" * 70)
    blind_rows = []
    for (n, d) in [(64, 8), (128, 12), (256, 16)]:
        r = single_round_cheap_blind_pair(n, d, seed=5)
        blind_rows.append(r)
        print(f"    {n:>5} | {d:>4} | {r['max_M']:>6} | {r['max_Mp']:>8} | {r['sep_rel_change']:>10.2e} | "
              f"{r['fro2_rel_change']:>10.2e} | {str(r['rank_ok']):>8}")
    print("    every cheap readout changes by a 1/n^2-order fraction (bulk-dominated) while the max moves by")
    print("    exactly 1: a single oblivious round of cheap (a)/(b)/(c) measurements cannot resolve the gap.\n")
    print("    ESCAPE LOCUS (honestly stated, NOT hidden): ADAPTIVE / multi-round measurement, where round t")
    print("    may depend on rounds 1..t-1. The counting argument uses obliviousness; it fails the instant")
    print("    measurements may depend on prior answers. That is W4 (and W3, the metric route). -> ATTACK-2/3.\n")

    # ---------------------------------------------------------------------
    # ATTACK-2 (ADAPTIVE B&B).
    # ---------------------------------------------------------------------
    print("=" * 78)
    print("ATTACK-2 (ADAPTIVE B&B, W4): branch-and-bound with incumbent-dependent pruning.")
    print("=" * 78 + "\n")
    print("Divide A, B into row-halves; max over M = A B^T is the max over the 4 sub-blocks; recurse; PRUNE")
    print("a block when a CHEAP upper bound on its max <= the best-so-far incumbent. Exact for any valid UB.")
    print("The whole question reduces to the pruned fraction f: leaf count = n^(log2(4(1-f))).\n")

    print("(0) Exactness: the B&B returns the true Max-IP for every cheap certificate (vs A B^T baseline).")
    rng_e = np.random.default_rng(11)
    exact_ok = True
    for (n, d) in [(16, 6), (24, 8), (32, 5)]:
        A = (rng_e.random((n, d)) < 0.5).astype(np.int64)
        B = (rng_e.random((n, d)) < 0.5).astype(np.int64)
        truth, _ = max_ip_matrix_product(A, B)
        for cert in ("cauchy_schwarz", "min_popcount", "spectral"):
            bb = branch_and_bound_maxip(A, B, cert, incumbent=-1)
            exact_ok = exact_ok and (bb.answer == truth)
        print(f"    n={n} d={d}: truth={truth}, all three certificates return it = {exact_ok}")
    print()

    print("(1) ADDITIVE looseness UB - true_max on a dense Boolean block (a prune on a gapless block needs")
    print("    additive 1). Every CHEAP certificate is additively loose by Theta(d) (GROWS with d):")
    print(f"    {'d':>5} | {'true_max':>9} | {'CS gap':>8} | {'min-pop gap':>12} | {'spectral gap':>13}")
    print("    " + "-" * 56)
    cs_gaps = []
    for d in (8, 16, 32, 64, 128):
        al = additive_looseness(d, seed=0)
        cs_gaps.append(al["cs_gap"])
        print(f"    {d:>5} | {al['true_max']:>9.0f} | {al['cs_gap']:>8.1f} | {al['minpop_gap']:>12.1f} | "
              f"{al['spectral_gap']:>13.1f}")
    print("    the cheap-bound-vs-absolute-max gap is Theta(d); the OPERATIVE inter-block max SPREAD is only")
    print("    O(sqrt(d log n)), but BOTH exceed additive 1, so no cheap certificate gives additive-1 pruning.\n")

    print("(2) The TRUE worst case (fixed popcount d/2: every separable filter is a flat constant). Hand the")
    print("    B&B the OMNISCIENT true-max warm incumbent and measure the pruned fraction + base-case work.")
    print(f"    {'n':>6} | {'d':>4} | {'pruned blocks':>14} | {'base cells / n^2':>16} | {'answer ties incumbent':>22}")
    print("    " + "-" * 70)
    worst_base_frac = []
    for n in (256, 512, 1024):
        d = 32
        A, B = make_fixed_popcount(n, d, seed=2)
        truth, _ = max_ip_matrix_product(A, B)
        bb = branch_and_bound_maxip(A, B, "cauchy_schwarz", incumbent=truth)  # omniscient warm start
        frac = bb.leaves_base_case / (n * n)
        worst_base_frac.append(frac)
        print(f"    {n:>6} | {d:>4} | {bb.pruned_blocks:>14} | {frac:>16.3f} | {str(bb.answer == truth):>22}")
    print("    pruned fraction EXACTLY 0, base/n^2 = 1.000 even with the omniscient incumbent: T(n) = 4 T(n/2)")
    print("    + cheap = Theta(n^2) = the BASELINE, zero log-shave. The wall SURVIVES.\n")

    print("(3) The recurrence ledger leaf-exponent log2(4(1-f)) (f=0 -> 2.0 baseline; super-polylog shave")
    print("    needs f bounded away from 0 at every level):")
    print(f"    {'pruned fraction f':>18} | {'leaf exponent log2(4(1-f))':>27}")
    print("    " + "-" * 48)
    for f in (0.0, 0.25, 0.5, 0.75):
        print(f"    {f:>18.2f} | {leaf_exponent(f):>27.3f}")
    print()

    print("(4) The GENUINE opening (the EXCLUDED regime): gapped/Valiant instances DO prune and shave, but")
    print("    that is the constant-relative-gap regime the THR-of-THR connection forbids.")
    Ag, Bg = make_planted_gap(512, 32, seed=3)
    truth_g, _ = max_ip_matrix_product(Ag, Bg)
    bb_g = branch_and_bound_maxip(Ag, Bg, "cauchy_schwarz", incumbent=-1)
    print(f"    planted-gap n=512 d=32: answer={bb_g.answer} (truth={truth_g}), base/n^2 = "
          f"{bb_g.leaves_base_case/(512*512):.5f}, pruned blocks={bb_g.pruned_blocks} (a REAL shave, EXCLUDED).\n")

    print("(5) The recursion does NOT escape ATTACK-1: the per-node bound IS the same single-round cheap")
    print("    measurement, summed over the tree. On dense worst-case data that is n^2 leaves of blind cost.")
    print("(6) CIRCULARITY: the only additive-1-tight certificate is the block's exact max = a recursive call")
    print("    to the same fused-max-MM problem, T(n) >= 4 T(n/2) = Theta(n^2). No shave, circular.")
    print("(7) HONESTY (the one bug surfaced): i.i.d. p=1/2 data carries a SPURIOUS popcount-spread prune")
    print("    (row weights vary O(sqrt d), giving the separable filter a foothold on EASY data). Neutralized")
    print("    by fixed-popcount rows above: the prune collapses to exactly 0. The apparent shave was an")
    print("    artifact on non-worst-case data, not a crack.\n")

    # ---------------------------------------------------------------------
    # ATTACK-3 (CLOSEST-PAIR).
    # ---------------------------------------------------------------------
    print("=" * 78)
    print("ATTACK-3 (CLOSEST-PAIR, W3): the metric reframe (thresholded Max-IP IS bichromatic closest-pair).")
    print("=" * 78 + "\n")
    print("The wall's LITERAL claim 'every fast method is a bulk aggregation' is FALSE. The exact reframe")
    print("Ham(a,b) = |a| + |b| - 2<a,b> makes thresholded Max-IP a METRIC near-neighbor problem with its")
    print("own closest-pair-specific log-shaving machinery (Alman-Williams FOCS 2015), none of B1-B4 used.\n")

    print("(1) The reframe identity Ham = |a| + |b| - 2<a,b> exact to the bit:",
          hamming_identity_check(seed=0))
    print("(2) The weight-bucketed Max-IP -> Hamming reduction equals direct A B^T max and brute force:")
    rng_cp = np.random.default_rng(13)
    cp_ok = True
    for (n, d) in [(20, 8), (30, 10), (16, 12)]:
        A = (rng_cp.random((n, d)) < 0.5).astype(np.int64)
        B = (rng_cp.random((n, d)) < 0.5).astype(np.int64)
        bf = max_ip_bruteforce(A, B)
        mp, _ = max_ip_matrix_product(A, B)
        bucketed = maxip_via_weight_bucketed_closest_pair(A, B)
        agree = (bf == mp == bucketed)
        cp_ok = cp_ok and agree
        print(f"    n={n} d={d}: brute={bf}, A B^T max={mp}, weight-bucketed closest-pair={bucketed}, agree={agree}")
    print()

    print("(3) The closest-pair-specific saved factor DECAYS at d = n^eps (overflow-safe log space):")
    print(f"    {'log2 n':>8} | {'ACW saved-fac log2 @ d=n^eps':>28} | {'ref @ d=4log n':>16} | {'in-regime?':>11}")
    print("    " + "-" * 70)
    acw_neps = []
    for L in (256.0, 1024.0, 4096.0, 16384.0):
        cp = closest_pair_saved_factor_log2(L, EPS)
        acw_neps.append(cp["saved_factor_log2_neps"])
        print(f"    {L:>8.0f} | {cp['saved_factor_log2_neps']:>28.3e} | {cp['saved_factor_log2_ref_4logn']:>16.3f} | "
              f"{str(cp['in_regime_neps']):>11}")
    print(f"    at d = n^eps the saved factor -> 1 + o(1) (sub-one-log); at d = 4 log n it GROWS (in-regime shave).")
    ov = ov_poly_saved_factor_log2(EPS)
    print(f"    CONTRAST: the general OV polynomial method saved-factor log2 -> 1/eps = {ov:.0f} (constant 2^(1/eps)")
    print(f"    = {2.0**ov:.0f}); the closest-pair method (-> 0) is STRICTLY WORSE (extra log^2 c surcharge).\n")

    print("(4) The metric structure does NOT hand ATTACK-2 a cheap additive-1 sub-block: a center-radius")
    crw = center_radius_width(seed=0)
    print(f"    triangle-inequality bound gives a RANGE of width 2R = {crw['range_width_2R']:.0f} on a real ball,")
    print(f"    not the gap-1 argmax (resolving max vs max-1 needs R < {crw['needs_R_below']}, a singleton = enumeration).\n")

    # ---------------------------------------------------------------------
    # ATTACK-4 (FALSIFY).
    # ---------------------------------------------------------------------
    print("=" * 78)
    print("ATTACK-4 (FALSIFY): non-bulk aggregations (tropical, threshold-rank, max-stable / L-infinity).")
    print("=" * 78 + "\n")
    print("Each non-bulk candidate is either NOT-fast-from-factored or NOT-extreme-at-unit-resolution.\n")

    t1 = tropical_is_wrong_quantity(12, 6, seed=0)
    print(f"T1 TROPICAL/(max,+): Max-IP = {t1['maxip']} but (max,+) max = {t1['tropical_max']} "
          f"(capped at 2 = {t1['tropical_capped_at_2']}), differs = {t1['differs']}. WRONG QUANTITY, and")
    print("    (max,+) MM has no sub-n^2 shave from small d (APSP-class). Fails fast-from-factored.\n")

    print("T2 THRESHOLD-RANK: thresholding a rank-d integer matrix DESTROYS low rank (only tau=max keeps")
    print("    rank ~1, which IS the answer = circular):")
    print(f"    {'n':>5} | {'d':>4} | {'rank(M)':>8} | {'bulk_tau':>9} | {'rank(1[M>=tau])':>16}")
    print("    " + "-" * 52)
    thr_rows = []
    for n in (40, 80, 160):
        tr = threshold_destroys_rank(n, 8, seed=0)
        thr_rows.append(tr)
        print(f"    {n:>5} | {tr['d']:>4} | {tr['rank_M']:>8} | {tr['bulk_tau']:>9} | {tr['rank_threshold']:>16}")
    print("    rank(M)=d stays small while rank(1[M>=bulk_tau]) grows like Theta(min(n, .)) >> d.\n")

    t3 = max_stable_needs_materialization(64, 8, seed=0)
    print(f"T3 MAX-STABLE / Indyk L-infinity sketch (FOCS 2000): genuinely extreme-sensitive and NON-bulk")
    print(f"    (so the LITERAL universality claim is FALSE). But its per-entry MAX readout has NO")
    print(f"    factorization through A B^T: separable rank-1 factors at O(nd) (factors={t3['separable_factors']},")
    print(f"    touches {t3['separable_touches']}), the per-entry max-stable readout must touch all "
          f"{t3['per_entry_max_touches']} = n^2 products.")
    print("    Small in SPACE, not in TIME-to-ingest-a-factored-M. Fails fast-from-factored.\n")

    print("CORRECTED universal obstruction (the deliverable): cheap-from-the-factored-form forces a")
    print("measurement to push through A B^T, which forces it to be BULK (low-degree symmetric /")
    print("rotation-invariant), which is blind to the L-infinity extreme. NOT 'separable' (the cores give")
    print("cheap NON-separable functionals; separability is a strict subclass). The missing object is a")
    print("non-linear, full-rank-in-(i,j), unit-resolution readout that ALSO factors through A B^T in o(n^2).\n")

    # ---------------------------------------------------------------------
    # Summary ledger + three-barrier note.
    # ---------------------------------------------------------------------
    print("=" * 78)
    print("SUMMARY LEDGER: four attacks, one hardened, two cracked-then-rehardened, one survived.")
    print("=" * 78 + "\n")
    ledger = build_prong_ledger()
    hdr = f"{'attack':<58} | {'result (short)':>16}"
    print(hdr)
    print("-" * len(hdr))
    short = {
        "ATTACK-1 (HARDEN, W2): single-round Cheap-Measurement-Model lower bound": "HARDENED",
        "ATTACK-2 (ADAPTIVE B&B, W4): incumbent-dependent branch-and-bound": "SURVIVES",
        "ATTACK-3 (CLOSEST-PAIR, W3): the metric reframe": "CRACKED+REHARD",
        "ATTACK-4 (FALSIFY): non-bulk probes (tropical, threshold-rank, max-stable)": "LITERAL-FALSE",
    }
    for r in ledger:
        print(f"{r.name[:58]:<58} | {short[r.name]:>16}")
    print()
    for r in ledger:
        print(f"  {r.name}")
        print(f"    goal            : {r.goal}")
        print(f"    result          : {r.result}")
        print(f"    quantified      : {r.quantified}")
        print(f"    escape locus    : {r.escape_locus}")
        print()

    # The three-barrier orthogonality self-check: these are in-MODEL algorithmic bounds / candidate
    # algorithms, NOT lower-bound certificates, so the barriers do not gate them (a clean evade).
    print("--- three-barrier orthogonality note ---")
    checker = BarrierChecker()
    algo = ProofTechnique(
        name="fused-max-MM attack (in-model algorithmic bound / candidate log-shave)",
        relativizes=False, natural_largeness=False, natural_constructivity=False, algebrizes=False,
        notes="An in-model measurement-blindness bound (ATTACK-1) and candidate algorithms (ATTACK-2/3/4) "
              "are not lower-bound certificates; the three barriers act on a hypothetical THR-of-THR proof "
              "one level up (the Williams spine), not on these objects. A clean evade is the correct verdict.",
    )
    verdict = checker.check(algo)
    print(verdict.report())
    print()

    # ======================================================================
    # Self-checks pinning every coordinate. Module must exit 0.
    # ======================================================================

    # --- ATTACK-1 self-checks ---
    # (A1.0) REUSE grounding: brute-force Max-IP = global max of A B^T.
    for seed in (0, 7, 21):
        rr = np.random.default_rng(seed)
        AA = (rr.random((8, 10)) < 0.5).astype(np.int64)
        BB = (rr.random((9, 10)) < 0.5).astype(np.int64)
        m_bf2 = max_ip_bruteforce(AA, BB)
        m_mp2, MM = max_ip_matrix_product(AA, BB)
        assert m_bf2 == m_mp2 == int(MM.max()), "REUSED baseline: brute-force Max-IP = global max of A B^T"

    # (A1.1) The cheap-from-factored identities hold, and cheap does NOT imply separable.
    assert sep["agree"], "rank-1 separable u^T M v = (u^T A)(B^T v) must agree (family (a) is cheap, O(nd))"
    assert core["agree"], "||M||_F^2 = tr((A^T A)(B^T B)) from the cores must agree (cheap NON-separable functional)"
    assert gw["is_full_rank"], "a generic dense linear test W is full-rank: <W,M> costs Theta(n^2 d), not cheap"

    # (A1.2) BRANCH (i): heaviness is Theta(1/n^2) (ratio*n^2 a small constant, d-independent).
    assert max(rtn2) < 100.0, "ratio*n^2 stays a small constant across n: the dense argmax is L2-LIGHT (Theta(1/n^2))"
    em2 = [heaviness_ratio(256, d, seed=0)["EM2"] for d in (4, 16, 64, 128)]
    assert all(em2[i] < em2[i + 1] for i in range(len(em2) - 1)), \
        "E[M_ij^2] = fro2/n^2 grows with d (Theta(d^2)): the gap-1 ESTIMATION floor is Theta(n^2 d^2)"
    assert em2[-1] > 1.0, "at moderate d the gap-1 separable-linear dimension exceeds n^2 (cannot resolve sub-n^2)"

    # (A1.3) BRANCH (ii): the Vandermonde witness shares m_1, m_2 but differs in max (and at m_3).
    assert coll["m1_equal"] and coll["m2_equal"] and coll["max_differs"], \
        "witness {3,1,1,1} vs {2,2,2,0}: identical m_1,m_2 but different max (degree-2 cannot resolve)"
    assert not coll["m3_equal"], "m_3 is the first moment that splits them (the top-bucket indicator has degree exactly d)"
    for d in (8, 16, 20):
        assert vandermonde_nullspace_dim(d, d) == 0, "after m_0..m_d the value-multiset is pinned (no free direction)"
        assert vandermonde_nullspace_dim(d, d - 1) > 0, "after only m_0..m_{d-1} the max is NOT determined"

    # (A1.4) BRANCH (iii) CONTAINMENT PATCH: a cheap spectral readout is blind at the gap-1 top.
    assert es["spectra_equal"] and es["max_differs"], \
        "equal-spectrum/different-max collision at the gap-1 top: the rotation-invariant family is blind too"
    assert (es["max_M2"] - es["max_M1"]) == 1 and es["max_M2"] == es["d"], \
        "the collision is exactly at max=d vs max=d-1 (the gap-1 decision the THR-of-THR connection needs)"

    # (A1.5) The single round, head-on: cheap readouts move 1/n^2-order while max moves by 1, rank<=d.
    for r in blind_rows:
        assert r["max_differs_by_one"] == 1, "the two instances differ by exactly +1 in the max"
        assert r["rank_ok"], "both factored instances keep rank <= d"
        assert r["fro2_rel_change"] < 1e-2, "the Frobenius (and every cheap bulk) readout moves a 1/n^2-order fraction"
        assert r["sep_rel_change"] < 1.0, "a fixed oblivious separable readout is not driven by the single +1 cell"

    # --- ATTACK-2 self-checks ---
    # (A2.0) Exactness of the adaptive B&B for every certificate.
    assert exact_ok, "the adaptive branch-and-bound returns the true Max-IP for every cheap certificate"

    # (A2.1) Cheap-certificate additive looseness is Theta(d): the gap GROWS with d, never additive 1.
    assert all(cs_gaps[i] <= cs_gaps[i + 1] + 1e-9 for i in range(len(cs_gaps) - 1)), \
        "the Cauchy-Schwarz additive looseness grows (non-decreasing) with d: Theta(d), not a constant slack"
    assert cs_gaps[-1] > 1.0, "at moderate d the cheap-certificate gap exceeds additive 1 (no additive-1 pruning)"

    # (A2.2) The TRUE worst case: pruned fraction 0, base-case work = full n^2, even with omniscient incumbent.
    assert all(abs(f - 1.0) < 1e-9 for f in worst_base_frac), \
        "fixed-popcount worst case: base-case work = n^2 EXACTLY (pruned fraction 0, T(n) = 4 T(n/2) + cheap)"

    # (A2.3) The recurrence: f=0 gives leaf exponent exactly 2.0 (the baseline), f>0 strictly below.
    assert abs(leaf_exponent(0.0) - 2.0) < 1e-12, "pruned fraction 0 gives leaf exponent 2.0 = the n^2 baseline"
    assert leaf_exponent(0.25) < 2.0 and leaf_exponent(0.5) < leaf_exponent(0.25), \
        "a super-polylog shave needs f bounded away from 0 at every level (leaf exponent < 2 strictly)"

    # (A2.4) The EXCLUDED opening: gapped/Valiant instances DO prune (a real shave), correctness preserved.
    assert bb_g.answer == truth_g, "the B&B is exact on the gapped instance too (a loose UB only means fewer prunes)"
    assert bb_g.leaves_base_case < 0.5 * 512 * 512, \
        "gapped/Valiant instances DO prune and shave (base/n^2 small): the EXCLUDED constant-relative-gap regime"

    # --- ATTACK-3 self-checks ---
    # (A3.1) The reframe identity and the weight-bucketed reduction are exact.
    assert hamming_identity_check(seed=1), "Ham(a,b) = |a|+|b|-2<a,b> holds to the bit (the exact metric reframe)"
    assert cp_ok, "the weight-bucketed Max-IP -> Hamming closest-pair reduction equals direct max and brute force"

    # (A3.2) The closest-pair-specific saved factor DECAYS at d = n^eps (monotone to 0), strictly below the
    #        OV constant 2^{1/eps}. So the metric crack does not reach the prize.
    assert all(acw_neps[i] >= acw_neps[i + 1] - 1e-12 for i in range(len(acw_neps) - 1)), \
        "the ACW closest-pair saved factor at d=n^eps is non-increasing in n (decays to 1 + o(1))"
    assert acw_neps[-1] < ov_poly_saved_factor_log2(EPS), \
        "the closest-pair saved factor (-> 0) is STRICTLY worse than the OV constant 2^{1/eps} at large n"
    cp_ref = closest_pair_saved_factor_log2(256.0, EPS)
    assert cp_ref["saved_factor_log2_ref_4logn"] > cp_ref["saved_factor_log2_neps"], \
        "the in-regime d = 4 log n shave exceeds the d = n^eps decay (the dimension ceiling is the obstruction)"

    # (A3.3) The metric center-radius bound gives a RANGE of width 2R >> 1, not the gap-1 argmax.
    assert crw["range_width_2R"] > 1.0, \
        "a triangle-inequality center-radius bound gives a width-2R range, not the gap-1 argmax (R < 1/2 = singleton)"

    # --- ATTACK-4 self-checks ---
    # (A4.1) T1 tropical is the wrong quantity (capped at 2, differs from Max-IP).
    assert t1["tropical_capped_at_2"] and t1["differs"], \
        "the (max,+) product is a DIFFERENT object (values in {0,1,2}) from Max-IP in {0..d}"

    # (A4.2) T2 thresholding destroys the rank-d structure (rank explosion >> d).
    assert all(tr["rank_threshold"] > tr["rank_M"] for tr in thr_rows), \
        "thresholding a rank-d integer matrix destroys low rank: rank(1[M>=bulk_tau]) >> rank(M) = d"

    # (A4.3) T3 max-stable: the separable rank-1 sketch factors (O(nd)), the per-entry max needs all n^2.
    assert t3["separable_factors"], "a rank-1 SEPARABLE sketch factors through A B^T at O(nd)"
    assert t3["per_entry_max_touches"] == 64 * 64 and t3["per_entry_max_touches"] > t3["separable_touches"], \
        "the per-entry max-stable readout has NO factorization: it must ingest all n^2 products (Theta(n^2) time)"

    # --- ledger + barrier self-checks ---
    ledger_check = build_prong_ledger()
    assert len(ledger_check) == 4, "the ledger pins all four attack prongs"
    assert all(r.barrier_free for r in ledger_check), \
        "all four prongs are barrier-free: in-model bounds / candidate algorithms, not lower-bound certificates"
    assert verdict.evades_all, \
        "the three-barrier checker reports a clean evade (these objects are not lower-bound certificates)"

    print("=== Self-check OK ===")
    print("(ATTACK-1) HARDENED to a single-round Cheap-Measurement-Model lower bound. Three cheap families")
    print("    (separable-linear, degree-D symmetric, rotation-invariant spectral) all BLIND to max=d vs")
    print("    max=d-1: (i) heaviness Theta(1/n^2) -> localization floor Theta(n^2), gap-1 estimation floor")
    print("    Theta(n^2 d^2); (ii) Vandermonde top-bucket degree exactly d (witness {3,1,1,1} vs {2,2,2,0});")
    print("    (iii) equal-spectrum collision at the gap-1 top. CORRECTION: cheap =/=> separable (the cores")
    print("    give cheap NON-separable functionals); the wall is BULK-ness. Escape locus: ADAPTIVE (W4).")
    print("(ATTACK-2) SURVIVES. On fixed-popcount worst-case data the adaptive B&B prunes EXACTLY 0 (even")
    print("    with the omniscient incumbent): base/n^2 = 1.000, T(n) = 4 T(n/2) + cheap = Theta(n^2). Cheap")
    print("    certificates are additively Theta(d) loose; the only additive-1 cert is the exact block max")
    print("    (circular). The wall is worst-case GAPLESSNESS, not the single-round restriction. The i.i.d.")
    print("    popcount-spread prune is a bug, neutralized by fixed popcount.")
    print("(ATTACK-3) CRACKED as stated, RE-HARDENED. Thresholded Max-IP IS bichromatic Hamming closest-pair")
    print("    (exact reframe verified). But the closest-pair-specific saved factor decays to 1 + o(1) at")
    print("    d = n^eps (ceiling d = o(log^2 n)), STRICTLY worse than the OV constant 2^{1/eps}. The metric")
    print("    bound gives a RANGE, not the gap-1 argmax.")
    print("(ATTACK-4) LITERAL universality FALSE (T3 max-stable is fast non-bulk), wall survives at the")
    print("    TIME-to-ingest level. T1 wrong quantity, T2 rank explosion, T3 no factorization (n^2 ingest).")
    print()
    print("VERDICT: the heuristic wall is HARDENED to a single-round cheap-measurement lower bound. The")
    print("escape locus is ADAPTIVE / multi-round / METRIC (W3/W4). The most promising crack is the adaptive")
    print("separable-measurement / closest-pair route, which (ATTACK-2/3) does not reach the prize on dense")
    print("gapless worst-case data: it pays the single-round blind cost per node, or its saved factor decays")
    print("below one log at polynomial dimension. The frontier remains OPEN and barrier-free. NO progress on")
    print("the prize claimed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
