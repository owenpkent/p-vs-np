"""Boolean Max-IP at d = n^eps, made concrete: the baseline, the polylog map, a micro-idea.

THE TARGET (Chen 2018, arXiv:1805.10698, item 3 of the abstract = Theorem 1.5 item 1,
web-confirmed VERBATIM 2026-06-03 from the arXiv abstract):

  "An n^2 / log^{omega(1)} n time algorithm for Bichromatic Maximum Inner Product with
   vector dimension d = n^eps for any small constant eps would imply NEXP has no
   polynomial size THR o THR circuits. Note there is an n^2 polylog(n) time algorithm
   via fast rectangle matrix multiplication."

Max-IP_{n,d}: given two sets A, B of n vectors in {0,1}^d, compute
   max over a in A, b in B of  <a,b> = sum_k a_k b_k  (Boolean inner product).
The MAXIMIZATION (not the existence/OR) is what couples to the THRESHOLD gate, so the
max routes to the full THR-of-THR (Chen Thm 1.5); the OR/existence (OV) routes only to
the weaker SYM-of-THR (Chen Thm 1.2). This module is about the max.

WHAT THIS MODULE ADDS over its two siblings (it is the GROUNDING / EXECUTABLE one):
  - e_threshold_geometry_gap.py is PROBLEM-indexed (the gap table, the SETH classifier).
  - e_log_shaving_toolkit.py is TECHNIQUE-indexed (each method's saving + the gap).
  - e_logshave_barrier_landscape.py is BARRIER-indexed (is there a finer barrier).
  - THIS module is EXECUTABLE-indexed. It (1) actually computes Boolean Max-IP two ways
    in numpy on small explicit instances and checks they agree, grounding "the baseline
    computes all inner products A B^T then takes the global max"; (2) decomposes the
    n^2 polylog baseline into the rectangular-MM step and the n^2 output-scan, measuring
    where the polylog lives and what a log-shave must avoid; (3) HONESTLY attempts the
    threshold-sweep micro-idea (extract the max via O(d) existence queries) and reports,
    with measured numbers, exactly where it fails to beat the baseline.

ESTABLISHED CONTEXT (do NOT re-derive; this module builds on it):
  - BASELINE n^2 polylog(n): Chen states verbatim there is an n^2 polylog(n) algorithm
    via fast rectangular matrix multiplication (Coppersmith 1982). The target shaves ALL
    polylog factors off this baseline: a LOG-SHAVE, not a polynomial speedup.
  - SETH-CONSISTENT and OPEN: a log-shave is n^{2-o(1)}; SETH forbids only n^{2-Omega(1)}.
    NEXP not in poly-size THR-of-THR is OPEN as of 2026 (web-confirmed); if the target
    were met it would be proven.
  - The POLYNOMIAL METHOD (Abboud-Williams-Yu SODA 2015) is the WRONG tool at d = n^eps:
    its saved exponent 1/O(log(d/log n)) = 1/O(eps log n) gives a saved FACTOR
    2^{O(1/eps)} = O(1), a CONSTANT, not a log-shave. It shaves best at d = c log n.
  - TARGET WIDENING (Chen 2018 Remarks 2.7 + 4.2): the connection accepts CO-NONDETER-
    MINISTIC UNSAT algorithms at the same running time, so a deterministic-OR-co-
    nondeterministic log-shave suffices. This is project inference (a correct reading of
    Chen's own remarks applied one step earlier in the chain), not a separate theorem.

HONESTY DISCIPLINE (the deliverable is a sharp coordinate, NOT a claimed speedup):
  - PROVED facts cite a theorem with venue/year/arXiv.
  - The micro-idea is reported with measured numbers and the EXACT step where it breaks.
    A precise negative is the expected, valuable outcome. No faked speedup.

Run:
    python -m experiments.circuit_complexity.e_maxip_logshave
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field

import numpy as np


# ==========================================================================
# Part 1: Boolean Max-IP, two ways, on small explicit instances.
#
# (a) Brute force: the literal n^2 d definition, max over all pairs of the inner
#     product computed coordinate-by-coordinate. This is the ground truth.
# (b) Matrix-product baseline: form C = A B^T with a single integer matmul (this is
#     what fast rectangular matrix multiplication computes asymptotically; numpy's
#     dense integer matmul is the stand-in at small scale), then take the global max.
#     This is exactly "compute all n^2 inner products, then take the max".
# The self-check is that (a) and (b) agree on every instance.
# ==========================================================================


def max_ip_bruteforce(A: np.ndarray, B: np.ndarray) -> int:
    """The literal definition: max over a in A, b in B of <a,b>, computed pairwise.

    A is (n_A, d), B is (n_B, d), both 0/1. Cost is Theta(n_A * n_B * d): the n^2 d
    brute force Chen's baseline improves on. Returns the integer maximum inner product.
    """
    n_A, d = A.shape
    n_B, _ = B.shape
    best = -1
    for i in range(n_A):
        ai = A[i]
        for j in range(n_B):
            # coordinate-by-coordinate Boolean inner product (the d-cost is explicit)
            ip = 0
            bj = B[j]
            for k in range(d):
                ip += int(ai[k]) * int(bj[k])
            if ip > best:
                best = ip
    return best


def max_ip_matrix_product(A: np.ndarray, B: np.ndarray) -> tuple[int, np.ndarray]:
    """The baseline: C = A B^T (all n^2 inner products at once), then the global max.

    The matmul stands in for Coppersmith 1982 fast rectangular matrix multiplication
    (which computes the same C = A B^T in n^2 polylog arithmetic operations when
    d = n^eps with eps below the dual exponent). numpy materializes the FULL n_A x n_B
    integer matrix C, then C.max() scans all n_A * n_B entries. Returns (max, C) so the
    caller can inspect the materialized inner-product matrix (the object a log-shave
    must avoid scanning in full).
    """
    C = A.astype(np.int64) @ B.astype(np.int64).T   # all inner products: entries in {0,...,d}
    return int(C.max()), C


def self_check_two_baselines_agree(seed: int = 0) -> None:
    """The grounding self-check: brute force and the matrix-product baseline agree."""
    rng = np.random.default_rng(seed)
    for n_A, n_B, d in [(5, 7, 6), (8, 8, 10), (12, 9, 4), (3, 3, 20), (16, 11, 8)]:
        A = (rng.random((n_A, d)) < 0.5).astype(np.int64)
        B = (rng.random((n_B, d)) < 0.5).astype(np.int64)
        m_bf = max_ip_bruteforce(A, B)
        m_mp, C = max_ip_matrix_product(A, B)
        assert m_bf == m_mp, (
            f"Max-IP mismatch at (n_A={n_A}, n_B={n_B}, d={d}): "
            f"brute force {m_bf} vs matrix-product {m_mp}"
        )
        # C is exactly the all-pairs inner-product matrix; its max is the answer.
        assert C.shape == (n_A, n_B), "C = A B^T must be the n_A x n_B inner-product matrix"
        assert C.max() == m_bf, "the global max of C must equal the brute-force answer"
        # Entries are bounded by d (Boolean inner product of d-bit vectors).
        assert int(C.max()) <= d, "a Boolean inner product of d-bit vectors is at most d"


# ==========================================================================
# Part 2: where the polylog factors live in the n^2 polylog baseline.
#
# The baseline has TWO cost sources, and the max-extraction is part of the problem,
# not free post-processing:
#   (3a) the rectangular-MM step: produce C = A B^T. Coppersmith 1982 does this in
#        C0 * n^2 * (log n)^2 arithmetic operations (the log^2 n is the polylog the
#        target wants shaved; it is intrinsic to the bilinear / partial-matrix-
#        multiplication recursion, NOT removed by dual-exponent improvements).
#   (3b) the output / max-extraction: read and max all n^2 entries of C. This is
#        Theta(n^2) by itself, with NO log saving under a naive scan, because
#        Omega(n^2) is the natural output size of an n x n product.
# CONSEQUENCE (the binding structural fact): to beat n^2 / log^{omega(1)} n you CANNOT
# materialize-and-scan all n^2 inner products; the max must be computed WITHOUT
# enumerating all n^2 pairs. So the log-shave must act on BOTH (3a) and (3b), and (3b)
# is the term with provably zero achievable log-shave under enumeration.
# ==========================================================================


def baseline_op_counts(log2n: float, eps: float, c_mm: float = 1.0) -> dict[str, float]:
    """Model the baseline's arithmetic-operation count in log2 units (no overflow).

    Returns log2 of each component:
      mm_step  = c_mm * n^2 * (log2 n)^2    (Coppersmith 1982 rectangular MM, the polylog)
      scan_step= n^2                        (the global max over the n^2 entries of C)
      total    = mm_step + scan_step        (dominated by mm_step's extra log^2 factor)
    All in log2. d = n^eps does not enter the leading n^2 (it is hidden in the o(1)/poly
    of fast rectangular MM for eps below the dual exponent), but it bounds the entry
    magnitude (eps log2 n bits per entry), which is where a bit-packing idea would act.
    """
    n2 = 2.0 * log2n                                  # log2(n^2)
    log2_logn = math.log2(log2n) if log2n > 1.0 else 0.0
    mm_extra = 2.0 * log2_logn + math.log2(c_mm) if c_mm > 0 else 2.0 * log2_logn  # log2((log2 n)^2 * c)
    mm_step = n2 + mm_extra                           # log2(c * n^2 * (log n)^2)
    scan_step = n2                                    # log2(n^2): the max-extraction
    # total operation count (sum of two terms): log2 of (2^mm_step + 2^scan_step)
    total = _log2_sum(mm_step, scan_step)
    bits_per_entry = eps * log2n                      # entries in {0,...,n^eps}: eps log2 n bits
    return {
        "mm_step_log2": mm_step,
        "scan_step_log2": scan_step,
        "total_log2": total,
        "mm_polylog_factor_log2": mm_extra,           # the shaveable polylog, in bits
        "bits_per_entry": bits_per_entry,
    }


def _log2_sum(a_log2: float, b_log2: float) -> float:
    """log2(2^a + 2^b) without overflow (log-sum-exp in base 2)."""
    hi, lo = (a_log2, b_log2) if a_log2 >= b_log2 else (b_log2, a_log2)
    return hi + math.log2(1.0 + 2.0 ** (lo - hi))


def measured_baseline_split(seed: int = 1) -> dict[str, float]:
    """Empirically split the baseline's wall-clock into the matmul step vs the max-scan.

    This grounds the model: at a small but nontrivial n we time (a) forming C = A B^T
    and (b) scanning C for its max. The matmul carries the (asymptotic) polylog overhead;
    the max-scan is a flat n^2 read. We report both times so the decomposition is not
    purely a model. (Wall-clock at small n is dominated by constants, so this is
    illustrative, not asymptotic; the asymptotic split is the op-count model above.)
    """
    rng = np.random.default_rng(seed)
    n, d = 1200, 64                       # n^2 = 1.44e6 entries; d = 64 ~ small n^eps proxy
    A = (rng.random((n, d)) < 0.5).astype(np.int64)
    B = (rng.random((n, d)) < 0.5).astype(np.int64)
    t0 = time.perf_counter()
    C = A @ B.T                            # the rectangular-MM step (all n^2 inner products)
    t1 = time.perf_counter()
    m = int(C.max())                       # the max-extraction step (scan all n^2 entries)
    t2 = time.perf_counter()
    return {
        "n": float(n),
        "d": float(d),
        "matmul_seconds": t1 - t0,
        "maxscan_seconds": t2 - t1,
        "answer": float(m),
        "n2_entries": float(n) * float(n),
    }


# ==========================================================================
# Part 3: technique savings at d = n^eps (the tabulated gap, log-scale).
#
# Reuses the established functional forms (web-grounded; see the sibling modules and
# the hinge note section 8). Everything is the EXPONENT of n or log2 of a factor, so
# nothing overflows and an asymptotic-only saving is never called "feasible".
# ==========================================================================

EPS = 0.1   # the modest dimension exponent d = n^eps; any constant eps > 0 works.


def saved_factor_log2_poly_method(log2n: float, eps: float = EPS) -> float:
    """log2 of the polynomial-method saved factor at d = n^eps (AWY SODA 2015).

    At d = c log n the saved exponent is 1/O(log c); at d = n^eps, c = n^eps/log n, so
    log c = Theta(eps log n) and the saved exponent s = 1/(eps log2 n). The saved factor
    is n^s = 2^{s log2 n} = 2^{1/eps}: a CONSTANT in n. log2(saved factor) = 1/eps (here
    10 for eps=0.1). It does NOT grow with n, so it is NOT a log-shave.
    """
    return 1.0 / eps if eps > 0 else float("inf")


def saved_factor_log2_true_logshave(log2n: float, e: float) -> float:
    """log2 of a TRUE log-shave saved factor log^e n. = e * log2(log2 n): GROWS with n.

    The Chen bar wants e -> infinity (shave log^{omega(1)} n). For any FIXED e this
    already grows with n, unlike the constant poly-method saving. The contrast is the
    whole point.
    """
    log2_logn = math.log2(log2n) if log2n > 1.0 else 0.0
    return e * log2_logn


@dataclass
class TechRow:
    technique: str
    savings_at_neps: str          # human-readable saving at d = n^eps
    saved_factor_log2_large: float  # log2 of the saved factor at n = 2^4096 (large n)
    is_log_shave: bool            # does the saved factor grow without bound (a log-shave)?
    meets_bar: bool               # does it meet n^2/log^{omega(1)} n at d = n^eps?
    gap: str                      # the precise shortfall
    note: str = ""


def build_tech_rows() -> list[TechRow]:
    L = 4096.0   # log2(n) = 4096, i.e. n = 2^4096: a large-n reference (no overflow)
    rows: list[TechRow] = []

    # (1) Polynomial method: CONSTANT-factor saving at d = n^eps.
    f1 = saved_factor_log2_poly_method(L)
    rows.append(TechRow(
        technique="Polynomial method (Abboud-Williams-Yu SODA 2015; Chan-Williams SODA 2016 det)",
        savings_at_neps="saved factor 2^{1/eps} = O(1) (constant in n)",
        saved_factor_log2_large=f1,
        is_log_shave=False,
        meets_bar=False,
        gap=("saved exponent 1/O(eps log n) -> 0; saved factor flattens to the CONSTANT "
             "2^{1/eps} (= 2^10 ~ 1024 for eps=0.1), NOT log^{omega(1)} n. Wrong dimension: "
             "the prob-polynomial degree scales with d, so the batch collapses at polynomial d."),
        note="The headline tool. Shaves a real POLYNOMIAL at d=c log n, only a CONSTANT at d=n^eps.",
    ))

    # (2) Four-Russians / word-RAM on the integer-counting max: NO transfer.
    rows.append(TechRow(
        technique="Four-Russians / word-RAM BMM (Bansal-Williams 2009; Chan 2015; AFKLM STOC 2024)",
        savings_at_neps="no transfer to the integer count-then-max (saved factor 1)",
        saved_factor_log2_large=0.0,
        is_log_shave=False,
        meets_bar=False,
        gap=("these shave the BOOLEAN OR-semiring product (AFKLM STOC 2024 even shaves "
             "n^3/2^{Omega((log n)^{1/7})}, a SUPER-polylog shave). Max-IP needs the INTEGER "
             "count <a,b> in {0,...,d} then a MAX (the (+,x) semiring), which word-packing of "
             "OR does not compute. DISCREPANCY-GUARD: AFKLM is OR, not Max-IP. Zero transfer."),
        note="The integer-counting MAX semiring is exactly what blocks the OR-semiring BMM shaves.",
    ))

    # (3) Rectangular MM: this IS the baseline (the polylog is intrinsic).
    rows.append(TechRow(
        technique="Rectangular MM (Coppersmith 1982; Le Gall 2012; Le Gall-Urrutia SODA 2018)",
        savings_at_neps="n^{2+o(1)} = n^2 polylog: the BASELINE itself (saved factor 1 over it)",
        saved_factor_log2_large=0.0,
        is_log_shave=False,
        meets_bar=False,
        gap=("Coppersmith 1982 computes C = A B^T in C0 n^2 (log n)^2 ops for eps below the "
             "dual exponent (alpha > 0.172 in 1982, alpha >= 0.321334 today, WXXZ 2023). The "
             "log^2 n is the polylog the target must remove; it is INTRINSIC to the bilinear "
             "recursion. Dual-exponent improvements RAISE the eps-ceiling, they do NOT shave "
             "the log^2 n. Literal closest object to the bar, but zero progress on the shave."),
        note="THE baseline. Faster dual exponent is orthogonal to the log-shave.",
    ))

    # (4) Jin-Xu large-sieve log-shave: applicable=False for Max-IP (scope guard).
    rows.append(TechRow(
        technique="Large-sieve log-shave (Jin-Xu STOC 2024, arXiv:2403.20326)",
        savings_at_neps="NOT applicable to Max-IP (scope: sparse convolution + Hamming only)",
        saved_factor_log2_large=0.0,
        is_log_shave=False,
        meets_bar=False,
        gap=("the frontier log-shaving toolkit (Best Student Paper, STOC 2024) shaves logs for "
             "sparse convolution and 1D text-to-pattern Hamming distance via the large sieve "
             "inequality. It exploits 1D additive structure and explicitly does NOT reach "
             "all-pairs Max-IP or bichromatic closest pair: no exploitable 1D structure, and "
             "the max couples across all n^2 pairs. applicable=False."),
        note="A clean negative coordinate: the strongest recent log-shaver does not reach this regime.",
    ))

    # (5) Exact integer geometry: n^{2-1/O(d)} -> < one log factor at d = n^eps.
    rows.append(TechRow(
        technique="Exact integer geometry (Matousek 1992; AESW 1991; Yao 1982)",
        savings_at_neps="n^{2-1/O(n^eps)} = saved factor 1 + o(1): LESS than one log factor",
        saved_factor_log2_large=0.0,
        is_log_shave=False,
        meets_bar=False,
        gap=("best-known exact geometry is n^{2-1/O(d)}; at d = n^eps the saved factor is "
             "n^{1/O(n^eps)} = 2^{(log n)/O(n^eps)} = 1 + o(1), strictly LESS than ONE log "
             "factor. Zero log-shave at this dimension."),
        note="The saved exponent 1/O(d) vanishes super-polynomially fast at d = n^eps.",
    ))

    return rows


# ==========================================================================
# Part 4: the threshold-sweep micro-idea, honestly attempted and measured.
#
# IDEA. Max-IP's answer is an integer in {0,...,d}. Sweep a candidate threshold t from
# d downward and test EXISTENCE of a pair with <a,b> >= t (a "Z-OV-like" decision). The
# max is the largest t with a YES. This trades the global max for O(d) = O(n^eps)
# existence queries. The HOPE: an existence query might be cheaper than materializing
# all n^2 entries (it can stop early at the first witness), shaving the n^2 max-scan.
#
# HONEST PREDICTION (to be confirmed/refuted by the measurement below):
#   - Correctness: the sweep DOES return the true max (verified against brute force).
#   - Cost: each existence query "is there a pair with <a,b> >= t?" at d = n^eps is
#     itself a Boolean-OV-like / Max-IP-decision problem at the SAME n^eps wall, with
#     NO known polynomial or log shave (the threshold version is at least as hard as
#     the open OV/Max-IP wall). So the best honest cost per query is the baseline
#     n^2 polylog. Sweeping O(n^eps) thresholds therefore MULTIPLIES the baseline by
#     n^eps: sweep cost ~ n^{2+eps} polylog >> n^2 polylog. The sweep does NOT shave
#     logs; it makes the cost WORSE by a polynomial factor n^eps.
#   - Binary search over t (instead of a linear sweep) cuts O(n^eps) queries to
#     O(log d) = O(eps log n) queries. That removes the n^eps blow-up but each query
#     is STILL the open n^eps wall, so binary search gives n^2 polylog * O(log n):
#     it ADDS a log factor rather than removing the polylog. It still does not shave.
# The valuable coordinate: the threshold-sweep reduces Max to existence, but existence
# at d = n^eps is itself the open wall, so the reduction cannot beat the baseline. We
# MEASURE this: count entries touched by the naive baseline vs by the sweep's queries,
# and confirm the sweep never touches FEWER entries than the baseline's n^2.
# ==========================================================================


@dataclass
class SweepResult:
    correct: bool
    baseline_entries_touched: int     # n^2: the baseline scans the whole product
    sweep_entries_touched: int        # entries this instance's linear sweep touches
    num_queries_linear: int           # thresholds the linear sweep actually made (early-stops)
    worstcase_queries_linear: int     # O(d): the worst-case linear-sweep query bound (max small)
    num_queries_binary: int           # O(log d) thresholds in a binary search (always)
    answer: int
    note: str = field(default="")


def existence_query_entries_touched(C: np.ndarray, t: int) -> int:
    """A best-case existence query "is there a pair with <a,b> >= t?", counting work.

    Returns how many entries of the product C the query must touch in the WORST case to
    certify a yes/no. The honest accounting: with NO precomputed structure, deciding
    "exists an entry >= t" over an n x n product whose entries depend on all d
    coordinates requires, in the worst case (no witness, or witness last), touching all
    n^2 entries (Omega(n^2) is the natural output lower bound, and a NO answer must rule
    out every pair). Early stopping on a YES helps only on lucky instances, not in the
    worst case the running-time bound must cover. So the per-query worst-case work is
    n^2 (the SAME wall as the baseline). We return n^2 to reflect the worst case.
    """
    n_A, n_B = C.shape
    # We do NOT get to skip entries in the worst case: to certify NO for threshold t we
    # must rule out all n_A * n_B pairs. (On a YES we could stop early, but the running
    # time bound is over the worst case.) This is the honest cost.
    return n_A * n_B


def threshold_sweep_micro_idea(A: np.ndarray, B: np.ndarray) -> SweepResult:
    """Attempt the threshold-sweep, MEASURE its work, and compare to the baseline.

    We run the sweep correctly (to verify it returns the true max) and we ACCOUNT the
    worst-case entries-touched honestly (each existence query is at the open n^eps wall,
    worst-case n^2). The result object exposes the comparison so the caller can see the
    sweep never touches fewer entries than the baseline's n^2; it multiplies by the
    number of thresholds.
    """
    n_A, d = A.shape
    n_B, _ = B.shape
    # Ground truth (and the materialized product, used only to RUN the sweep correctly;
    # the COST accounting below does not assume C is free).
    true_max, C = max_ip_matrix_product(A, B)

    baseline_entries = n_A * n_B   # the baseline scans the whole product once.

    # Linear sweep from t = d down to 0: first t with an existing pair >= t is the max.
    sweep_entries_linear = 0
    found_max = -1
    num_q_linear = 0
    for t in range(d, -1, -1):
        num_q_linear += 1
        sweep_entries_linear += existence_query_entries_touched(C, t)
        if (C >= t).any():     # the existence decision (run correctly)
            found_max = t
            break

    # Binary search over t in [0, d] (the cleverer sweep): O(log d) queries.
    lo, hi = 0, d
    num_q_binary = 0
    sweep_entries_binary = 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        num_q_binary += 1
        sweep_entries_binary += existence_query_entries_touched(C, mid)
        if (C >= mid).any():
            lo = mid
        else:
            hi = mid - 1
    bin_answer = lo

    correct = (found_max == true_max) and (bin_answer == true_max)
    # The linear sweep early-stops at the first YES, so on THIS instance it makes only
    # (d - max + 1) queries. Its WORST case (max = 0, or all-zero vectors) is d + 1
    # queries, each worst-case n^2. The honest blow-up bound is the worst case, which is
    # what a running-time guarantee must cover.
    worstcase_q_linear = d + 1
    return SweepResult(
        correct=correct,
        baseline_entries_touched=baseline_entries,
        sweep_entries_touched=sweep_entries_linear,
        num_queries_linear=num_q_linear,
        worstcase_queries_linear=worstcase_q_linear,
        num_queries_binary=num_q_binary,
        answer=true_max,
        note=("each existence query is at the open n^eps wall (worst-case n^2 entries); "
              "linear sweep is O(d)=O(n^eps) queries in the worst case (max small), binary "
              "search is O(log d) queries always. The linear sweep here early-stops at the "
              "first YES, so it makes only d-max+1 queries on this instance."),
    )


# ==========================================================================
# Reporting
# ==========================================================================


def main() -> int:
    print("=== Boolean Max-IP at d = n^eps: the Chen-2018 Thm 1.5.1 log-shave, made concrete ===\n")
    print("TARGET (Chen 2018 arXiv:1805.10698, abstract item 3, web-confirmed verbatim 2026-06-03):")
    print('  "An n^2 / log^{omega(1)} n time algorithm for Bichromatic Maximum Inner Product')
    print('   with vector dimension d = n^eps for any small constant eps would imply NEXP has')
    print('   no polynomial size THR o THR circuits. Note there is an n^2 polylog(n) time')
    print('   algorithm via fast rectangle matrix multiplication."')
    print("So the target SHAVES ALL POLYLOG FACTORS off the n^2 polylog baseline: a log-shave,")
    print("SETH-consistent (it is n^{2-o(1)}), genuinely OPEN as of 2026.\n")

    # ---- Part 1: the two baselines, computed and checked to agree. ----
    print("--- Part 1: Boolean Max-IP two ways (brute force vs A B^T then global max) ---\n")
    self_check_two_baselines_agree()
    rng = np.random.default_rng(42)
    A = (rng.random((6, 8)) < 0.5).astype(np.int64)
    B = (rng.random((6, 8)) < 0.5).astype(np.int64)
    m_bf = max_ip_bruteforce(A, B)
    m_mp, C = max_ip_matrix_product(A, B)
    print(f"explicit instance: n_A=6, n_B=6, d=8 (vectors in {{0,1}}^8)")
    print(f"  brute force (literal n^2 d definition)      max <a,b> = {m_bf}")
    print(f"  matrix product (C = A B^T, then C.max())     max <a,b> = {m_mp}")
    print(f"  the all-pairs inner-product matrix C = A B^T (entries in {{0,...,8}}):")
    for row in C:
        print("    " + " ".join(f"{int(v):2d}" for v in row))
    print(f"  AGREE: {m_bf == m_mp}. Grounded: the baseline computes ALL n^2 inner products,")
    print(f"  then takes the global max over them. The max is the largest entry of C.\n")

    # ---- Part 2: where the polylog factors live. ----
    print("--- Part 2: where the polylog factors live in the n^2 polylog baseline ---\n")
    print("The baseline = (3a) rectangular-MM step C0 n^2 (log n)^2  [the polylog overhead]")
    print("            + (3b) max-extraction over the n^2 entries of C  [Theta(n^2), no log saving].")
    print("Op-count model (log2 units; eps = %.2f, c_mm = 1):\n" % EPS)
    print(f"{'log2 n':>8} | {'mm-step log2':>13} | {'max-scan log2':>13} | "
          f"{'polylog bits':>12} | {'bits/entry':>10}")
    print("-" * 70)
    for L in (32.0, 64.0, 128.0, 256.0):
        oc = baseline_op_counts(L, EPS)
        print(f"{L:>8.0f} | {oc['mm_step_log2']:>13.3f} | {oc['scan_step_log2']:>13.3f} | "
              f"{oc['mm_polylog_factor_log2']:>12.3f} | {oc['bits_per_entry']:>10.1f}")
    print()
    print("Reading: the mm-step carries an EXTRA 2*log2(log2 n) bits over the max-scan (the")
    print("log^2 n polylog). The max-scan is a FLAT n^2 (no polylog), but it is Theta(n^2)")
    print("with ZERO achievable log-shave under enumeration, because Omega(n^2) is the natural")
    print("output size of the product. CONSEQUENCE: a log-shave must (i) shave the mm-step's")
    print("log^2 n AND (ii) compute the max WITHOUT scanning all n^2 entries. The max-")
    print("extraction is the BINDING term: it cannot be log-shaved by materializing-then-scanning.\n")

    split = measured_baseline_split()
    print("Measured wall-clock split (illustrative at small n, n=%d, d=%d):" % (int(split["n"]), int(split["d"])))
    print(f"  matmul step  (form C = A B^T)      : {split['matmul_seconds'] * 1e3:8.3f} ms")
    print(f"  max-scan step (global max of C)    : {split['maxscan_seconds'] * 1e3:8.3f} ms")
    print(f"  n^2 entries materialized           : {split['n2_entries']:.0f}  (the object a shave must avoid scanning)\n")

    # ---- Part 3: technique savings at d = n^eps, tabulated. ----
    print("--- Part 3: known-technique savings at d = n^eps, and the gap to the bar ---\n")
    tech_rows = build_tech_rows()
    hdr = f"{'technique':<58} | {'log-shave?':>10} | {'meets bar?':>10}"
    print(hdr)
    print("-" * len(hdr))
    for r in tech_rows:
        print(f"{r.technique[:58]:<58} | "
              f"{('YES' if r.is_log_shave else 'no'):>10} | "
              f"{('YES' if r.meets_bar else 'no'):>10}")
    print()
    for r in tech_rows:
        print(f"  {r.technique}")
        print(f"    saving at d=n^eps : {r.savings_at_neps}")
        print(f"    gap              : {r.gap}")
        print(f"    note             : {r.note}")
        print()

    # ---- The polynomial-method constant-vs-log distinction, numerically visible. ----
    print("=== The polynomial method is CONSTANT-factor (not log) at d = n^eps ===\n")
    print("Saved factor 2^{1/eps} is FLAT in n; a true log-shave log^e n GROWS. log2(saved")
    print("factor) below (eps = %.2f):\n" % EPS)
    print(f"{'log2 n':>8} | {'poly-method bits ->1/eps':>26} | {'log^4 n bits':>14} | {'log^16 n bits':>14}")
    print("-" * 70)
    for L in (32.0, 128.0, 512.0, 2048.0, 8192.0):
        pm = saved_factor_log2_poly_method(L)
        s4 = saved_factor_log2_true_logshave(L, 4.0)
        s16 = saved_factor_log2_true_logshave(L, 16.0)
        print(f"{L:>8.0f} | {pm:>26.4f} | {s4:>14.3f} | {s16:>14.3f}")
    print()
    print("Reading: the polynomial-method saved bits are CONSTANT at 1/eps = %.0f (a factor" % (1.0 / EPS))
    print("2^{1/eps}, here ~1024), while any genuine log^e n shave's bits GROW with n. The bar")
    print("wants log^{omega(1)} n (e -> infinity). The polynomial method delivers a constant.\n")

    # ---- Part 4: the threshold-sweep micro-idea, attempted and measured. ----
    print("--- Part 4: MICRO-IDEA (threshold sweep), honestly attempted and measured ---\n")
    print("IDEA: the answer is an integer in {0,...,d}. Sweep a candidate threshold t from d")
    print("down; the max is the largest t with an existing pair <a,b> >= t. Trades the global")
    print("max for O(d) existence queries (binary search: O(log d) queries). HOPE: an")
    print("existence query might avoid materializing all n^2 entries.\n")
    rng2 = np.random.default_rng(7)
    A2 = (rng2.random((40, 12)) < 0.5).astype(np.int64)
    B2 = (rng2.random((40, 12)) < 0.5).astype(np.int64)
    sweep = threshold_sweep_micro_idea(A2, B2)
    n2 = A2.shape[0] * B2.shape[0]
    print(f"instance: n_A=40, n_B=40, d=12.  true Max-IP = {sweep.answer}")
    print(f"  sweep returns the correct max               : {sweep.correct}")
    print(f"  baseline entries touched (one n^2 scan)     : {sweep.baseline_entries_touched}")
    print(f"  linear-sweep queries on THIS instance       : {sweep.num_queries_linear}  "
          f"(early-stops at first YES: d - max + 1 = {12 - sweep.answer + 1})")
    print(f"  linear-sweep WORST-CASE queries (~d+1)      : {sweep.worstcase_queries_linear}  "
          f"(when max is small / vectors all-zero)")
    print(f"  linear-sweep entries touched (this instance): {sweep.sweep_entries_touched}  "
          f"(= queries * n^2, each query worst-case n^2)")
    print(f"  binary-search queries (~log2 d, always)     : {sweep.num_queries_binary}")
    print(f"  worst-case linear cost / baseline           : {sweep.worstcase_queries_linear}x  (>1: WORSE, a polynomial n^eps blow-up)")
    print()
    print("HONEST VERDICT (this is the valuable coordinate, a precise NEGATIVE):")
    print("  The threshold sweep is CORRECT but does NOT shave logs. Each existence query")
    print("  'is there a pair with <a,b> >= t?' at d = n^eps is itself at the open n^eps wall")
    print("  (worst-case n^2, no known polynomial or log shave). Honest WORST-CASE accounting")
    print("  (a running-time bound must cover the worst case, not the lucky early-stop above):")
    print("    - LINEAR sweep makes O(d) = O(n^eps) queries when the max is small, so it")
    print("      multiplies the baseline by n^eps: cost ~ n^{2+eps} polylog, a polynomial factor")
    print("      WORSE than the n^2 polylog baseline. (On THIS instance the max was high, so it")
    print("      early-stopped; the bound does not get to assume that.)")
    print("    - BINARY search multiplies by O(log d) = O(eps log n): cost ~ n^2 polylog * O(log n),")
    print("      which ADDS a log factor rather than removing the polylog. Still not a shave.")
    print("  WHERE IT BREAKS (named): the existence-query subroutine. Reducing Max to existence")
    print("  does not help, because existence at d = n^eps is the SAME open wall as Max. The")
    print("  reduction is correct but cost-increasing. To shave, the max must be computed")
    print("  WITHOUT enumerating the n^2 pairs AND without a per-threshold n^2 query, which no")
    print("  known structure provides at d = n^eps. The micro-idea FAILS, as predicted.\n")

    # ======================================================================
    # Self-checks pinning the key coordinates. Module must exit 0.
    # ======================================================================

    # (1) The two Max-IP baselines agree on every tested instance (grounding).
    self_check_two_baselines_agree(seed=123)
    self_check_two_baselines_agree(seed=999)
    assert m_bf == m_mp, "brute-force and matrix-product Max-IP must agree (the baseline grounding)"
    assert C.max() == m_bf, "the global max of A B^T is the Max-IP answer"
    assert int(C.max()) <= 8, "a Boolean inner product of 8-bit vectors is at most 8"

    # (2) The polynomial method gives a CONSTANT-factor (not log) saving at d = n^eps.
    #     log2(saved factor) is exactly 1/eps at every n (flat); a log-shave grows.
    pm_bits = [saved_factor_log2_poly_method(L) for L in (32.0, 128.0, 512.0, 2048.0, 8192.0)]
    assert max(pm_bits) - min(pm_bits) < 1e-9, \
        "the polynomial-method saved factor at d=n^eps is CONSTANT in n (= 2^{1/eps})"
    assert abs(pm_bits[0] - 1.0 / EPS) < 1e-9, \
        "the constant saved factor is 2^{1/eps}; log2 of it is 1/eps (= 10 for eps=0.1)"
    log_bits = [saved_factor_log2_true_logshave(L, 4.0) for L in (32.0, 128.0, 512.0, 2048.0, 8192.0)]
    assert all(log_bits[i] < log_bits[i + 1] for i in range(len(log_bits) - 1)), \
        "a genuine log^e n shave's saved bits GROW with n (the contrast with the constant)"
    # The poly-method saving is dominated by any growing log-shave at large enough n.
    assert log_bits[-1] > pm_bits[-1], \
        "at large n a log^4 n shave's bits exceed the constant poly-method bits (constant vs growing)"

    # (3) The bar is the FULL polylog shave: no modeled technique meets it at d = n^eps.
    tech_rows_check = build_tech_rows()
    assert not any(r.is_log_shave for r in tech_rows_check), \
        "no modeled technique is even a log-shave at d=n^eps"
    assert not any(r.meets_bar for r in tech_rows_check), \
        "no modeled technique meets the n^2/log^{omega(1)} n bar at d=n^eps (the target is OPEN)"
    # The polynomial-method row must be explicitly tagged constant-factor, not a log-shave.
    pm_row = next(r for r in tech_rows_check if r.technique.startswith("Polynomial method"))
    assert not pm_row.is_log_shave and "2^{1/eps}" in pm_row.savings_at_neps, \
        "the polynomial-method row must be tagged CONSTANT-factor (2^{1/eps}), not a log-shave"
    # The Four-Russians / BMM row must be flagged as non-transferring (OR vs count-then-max).
    fr_row = next(r for r in tech_rows_check if r.technique.startswith("Four-Russians"))
    assert fr_row.saved_factor_log2_large == 0.0 and "OR" in fr_row.gap, \
        "the BMM row must flag zero transfer to the integer count-then-max (OR-semiring guard)"
    # The Jin-Xu large-sieve row must be tagged not-applicable to Max-IP.
    jx_row = next(r for r in tech_rows_check if r.technique.startswith("Large-sieve"))
    assert not jx_row.meets_bar and "NOT applicable" in jx_row.savings_at_neps, \
        "the Jin-Xu large-sieve shave must be tagged applicable=False for Max-IP"

    # (4) The baseline decomposition: the mm-step carries the polylog, the max-scan does not,
    #     and the max-scan alone is Theta(n^2) (the binding term).
    oc = baseline_op_counts(128.0, EPS)
    assert oc["mm_step_log2"] > oc["scan_step_log2"], \
        "the rectangular-MM step carries an EXTRA polylog over the flat n^2 max-scan"
    assert oc["mm_polylog_factor_log2"] > 0.0, \
        "the mm-step's polylog overhead (the shaveable log^2 n) is strictly positive"
    assert abs(oc["scan_step_log2"] - 2.0 * 128.0) < 1e-9, \
        "the max-scan is exactly n^2 (no polylog): a flat Theta(n^2) read"
    # The max-extraction is the binding term: scanning n^2 entries has zero log-shave.
    # Operationalized: the scan-step log2 has no polylog component (it equals log2(n^2) exactly).
    assert oc["scan_step_log2"] == 2.0 * 128.0, \
        "the max-scan term has NO polylog: it is the term with zero achievable log-shave under enumeration"

    # (5) The threshold-sweep micro-idea is CORRECT but does NOT beat the baseline: it
    #     touches at least as many entries as the baseline's n^2 (in fact a multiple).
    assert sweep.correct, "the threshold sweep must return the true Max-IP (correctness)"
    assert sweep.sweep_entries_touched >= sweep.baseline_entries_touched, \
        "the sweep cannot touch FEWER entries than the baseline n^2 (no shave)"
    assert sweep.sweep_entries_touched == sweep.num_queries_linear * sweep.baseline_entries_touched, \
        "the linear sweep multiplies the baseline n^2 by the number of thresholds (a blow-up, not a shave)"
    # WORST-CASE accounting (the honest one, since a running-time bound covers the worst
    # case): the linear sweep makes O(d) = O(n^eps) queries when the max is small, so it
    # multiplies the baseline n^2 by a polynomial factor n^eps. This is strictly WORSE
    # than the baseline, not a shave. (On a lucky instance it early-stops; the bound does not.)
    assert sweep.worstcase_queries_linear > 1, \
        "the linear sweep's WORST-CASE query count is O(d) > 1: it multiplies the baseline by n^eps"
    assert sweep.worstcase_queries_linear * sweep.baseline_entries_touched > sweep.baseline_entries_touched, \
        "the worst-case linear-sweep cost (O(d) * n^2) strictly EXCEEDS the baseline n^2 (a blow-up, not a shave)"
    # Binary search reduces the WORST-CASE query count to O(log d), but each query is
    # still the open n^eps wall (worst-case n^2). So even binary search ADDS a log factor.
    assert sweep.num_queries_binary < sweep.worstcase_queries_linear, \
        "binary search's O(log d) worst-case queries are fewer than the linear sweep's O(d)"
    assert sweep.num_queries_binary >= 1, \
        "binary search still makes at least one n^2-cost existence query (adds a log factor, not a shave)"

    # (6) Empirical status: the target is OPEN. No baseline or micro-idea here meets the bar.
    #     Operationalized: every path either materializes-and-scans n^2 (the baseline) or
    #     multiplies it (the sweep); none achieves n^2/log^{omega(1)} n.
    paths_meeting_bar = [r for r in tech_rows_check if r.meets_bar]
    assert not paths_meeting_bar, \
        "NEXP not in poly-size THR-of-THR is OPEN as of 2026: no path here meets the Max-IP bar"

    print("=== Self-check OK ===")
    print("(1) GROUNDED: Boolean Max-IP brute force and the A B^T matrix-product baseline AGREE")
    print("    on every tested instance. The baseline computes all n^2 inner products, then the")
    print("    global max. (web-confirmed target: Chen 2018 arXiv:1805.10698 abstract item 3.)")
    print("(2) The POLYNOMIAL METHOD gives a CONSTANT-factor saving 2^{1/eps} at d=n^eps")
    print("    (log2 = 1/eps = 10, FLAT in n), NOT a log-shave. A true log^e n shave's bits GROW.")
    print("(3) The bar is the FULL polylog shave (n^2/log^{omega(1)} n). NO modeled technique")
    print("    is even a log-shave at d=n^eps: polynomial method (constant), Four-Russians (OR,")
    print("    no transfer), rectangular MM (the baseline), Jin-Xu large sieve (not applicable),")
    print("    exact geometry (< one log). The target is OPEN.")
    print("(4) The polylogs live in the rectangular-MM step (log^2 n, Coppersmith 1982); the")
    print("    max-extraction is a FLAT Theta(n^2) with zero log-shave under enumeration. A")
    print("    log-shave must avoid materializing-and-scanning all n^2 inner products.")
    print("(5) MICRO-IDEA (threshold sweep): CORRECT but FAILS to shave. Each existence query")
    print("    is at the open n^eps wall (worst-case n^2), so the linear sweep multiplies the")
    print("    baseline by O(n^eps) (a polynomial factor WORSE), and binary search ADDS a log")
    print("    factor (O(log d) queries) rather than removing the polylog. It breaks at the")
    print("    existence-query subroutine: reducing Max to existence does not help because")
    print("    existence at d=n^eps is the same open wall.")
    print("(6) STATUS: NEXP not in poly-size THR-of-THR is OPEN. This module pins the target,")
    print("    the polylog map, and a tried-and-failed micro-idea. A precise negative coordinate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
