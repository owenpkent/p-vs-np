# Reading notes: Algebraic Topology (Allen Hatcher, 2002)

- **Source:** `references/algebraic_topology/hatcher_2002_algebraic_topology.pdf`
- **Type / venue:** Textbook, ~550 pages, Cambridge University Press 2002 (this PDF is a later reprinting carrying the "Note on the 2015 reprinting"; copyright 2001). The canonical free graduate text on the subject.
- **Dossier strand:** Strand-3 missing object (algebraic topology). The specific mod-2 torsion machinery (Ext torsion shift, the Bockstein homomorphism, and the relation $Sq^1 = \beta$) in which the project's candidate non-algebrizing invariant (a "Bockstein bridge" mod-2 torsion class) is phrased.
- **Read:** This is a ~550-page textbook; I did NOT read it all. I read in full the four project-relevant slices and read the table of contents, preface, and chapter openers for orientation:
  - Chapter 2 opener and Section 2.1 openings (PDF pages 112-118 / printed 103-109): $\Delta$-complexes, the boundary map $\partial$, $\partial^2 = 0$, chain complexes, simplicial and singular homology groups $H_n$. Read in full.
  - Chapter 3 opener and Section 3.1, "Cohomology Groups" (PDF pages 194-208 / printed 185-199): the idea of cohomology, the coboundary $\delta = \partial^*$, the universal coefficient theorem (Theorem 3.2), Corollaries 3.3 and 3.4, the Ext computation rules, cohomology of spaces. Read in full.
  - Section 3.E, "Bockstein Homomorphisms" (PDF pages 312-320 / printed 303-310): the Bockstein $\beta$ and $\tilde\beta$, the derivation property, Bockstein cohomology, Proposition 3E.3, Corollary 3E.4, lens-space and $SO(n)$ examples. Read in full.
  - Section 4.L, "Steenrod Squares and Powers" opening (PDF pages 496-502 / printed 487-493): cohomology operations (Proposition 4L.1), the Steenrod-square axiom list including property (7) $Sq^1 = \beta$, the Adem relation $Sq^{2i+1} = \beta Sq^{2i}$, stable splittings. Read in full.
  - Everything else (the fundamental group, van Kampen, covering spaces, the rest of Chapters 2-4, Poincare duality 3.3, the cup product 3.2 beyond its motivating opening, homotopy theory 4.1-4.3) I summarize only at the level of the table of contents and chapter introductions, and I flag those as not read in detail.

## Summary

This is the standard reference for singular and simplicial (co)homology. For this project only the torsion-tracking machinery matters. Three results carry the strand-3 weight. (1) The universal coefficient theorem (Section 3.1, Theorem 3.2) shows cohomology is homology dualized, and the dualization shifts torsion up one dimension via an $\mathrm{Ext}$ term: $\mathrm{Ext}(H_{n-1}, \mathbb{Z})$ captures exactly the torsion subgroup of $H_{n-1}$ (Corollary 3.3). (2) The Bockstein homomorphism $\beta : H^n(X;\mathbb{Z}_m) \to H^{n+1}(X;\mathbb{Z}_m)$ (Section 3.E) is the connecting map of the coefficient sequence $0 \to \mathbb{Z}_m \to \mathbb{Z}_{m^2} \to \mathbb{Z}_m \to 0$; it is precisely the operator that detects $\mathbb{Z}$-coefficient torsion that mod-$m$ reduction would otherwise blur. (3) For $m = 2$ this Bockstein equals the first Steenrod square: $Sq^1 = \beta$ (Section 4.L, Steenrod-square property (7)). These are exactly the "mod-2 torsion tools" the dossier's missing object is specified in.

## Key definitions and results

### Chain complexes and homology (Chapter 2 opener, Section 2.1, printed pp. 104-108)

A $\Delta$-complex structure on $X$ is a collection of maps $\sigma_\alpha : \Delta^n \to X$ satisfying injectivity on open simplices, face-compatibility, and a weak-topology condition (printed p. 103, conditions (i)-(iii)). The simplicial chain group $\Delta_n(X)$ is the free abelian group on the $n$-simplices. The boundary homomorphism is
$$\partial_n(\sigma_\alpha) = \sum_i (-1)^i \, \sigma_\alpha \,|\, [v_0,\dots,\hat v_i,\dots,v_n]$$
(printed p. 105). **Lemma 2.1 (p. 105):** $\partial_n \partial_{n+1} = 0$ (the signs cancel the two double-face summations). This makes $\cdots \to C_{n+1} \to C_n \to C_{n-1} \to \cdots$ a chain complex; the $n$th homology group is $H_n = \ker \partial_n / \mathrm{im}\, \partial_{n+1}$ (p. 106). Cycles are $\ker\partial$, boundaries are $\mathrm{im}\,\partial$.

A singular $n$-simplex is any continuous map $\sigma : \Delta^n \to X$ (printed p. 108). The singular chain group $C_n(X)$ is free abelian on these, the boundary uses the same alternating-face formula, $\partial^2 = 0$ again, and $H_n(X) = \ker\partial_n / \mathrm{im}\,\partial_{n+1}$. Singular homology is a homotopy invariant by construction (homeomorphic spaces give isomorphic $H_n$, p. 108), where simplicial homology was rigid. Proposition 2.6 splits $H_n$ over path-components; Proposition 2.7 gives $H_0(X) \cong \bigoplus \mathbb{Z}$, one $\mathbb{Z}$ per path-component (p. 109).

These are background only. The strand needs them so that "homology class" and "torsion subgroup of $H_n$" are well-defined objects to dualize.

### Cohomology as dualized homology (Section 3.1 opener, printed pp. 190-191)

Cohomology is "a simple dualization in the definition" (Chapter 3 opener, printed p. 185). Replace each chain group $C_n$ by its dual cochain group $C_n^* = \mathrm{Hom}(C_n, G)$ and each boundary $\partial$ by its dual coboundary $\delta = \partial^*$, which runs in the opposite (increasing) direction. From $\partial\partial = 0$ one gets $\delta\delta = 0$, and $H^n(C;G) = \ker\delta / \mathrm{im}\,\delta$ (printed p. 191). The explicit cochain formula is
$$\delta\varphi([v_0,\dots,v_{n+1}]) = \sum_i (-1)^i \varphi(\sigma | [v_0,\dots,\hat v_i,\dots,v_{n+1}])$$
so $\delta$ is the literal dual map of $\partial$ ("$\delta\varphi = \varphi\partial$", printed p. 189). Contravariance: induced maps $f^*$ go backwards, and (the point the chapter stresses) contravariance yields the extra ring structure, the cup product, which is the home of cohomology operations.

### The universal coefficient theorem (Section 3.1, Theorem 3.2, printed p. 195)

This is the load-bearing torsion result. **Theorem 3.2 (printed p. 195):** if a chain complex $C$ of free abelian groups has homology groups $H_n(C)$, then the cohomology groups $H^n(C;G)$ of the dual complex $\mathrm{Hom}(C_n, G)$ fit into split short exact sequences
$$0 \to \mathrm{Ext}(H_{n-1}(C), G) \to H^n(C; G) \xrightarrow{\ h\ } \mathrm{Hom}(H_n(C), G) \to 0.$$
The evaluation map $h$ is natural; the splitting is NOT natural (printed p. 196, with an exercise giving a topological example where it cannot be natural). The proof (pp. 191-195) builds $h$ from the free resolution $0 \to B_{n-1} \to Z_{n-1} \to H_{n-1}(C) \to 0$ and identifies the obstruction $\mathrm{Coker}\, i_{n-1}^*$ with $H^1$ of the dualized free resolution, i.e. with $\mathrm{Ext}(H_{n-1}, G)$. Lemma 3.1 (p. 194) proves free resolutions are unique up to canonical isomorphism, so $\mathrm{Ext}$ is well-defined.

The Ext computation rules (printed pp. 195-196) are the mechanical content the strand needs:
- $\mathrm{Ext}(H \oplus H', G) \cong \mathrm{Ext}(H,G) \oplus \mathrm{Ext}(H', G)$.
- $\mathrm{Ext}(H, G) = 0$ if $H$ is free.
- $\mathrm{Ext}(\mathbb{Z}_n, G) \cong G / nG$.

Consequences. (i) For finitely generated $H$, $\mathrm{Ext}(H, \mathbb{Z})$ is isomorphic to the torsion subgroup of $H$, while $\mathrm{Hom}(H, \mathbb{Z})$ is the free part. So **Corollary 3.3 (printed p. 196):** with $T_n \subset H_n$, $T_{n-1} \subset H_{n-1}$ the torsion subgroups, $H^n(C;\mathbb{Z}) \cong (H_n / T_n) \oplus T_{n-1}$. This is the precise sense in which **torsion shifts up one dimension** under dualization. (ii) **Corollary 3.4 (printed p. 196):** a chain map inducing a homology isomorphism induces a cohomology isomorphism with any coefficients $G$ (via naturality plus the five-lemma). (iii) Over a field $F$, the $\mathrm{Ext}$ term vanishes and $H^n(X; F) \cong \mathrm{Hom}(H_n(X; F), F)$ (printed pp. 198-199): cohomology is the exact dual of homology, and all torsion information is lost. This last point is the project-relevant warning: field coefficients erase exactly the torsion the strand wants to exploit.

The opening worked example (printed p. 190) is the toy that makes the shift visible: the complex with a $\mathbb{Z} \xrightarrow{2} \mathbb{Z}$ map has homology $\mathbb{Z}, \mathbb{Z}_2, 0, \mathbb{Z}$ in dimensions $0,1,2,3$, but cohomology $\mathbb{Z}, 0, \mathbb{Z}_2, \mathbb{Z}$: the $\mathbb{Z}_2$ in $H_1$ reappears as a $\mathbb{Z}_2$ in $H^2$, "shifted up a dimension."

### The Bockstein homomorphisms (Section 3.E, printed pp. 303-307)

This is the operator the dossier names directly. Hatcher works in cohomology to have cup products available (printed p. 303). A short exact sequence of coefficient groups $0 \to G \to H \to K \to 0$ stays exact after $\mathrm{Hom}(C_n(X), -)$ (because $C_n(X)$ is free), giving a long exact sequence
$$\cdots \to H^n(X;G) \to H^n(X;H) \to H^n(X;K) \xrightarrow{} H^{n+1}(X;G) \to \cdots$$
whose connecting map $H^n(X;K) \to H^{n+1}(X;G)$ is the **Bockstein homomorphism** (printed p. 303).

Two Bocksteins matter:
- $\beta : H^n(X;\mathbb{Z}_m) \to H^{n+1}(X;\mathbb{Z}_m)$, from $0 \to \mathbb{Z}_m \xrightarrow{m} \mathbb{Z}_{m^2} \to \mathbb{Z}_m \to 0$.
- $\tilde\beta : H^n(X;\mathbb{Z}_m) \to H^{n+1}(X;\mathbb{Z})$, from $0 \to \mathbb{Z} \xrightarrow{m} \mathbb{Z} \to \mathbb{Z}_m \to 0$ (the **integral Bockstein**).

These are tied by $\beta = \rho\,\tilde\beta$, where $\rho : H^*(X;\mathbb{Z}) \to H^*(X;\mathbb{Z}_m)$ is mod-$m$ reduction (printed p. 303, commutative triangle). The integral Bockstein $\tilde\beta$ is the one that "recovers $\mathbb{Z}$ coefficient information from $\mathbb{Z}_m$ coefficients" (printed p. 303), which is the explicit functionality the strand wants: a mod-$m$ class with nonzero $\tilde\beta$ certifies genuine integral torsion, not a coefficient artifact.

Properties established:
- **Derivation property** (printed p. 304, formula $*$): $\beta(a \smile b) = \beta(a)\smile b + (-1)^{|a|} a \smile \beta(b)$. Proved by lifting $\mathbb{Z}_m$ cocycles to $\mathbb{Z}_{m^2}$ cochains and computing $\delta$ of the lifted product.
- $\beta^2 = 0$ (printed p. 305), because $\beta = \rho\tilde\beta$ and $\tilde\beta\rho = 0$ in the long exact sequence. So the $H^n(X;\mathbb{Z}_m)$ form a chain complex under $\beta$, and one defines **Bockstein cohomology** $BH^n(X;\mathbb{Z}_m) = \ker\beta / \mathrm{im}\,\beta$. The interesting case is $m = p$ prime.
- **Proposition 3E.3 (printed p. 305):** for $H_n(X;\mathbb{Z})$ finitely generated, $BH^n(X;\mathbb{Z}_p)$ is computed summand-by-summand: each $\mathbb{Z}$ summand of $H^n(X;\mathbb{Z})$ contributes a $\mathbb{Z}_p$ to $BH^n$; each $\mathbb{Z}_{p^k}$ summand with $k > 1$ contributes $\mathbb{Z}_p$ to both $BH^{n-1}$ and $BH^n$; and a $\mathbb{Z}_p$ summand (i.e. $k = 1$, "primitive" torsion) gives $\mathbb{Z}_p$ summands of $H^{n-1}$ and $H^n$ with $\beta$ an isomorphism between them, so contributes nothing to $BH^*$. Proof uses minimal chain complexes (a direct-sum splitting into elementary pieces $M(g_i)$, p. 305-306). The takeaway: $\beta$ detects exactly the order-$p$ (not $p^2$) torsion; $BH^*$ strips that out and keeps only free part plus higher torsion.
- **Corollary 3E.4 (printed p. 306):** $H^*(X;\mathbb{Z})$ has no elements of order $p^2$ iff $\dim_{\mathbb{Z}_p} BH^n(X;\mathbb{Z}_p) = \mathrm{rank}\, H^n(X;\mathbb{Z})$ for all $n$; in that case $\rho$ is injective on the $p$-torsion and the image of the $p$-torsion equals $\mathrm{im}\,\beta$. This is the cleanest "$\beta$ sees torsion" statement in the section.

Worked examples that pin the behavior: $X = K(\mathbb{Z}_m, 1)$ (e.g. $\mathbb{R}P^\infty$ for $m=2$ or infinite lens spaces), where $\beta$ is an isomorphism $H^n \to H^{n+1}$ for $n$ odd and zero for $n$ even (Example 3E.1, p. 303-304); the cup product structure of lens spaces deduced via $\beta$ (Example 3E.2); $H^*(\mathbb{R}P^\infty \times \mathbb{R}P^\infty; \mathbb{Z})$ where all nontrivial classes have order 2 and $\mathrm{im}\,\beta = \ker\beta$ (Example 3E.5, p. 306-307); and the $H^*(SO(n);\mathbb{Z})$ calculations modulo odd torsion (Examples 3E.7, pp. 307-310), which use the Bockstein diagram to read off integral cohomology from $\mathbb{Z}_2$ cohomology.

### The relation $Sq^1 = \beta$ (Section 4.L, printed pp. 487-490)

A cohomology operation is a natural transformation $\Theta : H^m(-;G) \to H^n(-;H)$ (printed p. 488). **Proposition 4L.1 (p. 488):** operations $H^m(-;G) \to H^n(-;H)$ are in bijection with $H^n(K(G,m);H)$ via $\Theta \mapsto \Theta(\iota)$ on the fundamental class. The Bockstein is explicitly named as an example of a cohomology operation (printed p. 488).

The Steenrod squares $Sq^i : H^n(X;\mathbb{Z}_2) \to H^{n+i}(X;\mathbb{Z}_2)$ satisfy a seven-item axiom list (printed p. 489):
1. Naturality: $Sq^i(f^*\alpha) = f^*(Sq^i\alpha)$.
2. Additivity: $Sq^i(\alpha+\beta) = Sq^i\alpha + Sq^i\beta$.
3. Cartan formula: $Sq^i(\alpha\smile\beta) = \sum_j Sq^j\alpha \smile Sq^{i-j}\beta$.
4. Stability: $Sq^i$ commutes with the suspension isomorphism $\sigma$.
5. $Sq^i\alpha = \alpha^2$ if $i = |\alpha|$, and $Sq^i\alpha = 0$ if $i > |\alpha|$.
6. $Sq^0 = \mathbb{1}$.
7. **$Sq^1$ is the $\mathbb{Z}_2$ Bockstein homomorphism $\beta$ associated with the coefficient sequence $0 \to \mathbb{Z}_2 \to \mathbb{Z}_4 \to \mathbb{Z}_2 \to 0$.**

So $Sq^1 = \beta$ is an axiom (property 7, printed p. 489): the first Steenrod square literally is the mod-2 Bockstein. This is the exact identity the dossier names. Two further facts of project interest:
- **Adem relation** (printed p. 490): $Sq^{2i+1} = \beta\, Sq^{2i} = Sq^1 Sq^{2i}$. The odd squares are Bockstein-composed even squares; equivalently, the $Sq^{2i}$ behave as the odd-prime power operations $P^i$ do for $p = 2$.
- $Sq^1$ as a stable operation extends the cup-product square $\alpha \mapsto \alpha^2$ to a homomorphism that is invariant under suspension (where the raw squaring $\alpha \mapsto \alpha^2$ is not, since cup products of positive-dimensional classes die in a suspension, printed p. 489). This stability is exactly why $Sq^1 = \beta$ survives stabilization while the cup square does not.

Hatcher also remarks (printed p. 490) that only $Sq^1, Sq^2, Sq^4, Sq^8$ and the odd-prime $P^1$ detect homotopy of spheres; "$Sq^1$ detects a map $S^n \to S^n$ of degree 2." The $\mathbb{H}P^\infty$-degree-is-a-square argument (Example 4L.4, pp. 492-493) shows these operations carry genuine number-theoretic content (a degree must be a square mod every prime, hence a square).

## Techniques and proof ideas

A builder reusing this would take the following machinery, in increasing order of project relevance:

1. **Dualize, then read the Ext term.** The universal coefficient proof (Section 3.1) is the template for any "track the torsion" argument: take a free resolution of the homology, dualize with $\mathrm{Hom}(-, G)$, and the failure of exactness on the left end is precisely $\mathrm{Ext}(H, G)$, which for $G = \mathbb{Z}$ is the torsion subgroup. The split exact sequence is mechanical; the only subtlety is that the splitting is not natural, so torsion classes cannot be canonically separated from free classes, only filtered.

2. **Bockstein as the connecting map.** The construction (Section 3.E) is entirely formal: a short exact coefficient sequence plus the freeness of $C_n(X)$ gives a long exact sequence; the connecting homomorphism is $\beta$. The integral Bockstein $\tilde\beta$ valued in $\mathbb{Z}$ coefficients is the version that "lifts" mod-$m$ data back to integral torsion. The derivation property (formula $*$, p. 304) is proved by the explicit cochain lift to $\mathbb{Z}_{m^2}$: this is the concrete, finite, cocycle-level computation a builder would mechanize.

3. **Bockstein cohomology as a torsion-class detector.** Proposition 3E.3 and Corollary 3E.4 give a finite, summand-by-summand algorithm: from a finitely generated $H^*(X;\mathbb{Z})$, $\beta$ isolates exactly the order-$p$ torsion, and $BH^* = \ker\beta/\mathrm{im}\,\beta$ removes it. The minimal-chain-complex device (p. 305) reduces every computation to the two elementary pieces $0 \to \mathbb{Z} \to 0$ and $0 \to \mathbb{Z} \xrightarrow{k} \mathbb{Z} \to 0$, which is the same "split into elementary complexes" move used in the universal coefficient proof.

4. **$Sq^1 = \beta$ and the Steenrod axioms.** Section 4.L gives the operations purely axiomatically (Proposition 4L.1 reduces them to classes on Eilenberg-MacLane spaces; the actual construction is deferred to the second half of the section, which I did not read). For the project, the operative facts are property (7) ($Sq^1 = \beta$) and the Adem relation $Sq^{2i+1} = \beta Sq^{2i}$: the mod-2 Bockstein is the degree-1 generator of the Steenrod algebra, and it is stable under suspension. The Cartan formula and the explicit $Sq^i(\alpha^n) = \binom{n}{i}\alpha^{n+i}$ for degree-1 classes (printed p. 490, formula $*$) make these operations computable from binomial coefficients mod 2 (the mod-2 Pascal triangle, p. 491).

## Relevance to this project

The strand-3 dossier specifies the "missing object" as a quantity that a fast #SAT-style algorithm could compute but that does NOT algebrize, and it names a candidate: a mod-2 torsion "Bockstein bridge." Every rational trace, rank, determinant, or volume invariant algebrizes (these are the low-degree polynomial extensions the algebrization barrier of Aaronson-Wigderson 2008 captures). The dossier's bet is that a $\mathbb{Z}_2$-torsion invariant, something visible only after reducing mod 2 and applying a Bockstein, lives outside the algebrizing world because it is not a value of a low-degree polynomial over a field. This book is the source of the exact tools that invariant is written in:

- The universal coefficient theorem (Section 3.1, Theorem 3.2, Corollary 3.3) gives the precise statement that **field coefficients erase torsion** ($H^n(X;F) \cong \mathrm{Hom}(H_n(X;F), F)$, no Ext term, printed pp. 198-199), while integer coefficients see it via $\mathrm{Ext}(H_{n-1}, \mathbb{Z}) \cong$ torsion of $H_{n-1}$. This is the topological analog of the project's claim that polynomial-over-a-field invariants algebrize but a $\mathbb{Z}_2$-torsion quantity might not. The "torsion shifts up one dimension" phenomenon is the structural reason a mod-2 class can carry information no rational invariant does.

- The Bockstein $\beta$ / $\tilde\beta$ (Section 3.E) is literally the named operator in "Bockstein bridge." Hatcher's framing, that $\beta$ "recovers $\mathbb{Z}$ coefficient information from $\mathbb{Z}_p$ coefficients" (printed p. 303), is the exact functionality the project wants: a bridge from mod-2 data back to integral torsion. Corollary 3E.4 (the $\beta$-image equals the $p$-torsion) is the cleanest formalization of "this operator detects torsion."

- The identity $Sq^1 = \beta$ (Section 4.L, property 7, printed p. 489) connects the Bockstein to the Steenrod algebra. If the missing object is to be a stable, naturally-defined, suspension-invariant invariant (the kind a uniform fast algorithm could plausibly compute uniformly across input sizes), then it being a Steenrod operation, and specifically $Sq^1$, is the structural home Hatcher provides. The stability of $Sq^1$ (printed p. 489), in contrast to the non-stable cup square, is the property that would let such an invariant be defined coherently across a family of instances rather than instance-by-instance.

Note carefully what this source does and does not say. It is pure algebraic topology. It contains zero complexity theory: no circuits, no SAT, no algebrization, no mention of P vs NP. The connection to the dossier is entirely on the project's side: the dossier proposes to import these mod-2 torsion tools into a complexity setting. This book supplies the tools and their exact properties; it does not supply, and cannot supply, the bridge to complexity. That bridge is unbuilt and is the strand's open problem.

## What this enables / what remains open

Mapping to the research directions and the LEARNINGS findings:

- **Direction 02 (natural-proofs evasion / the MCSP crux) and the missing-object program (LEARNINGS finding 9, "the missing object is a non-algebrizing fast-computable invariant").** This book pins down the candidate's algebraic identity. The missing object, if it is the Bockstein bridge, is some complexity-theoretic shadow of $\beta : H^n(X;\mathbb{Z}_2) \to H^{n+1}(X;\mathbb{Z}_2)$ / its integral lift $\tilde\beta$, equivalently $Sq^1$. The two structural facts this source nails down for that program: (a) the invariant must be torsion-valued, because the universal coefficient theorem shows field-coefficient (hence rational, hence plausibly algebrizing) invariants lose exactly torsion; (b) the invariant should be stable / natural, because $Sq^1 = \beta$ is a stable cohomology operation and that is what makes it definable uniformly.

- **The TC0 hinge (Direction 01, LEARNINGS finding 1 "barriers compose").** Not addressed by this source, but the dossier's geometry is relevant: the polynomial method dies at $\mathsf{TC}^0$ because MAJORITY has approximate degree $\Theta(\sqrt{n})$, i.e. it is not low-degree over a field. The mod-2 Bockstein lives precisely in the regime where field-polynomial methods fail (torsion, not rank). Whether a Bockstein-style invariant is the non-algebrizing object that survives the $\mathsf{TC}^0$ hinge is the open question; this book gives no evidence either way, it only certifies that the torsion tools exist and are well-behaved.

- **The implied fourth barrier (LEARNINGS finding 10, "bounded-interface reconstruction").** The non-naturality of the universal-coefficient splitting (printed p. 196) is a suggestive structural caution: torsion cannot be canonically separated from free part, only detected via Ext / Bockstein. Any complexity invariant built on this would inherit that non-canonicity. Whether that is an obstruction or a feature (a source of the desired non-algebrization) is open.

Concrete open questions / cruxes this source exposes:

1. **What is the complexity-theoretic object whose cohomology one is taking?** Hatcher's $\beta$, $Sq^1$, and Ext act on the (co)homology of a topological space $X$. The strand has no specified space. The crux is to define a space (or simplicial / $\Delta$-complex, or chain complex over $\mathbb{Z}$) attached to a SAT instance or a circuit such that its mod-2 torsion is (i) computable by a fast #SAT-style algorithm and (ii) a hardness witness. Nothing in this book does that; it is the unbuilt bridge.

2. **Does a Bockstein-valued invariant actually evade algebrization?** The dossier asserts every rational trace/rank/volume invariant algebrizes and bets that $\mathbb{Z}_2$-torsion does not. This book gives the precise sense in which torsion is invisible to field coefficients (Section 3.1), which is necessary but not sufficient. Proving non-algebrization of a torsion invariant requires the algebrization framework (Aaronson-Wigderson), which this source does not touch. This is a question for ADVERSARY to run through the barrier checker once a candidate invariant is named.

3. **Stability vs uniformity.** $Sq^1 = \beta$ is stable under suspension (printed p. 489). If a complexity invariant is to be defined coherently across all input sizes (uniformity), the suspension-stability of $Sq^1$ is the natural model. Open: is there a sequence of spaces $\{X_n\}$ indexed by problem size whose $Sq^1$ / Bockstein data assembles into a uniform hard invariant, and is that assembly itself fast-computable?

4. **Higher torsion vs primitive torsion.** Proposition 3E.3 distinguishes order-$p$ torsion (which $\beta$ detects and $BH^*$ strips) from order-$p^k$ torsion ($k>1$, which $\beta$ leaves in $BH^*$). If the missing object is order-2 torsion specifically, $\beta = Sq^1$ is the right operator; if higher 2-power torsion is wanted, one needs the higher Bocksteins (mentioned at p. 305 and in Exercise 3 of Section 3.E, which I did not work through). Which torsion the strand actually needs is unspecified and is a crux for BUILDER.

What this source does NOT enable: it gives no lower bound, no algorithm, and no complexity-theoretic statement of any kind. It is the algebraic dictionary for the strand-3 vocabulary, read at the level needed to state the candidate object precisely. The map from this vocabulary to a P-vs-NP-relevant invariant remains entirely open and is the substance of the strand.
