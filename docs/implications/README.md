# Why P versus NP matters

The implications of a resolution, in both directions. The stakes are why this is
a Millennium Prize Problem rather than a curiosity.

## If P = NP

This would be one of the most consequential results in the history of
mathematics and computing. Every problem with efficiently checkable solutions
would have efficiently findable solutions.

- **Cryptography collapses.** Most public-key cryptography (RSA, Diffie-Hellman,
  elliptic-curve schemes) rests on problems that are easy to verify but believed
  hard to solve (factoring, discrete log). If $\mathsf{P} = \mathsf{NP}$ with a
  practical algorithm, these break. Note the caveat: a non-constructive proof, or
  one with an astronomical polynomial like $n^{100}$, would not immediately yield
  practical attacks. But the conceptual foundation of modern security would be
  gone.
- **Optimization becomes routine.** Scheduling, routing, protein folding, circuit
  design, and thousands of NP-hard optimization problems would admit efficient
  exact algorithms. Operations research and computational biology would be
  transformed.
- **Mathematics partly automates.** Finding a proof of a theorem (given a bound
  on its length) is in $\mathsf{NP}$: a proof is a short checkable witness. If
  $\mathsf{P} = \mathsf{NP}$, theorem-proving up to a length bound becomes
  efficient. Creativity in the sense of "search for a short certificate" would be
  mechanizable.
- **Machine learning.** Finding the smallest consistent hypothesis (Occam-style
  learning) is often NP-hard; $\mathsf{P} = \mathsf{NP}$ would make many learning
  problems tractable.

The near-universal expectation is that this does not hold. But the magnitude of
what it would mean is exactly why the question is so important.

## If P != NP

This is the expected outcome, and proving it would also be momentous.

- **Cryptography is on firmer ground.** $\mathsf{P} \ne \mathsf{NP}$ is necessary
  (though not sufficient) for the existence of one-way functions, the foundation
  of cryptography. It would not by itself prove cryptography secure (that needs
  average-case hardness and more), but it would remove the nightmare scenario.
- **Hardness is real.** It would confirm that for a vast range of problems,
  brute-force-like search is essentially unavoidable in the worst case. This
  validates the entire enterprise of approximation algorithms, heuristics, and
  fixed-parameter tractability as the right response to genuine hardness.
- **A new proof technique.** Because of the barriers, a proof of
  $\mathsf{P} \ne \mathsf{NP}$ would require a fundamentally new method: one that
  is non-relativizing, non-natural, and non-algebrizing. Such a method would
  almost certainly illuminate far more than P vs NP, the way the function-field
  proof of the Riemann Hypothesis analog illuminated arithmetic geometry.

## Either way: the value of the attempt

Even without resolution, the pursuit has produced foundational science:
NP-completeness theory (a unifying language across thousands of problems), the
PCP theorem (the basis of hardness of approximation), the theory of
pseudorandomness, interactive and probabilistically checkable proofs, and the
barrier theorems themselves. The problem has been a generator of ideas far out of
proportion to its statement.

## Connection to the experiments

- The [SAT phase transition](../../experiments/sat_phase_transition/) makes the
  average-case/worst-case distinction concrete, which is exactly the distinction
  that matters for whether cryptography can rest on NP-hardness.
- The [barrier experiments](../../experiments/_shared/) make precise why a proof
  in either direction must be so unusual, which is why a resolution would be a
  new technique, not just a new theorem.
