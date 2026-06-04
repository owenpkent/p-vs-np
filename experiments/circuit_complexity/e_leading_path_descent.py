"""The leading-path descent to NP: a DESCENT-LADDER LEDGER.

A transparent, self-checking artifact (in the spirit of the strand-3 ledger and
the gap calculators e_threshold_geometry_gap.py / e_maxip_logshave.py). It does
NOT compute new mathematics. It PINS, rung by rung, what the Williams
algorithm-to-lower-bound connection establishes on the descent NEXP -> NQP -> NP,
what each rung needs, and the proved / partial / open status, then classifies the
open joints (algorithmic / descent / non-constructivity / composition) with a
grind-vs-barrier judgment, and runs the NP-scale barrier-evasion bookkeeping
through experiments/_shared/barriers.py.

CAVEAT (load-bearing). This module encodes the LITERATURE-GROUNDED STATUS of the
leading path as of June 2026, not new theorems. Every "proved" row cites a named
result with venue/year. Every "open" / "partial" row is honest that the object is
not yet a discharged lemma. Where a parameter is repo-confirmed (cross-checked in
experiments/LEARNINGS.md findings 12/13/20/23/24/25 against the primary sources)
versus survey-confirmed, the provenance is recorded in the row note. No citation
here is invented; where the project reading is INFERENCE rather than a cited
theorem, the row says so. The point is a precise GAP MAP, not a claim that the
path closes (project stance: barriers are coordinates, not verdicts).

The three questions this ledger answers, from the survey brief:

  Q-LADDER. How far does the Williams connection reach? PROVED at NEXP (Williams
  2011, NEXP not in ACC0) and at NQP (Murray-Williams 2018, the easy-witness
  lemma for NP and NQP; NQP not in ACC-of-THR). It does NOT reach NP. The block
  is NOT a witness-circularity: Murray-Williams 2018 PROVED the NP easy-witness
  lemma, overcoming IKW 2002 (NEXP-only). The connection stops at NQP because the
  only available speedup is a one-layer ACC-of-THR SAT algorithm; an NP-scale
  dense-TC0 SAT algorithm would fire the existing NP easy-witness lemma. So the
  block is the algorithm-plus-diagonalization SCALE (corrected 2026-06-03; the
  dossier A2 "circular descent" kill is outdated).

  Q-JOINTS. The leading-path descent to NP is a SYNTHESIS with several open
  joints, NOT a one-missing-piece program. Four joints: (a) algorithmic (the
  dense THR-of-THR / Max-IP log-shave, findings 20/23/24, a quantitative grind),
  (b) descent (the NQP-to-NP connection, the algorithm + diagonalization scale,
  largely DOWNSTREAM of the algorithmic joint, so J1 and J2 are entangled),
  (c) non-constructivity (a PROVED high-Kt-against-TC0 lower bound, capped at
  AC0[p] by a named wall, a structural barrier, THE binding joint), (d) composition
  (the meta-complexity W2A core relativizes, so it supplies non-naturalness only;
  the spine must supply non-relativization; no combining theorem exists yet). The
  genuinely-independent hard structural barriers are (c) and (d).

  Q-BARRIERS. At the NP rung the grafted ingredient must be
  (non-large-OR-non-constructive) AND non-relativizing AND non-algebrizing. The
  division of labor (findings 12, 25): meta-complexity supplies the
  non-naturalness (via a non-constructive high-Kt object), the Williams spine
  supplies non-relativization + non-algebrization. The COMPOSITION CONCERN, pinned
  by a fixture: the meta-complexity W2A core ALONE relativizes (Hirahara 2018,
  ECCC TR18-138 Section 1.7, verbatim "our proofs do relativize"), so routing the
  non-relativizing content through it is mis-wired.

Run:
    python -m experiments.circuit_complexity.e_leading_path_descent
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from experiments._shared import ProofTechnique, BarrierChecker


# ==========================================================================
# PART 1. The descent ladder. One rung per class: NEXP, NQP, NP.
#
# Each rung records, for the Williams algorithm-to-lower-bound connection:
#   - what the connection ESTABLISHES at that scale (the proved separation, if any),
#   - the three INGREDIENTS the connection consumes and at what scale they hold:
#       (i)   the SAT/CAPP algorithm (the savings that opens the gate structure),
#       (ii)  the easy-witness lemma (the witness-circuit scale),
#       (iii) the diagonalization (the class that is diagonalized against),
#   - the STATUS (proved / partial / open),
#   - the CITATION and its provenance (survey-confirmed vs repo-confirmed).
# ==========================================================================


@dataclass
class LadderRung:
    rung: str                       # NEXP | NQP | NP
    connection_establishes: str     # the separation the connection yields at this scale
    sat_algorithm: str              # the circuit-SAT/CAPP savings the rung consumes
    easy_witness: str               # the easy-witness-lemma scale the rung consumes
    diagonalization: str            # the class diagonalized against
    status: str                     # proved | partial | open
    citation: str                   # named result, venue/year
    provenance: str                 # repo-confirmed | survey-confirmed | inference
    what_blocks_next: str           # what blocks pushing to the next rung down
    note: str = ""

    def check(self) -> None:
        assert self.rung in ("NEXP", "NQP", "NP")
        assert self.status in ("proved", "partial", "open")
        assert self.provenance in ("repo-confirmed", "survey-confirmed", "inference")


def build_ladder() -> List[LadderRung]:
    rungs: List[LadderRung] = []

    # --- RUNG 1: NEXP. Williams 2011. The base of the ladder, fully proved. ---
    rungs.append(LadderRung(
        rung="NEXP",
        connection_establishes="NEXP not in ACC0 (unconditional).",
        sat_algorithm=(
            "A nontrivial #SAT/CAPP algorithm for ACC0 circuits running in time "
            "2^{n - n^{Omega(1)}} (better than 2^n brute force). This is the savings "
            "that opens the gate structure (the non-relativizing ingredient)."
        ),
        easy_witness=(
            "IKW 2002 easy-witness lemma at the NEXP scale: if NEXP is in P/poly "
            "(here in ACC0) then NEXP has witness circuits, i.e. accepting "
            "computations have succinct (circuit) descriptions. Used at the "
            "EXPONENTIAL scale, where it is non-circular."
        ),
        diagonalization=(
            "Against NEXP, via a contradiction with the nondeterministic time "
            "hierarchy: the SAT algorithm plus easy witnesses would give too-fast "
            "NEXP simulation."
        ),
        status="proved",
        citation="Williams, 'Non-Uniform ACC Circuit Lower Bounds', CCC 2011 / JACM 2014.",
        provenance="repo-confirmed",
        what_blocks_next=(
            "Pushing NEXP -> NQP needs the easy-witness lemma and the SAT algorithm "
            "at the quasi-poly-time scale; this was supplied by Murray-Williams 2018 "
            "(next rung), so this step is CLOSED."
        ),
        note=(
            "The base case. Threads all three barriers (LEARNINGS finding 6; encoded "
            "as the williams_acc0 fixture in barriers.py). The non-naturalness here is "
            "by NON-LARGENESS (Williams 2013): the property is 'is this THE hard "
            "function', constructive but not large."
        ),
    ))

    # --- RUNG 2: NQP. Murray-Williams 2018. The first descent step, proved. ---
    rungs.append(LadderRung(
        rung="NQP",
        connection_establishes=(
            "NQP not in n^{log^k n}-size ACC-of-THR (one bottom threshold layer); "
            "upgraded to almost-everywhere and average-case by Chen-Lyu-Williams 2020."
        ),
        sat_algorithm=(
            "Williams's 2014 ACC-of-THR SAT algorithm (one bottom threshold layer), "
            "savings 2^{n - n^{Omega(1)}}. This is the first rung that crosses ONE "
            "threshold layer (the algorithmic frontier of findings 20/23/24)."
        ),
        easy_witness=(
            "The NEW easy-witness lemma of Murray-Williams 2018 for NP and NQP: if "
            "every NP problem has n^k-size circuits then NP verifiers have "
            "n^{O(k^3)}-size witness circuits (analogously for NQP). This is the "
            "load-bearing new theorem of the rung. NOTE: the lemma is STATED for NP "
            "AND NQP, but the CONNECTION (lower bound) is delivered only at NQP, "
            "because the SAT-algorithm-vs-diagonalization scale closes at NQP, not NP."
        ),
        diagonalization=(
            "Against NQP (nondeterministic quasi-polynomial time), via the "
            "quasi-poly nondeterministic time hierarchy."
        ),
        status="proved",
        citation=(
            "Murray, Williams, 'Circuit Lower Bounds for Nondeterministic "
            "Quasi-Polytime: An Easy Witness Lemma for NP and NQP', STOC 2018 / "
            "SIAM J. Comput. 2020 (18M1195887)."
        ),
        provenance="repo-confirmed",
        what_blocks_next=(
            "Pushing NQP -> NP is blocked by the ALGORITHM-plus-DIAGONALIZATION SCALE, "
            "NOT a witness-circularity. CORRECTED 2026-06-03 (the dossier A2 'circular "
            "easy-witness' kill is outdated): Murray-Williams 2018 PROVED the easy-witness "
            "lemma FOR NP (if NP in SIZE[n^k] then NP verifiers have n^{O(k^3)} witness "
            "circuits), overcoming the IKW-2002 NEXP-only barrier, so the NP witness lemma "
            "is NOT missing. The loop closes at NQP because the only available speedup is a "
            "one-bottom-layer ACC-of-THR SAT algorithm (Williams 2014); an NP-scale "
            "dense-TC0 SAT algorithm would fire the EXISTING NP easy-witness lemma. So this "
            "joint is substantially DOWNSTREAM of the algorithmic joint, with a residual "
            "diagonalization-scale question."
        ),
        note=(
            "The connection REACHES NQP, not NP (survey-confirmed against "
            "arXiv/STOC; repo-confirmed in findings 13/20/25). This is the decisive "
            "ladder coordinate: 'TC0 is the first rung' is imprecise. The first "
            "threshold rung (ACC-of-THR, one bottom layer) is already CLIMBED at NQP."
        ),
    ))

    # --- RUNG 3: NP. OPEN. The target a real P vs NP proof needs. ---
    rungs.append(LadderRung(
        rung="NP",
        connection_establishes=(
            "(WOULD establish) NP not in P/poly, or as the first concrete rung "
            "NP not in dense poly-size TC0. NONE of this is proved. The connection "
            "does NOT reach NP."
        ),
        sat_algorithm=(
            "(NEEDED, OPEN) a dense depth-2 THR-of-THR (LTF-of-LTF) SAT/CAPP speedup "
            "2^{n - n^{Omega(1)}}, equivalently the Chen 2018 polylog-dimension "
            "Max-IP log-shave (findings 20/23/24). No known algorithm meets the bar. "
            "This is the ALGORITHMIC joint (a quantitative grind, SETH-consistent)."
        ),
        easy_witness=(
            "ALREADY PROVED for NP (Murray-Williams 2018, n^{O(k^3)} witness circuits), "
            "overcoming IKW 2002 (NEXP-only). So the NP witness lemma is NOT the blocker "
            "(this corrects the dossier A2 'circular descent' kill). The residual DESCENT "
            "joint is the diagonalization-plus-algorithm SCALE: the connection fires at "
            "NQP because the only available speedup is one-layer ACC-of-THR. This joint is "
            "largely DOWNSTREAM of the algorithmic joint, not an independent circularity."
        ),
        diagonalization=(
            "(NEEDED, OPEN) an NP-scale diagonalization. At NP the bespoke non-large "
            "Williams property ('is this THE hard function') is unavailable for a "
            "generic NP target, so the non-naturalness must come from elsewhere "
            "(meta-complexity high-Kt, which is LARGE, so non-natural only if "
            "NON-CONSTRUCTIVE against TC0). That non-constructivity is OPEN (the "
            "NON-CONSTRUCTIVITY joint, capped at AC0[p] by a named wall)."
        ),
        status="open",
        citation=(
            "No theorem. NP not in P/poly and NP not in poly-size TC0 are OPEN as of "
            "June 2026. NP not in poly-size THR-of-THR is OPEN (findings 23/24)."
        ),
        provenance="repo-confirmed",
        what_blocks_next=(
            "This is the bottom of the descent (the P vs NP target). It is blocked by "
            "FOUR joints simultaneously (see the gap ledger): algorithmic, descent, "
            "non-constructivity, composition."
        ),
        note=(
            "The descent to NP is a multi-joint SYNTHESIS, not a one-missing-piece "
            "program. Do NOT encode it as closeable by discharging a single lemma."
        ),
    ))

    return rungs


# ==========================================================================
# PART 2. The gap ledger. The four open joints between the proved rungs and NP.
#
# Each joint carries a KIND (algorithmic / descent / non-constructivity /
# composition), a STATUS (proved / partial / open), and a GRIND-OR-BARRIER
# judgment: is the obstruction a QUANTITATIVE GRIND (a better algorithm or a
# tighter parameter, in principle reachable by current technique families) or a
# STRUCTURAL BARRIER (a named wall current techniques provably cannot cross)?
# ==========================================================================


@dataclass
class GapJoint:
    name: str
    kind: str                       # algorithmic | descent | non-constructivity | composition
    status: str                     # proved | partial | open
    grind_or_barrier: str           # quantitative-grind | structural-barrier | unclear
    the_wall: str                   # the named obstruction, if any
    what_is_proved: str             # the nearest proved result
    what_is_needed: str             # the exact object the descent needs
    provenance: str                 # repo-confirmed | survey-confirmed | inference
    note: str = ""

    def check(self) -> None:
        assert self.kind in (
            "algorithmic", "descent", "non-constructivity", "composition"
        )
        assert self.status in ("proved", "partial", "open")
        assert self.grind_or_barrier in (
            "quantitative-grind", "structural-barrier", "unclear"
        )
        assert self.provenance in (
            "repo-confirmed", "survey-confirmed", "inference"
        )


def build_gap_ledger() -> List[GapJoint]:
    joints: List[GapJoint] = []

    # --- JOINT A: ALGORITHMIC. The dense THR-of-THR / Max-IP log-shave. ---
    joints.append(GapJoint(
        name="The dense THR-of-THR SAT / Max-IP log-shave",
        kind="algorithmic",
        status="open",
        grind_or_barrier="quantitative-grind",
        the_wall=(
            "No named unconditional barrier. The strongest 'hardness of shaving logs' "
            "theorems (Abboud-Hansen-V.Williams-R.Williams 2016; Abboud-Bringmann "
            "2018) are proved only for SEQUENCE/alignment problems and provably do "
            "NOT cover OV / Max-IP (finding 24). The Chen implication runs "
            "shave-implies-lower-bound with no proven converse: a WANTED route, not "
            "an obstruction."
        ),
        what_is_proved=(
            "Best-known integer geometry n^{2 - 1/O(d)} (Matousek 1992; AESW 1991; "
            "Yao 1982), which at polylog d realizes ZERO log-shave; the baseline for "
            "Boolean Max-IP at d = n^eps is already n^2 polylog (Coppersmith 1982 "
            "rectangular matmul). The bar is SETH-CONSISTENT (a log-shave is "
            "n^{2-o(1)}), hence genuinely open, not a SETH refutation (finding 23)."
        ),
        what_is_needed=(
            "A SAT/CAPP speedup 2^{n - n^{Omega(1)}} for dense depth-2 LTF-of-LTF, "
            "equivalently shaving all log^{omega(1)} n factors off the polylog-"
            "dimension Max-IP baseline, computing the max without enumerating the "
            "n^2 pairs (finding 24)."
        ),
        provenance="repo-confirmed",
        note=(
            "Localized and attackable now (findings 20/23/24). A grind: it asks for "
            "a better algorithm within an existing technique family, not for crossing "
            "a proved wall. This is the joint with the clearest near-term handle."
        ),
    ))

    # --- JOINT B: DESCENT. The NQP-to-NP connection (algorithm + diagonalization scale). ---
    joints.append(GapJoint(
        name="The NQP-to-NP connection (algorithm + diagonalization scale)",
        kind="descent",
        status="open",
        grind_or_barrier="structural-barrier",
        the_wall=(
            "The algorithm-plus-diagonalization SCALE, NOT a witness-circularity "
            "(CORRECTED 2026-06-03; the dossier A2 'circular easy-witness' kill is "
            "outdated). Murray-Williams 2018 PROVED the NP easy-witness lemma (n^{O(k^3)} "
            "witness circuits if NP in SIZE[n^k]), overcoming the IKW-2002 NEXP-only "
            "barrier, so the NP witness lemma is NOT missing. The connection delivers its "
            "lower bound only at NQP because the only available speedup is a one-layer "
            "ACC-of-THR SAT algorithm; an NP-scale dense-TC0 SAT algorithm would fire the "
            "EXISTING NP easy-witness lemma. So this joint is largely DOWNSTREAM of the "
            "algorithmic joint; the genuinely-independent residue is the "
            "diagonalization-scale question."
        ),
        what_is_proved=(
            "The connection reaches NQP: Murray-Williams 2018 (NQP not in "
            "ACC-of-THR). The easy-witness lemma is PROVED for NP AND NQP; the "
            "phrase 'can imply circuit lower bounds for NQP, or even NP' is a "
            "CONDITIONAL implication (NP bounds GIVEN an NP-scale SAT algorithm), and the "
            "delivered LOWER BOUND is only at NQP."
        ),
        what_is_needed=(
            "An NP-scale SAT algorithm against a class rich enough (dense TC0 / "
            "THR-of-THR) that the diagonalization lands at NP, fed through the EXISTING "
            "NP easy-witness lemma. The NP witness lemma is already in hand; what is "
            "missing is the algorithm scale (the J1 grind) plus the diagonalization scale."
        ),
        provenance="repo-confirmed",
        note=(
            "Largely DOWNSTREAM of the algorithmic joint J1 (a strong enough NP-scale "
            "dense-TC0 SAT algorithm, not just a one-layer ACC-of-THR shave, would narrow "
            "or close it), with a residual independent diagonalization-scale question. So "
            "the four joints are NOT fully orthogonal: J1 and J2 are entangled on the "
            "algorithm/diagonalization scale, and the genuinely-independent hard "
            "structural barriers are J3 (its own named locality wall) and J4 (no "
            "combining theorem)."
        ),
    ))

    # --- JOINT C: NON-CONSTRUCTIVITY. high-Kt against TC0, capped at AC0[p]. ---
    joints.append(GapJoint(
        name="A proved non-constructivity of high-Kt against TC0",
        kind="non-constructivity",
        status="open",
        grind_or_barrier="structural-barrier",
        the_wall=(
            "Lower bounds on DECIDING MCSP/Kt are PROVABLY CAPPED at AC0[p]: MAJORITY "
            "is in non-uniform poly-size (AC0)^MCSP and NC1 is a subset of "
            "(AC0)^MCSP (Golovnev-Ilango-Impagliazzo-Kabanets-Kolokolova-Tal, ICALP "
            "2019). So a TC0 lower bound on MCSP cannot follow from these techniques "
            "without separating NC1 from AC0. The general form is the LOCALITY "
            "BARRIER (Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam, ITCS 2020 / "
            "JACM 2022): magnification problems have small-fan-in-oracle-gate "
            "circuits and weak-model techniques extend to such circuits, so the two "
            "fail to meet."
        ),
        what_is_proved=(
            "A genuine AC0[p] lower bound on deciding MCSP: depth-d AC0[p] circuits "
            "of size exp(N^{0.49/d}), N = 2^n (Golovnev et al, ICALP 2019). "
            "Non-relativizing NP-hardness of the PARTIAL-function variants MCSP*, "
            "MKTP*, MINKT* and of learning programs, under RANDOMIZED reductions "
            "(Hirahara, FOCS 2022). Conditional worst-case characterizations "
            "(Santhanam 2020 under the Universality Conjecture; Hirahara 2023 under "
            "NP not in io-P/poly, or under subexponentially-secure witness "
            "encryption). Liu-Pass 2020: OWFs iff K^t mildly avg-case hard "
            "(unconditional, but average-case and Minicrypt-scoped, the WRONG axis "
            "for a worst-case TC0 separation)."
        ),
        what_is_needed=(
            "A lower bound showing that DECIDING the high-Kt (or MCSP/MKTP) property "
            "requires large TC0 circuits, for the EXACT total truth tables a generic "
            "NP lower bound would certify, under deterministic poly-time reductions, "
            "unconditionally. None of the proved results is this object. Four upgrades "
            "are each separately open: variant -> exact/total, randomized -> "
            "deterministic, conditional -> unconditional, and (the wall) AC0[p] -> "
            "TC0."
        ),
        provenance="survey-confirmed",
        note=(
            "ASPIRATIONAL, not a discharged lemma. high-Kt is LARGE by Shannon "
            "counting (most truth tables are incompressible), so it can stay "
            "non-natural ONLY by being non-constructive, and the non-constructivity "
            "against TC0 is exactly what the named wall blocks. A builder proposing "
            "'high-Kt hard against TC0' must explain how it evades MAJORITY/NC1 "
            "reducing to MCSP with low-depth oracle gates, or it is non-local "
            "hardness magnification (an unbuilt object the dossier lists for "
            "2044-2047)."
        ),
    ))

    # --- JOINT D: COMPOSITION. The relativizing W2A core. ---
    joints.append(GapJoint(
        name="Composition past the relativization caveat",
        kind="composition",
        status="partial",
        grind_or_barrier="structural-barrier",
        the_wall=(
            "The meta-complexity worst-case-to-average-case (W2A) core RELATIVIZES: "
            "Hirahara 2018 (ECCC TR18-138 Section 1.7) states verbatim 'our proofs "
            "do relativize', and constructs (via Impagliazzo's oracle) a relativized "
            "world where GapMINKT is NOT NP-hard under P/poly-Turing reductions. So "
            "meta-complexity supplies NON-NATURALNESS only, NOT non-relativization."
        ),
        what_is_proved=(
            "The DIVISION OF LABOR is established (findings 12, 25, repo-confirmed): "
            "meta-complexity supplies non-naturalness (via the non-constructive "
            "high-Kt object); the Williams spine supplies non-relativization + "
            "non-algebrization (via the real circuit-SAT algorithm that opens the "
            "gate structure). The fixtures below pin that the W2A core ALONE hits "
            "relativization."
        ),
        what_is_needed=(
            "A graft in which the non-relativizing content is routed through the "
            "spine, NOT through the W2A core, AND in which the spine's non-largeness "
            "escape (unavailable at NP for a generic target) is replaced by the "
            "meta-complexity non-constructivity escape WITHOUT importing the "
            "relativizing W2A reduction as the barrier-clearing ingredient. The "
            "composition is COHERENT in principle (each barrier has an assigned "
            "supplier) but UNBUILT (the suppliers, joints A/B/C, do not yet exist)."
        ),
        provenance="repo-confirmed",
        note=(
            "PARTIAL, not open-from-scratch: the division of labor is a real, "
            "repo-confirmed coordinate. The residual concern is that a construction "
            "could mis-wire the non-relativizing content through the relativizing W2A "
            "core, which the fixtures below catch."
        ),
    ))

    return joints


# ==========================================================================
# PART 3. The NP-scale barrier-evasion bookkeeping.
#
# We reuse experiments/_shared/barriers.py. The grafted NP ingredient must clear
# all three barriers. We encode FOUR ProofTechniques and check them:
#   (1) the meta-complexity W2A core ALONE: HITS relativization (the composition
#       concern, finding 12). Supplies non-naturalness only.
#   (2) the Williams spine ALONE: evades relativization + algebrization, but at NP
#       its non-large escape is unavailable, so by itself it does not supply the
#       NP-scale non-naturalness.
#   (3) the GRAFTED ingredient (spine carries non-relativization/non-algebrization,
#       meta-complexity carries non-naturalness via NON-CONSTRUCTIVITY): the
#       intended NP-scale object. Encoded with natural_largeness=True (high-Kt is
#       large by Shannon counting) and natural_constructivity=False (non-natural
#       ONLY because deciding it is MCSP/MKTP-hard, i.e. the OPEN non-constructivity
#       obligation). The barrier checker reports 'evades all three' BUT this is a
#       CANDIDATE contingent on the open joints, not a discharged separation.
#   (4) a naive NP-scale CONSTRUCTIVE statistic (average sensitivity / approximate
#       degree / spectral norm): LARGE + CONSTRUCTIVE = natural, HITS the
#       natural-proofs barrier. This is the trap a builder must avoid (finding 25).
# ==========================================================================


def metacomplexity_w2a_core_alone() -> ProofTechnique:
    """Hirahara 2018 non-black-box W2A reduction, used as the barrier-clearing core.

    It RELATIVIZES (ECCC TR18-138 Section 1.7 verbatim). Non-black-box does NOT
    mean non-relativizing. So as a standalone barrier-clearing ingredient it is
    DISQUALIFIED. This fixture encodes the composition concern (finding 12).
    """
    return ProofTechnique(
        name="Meta-complexity W2A core alone (Hirahara 2018)",
        relativizes=True,
        natural_largeness=False,
        natural_constructivity=False,
        algebrizes=True,
        notes=(
            "The non-black-box worst-case-to-average-case reduction for GapMINKT "
            "RELATIVIZES (ECCC TR18-138 Section 1.7: 'our proofs do relativize'). "
            "Routing the non-relativizing content through it is mis-wired: it "
            "supplies non-naturalness, never non-relativization."
        ),
    )


def williams_spine_at_np() -> ProofTechnique:
    """The Williams algorithm-to-lower-bound spine, viewed at the NP target.

    Evades relativization (the SAT algorithm opens the gate structure) and we
    record algebrizes=False as the spine's assumed profile (consistent with the
    williams_acc0 base fixture). At NP the spine's non-LARGE escape ('is this THE
    hard function') is UNAVAILABLE for a generic NP target (finding 25), so by
    itself it does not yet supply the NP-scale non-naturalness. We model this by
    marking it NOT natural (largeness False) but flag in the notes that the escape
    is bespoke and unavailable, so the NP non-naturalness must come from the
    meta-complexity graft.
    """
    return ProofTechnique(
        name="Williams spine alone at NP (non-large escape unavailable)",
        relativizes=False,
        natural_largeness=False,        # the bespoke non-large escape (Williams 2013)
        natural_constructivity=True,    # constructivity is unavoidable (Williams 2013)
        algebrizes=False,
        notes=(
            "Non-natural by NON-LARGENESS at NEXP/NQP (Williams 2013: 'is this THE "
            "hard function'). At NP that bespoke property is unavailable for a "
            "generic target (finding 25), so the spine supplies the non-relativizing "
            "+ non-algebrizing content but NOT the NP-scale non-naturalness on its "
            "own. algebrizes=False is the spine's assumed profile, consistent with "
            "the williams_acc0 base fixture (note: algebrization at the dense-TC0 "
            "frontier is NOT-YET-ASSESSABLE, finding 20; here it tracks the spine "
            "template, not a discharged AW verdict)."
        ),
    )


def grafted_np_ingredient() -> ProofTechnique:
    """The intended NP-scale graft: spine + meta-complexity non-constructivity.

    Non-relativization + non-algebrization from the SPINE; non-naturalness from a
    LARGE-but-NON-CONSTRUCTIVE high-Kt object (the meta-complexity contribution).
    natural_largeness=True (Shannon counting: high-Kt is large),
    natural_constructivity=False (non-natural ONLY because deciding high-Kt is
    MCSP/MKTP-hard against TC0, the OPEN obligation of joint C). The checker reports
    'evades all three', BUT this is a CANDIDATE contingent on joints A/B/C/D, not a
    proved separation.
    """
    return ProofTechnique(
        name="Grafted NP ingredient (spine + non-constructive high-Kt)",
        relativizes=False,              # from the spine (the real SAT algorithm)
        natural_largeness=True,         # high-Kt is large by Shannon counting
        natural_constructivity=False,   # OPEN: non-natural only if MCSP/MKTP-hard vs TC0
        algebrizes=False,               # from the spine (assumed profile)
        notes=(
            "CANDIDATE, not discharged. Largeness is True (high-Kt is large), so it "
            "evades natural proofs ONLY via non-constructivity, and that "
            "non-constructivity against TC0 for the exact descent truth tables is "
            "OPEN and capped at AC0[p] (joint C). relativizes/algebrizes=False are "
            "supplied by the spine (joint D division of labor). The 'evades all "
            "three' verdict is contingent on joints A/B/C/D, which are unbuilt."
        ),
    )


def naive_constructive_np_statistic() -> ProofTechnique:
    """The trap: a LARGE + CONSTRUCTIVE NP-scale hardness statistic.

    Average sensitivity, approximate degree, spectral norm: efficiently checkable
    (constructive) and large. By Razborov-Rudich this is NATURAL, and the
    TC0-PRF collision bites it (finding 25). A builder reaching for an efficiently
    checkable descent certificate lands here. The fixture pins the trap.
    """
    return ProofTechnique(
        name="Naive constructive NP statistic (avg sensitivity / approx degree)",
        relativizes=False,
        natural_largeness=True,
        natural_constructivity=True,    # efficiently checkable => natural
        algebrizes=False,
        notes=(
            "LARGE + CONSTRUCTIVE = natural (Razborov-Rudich). The TC0-PRF collision "
            "bites it (finding 25): if dense TC0 computes PRFs, no large+constructive "
            "property separates against it. This is the trap the descent must avoid; "
            "it is WHY a non-constructive object (joint C) is required."
        ),
    )


# ==========================================================================
# Reporting + self-checks.
# ==========================================================================


def _print_ladder(rungs: List[LadderRung]) -> None:
    print("--- DESCENT LADDER: NEXP -> NQP -> NP (Williams connection) ---\n")
    hdr = f"{'rung':<6} | {'status':<8} | {'connection establishes':<58}"
    print(hdr)
    print("-" * len(hdr))
    for r in rungs:
        print(f"{r.rung:<6} | {r.status:<8} | {r.connection_establishes[:58]:<58}")
    print()
    for i, r in enumerate(rungs, 1):
        print(f"[{i}] RUNG {r.rung}  ({r.status.upper()}, {r.provenance})")
        print(f"    establishes : {r.connection_establishes}")
        print(f"    SAT algo    : {r.sat_algorithm}")
        print(f"    easy-witness: {r.easy_witness}")
        print(f"    diagonaliz. : {r.diagonalization}")
        print(f"    citation    : {r.citation}")
        print(f"    blocks next : {r.what_blocks_next}")
        print(f"    note        : {r.note}")
        print()


def _print_gap_ledger(joints: List[GapJoint]) -> None:
    print("--- GAP LEDGER: the four open joints to NP ---\n")
    hdr = (f"{'joint':<44} | {'kind':<19} | {'status':<8} | "
           f"{'grind/barrier':<20}")
    print(hdr)
    print("-" * len(hdr))
    for j in joints:
        print(f"{j.name[:44]:<44} | {j.kind:<19} | {j.status:<8} | "
              f"{j.grind_or_barrier:<20}")
    print()
    for i, j in enumerate(joints, 1):
        print(f"[{chr(64 + i)}] {j.name}")
        print(f"    kind        : {j.kind}   status: {j.status}   "
              f"grind/barrier: {j.grind_or_barrier}   ({j.provenance})")
        print(f"    the wall    : {j.the_wall}")
        print(f"    proved      : {j.what_is_proved}")
        print(f"    needed      : {j.what_is_needed}")
        print(f"    note        : {j.note}")
        print()


def _print_barrier_bookkeeping() -> None:
    print("--- NP-SCALE BARRIER-EVASION BOOKKEEPING (via _shared/barriers.py) ---\n")
    checker = BarrierChecker()
    for t in (
        metacomplexity_w2a_core_alone(),
        williams_spine_at_np(),
        grafted_np_ingredient(),
        naive_constructive_np_statistic(),
    ):
        v = checker.check(t)
        print(v.report())
        print()


def main() -> int:
    print("=== Leading-path descent to NP: descent-ladder ledger ===\n")
    print("This ledger encodes the LITERATURE-GROUNDED STATUS (June 2026) of the")
    print("Williams algorithm-to-lower-bound descent NEXP -> NQP -> NP, not new")
    print("theorems. 'proved' rows cite a named result; 'open'/'partial' rows are")
    print("honest that the object is not a discharged lemma. Barriers are coordinates.\n")

    rungs = build_ladder()
    joints = build_gap_ledger()

    _print_ladder(rungs)
    _print_gap_ledger(joints)
    _print_barrier_bookkeeping()

    # ----------------------------------------------------------------------
    # SELF-CHECKS. Pin the verdict and the proved/open status of each rung/joint.
    # ----------------------------------------------------------------------
    for r in rungs:
        r.check()
    for j in joints:
        j.check()

    nexp, nqp, np_rung = rungs

    # --- (1) Ladder status, pinned. The connection reaches NQP, not NP. ---
    assert nexp.rung == "NEXP" and nexp.status == "proved", \
        "NEXP not in ACC0 is proved (Williams 2011)"
    assert nqp.rung == "NQP" and nqp.status == "proved", \
        "NQP not in ACC-of-THR is proved (Murray-Williams 2018)"
    assert np_rung.rung == "NP" and np_rung.status == "open", \
        "the connection does NOT reach NP: NP not in P/poly (or TC0) is OPEN"
    # Exactly the bottom rung is open; the two upper rungs are proved.
    proved_rungs = [r for r in rungs if r.status == "proved"]
    open_rungs = [r for r in rungs if r.status == "open"]
    assert len(proved_rungs) == 2 and len(open_rungs) == 1, \
        "two proved rungs (NEXP, NQP) and exactly one open rung (NP)"
    assert open_rungs[0].rung == "NP", "the open rung is NP (the P vs NP target)"

    # --- (2) Gap-ledger status, pinned. Four joints, one per kind. ---
    kinds = sorted(j.kind for j in joints)
    assert kinds == ["algorithmic", "composition", "descent", "non-constructivity"], \
        "exactly the four named joints, one of each kind"
    by_kind = {j.kind: j for j in joints}

    # The algorithmic joint is a quantitative GRIND, no named unconditional barrier.
    assert by_kind["algorithmic"].grind_or_barrier == "quantitative-grind", \
        "the dense THR-of-THR / Max-IP log-shave is a grind (no finer unconditional barrier, finding 24)"
    assert by_kind["algorithmic"].status == "open"

    # The descent joint is a structural SCALE constraint (the algorithm +
    # diagonalization scale), largely DOWNSTREAM of the algorithmic joint J1, not
    # a witness-circularity (Murray-Williams 2018 proved the NP easy-witness lemma).
    assert by_kind["descent"].grind_or_barrier == "structural-barrier", \
        "the NQP-to-NP descent is the algorithm/diagonalization scale, entangled with J1"
    assert by_kind["descent"].status == "open"

    # The non-constructivity joint is a structural BARRIER (capped at AC0[p]).
    assert by_kind["non-constructivity"].grind_or_barrier == "structural-barrier", \
        "high-Kt against TC0 is capped at AC0[p] by the MAJORITY/NC1-in-(AC0)^MCSP wall"
    assert by_kind["non-constructivity"].status == "open", \
        "high-Kt-against-TC0 is ASPIRATIONAL (open), not a discharged lemma"

    # The composition joint is PARTIAL (division of labor real; W2A core relativizes).
    assert by_kind["composition"].kind == "composition"
    assert by_kind["composition"].status == "partial", \
        "composition is partial: the division of labor is real, the W2A core relativizes"
    assert by_kind["composition"].grind_or_barrier == "structural-barrier", \
        "the W2A core's relativization is a named structural fact (finding 12)"

    # --- (3) Barrier-evasion bookkeeping, pinned. ---
    checker = BarrierChecker()
    v_w2a = checker.check(metacomplexity_w2a_core_alone())
    v_spine = checker.check(williams_spine_at_np())
    v_graft = checker.check(grafted_np_ingredient())
    v_naive = checker.check(naive_constructive_np_statistic())

    # (3a) The composition concern: the W2A core ALONE HITS relativization.
    assert v_w2a.hits_relativization, \
        "meta-complexity W2A core alone HITS relativization (Hirahara 2018 Sec 1.7): the composition concern"
    assert not v_w2a.evades_all, \
        "the W2A core alone is DISQUALIFIED as a standalone barrier-clearing ingredient"

    # (3b) The spine supplies non-relativization + non-algebrization.
    assert not v_spine.hits_relativization, \
        "the Williams spine evades relativization (the real SAT algorithm opens the gate structure)"
    assert not v_spine.hits_algebrization, \
        "the spine evades algebrization (assumed profile, consistent with williams_acc0 base fixture)"
    # But by itself at NP it is non-natural only by largeness=False (bespoke, unavailable):
    assert not williams_spine_at_np().natural_largeness, \
        "the spine's non-large escape is the bespoke 'is this THE hard function' property"

    # (3c) The grafted NP ingredient evades all three, BUT only as a CANDIDATE:
    #      the non-naturalness rests on the OPEN non-constructivity (largeness=True).
    g = grafted_np_ingredient()
    assert g.natural_largeness and not g.natural_constructivity, \
        "high-Kt is LARGE (Shannon counting); non-natural ONLY via non-constructivity (OPEN, joint C)"
    assert not v_graft.hits_natural_proofs, \
        "the graft evades natural proofs by dropping CONSTRUCTIVITY (large but non-constructive)"
    assert v_graft.evades_all, \
        "the graft evades all three IN THE MODEL, but this is contingent on the open joints A/B/C/D"

    # (3d) The trap: a naive LARGE + CONSTRUCTIVE NP statistic is NATURAL.
    assert v_naive.hits_natural_proofs, \
        "a large+constructive NP hardness statistic is NATURAL (the trap, finding 25)"
    assert not v_naive.evades_all, \
        "the naive constructive statistic is DISQUALIFIED by the natural-proofs barrier"

    # The graft and the naive statistic differ ONLY in constructivity, and that single
    # bit is the whole descent question: large+non-constructive (candidate) vs
    # large+constructive (natural, dead). This pins WHY joint C is load-bearing.
    assert g.natural_largeness == naive_constructive_np_statistic().natural_largeness, \
        "both are large; they differ only in constructivity"
    assert g.natural_constructivity != naive_constructive_np_statistic().natural_constructivity, \
        "the descent hinges on a single bit: non-constructive (candidate) vs constructive (natural/dead)"

    # --- (4) The headline verdict: SEVERAL JOINTS, not one missing piece. ---
    open_or_partial_joints = [j for j in joints if j.status in ("open", "partial")]
    assert len(open_or_partial_joints) == 4, \
        "all four joints are open or partial: the descent is a multi-joint synthesis, NOT one missing piece"
    structural_barriers = [j for j in joints if j.grind_or_barrier == "structural-barrier"]
    grinds = [j for j in joints if j.grind_or_barrier == "quantitative-grind"]
    assert len(grinds) == 1 and grinds[0].kind == "algorithmic", \
        "exactly one joint (algorithmic) is a quantitative grind; the other three are structural"
    assert len(structural_barriers) == 3, \
        "three of the four joints are structural barriers (descent, non-constructivity, composition)"

    # The path does NOT close: at least one rung is open AND at least one joint is a
    # structural barrier. We assert the HONEST verdict, never 'closeable'.
    assert any(r.status == "open" for r in rungs) and len(structural_barriers) >= 1, \
        "HONEST: the descent does not close; the NP rung is open and three joints are structural barriers"

    print("=== Self-check OK ===")
    print("(1) LADDER: the Williams connection is PROVED at NEXP (Williams 2011) and")
    print("    NQP (Murray-Williams 2018); it does NOT reach NP. The NP rung is OPEN.")
    print("(2) GAPS: four joints, one per kind. ALGORITHMIC is a quantitative grind")
    print("    (the dense THR-of-THR / Max-IP log-shave, no finer unconditional")
    print("    barrier). DESCENT (the algorithm+diagonalization scale, downstream of")
    print("    the algorithmic joint: the NP easy-witness lemma is PROVED, Murray-")
    print("    Williams 2018), NON-CONSTRUCTIVITY (high-Kt vs TC0, capped at AC0[p] by")
    print("    the locality wall: the BINDING joint) and COMPOSITION (the W2A core")
    print("    relativizes, no combining theorem yet). Non-constructivity is OPEN/")
    print("    ASPIRATIONAL; composition is PARTIAL (the division of labor is real).")
    print("(3) BARRIERS at NP: the W2A core ALONE hits relativization (composition")
    print("    concern); the spine supplies non-relativization + non-algebrization")
    print("    (the latter NOT YET ASSESSABLE at dense TC0, finding 20); the graft")
    print("    evades all three ONLY as a candidate, resting on the OPEN non-")
    print("    constructivity (high-Kt is LARGE, non-natural only if MCSP-hard vs TC0);")
    print("    a naive large+constructive statistic is NATURAL and dead (finding 25).")
    print("(4) VERDICT: the leading-path descent to NP is a multi-joint SYNTHESIS,")
    print("    NOT a one-missing-piece program. One grind (algorithmic), entangled")
    print("    with the descent scale; two genuinely-independent structural barriers")
    print("    (non-constructivity, the binding one; composition). The path does not")
    print("    close; the joints are coordinates, not a verdict of impossibility.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
