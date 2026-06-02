"""Baker-Gill-Solovay relativization demo (experiment a).

Why this experiment exists. The first barrier any P-vs-NP proof technique must
clear is relativization. Baker, Gill and Solovay (1975) exhibited two oracles:

  - Oracle A with P^A = NP^A. The standard choice is any PSPACE-complete oracle
    (e.g. TQBF). Relative to it, both P^A and NP^A collapse to PSPACE^A = PSPACE,
    so they are equal. Intuition: a PSPACE oracle is so powerful that the
    nondeterministic guessing NP would do is already simulable deterministically
    with the oracle's help.

  - Oracle B with P^B != NP^B. B is built by diagonalization. Define the unary
    "oracle language" L_B = { 1^n : B contains some string of length n }.
    L_B is in NP^B trivially (guess the witness string of length n, ask B). The
    construction reserves, for each polynomial-time oracle machine M_i, a fresh
    length n_i and diagonalizes: simulate M_i^B(1^{n_i}) for fewer than 2^{n_i}
    steps, see which length-n_i strings it queried, then set B on length n_i so
    that M_i's answer is WRONG. Since M_i runs in poly time it cannot query all
    2^{n_i} strings, so a free string always remains to flip the truth of
    "1^{n_i} in L_B" against M_i's output. Hence no poly-time oracle machine
    decides L_B: L_B is in NP^B but not P^B.

Because a proof technique that "relativizes" would prove its conclusion for
EVERY oracle, and these two oracles force opposite answers, no relativizing
technique can resolve P vs NP. Diagonalization and simulation relativize, which
is the precise sense in which they are insufficient.

What this script does. It cannot build the real oracles (they are infinite),
but it makes the diagonalization mechanism concrete and checkable on a finite
model:

  1. Easy direction (P^A = NP^A): a small simulation showing that with a
     PSPACE-style oracle that answers "is this quantified Boolean formula true",
     a nondeterministic poly-time machine's accept condition (exists a witness)
     is itself a PSPACE query, so the oracle machine decides it deterministically
     with one query. This illustrates the collapse without claiming to prove it.

  2. Hard direction (P^B != NP^B): the actual diagonalization. We model a finite
     family of "poly-time oracle machines" by their query sets (each machine, on
     input 1^n, queries at most some budget < 2^n of the length-n strings and
     then outputs a bit). We run the BGS stage construction, building a finite
     oracle B that defeats every machine in the family, and verify that for the
     resulting B: (i) each machine answers 1^{n_i} incorrectly, while (ii) the
     true membership 1^{n_i} in L_B is determined by whether we planted a free
     string. The defeat of every poly-time machine is the separation in
     miniature.

Dependencies: standard library only.
"""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Set, Tuple


# ---------------------------------------------------------------------------
# Easy direction: P^A = NP^A with a PSPACE-complete oracle (illustration)
# ---------------------------------------------------------------------------

def qbf_true(formula: Callable[[], bool]) -> bool:
    """Stand-in PSPACE oracle: decide a (here, already-evaluated) QBF instance.

    A true PSPACE oracle answers arbitrary quantified Boolean formulas in one
    query. We model the *interface*: a poly-time machine with this oracle can
    ask "does there exist a witness w of length m with V(x, w) = 1?" as a single
    bounded-quantifier QBF query, which the oracle resolves. That is exactly the
    NP acceptance condition, so NP^A computation is simulable by a P^A machine
    making one oracle call. This function evaluates the supplied closure to
    represent that single resolved query.
    """
    return formula()


def np_accepts_via_oracle(verifier: Callable[[Tuple[int, ...]], bool], witness_len: int) -> bool:
    """An NP^A machine: accept iff exists a witness the verifier accepts.

    With a PSPACE oracle the existential is one query (qbf_true), so a P^A
    machine decides the same language. We exhibit both and check they agree.
    """
    exists_witness = lambda: any(
        verifier(w) for w in itertools.product((0, 1), repeat=witness_len)
    )
    # NP^A: nondeterministic guess + verify (modeled as the search).
    np_answer = exists_witness()
    # P^A: a single PSPACE-oracle query resolving the same existential.
    p_answer = qbf_true(exists_witness)
    return np_answer == p_answer  # they must coincide -> P^A = NP^A on this language


# ---------------------------------------------------------------------------
# Hard direction: the BGS diagonalization for P^B != NP^B
# ---------------------------------------------------------------------------

@dataclass
class OracleMachine:
    """A finite model of a poly-time oracle machine on inputs 1^n.

    On input 1^n the machine, given access to the (being-constructed) oracle B,
    queries some set of length-n strings (its `query_strategy`) and outputs a
    bit (its `decision`). The polynomial time bound is modeled by a query
    budget strictly less than 2^n, the key BGS resource constraint: a poly-time
    machine on input 1^n cannot inspect all 2^n strings of length n.
    """

    name: str
    # Given (n, current oracle membership on length-n strings), return the set
    # of length-n strings queried. Must respect the budget.
    query_strategy: Callable[[int, Dict[Tuple[int, ...], bool]], Set[Tuple[int, ...]]]
    # Given the answers to its queries, output an accept/reject bit.
    decision: Callable[[Dict[Tuple[int, ...], bool]], bool]


def all_strings(n: int) -> List[Tuple[int, ...]]:
    return list(itertools.product((0, 1), repeat=n))


def bgs_diagonalize(machines: List[OracleMachine], rng: random.Random):
    """Run the BGS stage construction; return (oracle_B, log).

    Stage i reserves a fresh length n_i (we use n_i = i + 2 so 2^{n_i} grows and
    leaves room beyond each machine's budget). The oracle is built only on the
    reserved lengths; all other lengths are empty. We:

      1. Let M_i query its strings of length n_i against B-so-far (empty on n_i).
      2. Read M_i's output bit b_i.
      3. Set B on length n_i so that the TRUE answer to "1^{n_i} in L_B"
         (i.e. does B contain ANY length-n_i string) is the OPPOSITE of b_i.
         If b_i = True (machine says 1^{n_i} in L_B), we make L_B exclude it by
         leaving all length-n_i strings out of B. If b_i = False, we plant one
         length-n_i string that M_i did NOT query (guaranteed to exist by the
         budget), so 1^{n_i} truly IS in L_B though M_i said no.

    The planted string exists precisely because the machine's query budget is
    < 2^{n_i}. That single fact is the engine of the separation.
    """
    oracle_B: Dict[int, Set[Tuple[int, ...]]] = {}
    log = []
    for i, M in enumerate(machines):
        n_i = i + 2
        strings = all_strings(n_i)
        membership = {s: False for s in strings}  # B is empty on length n_i so far
        queried = M.query_strategy(n_i, membership)
        budget_ok = len(queried) < 2 ** n_i
        b_i = M.decision({s: (s in oracle_B.get(n_i, set())) for s in queried})

        planted = None
        if b_i:
            # Machine claims 1^{n_i} in L_B. Make it false: keep B empty here.
            oracle_B[n_i] = set()
            true_membership = False
        else:
            # Machine claims 1^{n_i} not in L_B. Make it true by planting a
            # length-n_i string the machine did not query.
            free = [s for s in strings if s not in queried]
            planted = rng.choice(free)
            oracle_B[n_i] = {planted}
            true_membership = True

        machine_wrong = (b_i != true_membership)
        log.append(
            {
                "machine": M.name,
                "n_i": n_i,
                "queries_used": len(queried),
                "budget_limit": 2 ** n_i,
                "budget_ok": budget_ok,
                "machine_output": b_i,
                "true_membership": true_membership,
                "planted_free_string": planted,
                "machine_wrong": machine_wrong,
            }
        )
    return oracle_B, log


def make_poly_machine(name: str, n_total_lengths: int, rng: random.Random) -> OracleMachine:
    """Construct a sample poly-time oracle machine with a sub-2^n query budget.

    We model a generic poly-time strategy: on input 1^n it queries a random
    subset of length-n strings of size min(2^n - 1, n^2) (a polynomial in n,
    strictly below the 2^n total), then outputs a fixed but arbitrary decision
    rule (here: accept iff the number of queried strings present in B is even).
    The decision rule is irrelevant to the construction; diagonalization defeats
    any rule.
    """

    def query_strategy(n: int, membership: Dict[Tuple[int, ...], bool]) -> Set[Tuple[int, ...]]:
        budget = min(2 ** n - 1, n * n)
        strings = all_strings(n)
        return set(rng.sample(strings, budget))

    def decision(answers: Dict[Tuple[int, ...], bool]) -> bool:
        return (sum(1 for v in answers.values() if v) % 2) == 0

    return OracleMachine(name=name, query_strategy=query_strategy, decision=decision)


def main():
    rng = random.Random(2025)

    print("=" * 70)
    print("Baker-Gill-Solovay (1975): two oracles forcing opposite answers")
    print("=" * 70)

    print("\n[1] Easy direction: P^A = NP^A with a PSPACE-style oracle.")
    # An example NP language: exists a witness w of length 4 with parity-2 ones.
    verifier = lambda w: sum(w) == 2
    agree = np_accepts_via_oracle(verifier, witness_len=4)
    print("    NP^A accept (exists witness) and P^A accept (one PSPACE query) agree:", agree)
    print("    Interpretation: a PSPACE oracle resolves the NP existential in one")
    print("    query, so P^A and NP^A decide the same languages. P^A = NP^A.")
    assert agree

    print("\n[2] Hard direction: P^B != NP^B by diagonalization.")
    machines = [make_poly_machine(f"M_{i}", 6, rng) for i in range(5)]
    oracle_B, log = bgs_diagonalize(machines, rng)
    print(f"    Built oracle B defeating {len(machines)} poly-time oracle machines.")
    print(f"    {'machine':>8} {'n_i':>4} {'queries':>8} {'budget(2^n)':>12} "
          f"{'M says':>7} {'truth':>6} {'M wrong?':>9}")
    for row in log:
        print(f"    {row['machine']:>8} {row['n_i']:>4} {row['queries_used']:>8} "
              f"{row['budget_limit']:>12} {str(row['machine_output']):>7} "
              f"{str(row['true_membership']):>6} {str(row['machine_wrong']):>9}")
    all_wrong = all(row["machine_wrong"] for row in log)
    all_budget_ok = all(row["budget_ok"] for row in log)
    print(f"\n    Every poly-time machine answers 1^(n_i) incorrectly: {all_wrong}")
    print(f"    Every machine stayed within its sub-2^n query budget:  {all_budget_ok}")
    assert all_wrong and all_budget_ok
    print("    L_B = { 1^n : B has a length-n string } is in NP^B (guess + check)")
    print("    but no poly-time machine decides it. So P^B != NP^B.")

    print("\n" + "=" * 70)
    print("Conclusion: a technique that RELATIVIZES proves its claim for every")
    print("oracle. A and B force opposite answers, so no relativizing technique")
    print("can resolve P vs NP (the relativization barrier). The barrier checker")
    print("in experiments/_shared flags exactly such techniques.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
