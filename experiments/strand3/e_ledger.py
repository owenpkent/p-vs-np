"""Strand-3 coordinate ledger: run candidate invariants through the two strands.

The dossier's missing object must satisfy BOTH:
  - strand 1: cheaply computable by a faster-than-brute-force #SAT-style algorithm;
  - strand 3: provably not reconstructible from a low-degree oracle extension (does
    not algebrize).

The algebrization probe (experiments/_shared/algebrization_probe.py) tests strand 3.
This driver layers a strand-1 computability judgment and a circularity check on top,
and classifies each candidate:

  - DEAD (strand 3): the probe says it algebrizes (a char-0 trace/rank/volume count).
  - OPEN (strand-1 gap): non-algebrizing (strand 3 OK) but no #SAT-style algorithm is
    known to compute it cheaply.
  - LIVE: passes both strands (this is the object the dossier says does not yet exist).

Each row is a coordinate: it records what the candidate rules out, hence where the
real object must live. Honest by construction: a candidate that fails a strand is a
SUCCESS recorded as a coordinate, not hidden. Companion docs:
docs/03_research/strand3_ledger.md and docs/03_research/strand3_missing_object.md.

Run:
    python -m experiments.strand3.e_ledger
"""

from __future__ import annotations

from dataclasses import dataclass

from experiments._shared.algebrization_probe import InvariantProfile, probe


@dataclass
class Candidate:
    """A candidate strand-3 invariant plus the strand-1 and circularity judgments
    the probe does not model."""

    profile: InvariantProfile
    strand1_cheap: bool
    strand1_note: str
    circularity: str

    def status(self) -> str:
        v = probe(self.profile)
        if v.classification == "algebrizes":
            return "DEAD (strand 3): algebrizes"
        if v.classification == "candidate-non-algebrizing":
            return "LIVE" if self.strand1_cheap else "OPEN (strand-1 gap)"
        return "AMBIGUOUS (underdetermined profile)"


CANDIDATES: list[Candidate] = [
    Candidate(
        profile=InvariantProfile(
            name="Euler characteristic of the SAT solution complex",
            characteristic=0,
            is_trace_or_rank_functional=True,
            torsion_sensitive=False,
            notes="alternating sum of face counts; a rational count.",
        ),
        strand1_cheap=True,
        strand1_note="cheaply computable as an alternating sum of face counts, but it is a char-0 rational count.",
        circularity="none; defined directly from the instance's solution complex.",
    ),
    Candidate(
        profile=InvariantProfile(
            name="Stiefel-Whitney class w_i of the SAT solution complex",
            characteristic=2,
            is_trace_or_rank_functional=False,
            torsion_sensitive=True,
            reconstructible_from_low_degree_extension=None,
            notes="a mod-2 characteristic class; invisible to characteristic-0 low-degree extensions.",
        ),
        strand1_cheap=False,
        strand1_note="needs the mod-2 cohomology ring (cup products, Sq), not a count; no #SAT-style algorithm is known to compute it cheaply.",
        circularity="none obvious; defined from the solution complex, not from assuming a lower bound.",
    ),
    Candidate(
        profile=InvariantProfile(
            name="Steenrod-square refinement Sq^k of the complex's mod-2 cohomology",
            characteristic=2,
            is_trace_or_rank_functional=False,
            torsion_sensitive=True,
            reconstructible_from_low_degree_extension=None,
            notes="a stable mod-2 cohomology operation with no low-degree polynomial analog.",
        ),
        strand1_cheap=False,
        strand1_note="Sq^k acts on cochains; computing it needs the cochain-level structure, not a #SAT count.",
        circularity="none; the operation is intrinsic to the complex.",
    ),
    Candidate(
        profile=InvariantProfile(
            name="Fundamental-group class pi_1 of the SAT solution nerve",
            characteristic=2,
            is_trace_or_rank_functional=False,
            torsion_sensitive=True,
            reconstructible_from_low_degree_extension=None,
            notes="a non-abelian loop class, not a rational trace; invisible to char-0 extensions.",
        ),
        strand1_cheap=False,
        strand1_note="recovering a non-abelian pi_1 class needs the loop structure of the nerve, not a count.",
        circularity="none; defined from the instance's solution nerve.",
    ),
    Candidate(
        profile=InvariantProfile(
            name="Bockstein image beta(x) of a mod-2 cohomology class",
            characteristic=2,
            is_trace_or_rank_functional=False,
            torsion_sensitive=True,
            reconstructible_from_low_degree_extension=None,
            notes="the integral torsion detected by the Bockstein; the closest single piece to the bridge.",
        ),
        strand1_cheap=False,
        strand1_note="beta(x) alone is not a count; the LIVE object would be a rational count that FORCES beta(x) != 0 via a Bockstein sequence, which does not exist yet.",
        circularity="none; but note the forcing relation (not beta alone) is the missing bridge.",
    ),
    Candidate(
        profile=InvariantProfile(
            name="Persistent mod-2 homology barcode (discrete-Morse computable)",
            characteristic=0,
            is_trace_or_rank_functional=True,
            torsion_sensitive=False,
            reconstructible_from_low_degree_extension=True,
            notes="cheap via discrete Morse theory, but the barcode is rank/Betti data, a char-0 functional.",
        ),
        strand1_cheap=True,
        strand1_note="cheaply computable (discrete Morse collapse + persistence), but it outputs ranks/Betti numbers.",
        circularity="none; the coordinate is that even a cheap torsion-aware computation algebrizes if it outputs ranks.",
    ),
]


def main() -> int:
    print("=== Strand-3 coordinate ledger ===\n")
    print("Each candidate must clear strand 1 (cheap #SAT-style count) AND strand 3")
    print("(non-algebrizing). The probe tests strand 3; strand 1 is judged here.\n")

    live = 0
    for c in CANDIDATES:
        v = probe(c.profile)
        st = c.status()
        print(f"- {c.profile.name}")
        print(f"    strand 3 (algebrization probe): {v.classification}")
        print(f"    strand 1 (cheap #SAT-computable?): {'yes' if c.strand1_cheap else 'no'} -- {c.strand1_note}")
        print(f"    circularity: {c.circularity}")
        print(f"    => {st}")
        if st == "LIVE":
            live += 1

    # Expected probe classifications (the coordinates).
    by_name = {c.profile.name: probe(c.profile).classification for c in CANDIDATES}
    assert by_name["Euler characteristic of the SAT solution complex"] == "algebrizes", \
        "the Euler characteristic is a rational count and must algebrize"
    assert by_name["Stiefel-Whitney class w_i of the SAT solution complex"] == "candidate-non-algebrizing", \
        "a mod-2 characteristic class should pass the strand-3 probe"
    assert by_name["Steenrod-square refinement Sq^k of the complex's mod-2 cohomology"] == "candidate-non-algebrizing", \
        "a Steenrod operation should pass the strand-3 probe"
    assert by_name["Fundamental-group class pi_1 of the SAT solution nerve"] == "candidate-non-algebrizing", \
        "a non-abelian pi_1 class should pass the strand-3 probe"
    assert by_name["Bockstein image beta(x) of a mod-2 cohomology class"] == "candidate-non-algebrizing", \
        "a Bockstein image should pass the strand-3 probe"
    assert by_name["Persistent mod-2 homology barcode (discrete-Morse computable)"] == "algebrizes", \
        "persistent Betti/barcode data is rank data and must algebrize"

    print()
    print(f"LIVE candidates (clear both strands): {live}")
    # The honest finding: nothing is LIVE yet. The non-algebrizing candidates fail
    # strand 1 (no cheap count), and the cheap count (Euler characteristic) algebrizes.
    assert live == 0, "no current candidate clears both strands; that is the Bockstein-bridge gap"
    print("Coordinate: the non-algebrizing candidates (Stiefel-Whitney, Steenrod) fail")
    print("strand 1 (no cheap #SAT count), and the cheap count (Euler characteristic)")
    print("algebrizes. The two strands have not been met by one object. That is exactly")
    print("the Bockstein-bridge gap the dossier names: a char-0 count forcing a char-2")
    print("torsion class nonzero would link the strands, and it does not exist yet.")
    print()
    print("Self-check OK: probe classifications pinned; no candidate is LIVE (the gap")
    print("is recorded as a coordinate, not hidden).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
