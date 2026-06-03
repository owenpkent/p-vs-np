# TODO

Task tracking for the P vs NP research repo. Checkbox format.

## Infrastructure (Phase 0)

- [x] Repo structure mirroring the companion Riemann repo
- [x] Three-barrier wrong-approach detector (`experiments/_shared/barriers.py`)
- [x] `ProofTechnique` schema + canonical technique library
- [x] Smoke test (5/5 passing)
- [x] `.gitignore`, `.gitattributes`, `requirements.txt`
- [x] Agent role specifications (six roles)
- [x] Memory stub index

## Experiments

- [x] (a) BGS relativization oracle diagonalization, runnable
- [x] (b) Random 3-SAT phase transition + hardness peak, runnable
- [x] (c) Natural-proofs largeness / constructivity check, runnable
- [x] (d) Hastad switching-lemma parity demo, runnable
- [x] (e) TC0-SAT savings model: the Williams-program hinge + savings-mirage
      numeric coordinate (`circuit_complexity/e_tc0_sat_savings.py`), runnable
- [x] (f) Algebrization probe: rational-trace vs torsion invariant classifier
      (`_shared/algebrization_probe.py`), runnable
- [ ] ACC0 polynomial method (Razborov-Smolensky): MOD_2 has no low-degree
      approximation over F_3
- [ ] Resolution-width lower bound for the pigeonhole principle (Haken 1985)
- [ ] GCT permanent-vs-determinant multiplicity computation (with BIP 2016 no-go
      as the boundary)
- [ ] Nisan-Wigderson PRG demo (circuit hardness implies derandomization)
- [ ] Monotone clique lower bound (Razborov 1985) in miniature

## Documentation

- [x] `docs/00_intuitive/` (verifying vs finding)
- [x] `docs/01_undergraduate/` (P, NP, reductions, Cook-Levin)
- [x] `docs/02_graduate/` (circuit classes, the three barriers, polynomial hierarchy)
- [x] `docs/03_research/` overview + numbered research directions
- [x] `docs/03_research/reading_notes/` README
- [x] `docs/implications/` (crypto, optimization, science, AI)
- [x] `docs/solutions/` (known approaches and why each is stuck)
- [x] `docs/research_atlas/` (master map of all architectures + obstructions)
- [x] `docs/researcher_mindset.md`
- [x] `docs/03_research/2050_backward_induction.md` (backward-induction dossier:
      nine 2050 resolution paths, adversary-tested, ranked; leading path, the TC0
      hinge, the braided path, the implied fourth barrier)
- [ ] Expand intuitive docs with worked NP-completeness examples
- [ ] Add a graduate doc on interactive proofs / arithmetization (the
      algebrization story)

## Lean

- [x] `lakefile.lean`, `lean-toolchain` (match the companion repo)
- [x] `PvsNP.lean` main module + skeleton sub-modules
- [x] Typed statements with documented `sorry` (P, NP, SAT, Cook-Levin, BGS,
      circuit lower bounds, the P_neq_NP goal)
- [ ] Wire to any Mathlib complexity-theory definitions that exist
- [ ] Replace placeholder predicates with real statements where Mathlib allows
- [ ] Get a green `lake build` (currently a skeleton; not required)

## References and visualizations

- [x] `references/README.md` bibliography of real papers and books
- [x] `sources/README.md`
- [x] `visualizations/README.md` + one manim scene (SAT phase transition)
- [ ] manim scene for the relativization diagonalization
- [ ] manim scene for the switching lemma / random restriction

## Stretch

- [ ] Multi-agent orchestration loop wired to the barrier-checker gate
- [ ] A second independent code path for each experiment (verification layer 1)
- [ ] Survey of post-2020 fine-grained complexity (SETH-based hardness)
