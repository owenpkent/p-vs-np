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
