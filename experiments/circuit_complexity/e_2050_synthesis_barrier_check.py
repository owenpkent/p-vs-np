"""Barrier self-check for the 2050 machine-discovered synthesis scenario.

This encodes the candidate cross-architecture technique imagined in the 2050
historian scenario as a `ProofTechnique` and runs it through the published
three-barrier discipline. The point is honesty: a technique that "proves
P != NP" must explain, mechanically, how it dodges relativization, natural
proofs, and algebrization at once.

The candidate technique (working name "homotopy-witnessed local-list-decoding
lower bound", HLLB) has three ingredients:

  1. A meta-complexity core: a non-constructive, function-specific hardness
     certificate descended from the MCSP / Hirahara average-case-to-worst-case
     line. The certifying property is NOT large (it is specific to a padded
     NP-complete target), so it dodges the largeness clause of Razborov-Rudich.

  2. The algorithmic method (Williams) lifted to P/poly via a non-trivial
     #SAT-style algorithm for a self-correcting circuit class, supplying the
     non-relativizing, non-algebrizing diagonalization spine.

  3. A new combinatorial / topological invariant of the Boolean hypercube:
     the homotopy type of the SAT solution-space complex, which the algebraic
     oracle extension fails to preserve. This is the dedicated
     anti-algebrization device.

Run:
    python -m experiments.circuit_complexity.e_2050_synthesis_barrier_check
"""

from __future__ import annotations

from experiments._shared.barriers import BarrierChecker, BARRIERS
from experiments._shared.technique import ProofTechnique


HLLB_2050 = ProofTechnique(
    name="2050 HLLB: homotopy-witnessed, meta-complexity-anchored, Williams-lifted lower bound",
    # Non-relativizing: the diagonalization spine is the algorithmic method,
    # which opens up the circuit (it runs a #SAT algorithm on the candidate
    # circuit's structure). It does not treat the machine as a black box.
    relativizes=False,
    # The hardness-certifying property is function-specific (true of a padded
    # NP-complete target and a vanishing fraction of all functions), so it is
    # NOT large. This is the chosen escape from the largeness clause.
    natural_largeness=False,
    # The property is also non-constructive (its decidability is exactly an
    # MCSP-hard / meta-complexity-hard question shown hard along the way). We
    # set this False to record "not constructive". Either non-largeness alone or
    # non-constructivity alone suffices to evade; the scenario uses both.
    natural_constructivity=False,
    # Non-algebrizing: the topological invariant of the SAT solution complex is
    # not preserved by low-degree polynomial extension of the oracle. This is
    # the explicit anti-algebrization ingredient, the analog of how Williams's
    # argument fails to go through under algebraic oracles.
    algebrizes=False,
    notes=(
        "Cross-architecture synthesis: meta-complexity (non-large, non-constructive "
        "certificate) + algorithmic method (non-relativizing spine) + homotopy "
        "invariant of solution space (anti-algebrization). Honest risk: if the "
        "homotopy invariant turns out to be computable from the low-degree extension "
        "(i.e. it is an algebraic invariant in disguise), the algebrization evasion "
        "fails. That is the load-bearing uncertainty."
    ),
)


def main() -> None:
    checker = BarrierChecker()
    print("=== 2050 synthesis candidate (HLLB) ===")
    print(checker.check(HLLB_2050).report())
    print()
    print("=== Reference: Williams ACC0 (the proof-of-concept that threads all three) ===")
    print(checker.check(BARRIERS["williams_acc0"]).report())


if __name__ == "__main__":
    main()
