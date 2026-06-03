"""Razborov 1985 in miniature: the sunflower lemma, and why monotone lower bounds
are natural.

Razborov 1985 proved that monotone circuits for k-CLIQUE require size
$n^{\\Omega(\\sqrt{k})}$, the first super-polynomial monotone circuit lower bound.
The engine is the method of approximations: replace each AND/OR gate by a
"clique indicator" approximator, and bound the errors introduced. The errors are
controlled by the Erdos-Rado SUNFLOWER LEMMA, which lets one "pluck" a sunflower
and collapse many terms into their common core.

Sunflower lemma (Erdos-Rado 1960). A family of more than $s!\\,(p-1)^s$ distinct
sets, each of size at most $s$, contains a $p$-sunflower: $p$ sets with a common
core $C$ such that the petals $S_i \\setminus C$ are pairwise disjoint (equivalently,
all pairwise intersections equal $C$).

This module demonstrates the combinatorial heart of the method, and the barrier
status of the technique:

  1. Constructive Erdos-Rado extraction: given a family above the bound, find a
     $p$-sunflower (greedy disjoint packing, else recurse on the link of the most
     frequent element). Verified on explicit families.
  2. Barrier check: Razborov's method of approximations is a NATURAL proof (large +
     constructive). It does not violate Razborov-Rudich because it bounds only
     MONOTONE circuits, where no pseudorandom generators are assumed. Against general
     circuits a natural property would break PRGs, which is why the monotone bound
     does not transfer.

What is verified here (no overclaiming): the sunflower extraction is exhibited and
checked on explicit families above the Erdos-Rado bound; the barrier checker
confirms the method is natural and disqualified against $\\mathsf{P/poly}$. The full
clique error-counting (the actual lower-bound proof) is described, not reimplemented.

Run:
    python -m experiments.circuit_complexity.e_monotone_clique
"""

from __future__ import annotations

import itertools
from collections import Counter
from math import factorial

from experiments._shared import BarrierChecker, BARRIERS


def erdos_rado_bound(s: int, p: int) -> int:
    """The Erdos-Rado threshold s! (p-1)^s: a family of distinct sets of size <= s
    larger than this contains a p-sunflower."""
    return factorial(s) * (p - 1) ** s


def find_sunflower(family: list[frozenset], p: int) -> list[frozenset] | None:
    """Constructive Erdos-Rado: return a p-sunflower (list of p sets) or None.

    Greedily pack pairwise-disjoint sets; if p are found that is a sunflower with
    empty core. Otherwise the maximal packing meets every set, so some element is
    frequent; recurse on its link and add it back to the core.
    """
    family = [S for S in family if S is not None]
    if not family:
        return None
    # greedy maximal packing of pairwise-disjoint sets
    packed: list[frozenset] = []
    used: set = set()
    for S in family:
        if not (S & used):
            packed.append(S)
            used |= set(S)
            if len(packed) == p:
                return packed  # sunflower with empty core
    if not used:
        return None
    # every set meets `used`; recurse on the link of the most frequent element
    cnt: Counter = Counter()
    for S in family:
        for x in (set(S) & used):
            cnt[x] += 1
    x = cnt.most_common(1)[0][0]
    link = [S - {x} for S in family if x in S]
    sub = find_sunflower(link, p)
    if sub is None:
        return None
    return [S | {x} for S in sub]


def is_sunflower(sets: list[frozenset]) -> bool:
    """True if the sets form a sunflower: all pairwise intersections equal the common
    core (intersection of all)."""
    if len(sets) < 2:
        return False
    core = set(sets[0])
    for S in sets[1:]:
        core &= set(S)
    core = frozenset(core)
    for a, b in itertools.combinations(sets, 2):
        if frozenset(a & b) != core:
            return False
    # petals must be pairwise disjoint (equivalent, but check directly)
    petals = [set(S) - core for S in sets]
    for a, b in itertools.combinations(petals, 2):
        if a & b:
            return False
    return True


def main() -> int:
    print("=== Razborov 1985 in miniature: the sunflower lemma and naturalness ===\n")

    print("Erdos-Rado sunflower extraction on families above the bound s!(p-1)^s:")
    for universe, s, p in [(5, 2, 3), (8, 3, 3)]:
        bound = erdos_rado_bound(s, p)
        family = [frozenset(c) for c in itertools.combinations(range(universe), s)]
        print(f"    all {s}-subsets of [{universe}]: {len(family)} sets, Erdos-Rado bound s!(p-1)^s = {bound}"
              f"  ({'above' if len(family) > bound else 'at/below'} bound, p={p})")
        assert len(family) > bound, "test family must exceed the Erdos-Rado bound"
        sun = find_sunflower(family, p)
        assert sun is not None and len(sun) == p, f"a {p}-sunflower must exist above the bound"
        assert is_sunflower(sun), "the returned sets must actually form a sunflower"
        core = frozenset.intersection(*sun)
        print(f"      found {p}-sunflower: core = {set(core) if core else '{}'}, "
              f"petals = {[sorted(set(S) - set(core)) for S in sun]}")
    print()

    # A family that is itself a sunflower is detected; a generic small family is not
    # forced to contain one.
    explicit = [frozenset({0, 1}), frozenset({0, 2}), frozenset({0, 3})]  # core {0}
    assert is_sunflower(explicit), "the explicit star must be a sunflower"
    print(f"Explicit star {[sorted(S) for S in explicit]} is a sunflower (core {{0}}): "
          f"{is_sunflower(explicit)}")
    print()

    print("Barrier profile of Razborov's monotone method of approximations:")
    verdict = BarrierChecker().check(BARRIERS["razborov_monotone"])
    print(verdict.report())
    assert verdict.hits_natural_proofs, "the method of approximations is a natural proof"
    assert not verdict.evades_all, "natural proofs are disqualified against P/poly"
    print()

    print("Why this is restricted-class only (the coordinate):")
    print("  - Razborov 1985: monotone k-CLIQUE circuits need size n^Omega(sqrt(k)).")
    print("  - The method is NATURAL (large + constructive), so by Razborov-Rudich it")
    print("    cannot prove a P/poly bound: against general circuits it would break PRGs.")
    print("  - It works for monotone circuits precisely because they contain no PRGs.")
    print("  - Monotone hardness does NOT transfer: Razborov-Tardos show monotone")
    print("    functions in P (e.g. perfect matching) that need super-polynomial")
    print("    monotone circuits, so monotone lower bounds say nothing about P/poly.")
    print()
    print("Self-check OK: the sunflower lemma engine is exhibited and verified; the")
    print("method of approximations is natural, hence monotone-only and blocked against")
    print("P/poly by Razborov-Rudich.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
