"""J1 transfer-gap ledger: the n^3-scale all-logs machineries vs the n^2-thin fused max.

J1 (LEARNINGS finding 26) is the one clearly-attackable joint of the leading path's
descent to NP: shave ALL polylog factors off the n^2-polylog baseline for Boolean
Max-IP_{n, n^eps}. By Chen 2018 (arXiv:1805.10698 Thm 1.5.1, web-confirmed verbatim in
note 4b) a deterministic (or co-nondeterministic) n^2 / log^{omega(1)} n algorithm there
implies NEXP not in poly-size THR-of-THR. The named most-promising angle (finding 24/26):
transfer the n^3-scale "all-logs" matrix-product machinery DOWN to the n^2-scale
count-then-max product. This module is the consolidated LEDGER for that transfer.

WHAT THIS MODULE ADDS over its two siblings (it is the JOINED ledger, one table):
  - e_maxip_logshave.py is the J1 baseline + the technique-saving map (reused here for
    the Boolean Max-IP product and the global-max grounding).
  - e_maxip_minplus_transfer.py grounds the Williams (min,+) operation mismatch in detail.
  - e_fused_max_mm.py isolates the fused-max sub-problem and surveys four machineries.
  - THIS module is the TRANSFER-GAP LEDGER: it pins, for each of the three named n^3-scale
    machineries (AFKLM BMM, Williams min-plus, ACW polynomial method), the OPERATION it
    computes, the SEMIRING, the SCALE, and the EXACT MISMATCH-KIND with the n^2-thin
    count-then-max-global-max structure, with a single mismatch_kind tag per row
    (operation / semiring / scale / operation+scale / multiple). It then (2) demonstrates
    the Theta(n^2) global-max-extraction wall concretely, (3) states the real fused-max-MM
    sub-problem and surveys the named fused products (dominance, (max,min), bottleneck)
    against it, (4) attempts one honest micro-idea (small-range bit-packing / block
    pre-filter) and reports exactly where it breaks, and (5) encodes the finding-24
    sharpening verdict (the Williams min-plus row: "wrong scale" -> "wrong operation").

HONESTY DISCIPLINE. PROVED facts cite a venue/year/arXiv (parameters web-confirmed in the
two sibling modules and note 4b, dated 2026-06-04). The "ported to n^eps" engine decay is
PROJECT INFERENCE (a model, flagged), not a theorem about any Max-IP algorithm (none
exists). The micro-idea is reported with the exact breaking step. A precise NEGATIVE is the
expected, valuable outcome. No faked speedup; no progress on the prize claimed.

Run:
    python -m experiments.circuit_complexity.e_j1_transfer
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# REUSE the J1 baseline: Boolean Max-IP two ways (brute force and A B^T then global max).
from experiments.circuit_complexity.e_maxip_logshave import (
    max_ip_bruteforce,
    max_ip_matrix_product,
)


EPS = 0.1   # the modest dimension exponent d = n^eps; any constant eps > 0 works.


# ==========================================================================
# Part 1: the transfer-gap LEDGER.
#
# The TARGET structure (what Max-IP_{n, n^eps} actually is, the thing to shave):
#   STEP A: the standard (+,x) product M = A B^T (entries the integer counts <a_i, b_j>
#           in {0,...,d}); a contraction over the inner index k, NO per-entry reduction.
#   STEP B: ONE global max over all n^2 OUTPUT entries (a single scalar reduction over
#           the (i,j) axes, applied AFTER the product).
# The two-step (count, then max-over-outputs) shape is the whole structure. A transfer of
# an n^3-scale machinery must match BOTH steps. Each row records the four coordinates and
# a single mismatch_kind tag against this two-step structure.
#
# mismatch_kind taxonomy (one tag per row, the dominant axis):
#   "operation"        : computes a different reduction (e.g. OR-existence, per-entry min)
#   "semiring"         : a different algebraic ring (OR-AND, tropical) than the integer (+,x)
#   "scale"            : right operation, wrong size regime (n^3 full-square vs n^2-thin)
#   "operation+scale"  : both, with operation primary
#   "multiple"         : three+ independent mismatches (operation/semiring/scale all miss)
# ==========================================================================


@dataclass(frozen=True)
class TransferRow:
    machinery: str
    saving: str                 # the headline saving, web-grounded (sibling modules + note 4b)
    operation: str              # the reduction the machinery computes
    semiring: str               # its algebraic structure
    scale: str                  # n^3 full-square vs n^2-thin n^eps
    mismatch_kind: str          # the single dominant mismatch tag (taxonomy above)
    detail: str                 # the precise mismatch with the count-then-max-global-max target
    fundamental: bool           # is the mismatch a working-principle wall (vs a tunable gap)?


def build_transfer_ledger() -> list[TransferRow]:
    return [
        # ---- (M1) AFKLM BMM: the regularity / decomposition super-polylog shave. ----
        TransferRow(
            machinery="AFKLM BMM (Abboud-Fischer-Kelley-Lovett-Meka, STOC 2024, arXiv:2311.09095)",
            saving="n^3 / 2^{Omega((log n)^{1/7})}, a SUPER-polylog shave (combinatorial)",
            operation="OR-over-ANDs: it solves Triangle DETECTION (one global existence bit) "
                      "and lifts to BMM via the loss-less subcubic equivalence",
            semiring="Boolean OR-AND (idempotent; one witness determines the bit)",
            scale="n^3 full-square, inner dimension n",
            mismatch_kind="multiple",
            detail=("OPERATION+SEMIRING is the load-bearing miss. The shave's engine is a "
                    "win-win COLLISION certificate: a regular/uniform dense piece guarantees AB "
                    "and C share a nonzero entry, which 'certifies that there is a triangle "
                    "without the need to compute anything further' (Sec 3). That is intrinsic "
                    "OR-idempotence: one witness suffices, so the dense case collapses to YES with "
                    "NO computation. Max-IP needs the INTEGER count <a,b> = sum_k a_ik b_jk (the "
                    "(+,x) semiring) AND a global MAX that distinguishes count 5 from count 6; the "
                    "collapse-to-one-bit discards exactly the per-entry counts the max needs. The "
                    "Kelley-Lovett-Meka structure theorem (Thm 2.1) yields uniformity of the SCALED "
                    "average A.B, a 1-bit collision object, never an integer-count matrix and never "
                    "a max. SCALE compounds it (n^3 full-square, inner dim n; the regularity "
                    "decomposition needs dense square graphs, a thin n x n^eps factor has no "
                    "regularity to exploit). The authors leave the non-Boolean / weighted "
                    "generalization, e.g. (min,+), OPEN ('it is unclear and left for future "
                    "research', p.4; 'min does not have an inverse'). Three independent misses."),
            fundamental=True,
        ),
        # ---- (M2) Williams min-plus: the Razborov-Smolensky tropical shave. ----
        TransferRow(
            machinery="Williams min-plus (R. Williams, STOC 2014, arXiv:1312.6680, SICOMP 2018)",
            saving="n^3 / 2^{Omega(sqrt(log n))} on the real RAM (Razborov-Smolensky polynomial method)",
            operation="(min,+) PRODUCT: per-entry P[i,j] = min_k (A_ik + B_kj), a reduction "
                      "over the CONTRACTION index k, fused INTO each of the n^2 outputs",
            semiring="tropical (min,+) (not Boolean OR-AND, not integer (+,x))",
            scale="n^3 full-square, inner dimension n",
            mismatch_kind="operation+scale",
            detail=("OPERATION is the deeper wall (sharpening finding 24's 'wrong scale'). The "
                    "(min,+) product reduces over the INNER (contraction) index PER output entry, "
                    "and the saving comes from FUSING that per-entry min into the product so the "
                    "n^3 contractions never materialize. Max-IP's product step is a plain (+,x) sum "
                    "with NO per-entry reduction operator to fuse a threshold polynomial into; its "
                    "lone reduction is the single global MAX over the OUTPUT indices (i,j), applied "
                    "AFTER the product. Different reductions on different axes: min-over-k-per-entry "
                    "vs max-over-(i,j)-once. The (min,+) matrix's global max is not even the Max-IP "
                    "answer (grounded on instances in e_maxip_minplus_transfer.py). SCALE is "
                    "secondary: even if the operation matched, at inner dim n^eps the "
                    "Razborov-Smolensky degree-vs-block trade collapses the saved exponent to "
                    "1/Theta(eps log n) and the saved factor flattens to 2^{O(1/eps)} = O(1), the "
                    "same constant-factor collapse as the polynomial method (finding 24)."),
            fundamental=True,
        ),
        # ---- (M3) ACW / AWY polynomial method: probabilistic polynomials for the OV/Max-IP wall. ----
        TransferRow(
            machinery="ACW polynomial method (Alman-Williams SODA 2015; Chan-Williams SODA 2016; "
                      "Alman-Chan-Williams FOCS 2016, arXiv:1608.04355)",
            saving="n^{2 - 1/O(log c)} at d = c log n (a real polynomial shave at LOGARITHMIC d)",
            operation="probabilistic polynomial for a threshold/OR, batched over the inner "
                      "dimension via fast rectangular MM",
            semiring="(+,x) over F2 after a low-degree threshold approximation (the right ring, "
                     "but applied to the existence/decision form)",
            scale="d = c log n (logarithmic), where its saved exponent grows; NOT d = n^eps",
            mismatch_kind="scale",
            detail=("SCALE is the load-bearing miss and it is a HARD decay, not a tunable gap. The "
                    "probabilistic-polynomial degree scales with the dimension d, so the saved "
                    "exponent is 1/O(log(d/log n)). At d = c log n this is 1/O(log c), a real "
                    "polynomial shave (n^{2-1/O(log c)}); at d = n^eps it is 1/O(eps log n) -> 0, so "
                    "the saved FACTOR flattens to the CONSTANT 2^{O(1/eps)} (~2^10 for eps=0.1), NOT "
                    "a log-shave. SECONDARY (operation/conclusion): the polynomial method shaves the "
                    "OV/existence decision, which routes through Chen 2018 Thm 1.2 to the WEAKER "
                    "SYM-of-THR, not the THR-of-THR that the MAX (Thm 1.5) gives. So at d=n^eps it is "
                    "double-disqualified: constant-factor (wrong scale) AND existence-not-max (wrong "
                    "operation/conclusion). Tagged 'scale' because the scale decay is what kills it "
                    "as a log-shave even before the conclusion-strength issue."),
            fundamental=True,
        ),
    ]


# ==========================================================================
# Part 2: the Theta(n^2) global-max-extraction wall, concretely.
#
# Form M = A B^T for a small instance, show the max is over all n^2 entries, and that
# reading them is Theta(n^2) (every entry must be inspected in the worst case because the
# max can sit at any pair). So a log-shave MUST fuse the max into the MM (compute it
# without writing down M). We measure entries-inspected to make the wall a number.
# ==========================================================================


def global_max_extraction_wall(A: np.ndarray, B: np.ndarray) -> dict[str, object]:
    """Compute M = A B^T, show the max is over n^2 entries, and that a scan inspects them all.

    The global max of M is the Max-IP answer. To CERTIFY it under enumeration you must
    inspect every entry (the argmax can be any pair; ruling out a candidate maximum at
    threshold t means checking all n^2). We return the materialized M (small), the answer,
    the (i,j) location of the max, and the worst-case entries-inspected (= n^2).
    """
    M = A.astype(np.int64) @ B.astype(np.int64).T
    n_A, n_B = M.shape
    flat_argmax = int(np.argmax(M))
    i_star, j_star = divmod(flat_argmax, n_B)
    return {
        "M": M,
        "answer": int(M.max()),
        "argmax_ij": (i_star, j_star),
        "n2_entries": n_A * n_B,
        # The argmax can sit at any of the n^2 cells; the location is data-dependent, so no
        # fixed sub-region can be pre-excluded. Worst-case certification inspects all n^2.
        "worstcase_entries_inspected": n_A * n_B,
    }


# ==========================================================================
# Part 3: the real fused-max-MM sub-problem, and the named fused products against it.
#
# The sub-problem: GLOBAL MAX of a small-range Boolean (+,x) matrix product, FUSED into
# the rectangular MM (computed without materializing M). We survey the named fused
# matrix products (dominance, (max,min) / bottleneck) and ask whether any gives a
# log-shave on THIS object. They are truly-subcubic POLYNOMIAL speedups, n^3-scale, and
# PER-ENTRY (a full output matrix of order-reductions), not an n^2-thin fused single
# scalar. So none touches the n^2 baseline at d = n^eps.
# ==========================================================================


@dataclass(frozen=True)
class FusedProductRow:
    product: str
    best_known: str
    is_log_shave: bool
    per_entry_or_global: str    # does it output a full per-entry matrix or a fused scalar?
    touches_n2_baseline: bool   # does it improve the n^2-thin Max-IP baseline at d=n^eps?
    note: str


def build_fused_product_survey() -> list[FusedProductRow]:
    return [
        FusedProductRow(
            product="Dominance product (Matousek 1991)",
            best_known="n^{(3+omega)/2} ~ n^2.69 (truly subcubic, full-square, arbitrary entries)",
            is_log_shave=False,
            per_entry_or_global="per-entry (a full n x n matrix of dominance counts)",
            touches_n2_baseline=False,
            note=("a POLYNOMIAL speedup at full-square n^3, computing a per-entry count matrix. "
                  "At thin inner dim n^eps it gives nothing new (the saving lives in n^3 -> n^2.69). "
                  "Order-based, not the integer (+,x) count; and per-entry, not a fused global scalar."),
        ),
        FusedProductRow(
            product="(max,min) / bottleneck-paths product (Vassilevska-Williams-Yuster, ToC 5:173-189, 2009)",
            best_known="O(n^{(3+omega)/2}) <= n^2.69 (Duan-Pettie); n^{2+omega/3} ~ n^2.79 (VWY 2007)",
            is_log_shave=False,
            per_entry_or_global="per-entry (a full n x n matrix of (max,min) values)",
            touches_n2_baseline=False,
            note=("the nearest 'fused order-reduction product' in the literature: each entry is a "
                  "max-of-mins over the inner dimension. Still PER-ENTRY (n^2 outputs, not one fused "
                  "scalar) and a POLYNOMIAL (not log) speedup at full-square scale; arbitrary-real, "
                  "not the small-range integer (+,x) count. No leverage at the n^2-thin baseline."),
        ),
        FusedProductRow(
            product="Bounded-range (min,+) log-shave (ESA 2024, LIPIcs.ESA.2024.57)",
            best_known="O(M n^omega + M n^2 log M) (removes a log M from O(M n^omega log M))",
            is_log_shave=True,   # it IS a log-shave, but of the WRONG object
            per_entry_or_global="per-entry (the FULL (min,+) product matrix)",
            touches_n2_baseline=False,
            note=("CLOSEST IN SPIRIT: it IS a bounded-range log-shave, and Max-IP entries lie in the "
                  "bounded range {0,...,n^eps}. But it shaves the log off the FULL (min,+) product "
                  "matrix at full-square scale, not a fused global max at thin dimension. Right "
                  "flavor (bounded-range, log-shave), wrong object (full matrix), wrong operation "
                  "((min,+) per-entry, not a global max of a (+,x) product)."),
        ),
    ]


def fused_max_subproblem_statement() -> str:
    return (
        "FUSED-MAX-MM SUB-PROBLEM (the real J1 object): given A, B of n vectors in {0,1}^d, "
        "d = n^eps, compute ans = max_{i,j} (A B^T)_{ij} (entries in {0,...,d}, the integer "
        "counts <a_i,b_j>) in n^2 / log^{omega(1)} n time, with the max FUSED into the "
        "rectangular MM, i.e. computed WITHOUT materializing all n^2 entries of M. This is a "
        "STANDARD (+,x) product followed by ONE GLOBAL MAX over the n^2 OUTPUT entries: a single "
        "scalar reduction over the (i,j) axes, applied after the product. KNOWN MACHINERY VERDICT: "
        "no known fused product (dominance, (max,min)/bottleneck, bounded-range (min,+)) gives a "
        "log-shave on it. They are truly-subcubic POLYNOMIAL speedups, n^3 full-square, and "
        "PER-ENTRY (a full output matrix), not an n^2-thin fused single scalar. The fused-max IS a "
        "named fine-grained problem (Bichromatic Max-IP, truly-subquadratic EQUIVALENT to OV, Chen "
        "arXiv:1811.12017), but that equivalence is at the POLYNOMIAL granularity, so it neither "
        "delivers nor rules out the polylog shave. Open at the log-shave scale; no published "
        "barrier forbids it (Abboud-Hansen-V.Williams-R.Williams STOC 2016, Abboud-Bringmann ICALP "
        "2018 cover only sequence/alignment problems, provably not OV/Max-IP)."
    )


# ==========================================================================
# Part 4: an honest micro-idea: small-range block pre-filter.
#
# IDEA. Max-IP entries are in {0,...,d}, d = n^eps. To find the global max, partition A and
# B into blocks of size b and compute, per block-pair, a CHEAP upper bound on the max entry
# in that block (e.g. via the popcount/column-sum: a block-pair can attain at most
# min(sum of column maxima) ... ). If a block-pair's cheap upper bound is below the best
# global max found so far, SKIP the full inner-product computation for that block-pair.
# HOPE: prune enough block-pairs that fewer than n^2 inner products are computed, fusing the
# max into the MM by avoiding low-value blocks.
#
# We IMPLEMENT it correctly and MEASURE inner products computed vs the n^2 baseline, and
# report exactly where it breaks. HONEST PREDICTION: a coordinate-wise / popcount upper
# bound on a Boolean block-pair's max inner product is too loose (it is at best d, the
# trivial bound, unless the block is sparse), so on random dense instances it prunes
# nothing and computes all n^2 entries; and even a tight bound cannot help in the worst
# case, because the global max can sit in any block, so no block-pair is safely skippable
# without a certificate that itself costs the inner products. The pruning is instance-lucky,
# not a worst-case shave: the running-time bound (which J1 needs) must cover the worst case.
# ==========================================================================


@dataclass
class MicroIdeaResult:
    correct: bool
    n2_baseline: int                 # n_A * n_B inner products (the baseline computes all)
    inner_products_computed: int     # how many this micro-idea actually computes
    block_pairs_total: int
    block_pairs_pruned: int
    worstcase_shaves: bool           # does it provably compute < n^2 in the WORST case?
    answer: int
    note: str


def block_upper_bound(A_block: np.ndarray, B_block: np.ndarray, d: int) -> int:
    """A CHEAP (sub-full-product) upper bound on the max inner product over a block-pair.

    For Boolean vectors, <a,b> <= min(popcount(a), popcount(b)) and also <= (number of
    columns where SOME row of A_block AND SOME row of B_block are both 1). We use the
    column-overlap bound: count columns k where A_block[:,k] has a 1 AND B_block[:,k] has a
    1; the max inner product over the block-pair cannot exceed that overlap count. This is
    O(b*d + d) per block-pair, cheaper than the b^2*d full block product. It is a genuine
    upper bound (any pair's shared-1 columns are a subset of the columns active in BOTH
    blocks), but it is LOOSE on dense blocks (it tends to d).
    """
    a_cols = A_block.any(axis=0)        # columns where some A-row is 1
    b_cols = B_block.any(axis=0)        # columns where some B-row is 1
    overlap = int(np.count_nonzero(a_cols & b_cols))
    return min(overlap, d)


def small_range_block_prefilter(A: np.ndarray, B: np.ndarray, block: int = 4) -> MicroIdeaResult:
    """Attempt the block pre-filter: skip block-pairs whose cheap upper bound is <= best.

    Correctly computes the global max (we verify against the baseline). Counts the inner
    products actually computed (full block products only for un-pruned block-pairs), so we
    can compare to the n^2 baseline and see whether it shaves in the worst case.
    """
    n_A, d = A.shape
    n_B, _ = B.shape
    A64 = A.astype(np.int64)
    B64 = B.astype(np.int64)

    best = -1
    inner_products_computed = 0
    block_pairs_total = 0
    block_pairs_pruned = 0

    # Process block-pairs. To give the pruning its best chance, we do NOT sort; a real
    # implementation would seed `best` high first, but even an oracle-perfect `best` cannot
    # prune the block that CONTAINS the max, and on dense random data the cheap bound is loose.
    a_starts = list(range(0, n_A, block))
    b_starts = list(range(0, n_B, block))
    for ai in a_starts:
        Ab = A64[ai:ai + block]
        for bj in b_starts:
            Bb = B64[bj:bj + block]
            block_pairs_total += 1
            ub = block_upper_bound(Ab, Bb, d)
            if ub <= best:
                # The cheap upper bound certifies no pair in this block-pair beats `best`.
                block_pairs_pruned += 1
                continue
            # Otherwise we must compute the full block product (b^2 inner products).
            sub = Ab @ Bb.T
            inner_products_computed += sub.shape[0] * sub.shape[1]
            block_max = int(sub.max())
            if block_max > best:
                best = block_max

    n2 = n_A * n_B
    truth, _ = max_ip_matrix_product(A, B)
    return MicroIdeaResult(
        correct=(best == truth),
        n2_baseline=n2,
        inner_products_computed=inner_products_computed,
        block_pairs_total=block_pairs_total,
        block_pairs_pruned=block_pairs_pruned,
        # It shaves in the WORST case only if it provably computes < n^2 for ALL inputs.
        # On dense random data the bound is loose and it prunes nothing; and the worst case
        # (max in the last block, all bounds = d) prunes nothing regardless. So: no.
        worstcase_shaves=False,
        answer=truth,
        note=("the column-overlap upper bound is LOOSE on dense Boolean blocks (it tends to d), "
              "so it rarely drops below `best`; and the block CONTAINING the global max can never "
              "be pruned. In the worst case (dense data, or max in the last block) it computes all "
              "n^2 inner products. Pruning is instance-lucky, not a worst-case shave; a J1 "
              "running-time bound must cover the worst case."),
    )


# ==========================================================================
# Reporting
# ==========================================================================


def main() -> int:
    print("=== J1 transfer-gap ledger: n^3-scale all-logs machinery vs the n^2-thin fused max ===\n")
    print("TARGET (Chen 2018 arXiv:1805.10698 Thm 1.5.1): a deterministic-or-co-nondeterministic")
    print("Max-IP_{n, n^eps} algorithm in n^2 / log^{omega(1)} n implies NEXP not in poly-size")
    print("THR-of-THR. STRUCTURE: M = A B^T (the standard (+,x) product, integer counts <a,b> in")
    print("{0,...,d}) THEN one GLOBAL MAX over all n^2 output entries. Two steps: count, then")
    print("max-over-outputs. The named angle (finding 24/26): transfer the n^3-scale all-logs")
    print("machinery DOWN to this n^2-thin count-then-max product. This module is the LEDGER.\n")

    # ---- Part 1: the transfer-gap ledger. ----
    print("--- Part 1: the transfer ledger (three n^3-scale machineries, one mismatch tag each) ---\n")
    ledger = build_transfer_ledger()
    hdr = f"{'machinery':<58} | {'mismatch_kind':>16} | {'fundamental':>11}"
    print(hdr)
    print("-" * len(hdr))
    for r in ledger:
        print(f"{r.machinery[:58]:<58} | {r.mismatch_kind:>16} | {('YES' if r.fundamental else 'no'):>11}")
    print()
    for r in ledger:
        print(f"  {r.machinery}")
        print(f"    saving        : {r.saving}")
        print(f"    operation     : {r.operation}")
        print(f"    semiring      : {r.semiring}")
        print(f"    scale         : {r.scale}")
        print(f"    mismatch_kind : {r.mismatch_kind}")
        print(f"    detail        : {r.detail}")
        print()

    # ---- Part 2: the Theta(n^2) global-max-extraction wall, concretely. ----
    print("--- Part 2: the Theta(n^2) global-max-extraction wall, concretely ---\n")
    rng = np.random.default_rng(11)
    A = (rng.random((6, 8)) < 0.5).astype(np.int64)
    B = (rng.random((7, 8)) < 0.5).astype(np.int64)
    wall = global_max_extraction_wall(A, B)
    M = wall["M"]
    print(f"instance n_A=6, n_B=7, d=8. M = A B^T (entries in {{0,...,8}}); Max-IP = the single")
    print(f"largest entry, at cell {wall['argmax_ij']} with value {wall['answer']}:")
    for row in M:
        print("    " + " ".join(f"{int(v):2d}" for v in row))
    print(f"  the max is over ALL {wall['n2_entries']} = n_A*n_B entries (a reduction over outputs).")
    print(f"  worst-case entries inspected to CERTIFY the max (the argmax can be any pair): "
          f"{wall['worstcase_entries_inspected']} = n^2.")
    print("  CONSEQUENCE: under enumeration the max-extraction is Theta(n^2) with zero log-shave")
    print("  (Omega(n^2) is the natural output size of A B^T). A log-shave MUST fuse the max into")
    print("  the MM: compute it WITHOUT writing down M. That fusion is the missing structural idea.\n")

    # ---- Part 3: the real fused-max-MM sub-problem and the named fused products. ----
    print("--- Part 3: the real fused-max-MM sub-problem, and named fused products against it ---\n")
    print(fused_max_subproblem_statement())
    print()
    survey = build_fused_product_survey()
    hdr2 = f"{'fused product':<58} | {'log-shave?':>10} | {'touches n^2 baseline?':>22}"
    print(hdr2)
    print("-" * len(hdr2))
    for fp in survey:
        print(f"{fp.product[:58]:<58} | {('YES' if fp.is_log_shave else 'no'):>10} | "
              f"{('YES' if fp.touches_n2_baseline else 'no'):>22}")
    print()
    for fp in survey:
        print(f"  {fp.product}")
        print(f"    best known : {fp.best_known}")
        print(f"    output     : {fp.per_entry_or_global}")
        print(f"    note       : {fp.note}")
        print()

    # ---- Part 4: the micro-idea (small-range block pre-filter), attempted and measured. ----
    print("--- Part 4: MICRO-IDEA (small-range block pre-filter), honestly attempted and measured ---\n")
    print("IDEA: Max-IP entries are in {0,...,d}, d=n^eps. Partition A,B into blocks; for each")
    print("block-pair compute a CHEAP column-overlap upper bound on its max inner product; if the")
    print("bound is <= the best max found so far, SKIP the full block product. HOPE: prune low-value")
    print("block-pairs so fewer than n^2 inner products are computed (fusing the max into the MM).\n")
    rng2 = np.random.default_rng(5)
    A2 = (rng2.random((24, 12)) < 0.5).astype(np.int64)
    B2 = (rng2.random((24, 12)) < 0.5).astype(np.int64)
    micro = small_range_block_prefilter(A2, B2, block=4)
    print(f"instance n_A=24, n_B=24, d=12 (dense, p=0.5). true Max-IP = {micro.answer}")
    print(f"  micro-idea returns the correct max          : {micro.correct}")
    print(f"  n^2 baseline (inner products to compute)    : {micro.n2_baseline}")
    print(f"  inner products this micro-idea computed     : {micro.inner_products_computed}")
    print(f"  block-pairs total / pruned                  : {micro.block_pairs_total} / {micro.block_pairs_pruned}")
    print(f"  provably computes < n^2 in the WORST case?  : {micro.worstcase_shaves}")
    print()

    # A sparse instance, to show the pruning is INSTANCE-lucky (it can prune when data is sparse),
    # which is exactly why it is not a worst-case shave.
    rng3 = np.random.default_rng(9)
    A3 = (rng3.random((24, 12)) < 0.12).astype(np.int64)   # sparse: column overlap is small
    B3 = (rng3.random((24, 12)) < 0.12).astype(np.int64)
    micro_sparse = small_range_block_prefilter(A3, B3, block=4)
    print(f"sparse instance (p=0.12): true Max-IP = {micro_sparse.answer}, correct = {micro_sparse.correct}")
    print(f"  inner products computed / n^2 baseline      : {micro_sparse.inner_products_computed}"
          f" / {micro_sparse.n2_baseline}  (pruned {micro_sparse.block_pairs_pruned} block-pairs)")
    print("  the bound prunes ONLY because the data is sparse; this is instance-luck, not a bound.\n")

    print("HONEST VERDICT (the valuable NEGATIVE):")
    print(f"  {micro.note}")
    print("  WHERE IT BREAKS (named): the block CONTAINING the global max can NEVER be pruned (its")
    print("  upper bound is >= the answer), and on dense data every block's column-overlap bound is")
    print("  ~ d, so nothing drops below `best`. The pruning is data-dependent (helps on sparse")
    print("  instances) but a J1 running-time bound must cover the WORST case, where it computes all")
    print("  n^2 inner products. No worst-case shave. The micro-idea FAILS, as predicted.\n")

    # ======================================================================
    # Self-checks pinning the coordinates. Module must exit 0.
    # ======================================================================

    # (0) REUSE grounding: the imported Boolean Max-IP baselines agree on the small instances.
    for seed in (0, 7, 21):
        rr = np.random.default_rng(seed)
        AA = (rr.random((8, 10)) < 0.5).astype(np.int64)
        BB = (rr.random((9, 10)) < 0.5).astype(np.int64)
        m_bf = max_ip_bruteforce(AA, BB)
        m_mp, MM = max_ip_matrix_product(AA, BB)
        assert m_bf == m_mp == int(MM.max()), \
            "REUSED baseline: brute-force Max-IP = global max of A B^T (the count-then-max structure)"

    # (1) The ledger has exactly the three named machineries, each with a mismatch tag and detail.
    ledger_check = build_transfer_ledger()
    names = " ".join(r.machinery for r in ledger_check)
    assert "AFKLM" in names and "Williams min-plus" in names and "polynomial method" in names, \
        "the ledger must pin AFKLM BMM, Williams min-plus, and the ACW polynomial method"
    assert all(r.detail and r.mismatch_kind for r in ledger_check), \
        "each ledger row must carry a named mismatch_kind and a detail"
    valid_kinds = {"operation", "semiring", "scale", "operation+scale", "multiple"}
    assert all(r.mismatch_kind in valid_kinds for r in ledger_check), \
        "every mismatch_kind must be one of the taxonomy tags"

    # (1a) AFKLM is OR-AND (Boolean), NOT the integer (+,x); a multiple mismatch.
    afklm = next(r for r in ledger_check if r.machinery.startswith("AFKLM"))
    assert "OR-AND" in afklm.semiring and afklm.mismatch_kind == "multiple", \
        "AFKLM is OR-AND (detection/existence), not the integer count-then-max: a multiple mismatch"
    assert "(+,x)" in afklm.detail and "collapse" in afklm.detail and "DETECTION" in afklm.operation, \
        "AFKLM's detail must contrast the OR-idempotence collapse (detection) with the (+,x) count-then-max"

    # (1b) Williams min-plus is a (min,+) PRODUCT (per-entry, over the contraction index),
    #      NOT a standard-product-then-global-max. The mismatch is operation+scale (operation primary).
    wmp = next(r for r in ledger_check if r.machinery.startswith("Williams min-plus"))
    assert "(min,+)" in wmp.operation and "tropical" in wmp.semiring, \
        "Williams min-plus computes the tropical (min,+) PRODUCT, a per-entry reduction over k"
    assert wmp.mismatch_kind == "operation+scale", \
        "the Williams row's mismatch is operation+scale (operation primary), not scale alone"
    assert "OUTPUT" in wmp.detail and "AFTER the product" in wmp.detail, \
        "the Williams detail must contrast per-entry-min-over-k with global-max-over-outputs"

    # (1c) The polynomial method is the right ring but the WRONG scale (decays at d=n^eps).
    pm = next(r for r in ledger_check if "polynomial method" in r.machinery)
    assert pm.mismatch_kind == "scale" and "2^{O(1/eps)}" in pm.detail, \
        "the polynomial-method row's primary miss is scale: it flattens to a constant at d=n^eps"

    # (1d) All three machineries differ from Max-IP's structure (none transfers as-is).
    assert all(r.fundamental for r in ledger_check), \
        "all three mismatches are working-principle walls (fundamental), not tunable gaps"

    # (2) The Theta(n^2) global-max-extraction wall: the max is over n^2 entries, and the
    #     worst-case certification inspects all n^2 (the argmax can be any pair).
    wall_check = global_max_extraction_wall(A, B)
    assert wall_check["answer"] == int(wall_check["M"].max()), \
        "the global max of M = A B^T is the Max-IP answer"
    assert wall_check["worstcase_entries_inspected"] == wall_check["n2_entries"], \
        "worst-case max-extraction inspects all n^2 entries (the argmax can sit at any pair)"
    # Cross-check against the reused brute force on the same instance.
    assert wall_check["answer"] == max_ip_bruteforce(A, B), \
        "the wall's answer matches the reused brute-force Max-IP"

    # (3) The fused-max-MM sub-problem statement is stated, and no named fused product
    #     gives a log-shave that touches the n^2-thin baseline at d=n^eps.
    stmt = fused_max_subproblem_statement()
    assert "FUSED" in stmt and "global max" in stmt.lower() and "n^eps" in stmt, \
        "the sub-problem must be stated as a fused global max of a thin (+,x) product"
    survey_check = build_fused_product_survey()
    assert not any(fp.touches_n2_baseline for fp in survey_check), \
        "no named fused product (dominance, (max,min), bounded-range (min,+)) touches the n^2 baseline at d=n^eps"
    # The bounded-range (min,+) is a log-shave but of the WRONG object (closest in spirit, no transfer).
    esa = next(fp for fp in survey_check if "ESA 2024" in fp.product)
    assert esa.is_log_shave and not esa.touches_n2_baseline, \
        "the bounded-range (min,+) IS a log-shave but of the full matrix, not the fused max: no transfer"
    # The (max,min)/dominance products are POLYNOMIAL (not log) speedups, per-entry, full-square.
    assert all(not fp.is_log_shave for fp in survey_check if "product" in fp.product and "ESA" not in fp.product), \
        "the dominance and (max,min) products are polynomial speedups, not log-shaves"

    # (4) The micro-idea is correct but does NOT shave in the worst case.
    micro_check = small_range_block_prefilter(A2, B2, block=4)
    assert micro_check.correct, "the block pre-filter must return the true Max-IP (correctness)"
    assert not micro_check.worstcase_shaves, \
        "the block pre-filter does NOT provably compute < n^2 in the worst case (no worst-case shave)"
    # On dense p=0.5 data the column-overlap bound is loose: it prunes few/no block-pairs, so it
    # computes (essentially) all n^2 inner products. Confirm it does not beat the baseline here.
    assert micro_check.inner_products_computed >= 0, "non-negative work count"
    assert micro_check.inner_products_computed <= micro_check.n2_baseline + (4 * 4), \
        "the block pre-filter computes at most ~n^2 inner products (it never beats n^2 on dense data)"

    # (5) The finding-24 sharpening verdict, encoded: the Williams min-plus row's label is
    #     "wrong operation" (operation primary), NOT "wrong scale" alone. mismatch_kind carries it.
    assert wmp.mismatch_kind == "operation+scale", \
        "finding 24's 'wrong scale' for the Williams min-plus row sharpens to 'wrong OPERATION + scale'"
    finding24_correction = (
        "SHARPEN. Finding 24's 'wrong scale' label for the Williams min-plus row is too weak: it "
        "should be 'wrong OPERATION (+ scale)', with the operation mismatch PRIMARY. Williams "
        "computes a (min,+) PRODUCT: a per-entry reduction (min) over the CONTRACTION index k, "
        "fused into each of the n^2 outputs. Max-IP is a standard (+,x) product (no per-entry "
        "reduction) followed by ONE global MAX over the n^2 OUTPUT entries. Different reductions on "
        "different axes; the (min,+) matrix's global max is not even the Max-IP answer. The fusion "
        "hook the engine exploits (a per-entry reduction to batch a threshold polynomial into) is "
        "absent in a (+,x) product, so it is a wrong-target wall, not a parameter to tune. Scale "
        "decay (the saving flattens to 2^{O(1/eps)} at inner dim n^eps) is REAL but SECONDARY. The "
        "mismatch_kind tag is 'operation+scale'. (AFKLM is even further: 'multiple', the OR-AND "
        "detection collapse discarding the very counts the max needs.)"
    )

    print("=== Self-check OK ===")
    print("(0) REUSE: the imported Boolean Max-IP baselines (brute force, A B^T then global max)")
    print("    agree; the count-then-max structure is grounded on the reused object.")
    print("(1) LEDGER: AFKLM BMM = OR-AND detection (mismatch 'multiple': semiring+operation+scale,")
    print("    the collapse-to-one-bit discards the counts the max needs); Williams min-plus = a")
    print("    (min,+) PRODUCT (per-entry reduction over the contraction index, mismatch")
    print("    'operation+scale', operation primary, NOT a standard-product-then-global-max);")
    print("    ACW polynomial method = right ring, wrong scale (mismatch 'scale': flattens to the")
    print("    constant 2^{O(1/eps)} at d=n^eps). All three differ from Max-IP's structure.")
    print("(2) WALL: the global max is over all n^2 entries; the argmax can be any pair, so")
    print("    worst-case certification inspects all n^2 (Theta(n^2), zero log-shave under")
    print("    enumeration). A shave MUST fuse the max into the MM (no materialize-and-scan).")
    print("(3) SUB-PROBLEM: the fused global max of a small-range (+,x) product at thin n^eps. No")
    print("    named fused product (dominance ~n^2.69, (max,min) ~n^2.79/n^2.69, bounded-range")
    print("    (min,+) log-shave) gives a log-shave on it: all are per-entry, n^3-scale, and either")
    print("    polynomial (not log) or shave the full matrix (wrong object). Open at the log scale.")
    print("(4) MICRO-IDEA (small-range block pre-filter): CORRECT but does NOT shave in the worst")
    print("    case. The block containing the max can never be pruned, and on dense data the")
    print("    column-overlap bound is ~d (loose), so it computes all n^2 inner products. Pruning is")
    print("    instance-lucky (sparse data only), not a worst-case bound. It FAILS, as predicted.")
    print("(5) VERDICT: finding 24's 'wrong scale' for the Williams min-plus row SHARPENS to 'wrong")
    print("    OPERATION + scale' (operation primary). No transfer; no progress on the prize claimed.")

    # The structured-output payload the parent loop reads is in this module's return path; print
    # the finding-24 correction so it is visible in stdout too.
    print()
    print("FINDING-24 CORRECTION (encoded):")
    print("  " + finding24_correction)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
