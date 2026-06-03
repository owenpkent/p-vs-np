# Learnings from the proof-architecture experimental thread

> Companion to [PLAN.md](PLAN.md) (test plan and status table) and the
> per-architecture READMEs. The plan answers "what does each experiment do?".
> This document answers "what do they collectively teach?", organized by finding
> rather than by architecture. Updated as new experiments complete.

The dominant meta-finding mirrors the Riemann repo's marginal-positivity thesis,
translated to complexity: **the three barriers are not three separate walls but
one coordinate system.** Every technique that has worked on a weak class fails to
generalize for a barrier-shaped reason, and the few techniques that escape (ACC0,
GCT) do so by being non-natural, non-relativizing, and non-algebrizing at once.
That is a compass telling us where the proof must live, not a verdict that it
cannot be found.

---

## Cross-cutting findings

### 1. The barriers compose: a technique can clear one or two and still fall.

Arithmetization is the sharpest example. It is **non-relativizing** (there is an
oracle making $\mathsf{IP} \ne \mathsf{PSPACE}$, yet $\mathsf{IP} = \mathsf{PSPACE}$
holds unrelativized), which made it look like an escape from the 1975 barrier.
Aaronson-Wigderson 2008 showed it still **algebrizes**, so it cannot separate P
from NP. Lesson encoded in the checker: clearing relativization is necessary, not
sufficient. A technique must be checked against all three independently.

### 2. Natural proofs are common, and that is the point.

The Razborov 1985 monotone-circuit lower bound for clique IS a natural proof
(its method of approximations is large and constructive). It does not violate the
Razborov-Rudich barrier because it bounds only monotone circuits, where no
pseudorandom generators are assumed. The same is true of the AC0 parity bound in
[`circuit_complexity/`](circuit_complexity/). Finding: naturalness is the default
state of combinatorial lower-bound techniques. Non-naturalness is the rare,
expensive ingredient a P/poly separation needs, which is why so few candidates
have it.

### 3. The constructivity crux is concrete and it is MCSP.

The [natural-proofs experiment](natural_proofs/) shows that "minimum circuit size
$> s$" is the property a real lower bound wants, that it is large below the
Shannon counting bound, and that its constructivity is exactly the Minimum
Circuit Size Problem. MCSP's complexity is open (not known to be in P, not known
NP-hard under poly-time reductions). So the natural-proofs barrier reduces, for
this property, to a single open question about MCSP. This localizes where the
non-naturalness must come from.

### 4. Relativization is a finite, mechanical phenomenon.

The [BGS experiment](relativization/) reproduces the diagonalization defeating
every poly-time oracle machine on a finite model. The engine is one inequality:
a poly-time machine on input $1^n$ queries fewer than $2^n$ strings, so a free
string always remains to flip the answer against it. Finding: the relativization
barrier is not mysterious. It is the precise statement that any black-box (oracle)
argument inherits this diagonalization, so it cannot pin P vs NP. Opening the box
(circuit lower bounds) is the only known way past it.

### 5. Average-case hardness is not worst-case hardness, and the gap is visible.

The [SAT phase transition](sat_phase_transition/) locates the hardness peak at
$\alpha \approx 4.25$, coinciding with the SAT/UNSAT crossing near
$\alpha_c \approx 4.267$. But this is an average-case phenomenon: most random
instances away from the threshold are easy. P vs NP is a worst-case question.
Finding: the threshold is the cleanest experimental handle on SAT difficulty, yet
it does not touch the worst case. Any claimed easy algorithm for SAT must handle
the worst case, not just random instances, and any hardness proof must explain
the worst case the threshold only approaches.

### 6. The Williams technique is the existence proof that the barriers are passable.

$\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$ (Williams 2011) threads all three
barriers: it combines a non-trivial ACC0 circuit-satisfiability algorithm with a
non-constructive, non-relativizing, non-algebrizing diagonalization against NEXP.
Encoded in [`_shared/barriers.py`](_shared/barriers.py) as the one technique that
evades the checker. Finding: the barriers narrow the search but do not close it.
The frontier technique is precisely the one that satisfies all three "not" clauses
simultaneously, and the open problem is to push it from ACC0 down to P/poly and
from NEXP down to NP.

### 7. GCT relocated the obstruction into representation theory, then hit its own no-go.

Mulmuley-Sohoni's Geometric Complexity Theory aimed to separate permanent from
determinant via multiplicity obstructions in coordinate rings of orbit closures,
a conjecturally non-natural route. Burgisser-Ikenmeyer-Panova 2016 proved that
*occurrence* obstructions (the original plan) cannot work: the relevant
multiplicities are nonzero on both sides. Finding: GCT is not refuted, but its
first concrete plan is closed; any continuation must use *multiplicity* (not mere
occurrence) obstructions, which is a strictly harder representation-theoretic
computation. This is the GCT analog of the marginal-positivity coordinate: the
soft version is ruled out, so the work concentrates on the sharp version.

### 8. Forced to defend themselves, independent futures converge on the Williams spine.

The [2050 backward-induction dossier](../docs/03_research/2050_backward_induction.md)
is a speculative exercise, not mathematics: it imagines nine "2050 historian"
resolution paths, stress-tests each against the three barriers and for
circularity, then ranks the survivors (six died, three wounded). The headline is a
coordinate, not a theorem. Four of the kills carry the *same* repair, graft onto
the Williams algorithm-to-lower-bound spine rather than replace it, and that spine
is the only component no adversary could disqualify. Finding: the compass reading
is consistent across the architectures the exercise probed. The frontier is to
push Williams from ACC0 toward P/poly (the leading imagined path rides
meta-complexity on the spine, using a proved non-constructivity of high-$Kt$ truth
tables). The everything-routes-through milestone is the $\mathsf{TC}^0$ hinge: a
combinatorial non-algebrizing $\mathsf{TC}^0$-satisfiability speedup yielding
$\mathsf{NEXP} \not\subseteq \mathsf{TC}^0$, where the polynomial method that beat
$\mathsf{ACC}^0$ dies because MAJORITY has approximate degree $\Theta(n)$ (Paturi 1992), so it has no low-degree approximant.
That hinge is compute-light and attackable now; it is modeled in
[`circuit_complexity/e_tc0_sat_savings.py`](circuit_complexity/e_tc0_sat_savings.py),
which disqualifies the naive polynomial-method route (natural and algebrizing) and
shows the candidate Boolean-rank-collapse speedup evading all three barriers.

### 9. The missing object is a fast-to-compute invariant that does not algebrize.

The braided path needs one object that does not yet exist: a quantity computable
cheaply by a #SAT-style algorithm (the algorithmic strand) that is provably NOT
reconstructible from a low-degree oracle extension (the algebrization strand).
Every rational trace, rank, or volume invariant proposed for this role algebrizes
(Lefschetz number, Betti numbers, Sum-of-Squares degree, Schur multiplicity,
free-energy width all fail the same way). The only candidate reconciliation in the
[dossier](../docs/03_research/2050_backward_induction.md) is a "Bockstein bridge":
a characteristic-0 algorithmic count forcing a characteristic-2 torsion class to be
non-vanishing. Finding: this is a concrete shopping list, not a dead end, and it is
now operationalized in [`_shared/algebrization_probe.py`](_shared/algebrization_probe.py),
which classifies a proposed invariant as "algebrizes" (characteristic-0
trace/rank/volume functional) versus "candidate-non-algebrizing" (mod-2 torsion or
non-abelian, e.g. Steenrod, Bockstein, $\pi_1$). The probe turns the
strand-1-vs-strand-3 tension into a filter any future invariant must pass.

### 10. An implied fourth barrier: bounded-interface reconstruction.

The same [dossier](../docs/03_research/2050_backward_induction.md) reads the three
known barriers as instances of one pattern: a technique fails if its hardness
certificate can be reconstructed across a bounded, low-interaction interface
(relativization is bit access, algebrization is low-degree-point access, natural
proofs is a bounded-cost decision interface). Finding: this is a unifying
coordinate to aim for, not a proved theorem. It is not yet correctly axiomatized,
and every attempt so far to wield it as a separate obstruction collapsed back into
one of the three known barriers. Stated honestly: the prize would be an invariant
whose certificate survives every bounded interface, and the value of the conjecture
right now is as a sharper compass for the strand-1-vs-strand-3 search in finding 9.

### 11. Grounded reading corrects the record: MAJORITY needs linear approximate degree.

The reading-notes pass over the downloaded sources caught a factual error that the
dossier and several derived docs had propagated: they stated MAJORITY's approximate
degree as $\Theta(\sqrt{n})$. Paturi 1992 gives $\Theta(\sqrt{n(n - \Gamma(f))})$ for
symmetric $f$; MAJORITY has its sign change at the center ($\Gamma \approx 0$), so its
approximate degree is $\Theta(n)$, while OR and AND (endpoint change) are the ones at
$\Theta(\sqrt{n})$. The Bun-Thaler survey states $\widetilde{\deg}(\mathrm{MAJ}) =
\Theta(n)$ directly. Finding: the correction strengthens the $\mathsf{TC}^0$-hinge
argument rather than weakening it. MAJORITY requires the maximum (linear) approximate
degree, so it has no low-degree approximant at all, which is precisely why the
Razborov-Smolensky low-degree polynomial method cannot reach threshold gates. The
docs were corrected on 2026-06-02. Methodological lesson: grounded reading against
primary sources is the honesty mechanism that catches errors a confident summary
would carry forward.

### 12. Meta-complexity is the leading path's engine, but non-black-box is not non-relativizing.

The meta-complexity reading pass establishes MCSP and time-bounded Kolmogorov
complexity as a hub: a natural property IS a zero-error average-case algorithm for
MCSP, and MCSP average-case hardness is equivalent to succinct pseudorandomness
(Santhanam 2020); one-way functions exist iff $Kt$ is mildly average-case hard
(Liu-Pass 2020) and, under $\mathsf{NP} \not\subseteq \text{i.o.}\mathsf{P/poly}$,
iff approximating $K^{poly}$ is NP-hard (Hirahara 2023); restricted and partial
MCSP variants are NP-hard non-relativizingly (Hirahara 2022). Finding: this is why
meta-complexity is the dossier's leading path, it supplies a *proved* (not assumed)
non-constructivity. But the load-bearing catch is that Hirahara's non-black-box
worst-case-to-average-case reduction (2018) still *relativizes* (its Section 1.7),
so non-black-box does not equal non-relativizing. Meta-complexity supplies the
non-naturalness; the non-relativizing and non-algebrizing content must come from
the Williams algorithm-to-lower-bound spine. This independently confirms the
dossier's repair (graft meta-complexity onto the spine, do not let the arithmetizing
W2A core be the barrier-clearing ingredient). Source: the meta-complexity
[reading notes](../docs/03_research/reading_notes/meta_complexity/) and the
deepened [research direction 02](../docs/03_research/research_directions/02_natural_proofs_evasion.md).

### 13. The $\mathsf{TC}^0$ wall is confirmed from two independent sides, and the method is non-natural by non-largeness.

The Williams-method and approximate-degree reading establishes three things. First,
the algorithmic-method spine is barrier-clean and the first rung past $\mathsf{ACC}^0$
is already taken: Murray-Williams 2018 gives NQP lower bounds against ACC of THR
(one bottom threshold layer), upgraded to almost-everywhere and average-case by
Chen-Lyu-Williams 2020. Second, the $\mathsf{TC}^0$ wall is confirmed two ways:
(a) by approximate degree, MAJORITY needs $\Theta(n)$ (no low-degree approximant)
while $\mathsf{AC}^0$ already reaches $n^{1-\delta}$ (Bun-Thaler 2017), so the wall
is the threshold layer not $\mathsf{AC}^0$; (b) by certificate structure, the dual
polynomials and pattern-matrix lift (Bun-Thaler, Sherstov) are rational LP/spectral
objects that algebrize, so the approximate-degree method cannot itself be the
non-algebrizing ingredient. Third, a refinement to pin: Williams 2013 proves the
method is non-natural by dropping *largeness*, not constructivity (constructivity is
unavoidable), which sharpens the dossier's "non-constructive" phrasing. Williams
2021 independently names a fourth barrier (locality), corroborating finding 10.
Finding: the leading path's hinge is real and located precisely, and the
barrier-clearing speedup must be combinatorial (Boolean / sign-rank), not the
polynomial method. Source: the [reading notes](../docs/03_research/reading_notes/)
and the deepened [research direction 01](../docs/03_research/research_directions/01_circuit_lower_bounds.md).

### 14. Algebraic topology supplies the tools and a precedent for strand 3, but not the object.

The algebraic-topology reading shows the toolkit is exactly the right shape for the
dossier's missing non-algebrizing invariant. Hatcher gives the mod-2 torsion
machinery (universal coefficients, the Bockstein $\beta$, and $Sq^1 = \beta$);
field coefficients erase torsion, which is why a characteristic-0 functional cannot
see it. Kahn-Saks-Sturtevant (via Miller's survey) is a worked precedent where a
mod-$p$ torsion obstruction, through Smith theory and a Lefschetz fixed-point
argument under a vertex-transitive symmetry, forces a tight complexity lower bound,
the essential ingredient being $\mathbb{F}_p$ not rational homology. Bjorner maps
which invariants are rational/algebrizing (Euler characteristic, $\mathbb{Q}$-Betti,
$\mathbb{Q}$-Lefschetz) versus torsion-sensitive ($\mathbb{Z}/p$-acyclicity, the
$\mathbb{Z}_p$-index). Finding: the vocabulary and one precedent exist, but three
gaps remain, an explicit $(C, \text{instance})$ complex, the symmetry that would
make a fixed-point argument bite, and the Bockstein exact sequence forcing a char-2
torsion class nonzero from a char-0 count. The honest status is that topology gives
the words, not a route. Source: the
[strand-3 synthesis](../docs/03_research/strand3_missing_object.md) and the
[algebraic-topology reading notes](../docs/03_research/reading_notes/algebraic_topology/).
