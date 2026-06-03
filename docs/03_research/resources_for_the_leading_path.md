# Resources for the leading path: a prioritized reading guide

> What to read, and in what order, to actually work on the leading path of the
> [2050 backward-induction dossier](2050_backward_induction.md): meta-complexity
> riding the Williams algorithm-to-lower-bound spine, gated by the $\mathsf{TC}^0$
> hinge, with a cross-disciplinary missing object (a non-algebrizing invariant a
> fast algorithm can compute). This is the opinionated companion to the full
> bibliography in [`references/README.md`](../../references/README.md) (sections 08
> to 16), which has every entry with links and access tags. Here we give the
> entry points and the order. Access tags: *(free)* readable now, *(book)*
> purchase or library.

## Why these and not the canon

The repo's core bibliography (Arora-Barak, the barrier papers, the classic
circuit bounds) is the substrate, and you should have it. But the dossier's
findings point past the canon into areas it does not cover: meta-complexity,
approximate degree, the algorithmic method in depth, and (the genuinely new need)
algebraic topology and representation theory. The guide below is organized by the
dossier's strands, not by field, so each block answers "what do I read to make
progress on this specific part of the proof."

## If you read only five things

1. [Allender, *The New Complexity Landscape Around Circuit Minimization*](https://people.cs.rutgers.edu/~allender/papers/lata.pdf) *(free)*. The fastest map into meta-complexity, the leading path.
2. [Williams, *Algorithms for Circuits and Circuits for Algorithms* (ICM 2014)](https://people.csail.mit.edu/rrw/projects.html) *(free)*. The authoritative survey of the spine the whole path rides.
3. [Bun & Thaler, *Approximate Degree in Classical and Quantum Computing*](https://people.cs.georgetown.edu/jthaler/adegFnT.pdf) *(free)*. Why the $\mathsf{TC}^0$ hinge is a wall: MAJORITY has approximate degree $\Theta(\sqrt{n})$.
4. [Chen & Williams, *Stronger Connections ... via PCPs of Proximity* (CCC 2019)](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2019.19) *(free)*. The method working at the $\mathsf{TC}^0$ frontier, the most leveraged open step.
5. [Hatcher, *Algebraic Topology*](https://pi.math.cornell.edu/~hatcher/AT/ATpage.html) *(free)*, sections 3.1 and 3.E. The mod-2 machinery (Bockstein, Steenrod squares) the missing object is specified in.

The first four are complexity theory. The fifth is the tell: the leading path now
needs a tool from outside the field.

## Strand by strand

### The Williams spine (the non-relativizing, non-algebrizing engine)

This is the one component no adversary in the dossier could disqualify. Read in order:

1. [Williams, *Thinking Algorithmically About Impossibility* (CSL 2015)](https://drops.dagstuhl.de/storage/00lipics/lipics-vol041-csl2015/LIPIcs.CSL.2015.14/LIPIcs.CSL.2015.14.pdf) *(free)*: the thesis in cleanest form.
2. [Williams, *Algorithms for Circuits and Circuits for Algorithms* (ICM 2014)](https://people.csail.mit.edu/rrw/projects.html) *(free)*: the full survey up through ACC0.
3. [Williams, *Complexity Lower Bounds from Algorithm Design* (LICS 2021)](https://people.csail.mit.edu/rrw/LICS21.pdf) *(free)*: the current status and open frontier.
4. The base results are already in [`references/README.md`](../../references/README.md) section 03 (Williams ACC0; "Improving exhaustive search"). For the climb past ACC0, read [Murray & Williams (STOC 2018)](https://people.csail.mit.edu/rrw/easy-witness-nqp.pdf) and [Chen, Lyu & Williams (FOCS 2020)](https://people.eecs.berkeley.edu/~xinlyu/document/ae-lowerbounds.pdf), both *(free)*.

Full list: [`references/README.md`](../../references/README.md) section 10. See also
research direction [01](research_directions/01_circuit_lower_bounds.md).

### The $\mathsf{TC}^0$ hinge (approximate degree)

The single most-leveraged milestone. The polynomial method that beat ACC0 dies at
threshold gates. Read:

1. [Bun & Thaler survey](https://people.cs.georgetown.edu/jthaler/adegFnT.pdf) *(free)*: the modern, definitive treatment.
2. [Paturi (STOC 1992)](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/Paturi_1992_stoc.pdf) *(free)*: the source of the exact $\Theta(\sqrt{n})$ for MAJORITY.
3. [Chen & Williams (CCC 2019)](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2019.19) *(free)*: the algorithmic method aimed straight at the $\mathsf{TC}^0$ frontier.
4. [Kumar (CCC 2023)](https://arxiv.org/abs/2304.02770) *(free)*: the terrain between $\mathsf{AC}^0$ and $\mathsf{TC}^0$.
5. Prerequisite vocabulary: [O'Donnell, *Analysis of Boolean Functions*](https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf) *(free)*.

This hinge is modeled in
[`experiments/circuit_complexity/e_tc0_sat_savings.py`](../../experiments/circuit_complexity/e_tc0_sat_savings.py).
Full list: [`references/README.md`](../../references/README.md) section 09.

### The meta-complexity device (the leading path)

The non-natural device, via a proved (not assumed) non-constructivity of "high
$Kt$." Read:

1. [Allender survey](https://people.cs.rutgers.edu/~allender/papers/lata.pdf) *(free)*: the map.
2. [Hirahara, *Meta-Computational Average-Case Complexity* (BEATCS 2022)](http://bulletin.eatcs.org/index.php/beatcs/article/view/688) *(free)*: the worst-case-to-average-case program.
3. [Hirahara, *Non-Black-Box W2A Reductions within NP* (FOCS 2018)](https://eccc.weizmann.ac.il/report/2018/138/) *(free)*: the origin, and the non-relativizing move.
4. [Liu & Pass (FOCS 2020)](https://arxiv.org/abs/2009.11514) *(free)*: OWF iff $Kt$ mildly average-case hard.
5. [Hirahara, *Capturing OWFs via NP-Hardness of Meta-Complexity* (STOC 2023)](https://eccc.weizmann.ac.il/report/2023/037/) *(free)*: worst-case hardness of the device.
6. Lecture-grade: the [Simons Meta-Complexity Boot Camp (2023) videos](https://simons.berkeley.edu/workshops/meta-complexity-boot-camp/videos) *(free)*.

Full list: [`references/README.md`](../../references/README.md) section 08. See also
research direction [02](research_directions/02_natural_proofs_evasion.md).

### The strand-3 missing object (algebraic topology, the new need)

This is the part of the dossier with no resources in the existing bibliography,
because it reaches outside complexity theory. The braid needs a quantity a fast
algorithm computes that does NOT algebrize. Every rational trace/rank/volume
invariant algebrizes; the candidate content is mod-2 torsion. The probe in
[`experiments/_shared/algebrization_probe.py`](../../experiments/_shared/algebrization_probe.py)
is the filter. Read, roughly in order of how directly each bears on the Bockstein
bridge:

1. [Hatcher, *Algebraic Topology*](https://pi.math.cornell.edu/~hatcher/AT/ATpage.html) *(free)*: section 3.1 (universal coefficients, where the Bockstein appears) and 3.E (Steenrod squares).
2. [Miller, *Evasiveness of Graph Properties and Topological Fixed-Point Theorems*](https://arxiv.org/abs/1306.0110) *(free)*: the cleanest existing case of topology forcing a complexity lower bound (Kahn-Saks-Sturtevant). The template to study first.
3. [Bjorner, *Topological Methods*](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/bjorner2.pdf) *(free)*: which invariants of a combinatorial complex are computable, and which carry torsion.
4. Matousek, *Using the Borsuk-Ulam Theorem* *(book)*: the $\mathbb{Z}/2$-index bridge from topology to combinatorial lower bounds.
5. For the torsion machinery in depth: Mosher & Tangora, *Cohomology Operations* *(book)*, or Steenrod & Epstein *(book)*.
6. For the strand-1 requirement (cheap to compute): Edelsbrunner & Harer, *Computational Topology* *(book)*, and Kozlov, *Organized Collapse* (discrete Morse theory) *(book)*.

Full list: [`references/README.md`](../../references/README.md) section 11. This is
the highest-risk, highest-novelty block; the dossier itself flags the Bockstein
bridge as not existing yet.

### GCT and representation theory

For the GCT architecture and the multiplicity-obstruction sign coordinate:

1. [Ikenmeyer lecture notes](https://www.dcs.warwick.ac.uk/~u2270030/teaching_sb/summer18/firstintrotogct/index.html) *(free)*: the gentlest on-ramp.
2. Landsberg, *Geometry and Complexity Theory* *(book)*: the monograph.
3. [Dorfler, Ikenmeyer & Panova (ICALP 2019)](https://arxiv.org/abs/1901.04576) *(free)*: multiplicity vs occurrence obstructions, the live successor to BIP 2016.
4. [Shpilka & Yehudayoff, *Arithmetic Circuits*](https://www.cs.tau.ac.il/~shpilka/publications/SY10.pdf) *(free)*: which measures algebrize (the rational functionals strand 3 must avoid).
5. Background: Fulton & Harris, *Representation Theory* *(book)*; Sagan, *The Symmetric Group* *(book)*.

Full list: [`references/README.md`](../../references/README.md) section 12. See also
research direction [04](research_directions/04_geometric_complexity_theory.md).

### Proof complexity, bounded arithmetic, and the independence path

For the A6 independence path and the implied fourth barrier:

1. [Cook & Nguyen, *Logical Foundations of Proof Complexity*](https://www.cs.toronto.edu/~sacook/homepage/book/) *(draft free)*: the bounded-arithmetic / proof-system dictionary.
2. [Razborov, *Unprovability of Lower Bounds ... in Fragments of Bounded Arithmetic* (1995)](https://www.karlin.mff.cuni.cz/~krajicek/razborov95.pdf) *(free)*: the A6 path instantiated.
3. [Goos, Pitassi & Watson, *Query-to-Communication Lifting for BPP*](https://arxiv.org/abs/1703.07666) *(free)*: the lifting engine behind modern proof-complexity bounds.

Full list: [`references/README.md`](../../references/README.md) section 13.

### Statistical physics of computation

For the A7 physics-native path and the SAT-phase-transition experiment:

1. Moore & Mertens, *The Nature of Computation* *(book)*: the intuition-first bridge.
2. [Gamarnik, *The Overlap Gap Property* survey](https://arxiv.org/abs/2109.14409) *(free)*: why the overlap-gap statistic is natural and where it does not bound hardness.
3. Mezard & Montanari, *Information, Physics, and Computation* *(book)*: the rigorous-physics reference.

Full list: [`references/README.md`](../../references/README.md) section 14.

### Formalization and living resources

For the VERIFIER role, the `lean/` skeleton, and staying current:

- [*Theorem Proving in Lean 4*](https://lean-lang.org/theorem_proving_in_lean4/) and [*Mathematics in Lean*](https://leanprover-community.github.io/mathematics_in_lean/) *(free)*.
- [Williams, *Lower Bounds: Beyond the Bootcamp* (CS 294-152)](https://people.csail.mit.edu/rrw/cs294-152.html) *(free)*: lecture notes on the exact dossier spine.
- [ECCC](https://eccc.weizmann.ac.il/) and [arXiv cs.CC](https://arxiv.org/list/cs.CC/recent) *(free)*: where new results land first.

Full list: [`references/README.md`](../../references/README.md) sections 15 and 16.

## How this maps to the 2026 next moves

The dossier's five concrete 2026 moves draw on these blocks directly: the
$\mathsf{TC}^0$ hinge experiment (section 09 above), the meta-complexity
non-natural device (section 08), the algebrization probe and the strand-3 search
(section 11), and the proof-complexity scoping (section 13). Read the strand you
are about to work on, not the whole list at once.
