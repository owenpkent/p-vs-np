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
tables). The everything-routes-through milestone is the threshold hinge: a combinatorial
satisfiability speedup for dense threshold circuits, fed through the Williams
connection. CORRECTED by finding 20 (2026-06-03): the earlier claim here, that the
polynomial method "dies" at threshold gates because MAJORITY has approximate degree
$\Theta(n)$ (Paturi 1992), was a conflation. The satisfiability algorithm spends
PROBABILISTIC degree (MAJORITY $\Theta(\sqrt{n})$), not approximate degree, and it
already crosses one threshold layer; the open object is a SAT speedup for DENSE
depth-2 THR-of-THR, not "$\mathsf{NEXP} \not\subseteq \mathsf{TC}^0$" generically.
The hinge is compute-light and attackable now; it is modeled in
[`circuit_complexity/e_tc0_sat_savings.py`](circuit_complexity/e_tc0_sat_savings.py)
and grounded in
[`2050_tc0_hinge_grounded.md`](../docs/03_research/2050_tc0_hinge_grounded.md). The
"Boolean-rank-collapse" name is a placeholder coinage, retired in favor of its real
referents.

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
strand-1-vs-strand-3 tension into a filter any future invariant must pass. SHARPENED
by finding 21 (2026-06-03): the "Bockstein bridge" as a cheap-count-forces-located-
torsion object is a NO-GO. A cheap count forces only the EXISTENCE of torsion (a rank
fact that algebrizes); the located $\beta(x) \ne 0$ is the only non-algebrizing
candidate and is not count-forced. The probe's discriminating axis is therefore
rank-vs-operation, not char-0-vs-char-$p$ (the probe now classifies positive-
characteristic rank functionals as algebrizing too). The reframed live route is the
Smith-theory / symmetry route, not a count.

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
\Theta(n)$ directly. Finding: MAJORITY requires the maximum (linear) approximate
degree, so it has no low-degree (uniform) approximant. CORRECTED by finding 20
(2026-06-03): this fact blocks only the low-degree-CORRELATION route to a lower
bound; it does NOT block the satisfiability algorithm, which spends PROBABILISTIC
degree ($\Theta(\sqrt{n})$ for MAJORITY) and already crosses one threshold layer
(Alman-Chan-Williams 2016). The earlier gloss that this is "precisely why the
Razborov-Smolensky polynomial method cannot reach threshold gates" was itself the
conflation finding 20 retires. The approximate-degree fix in this finding (an
earlier $\Theta(\sqrt{n})$ error) was correctly landed on 2026-06-02. Methodological lesson: grounded reading against
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
Chen-Lyu-Williams 2020 (FOCS 2020, ECCC TR20-150). Second, the threshold
obstruction has two DISTINCT sides that finding 20 separates (correcting this
finding's "wall confirmed two ways" framing into "two sides of a hinge"): (a) on the
lower-bound/CORRELATION side, MAJORITY needs approximate degree $\Theta(n)$ (no
low-degree approximant) while $\mathsf{AC}^0$ already reaches $n^{1-\delta}$
(Bun-Thaler 2017); (b) on the ALGORITHM side the picture is the opposite, the
satisfiability algorithm spends PROBABILISTIC degree $\Theta(\sqrt{n})$ and DOES
cross one threshold layer (Alman-Chan-Williams 2016), so there is no flat wall, only
a density/depth/error budget. CORRECTED by finding 20: the claim that the
dual-polynomial / pattern-matrix objects "algebrize" is PROJECT INFERENCE, not an
Aaronson-Wigderson theorem (downgraded to speculation); the defensible reason the
approximate-degree route is not the non-algebrizing ingredient is that it is NATURAL
(large + constructive). Third: Williams 2013 proves the method is non-natural by
dropping *largeness*, not constructivity (constructivity is unavoidable), which
sharpens the dossier's "non-constructive" phrasing. Williams 2021 independently names
a fourth barrier (locality), corroborating finding 10. Finding: the hinge is located
precisely (dense depth-2 THR-of-THR), but "the speedup must be combinatorial (Boolean
/ sign-rank)" overstates: "combinatorial" is not the same axis as "non-algebrizing"
(ACW's algebraic method already crossed a layer), and sign-rank alone provably cannot
crack THR-of-THR. See finding 20. Source: the [reading notes](../docs/03_research/reading_notes/)
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
the words, not a route. CORRECTED and SHARPENED by finding 21 (2026-06-03): the third
gap (the count-forces-torsion sequence) is now a NO-GO, not an open slot, and the KSS
precedent here is described too strongly. The precedent's consumed certificate is the
RATIONAL Euler / Lefschetz number $\chi = 1$ (which algebrizes); $\mathbb{F}_p$ enters
as ACYCLICITY (a rank fact) via Smith theory, not as a located torsion class. So it is
an "$\mathbb{F}_p$ machinery supports a rational-count forcing" precedent, not "a
torsion class is the certificate". The reframed live route is symmetry (the
Smith-theory fixed-point route), not a count. Source: the
[strand-3 synthesis](../docs/03_research/strand3_missing_object.md) and the
[algebraic-topology reading notes](../docs/03_research/reading_notes/algebraic_topology/).

### 15. GCT after the no-go: multiplicity obstructions are provably stronger, and are the candidate non-algebrizing GCT invariant.

Burgisser 2015 confirms the occurrence-obstruction route is closed (plethysm
positivity forces the obstruction coefficients positive). But Dorfler-Ikenmeyer-Panova
2019 proves, in a model case (Chow variety vs higher Veronese secant, partition
$(n^2-2,n,2)$), that multiplicity obstructions strictly beat occurrence obstructions,
so the program is alive. Grochow 2015 ties this to strand 3: classical lower bounds
build GCT modules that are rank/minor/degree functionals (hence algebrize), and the
multiplicity obstruction is the one GCT quantity that is NOT the rank of an explicit
matrix, making it the natural GCT candidate for the missing non-algebrizing invariant.
Finding: the live GCT target is a padding-free multiplicity comparison, and GCT and
the strand-3 search point at the same kind of object. Source: the
[GCT reading notes](../docs/03_research/reading_notes/gct_rep_theory/) and
[research direction 04](../docs/03_research/research_directions/04_geometric_complexity_theory.md).

### 16. Average-case geometry (clustering, OGP) is a rigorous algorithm-class barrier, not a worst-case route, and is itself natural.

The statistical-physics reading sharpens LEARNINGS finding 5. Achlioptas-Coja-Oghlan-Ricci-Tersenghi
2011 rigorously establishes solution-space shattering into frozen clusters; Gamarnik
2021 shows the overlap-gap property rules out whole algorithm classes (stable,
low-degree, local, AMP, Langevin, QAOA). But Gamarnik is explicit that OGP bounds
algorithm families, not worst-case complexity, and the OGP statistic is itself
large-plus-constructive, hence natural in the Razborov-Rudich sense. Finding: the
clustering geometry is a candidate substrate for the strand-3 solution complex, but
the physics stays average-case and does not touch worst-case P vs NP. Source: the
[stat-physics reading notes](../docs/03_research/reading_notes/stat_physics/) and the
[SAT phase-transition writeup](sat_phase_transition/).

### 17. Razborov 1995 turns natural proofs into a formal unprovability theorem (the A6 path), and lifting is the modern proof-complexity engine.

Razborov 1995 shows that under a strong PRG, $S_2^2(\alpha)$ cannot refute "SAT has
small circuits", with an unconditional depth-3-with-PARITY case marking where the
crypto assumption becomes necessary. This is the dossier's A6 independence-from-a-
strong-arithmetic path made concrete, and it confirms the A6 caveat that the crypto
hypothesis carries the load. Goos-Pitassi-Watson 2017 (query-to-communication lifting
for BPP) is the engine behind modern cutting-planes and monotone lower bounds.
Finding: the honest near-term proof-complexity targets are intermediate systems where
the protocol-circuit duality that Bonet-Pitassi-Raz weaponize against extended Frege
is not provably blocked. Source: the
[proof-complexity reading notes](../docs/03_research/reading_notes/proof_complexity/) and
[research direction 03](../docs/03_research/research_directions/03_proof_complexity.md).

### 18. The width-size tradeoff is vacuous for the pigeonhole principle.

Computing the minimum resolution refutation width of $\mathrm{PHP}^{n+1}_n$ for the
two smallest cases (via width-bounded saturation) gives width exactly equal to the
hole count $n$ (2 and 3), which is the initial pigeon-clause width. So
$w(F \vdash \square) - w(F) \approx 0$, and with $N = \Theta(n^2)$ variables the
Ben-Sasson-Wigderson exponent $(w - w_0)^2 / N$ is $\approx 0$: the width-size
tradeoff gives no size lower bound for PHP. Finding: Haken's $2^{\Omega(n)}$ bound is
a bottleneck-counting argument, NOT a width argument, and PHP is a poor example for
"lower bound via width". BSW is exponential precisely for constant-width,
$O(n)$-variable formulas with refutation width $\Omega(n)$ (Tseitin on expanders,
random k-SAT), where the exponent is $\Theta(n)$. This is a coordinate: it tells a
builder which formula families the width method can and cannot reach. Source:
[`proof_complexity/e_resolution_width_php.py`](proof_complexity/e_resolution_width_php.py).

### 19. The Nisan-Wigderson generator's pseudorandomness genuinely requires hardness.

The polynomial $(l,k)$-design plus a parity-versus-majority distinguisher make the
hardness-randomness connection concrete. With an easy (linear) $f = $ PARITY, every
output bit of $NW_f$ is an $\mathbb{F}_2$-linear function of the seed, so once the
generator stretches ($m > d$) there is a linear dependency among the output bits
whose XOR is identically 0, a perfect distinguisher. With a nonlinear $f = $
MAJORITY the same dependency does not collapse, and the trivial attack fails.
Finding: the PRG property is not free, it is exactly the place the hardness of $f$
is spent (Nisan-Wigderson 1994). This is Architecture 5, the structural
surroundings: Impagliazzo-Wigderson 1997 turns hardness into $\mathsf{BPP} =
\mathsf{P}$, and Kabanets-Impagliazzo 2004 turns derandomization back into circuit
lower bounds, so the two are entangled, though none of this is a direct separation.
Source: [`hardness_randomness/e_nisan_wigderson_prg.py`](hardness_randomness/e_nisan_wigderson_prg.py).

### 20. The TC0 hinge, re-grounded: the polynomial method does not die at threshold gates, and the open object is a dense two-layer threshold SAT speedup.

A survey-plus-fact-check pass against the primary sources corrected a load-bearing
error that findings 8 and 11 had propagated, and located the hinge precisely. Three
corrections. First, "the polynomial method provably stops at threshold gates because
MAJORITY has approximate degree $\Theta(n)$" is FALSE as stated: it conflates two
measures. The SAT algorithm spends PROBABILISTIC degree, where MAJORITY and every
symmetric function are only $\Theta(\sqrt{n \log(1/\varepsilon)})$ (Alman-Williams
FOCS 2015, arXiv:1507.05106; Alman-Chan-Williams FOCS 2016, arXiv:1608.04355), tight
against Razborov-Smolensky 1987. The worst-case approximate degree $\Theta(n)$
(Paturi 1992) is real but blocks the SEPARATE low-degree-correlation route, not the
algorithm. Built from probabilistic polynomials, ACW 2016 (Thm 1.8, Cor 1.1) cross
one EXTRA threshold layer (deterministic $2^{n-n^\varepsilon}$ SAT for AC0[m] of LTF
of LTF with a subquadratic bottom threshold-GATE count, not wire count; this
gate-vs-wire distinction was itself a repo error, now fixed), yielding
$\mathsf{E}^{\mathsf{NP}}$ not in that class. Second, the FIRST threshold rung is
already climbed: Murray-Williams STOC 2018 (ECCC TR17-188) get $\mathsf{NQP}$ not in
$n^{\log^k n}$-size ACC of THR via Williams's 2014 ACC-of-THR SAT algorithm. So
"$\mathsf{NEXP} \not\subseteq \mathsf{TC}^0$ as the first rung" is imprecise; the
open frontier is the SECOND threshold layer once dense (general depth-2 THR-of-THR,
no subquadratic bottom restriction). The concrete target: a SAT/CAPP speedup
$2^{n-n^\varepsilon}$ for dense depth-2 LTF-of-LTF (equivalently, per Chen 2018
arXiv:1805.10698, shaving all polylog factors off a polylog-dimension
closest/furthest-pair problem; medium confidence). Third, the barrier profile is more
honest than "evades all three." Relativization is genuinely evaded (a real SAT
algorithm opens the gate structure). Natural proofs is CONDITIONALLY evaded.
[CORRECTED by finding 25: the next two sentences were over-pessimistic. The PRF
collision binds the LARGE-and-constructive ALTERNATIVES, not "any constructive method"
(Razborov-Rudich needs large AND constructive); the Williams route is non-large, so it
is NOT bound. The collision is the REASON a non-natural method is needed, not the
binding constraint on the leading path; it re-enters only at the NEXP-to-NP descent.]
This was stated as "arguably the BINDING constraint at dense poly-size TC0: that class
likely computes pseudorandom functions, which would make any constructive lower-bound
method there natural." It is double-sourced (ACW 2016, arXiv:1608.04355 Section 1 after
Theorem 1.9; Chen-Tell 2019 via a Miles-Viola 2015 candidate PRF in depth-d TC0 with
$n^{1+O(1/d)}$ wires) that TC0 likely has PRFs, but that binds only the natural
alternatives. See finding 25. Algebrization is NOT YET ASSESSABLE, not "evaded": $\mathsf{algebrizes} =
\mathsf{False}$ is a property of a nonexistent algorithm, in the same epistemic state
as the retired "Boolean-rank collapse" placeholder. The "combinatorial =
non-algebrizing, algebraic = algebrizing" dichotomy is false within our own solved
set, since ACW's algebraic probabilistic-polynomial method already crossed a
threshold layer. The claim that the dual-polynomial / pattern-matrix LP method
"algebrizes" (finding 13) is project inference, NOT an Aaronson-Wigderson theorem,
and is downgraded to speculation; the defensible reason that route fails is that it
is natural. Source: the new note
[`2050_tc0_hinge_grounded.md`](../docs/03_research/2050_tc0_hinge_grounded.md) and
[`circuit_complexity/e_tc0_sat_savings.py`](circuit_complexity/e_tc0_sat_savings.py).

### 21. The Bockstein bridge, computed: a cheap count forces only the EXISTENCE of torsion (a rank fact that algebrizes), so the count-forces-torsion bridge is a no-go; the live route is symmetry, not a count.

The strand-3 "Bockstein bridge" was named (finding 9, finding 14) as the missing
object: a cheap rational count (strand 1) that FORCES a char-2 torsion class
non-vanishing (strand 3, non-algebrizing). The
[`e_bockstein_forcing.py`](strand3/e_bockstein_forcing.py) computation, VERIFIER-checked
(real integral homology by hand-rolled Smith normal form cross-validated against sympy,
mod-2 Betti by GF(2) rank, 0 mismatches on RP^2, the Klein bottle, S^2, the Moebius
band, the $\mathbb{Z} \xrightarrow{2} \mathbb{Z}$ toy, $N(K_4)$, and small SAT
Vietoris-Rips complexes) and ADVERSARY-audited, turns the declarative ledger into
computation and lands a sharp NO-GO on that shape. The mechanism is a category
distinction the earlier framing conflated. A cheap count can force only the EXISTENCE
of torsion, never a LOCATED class: the universal coefficient theorem gives
$\dim_{\mathbb{F}_2} H_n = b_n(\mathbb{Q}) + t_n(2) + t_{n-1}(2)$, so a mod-2 Betti
number exceeding the rational Betti number forces $t_n + t_{n-1} \ge 1$, but BOTH
inputs are ranks of the same integer boundary matrices and the output is the integer
$t_n + t_{n-1}$, itself a rank functional. A low-degree extension carries the rational
chain data, hence every field rank, so by Aaronson-Wigderson the existence-of-torsion
fact ALGEBRIZES. The LOCATED operation $\beta(x) \ne 0$ is the only non-algebrizing
candidate and is NOT count-forced: the lens-space pair $L(p^2; q)$ vs $L(p; q)$ has
equal Betti and equal torsion-count yet $\beta = 0$ on the order-$p^2$ side and
$\beta \ne 0$ on the order-$p$ side (Hatcher 3E.3/3E.4), so no count can distinguish
them; locating $x$ needs the cup-square / mod-2 ring, not a number. The one worked
precedent does not rescue the original shape: in Kahn-Saks-Sturtevant evasiveness the
consumed certificate is the rational Euler / Lefschetz number $\chi = 1$ (which
algebrizes), and $\mathbb{F}_p$ enters only as the coefficient field making Smith
theory's operator splitting valid, as ACYCLICITY (a vanishing rank fact), not as a
located torsion class. This SHARPENS finding 14 (the precedent is "$\mathbb{F}_p$
machinery supports a rational-count forcing", not "a torsion class is the certificate")
and adds the third invariant category the algebrization probe's char-0/char-$p$ binary
misses: a positive-characteristic RANK / acyclicity functional, torsion-flavored in its
coefficient choice yet still algebrizing (recorded as two new ledger coordinates: the
existence-of-torsion Betti gap, and $\mathbb{F}_p$-acyclicity). Two honesty caveats the
audit requires: "this existence fact algebrizes" is the project's application of the
declarative probe logic, sound as informal A-W reasoning but not a cited theorem about
this construction; and "$\beta$ is non-algebrizing" is candidate-only, not a discharged
A-W theorem. Finding: the bridge as a cheap-count-forces-located-torsion object is a
no-go coordinate, not an open slot. The reframed live route is the Smith-theory /
symmetry route (a structured prime-power transitive group action plus an acyclicity
fact forcing a fixed-point contradiction; gap 2), with a secondary target of a located
non-algebrizing operation that certifies a bound DIRECTLY (Babson-Kozlov 2007 chromatic
2-torsion, a closer precedent than KSS). A negative coordinate also landed for gap 1: no
small SAT-derived complex tried carries 2-torsion, and the canonical literal-flip
symmetry of a generic instance is trivial, a structural obstruction to porting KSS.
Source: [`strand3/e_bockstein_forcing.py`](strand3/e_bockstein_forcing.py), the updated
[`strand3_ledger.md`](../docs/03_research/strand3_ledger.md) and
[`strand3_missing_object.md`](../docs/03_research/strand3_missing_object.md).

### 22. The symmetry / Smith fixed-point route (gap 2) is a no-go for strand 3: the prime-power-transitive symmetry provably EXISTS, but its certificate is the rational chi(Fix) (algebrizes), and its output is a query bound, not circuit size.

Finding 21 reframed strand 3's live route from the count-forces-torsion bridge (a no-go)
to the route the one worked precedent (Kahn-Saks-Sturtevant evasiveness) actually uses: a
structured prime-power-transitive group action plus an acyclicity fact forcing a
fixed-point contradiction via Smith theory and Oliver's theorem (gap 2). The
[`e_symmetry_route.py`](strand3/e_symmetry_route.py) computation, VERIFIER-checked (runs
to exit 0; the verifier independently re-derived $\mathrm{AGL}(1,q)$ normality and
2-transitivity, the $\mathrm{is\_normal\_robust}$ workaround for a genuine sympy bug, the
$\chi(\mathrm{Fix}) = 1$ Smith step, and an exhaustive-subgroup PHP Oliver-failure) and
ADVERSARY-audited (verdict no-go, no error or over-claim found), settles both decisive
questions NEGATIVELY. The symmetry is NO LONGER the missing piece: it provably EXISTS and
is fully explicit. $\mathrm{AGL}(1,q) = \mathbb{F}_q \rtimes \mathbb{F}_q^*$ on $q = p^k$
points has the exact Oliver $n_G = 0$ shape (translations = normal elementary-abelian
$p$-group of order $q$, quotient = cyclic $\mathbb{F}_q^*$ of order $q-1$, 2-transitive so
the only nonempty invariant graph is $K_q$), verified for $q \in \{4,5,8,9\}$; the
elementary-abelian Cayley translation core (Tseitin) and the Paley translation core carry
the same shape. Q1 (ALGEBRIZATION): NEGATIVE, and structurally inescapable by the
Oliver-number trichotomy. For finite $G$ not of prime-power order,
$\{\chi(X^G) - 1 : X$ a finite contractible $G$-CW complex$\} = n_G \mathbb{Z}$, and the
deciding invariant in every regime is the integer Euler characteristic $\chi(\mathrm{Fix})$
($n_G = 0$ forces $\chi = 1$; intermediate forces $\chi \equiv 1 \pmod{n_G}$; $n_G = 1$
gives no constraint). $\chi$ is coefficient-independent (verified on the
$\mathbb{Z} \xrightarrow{2} \mathbb{Z}$ toy), so it is a rank functional a low-degree oracle
extension carries, and it ALGEBRIZES (verified concretely: the order-3 rotation on the
$\mathbb{F}_2$-acyclic 2-simplex fixes a single barycenter with $\chi = 1$). This
GENERALIZES the $\mathbb{F}_p$-acyclicity DEAD ledger verdict (finding 21) from the single
KSS precedent to the whole Oliver branch (KSS, Tseitin/Cayley, affine/Singer, Paley all
consume the same rational $\chi = 1$). Q2 (CIRCUIT vs QUERY): NEGATIVE. The Oliver/KSS
output is the decision-tree bound $D(h) = \binom{n}{2} = O(n^2)$, a query measure whose
vertices are EDGE SLOTS (the symmetry acts on the query domain, not a gate structure);
the bound is polynomial, the implication runs the wrong way, and the trick needs
isomorphism-invariant properties a generic instance lacks (the literal-flip stabilizer of
a random formula is trivial). PHP is a definitive negative: its $S_m \times S_n$ symmetry
is transitive but not 2-transitive and has no normal prime-power subgroup with cyclic
quotient ($S_k$ is not prime-power for $k \ge 3$). The prime-power restriction is a hard
ceiling: no $\mathbb{F}_n$ and no $\mathrm{AGL}(1,n)$ for non-prime-power $n$ (smallest
$n = 6$), the literal boundary of the open AKR evasiveness cases. THE STRUCTURAL ROOT
(the audit's circularity finding): in KSS the topology is DOWNSTREAM of the algorithm
(the decision tree IS the collapsing schedule), so the complex is acyclic BY
CONSTRUCTION, torsion is never produced, and the certificate is forced to be rational.
An invariant computed cheaply downstream of an algorithm (strand 1) cannot carry torsion
the algorithm did not put there. This is why strand 1 and strand 3 resist meeting. The
ONE non-algebrizing certificate among surveyed symmetry families is the FREE
$\mathbb{Z}/2$ Babson-Kozlov route (located integral 2-torsion in
$H^*(\mathrm{Hom}(C_{2r+1}, K_n); \mathbb{Z})$ for even $n$, Stiefel-Whitney $w_1^k$ for
odd $n$), the structural OPPOSITE of Oliver (Borsuk-Ulam, NO fixed point); its torsion is
the PRIMARY object (not downstream of an algorithm), which is exactly why it can be
non-algebrizing where Oliver cannot, and exactly why it bounds chromatic number with no
circuit-size bridge: it clears Q1 and fails Q2. Two honesty caveats the audit requires:
"$\chi = 1$ algebrizes" and "located 2-torsion is non-algebrizing" are the project's sound
Aaronson-Wigderson reasoning, candidate-only, NOT discharged A-W theorems about
evasiveness or coloring; and the sign-rank circuit-size touchpoint ($\log$ sign-rank $=$
UPP communication $=$ depth-2 $\mathrm{THR} \circ \mathrm{MAJ}$ size, Forster 2002 /
Razborov-Sherstov, provably capped below $\mathrm{THR} \circ \mathrm{THR}$) is
survey-sourced. Finding: gap 2 is a no-go coordinate. The two topological precedents are
NOT interchangeable (Oliver fixed-point + rational $\chi$ + query model vs Babson-Kozlov
free $\mathbb{Z}/2$ + located torsion + chromatic model), and neither clears both
decisive questions. Source: [`strand3/e_symmetry_route.py`](strand3/e_symmetry_route.py),
the updated [`strand3_ledger.md`](../docs/03_research/strand3_ledger.md) and
[`strand3_missing_object.md`](../docs/03_research/strand3_missing_object.md).

### 23. The Chen-2018 geometry hinge, mapped: the THR-of-THR bottleneck is a polylog-dimension log-shave for the EXACT integer problems, and the bar is SETH-CONSISTENT (genuinely open), not a SETH refutation.

Finding 20 located the open object (a SAT/CAPP speedup for dense depth-2 THR-of-THR,
equivalently the Chen 2018 geometry log-shave) but never mapped how close known
algorithms are to the bar, nor whether the bar is consistent with SETH. A two-survey
plus builder plus adversary plus verifier pass (all Chen-2018 / Chen-2020-ToC /
AWY-2015 parameters web-confirmed verbatim against arXiv:1805.10698 and
arXiv:1802.02325; VERIFIER-checked, ADVERSARY verdict sound-with-fixes, all
required_fixes applied) supplies both, and the result is a precise, favorable
coordinate.

THE GAP. The THR-of-THR bottleneck (Chen 2018 Thm 1.1) is the EXACT integer geometry
at polylog dimension: $Z$-OV/Hopcroft, $\ell_2$-Furthest-Pair, exact
Bichrom.-$\ell_2$-Closest-Pair, $Z$-Max-IP. Best known is $n^{2-1/O(d)}$ (Matousek
1992; Agarwal-Edelsbrunner-Schwarzkopf-Welzl 1991; Yao 1982), which at polylog $d$ is
$n^{2-o(1)}$ with saved factor sub-$\log^1 n$: ZERO realized log-shave, so the entire
required $\log^{\omega(1)} n$ shave is the open gap. The single most attackable target
is Boolean Max-IP at $d = n^\varepsilon$ (Thm 1.5 item 1), where the baseline is
already $n^2\,\mathrm{polylog}$ (Coppersmith 1982 rectangular matmul) and only the logs
separate it from the bar.

THE TRAP, RESOLVED. The Boolean-OV polynomial-method shave ($n^{2-1/O(\log c)}$ at
$d = c\log n$; Abboud-Williams-Yu SODA 2015, derandomized Chan-Williams SODA 2016) does
NOT settle THR-of-THR, for three independent reasons pinned numerically and by assert
in [`e_threshold_geometry_gap.py`](circuit_complexity/e_threshold_geometry_gap.py): (i)
WRONG PROBLEM (Boolean OV, not the integer/exact problems Thm 1.1 needs); (ii) WRONG
DIMENSION (the exponent $1/O(\log c)$ decays to $o(1)$ by polylog $d$); (iii) WRONG
CONCLUSION, decisive (Boolean routes through Thm 1.2 to the strictly weaker SYM-of-THR,
already attackable by classical sign-rank / UPP methods). This refines the framing in
finding 20 and the note's section 4: the DIMENSION regime, not Booleanity alone,
decides the conclusion. Boolean Max-IP at polylog $d \to$ SYM-of-THR (Thm 1.2; routing
in the body, not the abstract, so NEEDS-BODY-VERIFICATION), at $d = n^\varepsilon \to$
THR-of-THR (Thm 1.5).

THE SETH ANSWER (highest-value, favorable). The genuine target (Thm 1.1 and Thm 1.5
item 1) is SETH-CONSISTENT and genuinely OPEN, NOT a SETH-refuting barrier. SETH (via
the OV conjecture, Williams 2005) forbids only a CONSTANT-exponent polynomial speedup
$n^{2-\Omega(1)}$; the Chen bar $n^2\,\mathrm{poly}(d)/\log^{\omega(1)} n$ is a pure
LOG-SHAVE, itself $n^{2-o(1)}$, sitting strictly inside the band SETH guarantees, so
meeting it refutes nothing. Chen disclaims this himself ("the SETH lower bound says
nothing about whether shaving logs is possible"). PRECISION (pre-empts a misreading):
polylog dimension is INSIDE the SETH-hard regime, NOT below it. SETH-hardness reaches
DOWN to $d = 2^{O(\log^\ast n)}$ for $Z$-Max-IP (Chen, Theory of Computing 16(4):1-50
2020, $\ell_2$-Furthest-Pair and Bichrom.-$\ell_2$-Closest-Pair inheriting via the
Williams SODA 2018 reduction) and to $d = \omega((\log\log n)^2)$ for the geometry
problems (Williams SODA 2018). The target is open because of the
log-shave-vs-polynomial-shave SCALE gap, not because the dimension dodges SETH. THE
LONE BARRIER: exactly one of seven routes, Thm 1.5 item 2 (Boolean Max-IP at
$d = \log^k n$ in $n^{2-\varepsilon}$, constant $\varepsilon$), is a genuine polynomial
speedup at $\omega(\log n)$ and WOULD refute SETH/OVC; a builder must not pursue it as a
live target. HONESTY: it is PROVED that SETH forces $n^{2-o(1)}$ at $2^{O(\log^\ast n)}$
(verbatim); it is INFERRED (uncontroversially, stated by Chen) that this does not block
the log-shave bar (no published positive consistency theorem exists).

STATUS. As of June 2026 NEXP not in poly-size THR-of-THR remains OPEN; the Chen-2018
program has not produced it. The only proved nontrivial THR-of-THR results are the
$n^{2-o(1)}$-WIRE bound (Chen-Tamaki / ACW) and the one-bottom-layer ACC-of-THR SIZE
bound (Murray-Williams 2018). arXiv:1805.10698 is an UNPUBLISHED preprint (DBLP: CoRR
only); the companion SETH paper IS published. A second, co-equal obstruction is
unchanged (finding 20): even a successful geometry log-shave only fires the Williams
connection; whether the resulting separation evades natural proofs stays conditional on
the open TC0-PRF question. Source:
[`circuit_complexity/e_threshold_geometry_gap.py`](circuit_complexity/e_threshold_geometry_gap.py)
and the new "Fine-grained gap map" subsection 4a of
[`2050_tc0_hinge_grounded.md`](../docs/03_research/2050_tc0_hinge_grounded.md).

### 24. The Max-IP-at-$n^\varepsilon$ log-shave, attacked: no known technique shaves even one log at $d=n^\varepsilon$, the smallest gap is the intrinsic $\log^2 n$ of Coppersmith rectangular MM for the $(+,\times)$-max semiring, and the threshold-sweep micro-idea is correct but strictly cost-increasing. Open-and-attackable, no finer barrier.

Finding 23 named Boolean Max-IP at $d = n^\varepsilon$ (Chen 2018 arXiv:1805.10698 Thm 1.5
item 1) as the single most attackable THR-of-THR target and confirmed the bar is
SETH-consistent, but stopped at "only the logs separate baseline from bar". A two-survey +
builder + adversary + verifier pass (Chen-2018 abstract/body parameters re-confirmed
verbatim; technique parameters web-confirmed against venues; VERIFIER overall high,
ADVERSARY sound-with-fixes, all required_fixes applied) attacks that bar and lands a sharp,
honest coordinate, with no progress on the prize claimed.

THE DECOMPOSITION. The $n^2\,\mathrm{polylog}$ baseline (Chen verbatim: "we only need to
shave logs on this naive algorithm") splits into (a) the Coppersmith-1982 rectangular-MM
overhead $\log^2 n$, intrinsic to the bilinear / partial-matrix-multiplication recursion
(dual-exponent improvements, $\alpha \ge 0.321334$ today via Williams-Xu-Xu-Zhou 2023/24,
only RAISE the $\varepsilon$-ceiling, they do not shave this $\log^2 n$), and (b) the
max-over-$n^2$ extraction, a flat $\Theta(n^2)$ scan with zero log-shave under enumeration,
since the all-pairs inner-product MATRIX has $\Omega(n^2)$ natural output size (scoped to the
matrix, NOT to Max-IP as a problem, per the adversary fix). PROJECT INFERENCE (flagged): a
log-shave must compute the max WITHOUT materializing-and-scanning all $n^2$ inner products;
the novelty must live in max-extraction-without-enumeration.

THE TECHNIQUE MAP (every known log-shaver lands zero logs at $d=n^\varepsilon$). Polynomial
method (AWY SODA 2015; Chan-Williams SODA 2016): only a CONSTANT factor $2^{O(1/\varepsilon)}$
(the saved exponent $1/O(\varepsilon\log n)\to 0$; pinned numerically), and it solves
OV/existence $\to$ the weaker SYM-of-THR (double-disqualified). Four-Russians / BMM, including
Abboud-Fischer-Kelley-Lovett-Meka STOC 2024 (arXiv:2311.09095, $n^3/2^{\Omega((\log n)^{1/7})}$,
a super-polylog shave): shaves the OR-AND semiring, does NOT transfer to the integer
count-then-max $(+,\times)$ semiring (a discrepancy-guard; AFKLM must not be cited as Max-IP
progress). Rectangular MM (Coppersmith 1982): IS the baseline, its $\log^2 n$ is the polylog
to remove, zero progress. Jin-Xu large sieve (STOC 2024, arXiv:2403.20326): scope is sparse
convolution + 1D Hamming, not applicable. Exact integer geometry (Matousek 1992; AESW 1991;
Yao 1982; Williams SODA 2018): $n^{2-1/O(d)}$, at $d=n^\varepsilon$ a $1+o(1)$ saving, under
one log. The SMALLEST GAP, two readings that disagree (the disagreement IS the finding): by
literal-object closeness, rectangular MM is first (the baseline, one polylog away in form,
shaves zero); by largest-actual-saving, the polynomial method is first (a real constant, wrong
shape). No technique is both close in form AND making log-progress. Precisely: shave the
intrinsic $\log^2 n$ off $n^{2+o(1)}$ rectangular MM at the Coppersmith $\alpha$-boundary for
the $(+,\times)$-max product, without enumerating the $n^2$ pairs.

THE MICRO-IDEA (reported as a precise FAILURE, the expected valuable negative). Threshold
sweep: sweep $t$ from $d$ down and test existence of a pair with $\langle a,b\rangle \ge t$,
the max being the largest YES; or binary-search $t$. Implemented and run
(`threshold_sweep_micro_idea`, $n_A=n_B=40$, $d=12$): CORRECT (returns the true max, asserted)
but does NOT shave. It breaks at the existence-query subroutine: each query at
$d=n^\varepsilon$ is itself the open $n^\varepsilon$ wall (certifying a NO rules out all $n^2$
pairs), so the LINEAR sweep multiplies the baseline by $O(n^\varepsilon)$ (a polynomial factor
WORSE) and BINARY search ADDS a $\log$ factor rather than removing the polylog. Reducing Max to
existence does not help because existence at $d=n^\varepsilon$ is the same open wall.

THE BARRIER VERDICT: open-and-attackable, no finer unconditional barrier. The decisive check:
the strongest "hardness of shaving logs" theorems (Abboud-Hansen-V.Williams-R.Williams STOC
2016 arXiv:1511.06022; Abboud-Bringmann ICALP 2018 arXiv:1804.08978) are proved ONLY for
SEQUENCE/alignment problems whose quadratic DP encodes a branching program; they provably do
NOT cover OV or Max-IP, so the candidate finer barrier does not bind. The Chen implication runs
shave-implies-lower-bound with no proven converse, so it is a WANTED route, not an obstruction.
Two finer obstructions, neither a proved barrier: the matrix-output wall (scoped to $A B^\top$,
pins where a new idea must act) and the inherited conditional natural-proofs collision (on the
RESULTING lower bound, not the algorithm; finding 20 / note section 6). PROJECT-INFERENCE
TARGET-WIDENING (carry as a hedge, VERIFIER tagged needs-citation): the connection needs only a
co-nondeterministic THR-of-MAJ UNSAT (or Max-IP-decision) log-shave (Chen Remarks 2.7/4.2 as
read by the survey; the verbatim remark text was not independently web-confirmed this pass),
wider than the stated deterministic hypothesis. The single most promising angle is transferring
the $n^3$-scale all-logs machinery (the STOC 2024 BMM regularity decomposition, or the STOC 2014
Razborov-Smolensky min-plus method) DOWN to the $n^2$-scale thin $n \times n^\varepsilon$
count-then-max product; this pass found no transfer and claims no progress.

STATUS. As of June 2026 NEXP not in poly-size THR-of-THR remains OPEN; no algorithm meets the
bar. Source: [`circuit_complexity/e_maxip_logshave.py`](circuit_complexity/e_maxip_logshave.py)
(exit 0, smoke 5/5) and the new subsection 4b of
[`2050_tc0_hinge_grounded.md`](../docs/03_research/2050_tc0_hinge_grounded.md).

### 25. The TC0-PRF natural-proofs collision does NOT doom the Williams route: it binds the LARGE-and-constructive alternatives (which is why a non-natural method is needed), the spine is non-natural by non-largeness, and the open locus flips to non-constructivity at the NEXP-to-NP descent.

The project had propagated (findings 20, atlas, STATE, note section 6) that "natural
proofs is plausibly the BINDING constraint at dense TC0, because that class likely
computes PRFs." A three-survey + builder + adversary + verifier pass (VERIFIER overall
high, every load-bearing claim web-confirmed verbatim; ADVERSARY sound-with-fixes; the
synthesizer agent failed to emit structured output and the deliverable was recovered
from the run journal and authored by hand) confronts the deepest strategic question and
CORRECTS that framing as too pessimistic, while guarding against the opposite overclaim.

THE CORRECTION. Razborov-Rudich requires a property that is LARGE AND constructive (the
checker encodes this: is_natural = largeness AND constructivity). The earlier phrasing
"any constructive lower-bound method collides" was the error: a NON-LARGE constructive
method does NOT collide. Williams 2013 ("Natural Proofs versus Derandomization", STOC
2013 / SICOMP 2016, Thm 1.1) proves CONSTRUCTIVITY IS UNAVOIDABLE for NEXP lower bounds
(verbatim: "Constructivity is unavoidable, even for NEXP lower bounds"; NEXP not in C
iff a poly-time property distinguishes SOME function from all C-circuits, the
"some function" = at-least-one = non-large reading). So the Williams algorithm-to-lower-
bound method evades natural proofs by DROPPING LARGENESS, not constructivity. A
non-large property carries no distinguishing bias against a PRF, so the PRF collision is
SILENT on the Williams route. The collision DOOMS the LARGE-and-constructive
(combinatorial / correlation / approximate-degree) ALTERNATIVES, which is exactly WHY a
non-natural method is required (ACW 2016, Chen-Tell 2019: TC0 bounds "may require
non-natural proofs"). The "binding constraint" framing inverted the direction: the wall
selects the non-natural route, it is not an obstruction to it.

THE RESIDUAL SUBTLETY (why the verdict is SUBTLE, not cleanly EVADED). At the
NEXP-to-NP DESCENT the bespoke non-large Williams property ("is this THE hard function")
is unavailable for a generic NP target. The candidate replacement is the meta-complexity
high-Kt device, but high-Kt-ness IS LARGE (Shannon counting: most truth tables are
incompressible). A large property can stay non-natural only by being NON-CONSTRUCTIVE
(deciding high Kt is MCSP/MKTP-hard). So at the descent the escape lever FLIPS from
largeness (Williams) to non-constructivity (meta-complexity), and that non-constructivity
against TC0 for the EXACT descent truth tables is OPEN: restricted/partial MCSP variants
are NP-hard non-relativizingly (Hirahara 2022), but the exact object is not. The smallest
breaking case: if a builder needing an efficiently-checkable descent certificate reaches
for a constructive hardness statistic (average sensitivity, approximate degree, spectral
norm), that is large+constructive = natural, and the PRF collision bites it. So "evaded"
is robust at the NEXP-level bound and one unproved non-constructivity claim away from
"doomed at the descent."

THE DIVISION OF LABOR (finding 12, reconfirmed). Meta-complexity supplies
NON-NATURALNESS only (via the non-constructive high-Kt object); it does NOT supply
non-relativization. Hirahara's 2018 non-black-box worst-case-to-average-case reduction
still RELATIVIZES (ECCC TR18-138 Section 1.7, verbatim: "our proofs do relativize"), so
the non-relativizing and non-algebrizing content must come from the Williams spine. The
experiment's metacomplexity_w2a_core_alone fixture HITS relativization, encoding this.
"Meta-complexity threads natural proofs at TC0" is PARTIAL: justified as the candidate
non-naturalness engine for the descent (escaping via non-constructivity), but the
non-constructivity is partially proved (restricted variants) and open for the exact
object, not a discharged repair.

FIXTURE CORRECTION. The shared `barriers.py` williams_acc0 fixture had
natural_constructivity=False and notes calling the diagonalization "non-constructive",
both wrong per Williams 2013. Corrected to natural_constructivity=True with notes
"non-natural by dropping largeness, not constructivity"; is_natural stays False (largeness
clears it), smoke test stays 5/5.

OVERCLAIM GUARDS (carried). "Non-natural by construction" should read "non-natural by the
ACC0 template, contingent on the dense-TC0 SAT algorithm existing" (the SAT algorithm
findings 20/23/24 do not yet exist). The PRFs-in-TC0 premise is itself CONDITIONAL
(Naor-Reingold under factoring/DDH; Miles-Viola candidates), which is a further reason the
collision does not unconditionally doom anything. The relativizes/algebrizes=False flags on
the combined route are assumptions (algebrization remains NOT YET ASSESSABLE, note section
6). And the correction must NOT be read as "the natural-proofs wall is gone": it still binds
every combinatorial/natural method, and the descent may still need it. Net: the genuine open
obstruction on the leading path is the ALGORITHMIC one (the dense THR-of-THR SAT / Max-IP
log-shave) plus the descent's non-constructivity question, NOT natural proofs at the
NEXP-level bound. Source:
[`natural_proofs/e_tc0_prf_collision.py`](natural_proofs/e_tc0_prf_collision.py) (exit 0,
smoke 5/5), the corrected `barriers.py` williams_acc0 fixture, and the framing corrections
in the atlas, STATE, note section 6, and finding 20.

### 26. The leading path's descent to NP is a MULTI-JOINT synthesis (not one missing piece): four open joints, the binding one is the non-constructivity wall (deciding MCSP is capped at AC0[p], cannot reach TC0 = the locality barrier); and the NP easy-witness lemma is PROVED, so the descent block is the algorithm scale, not a circularity.

A multi-agent pass (the meta-complexity survey survived; two surveys hit the recurring
StructuredOutput failure; builder ledger + adversary + verifier completed; VERIFIER
overall high, every load-bearing claim web-confirmed verbatim; ADVERSARY sound-with-fixes,
the one substantive fix applied) mapped whether the leading path actually reaches NP, which
is what a real P-vs-NP proof needs. Verdict: the descent to NP is a SYNTHESIS with FOUR
open joints, not a one-missing-piece program; the path does not close, and the joints are
coordinates. Modeled in
[`circuit_complexity/e_leading_path_descent.py`](circuit_complexity/e_leading_path_descent.py)
(a descent-ladder ledger; exit 0, smoke 5/5).

THE LADDER. The Williams connection is PROVED at NEXP (Williams 2011) and NQP
(Murray-Williams 2018, NQP not in $n^{\log^k n}$-size ACC-of-THR). It does NOT reach NP. It
delivers its bound at NQP because the only available speedup is a one-bottom-layer
ACC-of-THR SAT algorithm; the lower bound, not the witness lemma, is what stops at NQP.

THE FOUR JOINTS (one grind, the rest structural):

- **J1 ALGORITHMIC** (quantitative GRIND, attackable now): the dense depth-2 THR-of-THR /
  Max-IP log-shave (findings 23/24). No finer unconditional barrier; SETH-consistent. The
  clearest near-term handle.
- **J2 DESCENT / SCALE** (structural, but largely DOWNSTREAM of J1). CORRECTION to the
  dossier's A2 kill and the builder's first draft: the NQP-to-NP block is NOT a witness
  circularity. Murray-Williams 2018 PROVED the NP easy-witness lemma (if NP in SIZE[$n^k$]
  then NP verifiers have $n^{O(k^3)}$ witness circuits), overcoming IKW 2002 (NEXP-only,
  confirmed verbatim against ECCC TR17-188). The connection stops at NQP because of the
  ALGORITHM-plus-DIAGONALIZATION scale: an NP-scale dense-TC0 SAT algorithm would fire the
  EXISTING NP easy-witness lemma. So J2 is entangled with J1, not an independent circularity.
- **J3 NON-CONSTRUCTIVITY** (structural BARRIER, THE binding joint). The descent needs a
  PROVED non-constructivity of high-Kt / MCSP / MKTP against TC0 for the exact total truth
  tables (deterministic, unconditional). It is ASPIRATIONAL, blocked by a NAMED WALL: lower
  bounds on DECIDING MCSP are capped at AC0[p] (Golovnev-Ilango-Impagliazzo-Kabanets-
  Kolokolova-Tal, ICALP 2019 / ECCC TR19-018, verbatim: MCSP needs depth-$d$ AC0[p] of size
  $\exp(N^{0.49/d})$) and CANNOT reach TC0, because MAJORITY $\in (\mathrm{AC}^0)^{\mathrm{MCSP}}$
  and $\mathrm{NC}^1 \subseteq (\mathrm{AC}^0)^{\mathrm{MCSP}}$, so "MCSP hard for TC0" would
  separate NC1 from AC0. This is the LOCALITY BARRIER (Chen-Hirahara-Oliveira-Pich-Rajgopal-
  Santhanam, "Beyond Natural Proofs: Hardness Magnification and Locality", ITCS 2020 / JACM
  2022, arXiv:1911.08297). All proved meta-complexity hardness is on FOUR separately-open
  axes from the descent object: variant (MCSP*/MKTP*/MINKT*) not total; randomized not
  deterministic (Hirahara 2022 calls deterministic NP-hardness "extremely difficult");
  conditional not unconditional (Santhanam 2020 Universality Conjecture; Hirahara 2023 NP
  not in io-P/poly); and about NP or P/poly, NEVER about TC0 as the deciding class. The
  dossier's own critical path already lists defeating this as the unbuilt 2044-2047 object.
- **J4 COMPOSITION** (structural, PARTIAL). Meta-complexity supplies non-naturalness ONLY;
  its W2A core RELATIVIZES (Hirahara 2018, ECCC TR18-138 Section 1.7, "our proofs do
  relativize"), so non-relativization + non-algebrization come from the spine (findings 12,
  25). The division of labor is real (so "partial", not open-from-scratch), but there is NO
  COMBINING THEOREM that fuses (spine carries relativization/algebrization) with
  (meta-complexity carries non-naturalness via non-constructivity) into a single all-three-
  evading NP proof. A further audit flag: the graft's algebrization is ASSUMED, not assessed
  (dense-TC0 algebrization is NOT YET ASSESSABLE, finding 20), so "evades all three" for the
  graft is contingent on FIVE items, not four.

NET. The genuinely-independent hard structural barriers are J3 (its own named locality wall)
and J4 (no combining theorem); J1 is a grind and J2 is largely downstream of it. The single
most binding obstruction to a genuine NP lower bound is J3, the non-constructivity wall, a
named published no-go (locality), NOT a quantitative grind. The honest read: the leading path
is a coherent program with a clearly-attackable algorithmic joint and a binding structural
barrier (locality) that the field has not breached and the dossier itself flags as unbuilt.
Source: [`circuit_complexity/e_leading_path_descent.py`](circuit_complexity/e_leading_path_descent.py)
and the descent-map corrections to the dossier A2 framing.

### 27. Attacking J1: the n^3-scale all-logs machinery does NOT transfer to the Max-IP log-shave, for an OPERATION reason (not scale); the real frontier is the fused-max-MM, which is open and barrier-free. Sharpens finding 24.

Finding 26 named J1 (the dense THR-of-THR / Max-IP log-shave) as the leading path's one
attackable joint, and finding 24's most-promising angle was to transfer the $n^3$-scale
all-logs machinery DOWN to the $n^2$-scale count-then-max product. A dedicated pass (3
surveys, builder ledger, adversary, verifier; all completed, VERIFIER overall high,
ADVERSARY verdict SOUND, every machinery parameter web-confirmed verbatim 2026-06-04)
attacked that transfer and lands a sharp, honest coordinate, with no progress on the prize.

THE TRANSFER FAILS, FOR AN OPERATION REASON (not scale). Max-IP is a standard $(+,\times)$
product $M = A B^\top$ (entries the integer counts $\langle a,b\rangle \in \{0,\dots,d\}$)
followed by ONE global MAX over all $n^2$ OUTPUT entries. That is neither machinery's
operation. (i) AFKLM STOC 2024 ($n^3/2^{\Omega((\log n)^{1/7})}$, arXiv:2311.09095) shaves
TRIANGLE DETECTION via an OR-idempotent collapse: a dense uniform regular piece certifies
"some entry is nonzero" hence a triangle "without the need to compute anything further"
(Sec 3, verbatim). That one-bit existence collapse discards exactly the per-entry integer
counts a MAX needs (a max distinguishes count 5 from 6; the collapse cannot). The authors
themselves leave the non-Boolean / $(\min,+)$ generalization explicitly open ("min does not
have an inverse"). (ii) Williams STOC 2014 ($n^3/2^{\Omega(\sqrt{\log n})}$, arXiv:1312.6680)
shaves a $(\min,+)$ PRODUCT: a per-entry reduction over the contraction index $k$ FUSED
into each of the $n^2$ outputs. Max-IP's product step is a plain $(+,\times)$ sum with NO
per-entry reduction to fuse a threshold polynomial into; its lone reduction is the single
global max over the OUTPUT indices, applied AFTER the product (different reductions on
different axes; verified numerically, the $(\min,+)$ matrix's global max is generically not
the Max-IP answer, 5/5 trials disagree). (iii) The ACW polynomial method has the right ring
but dies on SCALE (degree-vs-dimension decay to the constant $2^{O(1/\varepsilon)}$ at
$d = n^\varepsilon$, finding 24).

SHARPEN FINDING 24. The "wrong scale" label on the Williams min-plus row was too weak and
mislocated the primary block; it is "wrong OPERATION (+ scale), operation primary". The
AFKLM / four-Russians row sharpens from "shaves the OR-AND semiring" to "the detection-OR
collapse discards the integer counts the MAX needs (operation + semiring + scale)". Both
are FUNDAMENTAL as transfers of the existing engines (the win-buying mechanism, OR-collapse
or per-entry-fusion, is exactly what is absent for count-then-max), not a tunable parameter.

THE TWO READINGS MUST STAY DISTINCT (the audit's load-bearing nuance). "Fundamental" means
fundamental to transferring THESE engines, NOT a barrier on the target problem. The real
frontier, the FUSED-MAX-MM (compute $\max_{ij}(A B^\top)_{ij}$ for small-range entries at
thin $d = n^\varepsilon$, fused into the rectangular MM, without materializing the $n^2$
entries), is OPEN at the log-shave scale, SETH-consistent ($n^{2-o(1)}$), and barrier-free
(the strongest log-shaving-hardness theorems, Abboud-Hansen-VW-RW 2016 / Abboud-Bringmann
2018, provably cover only sequence/alignment, not OV/Max-IP). No known fused product touches
it: dominance ($n^{2.69}$, Matousek), $(\max,\min)$/bottleneck (Vassilevska-Williams-Yuster
ToC 2009; Duan-Pettie), and bounded-range $(\min,+)$ (ESA 2024) are POLYNOMIAL speedups at
$n^3$ full-square, per-entry, not a log-shave at thin dimension. Bichromatic Max-IP IS
truly-subquadratic EQUIVALENT to OV (Chen, SODA 2019, arXiv:1811.12017), but at the
polynomial $n^{2-\Omega(1)}$ granularity, so it neither delivers a log-shave nor lets OV/SETH
rule one out.

THE MICRO-IDEA (a precise FAILURE, the expected negative). A small-range block pre-filter:
partition $A, B$ into blocks; per block-pair compute a cheap column-overlap upper bound on
its max inner product (count columns active in both blocks); skip the full block product if
the bound $\le$ best-so-far. Implemented and CORRECT, but it does NOT shave worst-case: the
block CONTAINING the global max can never be pruned, and on dense data the overlap bound is
loose ($\sim d$), so it computes all $n^2$ inner products (measured: 0 of 36 block-pairs
pruned). Sparse-instance pruning is instance-LUCK, not a worst-case bound. Like the
threshold-sweep (finding 24), it fails because the global argmax can sit at any pair.

NET. J1's frontier is sharpened from "transfer the $n^3$ machinery" (a fundamental operation
mismatch) to "build a fused-max-MM log-shave" (open, no machinery known to touch it, the
structural novelty must be max-extraction-without-enumeration: a succinct certificate of a
standard product's global max). Source:
[`circuit_complexity/e_j1_transfer.py`](circuit_complexity/e_j1_transfer.py) (exit 0, smoke
5/5; two sibling scratch experiments consolidated into it) and the sharpened technique map
in subsection 4b of
[`2050_tc0_hinge_grounded.md`](../docs/03_research/2050_tc0_hinge_grounded.md).

### 28. J1 BUILT: the fused-max-MM log-shave attacked as four candidate constructions; all four hit ONE shared, exactly-identified wall (fast bulk aggregation cannot read the $\ell_\infty$ extreme to unit precision), and the avenue is confirmed barrier-free. Extends finding 27.

Finding 27 sharpened J1 from "transfer the $n^3$ machinery" to "build a fused-max-MM
log-shave: compute $\max_{ij}(A B^\top)_{ij}$ for small-range entries at thin
$d = n^\varepsilon$, fused into the rectangular MM, without materializing the $n^2$
entries; the structural novelty must be max-extraction-without-enumeration." A dedicated
pass (3 surveys, 4 builder constructions, adversary on each, verifier; all completed,
every proved parameter web-confirmed against its venue, two adversary verdicts
SOUND-BARRIER-FREE and two NEEDS-REVISION with all corrections applied and re-verified)
BUILT that frontier as four natural constructions and lands four precise, honest
NEGATIVES, with no progress on the prize.

THE FOUR NATURAL MACHINERIES (each a genuine subquadratic fusion that avoids the $n^2$
materialization). (B1) MOMENT / tensor-power: the $p$-th power-sum moment factors as one
inner product in dimension $d^p$, $m_p = \sum_{ij}\langle a_i,b_j\rangle^p = \langle
\sum_i a_i^{\otimes p}, \sum_j b_j^{\otimes p}\rangle$ (fusion identity verified exactly
to $10^{-6}$); try to read the max off $m_1..m_P$. (B2) SPECTRAL / low-rank: the
rotation-invariant $\ell_2$ toolbox of the factors (Frobenius $\|M\|_F^2 = \mathrm{tr}
((A^\top A)(B^\top B))$, spectral norm, full spectrum via the $d\times d$ core, row
2-norms), all in $O(n d^2) = n^{1+2\varepsilon}$; try to bracket the max. (B3)
COUNT-PRESERVING REGULARITY: rebuild AFKLM/Kelley-Lovett-Meka to keep the integer
codegree counts instead of collapsing to a one-bit OR, partition into regularity blocks,
read each block's max off its average density $\rho_{s,t} d$. (B4) SKETCH / heavy-hitter:
Pagh compressed matrix multiplication (ITCS 2012, arXiv:1108.1320) plus count-sketch
heavy-hitters (Charikar-Chen-Farach-Colton ICALP 2002), localize the argmax as an
$\ell_2$-heavy entry.

THE ONE SHARED WALL (the bulk-vs-extreme wall). Every one of the four fuses a BULK
statistic of the $n^2$ inner products: an $\ell_2$ / average / low-moment / spectral /
Frobenius quantity that controls the typical entry. The Max-IP answer is an $\ell_\infty$
/ extreme / large-deviation quantity (the single most-deviant entry). The two live on
opposite sides of a quotient each fusion collapses. B1: $P$ moments span only degree-$\le
P$ polynomials of the entry value, and the top-value indicator needs degree $\ge d$
(information-theoretic Vandermonde bound, exact-arithmetic: matching $m_1..m_K$ leaves the
max free iff $K \le d-1$, witness $X=\{3,1,1,1\}$ vs $Y=\{2,2,2,0\}$ share $m_1=6, m_2=12$
but max $3$ vs $2$). B2: spectral aggregates are rotation-invariant, blind to the
$\ell_\infty$ coordinate (equal-spectrum spread-vs-spike pair, max-ratio EXACTLY $n$). B3:
regularity certifies block AVERAGES to additive $\varepsilon_{reg} d$, blind to a planted
cell that moves every density by $O(1/n)$ while moving the max by $\Theta(d)$. B4: the
dense argmax is $\ell_2$-LIGHT (heaviness ratio $\Theta(1/n^2)$), so a Frobenius sketch
cannot isolate it. The sharp common form (the adversary's load-bearing correction to B2,
verifier-endorsed): the binding constraint is NOT any one engine's multiplicative window
but the INTEGER-GAP-1 RESOLUTION plus ARGMAX LOCALIZATION the THR-of-THR connection
demands. Resolving max from $\text{max}-1$ to unit precision against an adversarial bulk
parked at $d-1$ forces the cost back to super-quadratic (B1 needs $P = \Omega(n^\varepsilon
\log n)$ moments at cost $n^{1+\omega(1)}$; B3 needs $2^{\Omega(n^{2\varepsilon})}$
regularity blocks) or to the $n^2$ baseline (B2 and B4 collapse to the enumeration scan on
dense data). One unit of extreme-value resolution is exactly what every bulk aggregation
discards to be fast.

TWO ADVERSARY CORRECTIONS, BOTH APPLIED AND RE-VERIFIED (the honesty discipline working).
(i) B2's "rotation-invariant $\Rightarrow \Theta(n)$ window $\Rightarrow$ dead" story was
internally inconsistent: a cheap NON-invariant per-factor-row Cauchy-Schwarz bound is
multiplicatively tight ($1.00\times$ to $1.24\times$ on dense Boolean data versus the
spectral norm's $56.8\times$ to $848\times$), so the window is not the wall; the operative
wall is the enumeration wall (gap-1 resolution + localization), the same as B1/B3/B4. The
"spectral certificate is doubly barrier-blocked (natural AND algebrizing)" claim was a
category error: those barriers act on a lower-bound proof object, not on an algorithmic
log-shave. (ii) B4's second claimed obstruction, "one-sparse recovery forces sketch
dimension $\Omega(n^2)$", was MIS-DERIVED: deterministic for-all 1-sparse recovery needs
only $\lceil\log_2 N\rceil+1$ linear measurements (bit-encoding matrix, demonstrated in $9$
rows for $N=256$), and the exhibited collision existed only because the sketch hand-zeroed
the target column. $M$ is dense and the DIFFERENCE is 1-sparse; recovering a 1-sparse
difference is cheap. The sound binding wall is the $\ell_\infty$-from-$\ell_2$ lightness
alone: gap-1 resolution needs $s > \|M\|_F^2/\mathrm{gap}^2 = \Theta(n^2 d)$, a factor $d$
WORSE than baseline.

BARRIER-FREE, CONFIRMED. No published result blocks the avenue. The two strongest
log-shaving-hardness theorems (Abboud-Hansen-V.Williams-R.Williams STOC 2016,
arXiv:1511.06022; Abboud-Bringmann ICALP 2018, arXiv:1804.08978) provably cover only
sequence/alignment problems whose quadratic DP simulates a branching program, not
OV/Max-IP. The OV-equivalence (Chen-Williams SODA 2019, arXiv:1811.12017) and the SETH
lower bound (Chen, ToC 2020, arXiv:1802.02325) hold only at polynomial granularity
$n^{2-\Omega(1)}$; the bar $n^{2-o(1)}$ sits strictly inside the SETH-permitted band.
Newly surfaced same-direction corroboration: Williams FOCS 2024 / SICOMP 2025 (ECCC
TR24-142) makes the OV log-shaving regime a WANTED route to $\mathsf{E}^{\mathsf{NP}}$
lower bounds against depth-two threshold circuits, the opposite of a barrier. The target
(Chen 2018, arXiv:1805.10698, Thm 1.5 item 1) is a WANTED implication and $\mathsf{NEXP}
\not\subseteq$ poly-size THR-of-THR is open as of 2026.

NET. J1's frontier is sharpened from "no machinery is known to touch it" (finding 27) to
"FOUR natural machineries touch it, all hit ONE shared quantified wall, and the precise
missing property is named." A winning fused-max-MM log-shave must be a subquadratic
aggregation that is SENSITIVE TO A SINGLE EXTREME ENTRY at unit integer resolution: it
must distinguish two factored instances whose products differ in exactly one cell by one
unit, without enumeration, with a worst-case (not constant-relative-gap) guarantee, and it
must be NON-LINEAR in the product entries. No candidate and no surveyed positive technique
has this: the published positive max-of-low-rank-via-MM methods (Valiant FOCS 2012;
Karppa-Kaski-Kohonen TALG 2018, arXiv:1510.03895; Alman SOSA 2019) are gap-dependent and
collapse to $n^{2-o(1)}$ on dense gapless data, the exact THR-of-THR-forcing regime.
Source: [`circuit_complexity/e_fused_max_mm.py`](circuit_complexity/e_fused_max_mm.py)
(exit 0, smoke 5/5; consolidates the four candidate models) and subsection 4c of
[`2050_tc0_hinge_grounded.md`](../docs/03_research/2050_tc0_hinge_grounded.md). No speedup
claimed; no progress on the prize.

### 29. The bulk-vs-extreme wall is HARDENED into a single-round cheap-measurement lower bound; the escape is RELOCATED to adaptive / multi-round / metric methods, and the most promising one (the closest-pair reframe) is shown to target the genuine hard instance but decay at $d = n^\varepsilon$. Extends finding 28.

Finding 28 stated the bulk-vs-extreme wall as a HEURISTIC verified on four oblivious
fusions (B1 moment, B2 spectral, B3 regularity, B4 sketch). A dedicated first-principles
pass (3 surveys reading the Chen-2018 reduction internals plus the closest-pair and
sketching literature directly, four attack prongs each with a runnable model, four
adversary audits, a verifier) attacked the wall from its four weak points (W1 information
vs computation, W2 the 1-sparse loose thread, W3 top-of-spectrum-is-closest-pair, W4
single-round vs adaptive). NET OUTCOME: the wall BOTH hardened and cracked. It hardened
from "four methods fail" to "ALL single-round cheap measurements provably fail" (an
in-model lower bound over a class that subsumes B1-B4). It cracked only at the level of
the slogan: the literal claim "every fast method is a bulk aggregation" is FALSE
(thresholded Max-IP literally IS bichromatic Hamming closest-pair, a metric method), but
the metric method decays at $d = n^\varepsilon$ to the same wall. No progress on the prize.

THE HARD INSTANCE IS NEAR-TOP, GAP-1, PLANTED (decisive survey finding, correcting a
citation). The Chen-2018 reduction forces Max-IP to be decided ONLY at the very top, at a
single planted ceiling $M$, with an integer gap of exactly $1$: Corollary 5.5 and Lemma
5.1 of arXiv:1805.10698 build the gadget on $P(x,y) = (x\cdot y - m)^2$, giving
$d_x(x)\cdot d_y(y) = P(x,y) + 2dm - m^2$ with ceiling $M_{d,m} = 2dm - m^2$, so
$\mathrm{Max}(A,B) = M$ iff a circuit sub-instance is satisfiable and $\le M-1$ otherwise
(a squared nonzero integer is $\ge 1$). The decision is exact-at-the-top: is there a
bichromatic pair hitting the ceiling? Chen Theorem 1.1 lists Bichromatic-Closest-Pair in
the SAME equivalence class, so the W3 metric reframe targets the genuine hard instance,
not a strawman. CITATION FIX (survey-flagged, now applied across the docs): arXiv:1805.10698
is "Toward Super-Polynomial Size Lower Bounds for Depth-Two Threshold Circuits"; the
Max-IP-hardness / SETH paper is the SEPARATE arXiv:1802.02325 (ToC v016a004, CCC 2018).
Theorem 1.5 genuinely lives in 1805.10698, so the target statement was correct; only the
docstring title was wrong. The co-nondeterministic widening (Remarks 2.7 / 4.2) makes the
OUTER UNSAT algorithm co-nondeterministic (to derandomize Structure Lemma II by guessing
primes); it does NOT relax the Max-IP call to approximate or away-from-top.

THE IN-MODEL LOWER BOUND (the hardened wall). Define the single-round Cheap-Measurement
Model (CMM): before seeing the input, fix $K$ measurements of $M = A B^\top$, each either
(a) a separable / low-rank linear functional $\langle W_k, M\rangle$ with $W_k = \sum_{l\le
r} u_{k,l} v_{k,l}^\top$ (a rank-$1$ $W$ pushes through as $(u^\top A)(B^\top v)$ at
$O(nd)$, a rank-$r$ at $O(rnd)$; subquadratic forces total rank $R = o(n^2/d)$), or (b) a
degree-$\le D$ entry-symmetric statistic $\sum_{ij} g(M_{ij}) = \sum_p c_p m_p$ (the
tensor-power moments; cheap iff $D < 1/\varepsilon$), or (c) a rotation-invariant spectral
statistic $f(\sigma_1,\dots,\sigma_d)$ from the $d\times d$ core $A^\top A, B^\top B$ at
$O(nd^2)$ (the CONTAINMENT PATCH the adversary required: $\sigma_{\max}$ and the full
spectrum are cheap, non-separable, AND non-entry-symmetric, so they need their own family).
THEOREM (CMM blindness): no single-round CMM of subquadratic budget resolves
$\mathrm{max} = d$ vs $\mathrm{max} \le d-1$ over rank-$\le d$ Boolean products. Three
branches, each with a verified witness. (i) SEPARABLE-LINEAR: the two instances differ by
a $1$-sparse perturbation $E_{i^\star j^\star}$ realizable in factored form at rank $\le d$;
an oblivious linear readout changes by $(W_k)_{i^\star j^\star}$, and the argmax cell is
$\ell_2$-LIGHT, $\mathrm{argmax}^2/\|M\|_F^2 = \Theta(1/n^2)$ (measured ratio$\cdot n^2$ in
$[3.0, 8.4]$, $d$-independent). Two distinct floors (the adversary's prose patch, both
sound): a LOCALIZATION floor $1/\mathrm{heaviness} = \|M\|_F^2/\mathrm{argmax}^2 =
\Theta(n^2)$ and the Price-Woodruff $\ell_\infty$-from-$\ell_2$ ESTIMATION floor $\dim \ge
\|M\|_F^2/\mathrm{gap}^2 = \Theta(n^2 d^2)$ (Price-Woodruff, ICALP 2012, arXiv:1206.5725).
Separable $W$ are a SUBSET of all linear sketches, so the floor transfers a fortiori, and
turnstile $=$ linear-sketch (Li-Nguyen-Woodruff, STOC 2014) makes it a genuine streaming
SPACE lower bound, not a model artifact. (ii) SYMMETRIC: $\sum_{ij} g(M_{ij})$ is a linear
functional of the value histogram $h_0,\dots,h_d$ determined by $m_0..m_D$; deciding
$\mathrm{max}=d$ is reading $h_d \ge 1 = $ the indicator $[v=d] = \binom{v}{d}$, a
polynomial of degree EXACTLY $d$ (the Vandermonde / Lagrange indicator). A degree-$D < d$
statistic lies in the $(d-D)$-dimensional Vandermonde nullspace; exact-rational witness
$\{3,1,1,1\}$ (max $3$) vs $\{2,2,2,0\}$ (max $2$) share $m_1=6, m_2=12$ and split first at
$m_3$ ($30$ vs $24$). Affordable $D < 1/\varepsilon$ (a constant) vs needed $d = n^\varepsilon
\to \infty$. (iii) SPECTRAL: an equal-spectrum collision at the gap-1 top (spectrum
$(2,0,0)$ realized by both a max $=d=2$ and a max $=d-1=1$ Boolean product; $594$ such
collisions in a $3\times 3$ $d=2$ census), so rotation-invariance is blind by symmetry.
The heaviness wall SURVIVES on the actual Chen gadget matrix after removing the rank-$1$
offset $2dm - m^2$ (residual ratio$\cdot n^2 = 1.25$), closing the "maybe the real
instances are easier" objection.

THE 1-SPARSE LOOSE THREAD (W2), RESOLVED HONESTLY. Finding 28's B4 correction noted
deterministic for-all $1$-sparse recovery is $O(\log N)$, which seemed to threaten the
sketch wall. The honest resolution is NOT non-separability: for power-of-two $n$ the
bit-encoding rows ARE rank-$1$ (separable), since bit $b$ of the flat index $i\,n+j$ is a
pure bit of $i$ or of $j$. The bit-sketch is excluded for two correct reasons: (R1) it is a
$1$-sparse DECODE that returns the row-SUM (value row $255$), not the max ($3$), on dense
$M$; (R3) you hold one instance, not a difference, so "recover the $1$-sparse difference" is
unposable single-shot. The cheap $\Rightarrow$ separable framing is itself a strict
overstatement (the $d\times d$ cores give cheap NON-separable functionals such as
$\|M\|_F^2 = \mathrm{tr}(A^\top A\, B^\top B)$), so the correct binding mechanism is
cheap-from-factored $\Rightarrow$ BULK (low-degree-symmetric / rotation-invariant)
$\Rightarrow$ blind, NOT cheap $\Rightarrow$ separable.

THE ESCAPE LOCUS (what the bound does NOT cover). The CMM is single-round and oblivious;
its branch-(i) counting argument USES obliviousness (the $W_k$ are fixed before the argmax
cell is known). The bound provably does NOT cover ADAPTIVE / MULTI-ROUND measurement, where
round $t$'s measurement is a function (ideally non-linear) of rounds $1..t-1$. Two prongs
probed the escape and BOTH came back negative-but-instructive, locating the wall more
precisely. W4 ADAPTIVE BRANCH-AND-BOUND: divide $A, B$ into halves, prune a block when a
cheap upper bound on its max $\le$ the incumbent; cost solves to $n^{\log_2(4(1-f))}$ for
pruned fraction $f$. On the TRUE worst case (every row popcount exactly $d/2$) every cheap
separable certificate (Cauchy-Schwarz, min-popcount, spectral, moment) is additively
$\Theta(d)$ loose (measured gaps $0.5 \to 27.9$ as $d: 8 \to 128$), so the pruned fraction
is EXACTLY $0$ and base-cells$/n^2 = 1.000$ even with an OMNISCIENT true-max incumbent:
$T(n) = 4T(n/2) + \text{cheap} = \Theta(n^2)$, ZERO log-shave. The only additive-$1$-tight
certificate is the block's exact max, a recursive call (circular). The apparent prune on
i.i.d. $p=1/2$ data ($46$-$54\%$) is a popcount-SPREAD artifact (easy gapped data),
neutralized by fixed popcount. This LOCATES the wall as worst-case GAPLESSNESS, not the
single-round restriction. W3 CLOSEST-PAIR: the exact reframe $\mathrm{Ham}(a,b) = |a| + |b|
- 2\langle a,b\rangle$ (verified to the bit) makes thresholded Max-IP exactly bichromatic
Hamming near-neighbor, weight-bucketed, a genuine metric method none of B1-B4 used. But the
closest-pair-specific engine (Alman-Williams, FOCS 2015, arXiv:1507.05106; Alman-Chan-
Williams FOCS 2016, arXiv:1608.04355) IS the same probabilistic-polynomial-of-degree-
$O(\sqrt d)$ $+$ rectangular-MM engine that powers the OV/Max-IP log-shave, with saved time
$n^{2 - 1/O(\sqrt c\,\mathrm{polylog}\,c)}$ at $d = c\log n$. At $d = n^\varepsilon$,
$c = n^\varepsilon/\log n$ grows polynomially and the saved factor decays to $1 + o(1)$
(log-space $\to 0$ by $\log_2 n = 1024$), STRICTLY worse than OV's constant $2^{1/\varepsilon}$
(the metric build adds a $\log^2 c$ surcharge). Every technique that survives to
$d = n^\varepsilon$ (LSH, derandomized LSH, May-Ozerov coding, Alman-Chan offline ANN,
SODA 2020) is $(1+\varepsilon)$-APPROXIMATE and cannot resolve the gap-$1$ exact decision;
exactness is SETH-hard at $d = 2^{O(\log^\star n)}$ (Chen, ToC 2020, arXiv:1802.02325;
Williams SODA 2018). A center-radius certificate gives a RANGE of width $2R$ (measured
$26, 34, 84$), not the gap-$1$ argmax.

THE COMMUNICATION FACE (why the single-round model is the right one and why it stops there).
Chen's exact-Max-IP hardness IS a Set-Disjointness communication theorem (an MA / NP.UPP
protocol plus a CRT dimensionality self-reduction), and Set-Disjointness has tight
$\Omega(n)$ randomized communication (Kalyanasundaram-Schnitger 1992; Razborov, TCS 1992);
the gap-$1$ resolution is exactly the UDISJ promise where the bound bites. The multi-pass
characterization (Ai-Hu-Li-Woodruff, CCC 2016) shows the optimal adaptive turnstile
algorithm is a SEQUENCE of linear sketches, so single-round bounds compose only up to a
$\#$rounds factor and do NOT exclude a polylog-round adaptive method whose per-round
measurement is non-linear in prior answers. The communication transcript is inherently
multi-round, so the prize-relevant escape must be adaptive.

THE UPDATED MISSING PROPERTY (sharper than finding 28). Finding 28 asked for a fast
aggregation sensitive to a single extreme entry at unit resolution, worst-case, non-linear.
Finding 29 sharpens this on three axes. (1) SINGLE-ROUND is now provably insufficient: any
oblivious cheap measurement (separable-linear of total rank $o(n^2/d)$, OR degree-$<1/
\varepsilon$ symmetric, OR rotation-invariant spectral) is blind, so the property must be
ADAPTIVE / multi-round, with round $t$ a NON-LINEAR function of prior answers. (2) The
binding obstruction is worst-case GAPLESSNESS, not bulkness per se: the missing object must
resolve the integer gap on dense data where every entry is $\Theta(d)$ and the max stands
additive $O(1)$ above the bulk (the regime Chen's reduction forces and Valiant/light-bulb
methods cannot reach). (3) The metric reframe is on-target but the engine must achieve
EXACT gap-$1$ at $d = n^\varepsilon$, where every published closest-pair shave either
decays to $1+o(1)$ (exact) or is $(1+\varepsilon)$-approximate. So: an adaptive,
non-linear, exact-gap-$1$, worst-case-gapless extreme-extractor on the low-rank factored
form, ideally exploiting the bichromatic-near-neighbor metric structure. No such object
exists yet.

NET. The front advanced from "four oblivious methods fail" (finding 28) to "ALL single-round
cheap measurements provably fail (the CMM theorem, subsuming B1-B4 plus the spectral patch),
the slogan that every fast method is bulk is literally false (closest-pair is metric), and
the escape is relocated to adaptive / multi-round / metric methods, of which the most
promising is the closest-pair reframe (it targets the genuine near-top gap-$1$ instance) but
it decays to $1+o(1)$ at $d = n^\varepsilon$." Source: the consolidated
[`circuit_complexity/e_fused_max_mm_attack.py`](circuit_complexity/e_fused_max_mm_attack.py)
(exit 0, self-check OK, smoke 5/5; ATTACK-1 hardening with the three-family containment
patch, ATTACK-2 adaptive B&B, ATTACK-3 closest-pair, ATTACK-4 falsifier) and subsection 4d
of [`2050_tc0_hinge_grounded.md`](../docs/03_research/2050_tc0_hinge_grounded.md). No speedup
claimed; $\mathsf{NEXP} \not\subseteq$ poly-size THR-of-THR remains open as of June 2026.

### 30. The single-round bulk-blindness wall (finding 29) EXTENDS to ADAPTIVE multi-round measurement and the deterministic+adaptive wall is now CLOSED against bulk methods; the metric escape is conditionally impossible; the last opening is CO-NONDETERMINISTIC certification, where the $n^2$ relocates to certificate size $=$ Set-Disjointness rectangle-cover $= \Omega(n)$. Extends finding 29.

Finding 29 hardened the bulk-vs-extreme wall to a SINGLE-ROUND cheap-measurement lower bound and relocated the escape to ADAPTIVE / MULTI-ROUND / METRIC / CO-NONDETERMINISTIC methods. A first-principles pass (3 surveys reading the multi-pass streaming, doubling-metric, and NSETH / Merlin-Arthur literature directly, three attack prongs each with a runnable model, three adversary audits, a verifier) attacked all four escape loci. NET: the deterministic+adaptive wall CLOSES against bulk methods, the metric route is conditionally impossible, and the genuine residual frontier is co-nondeterministic certification. No progress on the prize.

THE ADAPTIVE EXTENSION (the closed half). Define an adaptive bulk decision tree: round $t$ picks a query $Q_t$ as a function of answers $a_1..a_{t-1}$, each $Q_t$ cheap-from-factored from one of the finding-29 families (a) low-rank linear, (b) degree-$<1/\varepsilon$ entry-symmetric, (c) rotation-invariant spectral, restricted to an arbitrary sub-block. The single-round CMM theorem is the $K=1$ case. THEOREM (adaptive bulk blindness, communication form): on Chen's gap-1 planted family, deciding $\max(AB^\top)=d$ vs $\le d-1$ is Set-Disjointness on the planted pair's private coordinates ($\Omega(n)$ deterministic communication, Kalyanasundaram-Schnitger 1992; Razborov, TCS 1992), the gap-1 promise being UDISJ. Each cheap bulk round communicates $O(d \log n) = O(n^\varepsilon \log n)$ bits (a block-SUM factors as $\langle \sum_R a, \sum_C b\rangle$, so Alice ships a $d$-vector; this CORRECTS the overstated "polylog per round", adversary-flagged), so an adaptive $K$-round tree is a $K \cdot O(n^\varepsilon \log n)$-bit protocol and $K = \Omega(n^{1-\varepsilon}/\log n)$ rounds are forced, super-polylog and beyond any subquadratic budget. Per-round blindness has TWO mechanisms, not the single "invariance" one. FULL-block bulk queries carry $0$ location bits by invariance (a symmetric statistic changes by a value-only delta, identical for every cell: $m_1{=}1, m_2{=}23, m_3{=}397$ for any cell at $v{=}11$; the spectrum is permutation-invariant, spike@$(0,0)$ and spike@$(1,1)$ both give $(2,0,0)$). But SUB-block queries (what divide-and-conquer actually uses, where invariance FAILS, smallest breaker $n{=}4, d{=}4$) are SNR-floored: spike signal $\sim \sqrt{d\log n}\,d$ is buried in bulk fluctuation $\sim n d^2$, $\mathrm{SNR} \sim \sqrt{\log n}/(n\sqrt d) \to 0$ (measured $5.0\mathrm{e}{-}3, 1.3\mathrm{e}{-}3, 3.2\mathrm{e}{-}4$ at $n{=}64,128,256$). The TOTAL-ADVANTAGE argument: advantage over $K$ adaptive queries $\sim K \cdot \mathrm{heaviness}$, per-block heaviness $\sim C/b^2$ is $d$-INDEPENDENT (max/min across $d \in \{64,256,1024\}$ is $1.00$-$1.02$, $\Theta(1)$ at $b{=}1$, $1.29\mathrm{e}{-}2$ at $b{=}32$); $\mathrm{adv}(K{=}n)$ vanishes ($2.2\mathrm{e}{-}1 \to 3.0\mathrm{e}{-}2$), $\mathrm{adv}(K{=}n^2/4)$ saturates to $\Theta(1)$ ($\sim 3.8$), so any $K=o(n^2)$ gives $o(1)$. The task's proposed mechanism ("spike dominated for $b\ge2$, advantage $\le$ heaviness $\sim K/n^2$") was REJECTED: right direction, wrong reason. An exact bulk query reads the $+1$ exactly (abs tell $= 2d-1$) and heaviness at $b{=}1$ is $\Theta(1)$ not $o(1)$; the real mechanisms are invariance plus SNR-floor plus communication. Streaming corroboration: BGLWWZ (arXiv:2403.20283, Thm 1.6) gives $\Omega(\varepsilon^{-2}\log n / k)$ bits for $k$-pass $L_2$-point-query / heavy-hitters, so at $\varepsilon^2 \sim \mathrm{heaviness} \sim 1/n^2$ the space floor is $\sim n^2/k$, unshakeable by $k = \mathrm{polylog}$ passes; the optimal multi-pass turnstile algorithm is a SEQUENCE of linear sketches (Ai-Hu-Li-Woodruff, CCC 2016), so single-round bounds compose with only a $\#$passes loss.

PROVES-TOO-MUCH CHECK PASSES (the bound uses gaplessness essentially). A single row-aggregate query LOCATES the heavy row on the GAPPED Valiant/light-bulb instance ($z = 25.8, 39.0, 56.4$) but is BLIND on the gapless Chen family ($z = -1.26, 0.03, 0.53$); so the bound does NOT kill Valiant (FOCS 2012). Families (b),(c) are FALSE in the gapped regime (spectral sees the $\Theta(d)$ outlier direction), which is the correct behavior.

TWO HONEST SEAMS (why "closed" is a union, not one lemma). (1) The exact-entry $b{=}1$ read is OUTSIDE the bulk lemmas (an exact entry is not an invariant bulk summary) and is closed by a SEPARATE one-cell-among-$n^2$ adversary bound; per-block exact-Frobenius collisions are not generic at small block size ($5\%$ greedy at $m{=}6, d{=}64$), so the "exactness loophole" closes asymptotically by DOF counting, not a clean per-block identity. (2) Published streaming theorems force a LINEAR per-round sketch and so cover only family (a); the cheap NON-LINEAR families (b)/(c) used adaptively are covered only by strong SIMULATION evidence (a greedy spectral-flavored bulk descent does not localize, per-split bias $+0.040$ at $n{=}64$ collapsing to $-0.010$ by $n{=}256$), not yet by an MIC-style multi-pass information-complexity theorem (BGLWWZ Lemma 1.1, $\mathrm{MIC} \le 2ksn$, is the right tool). So the adaptive extension is "extended with strong simulation support", a theorem for bulk + linear, not yet a theorem for all non-linear per-round measurements.

THE METRIC ESCAPE (P2): BLOCKED and conditionally impossible. The reframe $2\langle a,b\rangle = |a|+|b| - \mathrm{Ham}(a,b)$ (verified $300/300$) makes the gap-1 ceiling decision exactly bichromatic Hamming near-neighbor at fixed radius. But every triangle-inequality structure (cover trees, Beygelzimer-Kakade-Langford ICML 2006, query $O(c^{12}\log n)$; navigating nets, Krauthgamer-Lee SODA 2004) is EXPONENTIAL in the doubling dimension, and $\mathrm{ddim}$ of $n$ Boolean vectors at $d=n^\varepsilon$ on the dense gapless instance is $\Theta(d) = \Theta(n^\varepsilon)$ (measured branching $B = 4/14/28/59$ at $d=4/8/16/24$, the $2^{\Theta(d)}$ signature). An exact query costs $2^{\Theta(n^\varepsilon)}\log n$ per call, worse than the $n^2$ baseline; even the dream case needs $\mathrm{ddim} = \log n - \omega(\log\log n)$, which $\Theta(n^\varepsilon)$ exceeds. The only escape (dimension reduction to $O(\log n)$) is $(1+\varepsilon)$-approximate and destroys the unit gap-1 decision (JL flip rate $0.05$-$0.42$, $\to 0$ only at sketch dim $\sim d^2$). The query is also CIRCULAR (the ceiling-radius near-neighbor query IS the gap-1 sub-decision; counts agree $1{=}1$), though the load-bearing kill is high $\mathrm{ddim}$ plus the SETH/OV exact-hardness floor: exact Max-IP at $d=\omega(\log n)$ is SETH/OV-hard, $n^{2-o(1)}$ (Williams 2005; Chen, ToC 2018, arXiv:1802.02325), and $n^\varepsilon = \omega(\log n)$, so a subquadratic exact metric algorithm would refute OV/SETH. PROVES-TOO-MUCH PASSES (LOCAL cover near the planted pair, not near-identical global $\mathrm{ddim}$): gapped local cover $=1$ (cover tree prunes, Valiant survives), gapless local cover $= 60$-$161 \sim m/2$ (no prune). HITS all three barriers (relativizes, natural via doubling dimension, algebrizes). $P2$ is CLOSED as a route, retained as a corollary feeding the lower-bound prong.

THE CO-NONDETERMINISTIC ESCAPE (P3): WALL-SURVIVES, anatomy is the value. The UNSAT certificate asks whether $N = \tau J - AB^\top$ (rank $\le d{+}1$, factored for free as $L R^\top$, $L = [\mathbf{1}\,|\,A]$, $R = [\tau\mathbf{1}\,|\,{-}B]$) is entrywise nonnegative. The pass FALSIFIED the cheap dismissal "the verifier must read all $n^2$ entries": deterministic equality of two factored rank-$q$ matrices is SUBQUADRATIC via the Gram-trace zero-test $\|PQ^\top\|_F^2 = \mathrm{tr}((P^\top P)(Q^\top Q))$ at $O(n q^2 + q^3) = O(n d^2)$ (returns exactly $0.0$ on equal, $56.0$ on a one-entry perturbation). So a poly($d$)-size nonnegative factorization $N = UV^\top$ ($U,V \ge 0$) would FIRE Chen's connection. The escape closes one level deeper, at the nonnegative rank $r_+(N)$: each rank-1 nonneg term has rectangle support inside $\mathrm{supp}(N)$, so the terms must cover $\mathrm{supp}(N)$ by rectangles avoiding the tight (ceiling-hit) ZERO set, whence $r_+(N) \ge$ the rectangle-cover number $=$ the co-nondeterministic communication cover number of the planted Set-Disjointness predicate $= \Omega(n)$ (fooling set $2^m$, amplified over $n$ row-tests by Chen's CRT self-reduction; measured cover$/n = 0.250$ CONSTANT across $n=32..256$ on the clean permutation tight set). Certificate $U,V$ are $n \times \Omega(n) = \Omega(n^2)$. The $n^2$ thus hides in CERTIFICATE SIZE, traced to the identical Set-Disjointness $\Omega(n)$ root that blocks the deterministic algorithm. Covering ($\Theta(d)$-loose Cauchy-Schwarz, $0$ certifying blocks) and sign-rank ($2^{\Omega(n^{1/4})}$, Chattopadhyay-Mande ECCC TR17-083) die independently. TWO GENUINE OPENINGS, both outside the co-nd model: (1) NSETH does NOT bind at $d=n^\varepsilon$ (Carmosino-Gao-Impagliazzo-Mihajlin-Paturi-Schneider, ITCS 2016, forbids a $(2-\varepsilon)^n$ nondeterministic shave; Chen needs only $2^n/n^k = 2^{n - k\log n}$, far inside the permitted), so a polylog shave is not barred unconditionally, only the $n^2$ floor is; (2) a Merlin-Arthur certificate of size $\Theta(\sqrt n \log n)$ EXISTS for batch-OV / DISJ (Williams, CCC 2016, arXiv:1601.04743; Rubinstein STOC 2018 DISJ MA, which Chen's hardness uses), a real sub-$n$ object, but randomized-verifier; per Chen Remarks 2.7/4.2 the hypothesis admits co-nd not MA, so it is outside scope. The open task is DERANDOMIZING the MA certificate into a pure co-nd one (or proving NSETH-style hardness at the $n^2/n^k$ granularity); the strong direct product theorem for DISJ (Klauck-Spalek-de Wolf; Sherstov) is the concrete wall blocking cheap batching. PROVES-TOO-MUCH PASSES (constant gap $\Rightarrow$ tight set tiny $\Rightarrow$ cover $O(1)$ $\Rightarrow$ small certificate exists, Valiant-consistent). EVADES all three barriers via non-largeness (function-specific).

THE UPDATED MISSING PROPERTY (sharper than finding 29). The deterministic adaptive-search side is now provably blind for bulk methods, so the missing object is no longer a deterministic search; it is a CO-NONDETERMINISTIC certificate for the UNSAT direction: a poly($d$)-size nonnegative factorization of $N = \tau J - AB^\top$, or a derandomization of the $\Theta(\sqrt n \log n)$ MA batch-OV certificate that removes Arthur's coins without re-incurring the $\Omega(n)$ rectangle-cover. It must be NON-ALGEBRIZING (arithmetization gives only the MA object), worst-case-gapless (the cover bound vanishes with a constant gap), and must beat the DISJ strong-direct-product wall. No such object exists yet.

NET. The front advanced from "all single-round cheap measurements fail" (finding 29) to "the wall EXTENDS to adaptive multi-round bulk decision trees (invariance for full blocks, SNR-floor for sub-blocks, Set-Disjointness $\Omega(n)$ forcing $K = \Omega(n^{1-\varepsilon}/\log n)$ rounds), the metric route is conditionally impossible (doubling dimension $\Theta(n^\varepsilon)$ plus exactness, SETH/OV-hard), and the deterministic+adaptive wall is CLOSED against bulk + metric methods, leaving the co-nondeterministic certificate (the harder half of Chen's deterministic-OR-co-nd hypothesis) as the genuine residual frontier, with the $n^2$ there pinned to nonneg rank $=$ Set-Disjointness rectangle-cover $= \Omega(n)$ and the only sub-$n$ certificate being randomized (MA), outside Chen's hypothesis." [CORRECTED by finding 32: the co-nd block is real but MIS-ATTRIBUTED here. The Set-Disjointness SDPT does not apply (Chen's NEXP-direction reduction is single-instance, Lemma 4.3) and the nonneg-rank $= \Omega(n)$ claim was a wrong-set error (the correct tight-free cover of $\mathrm{supp}(N)$ is $O(\log m)$); the real obstruction is the triple-lock UPIT/NSETH $+$ algebrization $+$ prAM-circularity.] Source: [`circuit_complexity/e_fused_max_mm_escape.py`](circuit_complexity/e_fused_max_mm_escape.py) (exit 0, self-check OK, smoke 5/5; P1 adaptive lower bound, P2 metric escape, P3 co-nondeterministic certificate) and subsection 4e of [`2050_tc0_hinge_grounded.md`](../docs/03_research/2050_tc0_hinge_grounded.md). No speedup claimed; $\mathsf{NEXP} \not\subseteq$ poly-size THR-of-THR remains open as of June 2026.

### 31. The non-linear adaptive seam (finding 30) CLOSES for the FULL-block case as a theorem via the sufficient-statistic / data-processing collapse, and the SUB-block case is sharpened from "strong simulation support" to a single NAMED OPEN LEMMA. Extends finding 30.

Finding 30 extended the bulk-blindness wall to adaptive multi-round decision trees but left the non-linear families (b) degree-$<1/\varepsilon$ entry-symmetric and (c) rotation-invariant spectral, used adaptively, as a theorem only "with strong simulation support". This pass discharges the full-block half cleanly and names the precise residual.

THE FULL-BLOCK THEOREM (sufficient-statistic collapse). The repo pivot intuition ("adaptively querying functions of a FIXED instance-determined statistic adds nothing beyond the statistic") is exactly the data-processing inequality applied to a sufficient statistic (Cover-Thomas, *Elements of Information Theory* 2nd ed., Thm 2.8.1 and Sec 2.9: if $T(X)$ is sufficient for $\theta$ then $I(\theta;X)=I(\theta;T(X))$, and for any $g$, $I(\theta;g(T(X)))\le I(\theta;T(X))$). For family (b) the multiset of all degree-$<1/\varepsilon$ symmetric queries is a deterministic function of the fixed moment vector $m=(m_1,\dots,m_D)$; for family (c) every rotation-invariant spectral query is a deterministic function of the fixed $d$-spectrum $\sigma$ of the $d\times d$ core. Both $m$ and $\sigma$ are instance-determined and query-INDEPENDENT, hence sufficient statistics for the planted-cell family. So any adaptive $K$-round tree over functions of $m$ (resp. $\sigma$) carries no more information about the spike LOCATION than one read of the statistic, and finding 30's location-invariance (a $+1$ at any cell moves $m_p$ identically; the spectrum is permutation-invariant) makes that information exactly zero. Verified: the moment vector AND singular spectrum are IDENTICAL across the spike at $(0,0)$, $(b{-}1,b{-}1)$, and off-diagonal $(1,2)$ at $(b,d,D)=(6,12,4),(8,16,4),(12,24,5)$, and an adaptive 3-round $(b)/(c)$ transcript that branches on prior answers is identical across location (Cover-Thomas, $0$ location bits). This is a clean theorem, no MIC machinery needed.

THE SUB-BLOCK NAMED OPEN LEMMA (honestly NOT closed). The Cover-Thomas collapse is exact only when the statistic is genuinely query-INDEPENDENT. An adaptive tree that CHOOSES which sub-block to read accumulates a statistic that is itself adaptive (a growing collection of sub-block spectra/moments chosen as a function of past answers), so it is not a single fixed sufficient statistic and the collapse does not apply. The per-query advantage is SNR-floored ($\mathrm{SNR}=(2d{-}1)/\text{fluctuation}\sim 1/b$, heaviness $\sim 1/b^2$: measured $1.31/0.175/0.069/0.0295/0.010$ at $b=2/4/8/16/32$, total advantage over $K=o(n^2)$ adaptive queries $o(1)$), but the union over $K$ adaptive queries assumes an additivity the adaptive tree can violate, and BGLWWZ (arXiv:2403.20283, Lemma 1.1, $\mathrm{MIC}\le 2ksn$) is gestured at, not instantiated (no fixed stream order, no UDISJ-to-needle lift). The two published frameworks that would close it (Simchowitz-El Alaoui-Recht, STOC 2018, arXiv:1804.01221; Kacham-Woodruff, NeurIPS 2023, arXiv:2311.17281) prove the orthogonalize-WLOG + truncated-likelihood per-round data-processing iteration for LINEAR matrix-vector measurements only (the repo's family (a), where the adaptive extension is already a theorem via turnstile sketches + BGLWWZ multi-pass space division), so neither black-boxes the non-linear sub-block case. The residual is one precisely-scoped non-linear per-round info lemma.

PROVES-TOO-MUCH PASSES (the collapse uses gaplessness essentially). The spectrum DETECTS a constant relative gap (top singular-value shift $\Theta(d)$ GAPPED vs $O(1)$ GAPLESS, ratio $2212/8376/19259$ at $d=64/128/192$, growing with $d$, $>100\times$), so a legitimate gap-exploiting spectral detector survives in the Valiant/light-bulb regime; the collapse is blind ONLY at gap $1$. Quantitative corroboration that one global spectral read is information-poor about a single planted cell: operator-norm estimation in turnstile streaming needs $\Omega(n^2/\alpha^4)$ dimension, Schatten-$p$ ($p>2$) needs $\Omega(n^{2-4/p})$ (Li-Nguyen-Woodruff, SIAM J. Comput. 2019, arXiv:1609.05885). HONESTY FLAG: the sufficient-statistic collapse is NOT a universal law; in quantum single-copy tomography there exist families where adaptive selection beats every non-adaptive design exponentially, so the collapse holds precisely when the statistic is query-independent (full-block) and can fail when the adaptive choice enriches it (sub-block), which is exactly why the residual is open.

NET. Finding 30's "extended with strong simulation support" upgrades to "full-block adaptive non-linear blindness is a THEOREM (Cover-Thomas data-processing on the fixed moment/spectral sufficient statistic), and the sub-block non-linear case is a single NAMED OPEN LEMMA (port the Simchowitz / Kacham-Woodruff orthogonalize+truncated-likelihood template to non-linear readouts, or instantiate BGLWWZ MIC with a UDISJ-to-needle lift)". The bulk model is now walled on every deterministic axis except this one lemma. Source: [`circuit_complexity/e_fused_max_mm_endgame.py`](circuit_complexity/e_fused_max_mm_endgame.py) (exit 0, self-check OK, smoke 5/5; Thrust B S1 full-block theorem, S2 adaptive transcript, S3 named sub-block lemma, PTM control) and subsection 4f of [`2050_tc0_hinge_grounded.md`](../docs/03_research/2050_tc0_hinge_grounded.md). No speedup claimed; $\mathsf{NEXP}\not\subseteq$ poly-size THR-of-THR remains open as of June 2026.

### 32. The co-nondeterministic frontier (finding 30) is PINNED-BLOCKED with the block CORRECTLY re-attributed: the obstruction is a triple-lock (UPIT/NSETH, algebrization, prAM-circularity), NOT the Set-Disjointness SDPT, and the CRT-correlation crack DISSOLVES because Chen's NEXP-direction reduction is single-instance. Extends finding 30.

Finding 30 named the residual frontier as derandomizing the $\Theta(\sqrt n\log n)$ Merlin-Arthur batch-OV/DISJ certificate (Williams, CCC 2016, arXiv:1601.04743; Rubinstein, STOC 2018, arXiv:1803.00904) into a pure co-nondeterministic (deterministic-verifier) certificate, so it lands inside Chen's deterministic-OR-co-nd hypothesis (arXiv:1805.10698, Remarks 2.7/4.2) and fires the NEXP-not-poly-THR-of-THR connection. This pass attacked the two flagged angles (the CRT crack and the SDPT) from first principles and corrected the attribution.

THE BLOCK IS A TRIPLE-LOCK, NOT THE SDPT. Arthur's randomness in the MA certificate is a SINGLE uniform random low-degree univariate evaluation point: Merlin sends the coefficients of $Q(x)$ of degree $\le dK$, Arthur checks $Q(r)=R(r)$ at one random $r$, soundness is Schwartz-Zippel (a cheating $Q\ne R$ caught except w.p. $\le dK/q^\ell$; Williams Thm 3.1). The earlier attack attributed the block to re-incurring the Strong Direct Product Theorem for Set-Disjointness (Klauck, STOC 2010, arXiv:0908.2940) at certificate size $\Theta(n^2)$; this is a MISAPPLICATION. The SDPT requires $k$ INDEPENDENT instances and lives on the SETH conditional-lower-bound side; Chen's NEXP-direction reduction is SINGLE-instance (Lemma 4.3 maps one THR-of-MAJ circuit to one Weighted-Max-IP instance over the two $n/2$-halves), so there is no n-fold independent-DISJ batch for the SDPT to bound. The correct obstruction is a triple-lock, all three verified: (a) UPIT/NSETH inside the protocol: naive derandomization (simulating all $O^*(2^{n/2})$ coins) recovers the full $O^*(2^n)$ nondeterministic algorithm, the bottleneck is univariate polynomial identity testing ($\tilde O(n)$ randomized, $\tilde O(n^2)$ deterministic), and Williams Cor 3.1 shows a sub-$n^2$ NONDETERMINISTIC UPIT already yields $\mathsf{E}^{\mathsf{NP}}$ lower bounds, so the co-nd derandomization IS the wanted breakthrough, not a free lemma; (b) algebrization on the engine: the Reed-Muller arithmetization + sum-check is THE canonical algebrizing technique (Aaronson-Wigderson 2008; repo probe classifies ALGEBRIZES), the NEXP-not-poly-THR-of-THR target is non-algebrizing (Williams spine), so an arithmetization-internal derandomization conflicts on the algebrization axis; (c) circularity of generic derandomization: $\mathrm{prAM}\subseteq\mathsf{NP}$ implies $\mathsf{E}^{\mathsf{NP}}$ requires $2^{\Omega(n)}$-size circuits (Miltersen-Vinodchandran, CCC 1999 / Comput. Complexity 2005; Impagliazzo-Kabanets-Wigderson 2002), the very lower bound sought.

THE CRT CRACK DISSOLVES. The proposed opening (Chen's instances are CRT-correlated, so the SDPT might not apply and the batch might compress below $N\cdot n$) targets a non-existent object. Chen's NEXP-direction reduction is single-instance, and its only randomness is a single random prime in Structure Lemma II (Lemma 3.2), ALREADY derandomized nondeterministically by guess-and-verify with one-sided error (Remark 3.3, $D(x)=1$ whenever $C(x)=1$). There is no independent-DISJ communication batch in that direction for correlation to evade; verified by reducing the model to a single instance (batch instances $=1$). The DISJ SDPT and the MA batch object both live on the SEPARATE SETH side. The crack is retired as a false lead.

THE CORRECTED NONNEG-RANK DERIVATION (a wrong-set fix that also corrects finding 30). The Yannakakis bound is $\mathrm{rank}_+(N)\ge$ the cover of $\mathrm{supp}(N)=\{M_{ij}\ne\tau\}$ (the COMPLEMENT of the tight set) by tight-free rectangles. Finding 30's `disj_cover_number` instead covered the TIGHT set (the diagonal of a permutation tight set) by $1\times1$ cells and reported $\Omega(m)$; this is the wrong set. An explicit tight-free rectangle cover of the off-diagonal $\mathrm{supp}(N)$ has size $2\lceil\log_2 m\rceil = O(\log m)$ (verified coverage and tight-freeness, $4/6/8/12/16/20$ at $m=4/8/16/64/256/1024$), so the nonneg-rank route gives only $\mathrm{rank}_+(N)\ge O(\log m)$, NOT $\Omega(m)$. The legitimate $\Omega(n)$ is the co-nondeterministic COMMUNICATION complexity of UDISJ on the SINGLE planted pair, bounding the certificate for ONE decision at $\Omega(n)$ bits; the jump to an $\Omega(n^2)$ certificate SIZE needs $n$ independent $\Omega(n)$ covers, which Chen's gap-1 family (ONE planted pair, not $n$) does not obviously supply, so the $n^2$ certificate size is now explicitly NAMED-AS-NOT-DERIVED.

THE SURVIVING NON-CIRCULAR OPENING. A barrier-clean win cannot come from arithmetization/AG-code fingerprinting (algebrizes) or a generic derandomization theorem (circular); it would need a problem-specific, non-algebrizing succinct co-nd certificate for the gap-1 statement. The one narrow, non-circular, possibly non-algebrizing micro-question that remains: does Chen's single random prime (Lemma 3.2) admit a DETERMINISTIC small-prime hitting set for the linear-form-nonzero event, computable in the target time, removing the only randomness in the NEXP-direction reduction without touching the SETH-side MA object (hitting-set size measured cheap, 33 primes for 32 bits). PROVES-TOO-MUCH PASSES (a constant gap shrinks the tight set, so a small certificate exists, Valiant-consistent). Three-barrier check on the routes: Route (i) deterministic hitting set HITS algebrization (DISQUALIFIED); Route (ii) Merlin-guessed points EVADES all three but is blocked by the triple-lock, not a barrier.

NET. The co-nd prong of finding 30 stays CLOSED, but the block is now correctly pinned: the obstruction is the triple-lock (UPIT/NSETH inside the protocol, algebrization on the engine, prAM-circularity of generic derandomization), the SDPT was misapplied to a non-existent batch, the CRT-correlation crack dissolves (single-instance reduction, already nondet-derandomized), and the prior nonneg-rank $\Omega(m)$ bound was a wrong-set error corrected to $O(\log m)$ with the $n^2$ certificate size named-as-not-derived. The sub-$n$ MA object remains randomized-verifier, outside Chen's hypothesis. Source: [`circuit_complexity/e_fused_max_mm_endgame.py`](circuit_complexity/e_fused_max_mm_endgame.py) (exit 0, self-check OK, smoke 5/5; Thrust A (i) MA sub-$n$, (ii) corrected nonneg-rank cover, (iii) CRT dissolves + small-prime hitting set, barrier logic) and subsection 4f of [`2050_tc0_hinge_grounded.md`](../docs/03_research/2050_tc0_hinge_grounded.md). No speedup claimed; $\mathsf{NEXP}\not\subseteq$ poly-size THR-of-THR remains open as of June 2026.

### 33. The sub-block non-linear per-round information lemma (finding 31) is OPEN, not partial: the marginal-info "telescope" rested on an inconsistent signal model, Route (a) is linear-only, and the named missing object is conditional-info uniformity under adaptive sub-block choice. Extends finding 31.

Finding 31 closed the FULL-block non-linear adaptive case as a theorem (Cover-Thomas sufficient-statistic collapse) and downgraded the SUB-block case to a single named open lemma. This pass ran both dossier routes with measured numbers and the verdict is OPEN, sharper than before but not closed; an earlier internal framing of "lemma-partial" is corrected here.

ROUTE (a) IS DEAD FOR SPECTRAL READS (measured). The Simchowitz-El Alaoui-Recht (STOC 2018, arXiv:1804.01221) / Kacham-Woodruff (NeurIPS 2023, arXiv:2311.17281) per-round data-processing chain rule rests on the orthogonalize-WLOG deflation (Simchowitz Obs 3.1 / Sec 3.4: past LINEAR responses $w_k=Mv_k$ determine $M$'s action on $\mathrm{span}$ of past queries) and on a Gaussian conditional-likelihood closure (Lemma 3.4), both linear-only. Measured cross-block deflation residual: LINEAR $\approx 10^{-15}$ (WLOG valid), non-additive SPECTRAL $\approx 0.997$ (no determination), so the chain rule does not type-check for spectral readouts. Honesty correction the adversary forced: degree-2 entry-symmetric MOMENTS tile EXACTLY (block moment $=$ sum of sub-quadrant moments, residual $0$), so a deflation DOES exist for the moment family; the no-port claim is sound ONLY for non-additive spectral reads.

ROUTE (b)'s TELESCOPE FAILS AS MEASURED (the load-bearing correction was an artifact). The would-be closing argument posited a per-round location law $I(\text{block moment};\mathbf{1}\{\text{spike in block}\}) \sim C\,b^2/n^2$ with $C\approx 4.5$, telescoped via the chain rule plus Fano to force $\sum_k b_k^2 \ge (2/C)\,n^2\log_2 n$. The $C\approx 4.5$ holds only under an INCONSISTENT signal model: the measurement injected a $\Theta(d^2)$ cell-upgrade, not the gap-1-faithful $+(2d-1)$ increment (a cell $d-1\to d$). Under the faithful increment the per-round info collapses to the binned-MI estimator NULL floor: I/f at $n=128,d=64$ is faithful $2.33/0.79/0.19/0.029/0.009$ vs null floor $1.77/0.50/0.089/0.026/0.007$ at $b=2,4,8,16,32$. So no $C\,b^2/n^2$ law survives and the telescope loses its premise. Two further adversary corrections: the test family was not gap-1 (a planted $d=64$ over a bulk maxing at $24$, a $4\times$ relative gap a single read detects), and detection $\neq$ localization (the task is a 1-bit decision $\max=d$ vs $\le d-1$; the Fano telescope lower-bounds the strictly harder localization, proving too little).

WHAT SURVIVES (evidence, not proof). The per-round SNR of a degree-2 sub-block membership test is $\Theta(1/(b\sqrt d))$ (measured $\mathrm{SNR}\cdot b\sqrt d \approx 15$-$16$ across $d\in\{16,64,256\}$, $b\in\{1,2,8\}$), so even a single cell is sub-SNR at gap 1 for $d\ge 5$ and no proper sub-block summary is a reliable bit. The cheapest adaptive tree (greedy quadrant descent, $O(\log n)$ reads) FAILS with success DECAYING as $n$ grows ($0.62/0.35/0.20/0.05$ at $n=64/128/256/512$). PROVES-TOO-MUCH (on a correctly-gapped family) passes: a spectral read DETECTS a constant relative gap (ratio $>100\times$, growing with $d$), blind only at gap 1.

NET. The lemma is OPEN. The named missing object is the per-round CONDITIONAL location-information uniformity $I(\text{answer}_k; L \mid \text{answer}_{<k}) = O(b_k^2/n^2)$ under adaptive sub-block choice; even the MARGINAL version is unestablished (the prong's measurement was artifactual). This is exactly the adaptive low-degree/spectral query lower bound the literature flags as open (Mardia-Verchand-Wein, arXiv:2402.05451, prove the non-linear low-degree phase transition for NON-ADAPTIVE queries only; Racz-Schiffer, ALEA 2020, arXiv:1903.12050, handle full adaptivity but only for single-entry boolean queries with no non-linear-aggregate analog). The more promising route is the BGLWWZ MIC measure (arXiv:2403.20283, Lemma 1.1, $\mathrm{MIC}\le 2ksn$, a SPACE bound agnostic to query linearity), with two unbridged steps: a streaming-simulation lemma and a gap-1-to-needle/MostlyEq reduction (BGLWWZ does NOT route through UDISJ, correcting the dossier's "gap-1 $=$ UDISJ to MIC needle" phrasing). Source: [`circuit_complexity/e_j1_subblock_j3_locality.py`](circuit_complexity/e_j1_subblock_j3_locality.py) (exit 0, smoke 5/5; the inconsistent-signal artifact is reproduced side-by-side as the central finding). Honesty caveat preserved: even if closed this is an IN-MODEL bound, not an unconditional algorithm lower bound. $\mathsf{NEXP}\not\subseteq$ poly-size THR-of-THR remains open as of June 2026.

### 34. J3 (the binding joint) ATTACKED and mapped: the locality barrier is an OPEN NO-GO with a precise evasion criterion; meta-complexity is disqualified as the non-local ingredient (S2E relativizes), the Williams spine is the only plausible source (a direction not a technique), and the single most-attackable sub-question is whether the AC0[p] localization collapse extends to threshold oracle gates. Extends finding 26.

Finding 26 named J3 (a proved high-Kt / MCSP-against-$\mathsf{TC}^0$ lower bound, blocked by the locality barrier) as the BINDING joint of the descent to NP. This pass maps it exactly. No progress on the prize; a sharp map and a precise OPEN verdict.

THE BARRIER, STATED EXACTLY. A lower-bound proof is LOCAL when it extends to the oracle-circuit model $[q,l,a]$-$\mathcal{C}$ (Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam, "Beyond Natural Proofs: Hardness Magnification and Locality", JACM 69(4) art 25, 2022, arXiv:1911.08297, Def 11): $q$ oracle gates of fan-in $\le l$, every input-output path meeting $\le a$ of them, for SOME oracle $O$. The barrier (Thm 2) couples an UNCONDITIONAL oracle-circuit upper bound on the magnified circuit (B1$^O$: $\mathrm{MCSP}[2^{n^{1/3}},2^{n^{2/3}}]\in$ Formula-$O$-XOR$[N^{1.01}]$ with oracle fan-in $\le N^\varepsilon$) with the fact that the known technique EXTENDS to those same oracle circuits (B3$^O$: InnerProduct cannot be computed by $N^{2-3\delta}$-size Formula-$O$-XOR for ANY oracle $O$). Technique and target provably meet inside one class, so the technique cannot separate. The weak target HM needs is slightly superlinear, $N^{1+\varepsilon}$ (e.g. $N^{1.01}$), and local techniques provably cannot reach even that against the magnifying model.

COVERAGE (broad). The polynomial method (CHOPRS Lemma 41: an oracle gate of fan-in $O_i$ becomes its multilinear extension, degree $\le O_i$, collapsing $\mathsf{AC}^0[+]^O$ to a low-degree probabilistic polynomial), approximate degree, random restrictions, and (definitively) reduction-based bounds are all proved LOCAL; this pass adds Razborov's APPROXIMATION METHOD (Pich, "Localizability of the approximation method", Computational Complexity 2024, arXiv:2212.09285). Natural proofs are a SEPARATE, already-cleared wall: HM refutes natural proofs (CHOPRS Thm 1 (a)$\iff$(d)), so locality is the second wall, matching the dossier's claim that the escape flips from non-largeness to non-constructivity and THAT is what locality blocks.

WHY MCSP IS LOW-LOCALITY (the cap, corrected). Golovnev-Ilango-Impagliazzo-Kabanets-Kolokolova-Tal (ICALP 2019, ECCC TR19-018): MCSP needs depth-$d$ $\mathsf{AC}^0[p]$ of size $\exp(\Omega(N^{0.49/d}))$ (corrected exponent $0.49/d$, NOT $0.49/(d-1)$: $0.245/0.1633/0.1225/0.0817$ at $d=2/3/4/6$, matching the repo's `e_leading_path_descent.py`). $\mathrm{MAJ}\in(\mathsf{AC}^0)^{\mathrm{MCSP}}$, $\mathsf{NC}^1\subseteq(\mathsf{AC}^0)^{\mathrm{MCSP}}$, so an $\mathsf{AC}^0$-with-MCSP-oracle device already computes $\mathrm{MAJORITY}/\mathsf{NC}^1$ and any $\mathsf{AC}^0[p]$/polynomial-method technique on MCSP-oracle circuits computes $\ge\mathrm{MAJORITY}$, capping the reach at $\mathsf{AC}^0[p]$.

THE PRECISE EVASION CRITERION (non-local HM characterized). A technique evades iff its argument FAILS under $o(N)$ arbitrary fan-in-$N^\varepsilon$ oracle gates, i.e. is NON-LOCALIZABLE and reaches $N^{1+\varepsilon}$ for an HM-frontier problem. CHOPRS exhibit exactly one proved non-localizable above-threshold bound (Thm 49, Frontier D, pseudorandom restrictions) but it does not match a magnification threshold for the right problem.

THE TWO NON-LOCAL INGREDIENTS, ASSESSED. Meta-complexity proved non-constructivity is DISQUALIFIED: the strongest engine, S2E near-maximum (Chen-Hirahara-Ren, "Symmetric Exponential Time Requires Near-Maximum Circuit Size", STOC 2024, arXiv:2309.12912), RELATIVIZES (verbatim) and avoids HM (it uses Korten range-avoidance plus the CLORS win-win), and a relativizing engine localizes trivially. The W2A core also relativizes (Hirahara 2018, ECCC TR18-138). So the Williams spine (non-relativizing, the SAT-algorithm-to-lower-bound link) is the ONLY plausible non-local source, a DIRECTION not a technique (Oliveira 2019 indirect diagonalization is suggestive but not at an HM threshold).

THE SINGLE MOST-ATTACKABLE SUB-QUESTION (demoted from a win-win to a genuine coordinate). The localization collapse is PROVED at $\mathsf{AC}^0[p]$ via Lemma 41's multilinear extension (degree $\le$ fan-in, a polynomial-method fact); a THRESHOLD oracle gate has high-degree multilinear extension (MAJORITY full degree $\Theta(N)$), so it does not obviously port to $\mathsf{TC}^0$-oracle circuits. PROBE: try to extend Lemma 41 to threshold oracle gates; success $\Rightarrow$ the no-go extends to $\mathsf{TC}^0$, failure $\Rightarrow$ a named gap where a non-local $\mathsf{TC}^0$ technique could live. HONEST DEMOTION (adversary-forced): the GIIKKT computational cap ($\mathrm{MAJ}, \mathsf{NC}^1\in(\mathsf{AC}^0)^{\mathrm{MCSP}}$) is gate-type-AGNOSTIC and already places MCSP-oracle devices above $\mathsf{AC}^0[p]$ WITHOUT the degree argument, so "cap at $\mathsf{AC}^0[p]$ but not $\mathsf{TC}^0$" is a mis-location; the seam is essentially the open $\mathsf{TC}^0$ lower-bound problem relabeled.

NET. J3 is an OPEN NO-GO with no completed candidate technique. The barrier is precise, broadly covering, and downstream of natural proofs; the evasion criterion is named (non-localizable, $N^{1+\varepsilon}$, HM-frontier); meta-complexity is disqualified; the spine carries the entire non-relativizing burden; J4 (no combining theorem) remains the composition obstacle. 2025 magnification work (Atserias-Muller, arXiv:2503.24061) stays within the paradigm with no locality-evasion claimed. Source: [`circuit_complexity/e_j1_subblock_j3_locality.py`](circuit_complexity/e_j1_subblock_j3_locality.py) (exit 0, smoke 5/5; corrected GIIKKT exponent, demoted seam, technique/locality table with zero non-local-at-HM-threshold). $\mathsf{NEXP}\not\subseteq$ poly-size $\mathsf{TC}^0$ remains open as of June 2026.
