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
