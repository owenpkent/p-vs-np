"""Fused-max-MM (the J1 frontier): four candidate max-extraction engines, each a NEGATIVE.

THE TARGET (Chen 2018, arXiv:1805.10698, Theorem 1.5 item 1, web-confirmed VERBATIM in
the sibling e_maxip_logshave.py):

  "An n^2 / log^{omega(1)} n time algorithm for Bichromatic Maximum Inner Product with
   vector dimension d = n^eps for any small constant eps would imply NEXP has no
   polynomial size THR o THR circuits. Note there is an n^2 polylog(n) time algorithm
   via fast rectangle matrix multiplication."

So: A, B are each n Boolean vectors in {0,1}^d with d = n^eps. M = A B^T is the n x n
INTEGER count matrix, M_{ij} = <a_i, b_j> in {0,...,d}, rank <= d, given in FACTORED form.
ans = max_{i,j} M_{ij}. The bar is a SUPER-polylog shave of the n^2 baseline (beat n^2 by a
factor growing faster than every fixed power of log n). The required structural novelty is
MAX-EXTRACTION-WITHOUT-ENUMERATION: compute the global max WITHOUT materializing all n^2
entries of M (a naive materialize-then-scan spends Theta(n^2) on the scan alone).

WHAT THIS MODULE IS. The consolidated fused-max-MM ledger: it isolates the sub-problem and
NUMERICALLY DEMONSTRATES the obstruction of each of FOUR candidate max-extraction engines,
each of which fuses a genuine subquadratic global aggregate of all n^2 inner products but
cannot deliver the max:

  C1 MOMENT / tensor-power counting-MM. m_p = sum_{i,j} <a_i,b_j>^p computed as ONE fused
     dimension-d^p contraction < sum_i a_i^{tensor p}, sum_j b_j^{tensor p} >, no n^2
     materialization. The max is an L^infinity / extreme-value statistic; moments are
     L^p / bulk statistics. INFORMATION-THEORETIC wall: matching m_1..m_K (ANY readout)
     leaves the max free iff K <= d-1 (Vandermonde nullspace), and the only subquadratic
     budget is P < 1/eps moments (a constant), giving a polynomial window n^{2/P}.

  C2 SPECTRAL / low-rank. Frobenius, spectral norm, full spectrum, leverage: all O(n^{1+2eps}).
     The strictly rotation-invariant ones are functions of the singular values alone, so an
     equal-spectrum / different-max pair pins a Theta(n) multiplicative window. But the SHARP,
     operative wall is not the window: even a cheap NON-invariant bound that is multiplicatively
     tight (per-factor-row Cauchy-Schwarz) cannot resolve the integer gap max vs max-1, which
     is exactly what the THR-of-THR connection demands, and that resolution + argmax
     localization collapses to the n^2 scan.

  C3 COUNT-PRESERVING REGULARITY. Rebuild AFKLM/Kelley-Lovett-Meka to track integer codegree
     counts instead of collapsing to a one-bit OR; read each pseudorandom block's max off its
     density. Regularity controls AVERAGES to additive eps_reg*d; the max is a single-unit
     large deviation. A planted pair worth Theta(d) moves every density by only O(1/n), so the
     density summary is information-theoretically blind to the answer. STEP 2 is heuristic
     (wrong) or exact (a recursive oracle for the very problem): heuristic=wrong / exact=circular.

  C4 SKETCH / heavy-hitter. Compressed matrix multiplication (Pagh 2013) + count-sketch
     heavy-hitters (CCF 2002) localize the argmax as an L2-heavy entry. On dense M the argmax
     is L2-LIGHT (heaviness ratio Theta(1/n^2)), so the count-sketch width forced is Theta(n^2):
     a LINEAR (count-)sketch resolving the dense argmax below the top gap needs dimension
     s > ||M||_F^2 / gap^2 = Theta(n^2 d), at least the baseline.

ADVERSARY CORRECTIONS APPLIED (the math the verifier fixed):
  - C1: the obstruction is upgraded from estimator-overshoot to the Vandermonde information
    bound (witness {3,1,1,1} vs {2,2,2,0} share m_1, m_2 but differ in max); the affordable
    readout class is exactly degree-<=P polynomials of the entry value.
  - C2: the builder's "every cheap subquadratic quantity is rotation-invariant => Theta(n)
    window" is OVERSTATED. The per-factor-row Cauchy-Schwarz bound is O(n d), NOT
    rotation-invariant, and is multiplicatively tight (1.0-1.25x) on dense Boolean data; so the
    window is NOT the binding constraint. The real wall is integer-gap-1 resolution + argmax
    localization (the enumeration wall). The avenue is NOT "doubly barrier-blocked": natural
    proofs and algebrization act on a hypothetical lower-bound certificate, not on the algorithm.
  - C3: the planted value is popcount(a_0), a Theta(d) random variable (seed-specific); the
    deviation is the order-statistic sigma*sqrt(2 ln(n^2)), sigma = sqrt(d*rho*(1-rho)); STEP 2
    is heuristic=wrong / exact=circular.
  - C4: the builder's "one-sparse recovery forces s = Omega(n^2)" is MATHEMATICALLY WRONG.
    Deterministic for-all 1-sparse recovery needs only ceil(log2 N)+1 measurements (bit-encoding
    matrix). The exhibited "collision" exists ONLY because the target column is hand-zeroed; a
    random sketch never collides on a single-cell difference. The sound, binding obstruction is
    Part 2 alone (L^infinity-from-L2 lightness), reframed correctly here.

HONESTY DISCIPLINE. PROVED facts cite venue/year/arXiv. Each obstruction is exhibited with an
explicit small instance and MEASURED numbers. A precise, quantified NEGATIVE is the expected,
valuable outcome. If a construction appeared to actually shave, that would be almost-certainly a
bug to hunt; none does. No speedup is claimed; no progress on the prize. No em dashes anywhere.

Run:
    python -m experiments.circuit_complexity.e_fused_max_mm
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np

# REUSE the J1 baseline ground truth: Boolean Max-IP two ways (brute force, A B^T then max).
from experiments.circuit_complexity.e_maxip_logshave import (
    max_ip_bruteforce,
    max_ip_matrix_product,
)


EPS = 0.1   # the modest dimension exponent d = n^eps; any constant eps > 0 works.


# ==========================================================================
# C1: MOMENT / tensor-power counting-MM.
#
# The fusion identity (verified below): m_p = sum_{i,j} <a_i,b_j>^p factorizes as a SINGLE
# inner product in dimension d^p,  m_p = < sum_i (a_i)^{tensor p}, sum_j (b_j)^{tensor p} >,
# so all n^2 inner products are aggregated WITHOUT forming M. m_p is the (unnormalized) p-th
# moment of the empirical distribution of the n^2 inner-product values. The attempt is to read
# the global MAX (an L^infinity / extreme statistic) off the first P moments (L^p / bulk).
# ==========================================================================


def tensor_power_sum(V: np.ndarray, p: int) -> np.ndarray:
    """S = sum_i (v_i)^{tensor p} as a flat vector in R^{d^p}, by literal outer-product accumulation.

    This is the fusion ingredient: the per-vector tensor powers are SUMMED first, so the n^2
    pairing never appears. (Cost O(n d^p), the source of the n^{1+p*eps} per-moment cost.)
    """
    n, d = V.shape
    acc = np.zeros(d ** p, dtype=np.float64)
    for i in range(n):
        t = np.array([1.0])
        vi = V[i].astype(np.float64)
        for _ in range(p):
            t = np.multiply.outer(t, vi).ravel()   # raise the tensor power one factor at a time
        acc += t
    return acc


def moment_via_tensor_identity(A: np.ndarray, B: np.ndarray, p: int) -> float:
    """m_p = < sum_i a_i^{tensor p}, sum_j b_j^{tensor p} >, the fused dimension-d^p contraction."""
    S_A = tensor_power_sum(A, p)
    S_B = tensor_power_sum(B, p)
    return float(np.dot(S_A, S_B))


def moment_via_bruteforce(A: np.ndarray, B: np.ndarray, p: int) -> float:
    """m_p = sum_{i,j} (M_{ij})^p computed by materializing M (the ground truth for the identity)."""
    M = A.astype(np.float64) @ B.astype(np.float64).T
    return float(np.sum(M.astype(np.float64) ** p))


def vandermonde_nullspace_dim(d: int, K: int) -> int:
    """dim of the space of count-multisets on {0,...,d} left FREE after matching m_1..m_K.

    The map (multiset on {0,...,d}) -> (m_0=count, m_1, ..., m_K) is the Vandermonde transform
    on the d+1 possible values. Matching m_0..m_K pins K+1 linear functionals of the (d+1)
    value-bucket counts, so the affine fiber has dimension (d+1) - (K+1) = d - K when K < d.
    When that is > 0 (i.e. K <= d-1) the max is NOT determined: there exist two multisets with
    identical m_1..m_K and different max. This is an INFORMATION bound (any readout, not just the
    power-mean), strictly stronger than the estimator-overshoot sandwich.
    """
    return max(0, (d + 1) - (K + 1))


def explicit_moment_collision() -> dict[str, object]:
    """The smallest exact witness: two value-multisets sharing m_1, m_2 but with different max.

    X = {3,1,1,1}, Y = {2,2,2,0} (entries of a 2x2 Boolean product with d=3, n^2=4 entries).
    Computed in exact rational arithmetic so the equality of m_1, m_2 is not a float artifact.
    """
    X = [3, 1, 1, 1]
    Y = [2, 2, 2, 0]
    def moments(vals: list[int], P: int) -> list[Fraction]:
        return [sum(Fraction(v) ** p for v in vals) for p in range(1, P + 1)]
    mX = moments(X, 2)
    mY = moments(Y, 2)
    return {
        "X": X, "Y": Y,
        "m1_X": mX[0], "m2_X": mX[1],
        "m1_Y": mY[0], "m2_Y": mY[1],
        "max_X": max(X), "max_Y": max(Y),
        "m1_equal": mX[0] == mY[0],
        "m2_equal": mX[1] == mY[1],
        "max_differs": max(X) != max(Y),
    }


@dataclass
class MomentBudget:
    eps: float
    P: int
    cost_exponent: float        # n^{1 + P*eps}: the exponent of the top-moment cost
    subquadratic: bool          # cost exponent < 2
    window_log2n_factor: float  # log_n of the multiplicative window n^{2/P} (= 2/P)


def moment_budget(eps: float, P: int) -> MomentBudget:
    """Cost exponent 1 + P*eps and recovery window exponent 2/P at P moments."""
    cost_exp = 1.0 + P * eps
    return MomentBudget(
        eps=eps, P=P, cost_exponent=cost_exp,
        subquadratic=(cost_exp < 2.0),
        window_log2n_factor=(2.0 / P),
    )


def moments_to_clear_bulk(n: float, c: float) -> float:
    """P needed before the planted max term d^P exceeds the n^2-strong bulk (c d)^P.

    (d/(c d))^P = (1/c)^P > n^2  <=>  P > (2 log2 n) / log2(1/c) = Omega(log n).
    c is the bulk mean / max ratio (c = 1/4 for two iid p=1/2 Boolean sides; the Omega(log n)
    holds for any constant c < 1).
    """
    return (2.0 * math.log2(n)) / math.log2(1.0 / c)


def moments_to_resolve_unit(n: float, d: float) -> float:
    """P needed to separate the top value v ~ d from v-1 against an n^2 bulk of (v-1)-copies.

    (v/(v-1))^P = (1 + 1/(v-1))^P ~ e^{P/d} > n^2  <=>  P/d > ln(n^2)  <=>  P = Omega(d log n).
    This is the exact integer resolution the THR-of-THR connection needs (gap-1 decision).
    """
    return d * math.log(n * n)


# ==========================================================================
# C2: SPECTRAL / low-rank.
#
# The strictly rotation-invariant aggregates (Frobenius, spectral norm, full spectrum) are
# functions of the singular values alone, so an equal-spectrum / different-max pair pins a
# Theta(n) window. The CORRECTION (adversary): a cheap NON-invariant bound, per-factor-row
# Cauchy-Schwarz max_i||a_i|| * max_j||b_j||, beats that window (1.0-1.25x on dense Boolean
# data), so the window is NOT the binding wall. The operative wall is integer-gap-1 resolution
# + argmax localization (the enumeration wall), shared with C1/C4.
# ==========================================================================


def equal_spectrum_different_max(n: int) -> dict[str, object]:
    """A spread rank-1 (u = v = ones/sqrt n) vs a spike rank-1 (e_1 e_1^T): same spectrum, max ratio n.

    Both are rank-1 with the single nonzero singular value 1 (identical Frobenius, spectral
    norm, full spectrum), but max entry 1/n (spread) vs 1 (spike). The max-ratio is exactly n:
    the rotation-invariant certificate is blind to a Theta(n) factor on the max.
    """
    ones = np.ones(n) / math.sqrt(n)
    M_spread = np.outer(ones, ones)              # every entry 1/n, sigma = {1, 0, ...}
    e1 = np.zeros(n); e1[0] = 1.0
    M_spike = np.outer(e1, e1)                    # one entry 1, sigma = {1, 0, ...}
    s_spread = np.linalg.svd(M_spread, compute_uv=False)
    s_spike = np.linalg.svd(M_spike, compute_uv=False)
    return {
        "n": n,
        "spectra_equal": bool(np.allclose(np.sort(s_spread), np.sort(s_spike), atol=1e-12)),
        "max_spread": float(M_spread.max()),
        "max_spike": float(M_spike.max()),
        "max_ratio": float(M_spike.max() / M_spread.max()),
        "sigma_max_spread": float(s_spread[0]),
        "sigma_max_spike": float(s_spike[0]),
    }


def cheap_cauchyschwarz_window(A: np.ndarray, B: np.ndarray) -> dict[str, float]:
    """The per-factor-row Cauchy-Schwarz upper bound vs the spectral-norm window, both on M = A B^T.

    CS bound = (max_i ||a_i||) * (max_j ||b_j||): O(n d), NOT rotation-invariant (a rotation
    U M V^T changes the factor row norms). On dense Boolean data the row norms concentrate at
    sqrt(d/2), so CS ~ d/2 ... d, multiplicatively TIGHT on the true max (which is itself ~ d).
    The spectral-norm window ||M||_2 / true_max is wide. So the window is NOT the binding wall.
    Yet CS gives neither the integer value nor the argmax pair: it cannot resolve max vs max-1.
    """
    M = A.astype(np.float64) @ B.astype(np.float64).T
    true_max = float(M.max())
    a_norms = np.sqrt((A.astype(np.float64) ** 2).sum(axis=1))
    b_norms = np.sqrt((B.astype(np.float64) ** 2).sum(axis=1))
    cs_bound = float(a_norms.max() * b_norms.max())
    spec_norm = float(np.linalg.svd(M, compute_uv=False)[0])
    return {
        "true_max": true_max,
        "cs_bound": cs_bound,
        "cs_window": cs_bound / true_max if true_max > 0 else float("inf"),
        "spectral_norm": spec_norm,
        "spectral_window": spec_norm / true_max if true_max > 0 else float("inf"),
    }


# ==========================================================================
# C3: COUNT-PRESERVING REGULARITY.
#
# Build a pseudorandom instance, plant ONE high pair, and show the density / average data is
# (near) identical to the no-plant instance while the max jumps by Theta(d). Regularity certifies
# densities to additive eps_reg*d; the planted pair moves every density by O(1/n). The averaging
# engine is blind to the extreme cell that carries the answer.
# ==========================================================================


def order_statistic_deviation(d: float, rho: float, n: float) -> float:
    """The expected max-of-N inner products above the mean: sigma * sqrt(2 ln(n^2)).

    sigma = sqrt(d * rho * (1-rho)) is the per-entry std of a Binomial(d, rho)-like count; the
    max of N = n^2 of them sits ~ sigma*sqrt(2 ln N) above the mean (Gaussian order statistic).
    This is the deviation the density (which knows only the mean d*rho) cannot resolve.
    """
    sigma = math.sqrt(d * rho * (1.0 - rho))
    return sigma * math.sqrt(2.0 * math.log(n * n))


def regularity_planted_spike(seed: int = 3) -> dict[str, object]:
    """Pseudorandom instance + one planted pair: max jumps Theta(d), densities move O(1/n)."""
    rng = np.random.default_rng(seed)
    n, d, rho = 2000, 400, 0.25
    p = math.sqrt(rho)                            # so E[<a_i,b_j>] = d * p^2 = d * rho
    A = (rng.random((n, d)) < p).astype(np.int64)
    B = (rng.random((n, d)) < p).astype(np.int64)

    # The bulk (no plant): mean and observed pseudorandom max.
    M_bulk = A @ B.T
    bulk_mean = float(M_bulk.mean())
    bulk_max = int(M_bulk.max())

    # Density data the decomposition would use (column densities), before the plant.
    densA_before = float(A.mean())
    densB_before = float(B.mean())

    # Plant one high pair: B[0] = A[0], so <a_0, b_0> = popcount(a_0) ~ d * p (a Theta(d) r.v.).
    B2 = B.copy()
    B2[0] = A[0]
    M_plant = A @ B2.T
    plant_max = int(M_plant.max())
    planted_value = int(A[0].sum())              # popcount(a_0): the planted cell's value
    densB_after = float(B2.mean())

    deviation_formula = order_statistic_deviation(float(d), rho, float(n))
    return {
        "n": n, "d": d, "rho": rho,
        "bulk_mean": bulk_mean,
        "bulk_max": bulk_max,
        "bulk_deviation": bulk_max - bulk_mean,
        "order_stat_deviation": deviation_formula,
        "planted_value_popcount_a0": planted_value,
        "plant_max": plant_max,
        "max_jump": plant_max - bulk_max,
        "densB_before": densB_before,
        "densB_after": densB_after,
        "density_move": abs(densB_after - densB_before),
        "one_over_n": 1.0 / n,
        "densA": densA_before,
    }


def regularity_granularity_cost(eps: float, log2n: float) -> dict[str, float]:
    """Single-unit precision forces eps_reg < 1/d, so weak-regularity blocks B = 2^{O(d^2)}.

    d = n^eps, so log2(d) = eps*log2(n) and the weak-regularity exponent 1/eps_reg^2 = d^2.
    Compare log2(#blocks) = d^2 against log2(n^2) = 2*log2(n): d^2 >> 2*log2(n) always.
    """
    log2d = eps * log2n
    d = 2.0 ** log2d
    return {
        "log2d": log2d,
        "d": d,
        "weak_reg_block_exponent_d2": d * d,       # log2(#blocks) ~ d^2 (Frieze-Kannan)
        "log2_n_squared": 2.0 * log2n,
    }


# ==========================================================================
# C4: SKETCH / heavy-hitter.
#
# Part A (heaviness wall, the SOUND obstruction): on dense M the argmax is L2-LIGHT
# (heaviness ratio Theta(1/n^2)), so a count-sketch resolving it below the top gap needs width
# Theta(n^2). Part B (the CORRECTION): the builder's "one-sparse recovery forces s = Omega(n^2)"
# is wrong; deterministic for-all 1-sparse recovery needs only ceil(log2 N)+1 measurements, and
# the exhibited collision exists ONLY because the target column is hand-zeroed. So the binding
# wall is heaviness, not a 1-sparse lower bound.
# ==========================================================================


def heaviness_ratio(n: int, d: int, seed: int = 0) -> dict[str, float]:
    """argmax^2 / ||M||_F^2 on dense Boolean M = A B^T, and the count-sketch width it forces.

    On dense data the argmax value ~ d is one of n^2 entries all of comparable Theta(d)
    magnitude, so ||M||_F^2 = Theta(n^2 d^2) and the heaviness ratio argmax^2/||M||_F^2 = Theta(1/n^2)
    (independent of d). The L2-heavy-hitter width needed is 1/ratio = Theta(n^2). The integer-gap
    version (resolve the top value from top-1, gap = 1): width s > ||M||_F^2 / gap^2 = Theta(n^2 d^2),
    i.e. fro2/n^2 = E[M_ij^2] = (d/4)^2 + 3d/16 = Theta(d^2), a factor Theta(d^2) WORSE than n^2.
    """
    rng = np.random.default_rng(seed)
    A = (rng.random((n, d)) < 0.5).astype(np.float64)
    B = (rng.random((n, d)) < 0.5).astype(np.float64)
    M = A @ B.T
    fro2 = float((M ** 2).sum())
    amax = float(M.max())
    ratio = amax * amax / fro2
    # The integer-gap-resolution width: distinguish the top value from top-1 -> gap = 1.
    gap = 1.0
    width_gap = fro2 / (gap * gap)
    return {
        "n": float(n), "d": float(d),
        "argmax": amax,
        "fro2": fro2,
        "heaviness_ratio": ratio,
        "ratio_times_n2": ratio * n * n,
        "width_heavy": 1.0 / ratio,
        "width_gap1_over_n2": width_gap / (n * n),   # = fro2/n^2 = E[M_ij^2] = Theta(d^2): factor d^2 WORSE
        "EM2": fro2 / (n * n),                        # the per-entry second moment, grows like Theta(d^2)
    }


def one_sparse_recovery_is_cheap(N: int, seed: int = 1) -> dict[str, object]:
    """The bit-encoding matrix: deterministic for-all 1-sparse recovery in ceil(log2 N)+1 rows.

    Row 0 carries the value (all-ones), rows 1..L carry the bit-pattern of the index. For a
    1-sparse x = c * e_k, sketch = S x gives sk[0] = c (value) and sk[r]/c = bit r-1 of k
    (location). So 1-sparse recovery costs O(log N), NOT Omega(N). This REFUTES the builder's
    "one-sparse recovery forces s = Omega(n^2)" claim used in C4 obstruction (B).
    """
    rng = np.random.default_rng(seed)
    L = (N - 1).bit_length()                      # ceil(log2 N) bits suffice for indices 0..N-1
    rows = 1 + L
    S = np.zeros((rows, N), dtype=np.float64)
    S[0, :] = 1.0                                 # value row
    for k in range(N):
        for b in range(L):
            if (k >> b) & 1:
                S[1 + b, k] = 1.0                 # location bit rows
    # Recover a random 1-sparse vector.
    k_true = int(rng.integers(0, N))
    c_true = float(rng.integers(1, 50))
    x = np.zeros(N); x[k_true] = c_true
    sk = S @ x
    c_rec = sk[0]
    k_rec = 0
    for b in range(L):
        if sk[1 + b] > 0.5 * c_rec:
            k_rec |= (1 << b)
    return {
        "N": N, "rows": rows, "ceil_log2_N_plus_1": (N - 1).bit_length() + 1,
        "recovered_location": (k_rec == k_true),
        "recovered_value": (abs(c_rec - c_true) < 1e-9),
        "k_true": k_true, "k_rec": k_rec,
    }


def single_entry_difference_factored(n: int, d: int, seed: int) -> dict[str, object]:
    """Two factored instances (A,B), (A,B') whose products differ in EXACTLY one cell by +1.

    Construction (deterministic, never fails): dedicate a PRIVATE coordinate k* set in exactly
    one A-row i* (A[:,k*] = indicator of i*) with B[j*,k*] = 0 originally. Then flip B'[j*,k*] = 1.
    Since only B-row j* changed and only A-row i* has a 1 in column k*, (A B'^T) - (A B^T) = + E_{i*,j*},
    a single +1 cell, rank of both products <= d. This grounds that the DIFFERENCE is 1-sparse (cheap
    to recover); what is actually hard is reading the L^infinity max of a DENSE M from a linear sketch
    (Part A), not the 1-sparse difference. (The builder's search-based version fails when no random
    column happens to be set in exactly one A-row; this constructed version is robust.)
    """
    rng = np.random.default_rng(seed)
    A = (rng.random((n, d)) < 0.5).astype(np.int64)
    B = (rng.random((n, d)) < 0.5).astype(np.int64)
    i_star, j_star, k_star = 0, 1, d - 1     # dedicate the last coordinate as the private column
    A[:, k_star] = 0
    A[i_star, k_star] = 1                     # column k* is the indicator of row i* (set in exactly one A-row)
    B[j_star, k_star] = 0                     # B's k*-bit is off, so M_{i*,j*} omits this coordinate
    Bp = B.copy()
    Bp[j_star, k_star] = 1                    # turn it on: M'_{i*,j*} = M_{i*,j*} + 1, all else unchanged
    M = A @ B.T
    Mp = A @ Bp.T
    diff = Mp - M
    nz = np.argwhere(diff != 0)
    rank_ok = (np.linalg.matrix_rank(M.astype(np.float64)) <= d and
               np.linalg.matrix_rank(Mp.astype(np.float64)) <= d)
    return {
        "ok": True,
        "i_star": i_star, "j_star": j_star, "k_star": k_star,
        "num_diff_cells": int((diff != 0).sum()),
        "diff_value": int(diff[i_star, j_star]),
        "exactly_one_plus_one": (int((diff != 0).sum()) == 1 and int(diff[i_star, j_star]) == 1),
        "rank_ok": bool(rank_ok),
        "nz_cells": [tuple(int(x) for x in c) for c in nz],
    }


# ==========================================================================
# The summary ledger row per candidate.
# ==========================================================================


@dataclass(frozen=True)
class CandidateRow:
    name: str
    fuses_what: str
    obstruction: str
    quantified_wall: str
    barrier_free: bool
    secret_speedup_risk: str


def build_candidate_ledger() -> list[CandidateRow]:
    return [
        CandidateRow(
            name="C1 Moment / tensor-power counting-MM",
            fuses_what="m_p = <sum_i a_i^{tp}, sum_j b_j^{tp}> = sum_{i,j} <a_i,b_j>^p (p-th moment, no n^2)",
            obstruction="moments are L^p/bulk; the max is L^infinity/extreme. Matching m_1..m_K leaves "
                        "the max free iff K <= d-1 (Vandermonde nullspace). Any readout, not just power-mean.",
            quantified_wall="subquadratic only for P < 1/eps (window n^{2/P} polynomial); clearing the bulk "
                            "needs P = Omega(log n); unit (v vs v-1) resolution needs P = Omega(d log n) = "
                            "Omega(n^eps log n), cost n^{1+omega(1)}. Each extra moment costs a factor d=n^eps.",
            barrier_free=True,
            secret_speedup_risk="none (subquadratic and useful moment regimes are DISJOINT)",
        ),
        CandidateRow(
            name="C2 Spectral / low-rank",
            fuses_what="rotation-invariant L2 aggregates of factored M: Frobenius, spectral norm, full spectrum, "
                       "leverage; all O(n^{1+2eps})",
            obstruction="strictly rotation-invariant aggregates are functions of the singular values alone "
                        "(equal-spectrum/different-max), BUT the binding wall is integer-gap-1 resolution + "
                        "argmax localization (the enumeration wall), shared with C1/C4. The Theta(n) window is "
                        "NOT the binding constraint (a cheap non-invariant CS bound is multiplicatively tight).",
            quantified_wall="equal-spectrum pair has max-ratio exactly n; yet cheap CS bound window is 1.0-1.25x "
                            "on dense data, so the window is not binding. Resolving max vs max-1 and localizing "
                            "the argmax both collapse to the n^2 scan.",
            barrier_free=True,
            secret_speedup_risk="none (never produces the max; the n^{1+2eps} cost buys the wrong invariant)",
        ),
        CandidateRow(
            name="C3 Count-preserving regularity",
            fuses_what="per-block-pair average codegree rho_{s,t}*d (an O(B^2) density summary of M), via "
                       "block-aggregated contractions, no n^2 entries",
            obstruction="regularity controls AVERAGES to additive eps_reg*d; the max is a single-unit large "
                        "deviation. A planted pair worth Theta(d) moves every density by O(1/n). STEP 2 is "
                        "heuristic (wrong) or exact (a recursive oracle for the same problem): heuristic=wrong / "
                        "exact=circular.",
            quantified_wall="single-unit precision forces eps_reg < 1/d, so weak-regularity blocks B = 2^{O(d^2)} "
                            "= 2^{O(n^{2eps})} >> n^2; planted max jumps Theta(d) while density moves O(1/n).",
            barrier_free=True,
            secret_speedup_risk="none (correctness needs B = 2^{Omega(n^{2eps})}; subquadratic B loses the argmax)",
        ),
        CandidateRow(
            name="C4 Sketch / heavy-hitter",
            fuses_what="signed hashed bucket-sums of the n^2 inner products (compressed MM, Pagh 2013; "
                       "count-sketch, CCF 2002): the L2 mass and L2-heavy entries",
            obstruction="on dense M the argmax is L2-LIGHT (heaviness ratio Theta(1/n^2)). A linear (count-)sketch "
                        "resolving the dense argmax below the top gap needs dimension s > ||M||_F^2/gap^2 = "
                        "Theta(n^2 d^2). NOTE: the '1-sparse recovery => Omega(n^2)' framing is WRONG (1-sparse "
                        "recovery is O(log N)); the difference is 1-sparse and cheap, the DENSE max is what is hard.",
            quantified_wall="heaviness ratio Theta(1/n^2) (measured ratio*n^2 in [2,11]); count-sketch width forced "
                            "Theta(n^2); integer-gap-1 width Theta(n^2 d^2), since E[M_ij^2] = Theta(d^2), WORSE than baseline.",
            barrier_free=True,
            secret_speedup_risk="none (the only sub-n^2 path needs L2-heaviness the dense argmax lacks)",
        ),
    ]


# ==========================================================================
# Reporting
# ==========================================================================


def main() -> int:
    print("=== Fused-max-MM (J1 frontier): four candidate max-extraction engines, all NEGATIVES ===\n")
    print("TARGET (Chen 2018 arXiv:1805.10698 Thm 1.5 item 1, web-confirmed verbatim in e_maxip_logshave.py):")
    print('  "An n^2 / log^{omega(1)} n time algorithm for Bichromatic Maximum Inner Product with vector')
    print('   dimension d = n^eps ... would imply NEXP has no polynomial size THR o THR circuits. Note there')
    print('   is an n^2 polylog(n) time algorithm via fast rectangle matrix multiplication."')
    print("M = A B^T (integer counts <a_i,b_j> in {0,...,d}, rank <= d, FACTORED). ans = max_{i,j} M_{ij}.")
    print("The required novelty: MAX-EXTRACTION-WITHOUT-ENUMERATION (compute the max without materializing")
    print("all n^2 entries). Each candidate fuses a genuine subquadratic aggregate but cannot deliver the max.\n")

    # ---------------------------------------------------------------------
    # C1: MOMENT / tensor-power counting-MM.
    # ---------------------------------------------------------------------
    print("--- C1: MOMENT / tensor-power counting-MM ---\n")
    print("FUSION: m_p = sum_{i,j} <a_i,b_j>^p = < sum_i a_i^{tensor p}, sum_j b_j^{tensor p} > in dim d^p.")
    print("(a) Identity grounding: the fused contraction equals the brute-force sum over pairs (exact).")
    rng = np.random.default_rng(1)
    id_ok = True
    for (n, d) in [(5, 4), (6, 3), (7, 5)]:
        A = (rng.random((n, d)) < 0.5).astype(np.int64)
        B = (rng.random((n, d)) < 0.5).astype(np.int64)
        for p in (1, 2, 3):
            m_id = moment_via_tensor_identity(A, B, p)
            m_bf = moment_via_bruteforce(A, B, p)
            agree = abs(m_id - m_bf) < 1e-6
            id_ok = id_ok and agree
            print(f"    n={n} d={d} p={p}: fused m_p = {m_id:10.1f}  brute m_p = {m_bf:10.1f}  agree={agree}")
    print()

    print("(b) INFORMATION wall (Vandermonde): matching m_1..m_K leaves the max free iff K <= d-1.")
    coll = explicit_moment_collision()
    print(f"    explicit witness: X = {coll['X']}, Y = {coll['Y']} (count-multisets of a 2x2 product, d=3)")
    print(f"      m_1(X)={coll['m1_X']}  m_1(Y)={coll['m1_Y']}  equal={coll['m1_equal']}")
    print(f"      m_2(X)={coll['m2_X']}  m_2(Y)={coll['m2_Y']}  equal={coll['m2_equal']}")
    print(f"      max(X)={coll['max_X']}  max(Y)={coll['max_Y']}  DIFFER={coll['max_differs']}")
    print(f"    so P=2 moments provably cannot tell max=3 from max=2. Nullspace dims (free directions):")
    for d in (4, 8, 16, 20):
        free_full = vandermonde_nullspace_dim(d, d)
        free_at_half = vandermonde_nullspace_dim(d, d // 2)
        print(f"      d={d:2d}: after m_1..m_{d} free dim = {free_full} (pinned); after m_1..m_{d//2} free dim = {free_at_half} (max NOT pinned)")
    print()

    print("(c) COST window: subquadratic only for P < 1/eps; the affordable window is polynomial (eps = %.2f)." % EPS)
    print(f"    {'P':>3} | {'cost exp 1+P*eps':>16} | {'subquadratic?':>13} | {'window n^{2/P} (log_n)':>22}")
    print("    " + "-" * 62)
    for P in (1, 2, 4, 9, 10, 11):
        b = moment_budget(EPS, P)
        print(f"    {P:>3} | {b.cost_exponent:>16.3f} | {('YES' if b.subquadratic else 'no'):>13} | "
              f"{b.window_log2n_factor:>22.4f}")
    print()
    print("(d) The useful regime is DISJOINT from the subquadratic one. To clear the n^2-strong bulk and")
    print("    to resolve v vs v-1 (the gap-1 decision the THR-of-THR connection needs):")
    for n in (256.0, 1e6, 2.0 ** 50):
        P_bulk = moments_to_clear_bulk(n, 0.25)
        P_unit = moments_to_resolve_unit(n, n ** EPS)
        print(f"      n={n:.3g}: clear-bulk P > {P_bulk:8.2f} = Omega(log n);  unit-resolution P > {P_unit:10.2f} "
              f"= Omega(n^eps log n)")
    print("    Each extra moment multiplies cost by d = n^eps, so the useful P costs n^{1+omega(1)}.\n")

    # ---------------------------------------------------------------------
    # C2: SPECTRAL / low-rank.
    # ---------------------------------------------------------------------
    print("--- C2: SPECTRAL / low-rank ---\n")
    print("(a) Equal-spectrum / different-max: spread (u=v=ones/sqrt n) vs spike (e_1 e_1^T).")
    print(f"    {'n':>6} | {'max_spread':>12} | {'max_spike':>10} | {'max_ratio':>10} | {'spectra equal?':>14}")
    print("    " + "-" * 60)
    spec_ratios = []
    for n in (16, 64, 256, 1024, 4096):
        r = equal_spectrum_different_max(n)
        spec_ratios.append((n, r["max_ratio"], r["spectra_equal"]))
        print(f"    {n:>6} | {r['max_spread']:>12.6f} | {r['max_spike']:>10.4f} | {r['max_ratio']:>10.1f} | "
              f"{str(r['spectra_equal']):>14}")
    print("    same spectrum, max-ratio EXACTLY n: the rotation-invariant certificate misses a Theta(n) factor.\n")

    print("(b) CORRECTION (adversary): the window is NOT the binding wall. A cheap NON-invariant bound")
    print("    (per-factor-row Cauchy-Schwarz, O(n d)) is multiplicatively TIGHT on dense Boolean data,")
    print("    while the spectral-norm window is wide. So the operative wall is integer-resolution +")
    print("    localization (the enumeration wall), not rotation-invariance.")
    rng2 = np.random.default_rng(7)
    for (n, d) in [(200, 8), (1000, 8), (2000, 45)]:
        A = (rng2.random((n, d)) < 0.5).astype(np.int64)
        B = (rng2.random((n, d)) < 0.5).astype(np.int64)
        w = cheap_cauchyschwarz_window(A, B)
        print(f"    n={n:>4} d={d:>3}: true_max={w['true_max']:>4.0f}  CS bound={w['cs_bound']:>7.2f} "
              f"(window {w['cs_window']:.2f}x)  ||M||_2={w['spectral_norm']:>8.2f} (window {w['spectral_window']:.1f}x)")
    print("    CS window ~ 1.0-1.25x (tight) but still gives neither the integer value nor the argmax pair:")
    print("    resolving max vs max-1 and finding the argmax both collapse to the n^2 scan. That is the wall.\n")
    print("    BARRIER NOTE: marking the avenue 'doubly barrier-blocked' (natural AND algebrizing) is a")
    print("    category error. Razborov-Rudich and Aaronson-Wigderson act on a hypothetical lower-bound")
    print("    CERTIFICATE, not on an algorithmic log-shave. The avenue is barrier-free; it dies internally.\n")

    # ---------------------------------------------------------------------
    # C3: COUNT-PRESERVING REGULARITY.
    # ---------------------------------------------------------------------
    print("--- C3: COUNT-PRESERVING REGULARITY ---\n")
    reg = regularity_planted_spike(seed=3)
    print(f"pseudorandom instance: n={reg['n']}, d={reg['d']}, rho={reg['rho']} (p=sqrt(rho), E[<a,b>]=d*rho).")
    print(f"  bulk mean (density-predicted)               : {reg['bulk_mean']:.2f}")
    print(f"  observed pseudorandom max (no plant)        : {reg['bulk_max']}  "
          f"(deviation {reg['bulk_deviation']:.1f} above the mean)")
    print(f"  order-statistic deviation sigma*sqrt(2 ln N): {reg['order_stat_deviation']:.1f}  "
          f"(the tail the DENSITY cannot resolve)")
    print(f"  plant B[0] = A[0]: <a_0,b_0> = popcount(a_0) = {reg['planted_value_popcount_a0']} (a Theta(d) r.v.)")
    print(f"  global max after plant                      : {reg['plant_max']}  "
          f"(jump {reg['max_jump']} = Theta(d))")
    print(f"  column density of B before / after plant    : {reg['densB_before']:.4f} / {reg['densB_after']:.4f}  "
          f"(moved {reg['density_move']:.5f} = O(1/n), 1/n = {reg['one_over_n']:.5f})")
    print("  CONCLUSION: the max moved Theta(d) while every density statistic moved O(1/n). The averaging")
    print("  engine (regularity certifies densities to additive eps_reg*d) is BLIND to the planted extreme.\n")
    print("  STEP 2 dichotomy: read each block's max off its density. heuristic = WRONG (blind to the tail);")
    print("  exact = a recursive oracle for the very fused-max-MM problem at smaller scale = CIRCULAR. No third option.\n")
    print("  Granularity cost of single-unit precision (eps_reg < 1/d forces B = 2^{O(d^2)} blocks):")
    print(f"    {'eps':>5} | {'log2 n':>7} | {'log2 d = eps*log2n':>18} | {'log2(#blocks) ~ d^2':>20} | {'log2(n^2)':>10}")
    print("    " + "-" * 70)
    for eps in (0.1, 0.2):
        for log2n in (64.0, 256.0, 1024.0):
            g = regularity_granularity_cost(eps, log2n)
            print(f"    {eps:>5.1f} | {log2n:>7.0f} | {g['log2d']:>18.2f} | {g['weak_reg_block_exponent_d2']:>20.3e} | "
                  f"{g['log2_n_squared']:>10.0f}")
    print("    d^2 >> 2*log2(n) always: correctness forces 2^{Omega(n^{2eps})} blocks, super-exponentially past n^2.\n")

    # ---------------------------------------------------------------------
    # C4: SKETCH / heavy-hitter.
    # ---------------------------------------------------------------------
    print("--- C4: SKETCH / heavy-hitter ---\n")
    print("(a) HEAVINESS wall (the SOUND obstruction): on dense M the argmax is L2-LIGHT.")
    print(f"    {'n':>5} | {'d':>4} | {'heaviness ratio':>16} | {'ratio*n^2':>10} | {'width forced 1/ratio':>20}")
    print("    " + "-" * 66)
    for n in (16, 32, 64, 128):
        d = max(2, round(n ** EPS))     # d floored to a small constant; the Theta(1/n^2) scaling is robust
        h = heaviness_ratio(n, d, seed=0)
        print(f"    {n:>5} | {d:>4} | {h['heaviness_ratio']:>16.3e} | {h['ratio_times_n2']:>10.2f} | "
              f"{h['width_heavy']:>20.1f}")
    print("    heaviness ratio ~ Theta(1/n^2) (ratio*n^2 stays a small constant), independent of d; the")
    print("    count-sketch width forced 1/ratio ~ n^2 (super-polylog). This is the SOUND binding wall.\n")
    print("    The integer-gap-1 width is s > ||M||_F^2/gap^2 = n^2 * E[M_ij^2], and E[M_ij^2] = (d/4)^2 +")
    print("    3d/16 = Theta(d^2) GROWS with d (a factor Theta(d^2) WORSE than n^2). Measured at fixed n=256:")
    print(f"      {'d':>4} | {'E[M_ij^2] = fro2/n^2':>20} | {'gap-1 width / n^2':>18}")
    print("      " + "-" * 46)
    EM2_by_d = []
    for d in (2, 8, 32, 128):
        hd = heaviness_ratio(256, d, seed=0)
        EM2_by_d.append((d, hd["EM2"]))
        print(f"      {d:>4} | {hd['EM2']:>20.3f} | {hd['width_gap1_over_n2']:>18.3f}")
    print("    E[M_ij^2] grows ~ d^2/16, so once d is not tiny the gap-1 sketch dimension exceeds n^2 by Theta(d^2).\n")

    print("(b) CORRECTION (adversary): the builder's 'one-sparse recovery forces s = Omega(n^2)' is WRONG.")
    print("    Deterministic for-all 1-sparse recovery needs only ceil(log2 N)+1 linear measurements:")
    sp = one_sparse_recovery_is_cheap(256)
    print(f"      N={sp['N']}: bit-encoding sketch rows = {sp['rows']} (= ceil(log2 N)+1 = {sp['ceil_log2_N_plus_1']}); "
          f"recovered location={sp['recovered_location']}, value={sp['recovered_value']}.")
    print("    The 'collision' the builder exhibited exists ONLY because the target column is hand-zeroed;")
    print("    a random sketch never collides on a single-cell difference. The DIFFERENCE is 1-sparse (cheap);")
    print("    what is hard is reading the L^infinity max of a DENSE M from a linear sketch (= part (a)).\n")

    print("(c) The single-entry-difference instance (grounds that the difference is 1-sparse, rank <= d):")
    sed = single_entry_difference_factored(8, 6, seed=3)
    if sed.get("ok"):
        print(f"      n=8 d=6: flip one B-bit at (j*={sed['j_star']}, k*) set in exactly one A-row i*={sed['i_star']};")
        print(f"      products differ in {sed['num_diff_cells']} cell by +{sed['diff_value']} "
              f"(exactly one +1 = {sed['exactly_one_plus_one']}), rank <= d preserved = {sed['rank_ok']}.")
    print()

    # ---------------------------------------------------------------------
    # Summary ledger.
    # ---------------------------------------------------------------------
    print("--- SUMMARY LEDGER: four fused-max-MM engines, four precise NEGATIVES ---\n")
    ledger = build_candidate_ledger()
    hdr = f"{'candidate':<38} | {'barrier-free?':>13} | {'secret speedup risk':>20}"
    print(hdr)
    print("-" * len(hdr))
    for r in ledger:
        print(f"{r.name[:38]:<38} | {('YES' if r.barrier_free else 'no'):>13} | {r.secret_speedup_risk[:20]:>20}")
    print()
    for r in ledger:
        print(f"  {r.name}")
        print(f"    fuses           : {r.fuses_what}")
        print(f"    obstruction     : {r.obstruction}")
        print(f"    quantified wall : {r.quantified_wall}")
        print()

    # ======================================================================
    # Self-checks pinning every coordinate. Module must exit 0.
    # ======================================================================

    # --- C1 self-checks ---
    # (C1.0) REUSE grounding: brute-force Max-IP = global max of A B^T (the count-then-max structure).
    for seed in (0, 7, 21):
        rr = np.random.default_rng(seed)
        AA = (rr.random((8, 10)) < 0.5).astype(np.int64)
        BB = (rr.random((9, 10)) < 0.5).astype(np.int64)
        m_bf2 = max_ip_bruteforce(AA, BB)
        m_mp2, MM = max_ip_matrix_product(AA, BB)
        assert m_bf2 == m_mp2 == int(MM.max()), \
            "REUSED baseline: brute-force Max-IP = global max of A B^T (count-then-max structure)"

    # (C1.1) The fusion identity holds EXACTLY (m_p via tensor power-sum = brute sum over pairs).
    assert id_ok, "the tensor identity m_p = <sum a^{tp}, sum b^{tp}> must equal sum_{i,j} M_{ij}^p exactly"
    rng_c = np.random.default_rng(99)
    for (n, d) in [(4, 3), (6, 4)]:
        A = (rng_c.random((n, d)) < 0.5).astype(np.int64)
        B = (rng_c.random((n, d)) < 0.5).astype(np.int64)
        for p in (1, 2, 3):
            assert abs(moment_via_tensor_identity(A, B, p) - moment_via_bruteforce(A, B, p)) < 1e-6, \
                "fusion identity must hold to 1e-6"

    # (C1.2) The Vandermonde information wall: matching m_1..m_K leaves the max free iff K <= d-1.
    assert coll["m1_equal"] and coll["m2_equal"] and coll["max_differs"], \
        "explicit witness {3,1,1,1} vs {2,2,2,0}: identical m_1,m_2 but different max (P=2 cannot resolve)"
    for d in (4, 8, 16, 20):
        assert vandermonde_nullspace_dim(d, d) == 0, \
            "after m_1..m_d (all d+1 moments m_0..m_d) the value-multiset is pinned (no free direction)"
        assert vandermonde_nullspace_dim(d, d - 1) > 0, \
            "after only m_1..m_{d-1} (K = d-1) one free direction remains: the max is NOT determined"

    # (C1.3) The subquadratic budget is P < 1/eps (a constant) and gives only a polynomial window.
    assert moment_budget(EPS, 9).subquadratic and not moment_budget(EPS, 10).subquadratic, \
        "at eps=0.1, P<=9 is subquadratic, P=10 hits exponent 2.0 (P < 1/eps is the ceiling)"
    assert moment_budget(EPS, 9).window_log2n_factor > EPS, \
        "the affordable window n^{2/P} at the largest subquadratic P is a polynomial factor (> n^eps)"

    # (C1.4) The useful regime is DISJOINT: clear-bulk P = Omega(log n), unit-resolution P = Omega(d log n).
    n_big = 2.0 ** 50
    P_bulk = moments_to_clear_bulk(n_big, 0.25)
    P_unit = moments_to_resolve_unit(n_big, n_big ** EPS)
    assert P_bulk > 1.0 / EPS, "clearing the bulk needs Omega(log n) moments, far above the subquadratic P < 1/eps"
    assert P_unit > P_bulk, "unit (v vs v-1) resolution needs even more moments (Omega(d log n))"

    # --- C2 self-checks ---
    # (C2.1) Equal-spectrum / different-max: spectra match, max-ratio is exactly n.
    for (n, ratio, eq) in spec_ratios:
        assert eq, "the spread and spike rank-1 matrices have identical spectra"
        assert abs(ratio - n) < 1e-6, "the equal-spectrum pair has max-ratio EXACTLY n (Theta(n) window)"

    # (C2.2) CORRECTION: a cheap non-invariant CS bound is multiplicatively tight, so the window is NOT
    #        the binding wall. (The avenue still dies, at integer-resolution + localization.)
    rng_c2 = np.random.default_rng(123)
    A = (rng_c2.random((1000, 8)) < 0.5).astype(np.int64)
    B = (rng_c2.random((1000, 8)) < 0.5).astype(np.int64)
    w = cheap_cauchyschwarz_window(A, B)
    assert w["cs_window"] <= 2.0, \
        "the per-factor-row CS bound is multiplicatively tight (<= 2x) on dense data: the window is NOT binding"
    assert w["spectral_window"] > w["cs_window"], \
        "the spectral-norm window is wider than the cheap CS window (rotation-invariance is not the operative wall)"

    # --- C3 self-checks ---
    # (C3.1) Planted spike: max jumps Theta(d) while every density moves O(1/n).
    assert reg["max_jump"] > 0, "planting B[0]=A[0] raises the global max"
    assert reg["density_move"] <= 2.0 / reg["n"] + 1e-9, \
        "the planted pair moves the column density by O(1/n) (it changed exactly one row of B)"
    assert reg["max_jump"] > 10 * reg["density_move"] * reg["d"], \
        "the max jump (Theta(d)) dwarfs the density move scaled by d: the averaging engine is blind to the extreme"
    # The deviation the density cannot resolve is order sqrt(d log n), positive and Theta of the formula.
    assert reg["order_stat_deviation"] > 0 and reg["bulk_deviation"] > 0, \
        "the bulk max sits a sqrt(d log n)-order deviation above the density-predicted mean"

    # (C3.2) Granularity cost: single-unit precision forces 2^{Omega(n^{2eps})} blocks >> n^2.
    for eps in (0.1, 0.2):
        g = regularity_granularity_cost(eps, 256.0)
        assert g["weak_reg_block_exponent_d2"] > g["log2_n_squared"], \
            "log2(#blocks) ~ d^2 >> log2(n^2): correctness forces super-exponentially more blocks than n^2"

    # --- C4 self-checks ---
    # (C4.1) The heaviness ratio is Theta(1/n^2) (ratio*n^2 a small constant), so width forced ~ n^2.
    #        This is the SOUND binding wall, robust at any d (including the floored small d).
    rtn2 = []
    for n in (16, 32, 64, 128):
        d = max(2, round(n ** EPS))
        h = heaviness_ratio(n, d, seed=0)
        rtn2.append(h["ratio_times_n2"])
        assert h["width_heavy"] > 0, "the forced count-sketch width is positive"
        # The count-sketch width forced (1/ratio) grows like n^2 (heaviness ratio Theta(1/n^2)).
        assert h["width_heavy"] > 0.5 * n * n / max(rtn2[-1], 1.0), \
            "the heavy-hitter width forced 1/ratio is Theta(n^2): the dense argmax is L2-light"
    assert max(rtn2) < 100.0, \
        "ratio*n^2 stays a small constant across n: the argmax is L2-LIGHT (heaviness Theta(1/n^2))"
    # The integer-gap-1 width per n^2 is E[M_ij^2] = Theta(d^2): it GROWS with d, exceeding 1 once
    # d is not tiny, so the gap-1 sketch dimension is a factor Theta(d^2) WORSE than n^2.
    em2 = [heaviness_ratio(256, d, seed=0)["EM2"] for d in (2, 8, 32, 128)]
    assert all(em2[i] < em2[i + 1] for i in range(len(em2) - 1)), \
        "E[M_ij^2] = fro2/n^2 grows with d (Theta(d^2)): the gap-1 sketch width is Theta(n^2 d^2), worse than n^2"
    assert em2[-1] > 1.0, \
        "at moderate d the gap-1 sketch width exceeds n^2 (the argmax cannot be resolved sub-n^2)"

    # (C4.2) CORRECTION: 1-sparse recovery is CHEAP (O(log N)), refuting the Omega(n^2) framing.
    for N in (64, 256, 1024):
        sp = one_sparse_recovery_is_cheap(N)
        assert sp["recovered_location"] and sp["recovered_value"], \
            "deterministic for-all 1-sparse recovery succeeds in ceil(log2 N)+1 measurements (NOT Omega(N))"
        assert sp["rows"] <= (N - 1).bit_length() + 1, \
            "the bit-encoding sketch uses O(log N) rows: the '1-sparse => Omega(n^2)' framing is WRONG"

    # (C4.3) The single-entry-difference instance: products differ in exactly one +1 cell, rank <= d.
    assert sed.get("ok") and sed["exactly_one_plus_one"] and sed["rank_ok"], \
        "the factored single-entry-difference instance: exactly one +1 cell, rank <= d preserved (difference is 1-sparse)"

    # --- ledger self-checks ---
    ledger_check = build_candidate_ledger()
    assert len(ledger_check) == 4, "the ledger pins all four fused-max-MM candidates"
    assert all(r.barrier_free for r in ledger_check), \
        "all four candidates are barrier-free (they die for internal reasons, not a barrier)"
    assert all("none" in r.secret_speedup_risk for r in ledger_check), \
        "none of the four secretly shaves (the speedup is never present at the max-extraction step)"

    print("=== Self-check OK ===")
    print("(C1) MOMENT: the fusion identity m_p = <sum a^{tp}, sum b^{tp}> = sum_{i,j} M_{ij}^p holds EXACTLY.")
    print("     INFORMATION wall: matching m_1..m_K leaves the max free iff K <= d-1 (Vandermonde nullspace;")
    print("     witness {3,1,1,1} vs {2,2,2,0} share m_1,m_2 but differ in max). Subquadratic only for P < 1/eps")
    print("     (window n^{2/P} polynomial); clearing the bulk needs P=Omega(log n), unit resolution P=Omega(n^eps log n).")
    print("(C2) SPECTRAL: equal-spectrum/different-max pair has max-ratio EXACTLY n, BUT a cheap non-invariant CS")
    print("     bound is multiplicatively tight (<= 2x), so the Theta(n) window is NOT the binding wall. The")
    print("     operative wall is integer-gap-1 resolution + argmax localization (the enumeration wall). The")
    print("     avenue is barrier-free (the natural/algebrization 'block' is a category error on the algorithm).")
    print("(C3) REGULARITY: the planted pair raises the max by Theta(d) while every density moves O(1/n); the")
    print("     averaging engine is blind to the extreme. Single-unit precision forces 2^{Omega(n^{2eps})} blocks")
    print("     >> n^2. STEP 2 is heuristic=wrong / exact=circular.")
    print("(C4) SKETCH: on dense M the argmax is L2-LIGHT (heaviness Theta(1/n^2)), so count-sketch width forced")
    print("     ~ n^2 (integer-gap width Theta(n^2 d^2), since E[M_ij^2]=Theta(d^2)). CORRECTION: the")
    print("     '1-sparse => Omega(n^2)' framing is WRONG (1-sparse recovery is O(log N)); the binding wall is")
    print("     L^infinity-from-L2 lightness of the dense argmax.")
    print()
    print("VERDICT: all four are precise, quantified NEGATIVES. Each fuses a genuine subquadratic aggregate of")
    print("all n^2 inner products but cannot extract the L^infinity max. The fused-max-MM frontier is OPEN and")
    print("barrier-free: the missing idea must extract an EXTREME value (not an average / L2 / moment / linear")
    print("sketch) from a factored low-rank Boolean count matrix without enumeration. No speedup claimed; no")
    print("progress on the prize.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
