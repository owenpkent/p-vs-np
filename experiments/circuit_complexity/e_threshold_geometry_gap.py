"""The threshold-geometry gap: best-known algorithms vs the Chen-2018 bar.

A GAP CALCULATOR for the leading-path hinge (NEXP not in poly-size THR-of-THR).
Companion to e_tc0_sat_savings.py (the SAT-savings model), e_chen2018_geometry_gap.py
(an earlier growth-condition model), and the grounded hinge note
(docs/03_research/2050_tc0_hinge_grounded.md, section 4, the "geometry form").

This module answers the two decisive questions the hinge note states but never maps.

  Q-GAP. For each (problem, dimension regime, savings bar) in Chen 2018
  (arXiv:1805.10698), what is the BEST-KNOWN algorithm, and how far is it from the
  bar? In particular: avoid the TRAP. Boolean Orthogonal Vectors has a real
  polynomial-method shave (Abboud-Williams-Yu, SODA 2015: n^{2-1/O(log(d/log n))};
  derandomized by Chan-Williams, SODA 2016). But Chen's THR-of-THR conclusion
  (Theorem 1.1) needs the HARDER problems over the integers / reals (Z-OV/Hopcroft,
  exact Z-Max-IP, exact ell_2-Furthest-Pair, exact Bichrom.-ell_2-Closest-Pair).
  Boolean OV / Boolean Max-IP / approximate closest-pair at polylog dimension give
  only the WEAKER SYM-of-THR conclusion (Theorem 1.2). So the Boolean-OV shave does
  NOT settle THR-of-THR. We resolve this trap in code with explicit self-checks.

  Q-SETH. Would meeting the Chen-2018 bar REFUTE SETH (making the TC0 lower bound a
  conditional barrier), or is the bar CONSISTENT with SETH (hence genuinely open and
  attackable)? The answer turns on a SCALE distinction the calculator makes numeric:
  SETH (via the OV conjecture) forbids only a POLYNOMIAL speedup n^{2-eps} (constant
  eps > 0) at dimension d = omega(log n). Chen's main bar asks only for a LOG-SHAVE
  n^2/log^{omega(1)} n, which is ITSELF n^{2-o(1)}, hence does NOT cross the SETH
  floor. Exactly one of Chen's sub-targets (Theorem 1.5 item 2: Boolean Max-IP at
  polylog dimension in n^{2-eps} for CONSTANT eps) is a genuine polynomial speedup at
  SETH-hard dimension and so WOULD refute SETH. The main route (Theorem 1.1, and
  Theorem 1.5 item 1) is SETH-consistent and open.

ALL PARAMETERS verbatim from the primary sources, web-confirmed 2026-06-03:
  - Chen 2018, arXiv:1805.10698 (abstract + Thms 1.1, 1.2, 1.5 fetched from arXiv):
    Thm 1.1 bar n^2 poly(d)/log^{omega(1)} n at polylog d, problems
    {ell_2-Furthest-Pair, Hopcroft / Z-OV, Bichrom.-ell_2-Closest-Pair, Integer
    Max-IP, Weighted-Max-IP} => NEXP not in poly THR-of-THR; Thm 1.2 (approximate
    closest-pair, Boolean Max-IP) => SYM-of-THR; Thm 1.5 (Boolean Max-IP at d = n^eps
    in n^2/log^{omega(1)} n, OR at d = log^k n in n^{2-eps}) => THR-of-THR, with an
    n^2 polylog(n) rectangular-matmul baseline noted.
  - Chen, arXiv:1802.02325 / CCC 2018 / ToC 16(4) 2020 (abstract fetched from arXiv):
    exact Z-Max-IP from Z^d at d = 2^{O(log* n)} requires n^{2-o(1)} under SETH; via
    the Williams SODA 2018 reduction, ell_2-Furthest-Pair and Bichrom.-ell_2-Closest-
    Pair at d = 2^{O(log* n)} require n^{2-o(1)}.
  - Abboud-Williams-Yu, SODA 2015: Boolean OV at d = c log n in n^{2-1/O(log c)}.
  - Alman-Chan-Williams, FOCS 2016: best-known integer geometry n^{2-1/O(d)}
    (Matousek 1992; AESW 1991; Yao 1982); approx Bichrom.-closest-pair
    n^{2-Omega(eps^{1/3})}.

EMPIRICAL STATUS (web-confirmed 2026-06-03): NEXP not in poly-size THR-of-THR is
still OPEN. No algorithm has met the Chen-2018 bar; the only proved nontrivial
THR-of-THR results are the n^{2-o(1)}-WIRE bound (Tamaki / ACW) and the one-bottom-
threshold-layer SIZE bound (Murray-Williams 2018). The arithmetic below is a GAP MAP,
not a proof.

Like e_tc0_sat_savings.py, all magnitudes are kept in log-scale (we work with the
EXPONENT of n, i.e. log_n of every running time and every saved factor) so nothing
overflows and we never call an asymptotic-only savings "feasible".

Run:
    python -m experiments.circuit_complexity.e_threshold_geometry_gap
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


# ==========================================================================
# Log-scale primitives. Everything is an EXPONENT of n.
#
# A running time T = n^a (times polylog) is represented by its leading exponent
# a (here always 2 for the quadratic problems) PLUS a separately-tracked saved
# factor. We write the saved factor F as n^s, and ALSO as log^e n, because the two
# views answer different questions:
#   - s = log_n(F) > 0 (constant)         <=>  POLYNOMIAL shave (n^{2-s}); this is
#                                              what SETH forbids at d = omega(log n).
#   - s = o(1) but F = log^e n, e -> inf  <=>  pure LOG-SHAVE (n^2/log^{omega(1)} n);
#                                              SETH permits this (it is n^{2-o(1)}).
# Keeping both views is the whole point: the SETH verdict is exactly the question of
# WHICH view a given algorithm's savings falls into.
# ==========================================================================


def saved_exponent_to_log_exponent(n: float, s: float) -> float:
    """Convert a saved factor n^s into the form log^e n; return e.

    n^s = 2^{s log2 n} = (log2 n)^e  with  e = s * log2(n) / log2(log2 n).
    A log-shave bar (shave log^{omega(1)} n) is met iff e(n) -> infinity. A genuine
    polynomial shave has s = Theta(1), so e(n) -> infinity trivially AND s stays
    bounded away from 0; the discriminator below is s, not e.
    """
    if math.isinf(s):
        return float("inf")
    ln = math.log2(n)
    lln = math.log2(ln) if ln > 1.0 else 1.0
    return s * ln / lln


def log10_saved_factor(n: float, s: float) -> float:
    """log10 of the saved factor n^s (so we never materialize the factor itself)."""
    if math.isinf(s):
        return float("inf")
    return s * math.log10(n)


# --------------------------------------------------------------------------
# Best-known saved exponents s = log_n(saved factor), per problem family.
# The O(.) constants are taken as 1 for a best-case illustration; the point is the
# functional form (how s scales with d and n), not the constant.
# --------------------------------------------------------------------------


def s_awy_boolean_ov(n: float, d: float) -> float:
    """Boolean OV (AWY 2015 / Chan-Williams 2016): time n^{2 - 1/O(log c)}, d = c log n.

    Saved exponent s = 1/O(log c). At d = c log n with c = O(1) this is a CONSTANT
    (a genuine polynomial shave). At d = log^k n we have c = log^{k-1} n, so
    s = 1/O((k-1) log log n) -> 0: the polynomial shave DEGRADES to a log-shave as d
    grows into the polylog regime. This is the TRAP problem (Boolean, routes to
    SYM-of-THR only at polylog d).
    """
    ln = math.log2(n)
    c = d / ln if ln > 0 else d
    if c <= 1.0:
        c = 1.0001
    lc = math.log2(c)
    return float("inf") if lc <= 0 else 1.0 / lc


def s_integer_geometry(n: float, d: float) -> float:
    """Exact integer/real geometry (Z-OV, Z-Max-IP, exact ell_2 furthest/closest pair).

    Best known n^{2 - 1/O(d)} (Matousek 1992; Agarwal-Edelsbrunner-Schwarzkopf-Welzl
    1991; Yao 1982). Saved exponent s = 1/O(d). At d = omega(log n) this gives a
    saved factor n^{1/omega(log n)} = 2^{(log n)/omega(log n)} = O(1): no polylog
    shave at all. This is the THR-of-THR BOTTLENECK (Theorem 1.1).
    """
    return 1.0 / d if d > 0 else 1.0


def s_approx_closest_pair(eps: float) -> float:
    """(1+eps)-approx Bichrom.-ell_2-Closest-Pair: n^{2 - Omega(eps^{1/3})} (ACW 2016).

    Saved exponent s = eps^{1/3}. At eps = Theta(1) this is a polynomial shave, but
    the route (approximate closest-pair) gives only SYM-of-THR (Theorem 1.2), and at
    eps << 1/log^3 n the shave vanishes.
    """
    return eps ** (1.0 / 3.0)


def s_rect_matmul_baseline() -> float:
    """Boolean Max-IP at d = n^eps: naive n^2 polylog via Coppersmith 1982 rect matmul.

    The baseline running time is n^2 polylog(n): the saved factor over n^2 is only a
    polylog, i.e. s = 0 (no polynomial savings yet). Chen Theorem 1.5 item 1 asks to
    push this baseline to n^2 / log^{omega(1)} n: a LOG-SHAVE off an already-n^2-polylog
    algorithm. This is the most attackable single target (only logs separate it from
    the bar).
    """
    return 0.0


# ==========================================================================
# The SETH classifier. The single most important function in this module.
#
# SETH (via Williams 2005 -> the Orthogonal-Vectors Conjecture) forbids a POLYNOMIAL
# speedup n^{2-eps} (constant eps > 0) for OV / Max-IP / closest-pair at dimension
# d = omega(log n). For the EXACT integer problems the SETH-hard dimension reaches
# DOWN to d = 2^{O(log* n)} (Chen 2020 ToC). It does NOT forbid a log-shave
# n^2/log^{omega(1)} n, because a log-shave is itself n^{2-o(1)} and so SATISFIES the
# SETH lower bound (it stays inside the band SETH guarantees).
#
# So a target's SETH status is decided by TWO axes:
#   (1) is the savings a constant-exponent polynomial shave (s = Theta(1))
#       or only a log-shave (s = o(1), saved factor = log^{omega(1)} n)?
#   (2) is the dimension in the SETH-hard regime (d = omega(log n), or down to
#       2^{O(log* n)} for the exact integer problems)?
# It REFUTES SETH iff BOTH hold: a polynomial shave AT a SETH-hard dimension.
# ==========================================================================


def seth_hard_dimension(problem_kind: str, d_regime: str) -> bool:
    """Is dimension d_regime inside the SETH-hard regime for this problem family?

    Boolean OV / Boolean Max-IP / approx closest-pair: SETH-hard at d = omega(log n).
    Exact integer geometry (Z-OV, Z-Max-IP, exact ell_2 pair): SETH-hard already at
    d = 2^{O(log* n)}, hence at every regime at or above that (clog, polylog, n^eps).
    """
    if d_regime == "clog":          # d = c log n, c constant: NOT omega(log n)
        # c log n is Theta(log n). The OV conjecture's SETH-hardness kicks in at
        # d = omega(log n); at exactly Theta(log n) a polynomial shave (AWY) exists,
        # so this regime is NOT (yet) SETH-hard for Boolean problems. For the exact
        # integer problems, 2^{O(log* n)} << c log n, so it IS SETH-hard.
        return problem_kind == "integer"
    # polylog and n^eps are both omega(log n): SETH-hard for all families here.
    return d_regime in ("polylog", "n_eps")


def classify_seth(bar_is_poly_shave: bool, d_regime: str, problem_kind: str) -> str:
    """Return one of 'would-refute-SETH', 'consistent-open', 'unclear'.

    This is a property of the BAR (the target running time), not of any best-known
    algorithm. The SETH floor forbids a POLYNOMIAL shave n^{2-eps} (constant eps) at a
    SETH-hard dimension. So:
      - bar is a polynomial shave (n^{2-eps}, constant eps) AND dimension is SETH-hard
        => meeting it would REFUTE SETH (a conditional barrier).
      - bar is a log-shave (n^2/log^{omega(1)} n, itself n^{2-o(1)}) => CONSISTENT with
        SETH at any dimension (it stays inside the band SETH guarantees).
      - bar is a polynomial shave at a NON-SETH-hard dimension (e.g. d = Theta(log n)
        for Boolean OV, where AWY already gives one) => CONSISTENT (the OV conjecture
        only bites at d = omega(log n)).

    CRUCIAL: do NOT confuse "best-known saves a tiny positive exponent 1/polylog"
    with "polynomial shave". 1/polylog = o(1) is a log-shave, not a constant eps. The
    discriminator is whether the saved exponent is bounded away from 0 (a constant),
    which only the n^{2-eps} BAR (Thm 1.5.2) and the AWY d=Theta(log n) algorithm are.
    """
    hard_dim = seth_hard_dimension(problem_kind, d_regime)
    if bar_is_poly_shave and hard_dim:
        return "would-refute-SETH"
    return "consistent-open"


# ==========================================================================
# The gap table. One row per (problem, dimension regime, Chen theorem).
# ==========================================================================


@dataclass
class GapRow:
    problem: str
    dimension_regime: str
    best_known: str                 # human-readable best-known running time
    chen_bar: str                   # the Chen-2018 bar for this row
    # numeric: the best-known saved EXPONENT of n at two scales, and the bar's nature
    s_small: float = field(default=0.0)     # saved exponent at n = 2^32
    s_large: float = field(default=0.0)     # saved exponent at n = 2^128
    bar_is_log_shave: bool = True           # True: bar asks only n^2/log^{omega(1)} n
    bar_is_poly_shave: bool = False         # True: bar asks n^{2-eps}, constant eps
    meets_bar: bool = False                 # does best-known meet the bar?
    conclusion_if_met: str = "other"        # THR-of-THR | SYM-of-THR | other
    seth_status: str = "unclear"            # would-refute-SETH | consistent-open | unclear
    problem_kind: str = "integer"           # integer | boolean | approx
    note: str = ""

    @property
    def gap(self) -> str:
        """A precise shortfall/surplus statement for the structured output."""
        e_small = saved_exponent_to_log_exponent(2.0 ** 32, self.s_small)
        e_large = saved_exponent_to_log_exponent(2.0 ** 128, self.s_large)
        if self.bar_is_poly_shave:
            # Two sub-cases. The AWY context row (meets_bar True, no Chen bar) is a real
            # n^{2-eps} algorithm at d=Theta(log n); the Thm 1.5.2 SETH-barrier row
            # (meets_bar False) needs a constant-eps shave at omega(log n) that no known
            # algorithm delivers.
            if self.meets_bar:
                return (f"best-known IS a polynomial shave (saved exponent s={self.s_large:.4f}, "
                        f"i.e. n^{{2-{self.s_large:.4f}}}) at d=Theta(log n); not a Chen bar, "
                        f"and SETH-consistent (omega(log n) not reached)")
            return ("best-known saved exponent s=o(1) (only a log-shave at polylog d); "
                    "bar needs a constant-exponent polynomial shave n^{2-eps} at omega(log n): "
                    "NOT met, and meeting it would refute SETH")
        # log-shave bar: compare the log-exponent growth
        if self.meets_bar:
            return (f"best-known log-exponent grows ({e_small:.3f} -> {e_large:.3f}); "
                    f"clears the shave-all-logs bar in form")
        return (f"best-known log-exponent does NOT grow ({e_small:.4f} -> {e_large:.4f}); "
                f"the full log^{{omega(1)}} n shave is the open gap (zero progress)")


def build_gap_rows() -> list[GapRow]:
    n1, n2 = 2.0 ** 32, 2.0 ** 128
    rows: list[GapRow] = []

    # --- ROW 1: the THR-of-THR bottleneck (Thm 1.1), exact integer geometry, polylog d.
    d1, d2 = math.log2(n1) ** 3, math.log2(n2) ** 3   # d = log^3 n
    s1, s2 = s_integer_geometry(n1, d1), s_integer_geometry(n2, d2)
    e1, e2 = saved_exponent_to_log_exponent(n1, s1), saved_exponent_to_log_exponent(n2, s2)
    rows.append(GapRow(
        problem="Z-OV/Hopcroft, l2-Furthest-Pair, exact Bichrom.-l2-Closest-Pair, Z-Max-IP",
        dimension_regime="polylog (d = log^3 n)",
        best_known="n^{2-1/O(d)} = n^{2-1/O(log^3 n)} (Matousek92/AESW91/Yao82)",
        chen_bar="n^2 poly(d) / log^{omega(1)} n  (shave ALL polylogs)  [Thm 1.1]",
        s_small=s1, s_large=s2,
        bar_is_log_shave=True, bar_is_poly_shave=False,
        meets_bar=(e2 > e1 + 1e-9),   # is the log-exponent GROWING?
        conclusion_if_met="THR-of-THR",
        seth_status=classify_seth(False, "polylog", "integer"),   # log-shave bar
        problem_kind="integer",
        note="THE BOTTLENECK. At polylog d the saved factor is sub-log^1 n: NO shave.",
    ))

    # --- ROW 2: the same bottleneck at d = c log n (still no shave; SETH-hard).
    d1, d2 = 10.0 * math.log2(n1), 10.0 * math.log2(n2)   # d = 10 log n
    s1, s2 = s_integer_geometry(n1, d1), s_integer_geometry(n2, d2)
    e1, e2 = saved_exponent_to_log_exponent(n1, s1), saved_exponent_to_log_exponent(n2, s2)
    rows.append(GapRow(
        problem="Z-OV/Hopcroft, Z-Max-IP, exact l2 pair (at the SETH boundary dimension)",
        dimension_regime="d = 10 log n (= Theta(log n))",
        best_known="n^{2-1/O(d)} = n^{2-1/O(log n)} -> saved factor O(1) (no shave)",
        chen_bar="n^2 poly(d) / log^{omega(1)} n  [Thm 1.1]",
        s_small=s1, s_large=s2,
        bar_is_log_shave=True, bar_is_poly_shave=False,
        meets_bar=(e2 > e1 + 1e-9),
        conclusion_if_met="THR-of-THR",
        seth_status=classify_seth(False, "clog", "integer"),   # log-shave bar
        problem_kind="integer",
        note="SETH-hard at this d (down to 2^{O(log* n)}); best-known saves a constant factor only.",
    ))

    # --- ROW 3: the TRAP. Boolean OV at polylog d. Polynomial-method shave DEGRADES,
    #     and even if it cleared the shape-bar it gives only SYM-of-THR.
    d1, d2 = math.log2(n1) ** 3, math.log2(n2) ** 3   # d = log^3 n
    s1, s2 = s_awy_boolean_ov(n1, d1), s_awy_boolean_ov(n2, d2)
    e1, e2 = saved_exponent_to_log_exponent(n1, s1), saved_exponent_to_log_exponent(n2, s2)
    rows.append(GapRow(
        problem="Boolean OV (AWY15/Chan-Williams16) -- THE TRAP",
        dimension_regime="polylog (d = log^3 n)",
        best_known="n^{2-1/O(log c)}, c=log^2 n -> saved exponent s=o(1) but log-factor grows",
        chen_bar="n^2 poly(d) / log^{omega(1)} n  [Thm 1.2, NOT Thm 1.1]",
        s_small=s1, s_large=s2,
        bar_is_log_shave=True, bar_is_poly_shave=False,
        meets_bar=(e2 > e1 + 1e-9),   # log-exponent grows: clears the SHAPE bar
        conclusion_if_met="SYM-of-THR",   # but only the weaker conclusion
        seth_status=classify_seth(False, "polylog", "boolean"),   # log-shave bar
        problem_kind="boolean",
        note="WRONG PROBLEM + WRONG CONCLUSION: clears shape-bar but yields only SYM-of-THR.",
    ))

    # --- ROW 4: Boolean OV at d = c log n: a genuine POLYNOMIAL shave, but Boolean +
    #     d = Theta(log n), so SYM-of-THR only; and consistent with SETH (OV conj bites
    #     at omega(log n), not at Theta(log n)).
    d1, d2 = 4.0 * math.log2(n1), 4.0 * math.log2(n2)   # d = 4 log n (c = 4)
    s1, s2 = s_awy_boolean_ov(n1, d1), s_awy_boolean_ov(n2, d2)
    rows.append(GapRow(
        problem="Boolean OV (AWY15/Chan-Williams16)",
        dimension_regime="d = 4 log n (c = 4 constant)",
        best_known="n^{2-1/O(log 4)} = n^{2-Theta(1)} (genuine polynomial shave)",
        chen_bar="(no Chen bar here; this is the existing strong algorithm, for context)",
        s_small=s1, s_large=s2,
        bar_is_log_shave=False, bar_is_poly_shave=True,   # a genuine polynomial shave
        meets_bar=True,   # it IS a real subquadratic algorithm
        conclusion_if_met="SYM-of-THR",
        # poly shave but at d=Theta(log n) (NOT omega(log n)): does NOT refute SETH.
        seth_status=classify_seth(True, "clog", "boolean"),
        problem_kind="boolean",
        note="A real n^{2-Omega(1)} algorithm, but Boolean -> SYM-of-THR; consistent with SETH.",
    ))

    # --- ROW 5: Thm 1.5 item 1. Boolean Max-IP at d = n^eps. Baseline n^2 polylog
    #     (Coppersmith 1982 rect matmul); bar = log-shave; conclusion THR-of-THR.
    s_base = s_rect_matmul_baseline()   # 0.0: only logs separate baseline from bar
    rows.append(GapRow(
        problem="Boolean Max-IP at modest dimension (Thm 1.5 item 1)",
        dimension_regime="d = n^eps (eps small constant)",
        best_known="n^2 polylog(n) (Coppersmith 1982 fast rectangular matmul)",
        chen_bar="n^2 / log^{omega(1)} n  (shave logs off n^2 polylog)  [Thm 1.5.1]",
        s_small=s_base, s_large=s_base,
        bar_is_log_shave=True, bar_is_poly_shave=False,
        meets_bar=False,   # the polylogs are not yet shaved
        conclusion_if_met="THR-of-THR",
        seth_status=classify_seth(False, "n_eps", "boolean"),   # log-shave bar
        problem_kind="boolean",
        note="MOST ATTACKABLE: baseline already n^2 polylog; only the logs remain. SETH-consistent (log-shave).",
    ))

    # --- ROW 6: Thm 1.5 item 2. Boolean Max-IP at polylog d in n^{2-eps} CONSTANT eps.
    #     This IS a polynomial shave at a SETH-hard dimension: it WOULD refute SETH.
    rows.append(GapRow(
        problem="Boolean Max-IP at polylog dimension in n^{2-eps} (Thm 1.5 item 2)",
        dimension_regime="d = log^k n (= omega(log n))",
        best_known="n^{2-Omega(1/sqrt(d/log n))} (ACW16) -> s=o(1) at polylog d (no constant-eps shave)",
        chen_bar="n^{2-eps} for CONSTANT eps>0  [Thm 1.5.2]  (a polynomial shave)",
        s_small=0.0, s_large=0.0,   # best-known gives no constant-eps shave here
        bar_is_log_shave=False, bar_is_poly_shave=True,
        meets_bar=False,
        conclusion_if_met="THR-of-THR",
        # The BAR itself, if met (constant eps at omega(log n)), would refute SETH:
        seth_status=classify_seth(True, "polylog", "boolean"),   # poly-shave bar at omega(log n)
        problem_kind="boolean",
        note="SETH BARRIER: the bar n^{2-eps} at omega(log n) dimension would itself refute SETH.",
    ))

    # --- ROW 7: approximate Bichrom.-l2-Closest-Pair (Thm 1.2). Polynomial shave for
    #     constant eps, but approximate -> SYM-of-THR only.
    eps_approx_small = 1.0 / (math.log2(n2) ** 3)   # eps = 1/log^3 n: shave vanishes
    s_approx = s_approx_closest_pair(eps_approx_small)
    rows.append(GapRow(
        problem="(1+eps)-approx Bichrom.-l2-Closest-Pair (Thm 1.2)",
        dimension_regime="polylog d, eps = 1/log^3 n",
        best_known="n^{2-Omega(eps^{1/3})} (ACW16) -> s=Omega(1/log n) -> o(1) at eps=1/log^3 n",
        chen_bar="(1+1/log^{omega(1)} n)-approx in n^2 poly(d)/log^{omega(1)} n  [Thm 1.2]",
        s_small=s_approx, s_large=s_approx,
        bar_is_log_shave=True, bar_is_poly_shave=False,
        meets_bar=False,
        conclusion_if_met="SYM-of-THR",
        seth_status=classify_seth(False, "polylog", "approx"),   # log-shave bar
        problem_kind="approx",
        note="APPROXIMATE route -> SYM-of-THR only; at eps=1/log^3 n the shave is o(1). Rubinstein STOC2018 SETH-hard.",
    ))

    return rows


# ==========================================================================
# Reporting
# ==========================================================================


def _fmt_seth(s: str) -> str:
    return {"would-refute-SETH": "REFUTES-SETH",
            "consistent-open": "SETH-OK/open",
            "unclear": "unclear"}.get(s, s)


def main() -> int:
    print("=== Threshold-geometry gap calculator (Chen 2018, arXiv:1805.10698) ===\n")
    print("All running times are kept as the EXPONENT of n. The Chen Thm 1.1/1.5.1/1.2")
    print("bars are LOG-SHAVES (run in n^2 / log^{omega(1)} n; exponent stays exactly 2,")
    print("divide by a super-polylog factor). The Chen Thm 1.5.2 bar is a POLYNOMIAL")
    print("shave (n^{2-eps}, constant eps). The SETH floor forbids only the polynomial")
    print("shave at dimension omega(log n). The gap, conclusion, and SETH status follow.\n")

    rows = build_gap_rows()

    print("--- GAP TABLE (best-known vs Chen bar, per problem and dimension) ---\n")
    hdr = (f"{'problem':<46} | {'dim regime':<24} | {'meets':>5} | "
           f"{'conclusion':<11} | {'SETH':<13}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        concl = r.conclusion_if_met if r.meets_bar else "(not met)"
        print(f"{r.problem[:46]:<46} | {r.dimension_regime[:24]:<24} | "
              f"{('YES' if r.meets_bar else 'no'):>5} | {concl:<11} | "
              f"{_fmt_seth(r.seth_status):<13}")
    print()

    print("--- Per-row gap detail ---\n")
    for i, r in enumerate(rows, 1):
        print(f"[{i}] {r.problem}")
        print(f"    dimension : {r.dimension_regime}")
        print(f"    best known: {r.best_known}")
        print(f"    Chen bar  : {r.chen_bar}")
        print(f"    gap       : {r.gap}")
        print(f"    conclusion if met: {r.conclusion_if_met}   SETH: {_fmt_seth(r.seth_status)}")
        print(f"    note      : {r.note}")
        print()

    # ----------------------------------------------------------------------
    # The log-shave vs polynomial-shave distinction, numerically visible.
    # ----------------------------------------------------------------------
    print("=== Log-shave vs polynomial-shave (why the bar is SETH-consistent) ===\n")
    print("A LOG-SHAVE n^2/log^c n keeps the exponent at 2 (it is n^{2-o(1)}), so it does")
    print("NOT cross the SETH floor. A POLYNOMIAL shave n^{2-eps} (constant eps) drops the")
    print("exponent below 2 and WOULD refute SETH at dimension omega(log n). Below: the")
    print("saved-exponent s = log_n(saved factor). s -> 0 is a log-shave (SETH-OK); s")
    print("bounded away from 0 is a polynomial shave (SETH-relevant).\n")
    print(f"{'n':>10} | {'log-shave n^2/log^3 n: s':>26} | {'poly-shave n^{1.9}: s':>22}")
    print("-" * 64)
    for log2n in (32, 64, 128, 256):
        n = 2.0 ** log2n
        # log-shave saved factor = log^3 n; its saved exponent of n:
        log3n = math.log2(n) ** 3
        s_log = math.log2(log3n) / math.log2(n)   # = log_n(log^3 n) -> 0
        s_poly = 0.1                               # n^{1.9}: constant saved exponent
        print(f"{('2^'+str(log2n)):>10} | {s_log:>26.6f} | {s_poly:>22.4f}")
    print()
    print("Reading: the log-shave's saved exponent s -> 0 as n grows (it is n^{2-o(1)},")
    print("SETH permits it). The polynomial shave's s stays at 0.1 (n^{1.9}, SETH forbids")
    print("it at omega(log n)). The Chen Thm 1.1 / 1.5.1 bar lives in the LEFT column:")
    print("SETH-consistent, genuinely open. Only Thm 1.5.2 lives in the RIGHT column.\n")

    # ----------------------------------------------------------------------
    # Self-checks pinning the load-bearing coordinates.
    # ----------------------------------------------------------------------
    bottleneck = rows[0]            # exact integer geometry at polylog d
    bottleneck_clog = rows[1]
    trap = rows[2]                  # Boolean OV at polylog d
    boolean_ov_clog = rows[3]
    thm15_attackable = rows[4]      # Boolean Max-IP at d = n^eps
    thm15_seth_bar = rows[5]        # Boolean Max-IP at polylog d in n^{2-eps}
    approx_cp = rows[6]

    # --- (A) The Boolean-OV trap, pinned. ---
    # The AWY Boolean-OV shave, even where its log-factor grows (clears the SHAPE bar),
    # yields ONLY the weaker SYM-of-THR conclusion (Chen Thm 1.2), never THR-of-THR.
    assert trap.problem_kind == "boolean"
    assert trap.meets_bar, "Boolean OV at polylog d clears the shave-all-logs SHAPE bar (log-exponent grows)"
    assert trap.conclusion_if_met == "SYM-of-THR", \
        "TRAP: Boolean OV gives only SYM-of-THR (Thm 1.2), NOT THR-of-THR (Thm 1.1)"
    assert boolean_ov_clog.conclusion_if_met == "SYM-of-THR", \
        "Boolean OV at d=c log n is a real poly shave but still only SYM-of-THR (Boolean route)"
    # No Boolean row ever yields THR-of-THR via the SHAVE conclusion at polylog d.
    boolean_thr_of_thr_via_shave = [
        r for r in rows
        if r.problem_kind == "boolean" and r.meets_bar
        and r.conclusion_if_met == "THR-of-THR" and r.bar_is_log_shave
        and r.dimension_regime.startswith("polylog")
    ]
    assert not boolean_thr_of_thr_via_shave, \
        "no Boolean polylog-dimension log-shave gives THR-of-THR (the Boolean-OV trap)"

    # --- (B) The bottleneck is the EXACT integer geometry at polylog d, and it meets
    #         the bar NOWHERE in the relevant regime (zero log-shave). ---
    assert bottleneck.problem_kind == "integer"
    assert not bottleneck.meets_bar, "integer geometry at polylog d does NOT meet the bar (the bottleneck)"
    assert not bottleneck_clog.meets_bar, "integer geometry at d=c log n does NOT meet the bar either"
    assert bottleneck.conclusion_if_met == "THR-of-THR", "the bottleneck targets the THR-of-THR prize"
    # The bottleneck's saved factor at polylog d is sub-log^1 n (log-exponent < 1).
    e_bottleneck = saved_exponent_to_log_exponent(2.0 ** 128, bottleneck.s_large)
    assert e_bottleneck < 1.0, \
        "at polylog d the integer saved factor is sub-log^1 n (does not even reach one log factor)"

    # --- (C) SETH consistency of the MAIN target (log-shave) vs the one SETH barrier. ---
    # The main THR-of-THR route (Thm 1.1, Thm 1.5.1) is SETH-CONSISTENT / open.
    assert bottleneck.seth_status == "consistent-open", \
        "Thm 1.1 bottleneck is a log-shave: SETH-consistent (n^2/log^{omega(1)} n is n^{2-o(1)})"
    assert thm15_attackable.seth_status == "consistent-open", \
        "Thm 1.5.1 (Boolean Max-IP at n^eps, log-shave) is SETH-consistent"
    # The single SETH-REFUTING sub-target: Thm 1.5.2 (n^{2-eps} at omega(log n)).
    assert thm15_seth_bar.bar_is_poly_shave, "Thm 1.5.2 bar is a polynomial shave n^{2-eps}"
    assert thm15_seth_bar.seth_status == "would-refute-SETH", \
        "Thm 1.5.2 bar (constant eps at omega(log n)) WOULD refute SETH: the lone conditional barrier"
    # The approximate-closest-pair route (Thm 1.2) is a log-shave bar (SETH-consistent)
    # and gives only SYM-of-THR; Rubinstein STOC 2018 makes the approximation SETH-hard
    # at the leading exponent, but the log-shave bar still does not refute SETH.
    assert approx_cp.problem_kind == "approx"
    assert approx_cp.conclusion_if_met == "SYM-of-THR", \
        "approximate Bichrom.-closest-pair gives only SYM-of-THR (Thm 1.2)"
    assert approx_cp.seth_status == "consistent-open", \
        "the approximate-closest-pair log-shave bar is SETH-consistent"

    # Exactly ONE row in the whole table would refute SETH (the lone barrier):
    refuting = [r for r in rows if r.seth_status == "would-refute-SETH"]
    assert len(refuting) == 1 and refuting[0] is thm15_seth_bar, \
        "exactly one Chen sub-target (Thm 1.5.2) is SETH-refuting; every other route is SETH-consistent"

    # --- (D) The log-shave bar is itself n^{2-o(1)}: its saved exponent s -> 0. ---
    # Honest version (the same asymptotic-vs-feasible discipline as e_tc0_sat_savings):
    # s -> 0 is an ASYMPTOTIC statement. At a finite scale (n = 2^256) it is ~0.094, NOT
    # tiny. We test the TREND (strictly decreasing toward 0 as n grows), which is the
    # correct way to certify "log-shave is o(1)", and we contrast with a constant
    # poly-shave exponent that does NOT decay. We do NOT pretend s is negligible at
    # feasible scale; we certify the limit, not a finite threshold.
    # Operate directly on L = log2(n) to avoid overflow (2^4096 overflows a float).
    def s_logshave_for_log2n(log2n: float) -> float:
        return math.log2(log2n ** 3) / log2n          # log_n(log^3 n) = log2(log^3 n)/log2 n
    s_seq = [s_logshave_for_log2n(float(k)) for k in (32, 64, 128, 256, 1024, 4096)]
    assert all(s_seq[i] > s_seq[i + 1] for i in range(len(s_seq) - 1)), \
        "the log-shave saved exponent must strictly DECREASE with n (it is o(1))"
    assert s_seq[-1] < 0.02, \
        "by n = 2^4096 the log-shave saved exponent is < 0.02 (visibly heading to 0)"
    s_polyshave = 0.1
    # The poly-shave exponent is CONSTANT: it never decays, so it eventually exceeds any
    # log-shave exponent. That qualitative gap is the SETH dividing line.
    assert s_polyshave > s_seq[-1], \
        "a constant poly-shave exponent (n^{1.9}) eventually dominates the decaying log-shave"
    assert s_logshave_for_log2n(32.0) > s_polyshave, \
        "at small n the log^3 n factor can LOOK larger; only the asymptotic trend separates them"

    # --- (E) The SETH classifier separates the two regimes correctly. ---
    # First argument is bar_is_poly_shave: True = n^{2-eps} bar, False = log-shave bar.
    assert classify_seth(True, "polylog", "boolean") == "would-refute-SETH", \
        "a polynomial-shave bar at omega(log n) dimension refutes SETH"
    assert classify_seth(False, "polylog", "integer") == "consistent-open", \
        "a log-shave bar is always SETH-consistent (it is n^{2-o(1)})"
    assert classify_seth(True, "clog", "boolean") == "consistent-open", \
        "a polynomial shave at d=Theta(log n) (NOT omega(log n)) does not refute SETH (AWY lives here)"
    assert classify_seth(True, "polylog", "integer") == "would-refute-SETH", \
        "a polynomial-shave bar for the exact integer problems at polylog d also refutes SETH"

    # --- (F) Empirical status: NEXP not in poly-size THR-of-THR is OPEN (2026). ---
    # Operationalized: NO row that targets THR-of-THR actually meets its bar with the
    # known algorithm. The lower bound is therefore not delivered by any row here.
    thr_of_thr_delivered = [
        r for r in rows if r.conclusion_if_met == "THR-of-THR" and r.meets_bar
    ]
    assert not thr_of_thr_delivered, \
        "no known algorithm meets a THR-of-THR bar: NEXP not in poly THR-of-THR is OPEN as of 2026"

    print("=== Self-check OK ===")
    print("(A) TRAP RESOLVED: the AWY Boolean-OV shave clears the shave-all-logs SHAPE")
    print("    bar (its log-exponent grows) but yields ONLY SYM-of-THR (Chen Thm 1.2),")
    print("    NOT THR-of-THR (Thm 1.1). It is the wrong problem (Boolean, not integer)")
    print("    and the wrong conclusion. The Boolean-OV shave does NOT settle THR-of-THR.")
    print("(B) BOTTLENECK: the EXACT integer geometry (Z-OV/Hopcroft, Z-Max-IP, exact")
    print("    l2 furthest/closest pair) at polylog d is the THR-of-THR obstruction; its")
    print("    best-known saved factor is sub-log^1 n (zero log-shave). Gap = full")
    print("    log^{omega(1)} n.")
    print("(C) SETH: the MAIN target (Thm 1.1, Thm 1.5.1) is a LOG-SHAVE, hence")
    print("    SETH-CONSISTENT and genuinely OPEN. Exactly one sub-target (Thm 1.5.2,")
    print("    n^{2-eps} at omega(log n) dimension) WOULD refute SETH: the lone barrier.")
    print("(D) The Chen log-shave bar is itself n^{2-o(1)} (saved exponent s -> 0); SETH")
    print("    forbids only the constant-exponent region n^{2-eps}. Different scales.")
    print("(F) NEXP not in poly-size THR-of-THR is OPEN as of 2026: no known algorithm")
    print("    meets any THR-of-THR bar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
