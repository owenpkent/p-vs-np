# Graduate level: circuit classes, the barriers, and the structure of the question

Prerequisites: algorithms, computability, a first course in complexity theory
(Turing machines, $\mathsf{P}$, $\mathsf{NP}$, reductions). Standard references:
Arora-Barak, *Computational Complexity: A Modern Approach*; Sipser,
*Introduction to the Theory of Computation*.

## Why circuits

A Boolean circuit on $n$ inputs is a directed acyclic graph of AND/OR/NOT gates
computing a function $\{0,1\}^n \to \{0,1\}$. A *family* $\{C_n\}$ has one circuit
per input length. The class $\mathsf{P/poly}$ is the languages decided by
polynomial-size circuit families (equivalently, $\mathsf{P}$ with polynomial
advice). Crucially:

$$\mathsf{P} \subseteq \mathsf{P/poly}.$$

So to prove $\mathsf{P} \ne \mathsf{NP}$ it suffices to prove the stronger
statement $\mathsf{NP} \not\subseteq \mathsf{P/poly}$: that some NP problem has no
polynomial-size circuits. This is the **circuit lower bound** program. It is
attractive because circuits are concrete combinatorial objects, and because a
non-uniform lower bound sidesteps subtleties about uniform machine models. The
Karp-Lipton theorem (1980) adds motivation: if
$\mathsf{NP} \subseteq \mathsf{P/poly}$ then the polynomial hierarchy collapses to
its second level, which is considered unlikely.

## Restricted circuit classes and their lower bounds

Unconditional lower bounds are known against weak circuit classes:

- **$\mathsf{AC}^0$** (constant depth, unbounded fan-in AND/OR/NOT, polynomial
  size): PARITY $\notin \mathsf{AC}^0$ (Furst-Saxe-Sipser 1981; Ajtai 1983;
  optimal size bound $2^{\Omega(n^{1/(d-1)})}$ at depth $d$ via Hastad's switching
  lemma, 1986). See the [parity restriction experiment](../../experiments/circuit_complexity/).
- **$\mathsf{AC}^0[p]$** ($\mathsf{AC}^0$ with $\mathrm{MOD}_p$ gates, $p$ prime):
  MAJORITY and $\mathrm{MOD}_q$ (for $q$ not a power of $p$) need exponential size
  (Razborov 1987; Smolensky 1987), via the polynomial method.
- **Monotone circuits** (AND/OR only): CLIQUE needs exponential-size monotone
  circuits (Razborov 1985; Alon-Boppana 1987).
- **$\mathsf{ACC}^0$** ($\mathsf{AC}^0$ with $\mathrm{MOD}_m$ gates, $m$
  composite): $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$ (Williams 2011). This
  is the current frontier for unconditional lower bounds against a natural circuit
  class.

The wall is stark: we cannot prove a super-linear lower bound for *general*
circuits against any explicit function. The barriers explain why.

## The three barriers

These are the central structural facts of the field. Each proves that a class of
proof techniques cannot resolve P vs NP. They are this project's wrong-approach
detector (see [`experiments/_shared/`](../../experiments/_shared/)).

### Relativization (Baker-Gill-Solovay 1975)

A proof technique *relativizes* if it remains valid when all machines are given
an arbitrary oracle $O$ (a black-box subroutine). BGS exhibited:

- an oracle $A$ (any $\mathsf{PSPACE}$-complete language) with
  $\mathsf{P}^A = \mathsf{NP}^A$, and
- an oracle $B$ (built by diagonalization) with $\mathsf{P}^B \ne \mathsf{NP}^B$.

Since a relativizing technique would prove its conclusion for *all* oracles, and
$A, B$ force opposite answers, no relativizing technique decides P vs NP.
Diagonalization and simulation relativize. See the
[relativization experiment](../../experiments/relativization/).

### Natural proofs (Razborov-Rudich 1994)

A property $\Phi$ of $n$-bit Boolean functions is **natural** if it is:

- *constructive*: decidable in time $\mathrm{poly}(2^n)$ from the truth table, and
- *large*: holds for at least a $2^{-O(n)}$ fraction of all functions.

It is **useful** if every function with $\Phi$ requires super-polynomial
circuits. Razborov-Rudich: a natural useful property yields a distinguisher that
breaks pseudorandom function generators. Under the standard assumption that
strong PRGs exist (e.g. from subexponential hardness of factoring or discrete
log), no natural useful property exists. So a circuit lower bound against
$\mathsf{P/poly}$ must use a non-natural property: non-constructive, or
non-large-but-useful. See the
[natural-proofs experiment](../../experiments/natural_proofs/).

### Algebrization (Aaronson-Wigderson 2008)

Extend relativization: give machines an oracle $O$ *and* access to a low-degree
polynomial extension $\tilde O$ of $O$ over a field or ring. A technique
*algebrizes* if it goes through in this setting. Arithmetization, the technique
behind $\mathsf{IP} = \mathsf{PSPACE}$ (Shamir 1992) and $\mathsf{MIP} =
\mathsf{NEXP}$, is non-relativizing but still algebrizes. Aaronson-Wigderson
exhibit algebraic oracles forcing the answer each way, so an algebrizing
technique cannot resolve P vs NP. This sharpened the picture: escaping
relativization via arithmetization is not enough.

### Composing the three

The barriers are independent constraints. A technique must clear all three. The
checker in [`experiments/_shared/barriers.py`](../../experiments/_shared/barriers.py)
encodes this. Williams's $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$ is the
canonical example that threads all three: a non-trivial $\mathsf{ACC}^0$
satisfiability algorithm combined with a non-constructive, non-relativizing,
non-algebrizing diagonalization against $\mathsf{NEXP}$.

## The polynomial hierarchy and other context

- The **polynomial hierarchy** $\mathsf{PH} = \bigcup_k \Sigma_k^p$ generalizes
  $\mathsf{NP}$ ($= \Sigma_1^p$) by alternating quantifiers. $\mathsf{P} =
  \mathsf{NP}$ would collapse $\mathsf{PH}$ to $\mathsf{P}$.
- **Time and space hierarchy theorems** (proved by diagonalization, hence
  relativizing) give $\mathsf{P} \subsetneq \mathsf{EXP}$ and similar strict
  separations, but cannot reach P vs NP.
- **Ladner's theorem (1975)**: if $\mathsf{P} \ne \mathsf{NP}$, there are
  NP-intermediate problems, neither in $\mathsf{P}$ nor NP-complete.

## Where to go next

- [`docs/03_research/`](../03_research/): current approaches and the research
  directions.
- [`docs/research_atlas/`](../research_atlas/): the master map of architectures
  and obstructions.
