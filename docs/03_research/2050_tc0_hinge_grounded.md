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
   (Thm 1.2 item 1, now CONFIRMED verbatim in the body, p.2), but Boolean Max-IP at
   $d = n^\varepsilon$ gives the full THR-of-THR (Thm 1.5). The reduction runs through two threshold-circuit structure
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

- RESOLVED (was NEEDS-BODY-VERIFICATION): "Boolean Max-IP at polylog $d \to$
  SYM-of-THR (Thm 1.2)" is now confirmed verbatim in the theorem body (Thm 1.2 item 1,
  p.2, read 2026-06-03 during the subsection-4b pass). The abstract names only
  approximate closest-pair; the body is literally Boolean Max-IP$_{n,d}$ at polylog $d$.
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

## 4b. The Max-IP-at-$n^\varepsilon$ log-shave, attacked

Added 2026-06-03 (a two-survey + builder + adversary + verifier pass; the Chen-2018
abstract/body parameters re-confirmed verbatim against arXiv:1805.10698, the technique
parameters web-confirmed against their venues, with two items hedged below). Subsection
4a names Boolean Max-IP at $d = n^\varepsilon$ (Thm 1.5 item 1) as the single most
attackable target but stops at "only the logs separate baseline from bar". This
subsection attacks that bar: it pins the decomposition of the polylog, maps every known
log-shaver against it, reports a tried-and-failed micro-idea, and confirms no finer
barrier. Runnable model:
[`../../experiments/circuit_complexity/e_maxip_logshave.py`](../../experiments/circuit_complexity/e_maxip_logshave.py)
(exit 0; smoke test stays 5/5), the executable companion to the problem-indexed
[`e_threshold_geometry_gap.py`](../../experiments/circuit_complexity/e_threshold_geometry_gap.py).

### The target and its baseline, decomposed

TARGET (Thm 1.5 item 1, verbatim): a deterministic Max-IP$_{n, n^\varepsilon}$ algorithm
in $n^2 / \log^{\omega(1)} n$ time, for some constant $\varepsilon > 0$, gives
$\mathsf{NEXP} \not\subseteq$ poly-size THR-of-THR. BASELINE (verbatim, p.3): $n^2\,
\mathrm{polylog}(n)$ via Coppersmith 1982 fast rectangular matrix multiplication, which
computes $M = A B^\top$ (all $n^2$ inner products) since $d = n^\varepsilon$ is below the
rectangular dual exponent $\alpha$ ($\alpha = 0.17227$ in 1982; current best $\alpha \ge
0.321334$, Williams-Xu-Xu-Zhou 2023/24). Chen states the goal verbatim: "we only need to
shave logs on this naive algorithm". The polylog has TWO sources:

- (a) RECTANGULAR-MM OVERHEAD $\log^2 n$, intrinsic to Coppersmith's bilinear / partial-
  matrix-multiplication recursion (the $C N^2 \log^2 N$ essential-multiplications bound).
  Dual-exponent improvements (Le Gall 2012; Le Gall-Urrutia SODA 2018; WXXZ 2023) only
  RAISE the $\varepsilon$-ceiling at which the $n^2$-polylog baseline holds; they do NOT
  shave this $\log^2 n$ (project inference from the bilinear framework, verifier-endorsed).
- (b) THE MAX-OVER-$n^2$ EXTRACTION, a flat $\Theta(n^2)$ scan with zero achievable
  log-shave under enumeration, since the all-pairs inner-product MATRIX has $\Omega(n^2)$
  natural output size (scoped to the matrix, NOT to Max-IP as a problem). PROJECT
  INFERENCE (flagged): a log-shave must compute the max WITHOUT materializing-and-scanning
  all $n^2$ inner products, so the structural novelty must live in max-extraction-without-
  enumeration, not in the matrix product.

### The technique map at $d = n^\varepsilon$ (every row falls short)

| Technique | Saving at $d=n^\varepsilon$ | Log-shave? | Precise shortfall |
| --- | --- | --- | --- |
| Polynomial method (AWY SODA 2015; Chan-Williams SODA 2016) | $2^{O(1/\varepsilon)} = O(1)$ constant factor | NO | Saved exponent $1/O(\varepsilon\log n)\to 0$; batch collapses as poly. degree scales with $d$. Also OV/existence $\to$ SYM-of-THR (Thm 1.2). Double-disqualified. |
| Four-Russians / BMM (Bansal-Williams 2009; Chan 2015; Abboud-Fischer-Kelley-Lovett-Meka STOC 2024, $n^3/2^{\Omega((\log n)^{1/7})}$) | zero transfer | NO | WRONG OPERATION + semiring (sharpened, finding 27). AFKLM's shave solves triangle DETECTION: a dense uniform piece certifies "some entry is nonzero" with NO computation (an OR-idempotent collapse, one witness suffices). That discards exactly the integer counts $\langle a,b\rangle$ a MAX needs; the authors leave the non-Boolean / $(\min,+)$ generalization explicitly open ("min has no inverse"). AFKLM must NOT be cited as Max-IP progress. |
| Rectangular MM (Coppersmith 1982; Le Gall; WXXZ) | this IS the baseline | NO | The $\log^2 n$ it carries is the polylog to remove and is intrinsic; dual-exponent gains move $\alpha$, not the polylog. Closest in FORM, zero progress on the shave. |
| Large-sieve (Jin-Xu STOC 2024, arXiv:2403.20326) | not applicable | NO | Scope is sparse convolution + 1D text-to-pattern Hamming; no 1D structure in all-pairs Max-IP, the max couples across all $n^2$ pairs. |
| Exact integer geometry (Matousek 1992; AESW 1991; Yao 1982; Williams SODA 2018) | $1+o(1)$, $< 1$ log | NO | $n^{2-1/O(d)}$; at $d=n^\varepsilon$ the saved exponent $1/O(n^\varepsilon)$ vanishes super-polynomially. |
| Min-plus / Razborov-Smolensky (Williams APSP STOC 2014, $n^3/2^{\Omega(\sqrt{\log n})}$) | wrong operation | NO | WRONG OPERATION, not just scale (sharpened, finding 27). Williams computes a $(\min,+)$ PRODUCT, a per-entry reduction over the contraction index $k$ FUSED into each of the $n^2$ outputs. Max-IP is a standard $(+,\times)$ product with NO per-entry reduction, then ONE global MAX over the OUTPUT indices $(i,j)$. Different reductions on different axes; the fusion hook the engine exploits is ABSENT, so it is a wrong-target wall (operation primary; the $n^\varepsilon$ scale decay to $2^{O(1/\varepsilon)}$ is secondary). |

SMALLEST GAP (two readings disagree, and that IS the finding): by literal-object
closeness, rectangular MM is first (it IS the baseline, one polylog away in form, shaves
zero); by largest-actual-saving, the polynomial method is first (a real constant
$2^{O(1/\varepsilon)} \approx 1024$ for $\varepsilon=0.1$, wrong shape). No technique is
both close in form AND making log-progress. Precisely: shave the intrinsic $\log^2 n$ off
$n^{2+o(1)}$ rectangular MM at the Coppersmith $\alpha$-boundary, for the $(+,\times)$
product with a max-reduction, without enumerating the $n^2$ pairs. That sub-problem is
itself open and is the precise frontier.

### The J1 transfer attempt: the n^3 machinery does not port, for an OPERATION reason (finding 27)

The named most-promising angle was to transfer the $n^3$-scale all-logs machinery DOWN
to the $n^2$-scale count-then-max product. A dedicated pass (modeled in
[`../../experiments/circuit_complexity/e_j1_transfer.py`](../../experiments/circuit_complexity/e_j1_transfer.py))
shows this does NOT port, and the obstruction is OPERATION, not scale. AFKLM 2024 shaves
triangle DETECTION via an OR-idempotent collapse (a dense uniform piece certifies "some
entry is nonzero" with no computation), which discards the integer counts a MAX needs;
Williams 2014 shaves a $(\min,+)$ PRODUCT (a per-entry reduction fused into each output),
but Max-IP has no per-entry reduction, only ONE global max over the output indices. Both
wins come from operations Max-IP does not have. This is FUNDAMENTAL as a transfer of the
existing engines, BUT it is not a barrier on the target: the real frontier is the
FUSED-MAX-MM problem (compute $\max_{ij}(A B^\top)_{ij}$ for small-range entries, fused
into the rectangular MM, without materializing the $n^2$ entries), which is OPEN at the
log-shave scale, SETH-consistent, and barrier-free among published results. No known fused
product touches it: dominance ($n^{2.69}$), $(\max,\min)$/bottleneck (Vassilevska-Williams-
Yuster), and bounded-range $(\min,+)$ (ESA 2024) are polynomial speedups at $n^3$
full-square, per-entry, not a log-shave at thin $n^\varepsilon$. Bichromatic Max-IP is
truly-subquadratic EQUIVALENT to OV (Chen, SODA 2019, arXiv:1811.12017), but at the
polynomial $n^{2-\Omega(1)}$ granularity, so it neither delivers a log-shave nor lets
OV/SETH rule one out. So J1's frontier is sharpened: not "transfer the machinery" (a
fundamental operation mismatch) but "build a fused-max-MM log-shave" (open, no machinery
known to touch it, the structural novelty must be max-extraction-without-enumeration).

### The micro-idea: threshold sweep (correct, but strictly cost-increasing)

Since the answer is an integer in $\{0,\dots,d\}$, sweep a candidate threshold $t$ from
$d$ downward and test existence of a pair with $\langle a,b\rangle \ge t$ (a $Z$-OV-like
decision), the max being the largest $t$ with a YES; or binary-search $t$. In
`e_maxip_logshave.py` (run on $n_A=n_B=40$, $d=12$) this is CORRECT (returns the true max
$9$, asserted against brute force) but does NOT shave, and the failure step is named: the
existence-query subroutine. Each query at $d=n^\varepsilon$ is itself at the open
$n^\varepsilon$ wall (certifying a NO rules out all $n^2$ pairs, worst-case $n^2$). The
LINEAR sweep makes $O(d)=O(n^\varepsilon)$ worst-case queries, MULTIPLYING the baseline by
$n^\varepsilon$ (a polynomial factor WORSE); BINARY search makes $O(\log d)=O(\varepsilon
\log n)$ queries, each still the $n^2$ wall, so it ADDS a log factor rather than removing
the polylog. Reducing Max to existence does not help because existence at $d=n^\varepsilon$
is the SAME open wall. The micro-idea FAILS. (Honest debugging note: the linear sweep
early-stops at the first YES, so on the high-max test it made only $4$ queries, not $d+1$;
the accounting was corrected to worst-case bounds, the load-bearing honest version.)

### Finer-barrier verdict: open, with one structural wall and one inherited collision

No finer UNCONDITIONAL barrier was found beyond the non-binding SETH-consistency (the bar
is $n^{2-o(1)}$, SETH forbids only $n^{2-\Omega(1)}$). The decisive check: the strongest
"hardness of shaving logs" theorems (Abboud-Hansen-V.Williams-R.Williams STOC 2016,
arXiv:1511.06022; Abboud-Bringmann ICALP 2018, arXiv:1804.08978) are proved ONLY for
SEQUENCE/alignment problems whose quadratic DP encodes a branching program; they provably
do NOT cover OV or Max-IP. So the candidate finer barrier does not bind, and the Chen
implication is a WANTED route, not an obstruction. Two finer obstructions, neither a proved
barrier: (i) the matrix-output wall ($\Omega(n^2)$ natural output size of $A B^\top$,
scoped to the matrix, not the problem), which pins WHERE a new idea must act
(max-without-enumeration); (ii) the inherited natural-proofs question (corrected in
section 6 / finding 25): the PRF collision binds the LARGE-and-constructive alternatives,
NOT the non-large Williams route, so it is evaded at the NEXP-level bound and re-enters
only at the NEXP-to-NP descent, where the escape flips to non-constructivity.

### Target-widening (project inference, carry as a hedge)

The final Williams-connection step needs only a CO-NONDETERMINISTIC THR-of-MAJ UNSAT (or
Max-IP-decision) algorithm (Chen Remarks 2.7, 4.2, as read by the survey; the deterministic
Thm 1.5 hypothesis is the clean statement because the structure-lemma reduction is randomized
and is derandomized by nondeterministic guessing). The verbatim remark text was NOT
independently web-confirmed this pass, so this is carried as project inference, not a
separately-stated theorem; a two-sided randomized Max-IP solver is not obviously enough
without derandomization. A builder targeting the cleanest path should aim at a deterministic-
or-co-nondeterministic UNSAT log-shave, wider than the stated deterministic hypothesis.

### Status stamp

As of June 2026 the target is GENUINELY OPEN: no published algorithm shaves the polylog off
Max-IP at $d = n^\varepsilon$; if one existed, $\mathsf{NEXP} \not\subseteq$ poly-size
THR-of-THR would be proven, and it is not. arXiv:1805.10698 remains an unpublished preprint
(DBLP: CoRR only).

## 4c. The fused-max-MM, BUILT: four candidate constructions, one shared wall (finding 28)

Added 2026-06-04 (a three-survey + four-builder + adversary-per-candidate + verifier pass;
the Chen-2018 and log-shaving-hardness parameters re-confirmed against their venues, two
adversary corrections applied and re-verified). Subsection 4b named the fused-max-MM as the
real J1 frontier and stopped at "no machinery is known to touch it, the structural novelty
must be max-extraction-without-enumeration." This subsection BUILDS that frontier as four
natural constructions, pins the ONE wall they share, and names the precise missing property.
Runnable model:
[`../../experiments/circuit_complexity/e_fused_max_mm.py`](../../experiments/circuit_complexity/e_fused_max_mm.py)
(exit 0; smoke test stays 5/5), the executable companion to
[`e_j1_transfer.py`](../../experiments/circuit_complexity/e_j1_transfer.py).

### The four natural machineries (each a genuine subquadratic fusion)

| Candidate | What it fuses (no $n^2$ materialization) | Subquadratic regime | Why it cannot read the max |
| --- | --- | --- | --- |
| B1 Moment / tensor-power | $m_p = \langle \sum_i a_i^{\otimes p}, \sum_j b_j^{\otimes p}\rangle$ in dim $d^p$ (exact $p$-th moments) | $P < 1/\varepsilon$ (cost $n^{1+\varepsilon P}$) | Degree-$\le P$ readout; top-value indicator needs degree $\ge d$. Vandermonde: max free iff $K \le d-1$. |
| B2 Spectral / low-rank | $\|M\|_F$, $\sigma_{\max}$, full spectrum, row 2-norms via the $d\times d$ core | $O(n d^2) = n^{1+2\varepsilon}$ | Rotation-invariant ($\ell_2$); the max is $\ell_\infty$. Equal-spectrum spread-vs-spike, max-ratio exactly $n$. |
| B3 Count-preserving regularity | per-block-pair average density $\rho_{s,t} d$ (rebuilt AFKLM, counts kept) | few blocks $\Rightarrow$ $B^2 d \ll n^2$ | Averages, not tails. A planted cell moves the max by $\Theta(d)$, every density by $O(1/n)$. |
| B4 Sketch / heavy-hitter | signed hashed bucket-sums (Pagh CMM + count-sketch) | width $w \ll n^2$ if argmax is heavy | Dense argmax is $\ell_2$-LIGHT (heaviness $\Theta(1/n^2)$); Frobenius primitive misses it. |

### The one shared wall (bulk vs extreme)

Each fusion computes a BULK statistic ($\ell_2$ / average / low-moment / spectral /
Frobenius) of the $n^2$ inner products; the Max-IP answer is an $\ell_\infty$ / extreme /
large-deviation statistic. The binding constraint, sharpened by the adversary on B2 and
endorsed by the verifier, is not any one engine's multiplicative window but the
INTEGER-GAP-1 RESOLUTION plus ARGMAX LOCALIZATION the THR-of-THR connection needs.
Resolving max from $\text{max}-1$ to unit precision against an adversarial bulk at $d-1$
forces super-quadratic cost (B1: $P = \Omega(n^\varepsilon \log n)$ moments; B3:
$2^{\Omega(n^{2\varepsilon})}$ regularity blocks) or the $n^2$ baseline (B2, B4 collapse to
the enumeration scan on dense data). The unit of extreme-value resolution is exactly what a
fast bulk aggregation throws away.

### Two corrections applied (the honesty discipline)

(i) B2's "$\Theta(n)$ window kills it" was wrong: a cheap NON-invariant per-factor-row
Cauchy-Schwarz bound is tight ($1.00\times$-$1.24\times$ on dense data), so the window is
not binding; the operative wall is the enumeration wall, like the other three. The
"natural + algebrizing double block" on the avenue is a category error (those barriers act
on a lower-bound object, not on the algorithm). (ii) B4's "one-sparse recovery forces
$\Omega(n^2)$" was mis-derived: deterministic for-all 1-sparse recovery costs
$\lceil\log_2 N\rceil+1$ rows (demonstrated, $9$ rows for $N=256$); the exhibited collision
came from hand-zeroing the target column. The sound wall is the $\ell_\infty$-from-$\ell_2$
lightness: gap-1 resolution needs $s > \|M\|_F^2/\mathrm{gap}^2 = \Theta(n^2 d)$, a factor
$d$ worse than baseline.

### Finer-barrier verdict: still open, still barrier-free

No finer barrier was found beyond the non-binding SETH-consistency. The strongest
log-shaving-hardness theorems (Abboud-Hansen-V.Williams-R.Williams STOC 2016,
arXiv:1511.06022; Abboud-Bringmann ICALP 2018, arXiv:1804.08978) cover only
sequence/alignment problems, not OV/Max-IP; the OV-equivalence (Chen-Williams SODA 2019,
arXiv:1811.12017) and SETH bound (Chen, ToC 2020, arXiv:1802.02325) are polynomial
granularity only. Williams FOCS 2024 (ECCC TR24-142) makes the OV log-shave a WANTED route
to $\mathsf{E}^{\mathsf{NP}}$ lower bounds, the opposite of a barrier. The published
positive max-of-low-rank-via-MM methods (Valiant FOCS 2012; Karppa-Kaski-Kohonen TALG
2018, arXiv:1510.03895; Alman SOSA 2019) are GAP-DEPENDENT and collapse to $n^{2-o(1)}$ on
dense gapless data, the exact THR-of-THR-forcing regime, so they are the most important
lead AND the most important pitfall.

### The precise missing property

A winning fused-max-MM log-shave must be a subquadratic aggregation SENSITIVE TO A SINGLE
EXTREME ENTRY at unit integer resolution: distinguish two factored instances whose products
$A B^\top$ differ in exactly one cell by one unit, without materializing the $n^2$ entries,
with a worst-case (not constant-relative-gap) guarantee, and NON-LINEAR in the product
entries. No candidate and no surveyed positive technique provides all three. The open
object is now precisely framed, not merely "untouched."

## 4d. The bulk-vs-extreme wall, HARDENED to a single-round lower bound and the escape RELOCATED to adaptive / metric (finding 29)

Added 2026-06-04 (a first-principles pass: 3 surveys reading the Chen-2018 reduction
internals plus the closest-pair and sketching literature directly, four attack prongs each
with a runnable model, four adversary audits, a verifier). Subsection 4c stated the
bulk-vs-extreme wall as a HEURISTIC verified on four oblivious fusions. This subsection
attacks it from its four weak points (information vs computation, the 1-sparse loose thread,
top-of-spectrum-is-closest-pair, single-round vs adaptive). The wall BOTH hardens and
cracks. Consolidated model:
[`../../experiments/circuit_complexity/e_fused_max_mm_attack.py`](../../experiments/circuit_complexity/e_fused_max_mm_attack.py)
(exit 0; self-check OK; smoke 5/5).

### The hard instance is near-top, gap-1, planted (and a citation fix)

The Chen-2018 reduction forces Max-IP to be decided ONLY at the very top, at a single
planted ceiling $M$, with integer gap exactly $1$. The gadget (Corollary 5.5, Lemma 5.1 of
arXiv:1805.10698) is built on $P(x,y) = (x\cdot y - m)^2$ with $d_x(x)\cdot d_y(y) = P(x,y)
+ 2dm - m^2$ and ceiling $M_{d,m} = 2dm - m^2$, so $\mathrm{Max}(A,B) = M$ iff a circuit
sub-instance is satisfiable and $\le M-1$ otherwise. The decision is exact-at-the-top, not
an arbitrary interior threshold, and Chen Theorem 1.1 lists Bichromatic-Closest-Pair in the
SAME equivalence class, so the metric reframe targets the genuine hard instance. CITATION
FIX: arXiv:1805.10698 is "Toward Super-Polynomial Size Lower Bounds for Depth-Two Threshold
Circuits"; the Max-IP-hardness / SETH paper is the SEPARATE arXiv:1802.02325 (ToC v016a004,
CCC 2018). Theorem 1.5 genuinely lives in 1805.10698 (target statement correct); only the
docstring title was wrong.

### The hardened wall: a single-round Cheap-Measurement-Model lower bound

Define the CMM: fix, before seeing the input, $K$ measurements of $M = A B^\top$, each
either (a) a separable / low-rank linear functional $\langle W_k, M\rangle$, $W_k =
\sum_{l\le r} u_{k,l} v_{k,l}^\top$ (rank-$1$ pushes through as $(u^\top A)(B^\top v)$ at
$O(nd)$; subquadratic forces total rank $R = o(n^2/d)$), or (b) a degree-$\le D$
entry-symmetric statistic $\sum_{ij} g(M_{ij}) = \sum_p c_p m_p$ (cheap iff $D < 1/
\varepsilon$), or (c) a rotation-invariant spectral statistic from the $d\times d$ core at
$O(nd^2)$ (the CONTAINMENT PATCH the adversary required: $\sigma_{\max}$ and the full
spectrum are cheap, non-separable, non-entry-symmetric, so they need their own family).

| Branch | Cheap family | Why it is blind to $\mathrm{max}=d$ vs $\le d-1$ |
| --- | --- | --- |
| (i) separable-linear | rank-$\le r$ $\langle W_k, M\rangle$, total $R = o(n^2/d)$ | argmax is $\ell_2$-LIGHT, $\mathrm{argmax}^2/\|M\|_F^2 = \Theta(1/n^2)$ (measured ratio$\cdot n^2 \in [3.0,8.4]$); localization floor $\Theta(n^2)$, Price-Woodruff estimation floor $\Theta(n^2 d^2)$ |
| (ii) symmetric | degree-$D < 1/\varepsilon$ in the entry value | top-bucket indicator $[v=d] = \binom{v}{d}$ has degree exactly $d$; Vandermonde nullspace, witness $\{3,1,1,1\}$ vs $\{2,2,2,0\}$ |
| (iii) spectral | $f(\sigma_1,\dots,\sigma_d)$ from the core | equal-spectrum collision at the gap-1 top: $(2,0,0)$ shared by max $=d$ and max $=d-1$ |

THEOREM (CMM blindness): no single-round CMM of subquadratic budget resolves $\mathrm{max} =
d$ vs $\mathrm{max} \le d-1$ over rank-$\le d$ Boolean products. The model demonstrably
CONTAINS B1-B4 (moment $=$ (b); spectral/Frobenius and regularity and sketch $=$ (a) or
(c)), so this is a real upgrade from a four-method heuristic. The two floors in branch (i)
are distinct objects (the adversary's prose patch): a LOCALIZATION floor $1/\mathrm{heaviness}
= \Theta(n^2)$ and the Price-Woodruff $\ell_\infty$-from-$\ell_2$ ESTIMATION floor $\dim \ge
\|M\|_F^2/\mathrm{gap}^2 = \Theta(n^2 d^2)$ (Price-Woodruff, ICALP 2012, arXiv:1206.5725).
Separable $W$ are a subset of all linear sketches so the floor transfers a fortiori, and
turnstile $=$ linear-sketch (Li-Nguyen-Woodruff, STOC 2014) makes it a genuine streaming
SPACE lower bound. The heaviness wall SURVIVES on the actual Chen gadget after removing the
rank-$1$ offset (residual ratio$\cdot n^2 = 1.25$).

### The 1-sparse loose thread (W2), resolved honestly

Deterministic for-all $1$-sparse recovery is $O(\log N)$, but the bit-encoding sketch is NOT
excluded by non-separability (its rows ARE rank-$1$ for power-of-two $n$). It is excluded
because it is a $1$-sparse DECODE returning the row-SUM ($255$), not the max ($3$), on dense
$M$, and because you hold one instance, not a difference. The correct mechanism is
cheap-from-factored $\Rightarrow$ BULK (low-degree-symmetric / rotation-invariant), NOT
cheap $\Rightarrow$ separable: the $d\times d$ cores give cheap NON-separable functionals
such as $\|M\|_F^2 = \mathrm{tr}(A^\top A\, B^\top B)$.

### The escape locus and the most promising crack

The CMM is single-round and oblivious; the bound does NOT cover ADAPTIVE / MULTI-ROUND
measurement. Two prongs probed the escape, both negative-but-instructive. W4 ADAPTIVE
BRANCH-AND-BOUND: on the true worst case (every row popcount $d/2$) every cheap separable
certificate is additively $\Theta(d)$ loose (gaps $0.5 \to 27.9$ as $d: 8 \to 128$), the
pruned fraction is EXACTLY $0$ even with an omniscient incumbent, and $T(n) = 4T(n/2) +
\text{cheap} = \Theta(n^2)$, zero shave; the only additive-$1$ certificate is the exact
block max (circular). This LOCATES the wall as worst-case GAPLESSNESS, not the single-round
restriction. W3 CLOSEST-PAIR (the most promising crack): the exact reframe $\mathrm{Ham} =
|a| + |b| - 2\langle a,b\rangle$ makes thresholded Max-IP literally bichromatic Hamming
near-neighbor, falsifying the slogan, and targeting the genuine near-top gap-$1$ instance.
But the closest-pair engine (Alman-Williams FOCS 2015, arXiv:1507.05106; Alman-Chan-Williams
FOCS 2016, arXiv:1608.04355) is the SAME probabilistic-polynomial-$+$-MM engine as the OV
shave: saved time $n^{2 - 1/O(\sqrt c\,\mathrm{polylog}\,c)}$ at $d = c\log n$ decays to
$1+o(1)$ at $d = n^\varepsilon$, STRICTLY worse than OV's constant $2^{1/\varepsilon}$. Every
technique reaching $d = n^\varepsilon$ (LSH, May-Ozerov, Alman-Chan offline ANN SODA 2020)
is $(1+\varepsilon)$-APPROXIMATE and cannot resolve gap-$1$; exactness is SETH-hard at $d =
2^{O(\log^\star n)}$ (Chen ToC 2020, arXiv:1802.02325; Williams SODA 2018). Chen's hardness
is itself a Set-Disjointness communication theorem ($\Omega(n)$ randomized,
Kalyanasundaram-Schnitger 1992, Razborov 1992), and adaptive turnstile $=$ a sequence of
linear sketches (Ai-Hu-Li-Woodruff CCC 2016), so single-round bounds compose only up to a
$\#$rounds factor: the prize-relevant escape must be adaptive.

### The precise missing property, sharpened

An ADAPTIVE / multi-round, NON-LINEAR, EXACT-gap-$1$, worst-case-GAPLESS extreme-extractor
on the low-rank factored form, ideally exploiting the bichromatic-near-neighbor metric
structure. Single-round is provably insufficient; the binding obstruction is worst-case
gaplessness, not bulkness; the metric reframe is on-target but every published engine
decays or is approximate at $d = n^\varepsilon$. No such object exists yet.

## 4e. The wall EXTENDS to adaptive multi-round and the metric route is conditionally impossible; the last opening is co-nondeterministic certification (finding 30)

> CORRECTION (finding 32, subsection 4f): the co-nondeterministic block below is REAL but MIS-ATTRIBUTED. The Set-Disjointness SDPT does not apply (Chen's NEXP-direction reduction is single-instance, Lemma 4.3), and the nonneg-rank $= \Omega(n)$ derivation was a wrong-set error (the correct tight-free cover of $\mathrm{supp}(N)$ is $O(\log m)$). The correct obstruction is the triple-lock (UPIT/NSETH, algebrization, prAM-circularity); see 4f.

Added 2026-06-04 (a first-principles pass on the finding-29 escape loci: 3 surveys reading the multi-pass streaming, doubling-metric, and NSETH / Merlin-Arthur literature directly, three attack prongs each with a runnable model, three adversary audits, a verifier). Subsection 4d hardened the wall to a SINGLE-ROUND lower bound and relocated the escape to adaptive / multi-round / metric / co-nondeterministic. This subsection attacks all four loci. The deterministic+adaptive wall CLOSES against bulk + metric; co-nondeterminism remains the genuine frontier. Consolidated model: [`../../experiments/circuit_complexity/e_fused_max_mm_escape.py`](../../experiments/circuit_complexity/e_fused_max_mm_escape.py) (exit 0; self-check OK; smoke 5/5).

### The adaptive extension (P1): the wall closes for bulk decision trees

An adaptive bulk decision tree picks query $Q_t$ as a function of prior answers, each $Q_t$ cheap-from-factored from the finding-29 families (a)/(b)/(c) on an arbitrary sub-block; the single-round CMM theorem is the $K=1$ case. THEOREM (communication form): on Chen's gap-1 family, deciding $\max=d$ vs $\le d-1$ is Set-Disjointness on the planted pair's private coordinates ($\Omega(n)$, Kalyanasundaram-Schnitger 1992; Razborov, TCS 1992; gap-1 $=$ UDISJ). Each cheap bulk round communicates $O(d\log n) = O(n^\varepsilon \log n)$ bits (a block-SUM factors as $\langle\sum_R a, \sum_C b\rangle$, so Alice ships a $d$-vector; this CORRECTS 4d's implicit "polylog per round"), forcing $K = \Omega(n^{1-\varepsilon}/\log n)$ rounds, super-polylog.

| Query scale | Blindness mechanism | Witness |
| --- | --- | --- |
| FULL block | invariance: $0$ location bits | $m_p$ delta value-only ($m_1{=}1, m_2{=}23, m_3{=}397$ at $v{=}11$); spectrum permutation-invariant (spike@$(0,0) =$ spike@$(1,1) = (2,0,0)$) |
| SUB block | SNR-floor (invariance FAILS, breaker $n{=}4,d{=}4$) | signal $\sqrt{d\log n}\,d \ll$ bulk noise $n d^2$; SNR $5.0\mathrm{e}{-}3, 1.3\mathrm{e}{-}3, 3.2\mathrm{e}{-}4$ ($n{=}64,128,256$) |

Total advantage $\sim K \cdot \mathrm{heaviness}$, heaviness $\sim C/b^2$ $d$-independent (max/min $1.00$-$1.02$); $\mathrm{adv}(K{=}n) \to 0$ ($2.2\mathrm{e}{-}1 \to 3.0\mathrm{e}{-}2$), $\mathrm{adv}(K{=}n^2/4) = \Theta(1)$ ($\sim 3.8$); any $K=o(n^2)$ gives $o(1)$. The task's "spike dominated for $b\ge2$" premise is REJECTED (right direction, wrong reason): an exact bulk query reads the $+1$ exactly (abs tell $= 2d-1$), heaviness at $b{=}1$ is $\Theta(1)$; the mechanisms are invariance plus SNR-floor plus communication. Streaming corroboration: BGLWWZ (arXiv:2403.20283, Thm 1.6) gives $\Omega(\varepsilon^{-2}\log n / k)$ bits, so at $\varepsilon^2 \sim 1/n^2$ the floor is $\sim n^2/k$; the optimal multi-pass turnstile algorithm is a sequence of linear sketches (Ai-Hu-Li-Woodruff, CCC 2016). PROVES-TOO-MUCH PASSES: a row-aggregate query LOCATES the heavy row on the GAPPED Valiant instance ($z = 25.8, 39.0, 56.4$) but is BLIND on the gapless Chen family ($z = -1.26, 0.03, 0.53$). TWO SEAMS: (1) the exact-entry $b{=}1$ read is outside the bulk lemmas, closed by a separate one-cell-among-$n^2$ argument; (2) published streaming theorems force a LINEAR per-round sketch, so families (b)/(c) used adaptively are covered only by strong simulation evidence (a greedy spectral-flavored descent does not localize, per-split bias $+0.040$ at $n{=}64 \to -0.010$ at $n{=}256$), not yet by an MIC-style theorem (BGLWWZ Lemma 1.1, $\mathrm{MIC} \le 2ksn$). The adaptive extension is thus "extended with strong simulation support", a theorem for bulk + linear.

### The metric escape (P2): conditionally impossible

$2\langle a,b\rangle = |a|+|b| - \mathrm{Ham}$ (verified $300/300$) makes the gap-1 decision bichromatic Hamming near-neighbor at fixed radius, but triangle-inequality structures (cover trees, Beygelzimer-Kakade-Langford ICML 2006; navigating nets, Krauthgamer-Lee SODA 2004) are $2^{\Theta(\mathrm{ddim})}$ and $\mathrm{ddim}$ of $n$ Boolean vectors at $d=n^\varepsilon$ on the gapless instance is $\Theta(d) = \Theta(n^\varepsilon)$ (branching $B = 4/14/28/59$ at $d=4/8/16/24$). Exact query $= 2^{\Theta(n^\varepsilon)}\log n$ per call, worse than $n^2$; dimension reduction is $(1+\varepsilon)$-approximate and destroys gap-1 (JL flip $0.05$-$0.42$, $\to 0$ at sketch dim $\sim d^2$). Same wall on the hardness side: exact Max-IP at $d=\omega(\log n)$ is SETH/OV-hard ($n^{2-o(1)}$; Williams 2005; Chen, arXiv:1802.02325), so a subquadratic exact metric algorithm refutes OV/SETH. PROVES-TOO-MUCH (LOCAL cover near the planted pair): gapped $=1$ (prunes, Valiant survives), gapless $= 60$-$161 \sim m/2$. HITS all three barriers. CLOSED as a route.

### The co-nondeterministic escape (P3): wall-survives, $n^2$ relocates to certificate size

The cheap dismissal ("read all $n^2$ entries") is FALSE: factored rank-$q$ equality is subquadratic via the Gram-trace zero-test $\mathrm{tr}((P^\top P)(Q^\top Q))$ at $O(nd^2)$ (returns $0.0$ equal, $56.0$ on one perturbation). So a poly($d$)-size nonnegative factorization of $N = \tau J - AB^\top$ would FIRE the connection. The escape closes at the nonnegative rank $r_+(N) \ge$ rectangle-cover of the tight set $=$ co-nd communication cover of the planted Set-Disjointness $= \Omega(n)$ (measured cover$/n = 0.250$ constant, $n=32..256$); certificate $U,V$ are $\Omega(n^2)$. The $n^2$ hides in CERTIFICATE SIZE, same Set-Disjointness root as the deterministic block. OPENINGS (outside co-nd model): NSETH does NOT bind at $d=n^\varepsilon$ (Carmosino et al., ITCS 2016, forbids only $(2-\varepsilon)^n$; Chen needs $2^n/n^k$); a $\Theta(\sqrt n \log n)$ MA certificate exists (Williams, CCC 2016, arXiv:1601.04743; Rubinstein STOC 2018) but is randomized-verifier (Chen Remarks 2.7/4.2 admit co-nd not MA). The open task is derandomizing the MA certificate, blocked by the DISJ strong direct product theorem (Klauck-Spalek-de Wolf; Sherstov). EVADES all three barriers via non-largeness.

### The precise missing property, re-sharpened

A CO-NONDETERMINISTIC certificate that all $n^2$ entries are $\le \tau$, verifiable in $n^2/\log^{\omega(1)} n$ on worst-case gapless data: equivalently a poly($d$)-size nonnegative factorization of $N = \tau J - AB^\top$, or a NON-ALGEBRIZING derandomization of the $\Theta(\sqrt n \log n)$ MA batch-OV certificate that removes Arthur's coins without re-incurring the $\Omega(n)$ rectangle-cover. The deterministic adaptive-search side is now provably blind for bulk methods, so the missing object is a certificate for the UNSAT direction, not a search. No such object exists yet.

## 4f. The non-linear adaptive seam CLOSES for full blocks (a theorem), the co-nondeterministic frontier is PINNED-BLOCKED by a corrected triple-lock, and the CRT crack dissolves (findings 31-32)

Added 2026-06-04 (an endgame pass on the two honest seams finding 30 left: 2 surveys reading the MA-derandomization / NSETH / SDPT literature and the multi-pass information-complexity / sufficient-statistic literature directly, one co-nd attack prong with a runnable model, one adversary audit, a verifier). Subsection 4e closed the deterministic+adaptive wall against bulk methods and named the co-nondeterministic certificate as the residual frontier, leaving two seams: (Thrust B) the non-linear families (b)/(c) used adaptively were a theorem only "with strong simulation support", and (Thrust A) the co-nd derandomization was flagged with two angles to chase (the CRT-correlation crack and the DISJ SDPT). This subsection discharges both. Consolidated model: [`../../experiments/circuit_complexity/e_fused_max_mm_endgame.py`](../../experiments/circuit_complexity/e_fused_max_mm_endgame.py) (exit 0; self-check OK; smoke 5/5).

THRUST B (the seam, PARTIALLY CLOSED). The full-block non-linear case is now a THEOREM via the sufficient-statistic / data-processing collapse. The set of all degree-$<1/\varepsilon$ symmetric queries is a deterministic function of the fixed moment vector $m=(m_1,\dots,m_D)$; every rotation-invariant spectral query is a deterministic function of the fixed $d$-spectrum $\sigma$. Both are instance-determined and query-INDEPENDENT, hence sufficient statistics, so by Cover-Thomas (Thm 2.8.1 + Sec 2.9) any adaptive tree over functions of $m$ (resp. $\sigma$) carries no more information about the spike location than one read of the statistic, which finding 30's location-invariance makes zero. Verified: moment vector and singular spectrum identical across spike at $(0,0)$, $(b{-}1,b{-}1)$, off-diagonal $(1,2)$ at $(b,d,D)=(6,12,4),(8,16,4),(12,24,5)$; adaptive 3-round transcript identical across location. The SUB-block case is honestly DOWNGRADED from closure to a NAMED OPEN LEMMA: an adaptive tree chooses which sub-block to read, so the accumulated statistic is itself adaptive and not a single fixed sufficient statistic; the per-query advantage is SNR-floored ($\mathrm{SNR}\sim 1/b$, $1.31/0.175/0.069/0.0295/0.010$ at $b=2/4/8/16/32$) but the union over $K=o(n^2)$ assumes an additivity the tree can violate, and BGLWWZ MIC (arXiv:2403.20283, Lemma 1.1) is not instantiated (no fixed stream order, no UDISJ-to-needle lift). The two published frameworks that would close it (Simchowitz-El Alaoui-Recht, STOC 2018, arXiv:1804.01221; Kacham-Woodruff, NeurIPS 2023, arXiv:2311.17281) prove the orthogonalize+truncated-likelihood per-round iteration for LINEAR measurements only (family (a)), so neither black-boxes the non-linear case. PROVES-TOO-MUCH PASSES: spectrum detects a constant relative gap (ratio $2212/8376/19259$ at $d=64/128/192$, $>100\times$), blind only at gap $1$, Valiant/light-bulb survives.

THRUST A (the frontier, PINNED-BLOCKED). No subquadratic co-nd certificate survives, and the block is correctly re-attributed to a TRIPLE-LOCK, not the SDPT. Arthur's randomness is a single random low-degree univariate evaluation point (Schwartz-Zippel; Williams, CCC 2016, arXiv:1601.04743, Thm 3.1). (a) UPIT/NSETH inside the protocol: naive derandomization recovers the full $2^n$ nondeterministic algorithm, and a sub-$n^2$ nondeterministic UPIT is already the $\mathsf{E}^{\mathsf{NP}}$ breakthrough (Cor 3.1), so the derandomization is the prize in disguise. (b) Algebrization on the engine: arithmetization + sum-check is THE algebrizing technique (Aaronson-Wigderson 2008; repo probe classifies ALGEBRIZES), the target is non-algebrizing, so an arithmetization-internal derandomization conflicts on the algebrization axis. (c) Circularity: $\mathrm{prAM}\subseteq\mathsf{NP}$ implies $\mathsf{E}^{\mathsf{NP}}$ requires $2^{\Omega(n)}$-size circuits (Miltersen-Vinodchandran, CCC 1999; Impagliazzo-Kabanets-Wigderson 2002), the very lower bound sought. The SDPT (Klauck, STOC 2010, arXiv:0908.2940) was MISAPPLIED: it needs independent instances and lives on the SETH side, but Chen's NEXP-direction reduction is SINGLE-instance (Lemma 4.3, one circuit to one Max-IP instance, arXiv:1805.10698), so there is no batch for it to bound. The CRT crack DISSOLVES: the only randomness in that direction is a single random prime (Lemma 3.2), already nondeterministically derandomized (Remark 3.3, one-sided error). NONNEG-RANK CORRECTION (also corrects 4e): the tight-free cover of $\mathrm{supp}(N)$ (the off-diagonal COMPLEMENT of a permutation tight set) is $2\lceil\log_2 m\rceil = O(\log m)$ (verified $4/6/8/12/16/20$ at $m=4/8/16/64/256/1024$), NOT $\Omega(m)$; the old diagonal-cover was the wrong set. The legitimate $\Omega(n)$ is co-nd communication of UDISJ on the SINGLE planted pair (one decision), and the $\Omega(n^2)$ certificate size is NAMED-AS-NOT-DERIVED (one planted pair, not $n$). Surviving non-circular opening: a deterministic small-prime hitting set for Chen's Lemma 3.2 (measured 33 primes for 32 bits, possibly non-algebrizing).

NET. The bulk / cheap-measurement model is walled on every deterministic axis (single-round CMM, adaptive full-block by theorem, linear by theorem, metric conditionally impossible) plus the co-nd prong (pinned-blocked by the triple-lock), with exactly one residual object: the sub-block non-linear per-round information lemma. Findings 31-32. No speedup claimed; $\mathsf{NEXP}\not\subseteq$ poly-size THR-of-THR remains open as of June 2026.

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
- **Natural proofs: CONDITIONALLY evaded via non-largeness at the NEXP-level bound
  (corrected 2026-06-03, finding 25; an earlier phrasing said "arguably the binding
  constraint", which inverted the direction).** Razborov-Rudich needs a property that
  is LARGE AND constructive. If dense poly-size $\mathsf{TC}^0$ supports strong PRFs
  (ACW 2016 "seems likely", arXiv:1608.04355 Section 1 after Thm 1.9; Naor-Reingold
  PRFs in $\mathsf{TC}^0$, JACM 2004; Miles-Viola candidate, JACM 2015; Chen-Tell 2019),
  then no LARGE-and-constructive (combinatorial / correlation / approximate-degree)
  property separates against it. That binds the natural ALTERNATIVES, and it is exactly
  WHY a non-natural method is required, not an obstruction to the leading path (ACW /
  Chen-Tell say precisely this: TC0 bounds "may require non-natural proofs"). The
  Williams spine is non-natural by dropping LARGENESS, NOT constructivity (Williams
  2013, STOC 2013 / SICOMP 2016: constructivity is unavoidable, the useful property is
  non-large, "distinguishes SOME function"). A genuinely non-large Williams-style proof
  carries no distinguishing bias, so the PRF collision is SILENT on it. The residual
  subtlety (why not cleanly evaded): at the $\mathsf{NEXP}$-to-$\mathsf{NP}$ DESCENT the
  bespoke non-large property is gone, and the candidate replacement is the
  meta-complexity high-Kt device, which is LARGE (Shannon counting), so it must escape
  by NON-CONSTRUCTIVITY (deciding high-Kt is MCSP/MKTP-hard). That non-constructivity
  against $\mathsf{TC}^0$ for the exact descent truth tables is OPEN (restricted MCSP
  variants are NP-hard non-relativizingly, Hirahara 2022; the exact object is not). So
  natural proofs is evaded at the base and open at the descent, where the escape lever
  flips from largeness to constructivity. Modeled in
  [`../../experiments/natural_proofs/e_tc0_prf_collision.py`](../../experiments/natural_proofs/e_tc0_prf_collision.py).
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
