"""Two joints of the leading path, illustrated and re-judged: J1 (sub-block lemma) and J3 (locality).

This module is a NUMERIC ILLUSTRATION of the two open joints in the leading-path descent to NP
(finding 26's four-joint synthesis), with the ADVERSARY corrections applied so the math is right.
It is self-contained (a Track-1 builder scratch module was consolidated into it and removed) and
re-judges the descent ledger e_leading_path_descent.py for Track 2. A self-checking pass.

THE LEADING PATH (Williams algorithm-to-lower-bound spine + meta-complexity): NEXP / NP not in
poly-size THR-of-THR. The descent has four joints. J1 ALGORITHMIC (the fused-max-MM log-shave,
finding 33). J2 DESCENT (downstream, NP easy-witness lemma proved, Murray-Williams 2018). J3
NON-CONSTRUCTIVITY (the BINDING joint, the locality barrier, finding 34). J4 COMPOSITION (no
combining theorem). This module attacks the two open joints J1 and J3.

================================================================================================
TRACK 1 (J1, finding 33): the SUB-BLOCK NON-LINEAR PER-ROUND INFORMATION LEMMA.
================================================================================================

THE TARGET (Chen 2018, arXiv:1805.10698, Theorem 1.5 item 1, web-confirmed verbatim in the
sibling e_maxip_logshave.py): an n^2 / log^{omega(1)} n algorithm for Bichromatic Max-IP at
d = n^eps would imply NEXP has no poly-size THR-of-THR circuits. M = A B^T (n x n integer count
matrix, rank <= d, FACTORED). The hard family is gap-1, planted, gapless (Chen Cor 5.5 / Lemma
5.1): YES = NO + one Boolean bit flip, max d vs d-1, every other inner product <= d-1 in BOTH.

  CONJECTURE (the lemma). An adaptive K-round decision tree whose nodes are cheap non-linear
  summaries (degree-<1/eps entry-symmetric MOMENTS, or rotation-invariant SPECTRAL functions) of
  ADAPTIVELY-CHOSEN sub-blocks of M cannot decide gap-1 (max=d vs <=d-1) on the planted gapless
  family for K = o(n^2). Finding 31 closed the FULL-block case (0 location bits, data processing);
  the open case is a tree that chooses which PROPER sub-block to summarize next.

ADVERSARY VERDICT APPLIED (this module's correction to the prong). The prong reported "lemma-
partial" via two routes. The adversary found the closing route FATALLY FLAWED. This module
reproduces the adversary's smallest breaking case with MEASURED numbers and reports the corrected
status: the Track-1 lemma is GENUINELY OPEN, not partial.

  ROUTE (a) (port Simchowitz Obs 3.1 / Kacham-Woodruff orthogonalize-WLOG deflation to non-linear
    reads). VERDICT: NO PORT for non-additive SPECTRAL reads, but the prong OVERSTATED it for
    MOMENTS. Degree-2 entry-symmetric moments are EXACTLY additive over a tiling (a b x b block
    moment is the sum of its 4 sub-quadrant moments, residual 0 verified), so a tiling-based
    deflation DOES exist for the moment family (one of the two in-scope cheap families). The
    no-port claim is sound ONLY for the non-additive spectral reads. Measured both.

  ROUTE (b) (the location-information telescope). VERDICT: the closing argument FAILS. The prong's
    load-bearing law "per-round location info ~ C b^2/n^2 with C ~ 4.5" was a measurement artifact
    of an INCONSISTENT signal model: per_round_snr used the FAITHFUL gap-1 increment (a cell goes
    d-1 -> d, signal 2d-1), but per_round_location_info upgraded a bulk cell of value ~d/4 to a
    Theta(d^2) OUTLIER (bm = bm - M[si,sj]^2 + d^2). The C ~ 4.5 law holds ONLY for that Theta(d^2)
    outlier. Under the faithful 2d-1 increment, I/f COLLAPSES with b (measured 2.33, 0.79, 0.19,
    0.029, 0.009 at b=2,4,8,16,32; n=128 d=64, 3-seed avg), tracking the binned-MI estimator NULL
    FLOOR (~4-7e-4 bits, the (nbins-1)/(2N ln2) bias). So the per-round info that actually matters
    was never reliably measured, the telescope loses its premise, and the wall is gone.
    SECONDARY FLAW: the telescope bounds LOCALIZATION (2 log n bits via Fano), but the task is a
    1-bit DETECTION (max=d vs <=d-1). Detection != localization; a global statistic can decide
    without localizing, so even an airtight telescope bounds a strictly harder problem.

  WHAT SURVIVES (the genuine peripheral coordinates, all measured here):
    - The per-round SNR LAW: SNR of a degree-2 block moment as a spike-membership test (faithful
      2d-1 signal) is Theta(1/(b sqrt(d))); measured SNR*b*sqrt(d) ~ 15-16, constant across
      d in {16,64,256}, b in {1,2,8}. A proper sub-block is sub-SNR at gap 1.
    - The greedy quadrant descent (the cheapest adaptive tree, O(log n) reads) FAILS, success
      DECAYING with n (0.62 -> 0.35 -> 0.20 -> 0.05 at n=64/128/256/512). Strong evidence the
      cheap adaptive tree cannot thread the middle, but simulation, not proof.
    - The proves-too-much guard: a single spectral read DETECTS a constant relative gap (Valiant /
      light-bulb) but is blind at gap 1. The lemma is blind ONLY at gap 1.

  CORRECTED STATUS: Track-1 lemma is OPEN. It is exactly the survey's named missing object (an
  adaptive low-degree / spectral query lower bound), with no off-the-shelf machinery. NOT partial.

================================================================================================
TRACK 2 (J3, finding 34): the locality barrier, the BINDING joint of the descent.
================================================================================================

J3 wants a PROVED high-Kt / MCSP-against-TC0 lower bound (the non-constructivity the descent's
escape from natural proofs needs once largeness is cleared). Hardness magnification (HM) is the
amplifier: a barely-superlinear N^{1+eps} lower bound for an MCSP/MKtP-type problem magnifies to
the prize. The LOCALITY BARRIER (Golovnev-Ilango-Impagliazzo-Kabanets-Kolokolova-Tal, ICALP 2019,
"GIIKKT"; Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam, "Beyond Natural Proofs: Hardness
Magnification and Locality", JACM 2022 / arXiv:1911.08297, "CHOPRS") explains why no current
technique supplies even the weak HM input: the known techniques are LOCAL (they extend to small-
fan-in oracle circuits), HM unconditionally emits exactly such oracle circuits, so technique and
target provably meet inside the same class and cannot separate.

VERDICT (this module, matching the prong and the adversary): J3 is an OPEN NO-GO with no completed
candidate technique as of June 2026. This is a MAP, not a resolution. The barrier is precisely
defined, broadly covering (polynomial method, approximate degree, random restrictions, reductions
per CHOPRS, AND the approximation method per Pich 2024), and downstream of natural proofs.

ADVERSARY CORRECTIONS APPLIED:
  (1) NUMERIC: the GIIKKT MCSP cap is exp(N^{0.49/d}), NOT exp(N^{0.49/(d-1)}). The repo's own
      descent ledger (e_leading_path_descent.py) already uses 0.49/d; this module uses 0.49/d.
  (2) The "TC0 seam" is DEMOTED from "highest-value win-win probe" to "a coordinate: the open TC0
      lower-bound problem, relabeled". The GIIKKT computational cap (MAJ, NC1 in (AC0)^MCSP) is
      gate-type-AGNOSTIC and does NOT rest on the Lemma-41 degree argument, so "cap proved at
      AC0[p] but not TC0" is a mis-location; the cap already places MCSP-oracle devices above
      AC0[p] independent of Lemma 41.
  (3) The headline of the meta-complexity assessment is: Chen-Hirahara-Ren S2E (STOC 2024,
      arXiv:2309.12912) RELATIVIZES (verbatim "Our proofs relativize"). A relativizing engine
      localizes trivially, so the strongest proved-non-constructivity engine is DISQUALIFIED as
      the non-local ingredient. The W2A core also relativizes (Hirahara 2018). So the entire
      non-relativizing burden falls on the Williams spine, which has not been pushed to an HM
      threshold (J4 sharpened, no combining theorem).
  (4) 2025 magnification (Atserias-Muller arXiv:2503.24061) is still within the magnification
      paradigm with no locality-evasion claimed.

ILLUSTRATION DISCIPLINE (Track 2 is a PINNED GAP MAP, not a proof). The magnification-threshold
arithmetic and the locality cap are encoded as NUMBERS so the barrier is concrete, and labeled
illustrative. No lower bound is proved.

HONESTY DISCIPLINE. PROVED facts cite venue/year/arXiv. Track 1 is an IN-MODEL (cheap-measurement)
bound even if closed (the max is information-theoretically cheap from the factors), not an
unconditional algorithm lower bound. NEXP not in poly-size THR-of-THR is OPEN as of June 2026.
No speedup is claimed. NO PROGRESS ON THE PRIZE CLAIMED. No em dashes or en dashes anywhere.

Run:
    python -m experiments.circuit_complexity.e_j1_subblock_j3_locality
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# REUSE the J1 baseline ground truth (Boolean Max-IP two ways) from the executable sibling.
from experiments.circuit_complexity.e_maxip_logshave import (
    max_ip_bruteforce,
    max_ip_matrix_product,
)
from experiments._shared.barriers import BarrierChecker
from experiments._shared.technique import ProofTechnique


EPS = 0.1   # d = n^eps; any constant eps > 0.


# ==========================================================================
# TRACK 1. The planted gapless family (Chen Cor 5.5 / Lemma 5.1): dense bulk capped at d-1, one
# spike of value d. The gap-1 increment is faithful: a cell goes d-1 -> d, signal 2d-1.
# ==========================================================================


def make_bulk(n: int, d: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Dense GAPLESS worst case: every row popcount EXACTLY d/2, so M_ij ~ d/4 with genuine
    Binomial-style fluctuation (std Theta(sqrt(d))). No popcount-spread lever exists."""
    rng = np.random.default_rng(seed)
    w = d // 2

    def rows(m: int) -> np.ndarray:
        R = np.zeros((m, d), dtype=np.float64)
        for i in range(m):
            R[i, rng.choice(d, size=w, replace=False)] = 1.0
        return R

    return rows(n), rows(n)


def make_planted_gap(n: int, d: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """GAPPED (Valiant/light-bulb): sparse bulk + one planted full-overlap pair. The spike is
    Theta(d) above the sparse bulk, so a single spectral read DETECTS it. The proves-too-much
    control must detect here while staying blind on the gapless gap-1 family."""
    rng = np.random.default_rng(seed)
    A = (rng.random((n, d)) < 0.08).astype(np.float64)
    B = (rng.random((n, d)) < 0.08).astype(np.float64)
    A[0, :] = 1.0
    B[0, :] = 1.0
    return A, B


def make_gap1_pair(n: int, d: int, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, tuple[int, int]]:
    """Two rank-<=d Boolean instances (A,B) and (A,B') differing in ONE cell by +1 (the grounding).

    a_{i*} = all-ones; b_{j*} all-ones EXCEPT a private bit k* (so M[i*,j*] = d-1, the NO top).
    Flipping b'_{j*}[k*]=1 makes M'[i*,j*] = d (the YES top); k* is set in exactly ONE A-row so
    ONLY that cell changes. Returns (A, B_no, B_yes, (i*,j*))."""
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


# ==========================================================================
# TRACK 1, ROUTE (a): the deflation contrast, with the adversary's MOMENT-ADDITIVITY correction.
# ==========================================================================


def deflation_residual_linear_vs_nonlinear(n: int, d: int, seed: int) -> dict[str, float]:
    """The Route-(a) contrast (the prong's measurement), kept for the spectral / cross-block case.

    LINEAR (Simchowitz Obs 3.1): given w_k = M v_k, the response to a new query v_k in span(past)
    is exactly determined (residual 0): the orthogonalize-WLOG step is valid. NON-LINEAR (a fresh
    block moment predicted from disjoint other-block moments): no determination (residual ~1).
    This is the prong's evidence the per-round chain rule does not type-check for non-linear reads.
    """
    rng = np.random.default_rng(seed)
    A, B = make_bulk(n, d, seed)
    M = np.minimum(A @ B.T, float(d - 1))

    V = rng.standard_normal((n, 5))
    W = M @ V
    v_new = V @ rng.standard_normal(5)          # a new query IN span(past)
    w_new = M @ v_new
    coef, *_ = np.linalg.lstsq(W, w_new, rcond=None)
    lin_resid = float(np.linalg.norm(W @ coef - w_new) / (np.linalg.norm(w_new) + 1e-12))

    b = 8
    rows = []
    targets = []
    for _ in range(200):
        ri = rng.integers(0, n - b + 1); ci = rng.integers(0, n - b + 1)
        rows.append([float((M[ri:ri + b, ci:ci + b] ** p).sum()) for p in (1, 2, 3)])
        rj = rng.integers(0, n - b + 1); cj = rng.integers(0, n - b + 1)
        targets.append(float((M[rj:rj + b, cj:cj + b] ** 2).sum()))   # a DIFFERENT fresh block
    X = np.array(rows); y = np.array(targets)
    Xa = np.hstack([X, np.ones((len(X), 1))])
    coef2, *_ = np.linalg.lstsq(Xa, y, rcond=None)
    pred = Xa @ coef2
    nonlin_resid = float(np.linalg.norm(pred - y) / (np.linalg.norm(y - y.mean()) + 1e-12))

    return {
        "linear_deflation_residual": lin_resid,        # ~ 0: determined (WLOG valid)
        "nonlinear_deflation_residual": nonlin_resid,  # ~ 1: not determined (cross-block)
    }


def moment_additivity_residual(n: int, d: int, seed: int) -> dict[str, float]:
    """ADVERSARY CORRECTION to Route (a). Degree-2 entry-symmetric MOMENTS are EXACTLY additive
    over a tiling: a b x b block moment is the sum of its 4 (b/2 x b/2) sub-quadrant moments, so a
    tiling-based deflation DOES exist for the moment family. The no-port claim is sound ONLY for the
    non-additive SPECTRAL reads (whose tiling residual is nonzero). We measure both residuals.
    """
    rng = np.random.default_rng(seed)
    A, B = make_bulk(n, d, seed)
    M = np.minimum(A @ B.T, float(d - 1))
    b = 16
    ri = int(rng.integers(0, n - b + 1)); ci = int(rng.integers(0, n - b + 1))
    blk = M[ri:ri + b, ci:ci + b]
    h = b // 2
    full_moment = float((blk ** 2).sum())
    tiled_moment = sum(float((blk[r:r + h, c:c + h] ** 2).sum()) for r in (0, h) for c in (0, h))
    moment_resid = abs(full_moment - tiled_moment)
    # Spectral (top singular value) is NOT additive over the same tiling: a genuine residual.
    full_spec = float(np.linalg.svd(blk, compute_uv=False)[0])
    tiled_spec = sum(float(np.linalg.svd(blk[r:r + h, c:c + h], compute_uv=False)[0])
                     for r in (0, h) for c in (0, h))
    spectral_resid = abs(full_spec - tiled_spec)
    return {
        "moment_tiling_residual": moment_resid,        # ~ 0: moments tile exactly (deflation exists)
        "spectral_tiling_residual": spectral_resid,    # > 0: spectral reads do NOT tile (no port)
        "moment_full": full_moment,
        "spectral_full": full_spec,
    }


# ==========================================================================
# TRACK 1, ROUTE (b): the location-information telescope and the adversary's FATAL inconsistency.
# ==========================================================================


def per_round_snr(n: int, d: int, b: int, seed: int, trials: int = 400) -> dict[str, float]:
    """SNR of a degree-2 sub-block moment as a spike-membership test, FAITHFUL gap-1 signal.

    signal = 2d-1 (the exact degree-2 moment shift when one cell goes d-1 -> d), noise = std of the
    block moment over random positions. Measured law: SNR ~ C0/(b sqrt(d)), so SNR*b*sqrt(d) is a
    constant (~15-16). A proper sub-block (b >= 2) is sub-SNR at gap 1; even a single cell has
    SNR ~ const/sqrt(d) < 1 for moderate d. The spike is below the per-cell bulk fluctuation.
    """
    rng = np.random.default_rng(seed)
    A, B = make_bulk(n, d, seed)
    M = np.minimum(A @ B.T, float(d - 1))
    masses = []
    for _ in range(trials):
        ri = rng.integers(0, n - b + 1); ci = rng.integers(0, n - b + 1)
        masses.append(float((M[ri:ri + b, ci:ci + b] ** 2).sum()))
    sig = float(np.std(masses)) + 1e-12
    delta = 2.0 * d - 1.0
    snr = delta / sig
    return {"b": float(b), "d": float(d), "signal": delta, "block_moment_std": sig,
            "snr": snr, "snr_times_b_sqrt_d": snr * b * math.sqrt(d)}


def _mutual_info_binned(x: list[float], y: list[int], nbins: int = 25) -> float:
    """I(x; y) in bits, x continuous (binned by quantile), y binary. Has a positive estimator bias
    ~ (nbins-1)/(2 N ln 2); the null floor below makes that bias visible."""
    xa = np.asarray(x, dtype=np.float64); ya = np.asarray(y, dtype=np.int64)
    edges = np.quantile(xa, np.linspace(0, 1, nbins + 1)); edges[-1] += 1e-6
    bx = np.clip(np.digitize(xa, edges) - 1, 0, nbins - 1)
    py = np.array([np.mean(ya == 0), np.mean(ya == 1)])
    info = 0.0
    for bb in range(nbins):
        mask = (bx == bb)
        pxb = mask.mean()
        if pxb == 0:
            continue
        for c in (0, 1):
            pj = np.mean(mask & (ya == c))
            if pj > 0:
                info += pj * math.log2(pj / (pxb * py[c] + 1e-300))
    return max(info, 0.0)


def per_round_location_info(n: int, d: int, b: int, seed: int, mode: str,
                            trials: int = 40000) -> dict[str, float]:
    """I( degree-2 block moment ; 1_{spike in this block} ), the prong's "load-bearing" quantity.

    THE ADVERSARY'S SMALLEST BREAKING CASE is the choice of `mode` (the spike-injection line):

      mode='outlier'  : bm = bm - M[si,sj]^2 + d^2   (the prong's per_round_location_info, line 251).
                        This upgrades a bulk cell of value ~d/4 to a Theta(d^2) OUTLIER, NOT the
                        gap-1 increment. The headline I/f ~ const ~4.5 holds ONLY here.
      mode='faithful' : bm = bm + (2d-1)             (the gap-1 increment used by per_round_snr).
                        Under the faithful signal, I/f COLLAPSES with b toward the estimator null
                        floor: no C b^2/n^2 law survives.
      mode='null'     : independent label with matched marginal f (the estimator's positive-bias
                        floor; any measured I below this floor is noise, not signal).

    The two load-bearing measurements in the prong used CONTRADICTORY signal models (faithful in
    per_round_snr, outlier here). Only the outlier signal is above the floor; the faithful one,
    the one that matters, sits at the floor. So Route (b)'s closing law is a measurement artifact.
    """
    rng = np.random.default_rng(seed)
    A, B = make_bulk(n, d, seed)
    M = np.minimum(A @ B.T, float(d - 1))
    f_target = (float(b) / float(n)) ** 2
    moms: list[float] = []
    inblock: list[int] = []
    for _ in range(trials):
        ri = rng.integers(0, n - b + 1); ci = rng.integers(0, n - b + 1)
        blk = M[ri:ri + b, ci:ci + b]
        bm = float((blk ** 2).sum())
        if mode == "null":
            # Label is independent of the moment (matched marginal): the estimator floor.
            inblock.append(int(rng.random() < f_target))
            moms.append(bm)
            continue
        si, sj = int(rng.integers(n)), int(rng.integers(n))
        if ri <= si < ri + b and ci <= sj < ci + b:
            if mode == "outlier":
                bm = bm - float(M[si, sj]) ** 2 + float(d) ** 2     # Theta(d^2) outlier (the artifact)
            else:                                                   # 'faithful'
                bm = bm + (2.0 * d - 1.0)                           # the gap-1 increment d-1 -> d
            inblock.append(1)
        else:
            inblock.append(0)
        moms.append(bm)
    info = _mutual_info_binned(moms, inblock)
    f = float(np.mean(inblock))
    return {"b": float(b), "d": float(d), "mode": mode, "f_b2_over_n2": f, "info_bits": info,
            "info_over_f": info / max(f, 1e-12)}


def greedy_descent_success(n: int, d: int, seed: int, repeats: int = 40) -> dict[str, float]:
    """The adaptive-conditioning probe (faithful gap-1: plant value d over a bulk capped at d-1).
    The cheapest adaptive tree (greedy quadrant descent, O(log n) reads) recursively descends into
    the heaviest degree-2 sub-block quadrant. Success DECAYS with n because the top-level quadrant
    tests are sub-SNR coins. Strong evidence the cheap adaptive tree cannot win, but a simulation.
    """
    succ = 0
    for s in range(repeats):
        rng = np.random.default_rng(seed + s)
        A, B = make_bulk(n, d, seed + s)
        M = np.minimum(A @ B.T, float(d - 1)).copy()
        si, sj = int(rng.integers(n)), int(rng.integers(n))
        M[si, sj] = float(d)
        r0, c0, R = 0, 0, n
        while R > 1:
            h = max(R // 2, 1)
            quads = [(r0, c0), (r0, c0 + h), (r0 + h, c0), (r0 + h, c0 + h)]
            best, bq = -1.0, (r0, c0)
            for (rr, cc) in quads:
                hr = min(h, r0 + R - rr); hc = min(h, c0 + R - cc)
                if hr <= 0 or hc <= 0:
                    continue
                mom = float((M[rr:rr + hr, cc:cc + hc] ** 2).sum())
                if mom > best:
                    best, bq = mom, (rr, cc)
            r0, c0 = bq
            R = h
        if r0 == si and c0 == sj:
            succ += 1
    return {"n": float(n), "d": float(d), "reads_per_run": float(4 * max(int(math.log2(n)), 1)),
            "success_rate": succ / repeats}


def proves_too_much(n: int, d: int, seed: int) -> dict[str, float]:
    """The guard: a single full-matrix spectral read DETECTS a constant relative gap (GAPPED Valiant
    family, spike Theta(d) above sparse bulk) but is BLIND at gap 1 (gapless family). The detection
    ratio GROWS with d, so the lemma is blind ONLY at gap 1 and Valiant FOCS 2012 survives."""
    Ag, Bg = make_planted_gap(n, d, seed)
    Mg = Ag @ Bg.T
    rng = np.random.default_rng(seed)
    Ag0 = Ag.copy(); Ag0[0, :] = (rng.random(d) < 0.08).astype(np.float64)
    Mg0 = Ag0 @ Bg.T
    shift_gapped = abs(float(np.linalg.svd(Mg, compute_uv=False)[0])
                       - float(np.linalg.svd(Mg0, compute_uv=False)[0]))
    Al, Bl = make_bulk(n, d, seed)
    Al[0, :] = 1.0; Bl[0, :] = 1.0
    ks = d - 1
    Al[:, ks] = 0.0; Al[0, ks] = 1.0
    Bn = Bl.copy(); Bn[0, ks] = 0.0; Mn = Al @ Bn.T
    By = Bn.copy(); By[0, ks] = 1.0; My = Al @ By.T
    shift_gapless = abs(float(np.linalg.svd(My, compute_uv=False)[0])
                        - float(np.linalg.svd(Mn, compute_uv=False)[0]))
    return {"n": float(n), "d": float(d), "shift_gapped": shift_gapped,
            "shift_gapless": shift_gapless, "ratio": shift_gapped / (shift_gapless + 1e-12)}


def subblock_lemma_technique() -> ProofTechnique:
    """The sub-block lemma route, encoded as a model-restricted (in-model) lower bound. Evades all
    three: concrete factored structure (non-relativizing), one planted instance (non-large), the
    force is the non-algebraic location / SNR floor (non-algebrizing). An information-theoretic
    query-model object, orthogonal to all three barriers (J1 is the algorithmic, barrier-free joint).
    """
    return ProofTechnique(
        name="Sub-block lemma (adaptive cheap-statistic query lower bound, in-model)",
        relativizes=False,
        natural_largeness=False,
        natural_constructivity=False,
        algebrizes=False,
        notes=("An in-model query bound; the force is the gap-1 SNR floor (Theta(1/(b sqrt(d))) per "
               "sub-block), an information-theoretic ingredient. Currently OPEN: the per-round "
               "conditional location-info under adaptive block choice is the survey's named missing "
               "object. Not a natural proof; not an unconditional algorithm lower bound."),
    )


# ==========================================================================
# TRACK 2 (J3): the locality barrier, made a number. ILLUSTRATIVE, not a proof.
# ==========================================================================


@dataclass
class TechRow:
    """A lower-bound technique and its locality status relative to the HM frontier."""
    technique: str
    locality: str          # LOCAL | NON-LOCAL-but-not-at-HM-threshold | RELATIVIZES=>LOCALIZES
    citation: str
    at_hm_threshold: bool   # does it reach an N^{1+eps} bound for an HM-frontier problem?


def magnification_gap(N: float, eps: float, delta: float) -> dict[str, float]:
    """The magnification-threshold arithmetic (CHOPRS Thm 2, coupled B1^O / B3^O). ILLUSTRATIVE.

    HM unconditionally emits the magnified circuit at size N^{1+eps} (B1^O). The known InnerProduct
    technique can only refute Formula-O-XOR of size up to N^{2-3delta} with oracle fan-in N^delta
    (B3^O). The magnified circuit (size N^{1+eps}) lives BELOW the technique floor (N^{2-3delta}),
    inside the class the technique provably HOLDS for, so the technique cannot separate it. We return
    the two exponents and the boolean `separates` (always False for the magnifying overlap regime).
    """
    magnified_exp = 1.0 + eps          # log_N(magnified circuit size)
    technique_floor_exp = 2.0 - 3.0 * delta   # log_N(technique impossibility floor)
    # The technique can only EXCLUDE the regime ABOVE its floor; the magnified circuit is below it,
    # so technique and target overlap inside the same class and cannot be separated.
    separates = magnified_exp > technique_floor_exp
    return {
        "N": N, "eps": eps, "delta": delta,
        "magnified_size_exp": magnified_exp,
        "technique_floor_exp": technique_floor_exp,
        "separates": separates,
        "overlap": (not separates),
    }


def giikkt_cap(d: int) -> dict[str, float]:
    """The GIIKKT MCSP cap (ICALP 2019 / ECCC TR19-018). ILLUSTRATIVE. The strongest unconditional
    MCSP lower bound: depth-d AC0[p] requires size exp(Omega(N^{0.49/d})), N = 2^n. ADVERSARY-
    CORRECTED exponent 0.49/d (NOT 0.49/(d-1)); matches the repo's e_leading_path_descent.py.
    The cap exponent decreases in d. It is the strongest MCSP bound and lives in AC0[p], far below
    any TC0-against-magnifying-model bound. (The computational cap that binds J3 is the membership
    MAJ, NC1 in (AC0)^MCSP, which is gate-type-agnostic and SEPARATE from this degree exponent.)"""
    return {"depth_d": float(d), "cap_exponent": 0.49 / d}


def localization_degree(fan_in_log_N_exp: float, gate_type: str) -> dict[str, object]:
    """The Lemma-41 localization collapse (CHOPRS). ILLUSTRATIVE. A fan-in-O oracle gate is replaced
    by its multilinear extension, a degree-<=O polynomial, for AC0[p]-family gates {AND,OR,XOR,MOD_p}
    (the polynomial-method collapse applies, keeping AC0[+]^O low-degree). For a THRESHOLD oracle
    gate the multilinear extension is HIGH degree (MAJORITY: approximate degree Theta(sqrt N), full
    degree Theta(N)), so Lemma 41 does NOT obviously port to threshold-oracle circuits.

    ADVERSARY DEMOTION: this is a SEAM in the Lemma-41 degree argument, NOT a loosening of the
    GIIKKT computational cap. The cap (MAJ, NC1 in (AC0)^MCSP) is gate-type-agnostic and holds
    WITHOUT Lemma 41, so "cap proved at AC0[p] but not TC0" is a mis-location. The seam is the open
    TC0 lower-bound problem relabeled, not a feature making TC0 specifically evasion-friendly.
    """
    poly_method_family = gate_type in ("AND", "OR", "XOR", "MOD_p")
    if poly_method_family:
        return {"gate_type": gate_type, "collapse_degree": "<= fan_in (low-degree)",
                "lemma41_ports": True}
    return {"gate_type": gate_type,
            "collapse_degree": "high (approx-deg Theta(sqrt N), full Theta(N))",
            "lemma41_ports": False}


def hm_technique_rows() -> list[TechRow]:
    """The technique / locality classification (CHOPRS; GIIKKT; Pich 2024; CHR 2024; Hirahara 2018).
    Every concrete combinatorial technique is LOCAL; the two non-local objects are not at an HM
    threshold; the relativizing engines localize trivially. Exactly ZERO are NON-LOCAL-AND-at-HM-
    threshold: the open no-go."""
    return [
        TechRow("counting / gate elimination", "LOCAL", "CHOPRS JACM 2022", False),
        TechRow("polynomial method (Razborov-Smolensky)", "LOCAL", "CHOPRS Lemma 41", False),
        TechRow("approximate degree (Tal Formula-XOR)", "LOCAL", "CHOPRS Lemma 44-45", False),
        TechRow("random restriction / switching lemma", "LOCAL", "CHOPRS Sec 5.1.5", False),
        TechRow("reduction-based bounds", "LOCAL", "CHOPRS Sec 5.1.6 (definitive)", False),
        TechRow("approximation method (Razborov)", "LOCAL", "Pich Comp.Compl. 2024 (2212.09285)", False),
        TechRow("Williams-spine algorithm-to-LB", "NON-LOCAL-but-not-at-HM-threshold",
                "Williams 2011 spine; Oliveira 2019 suggestive", False),
        TechRow("pseudorandom-restriction above-threshold", "NON-LOCAL-but-not-at-HM-threshold",
                "CHOPRS Thm 49 (Frontier D, wrong problem)", False),
        TechRow("S2E near-maximum (proved non-constructivity)", "RELATIVIZES=>LOCALIZES",
                "Chen-Hirahara-Ren STOC 2024 (2309.12912, 'Our proofs relativize')", False),
        TechRow("meta-complexity W2A core", "RELATIVIZES=>LOCALIZES",
                "Hirahara ECCC TR18-138 2018 ('our proofs do relativize')", False),
    ]


def proposed_nonlocal_route() -> ProofTechnique:
    """The proposed non-local route: the Williams spine (non-relativizing) as the non-local
    ingredient. CANDIDATE only, contingent on the open J3 obligation. Relativization pass-by-design;
    natural proofs cleared by HM but the route must then carry NON-CONSTRUCTIVITY (the open J3
    obligation); algebrization not-yet-assessable at dense TC0 (finding 20). Encoded as evading all
    three IN-MODEL, but only as a candidate, not a discharged claim."""
    return ProofTechnique(
        name="Williams-spine-as-non-local-ingredient (CANDIDATE, contingent on open J3)",
        relativizes=False,           # the whole point: the SAT-algorithm link is non-relativizing
        natural_largeness=False,     # HM clears naturalness (CHOPRS Thm 1 (a)<=>(d))
        natural_constructivity=False,
        algebrizes=False,            # not-yet-assessable at dense TC0; encoded as candidate-evading
        notes=("Locality is an oracle-extension (relativization-family) obstruction, so the evading "
               "ingredient must be non-relativizing in a strong oracle-gate-sensitive sense. The "
               "Williams spine is the only plausible source and is a DIRECTION, not a technique "
               "(not at an HM threshold). The meta-complexity non-constructivity engine (S2E, CHR "
               "2024) RELATIVIZES and is disqualified; J4 (no combining theorem) remains."),
    )


# ==========================================================================
# Reporting
# ==========================================================================


def main() -> int:
    print("=== J1 sub-block lemma (Track 1) + J3 locality barrier (Track 2): two open joints ===\n")
    print("Leading path: NEXP / NP not in poly-size THR-of-THR (Williams spine + meta-complexity).")
    print("Four joints (finding 26): J1 ALGORITHMIC, J2 DESCENT (proved), J3 NON-CONSTRUCTIVITY")
    print("(BINDING), J4 COMPOSITION. This module illustrates and re-judges the two open joints J1, J3,")
    print("with the ADVERSARY corrections applied. It does NOT modify the sibling modules.\n")

    # ======================================================================
    # TRACK 1.
    # ======================================================================
    print("=" * 78)
    print("TRACK 1 (J1, finding 33): the SUB-BLOCK NON-LINEAR PER-ROUND INFORMATION LEMMA.")
    print("=" * 78 + "\n")
    print("TARGET (Chen 2018 arXiv:1805.10698 Thm 1.5.1): an n^2/log^{omega(1)} n algorithm for Max-IP")
    print("at d=n^eps implies NEXP not in poly-size THR-of-THR. M = A B^T, gap-1 planted gapless family.")
    print("CONJECTURE: an adaptive K-round tree of cheap non-linear summaries (degree-<1/eps moments,")
    print("rotation-invariant spectral) of ADAPTIVELY-CHOSEN sub-blocks cannot decide max=d vs <=d-1 for")
    print("K=o(n^2). Finding 31 closed the FULL-block case; the open case is proper sub-blocks.\n")

    # Grounding: the gap-1 pair, both valid factored products, one cell apart.
    A, B_no, B_yes, _ = make_gap1_pair(64, 12, seed=5)
    max_no = int((A @ B_no.T).max())
    max_yes = int((A @ B_yes.T).max())
    diff = int(((A @ B_yes.T) - (A @ B_no.T) != 0).sum())
    bf_no = max_ip_bruteforce(A.astype(np.int64), B_no.astype(np.int64))
    print("GROUNDING (the gap-1 hard pair, both valid factored Boolean products):")
    print(f"  n=64, d=12: max(NO)={max_no} (=d-1), max(YES)={max_yes} (=d), cells changed={diff} (exactly one);")
    print(f"  brute force agrees with A B^T on NO: {bf_no}=={max_no} -> {bf_no == max_no}.\n")

    # ROUTE (a)
    print("-" * 78)
    print("ROUTE (a): port the orthogonalize-WLOG deflation to non-linear reads.")
    print("-" * 78 + "\n")
    dr = deflation_residual_linear_vs_nonlinear(128, 64, seed=0)
    print("Simchowitz Obs 3.1: past LINEAR responses w=Mv determine M on span(past); a new query in")
    print("span has residual 0 (WLOG valid). A fresh block moment from DISJOINT other-block moments")
    print("is not determined (cross-block residual ~1):")
    print(f"    LINEAR (w=Mv, new query in span):     residual = {dr['linear_deflation_residual']:.2e}  (~0)")
    print(f"    NON-LINEAR (cross-block moment):      residual = {dr['nonlinear_deflation_residual']:.3f}   (~1)")
    print()
    print("ADVERSARY CORRECTION: the no-port claim is OVERSTATED for MOMENTS. Degree-2 entry-symmetric")
    print("moments are EXACTLY additive over a tiling (block moment = sum of 4 sub-quadrant moments), so")
    print("a tiling-based deflation DOES exist for the moment family. Only the non-additive SPECTRAL read")
    print("genuinely fails to tile:")
    ma = moment_additivity_residual(128, 64, seed=2)
    print(f"    degree-2 MOMENT tiling residual:   {ma['moment_tiling_residual']:.2e}  (~0: moments tile, deflation EXISTS)")
    print(f"    top-singular-value tiling residual:{ma['spectral_tiling_residual']:>10.3f}   (>0: spectral does NOT tile)")
    print("    => Route (a) is dead ONLY for the spectral family; for moments a deflation exists.\n")

    # ROUTE (b): the fatal inconsistency.
    print("-" * 78)
    print("ROUTE (b): the location-information telescope. ADVERSARY: the closing argument FAILS.")
    print("-" * 78 + "\n")
    print("STEP 1 (survives). Per-round SNR of a degree-2 block moment (FAITHFUL gap-1 signal 2d-1) is")
    print("Theta(1/(b sqrt(d))). SNR*b*sqrt(d) ~ const (~15-16); proper sub-blocks are sub-SNR at gap 1:")
    print(f"    {'d':>5} | {'b':>3} | {'signal':>7} | {'mom std':>9} | {'SNR':>8} | {'SNR*b*sqrt(d)':>13}")
    print("    " + "-" * 58)
    for d in (16, 64, 256):
        for b in (1, 2, 8):
            s = per_round_snr(256, d, b, seed=0)
            print(f"    {d:>5} | {b:>3} | {s['signal']:>7.0f} | {s['block_moment_std']:>9.1f} | "
                  f"{s['snr']:>8.4f} | {s['snr_times_b_sqrt_d']:>13.2f}")
    print()

    print("STEP 2 (THE FATAL INCONSISTENCY). The prong's load-bearing law 'per-round info ~ C b^2/n^2,")
    print("C~4.5' depends ENTIRELY on which signal model is used. per_round_snr uses the faithful 2d-1")
    print("increment; the prong's per_round_location_info upgraded a bulk cell to a Theta(d^2) OUTLIER.")
    print("We measure I/f (f = b^2/n^2) under BOTH and against the estimator NULL floor (n=128, d=64):")
    print(f"    {'b':>3} | {'I/f OUTLIER':>12} | {'I/f FAITHFUL':>13} | {'I/f NULL floor':>14}")
    print("    " + "-" * 50)
    n_t, d_t = 128, 64
    faithful_over_null_ok = True
    for b in (2, 4, 8, 16, 32):
        io = np.mean([per_round_location_info(n_t, d_t, b, s, "outlier")["info_over_f"] for s in (3, 4, 5)])
        fa = np.mean([per_round_location_info(n_t, d_t, b, s, "faithful")["info_over_f"] for s in (3, 4, 5)])
        nu = np.mean([per_round_location_info(n_t, d_t, b, s, "null")["info_over_f"] for s in (3, 4, 5)])
        print(f"    {b:>3} | {io:>12.3f} | {fa:>13.4f} | {nu:>14.4f}")
        if b >= 16 and fa > 5.0 * nu + 1.0:
            faithful_over_null_ok = False
    print("    The OUTLIER column is the only one that holds C~4.5; the FAITHFUL column (the one that")
    print("    matters) COLLAPSES with b toward the NULL floor. The C b^2/n^2 law is a measurement")
    print("    artifact of the Theta(d^2) outlier, so the telescope loses its premise: the wall is gone.\n")
    print("    SECONDARY FLAW: the telescope bounds LOCALIZATION (2 log n bits, Fano), but the task is a")
    print("    1-bit DETECTION (max=d vs <=d-1). Detection != localization, so even an airtight telescope")
    print("    would bound a strictly harder problem (proves-too-little).\n")

    print("STEP 3 (survives as evidence, not proof). The cheapest adaptive tree (greedy quadrant descent,")
    print("O(log n) reads) FAILS, success DECAYING with n (top-level quadrant tests are sub-SNR coins):")
    print(f"    {'n':>5} | {'d':>4} | {'reads/run (~4 log n)':>20} | {'spike-found rate':>16}")
    print("    " + "-" * 54)
    descent = []
    for (nn, dd) in [(64, 32), (128, 64), (256, 64), (512, 64)]:
        gd = greedy_descent_success(nn, dd, seed=0, repeats=40)
        descent.append(gd["success_rate"])
        print(f"    {nn:>5} | {dd:>4} | {gd['reads_per_run']:>20.0f} | {gd['success_rate']:>16.2f}")
    print("    success 0.62 -> 0.05 DECAYS: strong evidence the cheap adaptive tree cannot win, but a")
    print("    simulation, not a proof of the per-round conditional-info uniformity (the open object).\n")

    print("PROVES-TOO-MUCH GUARD. A single spectral read DETECTS a constant relative gap (GAPPED Valiant,")
    print("spike Theta(d)) but is blind at gap 1; ratio GROWS with d, so the lemma is blind ONLY at gap 1:")
    print(f"    {'n':>5} | {'d':>5} | {'shift GAPPED':>14} | {'shift GAPLESS':>14} | {'ratio':>10}")
    print("    " + "-" * 60)
    ptm_ratios = []
    for (nn, dd) in [(256, 64), (512, 128), (768, 192)]:
        pt = proves_too_much(nn, dd, seed=1)
        ptm_ratios.append(pt["ratio"])
        print(f"    {nn:>5} | {dd:>5} | {pt['shift_gapped']:>14.3f} | {pt['shift_gapless']:>14.4f} | "
              f"{pt['ratio']:>10.1f}")
    print("    ratio GROWS with d: gaplessness used essentially; Valiant FOCS 2012 / light-bulb survives.\n")

    print("TRACK 1 VERDICT: the sub-block lemma is OPEN (the prong's 'lemma-partial' is OVERSTATED).")
    print("  Route (a) is dead only for spectral reads (moments tile, a deflation exists). Route (b)'s")
    print("  closing law is a measurement artifact (the faithful gap-1 info sits at the null floor) and")
    print("  bounds the wrong (harder) problem (localization, not detection). What survives is the SNR")
    print("  law and the greedy-descent decay, which are evidence, not a proof. The lemma is exactly the")
    print("  survey's named missing object: an adaptive low-degree / spectral query lower bound.\n")

    # ======================================================================
    # TRACK 2.
    # ======================================================================
    print("=" * 78)
    print("TRACK 2 (J3, finding 34): the LOCALITY BARRIER (the BINDING joint). A PINNED GAP MAP.")
    print("=" * 78 + "\n")
    print("J3 wants a PROVED MCSP-against-TC0 lower bound; hardness magnification (HM) would amplify a")
    print("weak N^{1+eps} bound to the prize. The LOCALITY BARRIER (GIIKKT ICALP 2019; CHOPRS JACM 2022)")
    print("says the known techniques are LOCAL (extend to small-fan-in oracle circuits) and HM emits")
    print("exactly such circuits, so technique and target meet in the same class. ILLUSTRATIVE numbers:\n")

    print("PART 1. The magnification-threshold arithmetic (CHOPRS Thm 2, coupled B1^O/B3^O). HM emits")
    print("the magnified circuit at size N^{1+eps}; the known technique can only refute size up to")
    print("N^{2-3delta}. The magnified circuit lives BELOW that floor, inside the class the technique")
    print("HOLDS for, so it cannot separate (overlap, not separation):")
    print(f"    {'eps':>5} | {'delta':>6} | {'magnified exp (1+eps)':>21} | {'technique floor (2-3d)':>22} | {'separates':>10}")
    print("    " + "-" * 76)
    any_separates = False
    for delta in (0.1, 0.2, 0.3):
        mg = magnification_gap(1e6, 0.01, delta)
        any_separates = any_separates or mg["separates"]
        print(f"    {mg['eps']:>5.2f} | {mg['delta']:>6.2f} | {mg['magnified_size_exp']:>21.3f} | "
              f"{mg['technique_floor_exp']:>22.3f} | {str(mg['separates']):>10}")
    print("    separates = False for every delta: the local technique provably cannot fire (illustrative).\n")

    print("PART 2. The GIIKKT MCSP cap (ICALP 2019 / ECCC TR19-018). ADVERSARY-CORRECTED exponent")
    print("0.49/d (NOT 0.49/(d-1)); matches the repo's e_leading_path_descent.py. depth-d AC0[p] needs")
    print("size exp(Omega(N^{0.49/d})), N=2^n. The exponent DECREASES in d; the cap lives in AC0[p]:")
    print(f"    {'depth d':>8} | {'cap exponent 0.49/d':>20} | {'exp(Omega(N^e))':>16}")
    print("    " + "-" * 50)
    caps = []
    for d in (2, 3, 4, 6):
        gc = giikkt_cap(d)
        caps.append(gc["cap_exponent"])
        print(f"    {int(gc['depth_d']):>8} | {gc['cap_exponent']:>20.4f} | "
              f"exp(Omega(N^{gc['cap_exponent']:.3f}))")
    print("    The BINDING computational cap is gate-type-AGNOSTIC: MAJ in (AC0)^MCSP and NC1 in")
    print("    (AC0)^MCSP (GIIKKT Cor 5.1/5.2), so an AC0-with-MCSP-oracle device already computes >=")
    print("    MAJORITY. This holds WITHOUT the degree exponent above; it places MCSP-oracle devices")
    print("    strictly above AC0[p] independent of Lemma 41.\n")

    print("PART 3. The Lemma-41 localization collapse and the (DEMOTED) TC0 seam. A fan-in-O oracle gate")
    print("becomes a degree-<=O multilinear extension for AC0[p]-family gates; a THRESHOLD gate's")
    print("extension is high-degree, so Lemma 41 does not obviously port to threshold oracles:")
    print(f"    {'gate type':>10} | {'collapse degree':>42} | {'Lemma 41 ports?':>15}")
    print("    " + "-" * 74)
    seam_cell = None
    for gt in ("AND", "XOR", "MOD_p", "THRESHOLD"):
        ld = localization_degree(0.1, gt)
        if gt == "THRESHOLD":
            seam_cell = ld
        print(f"    {gt:>10} | {str(ld['collapse_degree']):>42} | {str(ld['lemma41_ports']):>15}")
    print("    ADVERSARY DEMOTION: this seam is in the Lemma-41 DEGREE argument, NOT in the cap. The cap")
    print("    (MAJ, NC1 in (AC0)^MCSP) is gate-type-agnostic and is NOT loosened by it, so 'cap proved")
    print("    at AC0[p] but not TC0' is a MIS-LOCATION. The seam is the open TC0 lower-bound problem")
    print("    relabeled: a coordinate, not a win-win opening.\n")

    print("PART 4. The technique / locality classification. Every concrete combinatorial technique is")
    print("LOCAL; the non-local objects are not at an HM threshold; the relativizing engines localize.")
    rows = hm_technique_rows()
    print(f"    {'technique':<46} | {'locality':<33} | {'@HM thr':>7}")
    print("    " + "-" * 92)
    nonlocal_at_threshold = 0
    for r in rows:
        if r.locality.startswith("NON-LOCAL") and r.at_hm_threshold:
            nonlocal_at_threshold += 1
        print(f"    {r.technique[:46]:<46} | {r.locality:<33} | {str(r.at_hm_threshold):>7}")
    print(f"    techniques that are NON-LOCAL AND at an HM threshold: {nonlocal_at_threshold} (the open no-go).")
    print("    HEADLINE (meta-complexity disqualifier): Chen-Hirahara-Ren S2E (STOC 2024, arXiv:2309.12912)")
    print("    states VERBATIM 'Our proofs relativize'. A relativizing engine localizes trivially, so the")
    print("    strongest proved-non-constructivity engine CANNOT be the non-local ingredient. The W2A core")
    print("    relativizes too (Hirahara 2018). 2025 magnification (Atserias-Muller arXiv:2503.24061) is")
    print("    still within the magnification paradigm, no locality-evasion claimed.\n")

    print("PART 5. Three-barrier bookkeeping on the proposed non-local route (the Williams spine as the")
    print("non-local ingredient). CANDIDATE only, contingent on the open J3 obligation:")
    checker = BarrierChecker()
    v_route = checker.check(proposed_nonlocal_route())
    print(v_route.report())
    print()
    print("    Locality is itself an oracle-extension (relativization-family) obstruction, so the evading")
    print("    ingredient must be non-relativizing in a strong, oracle-gate-sensitive sense. The route is")
    print("    a DIRECTION (not at an HM threshold); J4 (no combining theorem) remains, with the entire")
    print("    non-relativizing burden on the spine because both meta-complexity engines relativize.\n")

    print("TRACK 2 VERDICT: J3 is an OPEN NO-GO with no completed candidate technique (June 2026). A sharp")
    print("  MAP, not a resolution. The single attackable coordinate (the open TC0 lower-bound problem,")
    print("  relabeled via the Lemma-41 / threshold-oracle seam) is a coordinate, not a win-win opening.\n")

    # ======================================================================
    # Three-barrier self-check on the Track-1 in-model object.
    # ======================================================================
    print("=" * 78)
    print("BARRIER DISCIPLINE (three-barrier self-check).")
    print("=" * 78 + "\n")
    v_sub = checker.check(subblock_lemma_technique())
    print(v_sub.report())
    print("  (Track 1 is an information-theoretic query-model object, orthogonal to all three barriers;")
    print("   consistent with J1 being the algorithmic, barrier-free joint.)\n")

    # ======================================================================
    # FINAL SUMMARY.
    # ======================================================================
    print("=" * 78)
    print("FINAL SUMMARY")
    print("=" * 78 + "\n")
    print("TRACK 1 (J1 sub-block lemma): OPEN (not closed, not partial). The prong's closing Route (b)")
    print("  is a measurement artifact: under the FAITHFUL gap-1 signal the per-round location info")
    print("  collapses to the estimator null floor (no C b^2/n^2 law), and the telescope bounds")
    print("  localization rather than the 1-bit detection task. Route (a) is dead only for spectral")
    print("  reads (degree-2 moments tile exactly, so a deflation exists). The surviving coordinates")
    print("  (SNR ~ Theta(1/(b sqrt d)); greedy-descent decay 0.62 -> 0.05; gap-1-only blindness) are")
    print("  evidence, not a proof. The lemma is the survey's named missing object.\n")
    print("TRACK 2 (J3 locality barrier): OPEN NO-GO (a sharp map). Every concrete combinatorial")
    print("  technique is LOCAL (CHOPRS; Pich 2024 adds the approximation method). The proved-non-")
    print("  constructivity engine (S2E, CHR STOC 2024) and the W2A core (Hirahara 2018) both")
    print("  RELATIVIZE, so meta-complexity cannot be the non-local ingredient. Zero techniques are")
    print("  NON-LOCAL-AND-at-HM-threshold. The TC0 seam is a coordinate (the open TC0 lower-bound")
    print("  problem relabeled), not a win-win opening. J4 (no combining theorem) remains.\n")
    print("HONESTY CAVEAT: even a closed Track-1 lemma is an IN-MODEL (cheap-measurement) bound, not an")
    print("  unconditional algorithm lower bound. NEXP not in poly-size THR-of-THR is OPEN as of June")
    print("  2026. NO PROGRESS ON THE PRIZE CLAIMED.\n")

    # ======================================================================
    # Self-checks pinning the key coordinates. Module must exit 0.
    # ======================================================================

    # (G) The gap-1 grounding: two valid factored products, one cell apart, max d vs d-1.
    assert max_no == 11 and max_yes == 12, "the gap-1 pair must have max d-1=11 (NO), d=12 (YES)"
    assert diff == 1, "YES = NO + exactly one Boolean bit flip"
    assert bf_no == max_no, "brute force must agree with A B^T on the NO instance"

    # (T1.a) Route (a): linear deflation works (residual ~0); cross-block non-linear does not.
    assert dr["linear_deflation_residual"] < 1e-6, "linear deflation residual must be ~0 (WLOG valid)"
    assert dr["nonlinear_deflation_residual"] > 0.5, "cross-block non-linear moment is not determined"
    # ADVERSARY CORRECTION: degree-2 moments tile EXACTLY (a deflation exists); spectral does not.
    assert ma["moment_tiling_residual"] < 1e-6, \
        "degree-2 moments must tile exactly (a tiling deflation exists for the moment family)"
    assert ma["spectral_tiling_residual"] > 1e-3, \
        "the top singular value does NOT tile (spectral reads genuinely fail to deflate)"

    # (T1.b) THE FATAL INCONSISTENCY: the C b^2/n^2 law holds for the OUTLIER signal but the FAITHFUL
    #        gap-1 signal collapses toward the null floor. The closing law is a measurement artifact.
    io_b16 = np.mean([per_round_location_info(128, 64, 16, s, "outlier")["info_over_f"] for s in (3, 4, 5)])
    fa_b16 = np.mean([per_round_location_info(128, 64, 16, s, "faithful")["info_over_f"] for s in (3, 4, 5)])
    nu_b16 = np.mean([per_round_location_info(128, 64, 16, s, "null")["info_over_f"] for s in (3, 4, 5)])
    assert io_b16 > 2.0, "the OUTLIER signal gives I/f ~ O(1) (the prong's artifact law)"
    assert fa_b16 < 0.5, "the FAITHFUL gap-1 signal's I/f COLLAPSES with b (no C b^2/n^2 law)"
    assert fa_b16 < 10.0 * max(nu_b16, 1e-9), \
        "the faithful I/f at b=16 is at the estimator null floor (it was never reliably measured)"
    assert faithful_over_null_ok, \
        "the faithful per-round info must sit at the null floor at large b (the closing law fails)"

    # (T1.SNR) The per-round SNR law survives: SNR*b*sqrt(d) ~ const, decaying SNR with b.
    snr_law = [per_round_snr(256, d, b, seed=0)["snr_times_b_sqrt_d"]
               for d in (16, 64, 256) for b in (1, 2, 8)]
    assert max(snr_law) / min(snr_law) < 1.3, \
        "SNR*b*sqrt(d) must be roughly constant (the SNR = Theta(1/(b sqrt d)) law)"
    s_b1 = per_round_snr(256, 64, 1, seed=0)["snr"]
    s_b8 = per_round_snr(256, 64, 8, seed=0)["snr"]
    assert s_b1 > s_b8, "SNR must decrease with block size b"

    # (T1.descent) The greedy adaptive descent success DECAYS with n (evidence, not proof).
    assert descent[0] > descent[-1] + 0.2, \
        "greedy quadrant descent success must DECAY with n (sub-SNR top-level coins)"
    assert descent[-1] < 0.2, "at n=512 the cheap adaptive descent essentially fails"

    # (T1.PTM) The proves-too-much guard: a constant relative gap is detectable; blind only at gap 1.
    assert all(r > 100.0 for r in ptm_ratios), \
        "the gapped/gapless spectral-shift ratio must be large (>100x): blind ONLY at gap 1"

    # (T2.1) The magnification gap NEVER separates in the overlap regime (the locality forbiddance).
    assert not any_separates, \
        "the local technique cannot separate the magnified circuit (overlap, illustrative)"

    # (T2.2) GIIKKT cap exponent is 0.49/d (ADVERSARY-CORRECTED), strictly decreasing in d. The
    #        smallest breaking case: giikkt_cap(2) must be 0.245, NOT the prong's 0.49.
    assert abs(giikkt_cap(2)["cap_exponent"] - 0.245) < 1e-9, \
        "GIIKKT cap exponent at d=2 must be 0.49/2 = 0.245 (NOT 0.49/(d-1) = 0.49)"
    assert all(caps[i] > caps[i + 1] for i in range(len(caps) - 1)), \
        "the GIIKKT cap exponent strictly decreases in depth d"

    # (T2.3) Lemma 41 ports for AC0[p]-family gates and NOT for THRESHOLD (the seam), but the seam is
    #        a coordinate, not a cap loosening (the cap is gate-type-agnostic).
    assert localization_degree(0.1, "XOR")["lemma41_ports"] is True, \
        "Lemma 41 ports for AC0[p]-family (poly-method) oracle gates"
    assert seam_cell is not None and seam_cell["lemma41_ports"] is False, \
        "Lemma 41 does NOT obviously port to a THRESHOLD oracle gate (the seam)"

    # (T2.4) Exactly ZERO techniques are NON-LOCAL-AND-at-HM-threshold: the open no-go.
    assert nonlocal_at_threshold == 0, \
        "no technique is both non-local and at an HM threshold (the open no-go)"
    # The S2E and W2A engines are flagged RELATIVIZES=>LOCALIZES (disqualified non-local ingredients).
    relativizing = [r for r in rows if r.locality.startswith("RELATIVIZES")]
    assert len(relativizing) == 2, \
        "exactly two engines (S2E, W2A core) are flagged relativizing => localizing (disqualified)"

    # (BARRIER) Track-1 in-model object evades all three; the proposed non-local route evades all
    #           three only as a CANDIDATE (contingent on the open J3 obligation).
    assert v_sub.evades_all, "the Track-1 in-model query bound evades all three barriers"
    assert v_route.evades_all, "the proposed non-local route evades all three IN-MODEL (candidate)"
    assert not v_route.hits_relativization, "the non-local route is non-relativizing by design"

    print("=== Self-check OK ===")
    print("(T1.a) Route (a): linear deflation residual ~0, cross-block non-linear ~1; ADVERSARY: degree-2")
    print("       moments tile EXACTLY (deflation exists), only spectral reads fail to tile.")
    print("(T1.b) FATAL INCONSISTENCY: C b^2/n^2 holds for the OUTLIER signal only; the FAITHFUL gap-1")
    print("       signal collapses to the null floor. Route (b)'s closing law is a measurement artifact.")
    print("(T1.SNR) Per-round SNR = Theta(1/(b sqrt d)) survives (SNR*b*sqrt(d) ~ const); proper sub-blocks")
    print("       are sub-SNR at gap 1.")
    print("(T1.descent) Greedy adaptive descent success DECAYS 0.62 -> 0.05 (evidence, not proof).")
    print("(T1.PTM) A constant relative gap is detectable (ratio >100x): blind ONLY at gap 1; Valiant survives.")
    print("(T2) Magnification overlap forbids separation; GIIKKT cap 0.49/d (corrected); Lemma-41 seam is")
    print("       a coordinate not a cap loosening; ZERO non-local-at-threshold techniques; S2E + W2A relativize.")
    print("(STATUS) TRACK 1 = OPEN (sub-block lemma); TRACK 2 = OPEN NO-GO (locality barrier). NEXP not in")
    print("       poly-size THR-of-THR is OPEN as of June 2026. NO PROGRESS ON THE PRIZE CLAIMED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
