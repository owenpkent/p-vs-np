"""Fourth-barrier scenario: the locality / low-interaction meta-barrier and the
technique engineered to thread all four.

This is a 2050-historian backward-induction scenario, encoded as a runnable
barrier self-check. It posits a FOURTH meta-barrier discovered in the late
2030s, alongside relativization (BGS 1975), natural proofs (RR 1994), and
algebrization (AW 2008). The candidate fourth barrier here is a LOCALITY /
LOW-INTERACTION barrier: it formalizes the observation that every post-2011
lower-bound technique (the Williams algorithm-to-lower-bound route included)
ultimately certifies hardness through an interface that exchanges only a
bounded amount of information with the structure of the hard instance. We call
such techniques "low-interaction." The barrier theorem (hypothetical, "Chen-
Tell-Williams 2038" in the scenario) shows there are LOCAL oracle worlds in
which P = NP, so any low-interaction technique cannot separate.

The candidate winning technique, "self-referential refutation lifting" (SRL),
is engineered to be HIGH-interaction: it threads the proof through the global
combinatorial geometry of a single explicit NP-complete instance family (a
self-referential SAT encoding of its own refutation search), so the certificate
cannot be reconstructed from any bounded interface.

We extend the three-field ProofTechnique with a fourth declarative field. The
three-barrier checker is reused unchanged for the legacy barriers; the locality
clause is checked alongside it. Run:

    python -m experiments.fourth_barrier.e_locality_barrier
"""

from __future__ import annotations

from dataclasses import dataclass

from experiments._shared import BarrierChecker, BARRIERS, ProofTechnique


@dataclass
class FourthBarrierTechnique:
    """A ProofTechnique plus a declarative fourth-barrier field.

    low_interaction is True if the argument certifies hardness through an
    interface that exchanges only poly(n)-bounded information with the hard
    instance (a black-box-low-communication signature). The scenario's fourth
    barrier (the "locality barrier") disqualifies any low_interaction technique
    the same way relativization disqualifies a black-box technique: there is a
    family of LOCAL oracle/instance worlds in which P = NP, and a low-interaction
    proof goes through unchanged in those worlds.
    """

    base: ProofTechnique
    low_interaction: bool
    locality_notes: str = ""

    @property
    def hits_locality(self) -> bool:
        return self.low_interaction

    def report(self) -> str:
        v = BarrierChecker().check(self.base)
        lines = [v.report()]
        lines.append(
            f"  locality (4th) barrier : {'HIT' if self.hits_locality else 'evaded'}"
        )
        if self.locality_notes:
            lines.append(f"    - {self.locality_notes}")
        evades_four = v.evades_all and not self.hits_locality
        verdict = (
            "EVADES ALL FOUR (necessary, not sufficient)"
            if evades_four
            else "DISQUALIFIED by a known barrier"
        )
        lines.append(f"  four-barrier verdict: {verdict}")
        return "\n".join(lines)


# Williams 2011 as seen through the 2038 lens: it threads the original three,
# but in the scenario it is LOW-INTERACTION (the algorithm-to-lower-bound link
# only needs a SAT algorithm's running-time as a bounded interface), which is
# exactly why the scenario says it stalled below TC0.
williams_relens = FourthBarrierTechnique(
    base=BARRIERS["williams_acc0"],
    low_interaction=True,
    locality_notes=(
        "Algorithm-to-lower-bound certifies hardness through a bounded interface: "
        "only the existence and running time of a circuit-SAT algorithm. In the "
        "scenario's local oracle worlds that interface is preserved, so the route "
        "cannot reach P/poly. This is the retro-diagnosis of why it stalled at ACC0."
    ),
)

# The candidate 2050 winning technique.
srl = FourthBarrierTechnique(
    base=ProofTechnique(
        name="Self-referential refutation lifting (SRL), 2050 candidate",
        # Non-relativizing: the argument opens the instance and reasons about the
        # global geometry of a specific self-referential SAT family, not about
        # machines as black boxes.
        relativizes=False,
        # Non-natural via the largeness escape: the certified property holds only
        # for the engineered self-referential family, a measure-zero set among all
        # functions, so it is not large. It is also not constructive (deciding it
        # requires solving the refutation-search fixpoint).
        natural_largeness=False,
        natural_constructivity=False,
        # Non-algebrizing: the obstruction is a high-degree, non-polynomially-
        # extendable invariant (a fixpoint of the instance's own refutation map),
        # which is destroyed by passing to any low-degree oracle extension.
        algebrizes=False,
        notes=(
            "SRL lifts a refutation-complexity lower bound for a self-referential SAT "
            "family into a circuit lower bound via a high-interaction encoding. The "
            "hardness certificate is a global fixpoint of the instance's own search "
            "for a short refutation, which cannot be reconstructed from any bounded "
            "interface, any oracle, or any low-degree extension."
        ),
    ),
    low_interaction=False,
    locality_notes=(
        "HIGH-interaction by construction: the certificate is the global fixpoint "
        "of a self-referential refutation map on a single explicit instance family. "
        "Reconstructing it requires Omega(2^n / poly) bits of interaction with the "
        "instance, so it survives the local oracle worlds of the 4th barrier."
    ),
)


def main() -> int:
    print("=== Fourth-barrier scenario: locality / low-interaction barrier ===\n")
    print("[Retro-diagnosis] Williams 2011 under the 2038 lens (low-interaction):")
    print(williams_relens.report())
    print()
    print("[Candidate 2050 winner] Self-referential refutation lifting (SRL):")
    print(srl.report())
    print()
    # Sanity: the legacy three-barrier checker must still pass on SRL's base.
    v = BarrierChecker().check(srl.base)
    assert v.evades_all, "SRL base must evade the legacy three barriers"
    assert not srl.hits_locality, "SRL must evade the locality barrier"
    assert williams_relens.hits_locality, "Williams is low-interaction in this scenario"
    print("Self-check: SRL evades all four; Williams is caught by the 4th. OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
