# Random k-SAT phase transition (the hardness landscape)

Experiment (b) in the [plan](../PLAN.md). Generates random 3-SAT at varying
clause/variable ratios, solves with a self-contained DPLL solver, and exhibits
both the satisfiability threshold near $\alpha_c \approx 4.267$ and the running-
time hardness peak there.

## Why this matters for P vs NP

SAT is the canonical NP-complete problem (Cook 1971; Levin independently). P vs
NP asks whether SAT is in P. The random k-SAT model gives the sharpest empirical
picture of *where* SAT instances are hard.

For random 3-SAT with $n$ variables and $m = \alpha n$ clauses, the satisfiable
fraction drops sharply from ~1 to ~0 as $\alpha$ crosses a critical ratio. The
threshold is conjectured sharp for $k = 3$ (and proved for large $k$ by
Ding-Sly-Sun 2015); the best numerical estimate is $\alpha_c \approx 4.267$
(Mertens-Mezard-Zecchina 2006; the empirical crossing was located near 4.2-4.3
by Crawford-Auton 1996).

The structurally important fact is the **coincidence of two curves**: the
SAT/UNSAT crossing and the running-time peak of complete solvers sit at the same
$\alpha_c$. This is the easy-hard-easy pattern. It is why most random instances
are not hard, and why hardness concentrates at the threshold. A proof that
NP-complete problems are hard must explain the worst case, which threshold
instances approach but random sampling never pins. That gap between average-case
and worst-case is one of the deepest features of the P-vs-NP landscape.

## What the script does

[`e_sat_phase.py`](e_sat_phase.py) implements DPLL with unit propagation and a
simple branching rule, sweeps $\alpha$ from 3.0 to 6.0, and reports the
satisfiable fraction and the median number of DPLL decisions (the standard
hardness proxy) at each ratio.

## Result (reproduced, $n = 60$, 60 trials per ratio)

```
 alpha=m/n    P(SAT)  median DPLL decisions
      3.50      1.00                   27.0
      4.00      0.88                  140.5
      4.25      0.52                  276.5   <- hardness peak
      4.50      0.37                  270.5
      5.00      0.02                  212.0
      6.00      0.00                  106.5

Empirical SAT/UNSAT crossing (P=0.5): alpha ~ 4.28
Empirical hardness peak (max median decisions): alpha = 4.25
```

The crossing (4.28) and the peak (4.25) coincide near the literature value
$\alpha_c \approx 4.267$. The finite-$n$ crossing drifts toward $\alpha_c$ from
above as $n$ grows.

## Caveat on what this does and does not show

This is an average-case probe. It locates where random instances are hard, not
where worst-case instances are. P vs NP is a worst-case question. The experiment
is included because the threshold is the cleanest experimental handle on SAT
difficulty and because the average-case/worst-case gap it makes visible is a
genuine obstruction the proof program must respect.

## The statistical-physics picture (from the June 2026 reading pass)

Synthesized from the stat-physics reading notes.

- [Mertens-Mezard-Zecchina 2006](../../docs/03_research/reading_notes/stat_physics/mertens_mezard_zecchina_2006_ksat_thresholds.md):
  the 1RSB cavity-method source for the threshold ($\alpha_c(3) = 4.26675 \pm
  0.00015$) and the large-$K$ expansion. It is the quantitative substrate for the
  value this experiment reproduces, and it is average-case heuristic physics, not a
  lower-bound technique.
- [Achlioptas-Coja-Oghlan-Ricci-Tersenghi 2011](../../docs/03_research/reading_notes/stat_physics/achlioptas_cojaoghlan_riccitersenghi_2011_solution_space_geometry.md):
  for $k \ge 8$ the solution space shatters below the threshold into exponentially
  many small, far-apart, heavily-frozen clusters. This is the rigorous geometry
  behind the hardness peak.
- [Gamarnik 2021](../../docs/03_research/reading_notes/stat_physics/gamarnik_2021_overlap_gap_property.md):
  the overlap-gap property is a rigorous average-case geometric obstruction ruling
  out stable, low-degree, local, AMP, Langevin, and QAOA algorithm classes. The
  load-bearing caveat: it bounds algorithm families rather than worst-case
  complexity, it is itself large-plus-constructive (hence natural in the
  Razborov-Rudich sense), and it proves no worst-case P-vs-NP hardness.

Bearing on the program: this clustering geometry is the candidate substrate for the
strand-3 missing object (a topological invariant of a solution complex, see
[`strand3_missing_object.md`](../../docs/03_research/strand3_missing_object.md)),
but the physics itself stays average-case. The average-case/worst-case gap above is
not a presentational caveat, it is a theorem about what the overlap-gap property
does and does not bound.

## Run

```powershell
python -m experiments.sat_phase_transition.e_sat_phase
```

A plot is saved if a working matplotlib is available; the numerical result does
not depend on it.
