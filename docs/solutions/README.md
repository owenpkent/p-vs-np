# Known approaches to P versus NP and why each is stuck

> A catalog of the serious approaches that have been tried, paired with the
> precise reason each is currently blocked. The companion to the
> [research atlas](../research_atlas/README.md): the atlas maps architectures,
> this document is a more candid "approach and obstruction" ledger, including the
> approaches that are popularly tried and provably cannot work.

## Approaches that provably cannot work (in their pure form)

These are not failures of effort; they are theorems about the limits of a method.

### Pure diagonalization / simulation

What it is: separate $\mathsf{P}$ from $\mathsf{NP}$ by building a problem that
defeats every polynomial-time machine, as the time hierarchy theorem does.

Why it is stuck: it relativizes (Baker-Gill-Solovay 1975). Any argument that
treats machines as black boxes proves its conclusion for every oracle, but
oracles force P vs NP both ways. A correct proof must be non-relativizing.

### Natural combinatorial circuit lower bounds

What it is: define a combinatorial property that explicit hard functions have and
easy functions lack, and use it to prove a circuit lower bound. This is how the
AC0 and monotone bounds were proved.

Why it is stuck (against $\mathsf{P/poly}$): if the property is large and
constructive, it is *natural*, and Razborov-Rudich (1994) show a natural useful
property breaks strong pseudorandom generators. Under standard cryptographic
assumptions, no such property exists for general circuits. The successful
restricted-class bounds escape only because AC0 and monotone circuits do not
contain pseudorandom generators.

### Arithmetization alone

What it is: encode Boolean computation as low-degree polynomials, the technique
behind $\mathsf{IP} = \mathsf{PSPACE}$. It is non-relativizing, so it looked like
an escape.

Why it is stuck: it algebrizes (Aaronson-Wigderson 2008), and algebrizing
techniques cannot resolve P vs NP. Escaping relativization is necessary but not
sufficient; you must also escape algebrization.

## Approaches that are open but blocked at a specific step

### Frege and extended-Frege proof-system lower bounds

What it is: prove $\mathsf{NP} \ne \mathsf{coNP}$ by showing strong proof systems
have no short proofs of some tautology family.

Where it is blocked: no super-polynomial lower bound is known for Frege.
Feasible interpolation, the main lower-bound engine, provably fails for strong
systems under cryptographic assumptions (Bonet-Pitassi-Raz 2000). This is the
proof-complexity analog of the natural-proofs barrier.

### Geometric Complexity Theory

What it is: separate permanent from determinant via representation-theoretic
obstructions in orbit-closure coordinate rings.

Where it is blocked: occurrence obstructions cannot work (Burgisser-Ikenmeyer-Panova
2016). Multiplicity obstructions remain open but require harder computations of
plethysm and Kronecker coefficients, themselves not well understood.

### Algorithm-to-lower-bound (the Williams program)

What it is: a faster-than-brute-force satisfiability algorithm for a circuit
class $\mathcal{C}$ implies a lower bound against $\mathcal{C}$ (Williams 2011),
yielding $\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$.

Where it is blocked: it is the live frontier, not blocked by a barrier. The open
problem is to extend it to stronger circuit classes ($\mathsf{TC}^0$ and beyond)
and to bring the hard function down from $\mathsf{NEXP}$ to $\mathsf{NP}$. This is
where unconditional progress has actually happened.

## Approaches the experts consider non-starters

- **"I found a fast algorithm for an NP-complete problem."** Almost always the
  algorithm is exponential in the worst case, or solves a special case, or the
  reduction is flawed. The SAT phase transition
  ([experiment](../../experiments/sat_phase_transition/)) shows random instances
  are mostly easy; worst-case hardness is the real question.
- **"I proved $\mathsf{P} \ne \mathsf{NP}$ by a counting argument."** Counting
  arguments are typically natural (they bound generic functions), so they fall to
  Razborov-Rudich for general circuits.
- **Ignoring the barriers.** Any claimed proof that does not address how it
  evades all three barriers is, with very high prior probability, mistaken. This
  is the operational reason for the [barrier checker](../../experiments/_shared/).

## The honest summary

No approach is known to be on track to resolve P vs NP. Every clean, soft, or
black-box approach meets a barrier. The approaches that are open (strong
proof-system lower bounds, GCT multiplicity obstructions, the Williams program)
are blocked at a specific, well-identified structural step rather than by a
general barrier. That specificity is the progress: we know where the hard part
is. See [`docs/researcher_mindset.md`](../researcher_mindset.md) for how to hold
this.
