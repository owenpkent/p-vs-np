# Backward induction from 2050: if P vs NP is solved, what is the proof?

> A speculative strategy document produced by reasoning backward from a solved
> future. Nine independent "2050 historians" each reconstructed a different
> resolution path; an adversary stress-tested each against the three barriers
> and for circularity; a synthesizer ranked what survived. Companion to the
> [research atlas](../research_atlas/README.md) and the
> [researcher mindset](../researcher_mindset.md). This is a compass-calibration
> exercise, not a claim. Read it for where the surviving signal points.

## What this is, and what it is not

This document imagines it is 2050 and P vs NP has been resolved, then pushes
backward to ask what the proof would have to be. The method was deliberate:
build many futures, let an adversary kill the weak ones, and read the structure
of the wreckage. Honesty is the load-bearing part. Every path here is either
wounded or dead when modeled mechanically against the 1994-and-2008-era
barriers, which is exactly the project's prior. The value is not any single
story. It is the **convergence**: when you force nine different futures to
defend themselves, they point back at the same skeleton.

Caveat to carry: these are constructed narratives, stress-tested at the level of
argument, not Lean-verified. None has a formal proof. Treat the probabilities as
calibration, not measurement.

## 1. The verdict spread

Sorted by adversary survival, not by the builders' self-assigned plausibility.
The canonical narrative tracks what survives scrutiny.

| Path | Resolution | Builder plausibility | Adversary verdict | Fatal / primary barrier |
|---|---|---|---|---|
| Williams scaled to P/poly | $\mathsf{P} \neq \mathsf{NP}$ | 0.07 | dead | natural proofs (largeness creep) + circular easy-witness lemma |
| Meta-complexity (MCSP/Kt fixed point) | $\mathsf{P} \neq \mathsf{NP}$ | 0.12 | **wounded** | algebrization (the W2A core arithmetizes); RR a close second |
| Fourth barrier + self-referential lifting | $\mathsf{P} \neq \mathsf{NP}$ | 0.04 | **wounded** | BPR / feasible interpolation; XOR toy refuted by parity in $\mathsf{ACC}^0$ |
| Independence from a strong arithmetic | independent | 0.04 | **wounded** | RR by self-reference; crypto hypothesis stronger than the conclusion |
| GCT multiplicity obstructions | $\mathsf{P} \neq \mathsf{NP}$ | 0.04 | dead | BIP 2016 domination has the wrong sign; the PIT bridge algebrizes |
| New proof-complexity engine (eFrege) | $\mathsf{NP} \neq \mathsf{coNP}$ | 0.06 | dead | BPR; protocol-to-circuit duality rebuilds the forbidden interpolant |
| Physics-native (spin-glass OGP) | $\mathsf{P} \neq \mathsf{NP}$ | 0.05 | dead | RR (the overlap-gap statistic is large + constructive); k-XOR counterexample |
| Machine-found topological invariant | $\mathsf{P} \neq \mathsf{NP}$ | 0.04 | dead | algebrization (Lefschetz/Betti are characteristic-0 trace functionals) |
| The upset: $\mathsf{P} = \mathsf{NP}$, galactic | $\mathsf{P} = \mathsf{NP}$ | 0.02 | dead | algebrization (the relaxation is low-degree); SoS lower bounds |

No path survived clean. Three are wounded (a repair exists that keeps a scoped
result alive). Six are dead (a known barrier or a concrete counterexample fires
before the speculative machinery engages). The honest read: the field's
strongest 2050 stories are still defeated by the published barriers when modeled
mechanically. The single robust finding across all nine is that the
algorithm-to-lower-bound spine (Williams 2011) is the only component no
adversary could disqualify, and **every wounded verdict reduces to the same
repair: graft the speculative idea onto that spine instead of replacing it.**

## 2. The leading path

The leading path is **meta-complexity riding the Williams spine**. It is the
only path the adversary did not kill on a structural counterexample, and four
independent kills (Williams-scaled, physics-native, the upset, and meta-
complexity itself) all carry the same repair instruction: fuse with the Williams
algorithm-to-lower-bound connection. That convergence, not any single builder's
optimism, is why this is the lead.

Stated cleanly: the winning 2050 theorem is most likely
$\mathsf{NP} \not\subseteq \mathsf{P/poly}$, proved by feeding a non-trivial
circuit-SAT (or #SAT) algorithm for a meta-problem's circuit class through the
Williams connection, where meta-complexity supplies the **non-natural device**
(proved, not assumed, non-constructivity of "this truth table has high $Kt$")
and the algorithmic method supplies the **non-relativizing, non-algebrizing
diagonalization spine**. The arithmetizing worst-case-to-average-case (W2A)
local-list-decoding core, which is what the adversary disqualified at
algebrization, is dropped as a load-bearing step.

Critical path, 2050 down to 2026 (the repaired version, not the builder's
original W2A-closure version):

- **2048-2050.** $\mathsf{NP} \not\subseteq \mathsf{P/poly}$ announced. A
  non-trivial SAT algorithm for the meta-problem's circuit class, fed through the
  Williams template, yields an unconditional lower bound that descends to
  $\mathsf{NP}$ via a proved (not assumed) non-constructivity of the $Kt$ / MCSP
  hardness property.
- **2046-2049.** Unconditional weak MCSP / $rKt$ lower bound, size
  $2^{\Omega(n/\log n)}$, established by a route that does NOT define its
  certifying gadget in terms of $Kt$ (avoiding the self-reference circularity).
  This is the non-natural device turned into a theorem.
- **2044-2047.** The non-local hardness-magnification gadget that defeats the
  Chen-Hirahara-Oliveira-Ren locality barrier, built without the self-referential
  reflective definition the adversary flagged as circular.
- **early 2040s.** The meta-complexity zoo ($Kt$, $Kpoly$, $rKt$, $pKt$, MCSP,
  MKtP) collapses to one master measure with a clean amplification calculus. A
  sister achievement, not a P vs NP result.
- **late 2030s.** MCSP proved NP-hard under deterministic poly-time reductions
  (de-randomizing and de-partializing Ilango-Loff-Oliveira and Hirahara's
  randomized-reduction results).
- **2030s.** The Williams program climbs from $\mathsf{ACC}^0$ to
  $\mathsf{TC}^0$. **This is the hinge.**
- **2026.** Hirahara W2A (conditional), Liu-Pass (OWF iff $Kt$ mildly avg-hard),
  MCSP NP-hard for partial functions, Williams $\mathsf{NEXP} \not\subseteq
  \mathsf{ACC}^0$.

The one milestone everything hinges on, the "if this falls, the dominoes start"
step, is the late-2030s **$\mathsf{TC}^0$ step of the Williams program**: a
non-trivial circuit-satisfiability algorithm for threshold circuits yielding
$\mathsf{NEXP} \not\subseteq \mathsf{TC}^0$. Every $\mathsf{P} \neq \mathsf{NP}$
path the adversary did not immediately kill routes through the Williams
connection, and that connection is stuck in 2026 at exactly one wall: the
polynomial method that powered $\mathsf{ACC}^0$ provably stops working at
threshold gates (MAJORITY has no low-degree polynomial representation). The
atlas already names this as the open frontier. $\mathsf{TC}^0$ is the first rung
past $\mathsf{ACC}^0$; if it falls, the climb to $\mathsf{NC}^1$ and
$\mathsf{P/poly}$ becomes a quantitative grind rather than a barrier. It is
compute-light and theory-bound, which means it is attackable now.

## 3. The braided path

The single-architecture framing understates the structure. No surviving path is
monolithic. Every wounded verdict, and several dead ones, has a repair that
imports a component from a different scenario. The real 2050 proof most likely
braids three strands, each supplying exactly the barrier evasion the other two
lack:

1. **Algorithmic method (Williams), the spine.** Supplies non-relativization
   (the SAT algorithm opens the circuit's gate structure rather than querying a
   black box) and non-algebrization (the speedup is combinatorial, not a
   low-degree polynomial functional). The only strand no adversary disqualified.

2. **Meta-complexity, the non-natural device.** Supplies the escape from
   Razborov-Rudich via PROVED non-constructivity: the certifying property is
   "this truth table has high $Kt$," whose decidability is itself the meta-problem
   shown not to be in $\mathsf{P/poly}$. The property is large (most functions are
   incompressible, by Shannon counting) yet provably non-constructive, so it
   cannot be $\mathrm{poly}(2^n)$-tested without contradicting the theorem.

3. **A new invariant, the contradiction engine,** computed cheaply by the SAT
   algorithm yet provably not recoverable from a low-degree oracle extension.
   This is the missing object. Every scenario that proposed one (persistent
   homotopy, free-energy width, a fixpoint-index, Schur multiplicity, semialgebraic
   degree) had its invariant killed for the SAME reason: the invariant was
   secretly a characteristic-0, low-degree, trace/rank/volume functional and
   therefore algebrized.

**The concrete cross-architecture bridge.** The braid is held together by a
single demand the dataset states three different ways and never satisfies: one
quantity $Q(C, \text{instance})$ that is (a) nonzero and cheaply certifiable by a
faster-than-brute-force #SAT-style algorithm on the candidate circuit's gate
structure, and (b) provably not reconstructible from any low-degree polynomial
extension of the oracle. Strand 1 needs $Q$ to be algorithm-computable (which
pushes toward a rational, trace-computable, hence algebrizing functional). Strand
3 needs $Q$ to be non-algebrizing (which pushes toward torsion, a non-abelian
fundamental-group class, or a mod-2 Steenrod / Bockstein obstruction that the
rational machinery is blind to). The only known reconciliation in the whole
dataset is a **Bockstein-type bridge**: a universal-coefficients or Bockstein
exact sequence forces a characteristic-2 non-algebrizing torsion class to be
non-vanishing precisely BECAUSE a characteristic-0 algorithmic count (an Euler
characteristic / Lefschetz number) takes a specific value. The rational count is
the cheap feasibility gate (strand 1); the torsion class is the lower-bound
obstruction (strand 3); meta-complexity certifies that testing the class is
itself hard (strand 2). That object does not exist in 2026 and no scenario
contained it. It is the precise specification of the missing tool, written as a
wiring diagram across three architectures.

## 4. The fourth barrier

Collectively the scenarios point at one structural feature of SAT that a winning
proof must finally exploit, and at one not-yet-formalized meta-barrier that
explains why no current technique exploits it.

**The structural feature: self-reference / non-localizable global coupling tied
to a function-specific (non-large) certificate.** SAT can encode its own
refutation search (a Kleene-recursion construction), and meta-complexity can
encode the hardness of computing hardness. No generic Boolean function has this
reflexive structure, which is exactly why it is anti-natural: a property that
holds for one self-referential family and a vanishing fraction of all functions
dodges the largeness clause by construction. Three independent scenarios (meta-
complexity, self-referential lifting, the homotopy bridge) converged on
reflexivity as the anti-natural feature without coordinating. That is the
strongest positive signal in the dataset.

**The implied meta-barrier.** Read against itself, the dataset suggests a fourth
barrier that the three published ones are special cases of: *a proof technique
fails if its hardness certificate can be reconstructed across a bounded,
low-interaction interface to the problem.* Relativization is the case where the
interface is a black-box oracle query (bit access). Algebrization is the case
where the interface is a low-degree polynomial extension (field-point access,
strictly more). Natural proofs is the case where the certificate is a
$\mathrm{poly}(2^n)$-time-testable property (a bounded-cost decision interface to
the truth table). Every attempt in the dataset to USE this fourth barrier as a
positive tool collapsed back into one of the three known ones (the
self-referential XOR-aggregate is degree-1 and algebrizes; the bounded-arithmetic
engine is RR inverted). That collapse is itself the evidence: the fourth barrier
is real but not yet correctly axiomatized. We can see its shadow in the
graveyard (every soft technique fails the same way) but no scenario stated it
sharply enough to evade it constructively.

**Flag for the program.** The repo's barrier checker models exactly three
barriers via four boolean fields, and it cannot audit a "non-constructivity is
PROVED not assumed" claim. Several dead/wounded scenarios passed the mechanical
checker only because a single hand-set `natural_largeness=False` or
`algebrizes=False` flag hid the collision. The checker is a discipline for honest
inputs, not a prover, and the fourth-barrier scenarios are precisely the ones
that game it. This is a known limitation to carry forward, not a defect to
integrate as a result.

## 5. Instructive mistakes (coordinates, not failures)

Each killed idea removes a region of technique-space. Honest accounting: every
entry is a dead branch that sharpens where the real proof lives.

- **W2A local list-decoding as the descent engine** (meta-complexity,
  physics-native). Killed at algebrization: Reed-Muller / low-degree encoding of
  the universal distribution arithmetizes, exactly like $\mathsf{IP} =
  \mathsf{PSPACE}$. Coordinate: the worst-case-to-average-case bridge CANNOT be
  the non-algebrizing component. Any meta-complexity path must get its
  non-algebrization from elsewhere (the Williams spine), and use W2A only where
  its arithmetization is harmless.

- **NP-scale easy-witness lemma** (Williams-scaled). Killed by circularity: a
  $\mathrm{poly}(n)$-time verifier certifying "no size-$n^c$ circuit decides $L$"
  from a poly-length string is an MCSP-style collapse as strong as the
  conclusion. Coordinate: the $\mathsf{NEXP}$-to-$\mathsf{NP}$ descent is not a
  quantitative strengthening of IKW 2002; the exponential-to-polynomial witness
  gap IS the problem. The hard function legitimately stays in $\mathsf{NEXP}$
  until a genuinely new descent theorem exists.

- **The $\varepsilon = 0.001$ superpolynomial savings** (Williams-scaled). Killed
  numerically: $2^{m^{0.001}}$ does not beat $m^3$ below astronomically large
  $m$. Coordinate: "superpolynomial in $m$" is not enough; the savings must
  dominate the $2^n$ truth-table verification at feasible scale. Drop
  sub-polynomial-in-exponent savings claims. (Pinned in code:
  [`experiments/circuit_complexity/e_tc0_sat_savings.py`](../../experiments/circuit_complexity/e_tc0_sat_savings.py).)

- **Multiplicity obstruction with $\mathrm{mult}_{\text{perm}} >
  \mathrm{mult}_{\text{det}}$** (GCT). Killed by sign: BIP 2016/2019 give
  multiplicity DOMINATION in the padded regime ($\mathrm{mult}_{\text{perm}} \le
  \mathrm{mult}_{\text{det}}$), the opposite of what the path needs, compounded by
  the non-normality of the determinant orbit closure. Coordinate: the GCT gap, if
  it exists, is not in the padded perm-vs-det multiplicity comparison; padding is
  exactly what BIP weaponized. A live GCT route must avoid padding (iterated
  matrix multiplication, trace-power families) or use a containment-monotone
  quantity (dimension/codimension), not raw Schur multiplicities. And no GCT
  separation yields $\mathsf{P} \neq \mathsf{NP}$ without a non-PIT Boolean bridge.

- **Witnessing-extracted monotone real protocol for eF** (proof complexity).
  Killed by BPR via protocol-to-circuit duality: a low-cost monotone real protocol
  IS a feasible monotone interpolant, the exact object BPR proves cannot exist for
  eF under crypto. Coordinate: relabeling "interpolant" as "protocol" does not
  evade BPR; the duality is forced. The only honest eF target is an intermediate
  system where the duality is genuinely broken ($\mathsf{AC}^0$-Frege + mod
  gates), or an explicitly conditional separation on Krajicek's NW-generator
  conjecture.

- **XOR-aggregate as global-coupling hardness** (fourth-barrier). Killed by
  parity: the XOR-aggregate has maximal global coupling (average sensitivity $n$,
  every coordinate pivotal) yet is computed by $n-1$ gates and lives in
  $\mathsf{ACC}^0$. Coordinate: non-localizable global coupling does NOT imply
  circuit-size hardness. Any "interaction forces size" lift must be tested against
  parity first; the load-bearing aggregate must be provably not in
  $\mathsf{ACC}^0$.

- **Free-energy width / OGP statistic as a worst-case lower bound**
  (physics-native). Killed by RR and by k-XOR: the OGP statistic is large (holds
  for a constant fraction of the planted ensemble) and constructive
  ($\mathrm{poly}(2^n)$-estimable), the definition of natural; and random k-XOR
  has a textbook overlap gap and exponential configurational entropy yet is in
  $\mathsf{P}$ via Gaussian elimination, so width $\ge$ cluster-diameter is false.
  Coordinate: solution-space clustering geometry is a natural property measured
  against the wrong distribution, and clustering is not sufficient for hardness. A
  geometric route must encode why Gaussian elimination is forbidden for the target
  class.

- **Lefschetz / Betti / persistent-homology invariant** (homotopy bridge). Killed
  by algebrization: the Lefschetz number is $\sum_i (-1)^i \mathrm{tr}(f_* \mid
  H_i; \mathbb{Q})$, a characteristic-0 trace functional that a low-degree oracle
  extension reconstructs. Coordinate: any algorithm-computable rational topological
  invariant algebrizes. The anti-algebrization content must be torsion /
  non-abelian / mod-2 (Steenrod, Bockstein). This is the cleanest statement of the
  strand-1-vs-strand-3 tension in Section 3. (Operationalized in code:
  [`experiments/_shared/algebrization_probe.py`](../../experiments/_shared/algebrization_probe.py).)

- **Bounded-degree semialgebraic relaxation after a GL change of coordinates**
  (the upset, $\mathsf{P} = \mathsf{NP}$). Killed by SoS lower bounds and
  algebrization: a linear (GL) reparameterization is a unit-degree automorphism of
  the polynomial ideal, so it cannot lower the $\Omega(n)$ SoS degree of random
  3-XOR (Grigoriev, Schoenebeck); and the whole decision procedure is built from
  low-degree primitives, so it algebrizes. Coordinate: no low-degree
  (semialgebraic, SoS, CAD) relaxation can collapse SAT, and GL coordinate changes
  do not help. A $\mathsf{P} = \mathsf{NP}$ collapse, if it exists, must be
  genuinely non-low-degree and non-relativizing, for which the dataset gives no
  candidate.

- **The "absoluteness rules out independence" claim** (independence). Killed by a
  logic error: Shoenfield absoluteness says forcing cannot CHANGE the truth value
  of a $\Pi^0_2$ statement; it does not say the statement is not independent (a
  fixed-truth-value sentence can still be unprovable). Coordinate:
  forcing-invariance and provability are different axes. Independence of P vs NP
  from ZFC is not ruled out by absoluteness; it is only made forcing-inaccessible.
  Also: a subexponentially-secure one-way function already implies $\mathsf{P} \neq
  \mathsf{NP}$, so the independence hypothesis was stronger than the conclusion.

## 6. What to actually do in 2026

These moves are on the critical path of the leading path (Section 2) and the
braid (Section 3), and they are runnable in this repo with the existing
barrier-checker substrate.

1. **Build the $\mathsf{TC}^0$-SAT savings model and pin it as the hinge.** The
   single most load-bearing milestone is the late-2030s $\mathsf{TC}^0$ step.
   [`experiments/circuit_complexity/e_tc0_sat_savings.py`](../../experiments/circuit_complexity/e_tc0_sat_savings.py)
   models threshold-circuit satisfiability, encodes a candidate
   "Boolean-rank-collapse" speedup as a `ProofTechnique`, runs it through the
   barrier checker, and pins the fact that the Razborov-Smolensky polynomial method
   fails at threshold gates (so a real escape needs `algebrizes=False`). It also
   reproduces the savings-mirage coordinate numerically.

2. **Make the meta-complexity non-natural device a checkable object.** Extend
   [`experiments/circuit_complexity/e_2050_synthesis_barrier_check.py`](../../experiments/circuit_complexity/e_2050_synthesis_barrier_check.py)
   to encode the "high $Kt$" property with `natural_largeness=True,
   natural_constructivity=False`, and add an explicit audit note that the
   non-constructivity is the meta-problem (MCSP not in $\mathsf{P/poly}$) and
   therefore must be PROVED, not asserted. The checker cannot itself verify this,
   so the flag is a claim to be discharged by a Lean lemma, not a result.

3. **Build the algebrization stress-test as a first-class experiment.** The
   braid's missing object (Section 3) is defined by a single test: does the
   candidate invariant survive a low-degree oracle extension?
   [`experiments/_shared/algebrization_probe.py`](../../experiments/_shared/algebrization_probe.py)
   classifies a proposed hardness invariant as a characteristic-0
   trace/rank/volume functional (which algebrizes) versus a torsion / mod-2 /
   non-abelian quantity (which may not), with the Lefschetz-number and
   semialgebraic-degree invariants as failing fixtures and a Steenrod / Bockstein
   placeholder as the open candidate.

4. **Falsify the global-coupling lift in code, cementing the parity coordinate.**
   The fourth-barrier and physics-native kills both reduce to: global coupling does
   not imply circuit size, and clustering does not imply hardness. Add explicit
   counterexample assertions: parity (average sensitivity $n$, in $\mathsf{ACC}^0$)
   refutes coupling-implies-size, and random 3-XOR (strong overlap gap, in
   $\mathsf{P}$ via Gaussian elimination) refutes clustering-implies-hardness.

5. **Scope the proof-complexity thread to where BPR does not bite.** Following the
   plan's existing next step (a resolution-width lower bound for the pigeonhole
   principle), extend
   [`experiments/proof_complexity/e_efrege_lifting_barrier_check.py`](../../experiments/proof_complexity/e_efrege_lifting_barrier_check.py)
   to model the intermediate-system target ($\mathsf{AC}^0$-Frege + mod gates)
   where feasible interpolation is not provably blocked, and mark eF itself as
   BPR-blocked.

## Appendix: the nine scenarios in brief

Each entry: the 2050 theorem, the single hardest leap, the verdict, and the
earliest place it breaks.

**A1. Meta-complexity closes the loop (wounded, 0.12).** Theorem: MCSP not in
$\mathsf{P/poly}$, lifted by a W2A bridge to $\mathsf{NP} \not\subseteq
\mathsf{P/poly}$, closed into a fixed point. Leap: turning the reflexive
obstruction into an unconditional contradiction (making "MCSP is hard" a lemma,
not a hypothesis). Breaks at: the W2A core is local list-decoding of low-degree
encodings, which algebrizes; specializing to an algebraic-oracle world defeats
the self-referential closure before the chain reaches $\mathsf{NP}$. Repair: keep
meta-complexity only for its non-relativizing self-reference, pair with the
Williams spine. This is the leading path after repair.

**A2. The algorithmic method scaled (dead, 0.07).** Theorem: $\mathsf{NP}
\not\subseteq \mathsf{P/poly}$ via a 2047 Witness-Compression Connection Theorem
plus an unconditional Boolean-rank-collapse SAT algorithm. Leap: the Compression
Lemma that lets Williams diagonalize at the polynomial $\mathsf{NP}$ witness scale
instead of the exponential $\mathsf{NEXP}$ scale. Breaks at: the easy-witness
step encodes the conclusion (circularity), and $2^{m^{0.001}}$ savings is a
mirage at feasible scale. Repair: the "Boolean-rank instead of polynomial-degree"
idea is the right anti-algebrization target; aim it at the honest frontier
($\mathsf{NEXP} \not\subseteq \mathsf{TC}^0$).

**A3. GCT delivers (dead, 0.04).** Theorem: a multiplicity obstruction separates
permanent from determinant, giving $\mathsf{VNP} \neq \mathsf{VP}$ and (via a
transfer) $\mathsf{P} \neq \mathsf{NP}$. Leap: compressing an infinite family of
multiplicity comparisons into one strict volume inequality. Breaks at: BIP gives
the opposite sign in the padded regime, and there is zero computed evidence of a
gap with the needed sign; the Boolean bridge routes through PIT and algebrizes.
Repair: abandon padding and the PIT bridge; pursue the machine-discovered
plethysm positivity as valuable representation theory regardless of P vs NP.

**A4. New proof-complexity engine for eF (dead, 0.06).** Theorem: an explicit
tautology family needs $2^{\Omega(n/\mathrm{polylog})}$-size Extended Frege
proofs, giving $\mathsf{NP} \neq \mathsf{coNP}$. Leap: replace feasible
interpolation with a witnessing-extracted monotone real protocol. Breaks at: the
witnessing core outputs a cost-bounded protocol that IS a feasible interpolant,
so BPR fires; a fork with no surviving branch. Repair: target an intermediate
system where the protocol-circuit duality breaks, or state the NW-generator
hypothesis explicitly as a conditional separation.

**A5. Fourth barrier + self-referential lifting (wounded, 0.04).** Theorem: a
self-referential SAT family whose models are fixpoints of its own refutation
search needs $2^{n^{\Omega(1)}}$-size circuits. Leap: define the fourth barrier
(bounded-interaction interface) correctly and escape it in the same stroke.
Breaks at: the toy XOR-aggregate has maximal coupling yet is in $\mathsf{ACC}^0$,
so the coupling-to-size lift is refuted by its own example. Repair: keep
self-reference as the anti-natural feature; aim first at a refutation-complexity
lower bound in an intermediate system with a non-$\mathsf{ACC}^0$ aggregate.

**A6. Independence from a strong arithmetic (wounded, 0.04).** Theorem: the
separating statement is unprovable in the strongest fragment of bounded
arithmetic, conditional on a cryptographic hypothesis; full ZFC-independence is
reoriented to "independence from feasible reasoning." Leap: a feasible witnessing
dichotomy converting the natural-proofs barrier into a formal unprovability
theorem. Breaks at: the $\mathsf{AC}^0$ specialization produces no contradiction,
so the contradiction in the $\mathsf{P/poly}$ case is entirely on loan from the
crypto assumption (which already implies $\mathsf{P} \neq \mathsf{NP}$, stronger
than the conclusion). Repair: reposition as a calibrated entry on the
proof-complexity-of-lower-bounds ladder; internalize Williams $\mathsf{ACC}^0$
inside the theory and show where it stalls.

**A7. Physics-native overlap-gap bridge (dead, 0.05).** Theorem: a worst-case
XOR-MAX-SAT on Ramanujan expanders needs $2^{\Omega(n/\mathrm{polylog})}$-size
circuits via a free-energy-width functional bounded below by the overlap-gap
diameter. Leap: a worst-case-to-average-case bridge preserving cluster geometry.
Breaks at: random k-XOR has a strong overlap gap yet is in $\mathsf{P}$, so the
width-implies-hardness inequality is false on a known-easy instance; the statistic
is also natural (large + constructive). Repair: keep the rigid expander geometry
as the hard core but deliver it through the Williams template, not thermodynamic
accounting.

**A8. The upset: $\mathsf{P} = \mathsf{NP}$, galactic (dead, 0.02).** Theorem:
3-SAT in time $O(n^k)$ with $k \le 6$, but with a galactic, non-constructively
bounded constant, via a Bounded-Degree Witness Manifold Theorem. Leap: that an
instance-dependent GL-coordinate change forces the satisfying set into a
bounded-degree semialgebraic variety. Breaks at: SoS-degree lower bounds for
random 3-XOR are invariant under GL reparameterization, so "bounded degree after a
coordinate change" is already false on the easiest fragment; the procedure
algebrizes. Repair: redirect the non-constructive WQO machinery from a collapse to
a lower bound in the Williams template.

**A9. Machine-found topological invariant (dead, 0.04).** Theorem: $\mathsf{NP}
\not\subseteq \mathsf{P/poly}$ via a persistent-homotopy invariant of the SAT
solution-space complex, machine-assembled and Lean-verified end to end. Leap: that
the homotopy type of a solution-space complex is a two-sided complexity invariant
(cheap to certify, impossible for small circuits, non-algebrizing). Breaks at: the
contradiction engine is a Lefschetz number, a characteristic-0 rational trace
functional that a low-degree oracle extension reconstructs, so it algebrizes at
the definition of the invariant. Repair: relocate the obstruction into a mod-2
torsion class and supply the Bockstein bridge of Section 3, which is the named
missing object the whole braid needs.
