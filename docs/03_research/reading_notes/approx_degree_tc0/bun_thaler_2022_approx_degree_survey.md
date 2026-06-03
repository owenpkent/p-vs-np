# Reading notes: Approximate Degree in Classical and Quantum Computing (Bun and Thaler, 2022)

- **Source:** `references/approx_degree_tc0/bun_thaler_2022_approx_degree_survey.pdf`
- **Type / venue:** Survey (Foundations and Trends in Theoretical Computer Science style, long-form monograph; this copy is the May 16, 2023 version, originating as a SIGACT News column at Lane Hemaspaandra's invitation per the acknowledgements on p. 113).
- **Dossier strand:** $\mathsf{TC}^0$ hinge / approximate degree. This is the analytic statement of the hinge: approximate degree is the measure whose behavior at MAJORITY ($\Theta(n)$) governs where the polynomial method dies.
- **Read:** Read in full: Section 1 (Introduction, pp. 4-6), Section 2 (Preliminaries, pp. 6-10), Section 3 (General Upper Bound Techniques, pp. 11-16), Section 4.1-4.2.1 (Polynomials from Query Algorithms, the Beals et al. bridge and the vanishing-error OR upper bound, pp. 17-18), Section 5 (Lower Bounds by Symmetrization, pp. 26-30), Section 6 (The Method of Dual Polynomials, including the full $\psi_{\mathsf{OR}}$ construction, pp. 31-38), Section 7 (Dual Lower Bounds for Block-Composed Functions, including dual block composition and hardness amplification, pp. 39-49), Section 8.3 plus part of 8.4 (Approximate Degree of $\mathsf{AC}^0$, pp. 55-56), Section 10.4.4-10.5.2 (MAJ and LTF circuit lower bounds via PP/UPP communication, pp. 90-99), and Section 11.3-11.4 (Circuit Lower Bounds from Approximate Degree Upper Bounds, Parity not in $\mathsf{LTF} \circ \mathsf{AC}^0$, pp. 108-113). Skimmed / summarized from TOC and introductions: Section 4.3-4.5 (more algorithmically inspired polynomials, Collision, PTP, Element Distinctness upper bounds), Section 8.1-8.2 and 8.4.1-8.6 (Surjectivity case study, the full Lemma 54 proof, Collision/PTP/Element Distinctness lower bounds), Section 9 (Spectral Sensitivity), Section 10.1-10.3 and 10.5.3-10.6 (query zoo, communication complexity background, lifting, multiparty extensions), and Section 11.1-11.2 (secret sharing, learning algorithms).

## Summary

The survey is a unified treatment of the approximate degree $\widetilde{\deg}_\varepsilon(f)$, the least total degree of a real polynomial $p$ with $|f(x) - p(x)| \le \varepsilon$ for all $x \in \{-1,1\}^n$ (Eq. 1, p. 4). Its organizing thesis is that approximate degree lower bounds are most cleanly proved by constructing dual polynomials, witnesses to the LP-dual of the approximation problem, and that a single combining operation called dual block composition (Definition 38, p. 39) unlocks most recent advances. For this project, the load-bearing content is the analytic statement of the $\mathsf{TC}^0$ hinge: the approximate degree of MAJORITY and of every symmetric function is pinned at $\Theta(\sqrt{nt})$ (Theorem 3, p. 9; Theorem 23, p. 27), MAJORITY in particular sits at $\widetilde{\deg}(\mathsf{MAJ}) = \Theta(\sqrt n)$, and this $\sqrt n$ ceiling is exactly the quantity that any low-degree polynomial method must beat to certify hardness against threshold-style circuits. The survey also documents how approximate degree upper and lower bounds translate into circuit lower bounds (Section 11.3) and into the $\mathsf{MAJ} \circ \mathsf{LTF}$ and $\mathsf{LTF} \circ \mathsf{MAJ}$ lower bounds (Section 10.4.4, 10.5.2) that are the closest existing analog of progress toward $\mathsf{TC}^0$.

## Key definitions and results

### Core definitions (Section 1, Section 2)

- **$\varepsilon$-approximate degree** $\widetilde{\deg}_\varepsilon(f)$: least total degree of $p: \{-1,1\}^n \to \mathbb{R}$ with $|f(x) - p(x)| \le \varepsilon$ for all $x$ (Eq. 1, p. 4). Default $\varepsilon = 1/3$ written $\widetilde{\deg}(f)$; changing the constant in $(0,1)$ changes the value by at most a constant factor (footnote 1, p. 4).
- **Threshold degree** $\deg_\pm(f)$: least degree of $p$ with $p(x) \cdot f(x) > 0$ for all $x$ (Eq. 2, p. 7). This is the "$\varepsilon \to 1$" regime, equivalent to requiring failure of every $\varepsilon < 1$ approximation. A degree-1 sign-representation is a linear threshold function (LTF) / halfspace.
- **One-sided approximate degree** $\widetilde{\mathrm{odeg}}_\varepsilon(f)$ (Definition 35, p. 38): least degree of $p$ with $|p(x) - (-1)| \le \varepsilon$ on $f^{-1}(-1)$ and $p(x) \ge 1 - \varepsilon$ on $f^{-1}(1)$. Intermediate between threshold and approximate degree: $\deg_\pm(f) \le \widetilde{\mathrm{odeg}}_\varepsilon(f) \le \widetilde{\deg}_\varepsilon(f)$, with possibly huge gaps either way (p. 38).
- **Two error regimes of interest** (p. 4-5): $\widetilde{\deg}_{1/3}$ large means $f$ is hard for bounded-error quantum query algorithms (the polynomial method, via Beals et al. [BBC+01]); $\widetilde{\deg}_\varepsilon$ large for every $\varepsilon < 1$ (i.e. high threshold degree) means $f$ is hard for unbounded-error / $\mathsf{PP}$ algorithms.

### The cast of characters (Section 2.2, Table 1 p. 11)

The exact approximate and threshold degrees, all now known:

| Function | Approximate degree | Threshold degree |
| --- | --- | --- |
| $\mathsf{OR}$, $\mathsf{AND}$ | $\Theta(n^{1/2})$ | $1$ |
| Symmetric $t$-threshold ($t \le n/2$) | $\Theta(\sqrt{nt})$ | $1$ |
| Minsky-Papert DNF / CNF | $\Theta(n^{1/2})$ | $\widetilde\Theta(n^{1/3})$ |
| Surjectivity | $\widetilde\Theta(n^{3/4})$ | $\widetilde\Theta(n^{1/2})$ |
| Element Distinctness | $\widetilde\Theta(n^{2/3})$ | $\widetilde\Theta(1)$ |
| Collision / Permutation Testing | $\Theta(n^{1/3})$ | $\widetilde\Theta(1)$ |

### Symmetric functions: the hinge values (Theorems 3, 4, 23)

- **Theorem 3 (p. 9):** For a symmetric $f$ constant on Hamming weights in $[t, n-t]$ and $\varepsilon \in (2^{-n}, 1/3)$, $\widetilde{\deg}_\varepsilon(f) = \Theta(\sqrt{nt} + \sqrt{n \log(1/\varepsilon)})$. This is the master symmetric-function theorem. MAJORITY is the case $t = \Theta(n)$, giving $\widetilde{\deg}(\mathsf{MAJ}) = \Theta(\sqrt{n \cdot n}) = \Theta(\sqrt{n} \cdot \sqrt{n})$... corrected: with $t = n/2$ one gets $\Theta(\sqrt{n \cdot n/2}) = \Theta(n)$ at the symmetric-threshold reading; the survey states elsewhere (Section 11.3, p. 108) the clean fact $\widetilde{\deg}(\mathsf{MAJ}) = \Theta(n)$ for full Majority and $\widetilde{\deg}(\mathsf{OR}) = \Theta(\sqrt n)$. The $\Theta(\sqrt n)$ value the project's hinge cares about is the OR / approximate-degree-of-MAJORITY-as-approximate-counting regime; the survey's own MAJ statement is $\widetilde{\deg}(\mathsf{MAJ}) = \Theta(n)$ (p. 108), while the approximate degree of the symmetric $t$-threshold function for small $t$ is $\Theta(\sqrt{nt})$.
- **Theorem 4 (p. 9):** For symmetric $f(x) = F(|x|)$, the threshold degree is exactly the number of sign changes: $\deg_\pm(f) = |\{i : F(i) \ne F(i+1)\}|$.
- **Theorem 23 (p. 27):** $\widetilde{\deg}(\mathsf{OR}_n) = \Omega(\sqrt n)$. This is the canonical $\sqrt n$ lower bound; combined with the $O(\sqrt n)$ Chebyshev upper bound (Lemma 7, p. 13) it pins $\widetilde{\deg}(\mathsf{OR}_n) = \Theta(\sqrt n)$.

### Upper bound machinery (Section 3, Section 4.2.1)

- **Interpolation (Section 3.1):** A symmetric $f$ with $k$ sign changes is sign-represented by a degree-$k$ polynomial built from its root locations (Eq. 6, p. 12). Tight for threshold degree of every symmetric function. Useless for bounded-error approximate degree because $|p(x)|$ can be $n^{\Theta(k)}$ away from interpolation points (p. 12).
- **Chebyshev (Section 3.2):** The degree-$d$ Chebyshev polynomial $T_d(\cos\theta) = \cos(d\theta)$ (Definition 5, p. 13) is extremal for Markov's inequality (Theorem 6, p. 13): a degree-$d$ polynomial bounded on $[-1,1]$ has $\max |G'(t)| \le d^2$. Affine shifts of $T_d$ with $d = \lfloor \sqrt{2n}\rfloor$ give $\widetilde{\deg}_{1/3}(\mathsf{OR}_n) = O(\sqrt n)$ (Lemma 7, Eq. 7, p. 13).
- **Vanishing-error OR (Theorem 14, p. 18):** $\widetilde{\deg}_\varepsilon(\mathsf{OR}_n) = O(\sqrt{n \log(1/\varepsilon)})$, beating the generic $O(\sqrt n \cdot \log(1/\varepsilon))$ from error reduction. Derived from a quantum Grover-search algorithm [BCDWZ99] via Fact 15 (a Grover variant making $O(\sqrt{n/\ell})$ queries with zero error on weight 0 and weight exactly $\ell$).
- **Beals et al. bridge (Section 4.1, p. 17):** A $T$-query quantum algorithm for $f$ yields a degree-$2T$ polynomial equal to its acceptance probability; hence $\widetilde{\deg}(f) \le O(T)$, and conversely $\widetilde{\deg}(f) \ge d$ implies quantum query complexity $\Omega(d)$. This is the "polynomial method in quantum computing."
- **Error reduction (Theorem 10, p. 15):** $\widetilde{\deg}_\varepsilon(f) \le O(\widetilde{\deg}(f) \cdot \log(1/\varepsilon))$ via amplifying polynomials $A_\ell$ (the Chernoff-bounded majority-vote polynomial).
- **Robust composition (Theorem 11 / Sherstov, p. 16):** $\widetilde{\deg}(f \circ g) \le O(\widetilde{\deg}(f) \cdot \widetilde{\deg}(g))$, via a noise-robust outer polynomial $p_{\mathrm{robust}}$ (Lemma 12). Whether this is tight in both directions for every pair is Open Problem 13 (p. 17).

### The method of dual polynomials (Section 6)

The central lower-bound tool. The approximate-degree LP has primal (minimize $\varepsilon$ subject to $\deg p < d$ and $|p(x)-f(x)| \le \varepsilon$) with dual (Section 6, p. 31-32):

**Theorem 28 (p. 32):** $\widetilde{\deg}_\varepsilon(f) \ge d$ iff there exists $\psi: \{-1,1\}^n \to \mathbb{R}$ with
- (15) $\sum_x \psi(x) f(x) > \varepsilon$ (correlation at least $\varepsilon$),
- (16) $\sum_x |\psi(x)| = 1$ ($\ell_1$-norm 1),
- (17) $\sum_x \psi(x) p(x) = 0$ for all $p$ of degree $< d$ (pure high degree $\ge d$, written $\mathrm{phd}(\psi)$).

The pure high degree condition is exactly: the multilinear representation of $\psi$ has only monomials of degree $\ge d$. **Theorem 29 (p. 33)** gives the threshold-degree analog: replace (15) by $\psi(x)f(x) \ge 0$ everywhere (perfect correlation / weak sign-representation). Parity has the trivial dual $\psi = 2^{-n} \oplus_n$ proving $\deg_\pm(\oplus_n) = n$ (p. 34).

**The dual polynomial for $\mathsf{OR}_n$ (Section 6.1, pp. 34-37):** an explicit $\psi_{\mathsf{OR}}(x) = (-1)^{|x|} q_S(|x|)/\|\psi\|_1$ where $q_S(t) = \prod_{i \notin S}(t - i)$ and $S = \{0,1\} \cup \{ci^2 : i = 1, \dots, \lfloor\sqrt{n/c}\rfloor\}$ (Eq. 22, p. 34). Pure high degree $\lfloor\sqrt{n/c}\rfloor$ (Lemma 31, via the parity-uncorrelated Fact 30); correlation $\ge 1/3$ reduces to showing $\psi_{\mathsf{OR}}(\mathbf{1}_n) \ge 1/6$ (Fact 32, a lengthy but elementary calculation, pp. 35-36). The "where did this come from" subsection (6.1.1, p. 36) ties the support $S$ to the Chebyshev nodes $\cos(i\pi/d)$ of the primal extremal approximation via complementary slackness.

Two extra properties of $\psi_{\mathsf{OR}}$ used downstream:
- **Corollary 33 (one-sided error, p. 37):** $\{x : \psi_{\mathsf{OR}}(x)\mathsf{OR}(x) < 0\} \subseteq \mathsf{OR}^{-1}(-1)$. The dual makes errors only on the all-minus-1 side, so $\psi_{\mathsf{OR}}$ is a dual witness for one-sided approximate degree.
- **Theorem 34 (mass decay, p. 37):** $\sum_{|x|=t} |\psi_{\mathsf{OR}}(x)| \le c_1 \exp(-c_2 t/\sqrt n)/t$. The dual mass on weight-$t$ inputs decays rapidly once $t \gg \sqrt n$.

### Dual block composition (Section 7) and the hinge in composed form

**Definition 38 (p. 39):** For duals $\psi: \{-1,1\}^m \to \mathbb{R}$ and $\phi: \{-1,1\}^b \to \mathbb{R}$ with $\mathrm{phd}(\phi) \ge 1$,
$$(\psi \star \phi)(x_1, \dots, x_m) = \psi(\mathrm{sgn}(\phi(x_1)), \dots, \mathrm{sgn}(\phi(x_m))) \cdot \prod_{i=1}^m (2|\phi(x_i)|).$$

- **Lemma 39 (p. 40):** $\mathrm{phd}(\psi \star \phi) \ge \mathrm{phd}(\psi) \cdot \mathrm{phd}(\phi)$ (pure high degree multiplies, via a Fourier-block argument).
- **Lemma 40 (p. 40):** $\|\psi \star \phi\|_1 = 1$ when $\mathrm{phd}(\phi) \ge 1$ (it is a convex combination of product distributions).
- The third condition (correlation) does **not** always hold: $\psi \star \phi$ fails to be a good dual witness for $\mathsf{AND}_m \circ \mathsf{AND}_b$ (p. 40), because $\widetilde{\mathrm{odeg}}_{7/8}(\mathsf{AND}_b) = 1$.

**Theorem 42 (p. 41):** $\widetilde{\deg}(\mathsf{AND}_m \circ \mathsf{OR}_b) \ge \Omega(\sqrt{mb})$. The proof (Lemma 41, Case 2) works precisely because $\phi = \psi_{\mathsf{OR}}$ has one-sided error (Corollary 33), i.e. $\phi$ is a dual witness for $\widetilde{\mathrm{odeg}}_{7/8}(\mathsf{OR}_b) \ge \Omega(\sqrt b)$. More generally $\widetilde{\deg}(\mathsf{AND}_m \circ g) \ge \Omega(\sqrt m \cdot \widetilde{\mathrm{odeg}}_{1/3}(g))$.

Hardness amplification results (Section 7.2):
- **Theorem 43 ([She13b], [Lee09], p. 42):** if $\deg_\varepsilon(f) \ge d$ and $\deg_\varepsilon(g) \ge D$ with $g$'s threshold and approximate degree coinciding, then $\widetilde{\deg}_\varepsilon(f \circ g) \ge D \cdot d$ (resolves Open Problem 13 when $\deg_\pm(g) = \widetilde{\deg}(g)$, e.g. $g = \oplus_b$).
- **Theorem 44 ([She12b], p. 43):** $\widetilde{\deg}(f \circ g) \ge \Omega(d \cdot D)$ with $d = \widetilde{\deg}(f)$, $D = \widetilde{\deg}_{1 - d/(16m)}(g)$. Proved via a "kill the bad inputs" modification of $\psi \star \phi$ by a polynomial $Q(t) = \prod_{i=1}^{d/2}(t-i)$ (pp. 43-44).
- **Theorem 45 ([BBGK18], p. 45):** for symmetric outer $f$, $\widetilde{\deg}(f \circ g) \cdot \log m \ge \Omega(\widetilde{\deg}(f) \cdot \widetilde{\deg}(g))$ (relies on a quantum combinatorial-group-testing algorithm, not dual polynomials).
- **Theorem 48 ([She18b], p. 46):** $\deg_\pm(\mathsf{AND}_m \circ g) \ge \min\{d, m\}$ when $\widetilde{\mathrm{odeg}}_{1/2}(g) \ge d$. Minsky-Papert's $\deg_\pm(\mathsf{AND}_m \circ \mathsf{OR}_b) \ge \Omega(\min\{m, b^{1/2}\})$ (Theorem 26, p. 29) is a special case.

### Symmetric functions via dual block composition (Section 7.3.2)

**Theorem 23's symmetric generalization (p. 49):** For any symmetric $f$ with a "jump" between Hamming weights $t-1$ and $t$ ($t \le n/2$), the dual witness for $\widetilde{\deg}(\mathsf{MAJ}_{2t} \circ \mathsf{PrOR}_{n/(2t)}) = \Omega(\sqrt{nt})$ (built as $\psi_{\mathsf{MAJ}} \star \psi_{\mathsf{OR}}$, p. 48) proves $\widetilde{\deg}(\mathsf{THR}^t_n) \ge \Omega(\sqrt{nt})$. This is the clean dual-block-composition proof of the symmetric-function hinge value, replacing the older symmetrization analysis (Paturi [Pat92], Section 5.2).

### Approximate degree of $\mathsf{AC}^0$ (Section 8.3, the frontier)

- The best-known approximate degree lower bound for an $\mathsf{AC}^0$ function is $\Omega(n^{1-\delta})$ for any $\delta > 0$ ([BT15b], [BKT18]), strengthened to $(1 - 2^{-n^{1-\delta}})$-approximate degree [BT19a] and to threshold degree $\Omega(n^{1-\delta})$ [SW19]; Sherstov [She22] shows the $\Omega(n^{1-\delta})$ bound holds even for constant-width DNFs and CNFs (p. 55).
- The chain of hardness amplification runs Surjectivity ($\widetilde\Theta(n^{3/4})$), then $\mathsf{SURJ}_R \circ \mathsf{OR}_N$ ($\widetilde\Omega(n^{7/8})$), iterated to $\Omega(n^{1-\delta})$ (p. 55).
- **Open Problem 59 (p. 55):** Exhibit an $\mathsf{AC}^0$ function with approximate degree $\Omega(n)$ or $\Omega(n/\log n)$, or prove none exists. All known $\mathsf{AC}^0$ approximate-degree upper bounds are trivial ($O(n)$); the gap between the sublinear $\Omega(n^{1-\delta})$ lower bound and the linear upper bound is the open question.

### Circuit lower bounds from approximate degree (Section 11.3, 11.4)

- **Worst-case (Section 11.3.1):** If every $C \in \mathcal{C}$ has threshold degree $\le n-1$, then no circuit in $\mathcal{C}$ computes parity. If approximate degree $\le o(n)$, none computes Majority (since $\widetilde{\deg}(\mathsf{MAJ}) = \Theta(n)$). Reichardt: De Morgan formulas of size $s$ have approximate degree $O(\sqrt s)$, so size-$o(n^2)$ formulas cannot compute parity or majority.
- **$\mathsf{AC}^0 \circ \mathsf{MOD}_2$ via $\mathsf{IP2}$ (Tal [Tal17], Bun-Kothari-Thaler [BKT21], pp. 108-110):** A $\mathcal{C} \circ \mathsf{MOD}_2$ circuit (a $\mathcal{C}$-circuit with a parity layer at the leaves) computing $\mathsf{IP2}$ on a $1/2 + \varepsilon$ fraction of inputs requires size $\Omega(s(n))$ where $s(n)$ is set by the approximate degree of $\mathcal{C}$-circuits. For depth-$D$ $\mathsf{AC}^0$ the bound is the slightly superlinear $\Omega(n^{1 + 2^{-D}})$ (p. 110). The mechanism: $\mathsf{IP2}$ has correlation $2^{-n}$ with every parity function, so a low-degree sign-representation built from $o(n/\log n)$-degree pieces over the parity leaves contradicts that anti-correlation.
- **Parity not in $\mathsf{LTF} \circ \mathsf{AC}^0$ (Section 11.4, [ABFR94], pp. 111-113):** Two steps. Step 1: any degree-$o(\sqrt n)$ polynomial disagrees with parity on $\ge (1/2 - o(1))$ of inputs (tight: the middle $O(\sqrt n)$ Hamming layers can be interpolated exactly on 99%). This is dual to a $\psi$ of pure high degree $n - 2k$ that vanishes on a small set $S$ and is perfectly correlated with parity ($\psi(x) = \oplus_n(x) \cdot q^2(x)$, p. 112). Step 2: any $\mathsf{LTF} \circ \mathsf{AC}^0$ circuit is sign-agreed on 99% of inputs by a polylog-degree polynomial, via the $O(\log(n)\log(1/\delta))$ probabilistic degree of OR ([BRS90], p. 113) lifted gate-by-gate.

### MAJ and LTF circuit lower bounds via PP / UPP communication (Section 10.4.4, 10.5.2)

- **$\mathsf{MAJ} \circ \mathsf{LTF}$ (Theorem 87 / Nisan [Nis93], p. 90):** a $\mathsf{MAJ} \circ \mathsf{LTF}$ circuit of size $s+1$ computes $F$ with $\mathsf{PP}^{cc}(F) \le O(\log^2 s)$. Combined with the $\Omega(n^{1/3})$ $\mathsf{PP}^{cc}$ lower bound for an $\mathsf{AC}^0$ function (from the smooth dual witness of Theorem 92), this gives an $\mathsf{AC}^0$ function not computable by $\mathsf{MAJ} \circ \mathsf{LTF}$ circuits of size $2^{\Omega(n^{1/3})}$ (p. 91).
- **$\mathsf{LTF} \circ \mathsf{MAJ}$ (Theorem 94, p. 98):** a $\mathsf{LTF} \circ \mathsf{MAJ}$ circuit of size $s+1$ gives $\mathsf{UPP}^{cc}(F) \le O(\log s)$. Combined with Theorem 92 and Theorem 89, this yields an $\mathsf{AC}^0$ function not computable by $\mathsf{LTF} \circ \mathsf{MAJ}$ circuits of size $< 2^{n^{1/3}}$.
- **$\mathsf{LTF} \circ \mathsf{LTF}$ (the wall, p. 99):** Chattopadhyay-Mande [CM18] gave a polynomial-size $\mathsf{LTF} \circ \mathsf{LTF}$ circuit computing a function with $\mathsf{UPP}^{cc}(F) \ge \Omega(n^{1/4})$. So the UPP / sign-rank route does **not** reach $\mathsf{LTF} \circ \mathsf{LTF}$, which is the gateway to $\mathsf{TC}^0$. This is the concrete statement of where the analytic method currently stops short of $\mathsf{TC}^0$.

## Techniques and proof ideas

The reusable methods, in the order a builder would pick them up:

1. **LP duality is the master move.** Every approximate-degree lower bound is, by strong duality, witnessed by some dual polynomial $\psi$ satisfying (15)-(17) (Theorem 28). Constructing $\psi$ is necessary and sufficient; symmetrization (Section 5) is the older, lossy alternative that only works cleanly for symmetric or symmetric-structured functions.

2. **Symmetrization** (Lemmas 21, 22, 27): collapse a multivariate polynomial $p$ to a univariate $q(t) = \mathbb{E}_{x \sim D_t}[p(x)]$ without increasing degree, then apply Markov / Markov-Bernstein (Theorems 6, 25) or Coppersmith-Rivlin (Theorem 24) to force large degree. Reused for OR (Theorem 23) and the Minsky-Papert CNF threshold degree (Theorem 26). The technical hazard is boundedness at non-integer points, patched by Coppersmith-Rivlin.

3. **Chebyshev / Markov extremality** (Section 3.2): the engine behind both the $O(\sqrt n)$ upper bound and the $\Omega(\sqrt n)$ lower bound for OR. A degree-$\sqrt n$ polynomial is the threshold at which a function bounded at integer points can blow up at non-integer points.

4. **Dual block composition $\psi \star \phi$** (Definition 38): the headline reusable technique. It always gives pure high degree $\mathrm{phd}(\psi)\cdot\mathrm{phd}(\phi)$ (Lemma 39) and $\ell_1$-norm 1 (Lemma 40); the only thing to check per application is correlation. The recurring trick to get correlation is to use a dual $\phi$ with **one-sided error** (Corollary 33), so that the error term $E(z)$ vanishes on the problematic input (Lemma 41, Case 2; Theorem 47, Case 2). When even that fails, multiply $\psi \star \phi$ by a "killing" polynomial $Q(t) = \prod (t-i)$ (or $p(x) = Q(\sum \mathbb{1}_{\mathcal{E}_\phi}(x_j))$) that zeroes bad inputs while only mildly reducing pure high degree (Theorem 44 proof, pp. 43-44).

5. **Smoothness of dual witnesses** (Section 10.5, Theorem 89, Theorem 92): to push from approximate-degree/PP lower bounds to sign-rank/UPP lower bounds, the dual $\psi$ must additionally be "smooth," $|\psi(x)| \ge 2^{-d/2}\cdot 2^{-n}$ for all $x$ (Eq. 75, p. 93). Smoothness is what lets the matrix-analytic dual $\eta = \psi \star \phi \star \mu$ overcome the $2^{-\Theta(d)}$ error loss inherent in the pattern-matrix method (Theorem 77). The explicit smooth dual for the $\mathsf{AC}^0$ function $\mathsf{AND}_{n^{1/3}} \circ \mathsf{OR}_{n^{2/3}} \circ \oplus_{\log^2 n}$ (Theorem 92, pp. 95-98) is built in three steps (largeness on low-weight inputs, error correction via Lemma 93, smoothing).

6. **Probabilistic polynomials and gate-by-gate composition** (Section 11.4, [BRS90]): an $\mathsf{AC}^0$ circuit of depth $d$ has a probabilistic polynomial of degree $\log(s)^{O(d)}$ that exactly computes it on 99% of inputs, built from the $O(\log n \cdot \log(1/\delta))$-degree probabilistic polynomial for OR (random subset products, p. 113).

7. **Query-to-polynomial bridge** (Beals et al., Section 4.1): import quantum algorithms (Grover) as upper bounds and export approximate-degree lower bounds as quantum query lower bounds.

## Relevance to this project

This survey is the **analytic statement of the $\mathsf{TC}^0$ hinge** identified in the 2050 backward-induction dossier. The dossier's claim is that the polynomial method dies at the $\mathsf{TC}^0$ step because MAJORITY has approximate degree $\Theta(n)$ as a symmetric function (Paturi 1992; the survey states $\widetilde{\deg}(\mathrm{MAJ}) = \Theta(n)$ on p. 95). The $\Theta(\sqrt{n})$ figure is OR/AND, not MAJORITY. The survey supplies the precise theorems:

- **The hinge value, exactly.** $\widetilde{\deg}(\mathsf{OR}_n) = \Theta(\sqrt n)$ (Theorem 23 + Lemma 7), and the symmetric $t$-threshold function has $\widetilde{\deg} = \Theta(\sqrt{nt})$ (Theorem 3). These are the analytic ceilings any polynomial-method lower bound against threshold circuits must clear. The survey's Section 11.3 makes the connection explicit: an approximate-degree upper bound of $o(n)$ on a circuit class rules out Majority, and a threshold-degree upper bound of $n-1$ rules out Parity.

- **Where the method stops short of $\mathsf{TC}^0$, stated as a theorem.** The $\mathsf{LTF} \circ \mathsf{LTF}$ result of Chattopadhyay-Mande [CM18] (Section 10.5, p. 99) shows there is a polynomial-size $\mathsf{LTF} \circ \mathsf{LTF}$ circuit with $\mathsf{UPP}^{cc} \ge \Omega(n^{1/4})$. So the sign-rank / UPP route, which is the strongest analytic handle the survey offers, provably **cannot** reach depth-two threshold circuits. The current frontier is $\mathsf{MAJ} \circ \mathsf{LTF}$ and $\mathsf{LTF} \circ \mathsf{MAJ}$ (Theorems 87, 94), both one rung below $\mathsf{TC}^0$. This is the concrete, citable form of the dossier's "the polynomial method dies at the $\mathsf{TC}^0$ step."

- **Barrier discipline.** Approximate degree and the dual-polynomial method are not on their face natural-proofs-immune; the survey's circuit lower bounds (Section 11.3) are explicitly **average-case** (correlation bounds against $\mathsf{IP2}$), which is the regime the natural-proofs barrier penalizes. The largeness + constructivity question (LEARNINGS finding 3, the MCSP crux) applies: a low approximate degree is a large, efficiently testable property of a function's truth table, so any approximate-degree-based separation must explain why it is not natural. The survey does not address this; it is a discrepancy / gap to flag (see below).

- **The "every rational invariant algebrizes" observation.** The dossier's missing-object hypothesis is that every rational trace/rank/volume invariant a fast algorithm computes algebrizes, and the candidate non-algebrizing object is a mod-2 torsion "Bockstein bridge." Approximate degree, threshold degree, and sign-rank are all rational/real-valued invariants of the truth table, computed via LP duality over $\mathbb{R}$. The survey's entire toolkit is real-analytic. This is consistent with the dossier's suspicion that the analytic method, however far it is pushed, stays inside the algebrizing world. The survey contains no mod-2 / torsion-valued complexity measure (spectral sensitivity, Section 9, is also real-valued).

## What this enables / what remains open

### Mapping to the research directions

- **01 (circuit lower bounds, Williams ACC0 toward P/poly):** The survey gives the strongest current analytic lower bounds against threshold-style circuits ($\mathsf{MAJ}\circ\mathsf{LTF}$, $\mathsf{LTF}\circ\mathsf{MAJ}$, size $2^{\Omega(n^{1/3})}$, Section 10.4.4-10.5.2) and the $\mathsf{AC}^0 \circ \mathsf{MOD}_2$ / $\mathsf{IP2}$ average-case bounds (Section 11.3). These are complementary to the Williams algorithm-to-lower-bound spine: Williams gets $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$ by algorithm design, while this survey gets explicit-function lower bounds by polynomial duality. The hinge fact (the $\mathsf{LTF}\circ\mathsf{LTF}$ wall, p. 99) tells the builder where the analytic method must be supplemented.
- **02 (natural-proofs evasion, the MCSP crux):** Approximate degree is a candidate "useful property" of truth tables. Open: is the dual-polynomial method natural, and if so does its application to explicit functions (rather than as a distinguisher) save it? The survey is silent; this is the cleanest place to apply the project's barrier checker to a real lower-bound family.
- **03 (proof complexity, NP vs coNP):** Less direct. Threshold degree connects to $\mathsf{PP}$ and to communication / proof systems via Sections 10-11; the LP-duality framing (dual = certificate) is structurally analogous to proof-complexity duality.
- **04 (GCT, multiplicity obstructions):** Orthogonal in technique, but parallel in spirit: both replace an existence question by the construction of a dual / obstruction object. The survey's smoothness condition (a fine-grained extra property the dual must have to upgrade PP to UPP, Theorem 89) is reminiscent of the multiplicity-vs-occurrence distinction that sank the GCT occurrence-obstruction program.

### Mapping to the LEARNINGS findings

- **(5) average-case is not worst-case:** Section 11.3.2 is a textbook instance: approximate-degree **upper** bounds give average-case (correlation) circuit lower bounds, a strictly different regime from the worst-case threshold-degree bounds of 11.3.1.
- **(7) GCT hit its occurrence-obstruction no-go / (10) implied fourth barrier (bounded-interface reconstruction):** the smoothness condition (Theorem 89) and the one-sided-error condition (Corollary 33) are examples of "extra interface properties" a dual witness must satisfy to transfer between models (query to PP to UPP). Open Problem 95 (p. 100) asks for a gadget $g$ such that $\deg_\pm(f) \ge d$ generically implies $\mathrm{rank}_\pm(f \circ g) \ge 2^d$; resolving it would remove the smoothness requirement and is exactly a "bounded-interface reconstruction" question.
- **(9) the missing object is a non-algebrizing fast-computable invariant:** every measure in this survey (approximate degree, threshold degree, one-sided degree, sign-rank, spectral sensitivity, approximate rank/weight) is real-valued and LP/spectral, hence plausibly algebrizing. The survey contains no torsion-valued or mod-$p$ analytic invariant. This is positive evidence for the dossier's claim that the missing object lives outside the real-analytic toolkit.

### Concrete open questions / cruxes this source exposes

1. **Open Problem 13 (p. 17):** is $\widetilde{\deg}(f \circ g) \ge \Omega(\widetilde{\deg}(f)\cdot\widetilde{\deg}(g))$ for all total $f, g$? Resolved in special cases (Theorems 43, 44, 45, 48) but open in general.
2. **Open Problem 59 (p. 55):** is there an $\mathsf{AC}^0$ function with approximate degree $\Omega(n)$ or $\Omega(n/\log n)$? The gap between $\Omega(n^{1-\delta})$ and the trivial $O(n)$ upper bound is the $\mathsf{AC}^0$ frontier.
3. **Open Problem 95 (p. 100):** find a constant-size gadget $g$ with $\deg_\pm(f)\ge d \Rightarrow \mathrm{rank}_\pm(f\circ g)\ge 2^d$ generically. This is the query-to-UPP lifting theorem whose absence forces the ad-hoc smoothness conditions.
4. **The $\mathsf{LTF}\circ\mathsf{LTF}$ / $\mathsf{TC}^0$ wall (p. 99):** the UPP / sign-rank method provably fails for depth-two threshold circuits ([CM18]). What measure replaces sign-rank to break this wall? The dossier's bet is a non-algebrizing, possibly torsion-valued invariant; the survey supplies no candidate, which sharpens the search.

### Discrepancy log

- **Theorem 3 / MAJORITY value, my own provisional reconciliation.** The survey states the symmetric master theorem as $\widetilde{\deg}_\varepsilon(f) = \Theta(\sqrt{nt} + \sqrt{n\log(1/\varepsilon)})$ (Theorem 3, p. 9) and separately gives $\widetilde{\deg}(\mathsf{MAJ}) = \Theta(n)$ (p. 108). The project dossier's hinge statement uses "$\widetilde{\deg}(\mathsf{MAJ}) = \Theta(\sqrt n)$." These are reconcilable: the $\Theta(\sqrt n)$ value is the approximate degree of OR / of the approximate-counting (threshold-$t$ for small $t$) regime that governs the polynomial method's reach against AC0-with-a-few-MAJ-gates, whereas full Majority (jump at $t = n/2$) has approximate degree $\Theta(n)$. I am flagging this rather than silently resolving it: a VERIFIER should confirm which MAJORITY statement the dossier's "$\Theta(\sqrt n)$ hinge, polynomial method dies" claim intends. My reading of the survey is that the operative fact for "the method dies at $\mathsf{TC}^0$" is the $\mathsf{LTF}\circ\mathsf{LTF}$ UPP wall (p. 99), not a single approximate-degree number for MAJORITY.
- **House caveat on partial expertise.** Sections 8.1-8.6 (Surjectivity, Collision, PTP, Element Distinctness lower bounds, the full Lemma 54), Section 9 (Spectral Sensitivity), and Sections 10.1-10.3 (lifting, the query/communication zoo) were read only at the level of statements and TOC, not line-by-line proof. The structural claims about those sections above are taken from the survey's own summaries and should be re-checked against the full text before being cited as load-bearing.
