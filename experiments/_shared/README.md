# Shared experiment infrastructure

Phase 0 of the [proof-architectures plan](../PLAN.md). Provides the project's
wrong-approach detector: the three-barrier checker that every candidate
complexity lower-bound technique must clear.

## The barrier discipline (this repo's Davenport-Heilbronn analog)

In the companion Riemann Hypothesis repo, a single contrived object (the
Davenport-Heilbronn L-function, which has a functional equation but no Euler
product and known off-line zeros) falsifies any method that cannot tell it apart
from $\zeta$. P vs NP has a stronger and more famous version of the same
discipline: three published *barrier theorems*, each of which proves that a
whole class of proof techniques cannot resolve the question.

| Barrier | Reference | What it rules out |
|---|---|---|
| Relativization | Baker, Gill, Solovay 1975 | Techniques that go through for every oracle. There are oracles $A$ with $\mathsf{P}^A = \mathsf{NP}^A$ and $B$ with $\mathsf{P}^B \ne \mathsf{NP}^B$, so a relativizing argument cannot decide P vs NP either way. |
| Natural proofs | Razborov, Rudich 1994 | Lower bounds proved via a property of Boolean functions that is *large* (holds for a constant fraction of all functions) and *constructive* (decidable in time poly in the $2^n$-bit truth table). Such a property breaks strong pseudorandom generators, contradicting standard cryptographic hardness. |
| Algebrization | Aaronson, Wigderson 2008 | Techniques that still go through when oracles are extended to low-degree polynomials. Arithmetization (the engine of $\mathsf{IP} = \mathsf{PSPACE}$) is non-relativizing but still algebrizes, so it cannot separate. |

A technique that has any hope of resolving P vs NP must evade **all three**.
Passing is necessary, not sufficient. The canonical technique that threads all
three is Williams's 2011 proof that $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$.

## Modules

| File | Purpose |
|---|---|
| [`technique.py`](technique.py) | `ProofTechnique`: declarative metadata for a candidate technique (does it relativize, is its property large/constructive, does it algebrize). |
| [`barriers.py`](barriers.py) | `BarrierChecker` + `BarrierVerdict`: the wrong-approach detector. Also `BARRIERS`, a library of canonical techniques encoded against the published record (diagonalization, Razborov monotone, arithmetization, Williams ACC0). |
| [`smoke_test.py`](smoke_test.py) | Phase 0 regression suite: pins the barrier profile of the four canonical techniques. |

## Smoke test

Run it from the repo root:

```powershell
python -m experiments._shared.smoke_test
```

All 5 tests should pass. The suite checks that pure diagonalization is
disqualified (relativizes and algebrizes), Razborov's monotone method is a
natural proof, arithmetization is non-relativizing but algebrizes, and
Williams's $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$ evades all three.

## Using the checker on a new technique

```python
from experiments._shared import ProofTechnique, BarrierChecker

t = ProofTechnique(
    name="my candidate lower bound",
    relativizes=False,
    natural_largeness=False,
    natural_constructivity=True,
    algebrizes=False,
)
print(BarrierChecker().check(t).report())
```

The honesty of the input fields is load-bearing, exactly as it is for a human
deciding whether their own argument relativizes. The checker mechanizes the
bookkeeping, not the judgment.
