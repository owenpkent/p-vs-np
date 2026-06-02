"""Shared infrastructure for the P vs NP proof-architecture experiments.

Re-exports the core abstractions so experiments can write

    from experiments._shared import ProofTechnique, BarrierChecker, BARRIERS

The design mirrors the role the Davenport-Heilbronn L-function plays in the
companion Riemann Hypothesis repo: there, D-H is a single object that any
candidate method must distinguish from zeta. Here the analog is not one object
but three theorems (the relativization, natural-proofs, and algebrization
barriers). A candidate lower-bound technique must evade all three. The
`BarrierChecker` is the wrong-approach detector: given a structured description
of a technique, it flags which barriers the technique runs into.
"""

from __future__ import annotations

from .technique import ProofTechnique
from .barriers import BarrierChecker, BARRIERS, BarrierVerdict

__all__ = [
    "ProofTechnique",
    "BarrierChecker",
    "BARRIERS",
    "BarrierVerdict",
]
