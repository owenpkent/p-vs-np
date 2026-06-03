# The TC0-SAT Hinge, Grounded

Status: research note. Integrates a BUILDER synthesis, an ADVERSARY audit, and a
final fact-check pass against primary sources (multi-agent run, 2026-06-03).
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

Citations marked needs-citation (training knowledge only, not web-confirmed this
pass): the average-case ACC-of-THR upgrade (Chen, plausibly FOCS 2019) and the
almost-everywhere upgrade (Chen-Lyu-Williams, "Almost-Everywhere Circuit Lower Bounds
from Non-Trivial Derandomization", plausibly FOCS 2020); Chen-Santhanam-Srinivasan
(CCC 2016) on low-wire depth-$d$ threshold SAT and average-case correlation;
Bajpai-Krishan-Kush-Limaye-Srinivasan (ITCS 2019) on near-linear $k$-PTF #SAT;
Chen-Tell (STOC 2019) on the $n^{1+c^{-d}}$ wire bootstrapping with $c \approx 2.41$
giving $\mathsf{TC}^0 \neq \mathsf{NC}^1$; and the exact Theorem 1.1 parameters of
Chen 2018 (arXiv:1805.10698; paper existence and title "Toward Super-Polynomial Size
Lower Bounds for Depth-Two Threshold Circuits" are confirmed, the precise problem
list and "shave all polylog factors" bar are not re-fetched).

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
2. **Geometry form.** An $n^2 \cdot \mathrm{poly}(d) / \log^{\omega(1)} n$ algorithm
   (shave ALL polylog factors) for a polylog-dimension closest/furthest-pair problem
   ($\ell_2$-Furthest-Pair, Bichromatic-Closest-Pair, Hopcroft, or Max-IP), per
   Chen 2018 (Thm 1.1, medium confidence pending citation check).

Either yields $\mathsf{NEXP} \not\subseteq$ poly-size THR of THR.

Against what current best: ACW 2016 Thm 1.8 (deterministic $2^{n - n^\varepsilon}$
for AC0[m] of LTF of LTF but ONLY with $n^{2-\delta}$ bottom gates), and the trivial
$2^n \cdot \mathrm{poly}$ brute force. No nontrivial algorithm exists for the dense
case.

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
  function candidates (specific sentence attribution needs-citation; the underlying
  concern that poly-size $\mathsf{TC}^0$ plausibly computes PRFs, Naor-Reingold
  style, is well established). If dense poly-size $\mathsf{TC}^0$ supports strong
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
AC0). But sign-rank PROVABLY cannot crack general THR of THR: there is a function
with linear-size THR-of-THR circuits yet exponential sign-rank, so any hoped-for
object must go strictly beyond sign-rank. The real, citable frontier objects are
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
  circuits." arXiv:1805.10698 (2018). Reduces a depth-2 THR-of-THR size lower bound
  to a polylog-dimension geometry log-shave. Title VERIFIED; exact Thm 1.1 parameters
  needs-citation.

needs-citation (training knowledge only): Chen (avg-case ACC-of-THR, plausibly
FOCS 2019); Chen-Lyu-Williams ("Almost-Everywhere Circuit Lower Bounds from
Non-Trivial Derandomization", plausibly FOCS 2020); Chen-Santhanam-Srinivasan
(CCC 2016); Bajpai-Krishan-Kush-Limaye-Srinivasan (ITCS 2019); Chen-Tell (STOC 2019,
$c \approx 2.41$); Razborov-Sherstov (sign-rank of AC0, 2010); the ACW "seems likely
supports PRFs" sentence.

## 9. Residual uncertainties for human review

These survived the fact-check as needs-citation or uncertain and should be confirmed
by a human expert before any of them is treated as settled:

- Venue/year of the average-case (Chen) and almost-everywhere (Chen-Lyu-Williams)
  ACC-of-THR upgrades.
- The exact Theorem 1.1 statement of Chen 2018 (which geometry problems, the precise
  log-shaving bar).
- Exact parameters and venues of Chen-Santhanam-Srinivasan, Bajpai et al, and
  Chen-Tell ($c \approx 2.41$).
- The exact ACW "seems likely supports PRFs" sentence (the underlying
  TC0-computes-PRFs concern is independently well established).
- Whether the dual-polynomial / pattern-matrix LP method "algebrizes" in any
  Aaronson-Wigderson sense (currently project inference, marked speculation).
- Whether the "budget composition" heuristic can be made a theorem or refuted.
- The Razborov-Sherstov 2010 sign-rank-of-AC0 citation and the exact statement of the
  THR-of-THR-with-exponential-sign-rank separation used in section 7.
