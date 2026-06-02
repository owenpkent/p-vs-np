"""Natural-proofs largeness / constructivity check (experiment c).

Why this experiment exists. Razborov and Rudich (1994) defined a *natural*
combinatorial property of Boolean functions and proved that no natural property
can separate P/poly from NP under the assumption that strong pseudorandom
generators exist (equivalently, sufficiently hard one-way functions). A property
Phi of n-bit Boolean functions is natural if it has:

  - Largeness: Phi holds for at least a 1/2^{O(n)} fraction of all 2^{2^n}
    Boolean functions (the standard versions ask for a constant fraction, or at
    least 1/poly(2^n)). Intuitively, the property is common, not bespoke.

  - Constructivity: given the 2^n-bit truth table of a function, Phi is
    decidable in time polynomial in 2^n. Intuitively, the property is something
    a small circuit could test.

Razborov-Rudich's theorem: if a property is natural and *useful* (it fails for
all easy functions, so any function with the property is hard), then it can be
used to break a pseudorandom generator, contradicting the cryptographic
assumption. So a useful natural property cannot exist for P/poly. To prove
NP not in P/poly via a combinatorial property, the property must therefore be
NON-natural: either non-constructive (cannot be tested in poly(2^n) time) or
non-large (specific to the hard function rather than common). Williams's ACC0
work and the GCT program are both attempts to use non-natural ingredients.

What this script does. On small n it measures largeness and constructivity for
several candidate properties, making the definitions concrete:

  1. "high average sensitivity" (a typical combinatorial hardness proxy):
     LARGE (most functions have high sensitivity) and CONSTRUCTIVE (computable
     from the truth table in poly(2^n) time). So it is NATURAL, and by
     Razborov-Rudich it cannot prove general circuit lower bounds. We measure
     the fraction of random functions satisfying it (largeness) and time its
     evaluation (constructivity).

  2. "equals this one specific hard function" (a non-large property): trivially
     constructive but NOT large (true for exactly one function out of 2^{2^n}).
     This is the escape hatch: a property tailored to the target function dodges
     the largeness clause. The catch is that to be USEFUL it must still exclude
     all easy functions, and certifying that exclusion is where the real work
     (and the non-naturalness) hides.

  3. "minimum circuit size > s" (the property we actually want): we note it is
     large for large s but its constructivity is exactly the Minimum Circuit
     Size Problem (MCSP), whose complexity is open. This is the precise point
     where naturalness becomes subtle.

The script prints largeness fractions and per-property timings, and classifies
each property as natural / non-natural by the measured criteria.

Dependencies: standard library only.
"""

from __future__ import annotations

import itertools
import random
import time
from typing import Callable, Dict, List, Tuple


def truth_table(func: Callable[[Tuple[int, ...]], int], n: int) -> Tuple[int, ...]:
    """Return the length-2^n truth table of an n-bit function."""
    return tuple(func(x) for x in itertools.product((0, 1), repeat=n))


def random_function_tt(n: int, rng: random.Random) -> Tuple[int, ...]:
    """A uniformly random n-bit Boolean function as a truth table."""
    return tuple(1 if rng.random() < 0.5 else 0 for _ in range(1 << n))


def average_sensitivity(tt: Tuple[int, ...], n: int) -> float:
    """Average sensitivity: expected number of pivotal coordinates.

    For each input x and each coordinate i, the pair (x, x^{e_i}) is a sensitive
    edge if the function value differs. Average sensitivity is the total number
    of sensitive edges divided by 2^n. Computable directly from the truth table
    in O(n * 2^n) time, hence CONSTRUCTIVE (poly in the 2^n table length).
    """
    N = 1 << n
    sensitive = 0
    for x in range(N):
        for i in range(n):
            y = x ^ (1 << i)
            if tt[x] != tt[y]:
                sensitive += 1
    # average sensitivity = (1/2^n) * sum_x #{i : f(x) != f(x^e_i)}
    return sensitive / N


def prop_high_sensitivity(tt: Tuple[int, ...], n: int, threshold: float) -> bool:
    """Candidate property: average sensitivity exceeds a threshold.

    A standard combinatorial hardness proxy (high-sensitivity functions resist
    shallow circuits). We will measure that this is LARGE and CONSTRUCTIVE,
    hence natural.
    """
    return average_sensitivity(tt, n) > threshold


def measure_largeness(prop: Callable[[Tuple[int, ...]], bool], n: int, samples: int, rng: random.Random) -> float:
    """Fraction of random n-bit functions satisfying `prop` (Monte Carlo)."""
    hits = 0
    for _ in range(samples):
        tt = random_function_tt(n, rng)
        if prop(tt):
            hits += 1
    return hits / samples


def measure_constructivity_time(prop: Callable[[Tuple[int, ...]], bool], n: int, reps: int, rng: random.Random) -> float:
    """Average wall-clock time to evaluate `prop` once (constructivity proxy).

    Constructivity (Razborov-Rudich) means decidable in time poly(2^n). We do
    not certify the asymptotic bound here, but we report the measured per-call
    time so the scaling can be inspected across n.
    """
    tts = [random_function_tt(n, rng) for _ in range(reps)]
    t0 = time.perf_counter()
    for tt in tts:
        prop(tt)
    return (time.perf_counter() - t0) / reps


def main():
    rng = random.Random(99)
    print("Natural-proofs largeness / constructivity check")
    print("(Razborov-Rudich 1994: a useful NATURAL property cannot separate P/poly")
    print(" from NP under standard pseudorandomness assumptions.)\n")

    # Property 1: high average sensitivity. Threshold n/2 (random functions have
    # average sensitivity ~ n/2, so this picks out "at least typical").
    print("Property 1: average sensitivity > n/2  (a common hardness proxy)")
    print(f"{'n':>3} {'largeness':>10} {'eval time (s)':>14} {'verdict':>22}")
    for n in (3, 4, 5):
        prop = lambda tt, n=n: prop_high_sensitivity(tt, n, threshold=n / 2.0)
        large = measure_largeness(prop, n, samples=400, rng=rng)
        t = measure_constructivity_time(prop, n, reps=200, rng=rng)
        # Natural = large (>= ~1/poly) AND constructive (poly-time). Both hold.
        is_large = large >= 0.1
        is_constructive = True  # O(n 2^n) by construction
        verdict = "NATURAL (barrier hits)" if (is_large and is_constructive) else "non-natural"
        print(f"{n:>3} {large:>10.3f} {t:>14.6f} {verdict:>22}")
    print("  -> large + constructive = natural. By Razborov-Rudich this property")
    print("     cannot prove super-polynomial lower bounds against general circuits.\n")

    # Property 2: equality to one fixed function. Non-large by construction.
    print("Property 2: 'equals this one specific function'  (the non-large escape)")
    n = 4
    target = random_function_tt(n, rng)
    prop_eq = lambda tt: tt == target
    large_eq = measure_largeness(prop_eq, n, samples=2000, rng=rng)
    expected = 1.0 / (1 << (1 << n))  # 1 / 2^{2^n}
    print(f"  n={n}: measured largeness {large_eq:.6f} (exact 1/2^(2^n) = {expected:.2e})")
    print("  -> constructive but NOT large: it dodges the largeness clause. The cost")
    print("     is usefulness: to certify a function is HARD this way you must still")
    print("     exclude every easy function, and that certification is the hard,")
    print("     non-natural part the barrier pushes the proof toward.\n")

    # Property 3: the property we actually want (MCSP).
    print("Property 3: 'minimum circuit size > s'  (what a real lower bound needs)")
    print("  Largeness: for s below the ~2^n/n counting bound, MOST functions need")
    print("  large circuits (Shannon 1949), so the property is large.")
    print("  Constructivity: deciding it from the truth table IS the Minimum Circuit")
    print("  Size Problem (MCSP), whose complexity is open (not known to be in P,")
    print("  not known NP-hard under poly-time reductions). This is the exact crux:")
    print("  if MCSP were easy the property would be natural and the barrier would")
    print("  bite; its apparent hardness is what a non-natural proof must exploit.\n")

    print("Takeaway: to separate NP from P/poly a combinatorial property must be")
    print("NON-natural (non-constructive, or non-large-yet-useful). This is a")
    print("coordinate, not a wall: it tells us where the proof must live.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
