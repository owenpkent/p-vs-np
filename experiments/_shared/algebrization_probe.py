"""The algebrization probe: does a proposed hardness invariant survive a
low-degree oracle extension?

The 2050 backward-induction dossier (docs/03_research/2050_backward_induction.md)
identifies a single missing object that the strongest surviving proof paths all
need: a quantity Q(circuit, instance) that is

  (strand 1) nonzero and cheaply certifiable by a faster-than-brute-force
             #SAT-style algorithm on the candidate circuit's gate structure, and
  (strand 3) provably NOT reconstructible from any low-degree polynomial
             extension of the oracle (so it does not algebrize, per
             Aaronson-Wigderson 2008).

Every scenario that proposed such an invariant had it killed for the SAME
reason: the invariant was secretly a characteristic-0, low-degree,
trace/rank/volume functional (a Lefschetz number, Euler characteristic, Betti
number, semialgebraic / Sum-of-Squares degree, Schur multiplicity, free-energy
width), and any low-degree algebraic oracle extension carries the rational data
needed to recompute it. The only candidate that could survive is a
characteristic-2 torsion class (a Steenrod square, a Bockstein image) or a
non-abelian fundamental-group class, which the rational machinery is blind to.

This module operationalizes that strand-1-vs-strand-3 tension. Given a
declarative profile of an invariant, it classifies the invariant as

  - "algebrizes"               : reconstructible from a low-degree extension, so
                                 by A-W it cannot carry the anti-algebrization
                                 load. Dead as a lower-bound engine on its own.
  - "candidate-non-algebrizing": a positive-characteristic torsion / non-abelian
                                 quantity not reconstructible from the low-degree
                                 extension. The open object the braid needs.
  - "ambiguous"                : not enough is declared to decide.

A "candidate-non-algebrizing" verdict is necessary, not sufficient: it means only
that this particular probe does not immediately disqualify the invariant. The
honesty discipline is the same as the three-barrier checker: a researcher (human
or agent) fills in the fields honestly, and the probe reports the consequence.

Run:
    python -m experiments._shared.algebrization_probe
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class InvariantProfile:
    """Declarative metadata about a proposed hardness invariant.

    Attributes:
        name: human-readable label.
        characteristic: the characteristic of the coefficient ring the invariant
            is computed over. 0 for rational / real / complex invariants (Euler
            characteristic, Lefschetz number, Betti numbers over Q, volumes, SoS
            degree). A prime p for mod-p invariants (Steenrod squares are p=2).
            Characteristic-0 invariants are the algebrizing-prone case.
        is_trace_or_rank_functional: True if the invariant is an alternating sum
            of traces, a rank, a dimension, a determinant, or a volume of a
            chain complex / variety. These are exactly the low-degree polynomial
            functionals A-W show a low-degree oracle extension can recompute.
        torsion_sensitive: True if the invariant detects torsion or non-abelian
            structure that is invisible to rational coefficients (Steenrod /
            Bockstein operations, the fundamental group, mod-p cohomology
            operations). This is the property that MIGHT escape algebrization.
        reconstructible_from_low_degree_extension: if known, the direct A-W test.
            True forces "algebrizes"; False allows "candidate-non-algebrizing".
            None means "not directly declared, infer from the other fields."
        notes: free-form commentary for the audit trail.
    """

    name: str
    characteristic: int
    is_trace_or_rank_functional: bool
    torsion_sensitive: bool
    reconstructible_from_low_degree_extension: Optional[bool] = None
    notes: str = ""


@dataclass
class ProbeVerdict:
    """Result of running the algebrization probe on one invariant."""

    invariant_name: str
    classification: str  # "algebrizes" | "candidate-non-algebrizing" | "ambiguous"
    reasons: List[str] = field(default_factory=list)

    @property
    def algebrizes(self) -> Optional[bool]:
        if self.classification == "algebrizes":
            return True
        if self.classification == "candidate-non-algebrizing":
            return False
        return None

    def report(self) -> str:
        lines = [f"Invariant: {self.invariant_name}"]
        lines.append(f"  classification: {self.classification.upper()}")
        for r in self.reasons:
            lines.append(f"    - {r}")
        return "\n".join(lines)


def probe(p: InvariantProfile) -> ProbeVerdict:
    """Classify an invariant by whether it survives a low-degree oracle extension.

    Decision order (transparent, like the three-barrier checker):
      1. An explicit reconstructibility declaration wins.
      2. A characteristic-0 trace/rank/volume functional algebrizes: the
         low-degree extension carries the rational chain-complex data, so the
         algebrized adversary recomputes it (the Lefschetz / Betti / SoS-degree
         kill from the dossier).
      3. A positive-characteristic torsion-sensitive invariant that is NOT a pure
         rational functional is a candidate non-algebrizing object (the Steenrod /
         Bockstein / pi_1 escape).
      4. Otherwise ambiguous.
    """
    reasons: List[str] = []

    if p.reconstructible_from_low_degree_extension is True:
        reasons.append(
            "explicitly reconstructible from a low-degree oracle extension, so by "
            "Aaronson-Wigderson 2008 it algebrizes and cannot carry the lower bound."
        )
        return ProbeVerdict(p.name, "algebrizes", reasons)

    if p.characteristic == 0 and p.is_trace_or_rank_functional:
        reasons.append(
            "characteristic-0 trace/rank/volume functional: an alternating sum of "
            "traces / a rank / a dimension / a volume of the chain complex, which a "
            "low-degree extension recomputes from the rational data (algebrizes)."
        )
        if p.torsion_sensitive:
            reasons.append(
                "declared torsion_sensitive yet rational: the torsion content is "
                "discarded by the rational functional, so the surviving signal still "
                "algebrizes. Relocate the obstruction into the torsion class itself."
            )
        return ProbeVerdict(p.name, "algebrizes", reasons)

    if p.characteristic != 0 and p.torsion_sensitive and not p.is_trace_or_rank_functional:
        reasons.append(
            f"characteristic-{p.characteristic} torsion-sensitive, non-rational invariant "
            "(Steenrod / Bockstein / non-abelian pi_1): invisible to characteristic-0 "
            "low-degree extensions, so it is NOT obviously reconstructible. Candidate "
            "non-algebrizing object (necessary, not sufficient)."
        )
        if p.reconstructible_from_low_degree_extension is None:
            reasons.append(
                "reconstructibility not directly declared: discharge it with a real "
                "Bockstein / universal-coefficients argument before relying on it."
            )
        return ProbeVerdict(p.name, "candidate-non-algebrizing", reasons)

    reasons.append(
        "underdetermined: declare the characteristic, whether it is a trace/rank "
        "functional, and torsion-sensitivity to classify it."
    )
    return ProbeVerdict(p.name, "ambiguous", reasons)


# A library of invariants drawn from the 2050 dossier's scenarios. Each rational
# functional is a documented kill; the torsion candidates are the open objects
# the braided path needs. These double as regression fixtures.
INVARIANTS = {
    "lefschetz_number": InvariantProfile(
        name="Lefschetz number of a self-map of the SAT solution complex (homotopy-bridge scenario)",
        characteristic=0,
        is_trace_or_rank_functional=True,
        torsion_sensitive=False,
        notes=(
            "L(f) = sum_i (-1)^i tr(f_* | H_i; Q): a characteristic-0 alternating trace. "
            "The contradiction engine of the machine-found topological proof; it algebrizes "
            "at the definition of the invariant."
        ),
    ),
    "betti_euler": InvariantProfile(
        name="Betti numbers / Euler characteristic of the solution-space complex over Q",
        characteristic=0,
        is_trace_or_rank_functional=True,
        torsion_sensitive=False,
        notes="Ranks of rational homology groups; a low-degree extension recomputes them.",
    ),
    "sos_degree": InvariantProfile(
        name="Sum-of-Squares / semialgebraic degree of a witness relaxation (the P=NP upset)",
        characteristic=0,
        is_trace_or_rank_functional=True,
        reconstructible_from_low_degree_extension=True,
        torsion_sensitive=False,
        notes=(
            "Low-degree by definition and GL-invariant (a linear reparameterization is a "
            "unit-degree automorphism), so Grigoriev/Schoenebeck lower bounds survive it. "
            "Explicitly reconstructible."
        ),
    ),
    "schur_multiplicity": InvariantProfile(
        name="Schur / plethysm multiplicity in an orbit-closure coordinate ring (GCT scenario)",
        characteristic=0,
        is_trace_or_rank_functional=True,
        torsion_sensitive=False,
        notes=(
            "A dimension of a multiplicity space over C: a rank functional. Beyond "
            "algebrization, the GCT Boolean bridge routes through PIT, which also algebrizes."
        ),
    ),
    "free_energy_width": InvariantProfile(
        name="Free-energy width / overlap-gap statistic (physics-native scenario)",
        characteristic=0,
        is_trace_or_rank_functional=True,
        reconstructible_from_low_degree_extension=True,
        torsion_sensitive=False,
        notes=(
            "An efficiently-estimable low-degree statistic (the 2020s low-degree-hardness "
            "program is built from exactly these). Both natural and algebrizing."
        ),
    ),
    "steenrod_bockstein": InvariantProfile(
        name="Steenrod square / Bockstein torsion class of the solution complex (the open candidate)",
        characteristic=2,
        is_trace_or_rank_functional=False,
        torsion_sensitive=True,
        reconstructible_from_low_degree_extension=None,
        notes=(
            "A mod-2 stable cohomology operation with no low-degree polynomial analog: the "
            "strand-3 object the braided path needs. Its non-vanishing would have to be "
            "FORCED by a rational count via a Bockstein exact sequence (the missing bridge). "
            "Candidate only: the reconstructibility must still be discharged."
        ),
    ),
    "pi1_class": InvariantProfile(
        name="Non-abelian fundamental-group class pi_1 of the satisfiability nerve (the open candidate)",
        characteristic=2,
        is_trace_or_rank_functional=False,
        torsion_sensitive=True,
        reconstructible_from_low_degree_extension=None,
        notes=(
            "A non-abelian loop class, not a rational trace. Like the Steenrod candidate, it "
            "is a possible escape, contingent on an actual non-reconstructibility argument."
        ),
    ),
}


def main() -> int:
    print("=== Algebrization probe: strand-1 (algorithm-computable) vs strand-3 (non-algebrizing) ===\n")

    algebrizing, candidates, ambiguous = [], [], []
    for key, profile in INVARIANTS.items():
        v = probe(profile)
        print(v.report())
        print()
        if v.classification == "algebrizes":
            algebrizing.append(key)
        elif v.classification == "candidate-non-algebrizing":
            candidates.append(key)
        else:
            ambiguous.append(key)

    print(f"Algebrizing (dead as a standalone engine): {', '.join(algebrizing)}")
    print(f"Candidate non-algebrizing (the open objects): {', '.join(candidates)}")
    if ambiguous:
        print(f"Ambiguous: {', '.join(ambiguous)}")
    print()

    # ---- self-checks pinning the dossier's coordinates ----
    rational_kills = ["lefschetz_number", "betti_euler", "sos_degree", "schur_multiplicity", "free_energy_width"]
    for key in rational_kills:
        assert probe(INVARIANTS[key]).algebrizes is True, f"{key} must be classified as algebrizing"
    for key in ["steenrod_bockstein", "pi1_class"]:
        assert probe(INVARIANTS[key]).algebrizes is False, f"{key} must be a candidate non-algebrizing object"

    print("Self-check OK: every characteristic-0 trace/rank/volume invariant algebrizes;")
    print("the mod-2 torsion / non-abelian candidates survive the probe (necessary, not")
    print("sufficient). The braid needs a Bockstein bridge linking a rational count to a")
    print("torsion class. That object does not exist yet; it is the named missing tool.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
