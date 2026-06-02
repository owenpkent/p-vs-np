# Relativization barrier (Architecture: Diagonalization)

Experiment (a) in the [plan](../PLAN.md). Demonstrates the Baker-Gill-Solovay
(1975) relativization barrier, the first and oldest wall any P-vs-NP proof
technique must clear.

## The result being illustrated

Baker, Gill and Solovay constructed two oracles:

- An oracle $A$ with $\mathsf{P}^A = \mathsf{NP}^A$. Any $\mathsf{PSPACE}$-complete
  oracle works (e.g. TQBF): relative to it both classes collapse to
  $\mathsf{PSPACE}$.
- An oracle $B$ with $\mathsf{P}^B \ne \mathsf{NP}^B$, built by diagonalization
  against an enumeration of polynomial-time oracle machines.

Because a *relativizing* proof technique proves its conclusion for every oracle,
and these two oracles force opposite answers, no relativizing technique can
resolve P vs NP. Diagonalization and simulation relativize. That is the precise
sense in which they are insufficient: they were enough for the time and space
hierarchy theorems, which is exactly why they cannot separate P from NP.

## What the script does

[`e_bgs_oracle.py`](e_bgs_oracle.py) makes the diagonalization mechanism concrete
on a finite model.

- **Easy direction.** Models the $\mathsf{PSPACE}$-oracle interface and checks
  that the $\mathsf{NP}^A$ acceptance condition (exists a witness) is resolved by
  a single oracle query, so $\mathsf{P}^A$ decides the same language.
- **Hard direction.** Runs the actual BGS stage construction. Each
  polynomial-time oracle machine is modeled by a query set with a budget
  strictly below $2^n$ (the key resource constraint). At each stage the oracle
  $B$ is set on a fresh length $n_i$ so the machine's answer to
  "$1^{n_i} \in L_B$?" is wrong, using a free string the machine could not have
  queried.

## Result (reproduced)

```
     machine  n_i  queries  budget(2^n)  M says  truth  M wrong?
         M_0    2        3            4    True  False      True
         M_1    3        7            8    True  False      True
         M_2    4       15           16    True  False      True
         M_3    5       25           32    True  False      True
         M_4    6       36           64    True  False      True
```

Every poly-time machine answers incorrectly, while staying within its sub-$2^n$
query budget. The free string exists precisely because the budget is below
$2^{n_i}$. That single fact is the engine of the separation.

## Reading in the project stance

This is a coordinate, not a verdict of hopelessness. The barrier tells us the
proof must be **non-relativizing**: it must open up the machine and use
something about its internal structure that an oracle cannot supply. Circuit
lower bounds (the [circuit_complexity](../circuit_complexity/) thread) are
exactly such non-relativizing techniques, which is why the search moved there.

## Run

```powershell
python -m experiments.relativization.e_bgs_oracle
```
