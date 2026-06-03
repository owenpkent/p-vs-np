# The TC0-SAT Hinge, Grounded

Status: research note. Integrates a BUILDER synthesis, an ADVERSARY audit, and a
final fact-check pass against primary sources (multi-agent run, 2026-06-03). Residual
citations were web-confirmed by a follow-up pass the same day (see section 8).
Supersedes the "polynomial method dies at threshold gates" framing in
[`2050_backward_induction.md`](2050_backward_induction.md) (the threshold-hinge
paragraph and appendix A2) and the conflation in
[`../../experiments/LEARNINGS.md`](../../experiments/LEARNINGS.md) findings 8, 11,
and 13 (now corrected, with finding 20 added as the canonical statement).

Project stance: a barrier that rules out a class of techniques is a coordinate, not
a dead end. This note narrows where the TC0 work must live and names a concrete,
attackable target. It is scrupulous about proved versus open.

## 1. The one-line correction

The repo previously said: "the polynomial method that powered ACC0 provably stops
working at threshold gates, because MAJORITY has approximate degree $\Theta(n)$
(Paturi 1992), so it has no low-degree approximant." That slogan is false as stated,
and it conflates two different complexity measures.

- The ACC0 SAT algorithm and its threshold descendants consume **probabilistic
  degree**: a distribution over polynomials, each correct on each fixed input with
  probability at least $1 - \varepsilon$. By that measure MAJORITY, every linear
  threshold function, and every symmetric Boolean function has probabilistic degree
  $\Theta(\sqrt{n \log(1/\varepsilon)})$ (Alman-Williams 2015;
  Alman-Chan-Williams 2016).
- MAJORITY's worst-case **approximate degree** is $\Theta(n)$ (Paturi 1992). That
  fact is real, but it is a fact about a different quantity. It blocks the
  low-degree-APPROXIMATION (correlation) route to a lower bound. It does not block
  the probabilistic-polynomial SAT algorithm.

So the two numbers $\Theta(n)$ and $\Theta(\sqrt{n})$ are obstructions on opposite
sides of the hinge, and conflating them was the error. One more precision: Williams's
actual ACC0 algorithm does not even use Razborov-Smolensky approximation. It uses the
exact Yao-Beigel-Tarui / Allender-Gore depth-reduction of ACC to a SYM-of-AND
circuit, plus fast rectangular matrix multiplication.

## 2. What is proved (the solved rungs)

| Class | Result | Source | Confidence |
| --- | --- | --- | --- |
| ACC0 (AC0 with $\mathrm{MOD}_m$) | $\mathsf{NEXP} \not\subseteq$ poly-size ACC0; $\mathsf{E}^{\mathsf{NP}} \not\subseteq$ depth-$d$ size-$2^{n^\delta}$ ACC0, via a $2^{n - n^\delta}$-time ACC-SAT algorithm | Williams, CCC 2011 / JACM 2014 | HIGH |
| ACC0 of THR (one bottom threshold layer) | $\mathsf{NQP}$ has no $n^{\log^k n}$-size ACC of THR for every fixed $k$ and depth $d$, via an easy-witness lemma feeding Williams's 2014 ACC-of-THR SAT algorithm | Murray-Williams, STOC 2018 (ECCC TR17-188); Williams, STOC 2014 | HIGH (worst-case core) |
| AC0[m] of LTF of LTF, subquadratic bottom THRESHOLD GATE count | deterministic SAT in $2^{n - n^\varepsilon}$; via the Williams connection, $\mathsf{E}^{\mathsf{NP}}$ not in that class | Alman-Chan-Williams, FOCS 2016, Thm 1.8 and Cor 1.1 (arXiv:1608.04355) | HIGH |
| MAJ of AC0 of LTF of AC0 of LTF, $O(n^{6/5 - \delta})$ top/middle fan-in | randomized SAT in $2^{n - n^\varepsilon}$, using a probabilistic PTF of degree $\approx n^{1/3}$ (Thm 1.3) | Alman-Chan-Williams, FOCS 2016, Thm 1.9 (arXiv:1608.04355) | HIGH |
| Sparse depth-2 LTF-of-LTF ($cn$ wires) | nontrivial SAT with savings $2^{sn}$, $s = 1/c^{O(c^2)}$, via reduction to Vector Domination; useful near $c = 1$ | Impagliazzo-Paturi-Schneider, FOCS 2013 (arXiv:1212.4548) | HIGH (web-confirmed) |
| Depth-2 LTF gate/wire (explicit, NOT via the connection) | $\widetilde{\Omega}(n^{3/2})$ gates and $\widetilde{\Omega}(n^{5/2})$ wires for a function in P, via a Littlewood-Offord random-restriction argument | Kane-Williams, STOC 2016 (arXiv:1511.07860) | HIGH (web-confirmed) |
| Restricted depth-2 via sign-rank | THR-of-MAJ and MAJ-of-THR computing inner-product-mod-2 need exponential size; does NOT cover general LTF-of-LTF | Forster, CCC 2001 | HIGH |

Two corrections inside this table that the verified record forced and that any
reader must carry:

1. **The ACW 2016 paper title is "Polynomial Representations of Threshold Functions
   and Algorithmic Applications" (Alman, Chan, Williams, FOCS 2016,
   arXiv:1608.04355).** The earlier title "Probabilistic Polynomials and Hamming
   Nearest Neighbors" belongs to a different paper, Alman-Williams FOCS 2015
   (arXiv:1507.05106). The parameters above are confirmed verbatim against
   arXiv:1608.04355; only the title-to-year label had been wrong.
2. **The ACW 2016 restriction is on the number of bottom-layer linear threshold
   GATES ($n^{2-\delta}$ gates), not wires.** The lower-bound bracket in the paper
   is $[2^{n^\varepsilon}, 2^{n^\varepsilon}, n^{2-\delta}]$, where the third
   parameter is the bottom-LTF gate count. A separate $n^{2-o(1)}$-WIRE THR-of-THR
   bound exists (Chen-Tamaki / ACW) and must not be blurred with this gate bound. The
   repo had said "wires" throughout; that is corrected here.

The Kane-Williams entry carries one more precision: the $n^{5/2}$ WIRE lower bound is
the depth-2 result. The depth-3 statement in that paper is a MAJORITY upper bound
(Andreev's function in $O(n)$ majority gates), not a depth-3 $n^{5/2}$ wire lower
bound.

Citation status (updated by the 2026-06-03 residual-citation pass, all web-confirmed
unless noted; full identifiers in section 8). The average-case ACC-of-THR upgrade is
Chen, "Non-deterministic Quasi-Polynomial Time is Average-case Hard for ACC Circuits",
FOCS 2019 (ECCC TR19-031), giving $\mathsf{NQP}$ not $(1/2 + 1/\log^c n)$-approximable
by poly-size ACC0, extended to $2^{\log^a n}$-size ACC0-of-THR. The almost-everywhere
upgrade is Chen-Lyu-Williams, "Almost-Everywhere Circuit Lower Bounds from Non-Trivial
Derandomization", FOCS 2020 (ECCC TR20-150), giving $\mathsf{E}^{\mathsf{NP}}$ not
$(1/2 + 2^{-n^\varepsilon})$-approximable by $2^{n^\varepsilon}$-size ACC0 a.e.,
extended to AC0[m]-of-THR (Corollary 1.3, via the Williams 2014 #SAT algorithm). These
are two DISTINCT regimes and must not be conflated: Chen 2019 is infinitely-often,
quasi-polynomial size, inverse-polylog correlation; CLW 2020 is almost-everywhere,
exponential size, $2^{-n^\varepsilon}$ correlation. Chen-Santhanam-Srinivasan,
Bajpai et al, Chen-Tell, and the Chen 2018 Theorem 1.1 parameters are now confirmed
too (section 8). The one item still open: whether Chen 2018 (arXiv:1805.10698) ever
appeared in a peer-reviewed venue (it appears to be an unpublished preprint; DBLP was
unreachable during the check).

## 3. Solved versus open: the boundary is the SECOND threshold layer once the circuit is dense

- SOLVED: one threshold layer (ACC of THR, the $\mathsf{NQP}$ lower bound,
  Murray-Williams 2018), and one EXTRA threshold layer under an AC0[m] cap with a
  subquadratic bottom THRESHOLD-GATE count ($\mathsf{E}^{\mathsf{NP}}$ not in that
  class, ACW 2016 Cor 1.1).
- OPEN: any superpolynomial SIZE lower bound for $\mathsf{NEXP}$, $\mathsf{NQP}$, or
  even $\mathsf{E}^{\mathsf{NP}}$ against general THR of THR (dense depth-2
  LTF-of-LTF, no subquadratic-bottom restriction). The only known nontrivial
  THR-of-THR bound is a WIRE bound ($\mathsf{E}^{\mathsf{NP}}$ not in
  $n^{2-o(1)}$-wire THR of THR), which is not a size bound.

The obstruction is NOT the Williams connection (it is intact and even reduces the
depth-2 size lower bound to a polylog-dimension geometry problem, per Chen 2018,
medium confidence pending citation check). It is NOT depth in the abstract. It is the
missing SAT/CAPP/evaluation algorithm for DENSE two-threshold-layer circuits.

The dossier's phrase "$\mathsf{NEXP} \not\subseteq \mathsf{TC}^0$ as the first rung
past ACC0" is imprecise on two counts: the first threshold rung (one layer) is
already taken, and general $\mathsf{TC}^0$ is several rungs past the actual open
frontier (dense depth-2 THR-of-THR).

## 4. The concrete numerical target

A deterministic-or-co-nondeterministic satisfiability (or CAPP / GAP-UNSAT)
algorithm for DENSE depth-2 linear-threshold circuits, THR of THR (LTF-of-LTF) with
no subquadratic-bottom restriction, on $n$ inputs and $n^k$ gates, beating brute
force by a superpolynomial factor.

Two equivalent bars:

1. **SAT form.** Savings $2^{n^\varepsilon}$ for some $\varepsilon > 0$ over the
   $2^n \cdot \mathrm{poly}$ truth-table cost, i.e. running time
   $2^{n - n^\varepsilon}$, with the bottom threshold layer allowed DENSE ($n^{2+}$
   GATES, relaxing the ACW $n^{2-\delta}$-gate cap). By Williams 2010 (STOC 2010 /
   SICOMP 2013, Thm 1.1) ANY superpolynomial factor $n^{\omega(1)}$ over
   $2^n \cdot \mathrm{poly}$ suffices to fire $\mathsf{NEXP} \not\subseteq
   \mathsf{P/poly}$ through the connection; the ACC and ACW algorithms hit the
   stronger $2^{n - n^\varepsilon}$.
2. **Geometry form.** An $n^2 \cdot \mathrm{poly}(d) / \log^{\omega(1)} n$ time
   deterministic algorithm in polylogarithmic dimension $d$ for ANY of: Hopcroft's
   problem / integer Orthogonal-Vectors $Z\text{-}\mathrm{OV}_{n,d}$,
   $\ell_2$-Furthest-Pair, exact Bichromatic-$\ell_2$-Closest-Pair, or Max-IP, per
   Chen 2018 (Thm 1.1, web-confirmed verbatim 2026-06-03). Caveat (refined in
   subsection 4a): the DIMENSION regime, not Booleanity alone, decides the
   conclusion. The APPROXIMATE Bichromatic-Closest-Pair gives only the weaker
   SYM-of-THR (Thm 1.2). Boolean Max-IP at POLYLOG $d$ also gives only SYM-of-THR
   (Thm 1.2; this routing is in the theorem body, not the abstract,
   NEEDS-BODY-VERIFICATION), but Boolean Max-IP at $d = n^\varepsilon$ gives the full
   THR-of-THR (Thm 1.5). The reduction runs through two threshold-circuit structure
   lemmas (Chen 2018 Lemmas 1.6-1.7: Lemma 1.6 is a deterministic poly-time
   normal form, every THR-of-THR is a Gap-OR of THR-of-MAJ; Lemma 1.7 is a randomized
   subexponential form, every $s$-size THR-of-THR with $s = 2^{o(n)}$ is a
   DOR-of-MAJ-of-MAJ).

Either yields $\mathsf{NEXP} \not\subseteq$ poly-size THR of THR. How far known
algorithms are from this bar, and whether the bar is SETH-consistent, is mapped in
subsection 4a below.

Against what current best: ACW 2016 Thm 1.8 (deterministic $2^{n - n^\varepsilon}$
for AC0[m] of LTF of LTF but ONLY with $n^{2-\delta}$ bottom gates), and the trivial
$2^n \cdot \mathrm{poly}$ brute force. No nontrivial algorithm exists for the dense
case.

## 4a. Fine-grained gap map: how close are known algorithms to the Chen-2018 bar, and is the bar SETH-consistent?

Added 2026-06-03 (a two-survey + builder + adversary + verifier pass; all Chen-2018
and Chen-2020-ToC parameters web-confirmed verbatim against arXiv:1805.10698 and
arXiv:1802.02325, except two items flagged below). Section 4 states the geometry
reduction exists but never maps the algorithm-vs-bar gap or the SETH status. This
subsection supplies both. Runnable model:
[`../../experiments/circuit_complexity/e_threshold_geometry_gap.py`](../../experiments/circuit_complexity/e_threshold_geometry_gap.py)
(exit 0; smoke test stays 5/5).

The two questions: **Q-GAP** (for each problem/dimension/bar, the best-known
algorithm and the gap) and **Q-SETH** (would meeting the bar refute SETH, a barrier,
or is it SETH-consistent, genuinely open).

### The gap table (best-known vs the Thm 1.1 bar $n^2\,\mathrm{poly}(d)/\log^{\omega(1)} n$ at polylog $d$)

| Problem (dim) | Best known | Conclusion if met | SETH |
| --- | --- | --- | --- |
| **Exact integer geometry** {$Z$-OV/Hopcroft, $\ell_2$-Furthest-Pair, exact Bichrom.-$\ell_2$-Closest-Pair, $Z$-Max-IP}, polylog $d$ | $n^{2-1/O(d)}$ (Matousek 1992; AESW 1991; Yao 1982): at polylog $d$ this is $n^{2-o(1)}$, saved factor sub-$\log^1 n$, **zero log-shave** | THR-of-THR | consistent-open |
| Same four, $d = c\log n$ | $n^{2-1/O(\log n)}$: constant-factor saving only | THR-of-THR | consistent-open |
| **Boolean OV**, polylog $d$ (THE TRAP) | $n^{2-1/O(\log c)}$ (AWY SODA 2015; Chan-Williams SODA 2016): log-exponent grows, clears the SHAPE bar | **SYM-of-THR** | consistent-open |
| **Boolean Max-IP**, $d = n^\varepsilon$ (Thm 1.5.1, MOST ATTACKABLE) | $n^2\,\mathrm{polylog}$ via rectangular matmul (Coppersmith 1982): only logs separate baseline from bar | THR-of-THR | consistent-open |
| **Boolean Max-IP**, $d = \log^k n$ in $n^{2-\varepsilon}$ (Thm 1.5.2, THE LONE BARRIER) | $n^{2-\Omega(1/\sqrt{d/\log n})}$ (ACW FOCS 2016): only a log-shave at polylog $d$ | THR-of-THR | **WOULD-REFUTE-SETH** |
| $(1+\varepsilon)$-approx Bichrom.-$\ell_2$-Closest-Pair, $\varepsilon = 1/\log^3 n$ | $n^{2-\Omega(\varepsilon^{1/3})}$ as Chen restates it (see caveat) | SYM-of-THR | consistent-open |

### Q-GAP: the bottleneck, and why the Boolean-OV shave does not settle it

The THR-of-THR bottleneck is the **exact integer geometry at polylog $d$** (cleanest
single object: $Z$-Max-IP), equivalently **Boolean Max-IP at $d = n^\varepsilon$**.
Best-known shaves ZERO logs on the integer problems at polylog $d$; the full
$\log^{\omega(1)} n$ shave is the open gap. The most attackable single target is
Thm 1.5.1 (Boolean Max-IP at $n^\varepsilon$), where the baseline is already
$n^2\,\mathrm{polylog}$ (Coppersmith 1982) and only the logs need shaving.

The **Boolean-OV polynomial-method shave** (AWY SODA 2015, $n^{2-1/O(\log c)}$ at
$d = c\log n$) is a TRAP, for three independent reasons: (i) WRONG PROBLEM (Boolean
OV, not the integer/exact problems Thm 1.1 needs); (ii) WRONG DIMENSION (the exponent
$1/O(\log c)$ decays to $o(1)$ by polylog $d$); (iii) WRONG CONCLUSION, decisive
(Boolean routes through Thm 1.2 to the weaker SYM-of-THR, already attackable by
classical sign-rank / UPP methods). The model tags the AWY row `meets_bar=True` but
`conclusion=SYM-of-THR`. **Discipline to carry:** any "clears the bar" phrasing MUST
be paired with the conclusion strength, or it overclaims progress on the prize.

### Q-SETH: the bar is SETH-consistent, the target is genuinely open

SETH (via OVC, Williams 2005) forbids only a CONSTANT-exponent polynomial speedup
$n^{2-\Omega(1)}$. The Chen bar $n^2\,\mathrm{poly}(d)/\log^{\omega(1)} n$ is a pure
LOG-SHAVE: the exponent stays exactly $2$, the bar is itself $n^{2-o(1)}$, so it lives
strictly inside the band SETH guarantees and refutes nothing. Chen disclaims this
himself: the SETH bound "says nothing about whether shaving logs is possible."

PRECISION (pre-empts a misreading): polylog dimension is INSIDE the SETH-hard regime,
NOT below it. SETH-hardness reaches DOWN to $d = 2^{O(\log^\ast n)}$ for $Z$-Max-IP
(Chen, ToC 16(4) 2020; $\ell_2$-Furthest-Pair and Bichrom.-$\ell_2$-Closest-Pair
inherit via the Williams SODA 2018 reduction) and to $d = \omega((\log\log n)^2)$ for
the geometry problems (Williams SODA 2018). The target is open because of the
log-shave-vs-polynomial-shave SCALE gap, not because the dimension dodges SETH.

The LONE SETH-refuting route is Thm 1.5.2 (Boolean Max-IP at $d = \log^k n$ in
$n^{2-\varepsilon}$, constant $\varepsilon$): a genuine polynomial speedup at
$\omega(\log n)$. A builder must NOT pursue it as a live target. The other six routes
are SETH-consistent.

Honest status separation: it is PROVED that SETH forces $n^{2-o(1)}$ at
$2^{O(\log^\ast n)}$ (Chen ToC 16(4) 2020, verbatim). It is INFERRED (uncontroversially,
and stated by Chen) that this does NOT block the log-shave bar. There is no published
positive consistency theorem; the consistency is the safe inference that SETH
lower-bounds only at the $n^{2-\Omega(1)}$ granularity.

### Two flagged items (carry as hedges)

- NEEDS-BODY-VERIFICATION: "Boolean Max-IP at polylog $d \to$ SYM-of-THR (Thm 1.2)"
  is in the theorem BODY; the Chen-2018 ABSTRACT names only approximate closest-pair
  for Thm 1.2. The trap resolution does not depend on this routing claim.
- NEEDS-CITATION: the $(1+\varepsilon)$-approx closest-pair exponent. Chen 2018
  restates ACW 2016 as $n^{2-\Omega(\varepsilon^{1/3})}$; the ACW primary
  (arXiv:1608.04355) is $n^{2-\Omega(\varepsilon^{1/3}/\log(1/\varepsilon))}$.
  Non-load-bearing (both vanish at $\varepsilon = 1/\log^3 n$).

### Status stamp

As of June 2026, NEXP not in poly-size THR-of-THR remains OPEN; the Chen-2018 program
has not produced it. The only proved nontrivial THR-of-THR results are the
$n^{2-o(1)}$-WIRE bound (Chen-Tamaki / ACW) and the one-bottom-layer ACC-of-THR SIZE
bound (Murray-Williams 2018). arXiv:1805.10698 is an UNPUBLISHED preprint (DBLP: CoRR
only); the companion SETH paper IS published.

## 5. Why a purely algebraic-polynomial approach is not obviously enough, stated carefully

The audit caught a real error in the earlier framing, and the corrected statement is
more honest and weaker. We do NOT claim "combinatorial = non-algebrizing, algebraic =
algebrizing." That dichotomy is false within our own solved set: ACW 2016's
$2^{n - n^\varepsilon}$ algorithm for one extra threshold layer is built from
probabilistic polynomials (algebraic objects over a field) and it fired the Williams
connection to a real $\mathsf{E}^{\mathsf{NP}}$ lower bound. An algebraic tool already
crossed a threshold layer. So "algebraic method" and "algebrizes (survives the
Aaronson-Wigderson algebraic-oracle game)" are different axes.

What "opening the gate structure" is actually buying, stated as the defensible
content:

- A SYM-of-AND-style exact normal form (the YBT / Allender-Gore route the ACC
  algorithm evaluates by one matrix-multiplication pass) has no known analog when
  threshold gates feed threshold gates.
- The methods that have crossed threshold rungs read structure: Vector Domination
  (IPS 2013), the Littlewood-Offord random restriction (Kane-Williams 2016), the
  probabilistic-polynomial pass plus rectangular matrix multiplication (ACW 2016), or
  a geometric log-shave (Chen 2018).

Three honest reasons the dense, deeper case is hard, with their epistemic status:

1. **Composition budget (HEURISTIC, not a theorem).** Stacking $\sqrt{n}$-degree
   probabilistic polynomials across two or more DENSE threshold layers, with error
   driven below $2^{-n}$ so a union bound over all inputs survives (cost
   $\log(1/\varepsilon)$ inside the square root), plausibly pushes the evaluation
   cost $2^{\text{total degree}}$ past the $2^n$ brute-force bar. This is a
   directional reading. Both internal fact-checkers and the final fact-check mark it
   uncertain. Do not state it as fact.
2. **No known normal form (TRUE structural gap).** Point above: the SYM-of-AND pass
   has no threshold-feeds-threshold analog.
3. **A looming natural-proofs collision (LIVE, NOT EVADED).** See section 6.

## 6. Barrier profile, honest

The corrected target keeps the same nominal three-barrier shape as Williams's ACC0
proof, but only one of the three flags is genuinely defensible. The barrier checker
in [`../../experiments/_shared/barriers.py`](../../experiments/_shared/barriers.py)
is a transparent lookup: it returns the flags it is handed. So "the checker confirms
it evades all three" means only "the declared profile is recorded", not that any
proof object cleared the barriers.

- **Relativization: genuinely evaded.** Any real circuit-SAT/CAPP speedup must read
  the gate structure (the BGS engine in LEARNINGS finding 4 leaves a free string for
  a black-box machine). This is the one defensible flag, true by construction for
  SAT.
- **Natural proofs: CONDITIONALLY evaded, and this is arguably the binding
  constraint.** The probabilistic-polynomial method is non-natural the Williams 2013
  way, dropping largeness not constructivity (LEARNINGS finding 13). BUT ACW 2016
  warn that their richest threshold class "seems likely" to support pseudorandom
  function candidates (located 2026-06-03: arXiv:1608.04355, Section 1, page 5, the
  paragraph after Theorem 1.9, "It would not be surprising ... it seems likely that
  ..."; the underlying concern that poly-size $\mathsf{TC}^0$ computes PRFs is well
  established, e.g. Naor-Reingold PRFs in $\mathsf{TC}^0$, JACM 2004). Chen-Tell 2019
  independently flag the same collision: proving $n^{1+O(1/d)}$-wire TC0 bounds may
  require non-natural proofs, since Miles-Viola 2015 give a candidate PRF in depth-$d$
  $\mathsf{TC}^0$ with $n^{1+O(1/d)}$ wires. If dense poly-size $\mathsf{TC}^0$ supports strong
  PRFs, no natural property separates against it, and any constructive lower-bound
  method there collides with Razborov-Rudich. This is not yet evaded. It sits exactly
  where the target wants to reach, so natural-proofs evasion is a co-equal open
  obstruction, not a clean pass.
- **Algebrization: NOT YET ASSESSABLE, not "evaded".** The flag $\mathsf{algebrizes}
  = \mathsf{False}$ is a property of a HYPOTHETICAL algorithm whose mechanism does
  not yet exist. No cited source establishes it; arXiv:1608.04355 does not contain
  the word "algebrization". You cannot assign a non-algebrization verdict to an
  object whose computational mechanism is undetermined. The honest status is
  "algebrization not yet assessable", which is weaker than "asserted". This is the
  single most fragile point and it is in the SAME epistemic state as the retired
  "Boolean-rank collapse" placeholder: a named hope with no theorem.

One further claim must be marked SPECULATION, not used as load-bearing: the assertion
that the dual-polynomial / pattern-matrix LP method "algebrizes" (used to argue the
approximate-degree route cannot be the non-algebrizing ingredient) is project
inference, NOT an Aaronson-Wigderson theorem. AW algebrization is about query access
to a low-degree oracle EXTENSION, not about whether a lower-bound certificate is an
LP/spectral functional. "Is a low-degree algebraic functional" and "survives the AW
game" are different properties. The defensible reason to set that route aside is
simpler: it is NATURAL (large plus constructive) and hits Razborov-Rudich. Use that,
drop the algebrization claim for that route, or mark it needs-citation.

## 7. The "Boolean-rank collapse" name: honest verdict

"Boolean-rank collapse" is a project coinage with NO published theorem behind it. As
used in the repo it was a vague gesture, not an object. It should be (and now is, in
the experiment) renamed.

There IS a real cluster of objects in the neighborhood: sign-rank / dimension
complexity, margin complexity, threshold weight, the unbounded-error communication
measure UPP. These carry genuine exponential lower bounds for RESTRICTED depth-2
threshold (Forster 2001 for THR-of-MAJ; Razborov-Sherstov 2010 for sign-rank of
AC0). But sign-rank PROVABLY cannot crack general THR of THR: Chattopadhyay-Mande
("Weights at the Bottom Matter When the Top is Heavy", ECCC TR17-083 /
arXiv:1705.02397) exhibit a function with LINEAR-size THR-of-THR circuits yet
sign-rank $2^{\Omega(n^{1/4})}$, so any hoped-for object must go strictly beyond
sign-rank. The real, citable frontier objects are
therefore (a) a dense depth-2 LTF-of-LTF SAT/CAPP speedup (open; sparse case solved
by IPS 2013) and (b) the equivalent log-shaving geometry algorithm of Chen 2018. The
fix: drop the placeholder as if it named a known candidate; re-point the object at
its real referents; and do NOT let a runnable self-check imply the algebrization
barrier has been independently cleared.

## 8. References (verified this pass unless flagged)

- R. Williams. "Improving exhaustive search implies superpolynomial lower bounds."
  STOC 2010, DOI 10.1145/1806689.1806723; SICOMP 2013. VERIFIED (Crossref).
- R. Williams. "Non-uniform ACC circuit lower bounds." CCC 2011 / JACM 2014. NEXP not
  in ACC0. VERIFIED (well-established).
- J. Alman, R. Williams. "Probabilistic polynomials and Hamming nearest neighbors."
  FOCS 2015, arXiv:1507.05106. Symmetric Boolean functions have probabilistic degree
  $O(\sqrt{n \log(1/\varepsilon)})$, optimal. VERIFIED (arXiv abstract).
- J. Alman, T. M. Chan, R. Williams. "Polynomial representations of threshold
  functions and algorithmic applications." FOCS 2016, arXiv:1608.04355. Thm 1.3 (PTF
  degree $\approx n^{1/3}$), Thm 1.8 (deterministic $2^{n-n^\varepsilon}$ SAT for
  AC0[m] of LTF of LTF, subquadratic bottom GATE count), Thm 1.9 (randomized, MAJ of
  AC0 of LTF of AC0 of LTF, $O(n^{6/5-\delta})$ fan-in), Cor 1.1
  ($\mathsf{E}^{\mathsf{NP}}$ lower bound). VERIFIED verbatim (arXiv:1608.04355).
- R. Paturi. "On the degree of polynomials that approximate symmetric Boolean
  functions." STOC 1992, DOI 10.1145/129712.129758. $\widetilde{\deg}(\mathrm{MAJ}) =
  \Theta(n)$, $\widetilde{\deg}(\mathrm{OR/AND}) = \Theta(\sqrt{n})$. VERIFIED
  (Crossref).
- A. Razborov (1987), R. Smolensky (1987). Matching
  $\Omega(\sqrt{n \log(1/\varepsilon)})$ probabilistic-degree lower bound for
  MAJORITY. VERIFIED (via the AW 2015 abstract attribution).
- R. Williams. "New algorithms and lower bounds for circuits with linear threshold
  gates." STOC 2014 / Theory of Computing 14:17 (2018). ACC-of-THR SAT/evaluation.
  VERIFIED (referenced by Murray-Williams).
- C. Murray, R. Williams. "An easy witness lemma for NP and NQP." STOC 2018, ECCC
  TR17-188. NQP not in $n^{\log^k n}$-size ACC of THR. VERIFIED (ECCC).
- R. Impagliazzo, R. Paturi, S. Schneider. "A satisfiability algorithm for sparse
  depth two threshold circuits." FOCS 2013, arXiv:1212.4548. Savings $2^{sn}$,
  $s = 1/c^{O(c^2)}$, via Vector Domination. VERIFIED (arXiv abstract).
- D. Kane, R. Williams. "Super-linear gate and super-quadratic wire lower bounds for
  depth-two and depth-three threshold circuits." STOC 2016, arXiv:1511.07860.
  $\widetilde{\Omega}(n^{3/2})$ gates, $\widetilde{\Omega}(n^{5/2})$ wires at depth 2,
  Littlewood-Offord. VERIFIED (arXiv).
- J. Forster. "A linear lower bound on the unbounded error probabilistic
  communication complexity." CCC 2001, DOI 10.1109/ccc.2001.933877. Sign-rank /
  linear UPP lower bound for inner-product-mod-2. VERIFIED (Crossref).
- L. Chen. "Toward super-polynomial size lower bounds for depth-two threshold
  circuits." arXiv:1805.10698 (2018), unpublished preprint (DBLP: CoRR only). Reduces
  a depth-2 THR-of-THR size lower bound to a polylog-dimension geometry log-shave.
  Thm 1.1 (the five exact integer/real problems), Thm 1.2 (the weaker SYM-of-THR via
  approximate closest-pair / Boolean Max-IP at polylog $d$), Thm 1.5 (modest-dimension
  Max-IP), and Lemmas 1.6-1.7 (the structure lemmas) all VERIFIED VERBATIM
  (2026-06-03, read from the arXiv PDF). See subsection 4a for the gap map.
- L. Chen. "On the hardness of approximate and exact (bichromatic) maximum inner
  product." CCC 2018 / Theory of Computing 16(4):1-50 (2020), DOI
  10.4086/toc.2019.v016a004 (arXiv:1802.02325). The companion SETH paper (Chen 2018's
  internal `[Che18]`): exact integer Max-IP requires $n^{2-o(1)}$ under SETH already at
  dimension $d = 2^{O(\log^\ast n)}$. PUBLISHED (unlike arXiv:1805.10698). VERIFIED
  verbatim (2026-06-03).
- R. Williams. "On the difference between closest, furthest, and orthogonal pairs:
  nearly-linear vs barely-subquadratic complexity." SODA 2018 (arXiv:1709.05282). The
  SETH reduction giving $d = \omega((\log\log n)^2)$ hardness for the geometry
  problems. VERIFIED (abstract).

Confirmed by the 2026-06-03 residual-citation pass (web-grounded, with identifiers):

- L. Chen. "Non-deterministic Quasi-Polynomial Time is Average-case Hard for ACC
  Circuits." FOCS 2019, ECCC TR19-031; SICOMP 54(4) 2025, DOI 10.1137/20M1321231.
  $\mathsf{NQP}$ not $(1/2 + 1/\log^c n)$-approximable by poly-size ACC0; extends to
  $2^{\log^a n}$-size ACC0-of-THR (infinitely-often, quasi-poly size).
- L. Chen, X. Lyu, R. Williams. "Almost-Everywhere Circuit Lower Bounds from
  Non-Trivial Derandomization." FOCS 2020, ECCC TR20-150.
  $\mathsf{E}^{\mathsf{NP}}$ a.e. not $(1/2 + 2^{-n^\varepsilon})$-approximable by
  $2^{n^\varepsilon}$-size ACC0; Cor 1.3 extends to AC0[m]-of-THR.
- R. Chen, R. Santhanam, S. Srinivasan. "Average-Case Lower Bounds and Satisfiability
  Algorithms for Small Threshold Circuits." CCC 2016, DOI 10.4230/LIPIcs.CCC.2016.1;
  Theory of Computing 14:9 (2018); arXiv:1806.06290. Depth-$d$ threshold,
  $\le n^{1+\varepsilon_d}$ wires; SAT beating brute force for depth $> 2$; Parity
  correlation $n^{-\varepsilon_d}$, Generalized Andreev $\exp(-n^{\varepsilon_d})$.
- S. Bajpai, V. Krishan, D. Kush, N. Limaye, S. Srinivasan. "A #SAT Algorithm for
  Small Constant-Depth Circuits with PTF Gates." ITCS 2019,
  DOI 10.4230/LIPIcs.ITCS.2019.8; ECCC TR18-162; arXiv:1809.05932. Depth-$d$
  $k$-PTF, size $\le n^{1+\varepsilon}$, zero-error randomized #SAT in
  $2^{n - n^{\Omega(\varepsilon)}}$.
- L. Chen, R. Tell. "Bootstrapping Results for Threshold Circuits 'Just Beyond' Known
  Lower Bounds." STOC 2019, DOI 10.1145/3313276.3316333; ECCC TR18-199.
  $n^{1+c^{-d}}$-wire bootstrapping with $c = 1 + \sqrt{2} \approx 2.41$ (the
  Impagliazzo-Paturi-Saks 1997 parity bound, too large to give new bounds); shaving
  $c$ for all large $d$ gives $\mathsf{TC}^0 \neq \mathsf{NC}^1$, and a $c = 1.61$
  derandomization gives $\mathsf{NEXP} \not\subseteq \mathsf{TC}^0$. The paper itself
  flags the natural-proofs collision via Miles-Viola 2015.
- A. Razborov, A. Sherstov. "The Sign-Rank of $\mathsf{AC}^0$." SICOMP 39(5):1833-1855
  (2010), DOI 10.1137/080744037; FOCS 2008, pp. 57-66. First exponential sign-rank
  lower bound for a function in AC0.
- A. Chattopadhyay, N. Mande. "Weights at the Bottom Matter When the Top is Heavy."
  ECCC TR17-083; arXiv:1705.02397. A linear-size THR-of-THR function with sign-rank
  $2^{\Omega(n^{1/4})}$: sign-rank alone cannot prove THR-of-THR lower bounds.
- M. Naor, O. Reingold. "Number-theoretic constructions of efficient pseudo-random
  functions." FOCS 1997 / JACM 51(2) (2004), DOI 10.1145/972639.972643. PRFs
  computable in $\mathsf{TC}^0$.

Still open: whether Chen 2018 (arXiv:1805.10698) appeared in a peer-reviewed venue
(it appears to be an unpublished preprint; DBLP was unreachable during the check).

## 9. Residual uncertainties for human review

The 2026-06-03 citation pass resolved every previously-flagged lookup (venues, years,
identifiers, and theorem parameters for Chen 2019, Chen-Lyu-Williams 2020,
Chen-Santhanam-Srinivasan, Bajpai et al, Chen-Tell, Razborov-Sherstov, the ACW PRF
remark, and Chen 2018 Theorem 1.1; see section 8). What remains is genuinely open
(not a lookup) and should be resolved by a human expert:

- Whether the dual-polynomial / pattern-matrix LP method "algebrizes" in any
  Aaronson-Wigderson sense. This is project inference, marked speculation; no
  published statement to this effect was found. The defensible disqualifier for that
  route is naturalness, not algebrization.
- Whether the "budget composition" heuristic (stacking $\sqrt{n}$-degree probabilistic
  polynomials over $\omega(1)$ dense layers pushes $2^{\text{total degree}}$ past
  $2^n$) can be made a theorem or refuted. Currently a directional reading only.
- Minor: whether Chen 2018 (arXiv:1805.10698) was ever published beyond arXiv (DBLP
  was unreachable during the citation pass; it appears to be an unpublished preprint).
