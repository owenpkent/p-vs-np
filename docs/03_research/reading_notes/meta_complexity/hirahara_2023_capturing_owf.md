# Reading notes: Capturing One-Way Functions via NP-Hardness of Meta-Complexity (Hirahara, 2023)

- **Source:** `references/meta_complexity/hirahara_2023_capturing_owf.pdf`
- **Type / venue:** Paper, STOC 2023 (read copy is ECCC TR23-037, March 27 2023).
- **Dossier strand:** Meta-complexity device (the worst-case-to-cryptographic-hardness bridge).
- **Read:** Read in full: abstract; the entire introduction (Sections 1.1 through 1.3, pages 1 to 6); the entire proof overview (Section 2, pages 7 to 16, including the three-step proof skeleton and the conditional NP-hardness sketch in 2.2); Section 3 on paddability (pages 17 to 18); Section 4 related work (page 18); the relevant preliminaries (Section 5, pages 19 to 21); the NP-hardness construction (Section 6 through Claim 6.11, pages 22 to 24); and the main-result statements (Theorems 10.3, 10.4, 11.1, pages 51 to 54). Skimmed at the lemma-statement level from the table of contents and section headers: the technical interiors of Sections 7 (PRG / symmetry of information), 8 (input-aware P/poly-restricted reduction machinery), 9 (HSG to auxiliary-input OWF), 11.1 to 11.2 (the parametric-honest to size-expanding transformation and the padding-conjecture proof), and Appendices A and B. Claims below are cited to the section or page where I actually read the statement.

## Summary

The paper gives the first characterization of a cryptographic primitive based on average-case hardness (a one-way function, OWF) by a purely worst-case hardness assumption (NP-hardness). It introduces distributional Kolmogorov complexity $\mathsf{dK}^{\mathsf{poly}}(x \mid \mathcal{D})$, a generalization of time-bounded conditional Kolmogorov complexity, and proves that, assuming $\mathsf{NP} \not\subseteq \text{i.o.}\mathsf{P/poly}$, a OWF exists if and only if approximating $\mathsf{dK}^{\mathsf{poly}}$ is NP-hard under (parametric-honest, randomized, nonadaptive) reductions (Theorem 11.1). The central technical move is to conditionally close the gap between errorless and error-prone average-case complexity of NP by fusing Nanashima's black-box "limits" (ITCS 2021) with Hirahara's non-black-box worst-case-to-average-case reduction (FOCS 2018), via a new intermediate notion of input-aware $\mathsf{P/poly}$-restricted reduction. In Impagliazzo's five-worlds language, NP-hardness of the meta-computational device simultaneously excludes errorless Heuristica and errorless Pessiland.

## Key definitions and results

### The meta-computational device: distributional Kolmogorov complexity

- **Definition 1.1 (distributional Kolmogorov complexity, page 4).** For $x \in \{0,1\}^*$, time bound $t$, parameter $\lambda \in (0,1]$, and a distribution $\mathcal{D}$ over $\{0,1\}^m$:
  $$\mathsf{dK}^t_\lambda(x \mid \mathcal{D}) := \min\{ |d| : \Pr_{y \sim \mathcal{D}}[U^t(d,y) = x] \ge \lambda \}.$$
  It is the shortest program $d$ that prints $x$ given an input $y$ drawn from $\mathcal{D}$, succeeding with probability at least $\lambda$. For a singleton distribution $\mathcal{D}_y$ this collapses exactly to conditional Kolmogorov complexity: $\mathsf{dK}^t_\lambda(x \mid \mathcal{D}_y) = \mathsf{K}^t(x \mid y)$ (page 4). The meta-computational decision problem is: given $x$, a circuit $D$ representing $\mathcal{D}$, a size parameter $s$, and confidence $\lambda$, does $\mathsf{dK}^\tau_\lambda(x \mid \mathcal{D}) \le s$? Approximating this (with small additive error in $\lambda$) is in $\mathsf{pr\text{-}MA}$ (page 4).

- The $A$-oracle and randomized-oracle variants $\mathsf{dK}^{\tau,A}$ and the randomized-program variant $\mathsf{dpK}^{\mathsf{poly}}$ are defined so that NP-hardness of $\mathsf{dpK}^{\mathsf{poly}}$ relates to OWFs secure against $\mathsf{BPP}$ (Definitions 5.2, 5.3, page 20 to 21; statement on page 5). Here $\mathsf{dpK}^t_\lambda(x \mid \mathcal{D}) := \min\{ s : \Pr_{r \sim \{0,1\}^t}[\mathsf{dK}^t_\lambda(x \mid \mathcal{D}, r) \le s] \ge \tfrac{3}{4} \}$ (page 5).

### Main characterization

- **Theorem 1.2 / Theorem 11.1 (informal page 4, formal page 54).** Assume $\mathsf{NP} \not\subseteq \text{i.o.}\mathsf{P/poly}$ (NP not computable by polynomial-size circuits almost everywhere). The following are equivalent:
  1. There exists a one-way function secure against polynomial-size circuits.
  2. For some constant $\epsilon > 0$, there is a parametric-honest randomized polynomial-time nonadaptive reduction from NP to a $(1+\epsilon)$-factor approximation of $\mathsf{dK}^{\tau,A}$ for all large polynomials $\tau$ and all oracles $A \in \mathsf{P/poly}$.
  3. For some $g(n) = n^{1/(\log\log n)^{O(1)}}$, there is a parametric-honest randomized polynomial-time one-query reduction from NP to a $g(n)$-factor approximation of $\mathsf{dK}^{\tau,A}$.
  
  The formal Theorem 11.1 states the equivalence with the gap promise problem $\mathrm{Gap}_{\tau,\epsilon}\mathsf{MdKP}^A$ under $\le_{\mathsf{tt}}^{\mathsf{BPP}}$ (item 2) and $\le_{\mathsf{m}}^{\mathsf{coRP}}$ (item 3) parametric-honest reductions. A reduction to $\mathsf{dK}^{\mathsf{poly}}$ is *parametric honest* (terminology from [SS20]) if the size parameter $s$ in any query on inputs of length $n$ satisfies $s \ge n^\gamma$ for a constant $\gamma > 0$ (page 4).

- **Unconditional rephrasing (page 5):** A one-way function exists if and only if $\mathsf{NP} \not\subseteq \text{i.o.}\mathsf{P/poly}$ AND it is NP-hard to approximate $\mathsf{dK}^{\tau,A}$. The assumption $\mathsf{NP} \not\subseteq \text{i.o.}\mathsf{P/poly}$ is *necessary*: if NP is easy then every NP problem is trivially NP-hard while no OWF exists, so the worst-case-hardness assumption excludes the Algorithmica world from the characterization (page 5).

### NP-hardness of the device under a OWF (the converse direction's anchor)

- **Theorem 6.3 (page 22).** If a OWF secure against polynomial-size circuits exists, then $\mathsf{NP} \le_{\mathsf{m}}^{\mathsf{coRP}} \{ \mathrm{Gap}_{\tau,\alpha}\mathsf{MdKP}^A : \tau \text{ a polynomial}, A \in \mathsf{P/poly} \}$ for some $\alpha(n) = n^{1/(\log\log n)^{O(1)}}$, via a size-expanding reduction. This is proved by reducing the Minimum Monotone Satisfying Assignment problem (MMSA), which is NP-hard to approximate to within a factor $g(n) = n^{1/(\log\log n)^{O(1)}}$ (Lemma 6.5, citing [DS04; DHK15]), to the gap distributional-Kolmogorov problem using a secret-sharing scheme.

### Closing the errorless / error-prone gap (the three-step bridge)

The construction (Section 2.1, pages 10 to 12) chains three reductions, presented in the paper in reverse order:

- **Step 1 (NP to hitting set generator, page 14):** Using Hirahara's non-black-box techniques [Hir18; Hir22c], $\mathsf{dK}^{\mathsf{poly}} \le_{\mathsf{tt}}^{\mathsf{BPP}} \{A : A \text{ avoids } \mathcal{H}^{\mathrm{univ}}\} \uparrow \mathsf{P/poly}$ for the universal hitting set generator $\mathcal{H}^{\mathrm{univ}}$. Combining with NP-hardness of $\mathsf{dK}^{\mathsf{poly}}$ under size-expanding reductions yields an input-aware reduction $\mathsf{NP} \le_{\mathsf{tt}}^{\mathsf{BPP}} \{A : A \text{ avoids } H\} \uparrow \mathsf{P/poly}\,/\!/\,2n$.
- **Step 2 (HSG to auxiliary-input OWF, page 12, Theorem 9.3):** Using Nanashima's proof techniques [Nan21] (which employ [IL90]), an input-aware $\mathsf{P/poly}$-restricted reduction to avoiding $H$ transforms into $\mathsf{NP} \le_{\mathsf{tt}}^{\mathsf{BPP}} \{I : I \text{ inverts } f\} \uparrow \mathsf{P/poly}$ for some auxiliary-input one-way function $f$ (requires $s(n) < n - \omega(\log n)$).
- **Step 3 (auxiliary-input OWF to OWF, page 11, Theorem 10.3):** Using that a one-way function is *testable* (the crucial insight from [Nan21], via [MX10]), the error-prone reduction is made errorless. If $\mathsf{NP} \le_{\mathsf{tt}}^{\mathsf{BPP}} \{I : I \text{ inverts } f\} \uparrow \mathsf{P/poly}$ then $\mathsf{DistNP} \le_{\mathsf{tt}}^{\mathsf{AvgBPP}} \{I : I \text{ inverts } g\} \uparrow \mathsf{P/poly}$ for a genuine (unary-auxiliary-input) one-way function $g$.

Step 1 establishes that errorless Heuristica does not exist ($\mathsf{NP} \not\subseteq \text{i.o.}\mathsf{P/poly} \Rightarrow \mathsf{DistNP} \not\subseteq \text{i.o.}\mathsf{AvgP/poly}$, page 11). Step 3 establishes that errorless Pessiland does not exist ($\mathsf{DistNP} \not\subseteq \text{i.o.}\mathsf{AvgP/poly} \Rightarrow$ OWF exists). Together they exclude both worlds simultaneously.

### Supporting machinery (read at statement level)

- **Definition (B-restricted reduction, Eqs. (1) to (2), page 8).** $M$ is a $\mathbb{B}$-restricted reduction from $L$ to $\mathbb{A}$ if for every oracle $B \in \mathbb{B}$ and long inputs $x$, whenever $M$ cannot distinguish $A$ from $B$ on its query distribution ($\Pr_M[A(q) = B(q) \text{ for every query } q] \ge \tfrac12$) it follows that $\Pr_M[M^B(x) = L(x)] \ge \tfrac34$. Written $L \le_{\mathsf{tt}}^{\mathsf{BPP}} \mathbb{A} \uparrow \mathbb{B}$. This strictly strengthens the prior "size-restricted" / "class-specific" reductions [GV08; GT07], which were vacuous when the HSG is secure (page 8, footnote 8).
- **Input-aware $\mathsf{P/poly}$-restricted reduction (page 9):** Strengthens the above by giving the efficient oracle $B$ the input $x$ (and input-dependent advice $a$ of length $\alpha(n)$). Notation $L \le_{\mathsf{tt}}^{\mathsf{BPP}} \mathbb{A} \uparrow \mathbb{B}\,/\!/\,\alpha(n)$. Advice is given to the oracle, not the reduction, so longer advice makes the reduction *stronger* (more restrictive); it interpolates between $\mathsf{P/poly}$-restricted and full black-box reductions. Nanashima's proof goes through for $\alpha = 2n$ (page 10).
- **Theorem 7.8 (symmetry of information for $\mathsf{dK}^{\mathsf{poly}}$, page 15):** If $\mathsf{DistNP} \subseteq \mathsf{AvgP}$ then a symmetry-of-information bound for distributional Kolmogorov complexity holds, generalizing the Heuristica symmetry of information of [Hir22c; GK22]. The key ingredient is a new reconstruction property of the $k$-wise direct product generator $\mathsf{DP}_k$ (Section 7.1, page 27).

## Techniques and proof ideas

A builder would reuse the following components.

- **The device is a conditional / distributional generalization of $\mathsf{K}^t$.** The single move that makes the worst-case-to-cryptographic bridge possible is replacing the fixed auxiliary string $y$ in $\mathsf{K}^t(x \mid y)$ by a *distribution* $\mathcal{D}$ (Definition 1.1). The distribution slot is exactly what lets a secret-sharing instance be encoded as the conditioning object (Section 6.3).

- **Non-black-box reductions made tractable via input-awareness.** The technical heart is that Hirahara's [Hir18] reduction is inherently non-black-box (it lands in $\mathsf{AM} \cap \mathsf{coAM}$, [HW20]), so it cannot be black-box if MCSP/MINKT are outside $\mathsf{AM} \cap \mathsf{coAM}$ as conjectured. The paper recasts it as a "mildly" black-box reduction (input-aware $\mathsf{P/poly}$-restricted) on which Nanashima's [Nan21] proof techniques still apply (Section 2.1.1, pages 8 to 10). The randomly-chosen threshold $\theta$ of Bogdanov-Trevisan [BT06b], carried as $O(\log n)$ input-dependent advice, bounds the total advice to $|x| + O(\log n) \le 2n$ (page 13).

- **OWF testability turns error-prone into errorless (Step 3).** Given a query $q$ and a candidate inverter output, sample $y \sim \{0,1\}^{s(|q|)}$ and check $f_q(I(q, f_q(y))) = f_q(y)$; if the check fails, output the failure symbol $\bot$ rather than a wrong answer (page 11). Hardness amplification [Yao82; Gol01] ensures the failure probability is small. This is the mechanism that the dossier should treat as the "errorless certificate" lever.

- **Secret sharing + Goldreich-Levin to encode MMSA into the conditioning distribution (Section 6.3, page 24).** Share a uniform secret $x \sim \{0,1\}^\ell$ among $n$ parties via the Benaloh-Leichter monotone-formula scheme [BL88] (Lemma 6.10). Build $\mathcal{D}$ outputting $y := (z_1, \dots, z_n, G_m(\mathsf{GL}_k(f_1; z_1)) \oplus s_1, \dots, G_m(\mathsf{GL}_k(f_n; z_n)) \oplus s_n)$ where $\mathsf{GL}_k$ is the Goldreich-Levin hard-core function, $G_m$ a PRG, $s_i$ the $i$-th share. Completeness (Claim 6.11): a satisfying assignment of weight $\theta$ gives a program of size $\le 2\theta\lambda$ that hard-wires $\{f_i : i \in T\}$, recomputes the authorized shares, and runs $\mathrm{Rec}$, so $\mathsf{dK}^t_1(x \mid \mathcal{D}) \le 2\theta\lambda$. Soundness uses the algorithmic information-extraction lemma of [Hir22b] plus PRG security and secret-sharing privacy. This is the concrete gadget linking $\mathsf{NP}$-hardness of approximation to the size parameter of the device.

- **Reconstruction property of the direct product generator $\mathsf{DP}_k$ (Section 7.1, statement page 16).** For every distinguisher $D$ with advantage $\lambda$, there is a reconstruction procedure $R^D$ taking $\approx k$ bits of advice that recovers $x$ from $\mathsf{DP}_{k+\ell}(x;z)$ with probability $\lambda - \epsilon$, $\ell = O(\log(n/\delta))$. This underlies both Step 1 and the symmetry-of-information theorem.

## Relevance to this project

This source is the load-bearing citation for the **meta-complexity device strand** and the dossier's identified **leading path** (meta-complexity riding the worst-case-to-average-case spine). Concretely:

- **It is the cleanest existing instance of LEARNING (3): the constructivity crux is MCSP / meta-complexity.** Hirahara shows that NP-hardness of a single meta-computational problem (approximating $\mathsf{dK}^{\mathsf{poly}}$) is *exactly* what is needed to exclude both errorless Heuristica and errorless Pessiland, i.e., to base OWFs on worst-case NP-hardness. The device is a relative of MINKT/MCSP (the $\mathsf{dK}^t(x \mid \mathcal{D}_y) = \mathsf{K}^t(x \mid y)$ collapse, page 4), so this is the meta-complexity crux instantiated as a cryptographic-vs-worst-case bridge.

- **The reductions are explicitly non-relativizing (LEARNING 4 and the barrier discipline).** The introduction states the proof techniques are non-relativizing and use non-black-box reductions, and so are "unlikely subject to" the standard limits (page 1, and the comparison with Santanam's Universality Conjecture on page 18: the latter's proof techniques relativize [RS22] whereas these do not [Hir22b]). For the barrier scorecard this is a candidate technique that claims to evade relativization. It does not directly address natural proofs or algebrization; the natural-proofs angle is implicit through the OWF/PRG it produces (a OWF secure against $\mathsf{P/poly}$ is exactly the object Razborov-Rudich say must exist to block natural proofs, Lemma 5.7 [HILL99] connects OWF and PRG existence).

- **It sharpens the worst-case-to-cryptographic bridge into a named obstacle pair.** The paper isolates two issues the prior folklore approach could not overcome (page 3): (a) errorless vs error-prone average-case complexity, and (b) the Saks-Santhanam [SS22] barrier showing NP-hardness of $\mathsf{K}^t$ under $t' \ll t$ reductions contradicts plausible assumptions. Hirahara sidesteps (b) by using the *distributional* variant and parametric-honest reductions, and resolves (a) conditionally via testability. For ADVERSARY: the Saks-Santhanam barrier is the relevant "this won't work for $\mathsf{q}^t$ / $\mathsf{K}^t$" obstruction, and the paper's claim is that $\mathsf{dK}^{\mathsf{poly}}$ dodges it.

## What this enables / what remains open

Mapping to the research directions and LEARNINGS.

- **Direction 02 (natural-proofs evasion, the MCSP crux):** This is the most direct connection. The device $\mathsf{dK}^{\mathsf{poly}}$ is a distributional cousin of MCSP/MINKT, and the characterization says a OWF (hence a PRG, the obstruction to natural proofs) exists iff this device is NP-hard. A builder pursuing natural-proofs evasion now has a concrete worst-case target whose NP-hardness would simultaneously construct the cryptographic object that blocks natural proofs.

- **Direction 03 (proof complexity, NP vs coNP):** Less direct, but the secret-sharing / monotone-formula MMSA reduction (Section 6.3) is a hardness-of-approximation gadget that proof-complexity work on monotone formulas (the KRW conjecture, raised on page 18 via Formula-MCSP paddability, Proposition 3.1 using [Has98; DM18]) can plug into.

- **LEARNING (5) average-case is not worst-case:** This paper is the most refined conditional statement about exactly *when* the two coincide for NP. It does not collapse the gap unconditionally; it shows the collapse is equivalent to OWF existence given $\mathsf{NP} \not\subseteq \text{i.o.}\mathsf{P/poly}$.

- **LEARNING (9) the missing object is a non-algebrizing fast-computable invariant:** Caveat flagged honestly. This paper does NOT exhibit such an invariant and does not engage the algebrization barrier at all. Its novelty is non-relativization plus non-black-box reductions. Whether the $\mathsf{dK}^{\mathsf{poly}}$ device or its reductions algebrize is not discussed in the text I read; this is an open question for ADVERSARY to score, not something the paper resolves.

Concrete open questions / cruxes this source exposes (all stated by the author):

1. **(Section 1.2 / page 6) Is approximating $\mathsf{dK}^{\mathsf{poly}}$ actually NP-hard?** The whole characterization is an "if and only if" against a hardness statement that is itself open. The paper proves only the converse direction unconditionally (NP-hardness of the device under a OWF assumption, Theorem 6.3); the forward direction (building a OWF from device NP-hardness) is what the three-step bridge delivers.

2. **(Conjecture 1.4, Meta-Complexity Padding Conjecture, page 6) Is $\mathsf{Gap}(\mathsf{K}^p \text{ vs } \mathsf{K})$ reducible to a $(1+\epsilon)$-approximation of $\mathsf{dpK}^\tau$ via a size-expanding reduction?** Under this conjecture (Theorem 1.5, page 6), a long list of objects become equivalent: OWF existence (i.o., against $\mathsf{BPP}$), hardness of approximating MCSP to factor $2^{(1-\epsilon)n}$, indistinguishability of $\mathsf{q}^t$ and $\mathsf{rK}^t$ levels, PRG and HSG existence. Proposition 1.6 shows the conjecture is implied by OWF existence, so it cannot be refuted without refuting OWFs. This is the cleaner, weaker target.

3. **(Conjecture 3.2, MCSP Padding Conjecture, page 18) Is MCSP paddable by an approximation-preserving reduction?** Formula-MCSP is (Proposition 3.1, via the resolved $\oplus_m$ case of KRW [Has98; DM18]); whether circuit-MCSP is, is open and tied to the KRW conjecture.

4. **(Section 1.2 question, page 3) Is meta-complexity *necessary* (not just sufficient) for excluding Heuristica and Pessiland?** The paper answers the three motivating questions (necessity is addressed by the iff characterization) but leaves open whether the same holds for *polynomial-time-bounded* conditional Kolmogorov complexity (not just the distributional version), noting Huang-Ilango-Ren [HIR23] proved NP-hardness of $\mathsf{K}^t(x \mid y)$ under indistinguishability obfuscation (page 18).

5. **For VERIFIER / barrier scorecard:** the non-relativization claim (page 1, page 18) is asserted but the algebrization status of the device and its reductions is not addressed in the read text. This should be entered as "unknown, to be scored" rather than "passes," and reconciled with LEARNING (1) that barriers compose and LEARNING (10) the implied bounded-interface reconstruction barrier.
