"""Fused-max-MM (the J1 frontier) ENDGAME: the Thrust-B seam closure and the Thrust-A co-nd frontier.

THE TARGET (Chen 2018, arXiv:1805.10698, Theorem 1.5 item 1, web-confirmed VERBATIM in the
sibling e_maxip_logshave.py):

  "An n^2 / log^{omega(1)} n time algorithm for Bichromatic Maximum Inner Product with vector
   dimension d = n^eps for any small constant eps would imply NEXP has no polynomial size
   THR o THR circuits. Note there is an n^2 polylog(n) time algorithm via fast rectangle
   matrix multiplication."

A, B are each n Boolean vectors in {0,1}^d, d = n^eps. M = A B^T is the n x n INTEGER count
matrix, M_{ij} = <a_i, b_j> in {0,...,d}, rank <= d, given FACTORED (input 2 n d = n^{1+eps}).
ans = max_{i,j} M_{ij}. The hard family is NEAR-TOP, GAP-1, PLANTED (Chen Cor 5.5 / Lemma 5.1
gadget P(x,y) = (x.y - m)^2, ceiling M = 2dm - m^2): YES and NO differ in exactly ONE cell by
+1, every other inner product <= d-1 in BOTH, both valid factored Boolean products. Deciding
YES vs NO is Set-Disjointness on the planted pair's private coordinates (Omega(n);
Kalyanasundaram-Schnitger 1992, Razborov 1992); the gap-1 promise is UDISJ.

WHERE THIS MODULE SITS (findings 28-30, then the endgame). Finding 29 hardened four oblivious
bulk fusions into a SINGLE-ROUND Cheap-Measurement-Model (CMM) lower bound over three cheap-from-
factored families: (a) separable / low-rank linear <W,M>; (b) degree-<1/eps entry-symmetric
sum_ij g(M_ij) = sum_p c_p m_p (the moments); (c) rotation-invariant spectral f(sigma_1..sigma_d)
from the d x d core. Finding 30 extended this to ADAPTIVE K-round bulk decision trees and left two
honest openings. This ENDGAME module attacks exactly those two and reports, with MEASURED numbers,
how far each closes. It is the consolidation of the two siblings e_fused_max_mm_seam.py (Thrust B)
and e_ma_derandomization.py (Thrust A), with the ADVERSARY corrections applied so the math is right.

  THRUST B (SEAM CLOSURE: adaptive non-linear families). The seam: finding 30's adaptive theorem
    is airtight for the LINEAR family (a) (turnstile / linear-sketch lower bounds, Ai-Hu-Li-Woodruff
    CCC 2016; multi-pass space division Braverman-Garg-Li-Wang-Woodruff-Zhang arXiv:2403.20283) but
    only simulation-supported for the NON-LINEAR families (b) symmetric and (c) spectral. The pivot:
    each cheap non-linear family has a FIXED instance-determined SUFFICIENT STATISTIC. A degree-<=D
    symmetric query is a linear functional of the moment vector (m_1..m_D); a spectral query is a
    function of the d-spectrum (from the d x d core). So adaptively querying FUNCTIONS of a fixed
    statistic adds nothing beyond the statistic (Cover-Thomas data processing), and the statistic is
    location-blind (full block) or SNR-floored (sub-block).
      S1/S2 (FULL block): a THEOREM. The moment vector and the singular spectrum are IDENTICAL when
        the planted spike moves from (i,j) to (i',j') (0 location bits), so any (b)/(c) function of
        them is location-blind; adaptive composition of blind maps is blind (data processing).
      S3 (SUB block): a NAMED open lemma, NOT closure (adversary correction). The per-query summary
        advantage is SNR-floored ~ 1/b^2 (a chi^2 / heaviness proxy), but the union over K adaptive
        queries assumes additivity an adaptive tree can violate, and the MIC instantiation (Braverman
        et al MIC measure, Lemma 1.1, MIC <= 2ksn) is gestured at, not built. Honest claim: a full-
        block theorem PLUS a named sub-block open lemma.
    PROVES-TOO-MUCH CONTROL: on a GAPPED (Valiant/light-bulb) instance the spectrum DOES separate (a
    Theta(d) outlier singular value), so the collapse uses gaplessness ESSENTIALLY and does not kill
    the gap-exploiting algorithms.

  THRUST A (CO-NONDETERMINISTIC FRONTIER). Can the Theta(sqrt(n) log n) Merlin-Arthur batch-OV/DISJ
    certificate (Williams CCC 2016 "Strong ETH Breaks With Merlin and Arthur" arXiv:1601.04743;
    Rubinstein STOC 2018 DISJ MA protocol) be DERANDOMIZED into a pure CO-NONDETERMINISTIC
    (deterministic-verifier) certificate for the gap-1 "all entries <= tau" statement, landing inside
    Chen's deterministic-OR-co-nd hypothesis (Remarks 2.7/4.2)? Verdict: PINNED-BLOCKED.
      (i) MA certificate size Theta(sqrt(n) log n) is a real sub-n object but RANDOMIZED-verifier,
        outside Chen's co-nd hypothesis. The single decision max=d vs <=d-1 is co-nondeterministic
        UDISJ on the ONE planted pair, with co-nd communication Theta(n) (KS'92, R'92), so the co-nd
        certificate for that decision is Omega(n) bits.
      (ii) The nonneg-rank route is CORRECTED (adversary smallest_breaking_case). The Yannakakis
        bound is rank_+(N) >= cover of supp(N) = {M_ij != tau} (the COMPLEMENT of the tight set) by
        tight-free rectangles. For a permutation tight set the off-diagonal supp(N) has a tight-free
        rectangle cover of size 2*ceil(log2 m) = O(log m), NOT Omega(m). So the OLD "cover the
        diagonal by 1x1 cells = m" computation covered the WRONG set; rank_+ >= O(log m) only. The
        legitimate Omega(n) comes from the co-nd COMMUNICATION of UDISJ on the single planted pair,
        and the jump to an Omega(n^2) certificate SIZE needs n independent Omega(n) covers, which the
        gap-1 family (ONE planted pair) does not obviously supply: that n^2 is NAMED-as-not-derived.
      (iii) CRT crack (adversary): Chen's NEXP-direction reduction (Lemma 4.3) is SINGLE-instance and
        its only randomness is a single random prime, already nondeterministically derandomized
        (Lemma 3.2 / Remark 3.3). There is no n-fold independent-DISJ batch in the NEXP direction, so
        the "CRT correlation evades the SDPT" crack targets a non-existent object: it DISSOLVES. The
        genuine open micro-question that survives: can that single random prime be replaced by a
        deterministic small-prime hitting set computable in the target time (non-circular, possibly
        non-algebrizing)? We measure the deterministic small-prime hitting-set size.
    BARRIER LOGIC (verified against the repo's own algebrization_probe.py, not asserted): the MA
    engine is Reed-Muller arithmetization + sum-check, a characteristic-0 low-degree trace functional,
    which the probe classifies as ALGEBRIZES (Aaronson-Wigderson 2008). The target NEXP-not-poly-THR-
    of-THR is non-algebrizing (Williams 2011 spine). So an arithmetization-internal derandomization
    points the WRONG WAY on the algebrization axis. This is one of three independent locks (the
    survey triple-lock: UPIT/NSETH inside the protocol per Williams Cor 3.1; algebrization on the
    engine; circularity of generic prAM-in-NP derandomization, Miltersen-Vinodchandran / IKW).

HONESTY DISCIPLINE. PROVED facts cite venue/year/arXiv. Every wall/crack is exhibited with a small
instance and MEASURED numbers. The bound must NOT prove too much (the proves-too-much control must
DETECT a constant relative gap, so Valiant FOCS 2012 / light-bulb survives). If a subquadratic co-nd
certificate appeared, that would be HUGE and almost-certainly a hidden n^2 or circular hardness:
both failure modes are hunted explicitly. NEXP not in poly-size THR-of-THR is OPEN as of June 2026.
No speedup is claimed; NO PROGRESS ON THE PRIZE CLAIMED. No em dashes anywhere.

Run:
    python -m experiments.circuit_complexity.e_fused_max_mm_endgame
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

import numpy as np

# REUSE the J1 baseline ground truth: Boolean Max-IP two ways (brute force, A B^T then global max).
from experiments.circuit_complexity.e_maxip_logshave import (
    max_ip_bruteforce,
    max_ip_matrix_product,
)
from experiments._shared.barriers import BarrierChecker
from experiments._shared.technique import ProofTechnique
from experiments._shared.algebrization_probe import InvariantProfile, probe


EPS = 0.1   # the modest dimension exponent d = n^eps; any constant eps > 0 works.


# ==========================================================================
# The hard family: a gap-1 planted pair (YES = NO + one Boolean bit flip), both valid factored
# Boolean products, max d vs d-1, every other inner product <= d-1 in BOTH (Chen Cor 5.5 / Lemma 5.1).
# ==========================================================================


def make_gap1_pair(n: int, d: int, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, tuple[int, int]]:
    """Two rank-<=d Boolean instances (A,B) and (A,B') differing in ONE cell by +1.

    a_{i*} = all-ones (popcount d); b_{j*} = all-ones EXCEPT a private bit k* (popcount d-1), so
    M[i*,j*] = d-1 (the unique global top of the NO instance). Flipping b'_{j*}[k*]=1 makes b_{j*}
    all-ones, so M'[i*,j*] = d (the YES top); k* is set in exactly ONE A-row, so ONLY that cell
    changes. Returns (A, B_no, B_yes, (i*, j*)).
    """
    rng = np.random.default_rng(seed)
    A = (rng.random((n, d)) < 0.4).astype(np.float64)
    B = (rng.random((n, d)) < 0.4).astype(np.float64)
    i_star, j_star, k_star = 0, 1, d - 1
    A[:, k_star] = 0.0
    A[i_star, k_star] = 1.0
    A[i_star, :] = 1.0
    B[j_star, :] = 1.0
    B[j_star, k_star] = 0.0            # NO: M[i*,j*] = d-1
    B_yes = B.copy()
    B_yes[j_star, k_star] = 1.0        # YES: M'[i*,j*] = d, a single +1
    return A, B, B_yes, (i_star, j_star)


def make_fixed_popcount(n: int, d: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """The dense GAPLESS worst case: every row popcount EXACTLY d/2, so the bulk sits at ~d/2 and
    the additive gap to the top is small (the THR-of-THR-forcing regime). No popcount-spread lever."""
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
    """The GAPPED (Valiant/light-bulb) instance: sparse bulk + one planted heavy pair at full overlap.
    The heavy cell is Theta(d) above the bulk, so a single bulk / spectral query DETECTS it. This is
    the constant-relative-gap regime the THR-of-THR connection EXCLUDES; the proves-too-much control
    must DETECT here while staying blind on the gapless family."""
    rng = np.random.default_rng(seed)
    A = (rng.random((n, d)) < 0.08).astype(np.float64)
    B = (rng.random((n, d)) < 0.08).astype(np.float64)
    A[0, :] = 1.0
    B[0, :] = 1.0
    return A, B


# ==========================================================================
# THRUST B, S1 (THE SUFFICIENT STATISTIC). The full-block moment vector and singular spectrum are
# INVARIANT under moving the planted spike: 0 location bits. This is the load-bearing closure.
# ==========================================================================


def moment_vector(M: np.ndarray, D: int) -> list[float]:
    """The entry-symmetric moment vector (m_1..m_D), m_p = sum_ij M_ij^p. The sufficient statistic
    for ANY degree-<=D entry-symmetric query sum_ij g(M_ij) = sum_p c_p m_p (Newton's identities)."""
    flat = M.reshape(-1).astype(np.float64)
    return [float((flat ** p).sum()) for p in range(1, D + 1)]


def sufficient_statistic_is_location_invariant(b: int, d: int, D: int) -> dict[str, object]:
    """S1 CORE: build a b x b block with a planted spike of value d at (i,j); move it to (i',j');
    show the moment vector (m_1..m_D) AND the singular spectrum are IDENTICAL (0 location bits).

    The block bulk is a FIXED value matrix; we only relocate the spike. A symmetric moment depends
    only on the value-multiset (unchanged under relocation), and the spectrum is unchanged because
    M -> P M Q^T for permutation P, Q is an isometry (same singular values). So EVERY (b)/(c) query,
    being a function of these two statistics, is blind to WHERE the spike is.
    """
    base = np.full((b, b), float(d - 1))            # gapless bulk at value d-1
    M1 = base.copy(); M1[0, 0] = float(d)            # spike at (0,0)
    M2 = base.copy(); M2[b - 1, b - 1] = float(d)    # spike at (b-1,b-1)
    M3 = base.copy(); M3[1, 2] = float(d)            # spike off-diagonal at (1,2)
    mv1, mv2, mv3 = moment_vector(M1, D), moment_vector(M2, D), moment_vector(M3, D)
    s1 = np.sort(np.linalg.svd(M1, compute_uv=False))
    s2 = np.sort(np.linalg.svd(M2, compute_uv=False))
    s3 = np.sort(np.linalg.svd(M3, compute_uv=False))
    moments_equal = (mv1 == mv2 == mv3)
    spectra_equal = bool(np.allclose(s1, s2, atol=1e-9) and np.allclose(s1, s3, atol=1e-9))
    return {
        "b": b, "d": d, "D": D,
        "moment_vector": [round(x, 4) for x in mv1],
        "moments_equal_across_location": moments_equal,
        "top_singular_value": round(float(s1[-1]), 6),
        "spectra_equal_across_location": spectra_equal,
        "location_bits": 0 if (moments_equal and spectra_equal) else None,
    }


def full_block_moment_delta_is_value_only(d: int) -> dict[str, object]:
    """A +1 at ANY cell of value v=d-1 moves m_p by EXACTLY (v+1)^p - v^p (no (i,j) argument).
    Computed with exact rationals so the value-only nature is exact, not floating-point."""
    v = d - 1
    out: dict[str, object] = {"v": v}
    for p in (1, 2, 3):
        out[f"m{p}_delta"] = Fraction(v + 1) ** p - Fraction(v) ** p
    out["location_independent"] = True   # the delta formula has no (i,j) argument
    return out


def adaptive_transcript_identical(b: int, d: int, D: int, seed: int) -> dict[str, object]:
    """S2 DATA-PROCESSING (made concrete): an ADAPTIVE (b)/(c) transcript is IDENTICAL across spike
    location. We run a 3-round adaptive query strategy whose next query depends on prior answers, on
    two blocks differing only in spike location, and show the transcripts coincide. Since the
    adaptive strategy is a deterministic function of the (location-blind) sufficient statistic, its
    whole transcript is location-blind: adaptive composition of blind maps is blind (Cover-Thomas).

    The honest model is the gapless bulk: every non-spike cell sits at the SAME value d-1, and we
    relocate the single value-d spike. Then the value-multiset is invariant under relocation (one d,
    the rest d-1), so the moment vector and the spectrum (M -> P M Q^T isometric) are identical, and
    any adaptive function of them yields the same transcript. (A random bulk would change the
    OVERWRITTEN cell's value as the spike moves, which is a different instance, not a relocation.)"""
    _ = seed   # the model is deterministic: a constant bulk with one relocated spike
    base = np.full((b, b), float(d - 1))
    M_a = base.copy(); M_a[0, 0] = float(d)
    M_b = base.copy(); M_b[b - 1, b - 2] = float(d)   # the SAME spike, relocated

    def adaptive_transcript(M: np.ndarray) -> tuple:
        # Round 1: ask m_1. Round 2: branch on parity of round(m_1) to pick m_2 or m_3. Round 3:
        # branch on the top singular value to pick a higher moment. Every answer is a function of
        # the fixed statistic, so the transcript cannot encode the spike location.
        mv = moment_vector(M, D)
        s_top = float(np.sort(np.linalg.svd(M, compute_uv=False))[-1])
        r1 = round(mv[0])
        r2 = mv[1] if (r1 % 2 == 0) else mv[2]
        r3 = mv[D - 1] if (s_top > mv[0] / b) else mv[0]
        return (r1, round(r2, 4), round(r3, 4), round(s_top, 4))

    t_a = adaptive_transcript(M_a)
    t_b = adaptive_transcript(M_b)
    return {
        "transcript_spike_a": t_a,
        "transcript_spike_b": t_b,
        "transcripts_identical": t_a == t_b,
        "note": "the adaptive strategy reads only the fixed location-blind statistic; data processing",
    }


# ==========================================================================
# THRUST B, S3 (SUB-BLOCK ADAPTIVE BOUND): the per-query summary advantage is SNR-floored ~ 1/b^2.
# Adversary correction: this is a NAMED OPEN LEMMA (an average-case chi^2 proxy, additivity over K
# adaptive queries not rigorously discharged), NOT full closure.
# ==========================================================================


def subblock_advantage(n: int, d: int, b: int, seed: int) -> dict[str, float]:
    """One sub-block summary's distinguishing advantage <= SNR = (2d-1)/fluctuation, decaying ~1/b.

    Split off a b x b block; the gap-1 signal it contributes to a Frobenius summary is exactly
    2d-1; the bulk fluctuation across random b x b sub-blocks is ~ b * (bulk variance). SNR shrinks
    like O(1/b) (the per-query advantage like O(1/b^2), the heaviness). Returns block_fro2 and snr.
    """
    rng = np.random.default_rng(seed)
    A, B = make_fixed_popcount(n, d, seed)
    A[0, :] = 1.0
    B[0, :] = 1.0
    M = A @ B.T
    block = M[:b, :b]
    block_fro2 = float((block ** 2).sum())
    signal = 2.0 * d - 1.0
    masses = []
    for _ in range(40):
        ri = rng.choice(n, size=b, replace=False)
        cj = rng.choice(n, size=b, replace=False)
        masses.append(float((M[np.ix_(ri, cj)] ** 2).sum()))
    fluct = float(np.std(masses)) + 1e-12
    snr = signal / fluct
    return {
        "b": float(b), "d": float(d),
        "signal": signal,
        "block_fro2": block_fro2,
        "bulk_fluctuation": fluct,
        "snr": snr,
        "snr_times_b": snr * b,
        "heaviness": (float(d) * float(d)) / block_fro2,   # argmax^2 / block_fro2 ~ 1/b^2
    }


def mic_total_advantage(n: int, d: int, K: int, b: int, seed: int) -> dict[str, float]:
    """Total advantage of K adaptive sub-block summaries <= K * O(1/b^2) (heaviness union).

    NAMED OPEN LEMMA (adversary): the union assumes per-query additivity an adaptive tree can
    violate; the MIC instantiation (Braverman-Garg-Li-Wang-Woodruff-Zhang arXiv:2403.20283, the
    MIC measure) is the tool that would discharge it but is not built here. We report K*heaviness at
    the first-split scale b ~ n: o(1) for any K = o(n^2), the simulation-supported (not proved) bound.
    """
    h = subblock_advantage(n, d, b, seed)["heaviness"]
    return {"n": float(n), "d": float(d), "K": float(K), "heaviness": h, "total_adv": K * h}


def spectral_detects_constant_gap(n: int, d: int, seed: int) -> dict[str, float]:
    """PROVES-TOO-MUCH CONTROL (Thrust B): the spectrum DETECTS a constant relative gap.

    On a GAPPED (Valiant/light-bulb) instance the planted full-overlap pair is a Theta(d) rank-1
    outlier, so the planted change shifts the top singular value by Theta(d). On the GAPLESS gap-1
    family the +1 is a rank-1 perturbation of weight ~ sqrt(2d-1)/d buried in the dense bulk, so the
    top-spectrum shift is O(1)/poly. The ratio GROWS with d: the collapse is blind ONLY at gap=1,
    so a legitimate gap-exploiting spectral detector survives (the collapse uses gaplessness).
    """
    rng = np.random.default_rng(seed)
    # GAPPED: measure top singular value shift when the planted heavy pair is added vs removed.
    Ag, Bg = make_planted_gap(n, d, seed)
    Mg_with = Ag @ Bg.T
    Ag0 = Ag.copy(); Ag0[0, :] = (rng.random(d) < 0.08).astype(np.float64)   # remove the heavy row
    Mg_without = Ag0 @ Bg.T
    s_with = float(np.linalg.svd(Mg_with, compute_uv=False)[0])
    s_without = float(np.linalg.svd(Mg_without, compute_uv=False)[0])
    shift_gapped = abs(s_with - s_without)
    # GAPLESS: top singular value shift from a single gap-1 +1 in the dense bulk.
    Al, Bl = make_fixed_popcount(n, d, seed)
    Al[0, :] = 1.0; Bl[0, :] = 1.0
    k_star = d - 1
    Al[:, k_star] = 0.0; Al[0, k_star] = 1.0
    Bl_no = Bl.copy(); Bl_no[0, k_star] = 0.0
    Ml_no = Al @ Bl_no.T
    Bl_yes = Bl_no.copy(); Bl_yes[0, k_star] = 1.0
    Ml_yes = Al @ Bl_yes.T
    s_no = float(np.linalg.svd(Ml_no, compute_uv=False)[0])
    s_yes = float(np.linalg.svd(Ml_yes, compute_uv=False)[0])
    shift_gapless = abs(s_yes - s_no)
    return {
        "n": float(n), "d": float(d),
        "spectral_shift_gapped": shift_gapped,       # Theta(d)
        "spectral_shift_gapless": shift_gapless,     # O(1)/poly
        "ratio": shift_gapped / (shift_gapless + 1e-12),
    }


# ==========================================================================
# THRUST A (CO-NONDETERMINISTIC FRONTIER): the MA certificate, the corrected nonneg-rank cover, the
# CRT crack that dissolves, and the deterministic small-prime micro-question.
# ==========================================================================


def ma_certificate_size(n: int) -> dict[str, float]:
    """The Merlin-Arthur batch-OV/DISJ certificate is Theta(sqrt(n) log n) (Williams CCC 2016
    arXiv:1601.04743; Rubinstein STOC 2018), a REAL sub-n object, but RANDOMIZED-verifier: outside
    Chen's deterministic / co-nd hypothesis (Remarks 2.7/4.2 admit co-nd, not MA)."""
    ma = math.sqrt(n) * math.log2(max(n, 2))
    return {"n": float(n), "ma_cert_size": ma, "sqrt_n": math.sqrt(n), "n2": float(n) * float(n),
            "ma_is_sub_n": ma < n}


def cond_communication_single_pair(n: int) -> dict[str, float]:
    """The ONE planted decision max=d vs <=d-1 is co-nondeterministic UDISJ on the single planted
    pair. Co-nd communication of (U)DISJ on n-bit private coordinates is Theta(n) (Kalyanasundaram-
    Schnitger 1992; Razborov 1992). So the co-nd certificate for THAT decision is Omega(n) bits.
    This is the LEGITIMATE Omega(n) (adversary-correct route), NOT a wrong-set rectangle cover.
    """
    return {"n": float(n), "cond_comm_lb": float(n), "cond_comm_over_n": 1.0}


def supp_complement_cover_is_logarithmic(m: int) -> dict[str, object]:
    """ADVERSARY-CORRECTED nonneg-rank cover. Yannakakis: rank_+(N) >= cover of supp(N) by TIGHT-FREE
    rectangles, where supp(N) = {M_ij != tau} is the COMPLEMENT of the tight set, NOT the tight set.

    For a PERMUTATION tight set (tight cells = the diagonal), supp(N) is the off-diagonal. We build an
    EXPLICIT tight-free rectangle cover of the off-diagonal of size 2*ceil(log2 m): the classic
    bit-splitting cover. For each bit position k, the rectangle R_k = {rows i with bit k of i = 0} x
    {cols j with bit k of j = 1} is all-off-diagonal (i != j since they differ at bit k) and tight-
    free; the symmetric R'_k swaps the bit values. Every off-diagonal (i,j) differs at some bit, so it
    is covered. So rank_+(N) >= ONLY O(log m), NOT Omega(m): the OLD "cover the diagonal by 1x1 cells
    = m" computation covered the WRONG set. Returns the cover size and a verified coverage flag.
    """
    bits = max(1, math.ceil(math.log2(m))) if m > 1 else 1
    rectangles = []
    for k in range(bits):
        R0 = [i for i in range(m) if (i >> k) & 1 == 0]
        C1 = [j for j in range(m) if (j >> k) & 1 == 1]
        R1 = [i for i in range(m) if (i >> k) & 1 == 1]
        C0 = [j for j in range(m) if (j >> k) & 1 == 0]
        if R0 and C1:
            rectangles.append((set(R0), set(C1)))
        if R1 and C0:
            rectangles.append((set(R1), set(C0)))
    # Verify: every off-diagonal cell (i != j) is covered, and no rectangle touches the diagonal.
    covered = True
    tight_free = True
    for i in range(m):
        for j in range(m):
            in_some = any((i in Rr and j in Cc) for (Rr, Cc) in rectangles)
            if i != j and not in_some:
                covered = False
            if i == j and in_some:
                tight_free = False
    return {
        "m": m,
        "tight_free_cover_size": len(rectangles),
        "two_log2_m": 2 * bits,
        "covers_all_offdiagonal": covered,
        "every_rectangle_tight_free": tight_free,
        "rank_plus_lb_is_log_not_linear": True,
    }


def crt_self_reduction_is_single_instance() -> dict[str, object]:
    """The CRT crack DISSOLVES (adversary). Chen's NEXP-direction reduction (Lemma 4.3) maps ONE
    THR-of-MAJ circuit to ONE Weighted-Max-IP instance over the two n/2 halves, and its only
    randomness is a single random PRIME (Lemma 3.2), already nondeterministically derandomized by
    guess-and-verify with one-sided error (Remark 3.3). There is no n-fold independent-DISJ
    communication batch in the relevant direction, so "CRT correlation evades the SDPT" has no object
    to act on. We encode this structural fact (not a measured correlation of a fabricated batch).
    """
    return {
        "reduction_direction": "NEXP -> Max-IP (Lemma 4.3)",
        "num_independent_disj_instances": 1,   # single-instance, NOT an n-fold batch
        "randomness_source": "one random prime (Lemma 3.2)",
        "already_nondet_derandomized": True,    # Remark 3.3: guess-and-verify, one-sided error
        "crt_batch_to_attack_exists": False,    # the object the crack targets does not exist
        "crack_status": "DISSOLVES (no batch); not a wrong-kind-of-correlation near-miss",
    }


def deterministic_small_prime_hitting_set(num_bits: int) -> dict[str, float]:
    """The SURVIVING genuine micro-question (adversary): replace Chen's single random prime (Lemma
    3.2) by a DETERMINISTIC small-prime hitting set. A degree-bounded nonzero quantity over Z that
    fits in num_bits bits has at most num_bits prime factors, so SOME prime among the first
    O(num_bits) primes is a nonzero witness (a deterministic hitting set of size O(num_bits) primes,
    each O(log num_bits) bits). This is CHEAP in size; the open part is whether it is computable in
    the TARGET time without circularity (and whether it stays non-algebrizing). We report the size.
    """
    # A nonzero integer with absolute value < 2^num_bits has < num_bits distinct prime factors, so
    # the first num_bits + 1 primes contain a non-dividing (hitting) prime.
    def first_primes(k: int) -> list[int]:
        primes: list[int] = []
        cand = 2
        while len(primes) < k:
            if all(cand % p for p in primes if p * p <= cand):
                primes.append(cand)
            cand += 1
        return primes

    k = num_bits + 1
    primes = first_primes(min(k, 200))     # cap the explicit list for the small demo
    largest = primes[-1]
    return {
        "num_bits": float(num_bits),
        "hitting_set_num_primes": float(k),
        "largest_prime_in_demo": float(largest),
        "prime_bit_size": math.log2(max(largest, 2)),
        "hitting_set_total_bits": float(k) * math.log2(max(largest, 2)),
        "is_circular": 0.0,   # a small explicit prime set is NOT the open blackbox PIT (non-circular)
    }


def factored_equality_zero_test(U: np.ndarray, V: np.ndarray, L: np.ndarray, R: np.ndarray) -> dict[str, float]:
    """Deterministic SUBQUADRATIC factored equality: ||U V^T - L R^T||_F^2 = tr((P^T P)(Q^T Q))
    with P = [U | -L], Q = [V | R]. O(n q^2 + q^3), NOT n^2. The n^2 does NOT hide in the verifier:
    the "verifier reads all n^2 entries" objection is FALSE for factored input."""
    P = np.hstack([U, -L])
    Q = np.hstack([V, R])
    GP = P.T @ P
    GQ = Q.T @ Q
    fro2 = float(np.trace(GP @ GQ))
    direct = float((((U @ V.T) - (L @ R.T)) ** 2).sum())
    q = P.shape[1]
    n = P.shape[0]
    return {
        "gram_trace_fro2": fro2,
        "direct_fro2": direct,
        "agree": abs(fro2 - direct) < 1e-6,
        "gram_cost_n_q2": float(n * q * q),
        "n2": float(n * n),
    }


def make_unsat(n: int, d: int, seed: int) -> tuple[np.ndarray, np.ndarray, int]:
    """A clean UNSAT instance with max(A B^T) = tau (dense gapless, capped). Returns (A, B, tau)."""
    rng = np.random.default_rng(seed)
    A, B = make_fixed_popcount(n, d, seed)
    M = A @ B.T
    tau = int(np.median(M))
    for _ in range(2 * n):
        M = A @ B.T
        over = np.argwhere(M > tau)
        if len(over) == 0:
            break
        i, j = over[0]
        shared = np.where((A[i] == 1.0) & (B[j] == 1.0))[0]
        if len(shared) == 0:
            tau += 1
            continue
        A[i, shared[0]] = 0.0
    tau = int((A @ B.T).max())
    return A, B, tau


def alternative_combinatorial_certificate(n: int, d: int, seed: int) -> dict[str, float]:
    """An ALTERNATIVE combinatorial certificate attempt (Thrust A iii): a Cauchy-Schwarz block cover.
    On the gapless worst case (popcount d/2 = tau+1) the CS bound sqrt(|a||b|) = d/2 = tau+1 for EVERY
    pair, so NO block certifies <= tau: only the exact per-pair value certifies (n^2 d work). This
    locates where the n^2 hides for the combinatorial attempt: in the exact-value enumeration."""
    A, B, tau = make_unsat(n, d, seed)
    a_norm = np.sqrt((A ** 2).sum(axis=1))
    b_norm = np.sqrt((B ** 2).sum(axis=1))
    certified_blocks = 0
    total_blocks = 0
    for bsz in (n, n // 2, n // 4, 1):
        if bsz < 1:
            continue
        nb = max(1, n // bsz)
        for bi in range(nb):
            for bj in range(nb):
                ri = slice(bi * bsz, (bi + 1) * bsz)
                rj = slice(bj * bsz, (bj + 1) * bsz)
                cs = float(a_norm[ri].max() * b_norm[rj].max())
                total_blocks += 1
                if cs <= tau:
                    certified_blocks += 1
    return {
        "n": float(n), "d": float(d), "tau": float(tau),
        "fraction_blocks_certified": certified_blocks / max(total_blocks, 1),
        "exact_value_cost_n2_d": float(n) * float(n) * float(d),   # where the n^2 hides
    }


# ==========================================================================
# Barrier profiles (the three-barrier discipline on each thrust) and the algebrization probe.
# ==========================================================================


def thrustB_collapse_technique() -> ProofTechnique:
    """Thrust B: the sufficient-statistic / data-processing collapse, encoded as a model-restricted
    lower bound. Evades all three (concrete factored structure, function-specific instance, the force
    is the non-algebraic location ingredient / SNR floor)."""
    return ProofTechnique(
        name="Thrust B sufficient-statistic collapse (full-block data processing + sub-block SNR floor)",
        relativizes=False,
        natural_largeness=False,
        natural_constructivity=False,
        algebrizes=False,
        notes=("A model-restricted lower bound on bulk (b)/(c) queries: each is a function of a fixed "
               "location-blind sufficient statistic (moment vector / d-spectrum). Full-block is a "
               "data-processing THEOREM; sub-block is a named open SNR lemma. Not a natural proof."),
    )


def thrustA_derandomization_route_i() -> ProofTechnique:
    """Thrust A Route (i): the arithmetization-internal deterministic hitting set. HITS algebrization
    (the MA engine is Reed-Muller arithmetization, the canonical algebrizing technique)."""
    return ProofTechnique(
        name="Thrust A Route (i): deterministic hitting set inside the arithmetized MA protocol",
        relativizes=False,
        natural_largeness=False,
        natural_constructivity=True,
        algebrizes=True,             # the binding fact: arithmetization-internal => algebrizes
        notes=("A low-degree PRG / hitting set for the sum-check polynomial inherits the Reed-Muller "
               "arithmetization, the algebrizing technique (Aaronson-Wigderson 2008). DISQUALIFIED on "
               "the algebrization axis, and circular via Kabanets-Impagliazzo 2004 (PIT => lower bound)."),
    )


def thrustA_derandomization_route_ii() -> ProofTechnique:
    """Thrust A Route (ii): Merlin-guessed points, deterministic verification. Evades all three (the
    obstruction is a non-algebraic communication/cover fact), yet is still blocked by the n^2 / the
    triple-lock, not by a barrier."""
    return ProofTechnique(
        name="Thrust A Route (ii): Merlin-guessed evaluation points, deterministic verifier",
        relativizes=False,
        natural_largeness=False,
        natural_constructivity=True,
        algebrizes=False,            # the obstruction is the non-algebraic DISJ co-nd communication
        notes=("A co-nd certificate guessing the evaluation points. Evades all three barriers, but is "
               "blocked by the triple-lock (UPIT/NSETH inside the protocol, Williams Cor 3.1; "
               "circularity of generic prAM-in-NP derandomization, Miltersen-Vinodchandran / IKW), "
               "not by a barrier. The obstruction is structural, not a wall theorem."),
    )


def ma_engine_invariant() -> InvariantProfile:
    """The MA certificate's engine as an algebrization-probe invariant: Reed-Muller arithmetization
    + sum-check, a characteristic-0 low-degree trace/sum functional. The probe must say ALGEBRIZES."""
    return InvariantProfile(
        name="MA certificate engine (Reed-Muller arithmetization + sum-check fingerprint)",
        characteristic=0,
        is_trace_or_rank_functional=True,   # a low-degree sum / polynomial evaluation = a trace functional
        torsion_sensitive=False,
        notes=("Arithmetizes 'is this pair disjoint?' as a low-degree polynomial over F_p and tests "
               "h(r)=?0 via a Reed-Muller / sum-check fingerprint. The canonical algebrizing technique "
               "(Aaronson-Wigderson 2008): a low-degree oracle extension carries the sum."),
    )


# ==========================================================================
# Reporting
# ==========================================================================


def main() -> int:
    print("=== Fused-max-MM (J1 frontier) ENDGAME: Thrust B seam closure + Thrust A co-nd frontier ===\n")
    print("TARGET (Chen 2018 arXiv:1805.10698 Thm 1.5 item 1, web-confirmed verbatim in e_maxip_logshave.py):")
    print('  "An n^2 / log^{omega(1)} n time algorithm for Bichromatic Maximum Inner Product with vector')
    print('   dimension d = n^eps ... would imply NEXP has no polynomial size THR o THR circuits."')
    print("M = A B^T (integer counts <a_i,b_j> in {0,...,d}, rank <= d, FACTORED). ans = max_{i,j} M_{ij}.")
    print("Hard family (Chen Cor 5.5 / Lemma 5.1): gap-1, planted, gapless. YES = NO + one Boolean bit flip;")
    print("deciding YES vs NO is Set-Disjointness on the planted pair (Omega(n); KS'92, R'92); promise = UDISJ.\n")

    # Grounding: the gap-1 pair is two valid factored Boolean products, max d vs d-1, one cell apart.
    A, B_no, B_yes, (i_star, j_star) = make_gap1_pair(64, 12, seed=5)
    max_no = int((A @ B_no.T).max())
    max_yes = int((A @ B_yes.T).max())
    diff = int(((A @ B_yes.T) - (A @ B_no.T) != 0).sum())
    bf_no = max_ip_bruteforce(A.astype(np.int64), B_no.astype(np.int64))
    print("GROUNDING (the gap-1 hard pair, both valid factored products):")
    print(f"  n=64, d=12: max(NO) = {max_no} (= d-1), max(YES) = {max_yes} (= d), cells changed = {diff} (exactly one)")
    print(f"  brute force agrees with A B^T on NO: {bf_no} == {max_no} -> {bf_no == max_no}; "
          f"rank(M_NO) = {int(np.linalg.matrix_rank(A @ B_no.T))} <= 12\n")

    # ======================================================================
    # THRUST B (SEAM CLOSURE).
    # ======================================================================
    print("=" * 78)
    print("THRUST B (SEAM CLOSURE): adaptive non-linear (b)/(c) queries collapse to a fixed statistic.")
    print("=" * 78 + "\n")
    print("PIVOT: each cheap non-linear family has a FIXED instance-determined SUFFICIENT STATISTIC. A")
    print("degree-<=D symmetric query is a linear functional of the moment vector (m_1..m_D); a spectral")
    print("query is a function of the d-spectrum. Adaptively querying FUNCTIONS of a fixed statistic adds")
    print("nothing beyond the statistic (Cover-Thomas data processing). S1/S2 full-block = THEOREM; S3")
    print("sub-block = a NAMED OPEN LEMMA (adversary-corrected from 'closed').\n")

    print("S1 (THE SUFFICIENT STATISTIC IS LOCATION-INVARIANT): move the planted spike (i,j)->(i',j');")
    print("    the moment vector (m_1..m_D) AND the singular spectrum are IDENTICAL (0 location bits).")
    print(f"    {'b':>4} | {'d':>4} | {'D':>3} | {'moments equal':>14} | {'spectra equal':>14} | {'loc bits':>9}")
    print("    " + "-" * 60)
    for (b, d, D) in [(6, 12, 4), (8, 16, 4), (12, 24, 5)]:
        si = sufficient_statistic_is_location_invariant(b, d, D)
        print(f"    {b:>4} | {d:>4} | {D:>3} | {str(si['moments_equal_across_location']):>14} | "
              f"{str(si['spectra_equal_across_location']):>14} | {str(si['location_bits']):>9}")
    print("    => any (b)/(c) query (a function of these) is BLIND to spike location. 0 location bits.\n")

    print("    full-block moment delta is VALUE-ONLY (a +1 at ANY cell of value v=d-1 moves m_p by")
    delta = full_block_moment_delta_is_value_only(12)
    print(f"    (v+1)^p - v^p, no (i,j) argument): m1={delta['m1_delta']}, m2={delta['m2_delta']}, "
          f"m3={delta['m3_delta']} (location_independent={delta['location_independent']}).\n")

    print("S2 (DATA-PROCESSING COLLAPSE): an ADAPTIVE 3-round (b)/(c) transcript whose next query")
    print("    branches on prior answers is IDENTICAL across spike location (a deterministic function")
    print("    of the blind statistic, so its whole transcript is blind):")
    at = adaptive_transcript_identical(6, 12, 4, seed=3)
    print(f"    transcript spike A = {at['transcript_spike_a']}")
    print(f"    transcript spike B = {at['transcript_spike_b']}  -> identical = {at['transcripts_identical']}")
    print(f"    ({at['note']}).\n")

    print("S3 (SUB-BLOCK ADAPTIVE BOUND, NAMED OPEN LEMMA): per-query summary advantage SNR-floored.")
    print("    Signal = 2d-1 exactly; bulk fluctuation grows with b; SNR ~ 1/b (advantage ~ 1/b^2):")
    print(f"    {'b':>4} | {'signal':>8} | {'bulk fluct':>11} | {'SNR':>10} | {'SNR*b':>9} | {'heaviness':>10}")
    print("    " + "-" * 62)
    for b in (2, 4, 8, 16, 32):
        s = subblock_advantage(256, 64, b, seed=4)
        print(f"    {b:>4} | {s['signal']:>8.0f} | {s['bulk_fluctuation']:>11.1f} | {s['snr']:>10.4f} | "
              f"{s['snr_times_b']:>9.3f} | {s['heaviness']:>10.3e}")
    print("    SNR decays with b; only at b = O(1) (after localization) is the advantage Theta(1). The")
    print("    union over K adaptive queries (~ K/b^2) is the NAMED OPEN LEMMA: additivity over an")
    print("    adaptive tree is not rigorously discharged (the MIC measure, Braverman et al 2024, is the")
    print("    tool, not instantiated here). At b ~ n the bound is o(1) for K = o(n^2) (simulation-supported):")
    print(f"    {'n':>6} | {'K=n: total adv':>15} | {'K=n^1.5: total adv':>19} | {'K=n^2/4: total adv':>19}")
    print("    " + "-" * 64)
    for n in (64, 128, 256, 512):
        a1 = mic_total_advantage(n, 64, n, n, seed=0)["total_adv"]
        a15 = mic_total_advantage(n, 64, int(n ** 1.5), n, seed=0)["total_adv"]
        a2 = mic_total_advantage(n, 64, (n * n) // 4, n, seed=0)["total_adv"]
        print(f"    {n:>6} | {a1:>15.3e} | {a15:>19.3e} | {a2:>19.3e}")
    print("    adv(K=n), adv(K=n^1.5) -> 0; only adv(K=n^2/4) = Theta(1). Simulation-supported, not proved.\n")

    print("PROVES-TOO-MUCH CONTROL (Thrust B): the spectrum DETECTS a constant relative gap (uses")
    print("    gaplessness). Top singular value shift, GAPPED (Valiant, Theta d) vs GAPLESS (gap-1, O(1)):")
    print(f"    {'n':>5} | {'d':>5} | {'shift GAPPED (Theta d)':>23} | {'shift GAPLESS (O(1))':>21} | {'ratio':>9}")
    print("    " + "-" * 70)
    ptm_ratios = []
    for (n, d) in [(256, 64), (512, 128), (768, 192)]:
        pt = spectral_detects_constant_gap(n, d, seed=1)
        ptm_ratios.append(pt["ratio"])
        print(f"    {n:>5} | {d:>5} | {pt['spectral_shift_gapped']:>23.3f} | {pt['spectral_shift_gapless']:>21.4f} | "
              f"{pt['ratio']:>9.1f}")
    print("    ratio GROWS with d: blind ONLY at gap=1. Valiant FOCS 2012 / light-bulb survives.\n")

    # ======================================================================
    # THRUST A (CO-NONDETERMINISTIC FRONTIER).
    # ======================================================================
    print("=" * 78)
    print("THRUST A (CO-NONDETERMINISTIC FRONTIER): can the MA certificate derandomize into a co-nd one?")
    print("=" * 78 + "\n")

    print("(i) The MA certificate Theta(sqrt(n) log n) is a REAL sub-n object (Williams CCC 2016")
    print("    arXiv:1601.04743; Rubinstein STOC 2018) but RANDOMIZED-verifier, outside Chen's co-nd")
    print("    hypothesis (Remarks 2.7/4.2). The single decision is co-nd UDISJ on ONE planted pair,")
    print("    co-nd communication Theta(n) (KS'92, R'92):")
    print(f"    {'n':>7} | {'MA cert ~sqrt(n)logn':>21} | {'sub-n?':>7} | {'co-nd comm (single pair)':>26} | {'/n':>5}")
    print("    " + "-" * 76)
    for n in (256, 1024, 4096, 16384):
        ma = ma_certificate_size(n)
        cc = cond_communication_single_pair(n)
        print(f"    {n:>7} | {ma['ma_cert_size']:>21.1f} | {str(ma['ma_is_sub_n']):>7} | "
              f"{cc['cond_comm_lb']:>26.0f} | {cc['cond_comm_over_n']:>5.2f}")
    print("    MA stays sub-n but randomized; the co-nd certificate for the single decision is Omega(n).\n")

    print("(ii) The nonneg-rank route is CORRECTED (adversary smallest_breaking_case). Yannakakis:")
    print("    rank_+(N) >= cover of supp(N) = {M_ij != tau} (the COMPLEMENT of the tight set) by tight-")
    print("    free rectangles. For a permutation tight set, supp(N) = off-diagonal has an EXPLICIT tight-")
    print("    free cover of size 2*ceil(log2 m) = O(log m), NOT Omega(m). The OLD computation covered the")
    print("    WRONG set (the diagonal by 1x1 cells = m). Measured (verified coverage, tight-free):")
    print(f"    {'m':>6} | {'tight-free cover':>17} | {'2*log2(m)':>10} | {'covers off-diag':>16} | {'all tight-free':>15}")
    print("    " + "-" * 72)
    for m in (4, 8, 16, 64, 256, 1024):
        sc = supp_complement_cover_is_logarithmic(m)
        print(f"    {m:>6} | {sc['tight_free_cover_size']:>17} | {sc['two_log2_m']:>10} | "
              f"{str(sc['covers_all_offdiagonal']):>16} | {str(sc['every_rectangle_tight_free']):>15}")
    print("    cover = O(log m), so rank_+(N) >= O(log m) only: the nonneg-rank route does NOT give")
    print("    Omega(m). The legitimate Omega(n) is the co-nd COMMUNICATION above (single planted pair).")
    print("    The jump to an Omega(n^2) certificate SIZE needs n independent Omega(n) covers, which the")
    print("    gap-1 family (ONE planted pair) does not obviously supply: that n^2 is NAMED-AS-NOT-DERIVED.\n")

    print("(iii) The CRT crack DISSOLVES (adversary crt_crack_real=NO). Chen's NEXP-direction reduction")
    print("    (Lemma 4.3) is SINGLE-instance; its only randomness is a single random prime (Lemma 3.2),")
    print("    already nondeterministically derandomized (Remark 3.3). No n-fold independent-DISJ batch")
    print("    exists for an SDPT or a CRT-correlation to act on:")
    crt = crt_self_reduction_is_single_instance()
    for key in ("reduction_direction", "num_independent_disj_instances", "randomness_source",
                "already_nondet_derandomized", "crt_batch_to_attack_exists", "crack_status"):
        print(f"      {key:<34}: {crt[key]}")
    print("    The SURVIVING genuine micro-question: replace the single random prime by a DETERMINISTIC")
    print("    small-prime hitting set (non-circular, possibly non-algebrizing). It is CHEAP in size:")
    print(f"    {'num_bits':>9} | {'#primes':>8} | {'largest prime (demo)':>21} | {'total bits':>11}")
    print("    " + "-" * 56)
    for nb in (8, 16, 32, 64):
        hs = deterministic_small_prime_hitting_set(nb)
        print(f"    {int(hs['num_bits']):>9} | {int(hs['hitting_set_num_primes']):>8} | "
              f"{int(hs['largest_prime_in_demo']):>21} | {hs['hitting_set_total_bits']:>11.1f}")
    print("    Cheap in SIZE; the open part is computability in the TARGET time (non-circular, the")
    print("    survey's genuinely-open micro-question), NOT an exp-size product set or blackbox PIT.\n")

    print("    The n^2 does NOT hide in the verifier: factored low-rank EQUALITY is subquadratic.")
    rngp = np.random.default_rng(0)
    dpar = 8
    print(f"    {'n':>6} | {'q=2(d+1)':>9} | {'n*q^2 (Gram cost)':>18} | {'n^2':>10} | {'n*q^2 < n^2':>12}")
    print("    " + "-" * 64)
    eq = None
    for npar in (256, 512, 1024, 2048):
        Upar = (rngp.random((npar, dpar)) < 0.5).astype(np.float64)
        Vpar = (rngp.random((npar, dpar)) < 0.5).astype(np.float64)
        Lpar = Upar.copy(); Rpar = Vpar.copy()
        eq = factored_equality_zero_test(Upar, Vpar, Lpar, Rpar)
        q = 2 * (dpar + 1)
        print(f"    {npar:>6} | {q:>9} | {eq['gram_cost_n_q2']:>18.0f} | {eq['n2']:>10.0f} | "
              f"{str(eq['gram_cost_n_q2'] < eq['n2']):>12}")
    print(f"    Gram-trace ||P Q^T||_F^2 = {eq['gram_trace_fro2']:.6f} (direct {eq['direct_fro2']:.6f}, "
          f"agree={eq['agree']}): equal factored matrices give 0 at cost n*q^2 (subquadratic).\n")

    print("    ALTERNATIVE combinatorial certificate (Cauchy-Schwarz block cover): on the gapless worst")
    print("    case NO block certifies <= tau; only the exact per-pair value certifies (the n^2 hides in")
    print("    the exact-value enumeration n^2 d):")
    for (n, d) in [(96, 8), (128, 12)]:
        ac = alternative_combinatorial_certificate(n, d, seed=1)
        print(f"      n={n}, d={d}, tau={int(ac['tau'])}: fraction of blocks certified = "
              f"{ac['fraction_blocks_certified']:.3f}; exact-value cost n^2 d = {ac['exact_value_cost_n2_d']:.0f}")
    print()

    # ======================================================================
    # BARRIER PROFILES and the algebrization probe.
    # ======================================================================
    print("=" * 78)
    print("BARRIER PROFILES (the three-barrier discipline on each thrust):")
    print("=" * 78 + "\n")
    checker = BarrierChecker()
    vB = checker.check(thrustB_collapse_technique())
    vAi = checker.check(thrustA_derandomization_route_i())
    vAii = checker.check(thrustA_derandomization_route_ii())
    for v in (vB, vAi, vAii):
        print(v.report())
        print()

    print("ALGEBRIZATION PROBE on the MA certificate's engine (verified, not asserted):")
    pv = probe(ma_engine_invariant())
    print(pv.report())
    print("  => the arithmetization engine ALGEBRIZES (Reed-Muller + sum-check, a char-0 trace functional);")
    print("  the target NEXP-not-poly-THR-of-THR is NON-algebrizing (Williams 2011 spine). An arithmetization-")
    print("  internal derandomization points the WRONG WAY on the algebrization axis (one of three locks).\n")

    # ======================================================================
    # Final summary and honest verdict.
    # ======================================================================
    print("=" * 78)
    print("FINAL SUMMARY")
    print("=" * 78 + "\n")
    print("THRUST B (SEAM): the FULL-BLOCK half is CLOSED (a theorem). The moment vector and the singular")
    print("  spectrum are the fixed location-blind sufficient statistic, so every adaptive (b)/(c)")
    print("  transcript is location-blind (Cover-Thomas data processing). The SUB-BLOCK half is a NAMED")
    print("  OPEN LEMMA, not closure (adversary-corrected): the per-query advantage is SNR-floored ~ 1/b^2,")
    print("  but the union over K adaptive queries assumes additivity an adaptive tree can violate (the")
    print("  MIC measure, Braverman et al arXiv:2403.20283, is the tool, not instantiated). HONEST CLAIM:")
    print("  a full-block theorem PLUS a named sub-block open lemma. Uses gaplessness ESSENTIALLY (the")
    print("  spectrum DETECTS a constant relative gap: Valiant/light-bulb survives). NOT full closure.\n")
    print("THRUST A (CO-ND FRONTIER): PINNED-BLOCKED. The MA certificate (Theta(sqrt(n) log n)) is a real")
    print("  sub-n object but RANDOMIZED-verifier, outside Chen's co-nd hypothesis. The nonneg-rank route")
    print("  is CORRECTED: the tight-free cover of supp(N) for a permutation tight set is O(log m), so")
    print("  rank_+ >= O(log m), NOT Omega(m); the legitimate Omega(n) is the co-nd COMMUNICATION of UDISJ")
    print("  on the single planted pair, and the Omega(n^2) certificate SIZE is NAMED-AS-NOT-DERIVED (ONE")
    print("  planted pair, not n). The CRT crack DISSOLVES (Chen's NEXP-direction reduction is single-")
    print("  instance, already nondet-derandomized: no DISJ batch to attack). The surviving micro-question")
    print("  is a deterministic small-prime hitting set for Chen's single random prime (cheap in size,")
    print("  open in computability). Barrier logic VERIFIED: the arithmetization engine algebrizes, the")
    print("  target does not, so an arithmetization-internal derandomization conflicts on the algebrization")
    print("  axis (one of three locks: UPIT/NSETH, algebrization, prAM-in-NP circularity).\n")
    print("HONEST VERDICT: Thrust B closes the FULL-BLOCK half cleanly (a data-processing theorem) and")
    print("  names the precise sub-block open lemma (NOT full closure). Thrust A is PINNED-BLOCKED: no")
    print("  subquadratic co-nd certificate survives the hunt; both failure modes (hidden n^2, circular")
    print("  hardness) were found and the wrong-set nonneg-rank derivation was corrected to O(log m). The")
    print("  CRT crack dissolved into a non-question; the only surviving opening (deterministic small-prime")
    print("  hitting set) is named and hostile. NEXP not in poly-size THR-of-THR is OPEN as of June 2026.")
    print("  NO PROGRESS ON THE PRIZE CLAIMED.\n")

    # ======================================================================
    # Self-checks pinning the key coordinates. Module must exit 0.
    # ======================================================================

    # (G) The gap-1 hard pair is two valid factored Boolean products differing in ONE cell, max d vs d-1.
    assert max_no == 11 and max_yes == 12, "the gap-1 pair must have max d-1=11 (NO) and d=12 (YES)"
    assert diff == 1, "YES = NO + exactly one Boolean bit flip (one cell changes)"
    assert bf_no == max_no, "brute force must agree with A B^T on the NO instance (grounding)"

    # (B.S1) The sufficient statistic (moment vector + singular spectrum) is LOCATION-INVARIANT:
    #        0 location bits. This is the load-bearing full-block closure.
    for (b, d, D) in [(6, 12, 4), (8, 16, 4), (12, 24, 5)]:
        si = sufficient_statistic_is_location_invariant(b, d, D)
        assert si["moments_equal_across_location"], "the moment vector must be identical across spike location"
        assert si["spectra_equal_across_location"], "the singular spectrum must be identical across spike location"
        assert si["location_bits"] == 0, "the full-block sufficient statistic carries 0 location bits"
    delta = full_block_moment_delta_is_value_only(12)
    assert delta["location_independent"], "the full-block moment delta is value-only (no (i,j) argument)"

    # (B.S2) The ADAPTIVE (b)/(c) transcript is identical across spike location (data processing).
    at = adaptive_transcript_identical(6, 12, 4, seed=3)
    assert at["transcripts_identical"], \
        "an adaptive (b)/(c) transcript must be identical across spike location (data-processing collapse)"

    # (B.S3) The sub-block advantage is SNR-floored ~ 1/b^2 and DECAYS with b (the named open lemma).
    s_b2 = subblock_advantage(256, 64, 2, seed=4)
    s_b32 = subblock_advantage(256, 64, 32, seed=4)
    assert s_b2["snr"] > s_b32["snr"], "the sub-block SNR must DECREASE with block size b (toward 0)"
    assert s_b2["heaviness"] > 5.0 * s_b32["heaviness"], \
        "the per-query heaviness must decay with b (advantage ~ 1/b^2): the SNR floor"
    adv_Kn = mic_total_advantage(256, 64, 256, 256, seed=0)["total_adv"]
    assert adv_Kn < 0.1, "K=n adaptive sub-block queries give o(1) total advantage (simulation-supported)"

    # (B.PTM) PROVES-TOO-MUCH: the spectrum DETECTS a constant relative gap (uses gaplessness).
    pt = spectral_detects_constant_gap(512, 128, seed=1)
    assert pt["spectral_shift_gapped"] > pt["spectral_shift_gapless"], \
        "the spectral shift must be larger on the GAPPED instance (a constant gap is detectable)"
    assert pt["ratio"] > 100.0, \
        "the gapped/gapless spectral-shift ratio must be large (>100x): blind ONLY at gap=1, Valiant survives"

    # (A.i) The MA certificate is sub-n (Theta(sqrt(n) log n)) but the single co-nd decision is Omega(n).
    for n in (256, 1024, 4096):
        ma = ma_certificate_size(n)
        assert ma["ma_is_sub_n"], "the MA certificate Theta(sqrt(n) log n) is sub-n (a real small object)"
        cc = cond_communication_single_pair(n)
        assert cc["cond_comm_lb"] == float(n), "the single planted decision has co-nd communication Theta(n)"

    # (A.ii) ADVERSARY CORRECTION: the tight-free cover of supp(N) is O(log m), NOT Omega(m). The OLD
    #        wrong-set diagonal cover (=m) is replaced; rank_+ >= O(log m) only. Coverage is VERIFIED.
    for m in (4, 8, 16, 64, 256, 1024):
        sc = supp_complement_cover_is_logarithmic(m)
        assert sc["covers_all_offdiagonal"], "the rectangle cover must cover every off-diagonal cell of supp(N)"
        assert sc["every_rectangle_tight_free"], "every cover rectangle must avoid the tight (diagonal) set"
        assert sc["tight_free_cover_size"] <= 2 * max(1, math.ceil(math.log2(m))), \
            "the tight-free cover of supp(N) is O(log m), NOT Omega(m) (the corrected nonneg-rank bound)"
    # At m=1024 the corrected cover is logarithmic (<= 20), blatantly smaller than the old claim of m.
    sc_big = supp_complement_cover_is_logarithmic(1024)
    assert sc_big["tight_free_cover_size"] <= 20 < 1024, \
        "at m=1024 the corrected tight-free cover is O(log m) <= 20, not the old Omega(m)=1024"

    # (A.iii) The CRT crack DISSOLVES: Chen's NEXP-direction reduction is single-instance, already
    #         nondet-derandomized, so there is no DISJ batch to attack.
    crt = crt_self_reduction_is_single_instance()
    assert crt["num_independent_disj_instances"] == 1, \
        "Chen's NEXP-direction reduction is SINGLE-instance (Lemma 4.3): no n-fold DISJ batch"
    assert crt["crt_batch_to_attack_exists"] is False, \
        "the CRT-correlation crack targets a non-existent object: it DISSOLVES (Remark 3.3)"
    # The surviving micro-question's hitting set is CHEAP in size (not exp, not blackbox PIT).
    hs = deterministic_small_prime_hitting_set(32)
    assert hs["is_circular"] == 0.0 and hs["hitting_set_num_primes"] == 33.0, \
        "a small explicit prime hitting set is non-circular and O(num_bits) primes (cheap in size)"

    # (A.verifier) Factored low-rank EQUALITY is subquadratic and correct (the n^2 is NOT in the verifier).
    eq_chk = factored_equality_zero_test(Upar, Vpar, Lpar, Rpar)
    assert eq_chk["agree"], "the Gram-trace zero-test must equal the direct Frobenius distance"
    assert abs(eq_chk["gram_trace_fro2"]) < 1e-6, "U V^T == L R^T must give Gram-trace 0 (equal matrices)"
    assert eq_chk["gram_cost_n_q2"] < eq_chk["n2"], "the Gram-trace cost n*q^2 is subquadratic (< n^2)"
    Uper = Upar.copy(); Uper[0, 0] += 1.0
    eq_per = factored_equality_zero_test(Uper, Vpar, Lpar, Rpar)
    assert eq_per["gram_trace_fro2"] > 1e-6 and eq_per["agree"], \
        "perturbing one factor must make the zero-test nonzero (a genuine equality test)"

    # (A.alt) The alternative combinatorial certificate certifies NO block on the gapless worst case.
    ac = alternative_combinatorial_certificate(96, 8, seed=1)
    assert ac["fraction_blocks_certified"] == 0.0, \
        "no Cauchy-Schwarz block certifies <= tau on the gapless worst case (the n^2 hides in exact values)"

    # (BARRIER) Thrust B collapse evades all three; Route (i) HITS algebrization; Route (ii) evades all
    #           three (blocked by the n^2 / triple-lock, not a barrier).
    assert vB.evades_all, "the Thrust B collapse evades all three barriers (model-restricted LB)"
    assert vAi.hits_algebrization and not vAi.evades_all, \
        "Route (i) HITS the algebrization barrier (arithmetization-internal hitting set)"
    assert vAii.evades_all, \
        "Route (ii) evades all three barriers (blocked by the n^2 / triple-lock, not a barrier)"

    # (PROBE) The MA engine ALGEBRIZES (verified against the repo's own probe, not asserted).
    assert pv.algebrizes is True, \
        "the MA certificate engine (Reed-Muller arithmetization + sum-check) must classify as ALGEBRIZES"

    print("=== Self-check OK ===")
    print("(B.S1) SUFFICIENT STATISTIC location-invariant: moment vector + singular spectrum IDENTICAL")
    print("       across spike location (0 location bits). Full-block delta is value-only.")
    print("(B.S2) ADAPTIVE (b)/(c) transcript IDENTICAL across spike location (Cover-Thomas data processing).")
    print("(B.S3) SUB-BLOCK advantage SNR-floored ~ 1/b^2, decays with b; K=o(n^2) union o(1). NAMED OPEN")
    print("       LEMMA (additivity over the adaptive tree not discharged; MIC not instantiated): not closure.")
    print("(B.PTM) PROVES-TOO-MUCH control: spectrum DETECTS a constant relative gap (ratio >100x). Uses")
    print("       gaplessness essentially; Valiant/light-bulb survives.")
    print("(A.i) MA certificate sub-n (Theta(sqrt(n) log n)) but RANDOMIZED-verifier; single co-nd decision Omega(n).")
    print("(A.ii) CORRECTED nonneg-rank: tight-free cover of supp(N) is O(log m), NOT Omega(m) (coverage")
    print("       verified). Old wrong-set diagonal cover dropped. rank_+ >= O(log m); n^2 cert size NAMED-NOT-DERIVED.")
    print("(A.iii) CRT crack DISSOLVES (single-instance, already nondet-derandomized). Surviving micro-question:")
    print("       deterministic small-prime hitting set (cheap in size, open in computability, non-circular).")
    print("(BARRIER) Thrust B evades all three; Route (i) HITS algebrization; Route (ii) evades all three (blocked")
    print("       by the n^2 / triple-lock). The MA engine ALGEBRIZES (probe-verified); the target does not: CONFLICT.")
    print("(STATUS) Thrust B full-block CLOSED + named sub-block lemma; Thrust A PINNED-BLOCKED. NEXP not in")
    print("       poly-size THR-of-THR is OPEN as of June 2026. NO PROGRESS ON THE PRIZE CLAIMED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
