# Natural proofs barrier (Architecture: Circuit lower bounds, the wall)

Experiment (c) in the [plan](../PLAN.md). Demonstrates the Razborov-Rudich
(1994) natural-proofs barrier by measuring largeness and constructivity of
candidate hardness properties on small truth tables.

## The result being illustrated

A property $\Phi$ of $n$-bit Boolean functions is **natural** if it is:

- **Large**: satisfied by at least a $2^{-O(n)}$ fraction of all $2^{2^n}$
  functions (the property is common, not bespoke).
- **Constructive**: decidable in time polynomial in the truth-table length
  $2^n$ (a small circuit could test it).

Razborov and Rudich proved that if a natural property is also **useful** (it
fails for all easy functions, so any function having it is hard), then it yields
a distinguisher that breaks strong pseudorandom generators. Under the standard
assumption that such generators exist (from the hardness of factoring or
discrete log), no useful natural property can prove super-polynomial lower
bounds against $\mathsf{P/poly}$.

Consequence: a combinatorial proof of $\mathsf{NP} \not\subseteq \mathsf{P/poly}$
must use a **non-natural** property: either non-constructive, or non-large but
still useful.

## What the script does

[`e_largeness_constructivity.py`](e_largeness_constructivity.py) makes the two
conditions concrete.

- **Property 1, high average sensitivity.** Large (most functions have it) and
  constructive (computable from the truth table in $O(n\,2^n)$ time). So it is
  natural, and by Razborov-Rudich cannot separate general circuits. The script
  measures the largeness fraction (~0.35-0.49 across $n = 3,4,5$) and the
  per-call evaluation time.
- **Property 2, equality to one fixed function.** Constructive but not large
  (true for exactly one of $2^{2^n}$ functions). It dodges the largeness clause.
  The cost is usefulness: certifying a function is hard this way still requires
  excluding every easy function, which is where the non-naturalness hides.
- **Property 3, minimum circuit size $> s$ (MCSP).** Large for $s$ below the
  Shannon counting bound, but its constructivity is exactly the Minimum Circuit
  Size Problem, whose complexity is open. This is the crux: if MCSP were easy,
  the property would be natural and the barrier would bite.

## Result (reproduced)

```
Property 1: average sensitivity > n/2  (a common hardness proxy)
  n  largeness  eval time (s)                verdict
  3      0.375       0.000005 NATURAL (barrier hits)
  4      0.352       0.000014 NATURAL (barrier hits)
  5      0.485       0.000029 NATURAL (barrier hits)
Property 2: n=4 measured largeness 0.000000 (exact 1/2^(2^n) = 1.53e-05)
```

## Reading in the project stance

A coordinate, not a wall. The barrier says the proof must engage a property that
is either hard to compute or special to the target function. That is precisely
the territory of Williams's ACC0 work (a non-constructive, non-relativizing,
non-algebrizing diagonalization combined with a circuit-satisfiability
algorithm) and of Geometric Complexity Theory (representation-theoretic
obstructions that are conjecturally not natural). The barrier narrows the search
to those structural routes.

## Run

```powershell
python -m experiments.natural_proofs.e_largeness_constructivity
```
