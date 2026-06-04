"""The TC0-PRF collision, and its (non-)effect on the Williams/TC0 route.

HONESTY CAVEAT (read before trusting the PASS counts). The PART 1-5 PASS counts
verify INTERNAL CONSISTENCY of the AND-logic given hand-set largeness/constructivity
flags. They are NOT independent evidence: is_natural is a transparent AND of the
declared flags, so the checks are tautological given the encoding. The mathematical
load is carried by the cited theorems (Williams 2013 Thm 1.1/1.2 that constructivity
is unavoidable and the useful property is non-large; Razborov-Rudich; Hirahara 2018
that the meta-complexity W2A core relativizes), not by the run. PART 2's numerical PRF
distinguisher is an ILLUSTRATION of the largeness mechanism, not a cryptographic proof.

THE QUESTION. The leading path on the Williams spine aims at
NEXP not in dense poly-size TC0 (THR-of-THR) via a circuit-SAT log-shave (the
algorithm-to-lower-bound connection). The project has documented a wall at the
destination: dense poly-size TC0 likely computes strong pseudorandom functions
(Naor-Reingold, JACM 2004; Miles-Viola candidate, JACM 2015; ACW 2016 "seems
likely"; Chen-Tell 2019). The project has propagated this as "natural proofs is
plausibly the BINDING constraint at dense TC0." Does the PRF collision DOOM the
Williams-spine route, or is it EVADED?

THE ANSWER THIS EXPERIMENT ENCODES (verdict: SUBTLE, leaning EVADED). The PRF
collision does NOT, by itself, doom the Williams route. The "binding constraint"
framing is too pessimistic AS STATED: it conflates "any constructive lower-bound
method" with "natural (large AND constructive) method." Razborov-Rudich forbids
a property that is BOTH large AND constructive. The distinguisher that breaks a
PRF is powered by the LARGENESS clause: the property must accept a noticeable
fraction of truly random truth tables (so it separates random from
pseudorandom). The Williams algorithm-to-lower-bound method is non-natural
precisely by DROPPING LARGENESS, not constructivity (Williams 2013, "Natural
Proofs versus Derandomization", STOC 2013 / SICOMP 2016, Theorems 1.1/1.2:
NEXP not in C iff a polynomial-time CONSTRUCTIVE property useful against C
exists, with no largeness requirement; constructivity is unavoidable). A
non-large property carries no distinguishing bias against a PRF, so the collision
is silent on it. The collision therefore DOOMS the natural / combinatorial /
correlation / approximate-degree alternatives (correctly ruling them out), which
is exactly WHY a non-natural method like Williams is the one that can survive.
This is what ACW 2016 and Chen-Tell 2019 actually say: TC0 lower bounds "may
require non-natural proofs."

THE RESIDUAL SUBTLETY (why this is SUBTLE, not cleanly EVADED). There are TWO
distinct, both-valid Razborov-Rudich escapes, and they pull the two levers in
OPPOSITE directions:

  (A) the Williams route: NON-LARGE + constructive (function-specific: certifies
      that one diagonal hard NEXP function has no small C-circuits). Escapes by
      lacking largeness.
  (B) the meta-complexity high-Kt device, needed for the NEXP-to-NP DESCENT:
      LARGE (most truth tables are incompressible, Shannon counting) but
      NON-CONSTRUCTIVE (deciding high Kt is the meta-problem MCSP/MKTP, conjectured
      and partially proven hard). Escapes by lacking constructivity.

At the NEXP-level TC0 bound, the Williams non-largeness (route A) already supplies
non-naturalness for free. Meta-complexity (route B) becomes load-bearing at the
DESCENT toward NP, where the bespoke "is this THE hard function" property is no
longer available. That descent is the single place where a naive replacement (a
LARGE + constructive hardness statistic) WOULD be natural and WOULD collide. So
the live risk is localized at the descent, where route B must carry the
non-naturalness via NON-CONSTRUCTIVITY, and that device is least discharged
(exact MCSP/MKTP non-constructivity against TC0 for the needed truth tables is
open). Meta-complexity also carries a SEPARATE liability: Hirahara's 2018
non-black-box worst-case-to-average-case reduction still RELATIVIZES (ECCC
TR18-138, Section 1.7), so meta-complexity supplies non-NATURALNESS only; the
non-relativizing and non-algebrizing content must come from the Williams spine
(LEARNINGS finding 12).

WHAT THIS MODULE DOES. Five parts, each a self-check that prints PASS/FAIL and
contributes to a single pinned verdict at the end:

  PART 1. Encodes the distinction as ProofTechnique fixtures and runs the SHARED
          BarrierChecker (experiments/_shared/barriers.py) on them: the
          combinatorial / natural TC0 method HITS natural proofs; the Williams
          route (non-large) and the meta-complexity device (non-constructive) do
          NOT, for OPPOSITE reasons.
  PART 2. Models the PRF distinguisher numerically: makes the LARGENESS threshold
          the load-bearing distinction. A large property is a distinguisher (it
          accepts ~ a constant fraction of random truth tables but rejects the
          PRF's pseudorandom ones, giving non-negligible advantage); a non-large
          property is not (it accepts a vanishing fraction of random tables, so it
          cannot tell random from pseudorandom). Computes the distinguishing
          advantage as a function of the property's largeness.
  PART 3. Encodes the division of labor (finding 12): the combined dense-TC0
          profile (non-relativizing + non-large-non-natural + non-algebrizing)
          evades all three, like williams_acc0; the SAT algorithm is split off
          (it carries no largeness attribute) from the certified property (which
          does).
  PART 4. Localizes the descent: shows that a LARGE + constructive replacement
          statistic at the NEXP-to-NP step is killed by the PRF assumption, while
          the non-constructive high-Kt route is not. Pins where naturalness could
          re-enter.
  PART 5. Pins the verdict and the framing correction.

Dependencies: standard library only, plus experiments/_shared (the shared
ProofTechnique / BarrierChecker). Does NOT mutate barriers.py: it builds its own
local fixtures so the 5/5 smoke test stays invariant.

PROVED vs INFERENCE. Citations in the fixture notes mark what is a theorem
(venue/year) versus project inference. The numerical PRF model in PART 2 is an
ILLUSTRATION of the Razborov-Rudich distinguisher mechanism, not a proof; it
makes the largeness-is-load-bearing point concrete and checkable, it does not
certify any cryptographic claim. PRFs in TC0 are conditional (Naor-Reingold under
factoring/DDH; Miles-Viola is a CANDIDATE), so the collision is itself
conditional, which is a further reason it does not unconditionally doom anything.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, List, Tuple

from experiments._shared import BarrierChecker, ProofTechnique


# ---------------------------------------------------------------------------
# Local fixtures. These are NOT added to the shared BARRIERS dict, so the
# canonical smoke test (5/5) is untouched. Each encodes a published profile.
# ---------------------------------------------------------------------------

def combinatorial_tc0_method() -> ProofTechnique:
    """A natural / combinatorial TC0 lower-bound method.

    The correlation / approximate-degree / polynomial-method family treated as a
    STANDALONE lower-bound certificate: a property of truth tables that is LARGE
    (most hard functions have high average sensitivity / high approximate degree)
    and CONSTRUCTIVE (computable from the 2^n-bit table in poly(2^n) time). This
    is exactly the natural-proofs profile (cf. the e_largeness_constructivity
    Property 1, and the e_acc0 polynomial-method experiment). Against dense TC0
    (which likely computes PRFs) it is DEFINITIVELY blocked: a large + constructive
    property useful against a class that computes strong PRFs is a distinguisher,
    contradicting the PRF (Razborov-Rudich 1994; the CIKK 2016 learning
    equivalence; Santhanam 2020).
    """
    return ProofTechnique(
        name="Combinatorial / natural TC0 method (correlation, approx-degree)",
        relativizes=False,             # opens the circuit (polynomial method)
        natural_largeness=True,        # most hard functions satisfy it
        natural_constructivity=True,   # computable from the truth table in poly(2^n)
        algebrizes=False,
        notes=(
            "Large + constructive = NATURAL (Razborov-Rudich 1994). Useful against "
            "a class that computes strong PRFs, it is a distinguisher and breaks the "
            "PRF, which is impossible. So at dense TC0 (Naor-Reingold JACM 2004; "
            "Miles-Viola candidate JACM 2015; ACW 2016 'seems likely') this family "
            "is DEFINITIVELY blocked. This is the binding constraint on the NATURAL "
            "ALTERNATIVES, which is why a non-natural method is required."
        ),
    )


def williams_tc0_route() -> ProofTechnique:
    """The Williams algorithm-to-lower-bound route, generalized ACC0 -> TC0.

    Non-natural by dropping LARGENESS, not constructivity. Williams 2013
    (STOC 2013 / SICOMP 2016, Thm 1.1/1.2): NEXP not in C iff there is a
    polynomial-time CONSTRUCTIVE property useful against C; constructivity is
    unavoidable, the useful property is true of essentially ONE diagonal hard
    function (at-least-one, not a 1/2^{O(n)} fraction), so it is NON-LARGE. A
    non-large property is invisible to the PRF distinguisher, so the TC0-PRF
    collision does NOT block it.

    NOTE on the field values. We set natural_constructivity=True here, which is
    the precise Williams 2013 reading (constructivity is unavoidable). The shared
    williams_acc0 fixture sets natural_constructivity=False; that is slightly
    over-strong but its VERDICT is identical, because is_natural requires BOTH
    clauses and natural_largeness=False already clears the barrier. We flag the
    cosmetic fixture-comment fix in the verdict, we do not mutate the shared
    fixture (the 5/5 smoke test is invariant either way).
    """
    return ProofTechnique(
        name="Williams algorithm-to-lower-bound route (NEXP not in TC0)",
        relativizes=False,             # a real SAT algorithm opens the gate structure
        natural_largeness=False,       # function-specific: true of ONE diagonal function
        natural_constructivity=True,   # Williams 2013: constructivity is UNAVOIDABLE
        algebrizes=False,              # the SAT-algorithm spine is non-algebrizing
        notes=(
            "Non-natural by dropping LARGENESS, not constructivity (Williams 2013, "
            "STOC 2013 / SICOMP 2016, Thm 1.1/1.2: constructivity is unavoidable; the "
            "useful property is non-large). A non-large property is not a PRF "
            "distinguisher, so the TC0-PRF collision is SILENT on it. Evades the same "
            "way williams_acc0 does, via the non-largeness clause."
        ),
    )


def metacomplexity_high_kt() -> ProofTechnique:
    """The meta-complexity high-Kt device for the NEXP-to-NP descent.

    The OTHER Razborov-Rudich escape, pulling the opposite lever. The certifying
    property is "this truth table has high Kt / circuit complexity." It is LARGE:
    almost all truth tables are incompressible (Shannon counting). Being large, it
    can only escape Razborov-Rudich by being NON-CONSTRUCTIVE, i.e. deciding it is
    the meta-problem MCSP/MKTP, conjectured and partially proven hard (Hirahara
    2022, FOCS 2022: partial/restricted MCSP variants are NP-hard non-relativizingly;
    exact single-output MCSP under deterministic reductions is open). This is the
    device the leading path proposes for the descent, where the Williams bespoke
    non-large property is no longer available.

    Honest caveat (finding 12): meta-complexity supplies non-NATURALNESS only.
    Hirahara's 2018 non-black-box W2A reduction still RELATIVIZES (ECCC TR18-138,
    Section 1.7). So if a technique leaned on the W2A core for its barrier-clearing
    content it would still hit relativization. We model the HONEST grafted version:
    meta-complexity for non-naturalness, the Williams spine for
    non-relativization / non-algebrization.
    """
    return ProofTechnique(
        name="Meta-complexity high-Kt device (descent engine)",
        relativizes=False,             # ONLY when grafted onto the Williams spine
        natural_largeness=True,        # most truth tables are incompressible (Shannon)
        natural_constructivity=False,  # deciding high Kt is MCSP/MKTP-hard
        algebrizes=False,              # supplied by the spine, not the W2A core
        notes=(
            "LARGE but NON-CONSTRUCTIVE: the opposite Razborov-Rudich escape from "
            "Williams. Escapes natural proofs via the non-constructivity clause "
            "(deciding high Kt is MCSP/MKTP-hard). Caveat (finding 12): the W2A core "
            "RELATIVIZES (Hirahara 2018, ECCC TR18-138 1.7); non-relativization must "
            "come from the Williams spine. relativizes=False holds ONLY for the "
            "grafted-onto-spine version modeled here."
        ),
    )


def metacomplexity_w2a_core_alone() -> ProofTechnique:
    """The meta-complexity W2A core WITHOUT the Williams spine (the honest no-go).

    Finding 12 made concrete: if the barrier-clearing ingredient is Hirahara's
    non-black-box worst-case-to-average-case reduction core BY ITSELF, it still
    RELATIVIZES (ECCC TR18-138, Section 1.7; Impagliazzo's oracle A). So
    "non-black-box" is NOT "non-relativizing." This fixture HITS relativization, to
    pin that meta-complexity alone does not clear the spine's barriers.
    """
    return ProofTechnique(
        name="Meta-complexity W2A core alone (no Williams spine)",
        relativizes=True,              # Hirahara 2018, Section 1.7: "our proofs do relativize"
        natural_largeness=True,
        natural_constructivity=False,
        algebrizes=True,               # arithmetizing local-list-decoding core
        notes=(
            "Hirahara 2018 (ECCC TR18-138, Section 1.7): the non-black-box W2A "
            "reduction's proofs RELATIVIZE; Impagliazzo's oracle A blocks GapMINKT "
            "NP-hardness relative to A. Non-black-box != non-relativizing. The "
            "arithmetizing core also algebrizes. So the W2A core ALONE is "
            "disqualified; it supplies non-naturalness only, the spine must supply "
            "the rest. This is the finding-12 repair, encoded as a no-go fixture."
        ),
    )


def descent_naive_large_statistic() -> ProofTechnique:
    """The naive (wrong) descent: replace the bespoke property by a LARGE statistic.

    At the NEXP-to-NP descent the Williams non-large "is this THE function"
    property is unavailable for a generic NP target. The TEMPTING but WRONG
    replacement is a large + constructive hardness statistic (average sensitivity,
    spectral norm, approximate degree of the NP-witness function). That is natural
    and is killed by the TC0-PRF assumption. This fixture exists to show the
    checker correctly flags the WRONG descent as blocked, isolating WHY the
    descent must use the non-constructive high-Kt route instead.
    """
    return ProofTechnique(
        name="Naive descent: large+constructive hardness statistic at NP",
        relativizes=False,
        natural_largeness=True,        # a generic hardness statistic is large
        natural_constructivity=True,   # and computable from the truth table
        algebrizes=False,
        notes=(
            "The wrong way to do the descent. A large + constructive replacement "
            "for the Williams bespoke property is NATURAL and collides with the "
            "TC0-PRF. This is the precise re-entry point for naturalness, and the "
            "reason the descent must use the non-constructive high-Kt route "
            "(metacomplexity_high_kt) instead."
        ),
    )


# ---------------------------------------------------------------------------
# PART 2. The PRF distinguisher, modeled numerically.
#
# Razborov-Rudich mechanism: a property Phi useful against C, applied as a test,
# breaks a PRF family in C iff it distinguishes truly-random truth tables from
# the PRF's outputs. A truly random function does NOT have small C-circuits (w.h.p.),
# so a USEFUL Phi (which rejects every small-C-circuit function) tends to ACCEPT
# random functions and tends to REJECT PRF outputs (which DO have small C-circuits).
# The distinguishing ADVANTAGE is roughly
#     | Pr[Phi accepts random] - Pr[Phi accepts PRF output] |.
# Pr[Phi accepts random] is exactly the property's LARGENESS. Pr[Phi accepts PRF
# output] is ~0 for a useful Phi (PRF outputs have small circuits, which Phi
# rejects). So advantage ~ largeness. LARGE -> noticeable advantage -> breaks the
# PRF (impossible if the PRF is secure). NON-LARGE -> negligible advantage -> no
# break. This is the load-bearing computation: the threshold is largeness.
# ---------------------------------------------------------------------------

def distinguishing_advantage(largeness: float, prf_acceptance: float = 0.0) -> float:
    """Razborov-Rudich distinguishing advantage of a USEFUL property.

    Args:
        largeness: Pr[Phi accepts a uniformly random truth table]. This is the
            Razborov-Rudich largeness fraction.
        prf_acceptance: Pr[Phi accepts a PRF output]. For a USEFUL property this
            is ~0, because PRF outputs have small C-circuits and a useful property
            rejects every small-C-circuit function.

    Returns:
        The distinguishing advantage |largeness - prf_acceptance|. A PRF secure
        against the test class is broken iff this is non-negligible.
    """
    return abs(largeness - prf_acceptance)


def breaks_prf(largeness: float, negligible: float) -> bool:
    """Does a useful property with this largeness break a strong PRF?

    Yes iff its distinguishing advantage exceeds the negligibility threshold.
    Large properties break the PRF (the collision); non-large ones do not.
    """
    return distinguishing_advantage(largeness) > negligible


# ---------------------------------------------------------------------------
# Numerical largeness measurement (reused idea from e_largeness_constructivity).
# Confirms: a combinatorial statistic is genuinely LARGE on random truth tables,
# while a function-specific property is genuinely NON-LARGE (vanishing fraction).
# ---------------------------------------------------------------------------

def random_tt(n: int, rng: random.Random) -> Tuple[int, ...]:
    return tuple(1 if rng.random() < 0.5 else 0 for _ in range(1 << n))


def average_sensitivity(tt: Tuple[int, ...], n: int) -> float:
    N = 1 << n
    sensitive = 0
    for x in range(N):
        for i in range(n):
            if tt[x] != tt[x ^ (1 << i)]:
                sensitive += 1
    return sensitive / N


def measure_largeness(prop: Callable[[Tuple[int, ...]], bool], n: int, samples: int, rng: random.Random) -> float:
    hits = sum(1 for _ in range(samples) if prop(random_tt(n, rng)))
    return hits / samples


# ---------------------------------------------------------------------------
# Self-check harness.
# ---------------------------------------------------------------------------

@dataclass
class Check:
    label: str
    ok: bool
    info: str = ""


def emit(checks: List[Check]) -> bool:
    all_ok = True
    for c in checks:
        status = "PASS" if c.ok else "FAIL"
        suffix = f" - {c.info}" if c.info else ""
        print(f"  [{status}] {c.label}{suffix}")
        all_ok = all_ok and c.ok
    return all_ok


def part1_barrier_profiles() -> bool:
    print("PART 1. Barrier profiles via the SHARED BarrierChecker")
    print("  (combinatorial method HITS natural proofs; Williams + meta-complexity")
    print("   evade it, for OPPOSITE reasons.)")
    checker = BarrierChecker()

    comb_t = combinatorial_tc0_method()
    will_t = williams_tc0_route()
    meta_t = metacomplexity_high_kt()
    comb = checker.check(comb_t)
    will = checker.check(will_t)
    meta = checker.check(meta_t)

    checks = [
        Check("combinatorial TC0 method HITS natural proofs (large + constructive)",
              comb.hits_natural_proofs),
        Check("combinatorial method is DISQUALIFIED (the PRF collision bites it)",
              not comb.evades_all),
        Check("Williams route EVADES natural proofs (non-large)",
              not will.hits_natural_proofs),
        Check("Williams route evades via NON-LARGENESS (constructive but small)",
              (not will_t.natural_largeness) and will_t.natural_constructivity),
        Check("meta-complexity device EVADES natural proofs (non-constructive)",
              not meta.hits_natural_proofs),
        Check("meta-complexity evades via NON-CONSTRUCTIVITY (large but non-constructive)",
              meta_t.natural_largeness and (not meta_t.natural_constructivity)),
        Check("the two escapes pull OPPOSITE levers (largeness vs constructivity)",
              (will_t.natural_largeness != meta_t.natural_largeness)
              and (will_t.natural_constructivity != meta_t.natural_constructivity)),
    ]
    ok = emit(checks)
    print()
    print("  Williams route reasons (should cite the non-largeness escape):")
    for r in will.reasons:
        print(f"    . {r}")
    print("  Meta-complexity reasons (should cite the non-constructivity escape):")
    for r in meta.reasons:
        print(f"    . {r}")
    print()
    return ok


def part2_prf_distinguisher() -> bool:
    print("PART 2. The PRF distinguisher: LARGENESS is the load-bearing threshold")
    print("  advantage ~ Pr[Phi accepts random] - Pr[Phi accepts PRF output].")
    print("  For a USEFUL Phi the second term ~ 0 (PRF outputs have small circuits,")
    print("  which a useful property rejects), so advantage ~ largeness.\n")

    negligible = 1e-3  # a stand-in negligibility threshold for the illustration

    rng = random.Random(2025)
    # Empirically confirm a combinatorial statistic is LARGE on random tables.
    n = 4
    comb_prop = lambda tt: average_sensitivity(tt, n) > n / 2.0
    comb_largeness = measure_largeness(comb_prop, n, samples=600, rng=rng)
    # And a function-specific property is NON-LARGE (1 / 2^{2^n}).
    target = random_tt(n, rng)
    eq_prop = lambda tt: tt == target
    eq_largeness = measure_largeness(eq_prop, n, samples=4000, rng=rng)
    eq_exact = 1.0 / (1 << (1 << n))

    print(f"{'property':<46} {'largeness':>12} {'advantage':>11} {'breaks PRF?':>12}")
    rows = [
        ("combinatorial (avg-sensitivity > n/2), measured", comb_largeness),
        ("Williams non-large (= one function), measured", eq_largeness),
        ("Williams non-large (= one function), exact 1/2^(2^n)", eq_exact),
        ("meta-complexity high-Kt (large, NON-constructive)", 0.99),
    ]
    for label, large in rows:
        adv = distinguishing_advantage(large)
        # The meta-complexity row is large but NON-constructive: it cannot be run
        # as an efficient test at all, so it is not a distinguisher despite being
        # large. We annotate that explicitly below.
        if label.startswith("meta-complexity"):
            verdict = "n/a (not constructive: cannot run as a test)"
        else:
            verdict = "YES (collision)" if breaks_prf(large, negligible) else "no (safe)"
        print(f"{label:<46} {large:>12.6f} {adv:>11.6f} {verdict:>12}")

    print()
    checks = [
        Check("combinatorial statistic is genuinely LARGE on random tables",
              comb_largeness >= 0.1, f"measured {comb_largeness:.3f}"),
        Check("the LARGE property breaks the PRF (collision: advantage non-negligible)",
              breaks_prf(comb_largeness, negligible)),
        Check("function-specific property is genuinely NON-LARGE",
              eq_largeness <= 1e-2, f"measured {eq_largeness:.6f}, exact {eq_exact:.2e}"),
        Check("the NON-LARGE property does NOT break the PRF (advantage negligible)",
              not breaks_prf(eq_largeness, negligible)),
        Check("largeness is the threshold: same usefulness, opposite PRF verdict",
              breaks_prf(comb_largeness, negligible) and not breaks_prf(eq_largeness, negligible)),
        Check("meta-complexity high-Kt is large but NON-constructive, so it is not a runnable distinguisher",
              True, "non-constructivity, not non-largeness, is its escape"),
    ]
    ok = emit(checks)
    print("  -> The PRF collision is a LARGENESS phenomenon. Dropping largeness")
    print("     (Williams) or dropping constructivity (meta-complexity) both escape;")
    print("     keeping both (combinatorial) is what collides.\n")
    return ok


def part3_division_of_labor() -> bool:
    print("PART 3. Division of labor (finding 12): the combined dense-TC0 profile")
    print("  evades all three, like williams_acc0. The SAT algorithm carries NO")
    print("  largeness attribute; only the certified property does.\n")
    checker = BarrierChecker()

    will = checker.check(williams_tc0_route())
    w2a_alone = checker.check(metacomplexity_w2a_core_alone())

    checks = [
        Check("Williams TC0 route evades RELATIVIZATION (real SAT algorithm opens gates)",
              not will.hits_relativization),
        Check("Williams TC0 route evades NATURAL PROOFS (non-large)",
              not will.hits_natural_proofs),
        Check("Williams TC0 route evades ALGEBRIZATION",
              not will.hits_algebrization),
        Check("combined dense-TC0 profile EVADES ALL THREE (like williams_acc0)",
              will.evades_all),
        Check("meta-complexity W2A core ALONE still HITS relativization (Hirahara 2018 1.7)",
              w2a_alone.hits_relativization),
        Check("so non-black-box is NOT non-relativizing: the spine supplies that, not the W2A core",
              not w2a_alone.evades_all),
    ]
    ok = emit(checks)
    print()
    print("  Algorithm vs certified property (the separation finding 12 / note 6 flag):")
    print("    - SAT / Max-IP log-shave + structure lemmas: ALGORITHMS, not truth-table")
    print("      properties. They carry NO largeness attribute and cannot reintroduce")
    print("      naturalness. They are relativization-relevant, naturalness-irrelevant.")
    print("    - The property the completed proof certifies: this is the only object with")
    print("      a largeness status, and Williams 2013 makes it non-large.")
    print()
    return ok


def part4_descent_localization() -> bool:
    print("PART 4. Descent localization: WHERE naturalness could re-enter (NEXP -> NP)")
    print("  The Williams bespoke non-large property is unavailable for a generic NP")
    print("  target. A naive LARGE+constructive replacement is killed by the PRF; the")
    print("  non-constructive high-Kt route is not.\n")
    checker = BarrierChecker()

    naive = checker.check(descent_naive_large_statistic())
    meta_t = metacomplexity_high_kt()
    meta = checker.check(meta_t)

    checks = [
        Check("naive descent (large+constructive statistic) HITS natural proofs",
              naive.hits_natural_proofs),
        Check("naive descent is DISQUALIFIED at dense TC0 (PRF collision bites)",
              not naive.evades_all),
        Check("non-constructive high-Kt descent EVADES natural proofs",
              not meta.hits_natural_proofs),
        Check("so the descent must drop CONSTRUCTIVITY (high-Kt is large), not largeness",
              meta_t.natural_largeness and not meta_t.natural_constructivity),
    ]
    ok = emit(checks)
    print()
    print("  HONEST status of the descent (the genuine open subtlety):")
    print("    - At the NEXP-level TC0 bound, Williams non-largeness suffices; meta-")
    print("      complexity is NOT needed there.")
    print("    - At the descent toward NP, the non-constructive high-Kt route is the")
    print("      candidate, and it is LEAST discharged: exact MCSP/MKTP non-constructivity")
    print("      against TC0 for the needed truth tables is OPEN. Partial / restricted")
    print("      variants are NP-hard non-relativizingly (Hirahara 2022, FOCS 2022); the")
    print("      exact object is not. So 'proved-not-assumed non-constructivity' is")
    print("      PARTIAL, not a theorem for the descent's exact truth tables.")
    print()
    return ok


def part5_verdict() -> bool:
    print("PART 5. Pinned verdict and framing correction")
    checks = [
        Check("the combinatorial / natural method IS blocked by the PRF collision",
              not BarrierChecker().check(combinatorial_tc0_method()).evades_all),
        Check("the non-large Williams route is NOT blocked by the PRF collision",
              BarrierChecker().check(williams_tc0_route()).evades_all),
        Check("the 'binding constraint dooms the Williams route' framing is TOO PESSIMISTIC",
              # It is too pessimistic iff the Williams route evades and the combinatorial
              # one does not: the collision binds the alternatives, not the leading path.
              BarrierChecker().check(williams_tc0_route()).evades_all
              and not BarrierChecker().check(combinatorial_tc0_method()).evades_all),
    ]
    ok = emit(checks)
    print()
    print("  VERDICT: SUBTLE, leaning EVADED.")
    print("  - The TC0-PRF collision DOOMS the LARGE+constructive (natural / combinatorial")
    print("    / correlation / approximate-degree) alternatives. Correct, and that is")
    print("    exactly WHY a non-natural method is required (ACW 2016, Chen-Tell 2019:")
    print("    TC0 lower bounds 'may require non-natural proofs').")
    print("  - The Williams algorithm-to-lower-bound route is non-natural by DROPPING")
    print("    LARGENESS, not constructivity (Williams 2013, STOC 2013 / SICOMP 2016,")
    print("    Thm 1.1/1.2). A non-large property is invisible to the PRF distinguisher,")
    print("    so the collision is SILENT on the leading path. NOT doomed.")
    print("  - The 'natural proofs is the BINDING constraint at dense TC0' framing is")
    print("    too pessimistic AS STATED: it binds the natural ALTERNATIVES, which is the")
    print("    REASON the non-natural Williams route is needed, not an obstruction to it.")
    print("  - RESIDUAL SUBTLETY (why not cleanly EVADED): the NEXP-to-NP descent. There")
    print("    the bespoke non-large property is gone; the candidate is the LARGE but")
    print("    NON-CONSTRUCTIVE high-Kt device, whose non-constructivity against TC0 for")
    print("    the exact truth tables is OPEN, and whose W2A core RELATIVIZES (finding 12,")
    print("    Hirahara 2018), so non-relativization must come from the spine.")
    print()
    print("  PROPOSED FRAMING CORRECTION (returned for SYNTHESIZER, not applied here):")
    print("    Replace 'natural proofs is plausibly the BINDING constraint at dense TC0'")
    print("    with 'the TC0-PRF collision binds the LARGE+constructive (combinatorial)")
    print("    alternatives, which is WHY a non-natural method is required; the Williams")
    print("    route is non-natural by dropping LARGENESS (Williams 2013 Thm 1.1/1.2), so")
    print("    the collision does NOT bind the leading path. Natural proofs on the leading")
    print("    path: CONDITIONALLY EVADED via non-largeness. The genuinely binding open")
    print("    obstruction is the ALGORITHMIC one (the dense THR-of-THR SAT/Max-IP log-")
    print("    shave, findings 20/23/24), plus the not-yet-assessable algebrization flag,")
    print("    plus the descent's non-constructivity question.'")
    print()
    return ok


def main() -> int:
    print("=" * 78)
    print("The TC0-PRF collision and the Williams/TC0 route")
    print("Does dense-TC0 computing PRFs DOOM the leading path, or is it EVADED?")
    print("=" * 78)
    print()

    results = [
        part1_barrier_profiles(),
        part2_prf_distinguisher(),
        part3_division_of_labor(),
        part4_descent_localization(),
        part5_verdict(),
    ]

    n_pass = sum(results)
    print("=" * 78)
    print(f"Self-checks: {n_pass}/{len(results)} parts passed")
    print("=" * 78)
    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
