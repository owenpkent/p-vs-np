# Undergraduate level: P, NP, reductions, and NP-completeness

Prerequisites: discrete math, basic algorithms, comfort with asymptotic
($O(\cdot)$) notation.

## Decision problems and languages

A decision problem asks a yes/no question about an input, for example "does this
graph have a clique of size $k$?". We encode inputs as strings, and a problem
becomes a **language** $L$: the set of strings whose answer is yes. An algorithm
*decides* $L$ if it halts on every input and accepts exactly the strings in $L$.

## The class P

$\mathsf{P}$ is the class of languages decidable by a deterministic Turing
machine in time $O(n^c)$ for some constant $c$, where $n$ is the input length.
Informally: solvable in polynomial time. Examples: shortest paths, linear
programming, primality testing (Agrawal-Kayal-Saxena 2002), matching.

## The class NP

There are two equivalent definitions, and both are worth knowing.

**Verifier definition (the useful one).** $L \in \mathsf{NP}$ if there is a
polynomial-time algorithm $V$ (the verifier) and a polynomial $p$ such that for
every input $x$:

$$x \in L \iff \exists\, w,\ |w| \le p(|x|)\ \text{and}\ V(x, w) = 1.$$

The string $w$ is a *certificate* or *witness*. So $\mathsf{NP}$ is the class of
problems whose yes-instances have short, efficiently checkable proofs.

**Nondeterministic definition (the name).** $L \in \mathsf{NP}$ if a
nondeterministic Turing machine decides it in polynomial time. The machine
guesses the witness and verifies it. "NP" stands for nondeterministic polynomial
time.

These definitions are equivalent: the guessed branch is the witness.

**P sits inside NP.** If you can decide $L$ in polynomial time, you can verify it
in polynomial time (ignore the witness and just decide). So
$\mathsf{P} \subseteq \mathsf{NP}$. The P-versus-NP question is whether this
containment is strict.

## SAT and the Boolean satisfiability problem

A Boolean formula in conjunctive normal form (CNF) is an AND of clauses, each
clause an OR of literals (variables or their negations). SAT asks: is there an
assignment of true/false to the variables making the whole formula true?

SAT is in $\mathsf{NP}$: a satisfying assignment is a witness, and checking it is
fast. 3-SAT restricts every clause to exactly three literals and is already as
hard as general SAT.

## Reductions

A **polynomial-time many-one reduction** from $A$ to $B$ (written
$A \le_p B$) is a polynomial-time computable function $f$ with
$x \in A \iff f(x) \in B$. If $A \le_p B$ and $B \in \mathsf{P}$, then
$A \in \mathsf{P}$: solve $A$ by transforming and calling $B$'s solver.
Reductions let us say "$B$ is at least as hard as $A$."

## NP-completeness and Cook-Levin

A language $B$ is **NP-hard** if $A \le_p B$ for every $A \in \mathsf{NP}$. It is
**NP-complete** if it is NP-hard and itself in $\mathsf{NP}$. NP-complete problems
are the hardest problems in $\mathsf{NP}$: if any one of them is in $\mathsf{P}$,
then all of $\mathsf{NP}$ is, so $\mathsf{P} = \mathsf{NP}$.

**Cook-Levin theorem (Cook 1971, Levin independently).** SAT is NP-complete. The
proof encodes the computation of an arbitrary polynomial-time verifier on input
$x$ and witness $w$ as a CNF formula that is satisfiable exactly when an accepting
$w$ exists. Every step of the machine becomes local clauses about the tableau of
its configurations.

**Karp 1972.** Twenty-one natural problems are NP-complete, including 3-SAT,
CLIQUE, VERTEX COVER, HAMILTONIAN CIRCUIT, SUBSET SUM, and graph coloring. This
showed NP-completeness is pervasive, not a curiosity about SAT.

## The restatement of P versus NP

Because SAT (or any NP-complete problem) is in $\mathsf{P}$ if and only if
$\mathsf{P} = \mathsf{NP}$, the whole question reduces to one problem:

$$\mathsf{P} = \mathsf{NP} \iff \mathsf{SAT} \in \mathsf{P}.$$

This is why the [SAT phase transition experiment](../../experiments/sat_phase_transition/)
is a natural place to probe where SAT is hard.

## coNP and the proof-system view

$\mathsf{coNP}$ is the class of problems whose *no*-instances have short
certificates (equivalently, the complements of $\mathsf{NP}$ languages). Tautology
checking (is a formula true under every assignment?) is coNP-complete. Whether
$\mathsf{NP} = \mathsf{coNP}$ is open and is implied by $\mathsf{P} = \mathsf{NP}$.
Cook and Reckhow (1979) connected $\mathsf{NP} = \mathsf{coNP}$ to whether there
is a propositional proof system in which every tautology has a short proof. That
connection is the seed of the [proof-complexity architecture](../research_atlas/README.md).

## Where to go next

- [`docs/02_graduate/`](../02_graduate/): circuit classes, $\mathsf{P/poly}$, the
  polynomial hierarchy, and the three barriers.
- [`docs/research_atlas/`](../research_atlas/): the candidate proof architectures
  and their obstructions.
