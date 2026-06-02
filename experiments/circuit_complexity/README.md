# Circuit complexity (Architecture 1)

Experiment (d) in the [plan](../PLAN.md). Demonstrates the Hastad switching
lemma in miniature: why constant-depth circuits (AC0) need super-polynomial size
to compute parity.

## The architecture

Architecture 1 of the [research atlas](../../docs/research_atlas/README.md) is
circuit lower bounds. To prove $\mathsf{P} \ne \mathsf{NP}$ it would suffice to
prove $\mathsf{NP} \not\subseteq \mathsf{P/poly}$ (no polynomial-size circuit
family decides an NP-complete problem). The program has produced real
unconditional separations against weak circuit classes:

- AC0 (constant depth, unbounded fan-in): PARITY is not in AC0
  (Furst-Saxe-Sipser 1981; Ajtai 1983; optimal bound Hastad 1986).
- Monotone circuits: CLIQUE needs exponential-size monotone circuits
  (Razborov 1985; Alon-Boppana 1987).
- ACC0 (AC0 with mod-$m$ gates): $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$
  (Williams 2011), the current frontier.

The open gap is vast: we cannot yet prove a super-linear lower bound for general
circuits against an explicit NP function. The barrier theorems explain why.

## What the script does

[`e_parity_restriction.py`](e_parity_restriction.py) exhibits the switching-lemma
mechanism on small truth tables.

- **Part 1.** PARITY is restriction-robust: under a random restriction leaving
  $k$ of $n$ variables free, the restricted function is still parity on the $k$
  survivors, so its exact minimum decision-tree depth stays $k$. Parity has
  nowhere to hide. Verified on every sampled restriction (1856/1856 with the
  default seed).
- **Part 2.** A width-$w$ AND-term (a DNF building block) is fragile: it collapses
  to a constant with high probability. The measured collapse rate matches the
  exact prediction $1 - \big(((1+p)/2)^w - ((1-p)/2)^w\big)$ (empirical 0.589 vs
  predicted 0.594 at $p = 1/2$, $w = 3$).

Putting these together: a DNF small enough to be AC0 has all its terms collapse
under restriction, so the circuit becomes a shallow decision tree, but parity's
decision-tree depth does not drop. That gap is the lower bound in miniature.

## Barrier status

This technique is **non-relativizing** (it opens up the circuit and argues about
its gates), which is exactly why it proves a real separation that diagonalization
cannot. Run it through the checker:

```python
from experiments._shared import ProofTechnique, BarrierChecker
ac0 = ProofTechnique("AC0 random restrictions (Hastad)",
                     relativizes=False, natural_largeness=True,
                     natural_constructivity=True, algebrizes=False)
print(BarrierChecker().check(ac0).report())
```

Note that the AC0 lower bound IS a natural proof. It does not contradict the
Razborov-Rudich barrier because it bounds a restricted circuit class (AC0), not
general circuits, and no pseudorandom generators are claimed inside AC0. The
barrier only bites when the target class is strong enough to contain
cryptography. This is the precise reason AC0 results were possible and
$\mathsf{P/poly}$ results are not.

## Run

```powershell
python -m experiments.circuit_complexity.e_parity_restriction
```
