# References library (reading list)

> Curated bibliography for the proof program. PDFs are copyrighted and
> **gitignored** (`*.pdf`); this index is tracked. Organized by role, mapped to
> the research directions in
> [`../docs/03_research/research_directions/`](../docs/03_research/research_directions/)
> and the strategic snapshot [`../STATE_OF_THE_PROGRAM.md`](../STATE_OF_THE_PROGRAM.md).

All entries are real, published works. Where a result is open, the entry says so.

## 00 Foundational texts (the substrate)

| Reference | Role |
|---|---|
| Arora & Barak, *Computational Complexity: A Modern Approach*, Cambridge 2009 | The standard graduate text. Circuit complexity, the barriers, PCP. The substrate for every direction. |
| Sipser, *Introduction to the Theory of Computation*, 3rd ed. | The standard undergraduate text. P, NP, reductions, Cook-Levin. |
| Goldreich, *Computational Complexity: A Conceptual Perspective*, Cambridge 2008 | Conceptual companion; pseudorandomness and the hardness-vs-randomness landscape. |
| Cook, *The P versus NP Problem* (official Clay Millennium Prize problem statement) | The authoritative problem statement. |

## 01 The definition of the question (Direction: foundations)

| Reference | Role |
|---|---|
| Cook, *The complexity of theorem-proving procedures*, STOC 1971 | SAT is NP-complete. The origin of the field. |
| Levin, *Universal sequential search problems*, 1973 | Independent discovery of NP-completeness. |
| Karp, *Reducibility among combinatorial problems*, 1972 | The 21 NP-complete problems; NP-completeness is pervasive. |
| Cook & Reckhow, *The relative efficiency of propositional proof systems*, JSL 1979 | NP = coNP iff a polynomially bounded proof system exists. Seeds Direction 3. |

## 02 The three barriers (the wrong-approach detector)

| Reference | Role |
|---|---|
| Baker, Gill & Solovay, *Relativizations of the P =? NP question*, SIAM J. Comput. 1975 | The relativization barrier. Oracles forcing the answer both ways. |
| Razborov & Rudich, *Natural proofs*, JCSS 1997 (STOC 1994) | The natural-proofs barrier. Large + constructive properties break PRGs. |
| Aaronson & Wigderson, *Algebrization: a new barrier in complexity theory*, ToCT 2009 (STOC 2008) | The algebrization barrier. Arithmetization is non-relativizing but still algebrizes. |

## 03 Circuit lower bounds (Direction 1)

| Reference | Role |
|---|---|
| Furst, Saxe & Sipser, *Parity, circuits, and the polynomial-time hierarchy*, 1984 | PARITY not in AC0 (first proof). |
| Hastad, *Almost optimal lower bounds for small depth circuits*, 1986 | The switching lemma; optimal AC0 size bound. Basis of `circuit_complexity/`. |
| Razborov, *Lower bounds on the monotone complexity of some Boolean functions*, 1985 | Exponential monotone lower bound for clique. |
| Razborov, 1987 and Smolensky, 1987 | AC0[p] lower bounds via the polynomial method. |
| Williams, *Nonuniform ACC circuit lower bounds*, JACM 2014 (CCC 2011) | NEXP not in ACC0. The technique that threads all three barriers. |
| Williams, *Improving exhaustive search implies superpolynomial lower bounds*, 2010 | The algorithm-to-lower-bound connection. |

## 04 Proof complexity (Direction 3)

| Reference | Role |
|---|---|
| Haken, *The intractability of resolution*, TCS 1985 | Exponential resolution lower bound for the pigeonhole principle. Direction 3 M1. |
| Ben-Sasson & Wigderson, *Short proofs are narrow*, JACM 2001 | The width-size tradeoff for resolution. |
| Ajtai, *The complexity of the pigeonhole principle*, 1994 | Bounded-depth Frege lower bound. |
| Bonet, Pitassi & Raz, *On interpolation and automatization for Frege systems*, 2000 | Feasible interpolation fails for strong systems (the proof-complexity barrier). |
| Krajicek, *Proof complexity*, Cambridge 2019 | The modern reference; bounded arithmetic connection. |

## 05 Geometric Complexity Theory (Direction 4)

| Reference | Role |
|---|---|
| Valiant, *Completeness classes in algebra*, STOC 1979 | VP, VNP; permanent vs determinant as algebraic P vs NP. |
| Mulmuley & Sohoni, *Geometric complexity theory I, II*, SIAM J. Comput. 2001, 2008 | The GCT program; obstructions in orbit-closure coordinate rings. |
| Burgisser, Ikenmeyer & Panova, *No occurrence obstructions in geometric complexity theory*, JAMS 2019 (FOCS 2016) | The no-go: occurrence obstructions cannot separate permanent from determinant. |
| Mignon & Ressayre, *A quadratic bound for the determinant and permanent problem*, 2004 | Best known determinantal-complexity lower bound for the permanent. |

## 06 Hardness vs randomness (Direction 5, the surroundings)

| Reference | Role |
|---|---|
| Nisan & Wigderson, *Hardness vs randomness*, JCSS 1994 | Circuit hardness yields pseudorandom generators / derandomization. |
| Impagliazzo & Wigderson, *P = BPP if E requires exponential circuits*, STOC 1997 | Strong derandomization from circuit lower bounds. |
| Arora, Lund, Motwani, Sudan & Szegedy, *Proof verification and the hardness of approximation problems*, JACM 1998 | The PCP theorem. |
| Kabanets & Impagliazzo, *Derandomizing polynomial identity tests means proving circuit lower bounds*, 2004 | The two programs are entangled. |

## 07 Surveys

| Reference | Role |
|---|---|
| Aaronson, *P =? NP*, in *Open Problems in Mathematics*, 2016 | The best modern survey of the whole landscape. |
| Fortnow, *The status of the P versus NP problem*, CACM 2009 | A readable status report. |
| Wigderson, *Mathematics and Computation*, Princeton 2019 | Broad context; complexity in mathematics. |

---

## Resources for the leading path (added for the 2050 dossier)

Sections 08 to 16 were added to support the leading path identified in the
speculative [2050 backward-induction dossier](../docs/03_research/2050_backward_induction.md):
meta-complexity riding the Williams spine, gated by the $\mathsf{TC}^0$ step, with
a cross-disciplinary missing object (a non-algebrizing invariant a fast algorithm
can compute). They cover the gap areas beyond the core canon above. For a
prioritized learning order (what to read first, by strand) see the companion
[reading guide](../docs/03_research/resources_for_the_leading_path.md). Each entry
is marked by access: *(free)* readable now, *(book)* purchase/library,
*(paywalled)* journal access, *(mixed)* part free.

## 08 Meta-complexity (the leading path)

| Reference | Role |
|---|---|
| [Allender, *The New Complexity Landscape Around Circuit Minimization*, LATA 2021](https://people.cs.rutgers.edu/~allender/papers/lata.pdf) *(free)* | Annotated-bibliography survey of MCSP and meta-complexity. The fastest map in; read first. |
| [Hirahara, *Meta-Computational Average-Case Complexity*, BEATCS 2022](http://bulletin.eatcs.org/index.php/beatcs/article/view/688) *(free)* | Hirahara's own framing of the worst-case-to-average-case program via time-bounded Kolmogorov complexity. |
| [Hirahara, *Non-Black-Box Worst-Case to Average-Case Reductions within NP*, FOCS 2018](https://eccc.weizmann.ac.il/report/2018/138/) *(free)* | Origin of the W2A line; the non-black-box reduction is the non-relativizing move the dossier needs. |
| [Hirahara, *Capturing One-Way Functions via NP-Hardness of Meta-Complexity*, STOC 2023](https://eccc.weizmann.ac.il/report/2023/037/) *(free)* | OWF from a worst-case (NP-hardness) assumption on a meta-problem. Ties the device to the worst-case spine. |
| [Hirahara, *NP-Hardness of Learning Programs and Partial MCSP*, FOCS 2022](https://eccc.weizmann.ac.il/report/2022/119/) *(free)* | The strongest worst-case-hardness foothold for meta-complexity. |
| [Liu & Pass, *On One-Way Functions and Kolmogorov Complexity*, FOCS 2020](https://arxiv.org/abs/2009.11514) *(free)* | OWF existence iff $Kt$ is mildly average-case hard. Anchors the strand-1 claim that a cheap count captures crypto hardness. |
| [Santhanam, *Pseudorandomness and the Minimum Circuit Size Problem*, ITCS 2020](https://eccc.weizmann.ac.il/report/2019/155/) *(free)* | Connects MCSP average-case hardness, pseudorandomness, and OWFs; why meta-complexity may evade natural proofs. |
| [Kabanets & Cai, *Circuit Minimization Problem*, STOC 2000](https://www2.cs.sfu.ca/~kabanets/papers/mincircuit.pdf) *(free)* | Defined MCSP as a complexity object. The historical prerequisite. |
| Li & Vitanyi, *An Introduction to Kolmogorov Complexity and Its Applications*, 4th ed., Springer 2019 *(book)* | The canonical reference grounding the time-bounded variants ($Kt$, $rKt$, $pKt$). |
| [Simons Institute, *Meta-Complexity Boot Camp* (video archive), 2023](https://simons.berkeley.edu/workshops/meta-complexity-boot-camp/videos) *(free)* | Lecture-grade onramp: intro, Kolmogorov complexity, hardness of meta-complexity, crypto. |
| [Simons Institute, *Meta-Complexity Program* (hub + workshops), 2023](https://simons.berkeley.edu/programs/Meta-Complexity2023) *(free)* | The broadest verified set of current talks and open-problem lists for the leading path. |

## 09 Approximate degree and the $\mathsf{TC}^0$ hinge

| Reference | Role |
|---|---|
| [Bun & Thaler, *Approximate Degree in Classical and Quantum Computing*, FnT 2022](https://people.cs.georgetown.edu/jthaler/adegFnT.pdf) *(free)* | The definitive survey. Why MAJORITY's $\Theta(n)$ approximate degree (no low-degree approximant) is the wall where the polynomial method dies at $\mathsf{TC}^0$. |
| [Paturi, *On the Degree of Polynomials that Approximate Symmetric Boolean Functions*, STOC 1992](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/Paturi_1992_stoc.pdf) *(free)* | Source of the exact approximate degree of every symmetric function: MAJORITY (central jump) needs $\Theta(n)$, OR/AND (endpoint jump) only $\Theta(\sqrt{n})$. The MAJORITY bound defines the hinge. |
| Nisan & Szegedy, *On the Degree of Boolean Functions as Real Polynomials*, 1994 *(paywalled)* | Exact and approximate degree are polynomially related to decision-tree complexity. |
| [O'Donnell, *Analysis of Boolean Functions*, Cambridge 2014](https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf) *(free)* | The prerequisite vocabulary (degree, influence, noise sensitivity) for any approximate-degree result. |
| Jukna, *Boolean Function Complexity: Advances and Frontiers*, Springer 2012 *(book)* | Comprehensive circuit-complexity reference; locates the $\mathsf{TC}^0$ hinge in the broader landscape. |
| [Sherstov, *The Pattern Matrix Method*, 2011](https://arxiv.org/abs/0906.4291) *(free)* | Approximate degree (via dual polynomials) lifts to communication and approximate-rank lower bounds. |
| [Bun & Thaler, *A Nearly Optimal Lower Bound on the Approximate Degree of $\mathsf{AC}^0$*, FOCS 2017](https://people.cs.georgetown.edu/jthaler/ThalerAdegAC0.pdf) *(free)* | $\mathsf{AC}^0$ contains functions of approximate degree $n^{1-\delta}$; motivates why $\mathsf{TC}^0$ is the genuine obstruction. |
| [Bun & Thaler, *Dual Polynomials for Collision and Element Distinctness*, 2016](https://arxiv.org/abs/1503.07261) *(free)* | Explicit dual witnesses certifying approximate-degree lower bounds (the primal-dual object a builder needs). |
| Hajnal, Maass, Pudlak, Szegedy & Turan, *Threshold Circuits of Bounded Depth*, 1993 *(paywalled)* | The depth-2 vs depth-3 threshold separation; shows how thin $\mathsf{TC}^0$ knowledge is above depth 2. |
| [Kumar, *Tight Correlation Bounds for Circuits Between $\mathsf{AC}^0$ and $\mathsf{TC}^0$*, CCC 2023](https://arxiv.org/abs/2304.02770) *(free)* | A graded gate family interpolating $\mathsf{AC}^0$ to $\mathsf{TC}^0$; maps the terrain just below the MAJORITY wall. |
| [Kane & Williams, *Super-Linear Gate and Super-Quadratic Wire Lower Bounds for Depth-Two and Depth-Three Threshold Circuits*, STOC 2016](https://arxiv.org/abs/1511.07860) *(free)* | The strongest unconditional lower bounds at the depth-2/3 threshold frontier the leading path must cross. |

## 10 The algorithmic method in depth (the Williams spine)

Base results (Williams ACC0 and the algorithm-to-lower-bound connection) are in
section 03. The entries here extend the method toward $\mathsf{TC}^0$ and $\mathsf{NP}$.

| Reference | Role |
|---|---|
| [Williams, *Thinking Algorithmically About Impossibility*, CSL 2015](https://drops.dagstuhl.de/storage/00lipics/lipics-vol041-csl2015/LIPIcs.CSL.2015.14/LIPIcs.CSL.2015.14.pdf) *(free)* | The cleanest statement of the thesis: treat a lower-bound problem as algorithm design on the circuit class. |
| [Williams, *Algorithms for Circuits and Circuits for Algorithms*, ICM/CCC 2014](https://people.csail.mit.edu/rrw/projects.html) *(free)* | The authoritative survey of the full algorithmic method up through ACC0. The canonical map. |
| [Murray & Williams, *Circuit Lower Bounds for Nondeterministic Quasi-Polytime: an Easy Witness Lemma for NP and NQP*, STOC 2018](https://people.csail.mit.edu/rrw/easy-witness-nqp.pdf) *(free)* | Pushes the hard class from NEXP to NQP and extends to ACC0 with one threshold layer (ACC of THR): the first step toward $\mathsf{TC}^0$. |
| [Chen & Williams, *Stronger Connections Between Circuit Analysis and Circuit Lower Bounds, via PCPs of Proximity*, CCC 2019](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2019.19) *(free)* | Works directly at the $\mathsf{TC}^0$ frontier: reduces a non-trivial CAPP algorithm for THR-of-THR to a $\mathsf{TC}^0$-type lower bound. |
| [Williams, *Natural Proofs versus Derandomization*, STOC 2013](https://arxiv.org/abs/1212.1891) *(free)* | Equivalence between useful properties against $\mathsf{P/poly}$ and NEXP lower bounds; the barrier-evasion content. |
| [Chen, Lyu & Williams, *Almost-Everywhere Circuit Lower Bounds from Non-Trivial Derandomization*, FOCS 2020](https://people.eecs.berkeley.edu/~xinlyu/document/ae-lowerbounds.pdf) *(free)* | Upgrades the ACC0 bounds to almost-everywhere and average-case: the robust count a strand-1 algorithm must produce. |
| [Williams, *Complexity Lower Bounds from Algorithm Design*, LICS 2021](https://people.csail.mit.edu/rrw/LICS21.pdf) *(free)* | The most recent short retrospective of the method's reach and open frontier. Best up-to-date status check. |

## 11 Algebraic topology (the strand-3 missing object)

The dossier's missing object is a non-algebrizing invariant a fast algorithm can
compute. Every rational trace/rank/volume invariant algebrizes; the candidate
content is mod-2 torsion (Steenrod, Bockstein). This section is the cross-disciplinary
toolkit for that, which the core complexity canon does not cover.

| Reference | Role |
|---|---|
| [Hatcher, *Algebraic Topology*, Cambridge 2002](https://pi.math.cornell.edu/~hatcher/AT/ATpage.html) *(free)* | The free canonical text. Section 3.E (Steenrod squares) and 3.1 (universal coefficients / Bockstein) are the exact mod-2 machinery. |
| Mosher & Tangora, *Cohomology Operations and Applications in Homotopy Theory*, 1968 (Dover 2008) *(book)* | Constructs Steenrod squares and proves the Bockstein and Adem relations: the operations a rational functional cannot see. |
| Steenrod & Epstein, *Cohomology Operations* (Annals of Math Studies 50), Princeton 1962 *(book)* | The original axiomatic source for the Steenrod squares ($Sq^1 = $ Bockstein) and the Steenrod algebra. |
| Matousek (with Bjorner & Ziegler), *Using the Borsuk-Ulam Theorem*, Springer 2003 *(book)* | The standard bridge from topology ($\mathbb{Z}/2$ index, Borsuk-Ulam) to combinatorial lower bounds. |
| Kozlov, *Combinatorial Algebraic Topology*, Springer 2008 *(book)* | First book-length treatment; Stiefel-Whitney classes, $\mathbb{Z}/2$-space index, graph-homomorphism complexes. |
| Edelsbrunner & Harer, *Computational Topology: An Introduction*, AMS 2010 *(book)* | Topology through algorithms (simplicial homology, persistence): the strand-1 requirement that the invariant be cheaply computable. |
| Kozlov, *Organized Collapse: An Introduction to Discrete Morse Theory* (GSM 207), AMS 2020 *(book)* | Discrete Morse theory reduces a complex via acyclic matchings: how a cheap count could compute an invariant while torsion survives. |
| [Miller, *Evasiveness of Graph Properties and Topological Fixed-Point Theorems*, FnT 2013](https://arxiv.org/abs/1306.0110) *(free)* | The cleanest existing topology-forces-a-lower-bound result (Kahn-Saks-Sturtevant): the template for a topological obstruction certifying hardness. |
| [Bjorner, *Topological Methods* (Handbook of Combinatorics ch. 34), 1995](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/bjorner2.pdf) *(free)* | The canonical survey: nerve lemma, $\mathbb{Z}/2$-index, Lefschetz counting; which invariants are computable and which carry torsion. |

## 12 Representation theory and algebraic complexity (GCT depth)

| Reference | Role |
|---|---|
| Landsberg, *Geometry and Complexity Theory*, Cambridge 2017 *(book)* | The modern GCT monograph: orbit closures, coordinate rings, occurrence/multiplicity obstructions. The dossier's sign coordinate lives here. |
| Fulton & Harris, *Representation Theory: A First Course* (GTM 129), Springer 1991 *(book)* | The standard reference for $GL_n$ and $S_n$ representation theory (Schur-Weyl, Young diagrams, highest weights). |
| Fulton, *Young Tableaux* (LMS Student Texts 35), Cambridge 1997 *(book)* | Young-tableaux combinatorics, Littlewood-Richardson; to actually compute plethysm and Kronecker coefficients. |
| Sagan, *The Symmetric Group* (GTM 203), Springer 2001 *(book)* | Clean self-contained $S_n$ representation theory (Specht modules, RSK) underlying Kronecker-coefficient computations. |
| Burgisser, Clausen & Shokrollahi, *Algebraic Complexity Theory* (Grundlehren 315), Springer 1997 *(book)* | The comprehensive reference for the algebraic model ($\mathsf{VP}$, $\mathsf{VNP}$, determinantal complexity). |
| [Shpilka & Yehudayoff, *Arithmetic Circuits: A Survey*, FnT 2010](https://www.cs.tau.ac.il/~shpilka/publications/SY10.pdf) *(free)* | The trace/rank/partial-derivative measures the dossier flags as algebrizing rational functionals; makes explicit what strand 3 must avoid. |
| [Burgisser, *Permanent versus determinant, obstructions, and Kronecker coefficients*, 2015](https://arxiv.org/abs/1511.08113) *(free)* | Short authoritative survey tying GCT to the (hard) complexity of testing Kronecker-coefficient positivity. |
| [Dorfler, Ikenmeyer & Panova, *Multiplicity obstructions are stronger than occurrence obstructions*, ICALP 2019](https://arxiv.org/abs/1901.04576) *(free)* | The live successor to the BIP 2016 occurrence no-go: a setting where multiplicities separate but occurrences provably cannot. |
| [Grochow, *Unifying and generalizing known lower bounds via GCT*, 2015](https://arxiv.org/abs/1304.6333) *(free)* | Shows Nisan-Wigderson, Razborov-Smolensky, etc. sit inside the GCT frame; which measures algebrize and where a non-algebrizing one would differ. |
| [Ikenmeyer, *A first introduction to geometric complexity theory* (lecture notes), 2018](https://www.dcs.warwick.ac.uk/~u2270030/teaching_sb/summer18/firstintrotogct/index.html) *(free)* | Builds the algebraic geometry and orbit-closure machinery from scratch. The gentlest GCT on-ramp. |

## 13 Bounded arithmetic and the logic of lower bounds

Extends section 04 (proof complexity) toward the dossier's A6 independence path and
the implied fourth barrier.

| Reference | Role |
|---|---|
| [Cook & Nguyen, *Logical Foundations of Proof Complexity*, Cambridge 2010](https://www.cs.toronto.edu/~sacook/homepage/book/) *(mixed; draft free)* | The canonical bounded-arithmetic / propositional-proof-system correspondence. The formal machinery the A6 strand needs. |
| Krajicek, *Bounded Arithmetic, Propositional Logic, and Complexity Theory*, Cambridge 1995 *(book)* | The foundational text on the dictionary, witnessing theorems, and feasible interpolation. |
| Pudlak, *Logical Foundations of Mathematics and Computational Complexity*, Springer 2013 *(book)* | A reflective treatment situating the fourth-barrier "bounded-interaction interface" idea against what is formalizable in weak theories. |
| Razborov, *Bounded Arithmetic and Lower Bounds in Boolean Complexity*, 1995 *(paywalled)* | Frames whether circuit lower bounds are provable in weak arithmetic fragments: the A6 bet. |
| [Razborov, *Unprovability of Lower Bounds on Circuit Size in Certain Fragments of Bounded Arithmetic*, 1995](https://www.karlin.mff.cuni.cz/~krajicek/razborov95.pdf) *(free)* | Instantiates A6: under strong-PRG assumptions, "SAT has small circuits" is not refutable in $S_2^2$. |
| Pich, *Circuit Lower Bounds in Bounded Arithmetics*, APAL 2015 *(paywalled)* | Which circuit lower bounds are provable in PV / $V^0_1$: the "internalize Williams ACC0 and see where it stalls" move. |
| [Goos, Pitassi & Watson, *Query-to-Communication Lifting for BPP*, FOCS 2017](https://arxiv.org/abs/1703.07666) *(free)* | The canonical lifting theorem behind modern proof-complexity lower bounds; for scoping the A4 eFrege thread. |

## 14 Statistical physics of computation

For the dossier's A7 physics-native path (and the SAT-phase-transition experiment).

| Reference | Role |
|---|---|
| Mezard & Montanari, *Information, Physics, and Computation*, Oxford 2009 *(book)* | The standard text on the cavity method, replica symmetry breaking, and clustering: the rigorous-physics vocabulary of A7. |
| Moore & Mertens, *The Nature of Computation*, Oxford 2011 *(book)* | An intuition-first bridge from complexity to the statistical physics of random-SAT phase transitions. |
| [Gamarnik, *The Overlap Gap Property: a Geometric Barrier to Optimizing over Random Structures*, 2021](https://arxiv.org/abs/2109.14409) *(free)* | The authoritative OGP survey; makes precise why the overlap-gap statistic is natural and where it does not bound hardness. |
| [Mertens, Mezard & Zecchina, *Threshold Values of Random K-SAT from the Cavity Method*, 2006](https://arxiv.org/abs/cs/0309020) *(free)* | The cavity computation of the random K-SAT thresholds ($\alpha_c \approx 4.267$): substrate for the phase-transition experiment. |
| Mezard, Parisi & Zecchina, *Analytic and Algorithmic Solution of Random Satisfiability Problems*, Science 2002 *(paywalled)* | Survey propagation and the analytic 1RSB solution: when clustering geometry actually obstructs poly-time algorithms. |
| [Achlioptas, Coja-Oghlan & Ricci-Tersenghi, *On the Solution-Space Geometry of Random CSPs*, 2011](https://cgi.di.uoa.gr/~optas/papers/structure.pdf) *(free)* | Clustering/shattering geometry (components, frozen variables): what a topological invariant of a solution complex would be built on. |

## 15 Formalization (Lean / Mathlib)

For the VERIFIER role and the `lean/` skeleton.

| Reference | Role |
|---|---|
| [*Theorem Proving in Lean 4*, Lean Community](https://lean-lang.org/theorem_proving_in_lean4/) *(free)* | The canonical tutorial for the dependent-type-theory and tactic mechanics to discharge the `lean/` skeleton's `sorry` targets. |
| [*Mathematics in Lean*, Avigad & Massot](https://leanprover-community.github.io/mathematics_in_lean/) *(free)* | The Mathlib-based formalization course; the bridge from syntax to the actual library. |
| [Gaher & Kunze, *Mechanising Complexity Theory: The Cook-Levin Theorem in Coq*, ITP 2021](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2021.20) *(free)* | The closest existing full mechanization of NP-completeness of SAT: a proven blueprint for the Cook-Levin targets. |
| [lean-dojo, *LeanMillenniumPrizeProblems* (Lean 4)](https://github.com/lean-dojo/LeanMillenniumPrizeProblems) *(free)* | An external Lean 4 statement surface for P, NP, reductions, NP-completeness to diff against this project's skeleton. |

## 16 Living resources (preprints, references, courses, blogs)

| Reference | Role |
|---|---|
| [Williams, *Lower Bounds: Beyond the Bootcamp* (CS 294-152), 2018](https://people.csail.mit.edu/rrw/cs294-152.html) *(free)* | Lecture notes covering the exact dossier spine: SAT-algorithms-imply-lower-bounds, ACC0 via Beigel-Tarui, natural proofs, MCSP. |
| [O'Donnell, *15-855 Graduate Computational Complexity* (videos + notes), 2017](http://www.cs.cmu.edu/~odonnell/complexity17/) *(free)* | A full graduate video course through circuits, hardness amplification, and $\mathsf{IP} = \mathsf{PSPACE}$. |
| [ECCC: Electronic Colloquium on Computational Complexity](https://eccc.weizmann.ac.il/) *(free)* | The primary preprint repository for circuit lower bounds and meta-complexity. |
| [arXiv cs.CC](https://arxiv.org/list/cs.CC/recent) *(free)* | The living feed for new lower-bound and meta-complexity preprints. |
| [Complexity Zoo](https://complexityzoo.net/Complexity_Zoo) *(free)* | The living reference mapping containments and oracle separations among classes. |
| [Simons Institute video archive](https://simons.berkeley.edu/videos) *(free)* | Searchable talk archive at the research frontier of the leading path. |
| [Lipton & Regan, *Godel's Lost Letter and P=NP*](https://rjlipton.com/) *(free)* | Long-running expository blog on P vs NP techniques, barriers, and community vetting of claimed proofs. |
| [Fortnow & Gasarch, *Computational Complexity* (blog)](https://blog.computationalcomplexity.org/) *(free)* | The oldest TCS blog; community reaction and survey-level context. |
