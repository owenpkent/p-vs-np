"""Barrier self-check for the 2050 reconstruction: an Extended Frege lower bound
via a "monotone-relativized lifting" engine that replaces feasible interpolation.

BUILDER candidate (provisional). The claimed 2050 result is a super-polynomial
lower bound for Extended Frege (eF) on a tautology family, hence NP != coNP and
P != NP. Feasible interpolation is blocked for strong systems (Bonet-Pitassi-Raz
2000), so the engine here is NOT interpolation. It is a lifting theorem that
sends a query-complexity (decision-tree / communication) lower bound up to an eF
proof-size lower bound through a gadget composition, combined with a bounded-
arithmetic witnessing step that forces the proof to commit to a hard search
problem.

This module encodes the technique as a ProofTechnique and runs the project's
three-barrier checker on it, alongside the canonical Williams ACC0 fixture for
comparison. The honesty discipline: the fields are filled to reflect what the
technique actually does, not what we wish it did.

Run:
    python -m experiments.proof_complexity.e_efrege_lifting_barrier_check
"""

from __future__ import annotations

from experiments._shared import BarrierChecker
from experiments._shared.technique import ProofTechnique


# The candidate engine. Rationale for each field is in the notes and in the
# accompanying writeup. The load-bearing claims:
#   - relativizes = False: a proof-size lower bound for eF is a statement about
#     concrete propositional proofs (line-by-line Boolean formulas), not about
#     machines with oracle access. Proof complexity has no native oracle notion;
#     the relativized barrier does not even type-check here. More sharply, the
#     lifting gadget reads the *internal structure* of each proof line, so it is
#     not black-box in any computation.
#   - natural_largeness = False: the hardness certificate is a property of one
#     specific tautology family (a lifted, gadget-composed search problem), not a
#     property holding for a constant fraction of all Boolean functions. It is
#     function-specific, which is the standard largeness escape.
#   - natural_constructivity = True: the lifting analysis is explicit. We mark it
#     constructive to be conservative (worst case for us). Because largeness
#     fails, the conjunction (naturalness) still fails.
#   - algebrizes = False: the witnessing / conservativity step is a finitistic
#     combinatorial extraction in bounded arithmetic, not an arithmetization. No
#     low-degree polynomial extension of an oracle is used; there is no oracle.
EFREGE_LIFTING = ProofTechnique(
    name="2050 candidate: eF lower bound via monotone lifting + bounded-arithmetic witnessing",
    relativizes=False,
    natural_largeness=False,
    natural_constructivity=True,
    algebrizes=False,
    notes=(
        "Replaces feasible interpolation (blocked by Bonet-Pitassi-Raz 2000) with a "
        "lifting theorem from query/communication complexity to eF proof size, plus a "
        "witnessing step in a bounded-arithmetic theory V^1_2 / T^1_2 that pins the proof "
        "to a hard total search problem (TFNP). Largeness fails (the certificate is about "
        "one tautology family, not generic functions), so it is non-natural even though the "
        "analysis is explicit. No oracle and no arithmetization, so relativization and "
        "algebrization do not apply."
    ),
)


def main() -> int:
    checker = BarrierChecker()
    verdict = checker.check(EFREGE_LIFTING)
    print(verdict.report())
    print()
    print("Comparison fixture (Williams ACC0):")
    from experiments._shared import BARRIERS
    print(checker.check(BARRIERS["williams_acc0"]).report())
    print()
    if verdict.evades_all:
        print("Self-check result: candidate EVADES all three known barriers "
              "(necessary, not sufficient). Hand off to VERIFIER and ADVERSARY.")
        return 0
    print("Self-check result: candidate DISQUALIFIED. Revise before deeper investment.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
