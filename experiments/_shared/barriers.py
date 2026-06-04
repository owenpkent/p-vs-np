"""The three-barrier wrong-approach detector.

This is the P-vs-NP analog of the Davenport-Heilbronn discipline in the
companion Riemann Hypothesis repo. There, a single contrived L-function with a
known off-line zero falsifies any method that cannot distinguish it from zeta.
Here the discipline is enforced by three published *barrier theorems*, each of
which proves that a whole class of proof techniques cannot resolve P vs NP:

  1. Relativization (Baker, Gill, Solovay 1975). There are oracles A, B with
     P^A = NP^A and P^B != NP^B. Any proof that relativizes (goes through for
     all oracles) would have to settle the question both ways at once, which is
     impossible. So a relativizing technique cannot separate P from NP, and
     cannot collapse them either.

  2. Natural proofs (Razborov, Rudich 1994). If a circuit lower bound is proved
     via a property of Boolean functions that is "large" (holds for a constant
     fraction of all functions) and "constructive" (decidable in time
     polynomial in the 2^n-bit truth table), then that property breaks
     sufficiently strong pseudorandom generators. Under the widely believed
     assumption that such generators exist (e.g. from the hardness of
     factoring/discrete log), no natural property can prove super-polynomial
     lower bounds against P/poly. So a natural technique cannot separate.

  3. Algebrization (Aaronson, Wigderson 2008). Extend relativization so the
     oracle is also available as a low-degree polynomial extension over a field.
     They show all then-known techniques "algebrize," and that algebrizing
     techniques cannot resolve P vs NP (there are algebraic oracles forcing the
     answer each way). Arithmetization (the technique behind IP = PSPACE and
     MIP = NEXP) is non-relativizing but still algebrizing.

A technique that has any hope of resolving P vs NP must evade ALL THREE. The
checker below reports, for a `ProofTechnique`, which barriers it hits and
whether it is therefore disqualified by current knowledge. A clean pass is
necessary, not sufficient: it means only that the three known no-go theorems do
not immediately rule the technique out. Williams's 2011 NEXP-not-in-ACC0 proof
is the canonical example of a technique that threads all three (see the
circuit_complexity experiment writeup).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .technique import ProofTechnique


@dataclass
class BarrierVerdict:
    """Result of running the barrier checker on one technique."""

    technique_name: str
    hits_relativization: bool
    hits_natural_proofs: bool
    hits_algebrization: bool
    reasons: List[str]

    @property
    def evades_all(self) -> bool:
        """True iff the technique evades all three known barriers."""
        return not (
            self.hits_relativization
            or self.hits_natural_proofs
            or self.hits_algebrization
        )

    def report(self) -> str:
        lines = [f"Technique: {self.technique_name}"]
        lines.append(f"  relativization barrier : {'HIT' if self.hits_relativization else 'evaded'}")
        lines.append(f"  natural-proofs barrier : {'HIT' if self.hits_natural_proofs else 'evaded'}")
        lines.append(f"  algebrization barrier  : {'HIT' if self.hits_algebrization else 'evaded'}")
        for r in self.reasons:
            lines.append(f"    - {r}")
        verdict = "EVADES ALL THREE (necessary, not sufficient)" if self.evades_all else "DISQUALIFIED by a known barrier"
        lines.append(f"  verdict: {verdict}")
        return "\n".join(lines)


class BarrierChecker:
    """The wrong-approach detector for P vs NP lower-bound techniques.

    Usage:
        checker = BarrierChecker()
        verdict = checker.check(technique)
        print(verdict.report())

    The logic is deliberately transparent. Each barrier is hit exactly when the
    corresponding property of the technique holds, with the natural-proofs case
    requiring both largeness and constructivity (the definition of a "natural"
    property). The reasons list records the specific clause that fired, so the
    output is an audit trail, not a verdict from nowhere.
    """

    def check(self, t: ProofTechnique) -> BarrierVerdict:
        reasons: List[str] = []

        hits_rel = t.relativizes
        if hits_rel:
            reasons.append(
                "relativizes: there exist oracles A, B with P^A=NP^A and P^B!=NP^B "
                "(Baker-Gill-Solovay 1975), so a relativizing argument cannot decide P vs NP."
            )

        hits_nat = t.is_natural
        if hits_nat:
            reasons.append(
                "natural (large + constructive): such a property would break strong "
                "pseudorandom generators (Razborov-Rudich 1994), contradicting the standard "
                "cryptographic hardness assumption."
            )
        else:
            if t.natural_largeness and not t.natural_constructivity:
                reasons.append(
                    "uses a large but non-constructive property: evades natural proofs only "
                    "if the non-constructivity is essential (cf. Williams's algebraic / "
                    "non-constructive ingredient)."
                )
            if t.natural_constructivity and not t.natural_largeness:
                reasons.append(
                    "uses a constructive but small (function-specific) property: evades the "
                    "largeness clause, which is the standard way out (a property true of the "
                    "hard function but rare among all functions)."
                )

        hits_alg = t.algebrizes
        if hits_alg:
            reasons.append(
                "algebrizes: goes through under low-degree oracle extensions, so by "
                "Aaronson-Wigderson 2008 it cannot resolve P vs NP."
            )

        return BarrierVerdict(
            technique_name=t.name,
            hits_relativization=hits_rel,
            hits_natural_proofs=hits_nat,
            hits_algebrization=hits_alg,
            reasons=reasons,
        )


# A small library of canonical techniques, encoded against the published record.
# These double as regression fixtures for the smoke test: each entry's barrier
# profile is a documented fact about the corresponding result.
BARRIERS = {
    "diagonalization": ProofTechnique(
        name="Pure diagonalization / simulation (time hierarchy style)",
        relativizes=True,
        natural_largeness=False,
        natural_constructivity=False,
        algebrizes=True,
        notes=(
            "Hierarchy theorems relativize: the simulation treats the machine as a "
            "black box, so it goes through with any oracle. Hence it cannot separate "
            "P from NP (BGS). This is why diagonalization alone is known to be "
            "insufficient."
        ),
    ),
    "razborov_monotone": ProofTechnique(
        name="Razborov 1985 monotone circuit lower bound for clique",
        # Monotone lower bounds do not relativize (they open the circuit), but the
        # method of approximations is large + constructive, so it is a natural
        # proof. It does not contradict the barrier because it proves a bound only
        # against MONOTONE circuits, where no pseudorandom generators are claimed.
        relativizes=False,
        natural_largeness=True,
        natural_constructivity=True,
        algebrizes=False,
        notes=(
            "A natural proof in the Razborov-Rudich sense. It does not violate the "
            "barrier because the natural-proofs theorem is about general (non-monotone) "
            "circuits; monotone pseudorandom generators are not assumed. This is the "
            "textbook example that naturalness is a real, common phenomenon."
        ),
    ),
    "arithmetization_ip": ProofTechnique(
        name="Arithmetization (IP = PSPACE, MIP = NEXP)",
        relativizes=False,
        natural_largeness=False,
        natural_constructivity=False,
        algebrizes=True,
        notes=(
            "The motivating example for algebrization: it is non-relativizing (there is "
            "an oracle making IP != PSPACE) yet still algebrizes, so Aaronson-Wigderson "
            "show it cannot by itself separate P from NP."
        ),
    ),
    "williams_acc0": ProofTechnique(
        name="Williams 2011: NEXP not in ACC0",
        relativizes=False,
        # Non-natural by dropping LARGENESS, not constructivity. Williams 2013
        # ("Natural Proofs versus Derandomization", STOC 2013 / SICOMP 2016, Thm 1.1)
        # proves CONSTRUCTIVITY IS UNAVOIDABLE for NEXP lower bounds: NEXP not in C iff
        # a poly-time (constructive) property distinguishes SOME function from all
        # C-circuits. The "some function" / at-least-one reading is the non-large
        # escape. So the correct profile is constructive=True, large=False. (Corrected
        # 2026-06-03; see LEARNINGS finding 25. is_natural stays False since largeness
        # clears it, so the smoke test is unchanged.)
        natural_largeness=False,
        natural_constructivity=True,
        algebrizes=False,
        notes=(
            "The canonical technique that threads all three barriers. It combines a "
            "non-trivial ACC0 satisfiability algorithm with a non-LARGE (function-specific, "
            "but constructive: constructivity is unavoidable, Williams 2013), "
            "non-relativizing, non-algebrizing diagonalization against NEXP. It evades the "
            "natural-proofs barrier by dropping largeness, NOT constructivity. The current "
            "frontier of unconditional lower bounds."
        ),
    ),
}
