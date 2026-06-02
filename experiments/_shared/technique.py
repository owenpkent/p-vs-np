"""Structured description of a candidate lower-bound proof technique.

A `ProofTechnique` is the abstract object the barrier checker consumes. We
deliberately keep the schema small and declarative: the three known barriers
(relativization, natural proofs, algebrization) are each characterized by a
property of the *proof technique*, not of the final theorem, so the technique
must carry enough metadata to evaluate those properties.

The fields encode the questions the barrier theorems actually ask:

  - Does the argument go through unchanged when every machine is given an
    arbitrary oracle? (relativization, Baker-Gill-Solovay 1975)
  - Does the argument exhibit a property of Boolean functions that is large
    (holds for a constant fraction of all functions) and constructive
    (decidable in time polynomial in the truth-table size)? (natural proofs,
    Razborov-Rudich 1994)
  - Does the argument go through unchanged when oracles are extended to their
    low-degree polynomial extensions over a field/ring? (algebrization,
    Aaronson-Wigderson 2008)

This is intentionally a *modeling* layer, not a theorem prover. The point is to
make the discipline mechanical: a researcher (human or agent) fills in the
fields honestly, and the checker reports which walls the technique hits. The
honesty is the load-bearing part, exactly as it is for a human who must decide
whether their argument "relativizes."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProofTechnique:
    """Declarative metadata about a candidate complexity lower-bound technique.

    Attributes:
        name: human-readable label.
        relativizes: True if the argument treats machines as black boxes and so
            goes through for every oracle. Diagonalization and simulation
            arguments relativize; arguments that open up the machine (counting
            gates, switching lemma on an explicit circuit) generally do not.
        natural_largeness: True if the combinatorial property the technique uses
            to certify hardness is satisfied by a constant (or 1/poly) fraction
            of all Boolean functions on n bits. Razborov-Rudich's "largeness".
        natural_constructivity: True if that property is decidable in time
            polynomial in the truth-table length 2^n. Razborov-Rudich's
            "constructivity".
        algebrizes: True if the argument still goes through when oracle queries
            are answered by a low-degree polynomial extension of the oracle.
            Most relativizing arguments algebrize; some non-relativizing ones
            (arithmetization-based, e.g. IP = PSPACE) algebrize too.
        notes: free-form commentary recorded for the audit trail.
    """

    name: str
    relativizes: bool
    natural_largeness: bool
    natural_constructivity: bool
    algebrizes: bool
    notes: str = ""

    @property
    def is_natural(self) -> bool:
        """A property is *natural* (Razborov-Rudich) when it is both large and
        constructive. Naturalness is what makes a technique fall to the
        natural-proofs barrier under the standard pseudorandomness assumption.
        """
        return self.natural_largeness and self.natural_constructivity
