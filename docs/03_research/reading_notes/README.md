# Reading notes

Section-by-section notes on the reference library, as they are produced. The
bibliography itself is tracked in [`references/README.md`](../../../references/README.md);
the PDFs are gitignored (copyrighted).

## Convention

Each note file is named for its source and ends with a "What this enables / what
remains open" section mapping the source to the research directions
([`../research_directions/`](../research_directions/)) and the cross-architecture
findings ([`experiments/LEARNINGS.md`](../../../experiments/LEARNINGS.md)).

## Priority reading order

For a prioritized, strand-by-strand reading guide tied to the dossier's leading
path (with entry points and access tags), see
[`../resources_for_the_leading_path.md`](../resources_for_the_leading_path.md).
The short version, for the live front (the circuit-lower-bound architecture via
the Williams template):

1. Arora-Barak, *Computational Complexity*, chapters on circuit complexity and
   the barriers (the textbook substrate).
2. Razborov-Rudich, *Natural Proofs* (the central barrier for circuit lower
   bounds).
3. Williams, *Improving exhaustive search implies superpolynomial lower bounds*
   and *Non-uniform ACC circuit lower bounds* (the frontier technique).
4. Aaronson-Wigderson, *Algebrization* (the third barrier, and why
   arithmetization is not enough).

## Notes index (31 sources, June 2026)

Thorough grounded notes on every freely-downloaded source, organized by topic.
Each note cites sections/pages and ends with the "what this enables / what
remains open" mapping. The reading pass also corrected a propagated error
(MAJORITY's approximate degree is $\Theta(n)$, not $\Theta(\sqrt{n})$; see
LEARNINGS finding 11).

### Meta-complexity (the leading path)

- [Allender 2020](meta_complexity/allender_2020_circuit_minimization.md): map of MCSP/meta-complexity; Table 1 of separations from MCSP hardness; magnification and Hirahara W2A as the live frontier.
- [Liu-Pass 2020](meta_complexity/liu_pass_2020_owf_kolmogorov.md): OWFs exist iff $Kt$ is mildly average-case hard; the first natural meta-complexity problem characterizing private-key crypto.
- [Kabanets-Cai 2000](meta_complexity/kabanets_cai_2000_mcsp.md): names MCSP; proves the natural-proofs link (MCSP in P/poly implies no strong PRG).
- [Hirahara 2018](meta_complexity/hirahara_2018_w2a_within_np.md): non-black-box W2A within NP; honestly flags that it still relativizes (Section 1.7), so the non-relativizing demand falls on the open NP-hardness step.
- [Hirahara 2023](meta_complexity/hirahara_2023_capturing_owf.md): assuming NP not in i.o.P/poly, OWF exists iff approximating $dK^{poly}$ is NP-hard.
- [Hirahara 2022](meta_complexity/hirahara_2022_learning_partial_mcsp.md): first non-relativizing NP-hardness of learning programs and partial MCSP variants.
- [Santhanam 2020](meta_complexity/santhanam_2020_pseudorandomness_mcsp.md): natural proofs are zero-error average-case MCSP algorithms; MCSP average-case hardness equals succinct pseudorandomness.

### Approximate degree and the $\mathsf{TC}^0$ hinge

- [Bun-Thaler 2022 survey](approx_degree_tc0/bun_thaler_2022_approx_degree_survey.md): the analytic statement of the hinge; dual polynomials; the LTF-of-LTF UPP wall one rung short of $\mathsf{TC}^0$.
- [Paturi 1992](approx_degree_tc0/paturi_1992_symmetric_approx_degree.md): exact approximate degree of symmetric functions; MAJORITY (central jump) is $\Theta(n)$, OR/AND (endpoint) $\Theta(\sqrt{n})$.
- [O'Donnell 2014](approx_degree_tc0/odonnell_2014_analysis_of_boolean_functions.md): the L2 Fourier vocabulary; supplies the L2 shadow, not the L-infinity approximate-degree theorem.
- [Sherstov 2011](approx_degree_tc0/sherstov_2011_pattern_matrix.md): the pattern matrix method lifts degree obstructions to communication / approximate-rank bounds; all rational and algebrizing.
- [Bun-Thaler 2017](approx_degree_tc0/bun_thaler_2017_ac0_approx_degree.md): $\mathsf{AC}^0$ has approximate degree $n^{1-\delta}$, so the wall is the threshold layer, not $\mathsf{AC}^0$.
- [Bun-Thaler 2016](approx_degree_tc0/bun_thaler_2016_dual_polynomials.md): explicit dual witnesses for Collision / Element Distinctness; the concrete primal-dual obstruction objects.
- [Kumar 2023](approx_degree_tc0/kumar_2023_ac0_to_tc0_correlation.md): a graded gate family dialing $\mathsf{AC}^0$ up to $\mathsf{TC}^0$; maps the terrain just below the MAJORITY wall.
- [Kane-Williams 2016](approx_degree_tc0/kane_williams_2016_threshold_lower_bounds.md): first super-linear gate / super-quadratic wire bounds for depth-2/3 threshold circuits.

### The algorithmic method (the Williams spine)

- [Williams 2015](williams_method/williams_2015_thinking_algorithmically.md): the manifesto; sub-$2^n$ Circuit SAT implies a circuit lower bound.
- [Murray-Williams 2018](williams_method/murray_williams_2018_easy_witness_nqp.md): easy witness lemma down to NQP/NP; first step from $\mathsf{ACC}^0$ toward $\mathsf{TC}^0$ (ACC of THR).
- [Williams 2013](williams_method/williams_2013_natural_proofs_vs_derandomization.md): NEXP lower bounds equal constructive useful (not large) properties; the method is non-natural by dropping largeness.
- [Chen-Lyu-Williams 2020](williams_method/chen_lyu_williams_2020_ae_lower_bounds.md): upgrades ACC0 bounds to almost-everywhere and average-case; stops at ACC0 o THR.
- [Williams 2021](williams_method/williams_2021_lower_bounds_from_algorithm_design.md): the status check; names a fourth barrier (locality) alongside the three.

### Algebraic topology (the strand-3 missing object)

- [Hatcher 2002](algebraic_topology/hatcher_2002_algebraic_topology.md): the mod-2 torsion toolkit; UCT (3.1), Bockstein (3.E), $Sq^1 = $ mod-2 Bockstein (4.L). No complexity theory: the bridge is open.
- [Miller 2013](algebraic_topology/miller_2013_evasiveness_topological_fixed_point.md): the worked precedent (Kahn-Saks-Sturtevant evasiveness), where $\mathbb{F}_p$ torsion (not rational homology) carries the lower bound.
- [Bjorner 1995](algebraic_topology/bjorner_1995_topological_methods.md): the map separating rational/algebrizing invariants from torsion-sensitive ones.

### GCT and representation theory

- [Burgisser 2015](gct_rep_theory/burgisser_2015_permanent_determinant_kronecker.md): the occurrence-obstruction program and its 2016 collapse; multiplicity version left open.
- [Dorfler-Ikenmeyer-Panova 2019](gct_rep_theory/dorfler_ikenmeyer_panova_2019_multiplicity_obstructions.md): first proof multiplicity obstructions strictly beat occurrence obstructions.
- [Grochow 2015](gct_rep_theory/grochow_2015_unifying_lower_bounds_gct.md): classical lower bounds are GCT rank/minor/degree functionals (hence algebrize); the multiplicity obstruction is the candidate non-algebrizing one.

### Proof complexity and bounded arithmetic

- [Razborov 1995](proof_complexity/razborov_1995_unprovability_circuit_lower_bounds.md): under a strong PRG, $S_2^2$ cannot refute "SAT has small circuits"; natural proofs as an arithmetic unprovability theorem.
- [Goos-Pitassi-Watson 2017](proof_complexity/goos_pitassi_watson_2017_lifting_bpp.md): query-to-communication lifting for BPP; the engine behind modern proof-complexity bounds.

### Statistical physics of computation

- [Gamarnik 2021](stat_physics/gamarnik_2021_overlap_gap_property.md): the OGP bounds algorithm classes, is itself large+constructive (natural), and proves no worst-case hardness.
- [Mertens-Mezard-Zecchina 2006](stat_physics/mertens_mezard_zecchina_2006_ksat_thresholds.md): the 1RSB cavity computation of $\alpha_c(3) \approx 4.267$; average-case heuristic physics.
- [Achlioptas-Coja-Oghlan-Ricci-Tersenghi 2011](stat_physics/achlioptas_cojaoghlan_riccitersenghi_2011_solution_space_geometry.md): random k-SAT solution spaces shatter into exponentially many frozen clusters; the substrate a topological invariant would be built on.
