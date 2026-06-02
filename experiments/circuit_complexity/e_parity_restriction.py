"""Hastad switching lemma demo: parity collapses under random restrictions (experiment d).

Why this experiment exists. The single most important unconditional lower bound
in the early circuit-complexity program is that PARITY is not in AC0: no family
of constant-depth, polynomial-size, unbounded-fan-in AND/OR/NOT circuits
computes the parity of n bits (Furst-Saxe-Sipser 1981; Ajtai 1983; and with
the optimal exponential bound, Hastad 1986 via the switching lemma). This is a
proof technique that does NOT relativize (it opens up the circuit and argues
about its gates), which is exactly why it can prove a real separation where
diagonalization cannot. It is the prototype for the whole circuit-lower-bound
architecture aimed at NP not in P/poly.

The engine is the Hastad switching lemma: a random restriction that leaves each
variable free with probability p, and otherwise sets it to 0/1 at random,
turns a width-w DNF/CNF into something computable by a small decision tree with
high probability. Constant-depth circuits collapse layer by layer under
iterated restrictions, until a single gate would have to compute parity on the
surviving variables. But parity on k surviving variables genuinely depends on
all k, so it cannot be a small-depth decision tree. Contradiction: a small AC0
circuit for parity cannot exist.

What this script does (empirically, on small n). It cannot prove the asymptotic
theorem, but it exhibits its mechanism on truth tables:

  1. PARITY is restriction-robust: under a random restriction that leaves k of
     n variables free, the restricted function is ALWAYS parity (or its
     negation) on the k survivors, hence still depends on all k of them. Its
     minimum decision-tree depth stays exactly k. Parity has nowhere to hide.

  2. A width-w term (a single AND gate, the building block of a DNF) is fragile:
     under the same random restriction it becomes constant (trivial) with high
     probability, because any one variable set against the term kills it. We
     measure the collapse probability and compare to the switching-lemma
     intuition.

  3. Putting these together: a DNF small enough to be AC0 has all its terms
     collapse, so the whole DNF becomes a shallow decision tree, but parity's
     decision-tree depth does not drop. That gap is the lower bound in
     miniature.

Dependencies: standard library + numpy (numpy only for convenience; the logic
is pure Python).
"""

from __future__ import annotations

import random
from typing import Dict, List, Tuple


def parity(bits: Tuple[int, ...]) -> int:
    """Parity (XOR) of a bit tuple."""
    return sum(bits) & 1


def min_decision_tree_depth(values: List[int], k: int) -> int:
    """Exact minimum decision-tree depth of a k-variable Boolean function.

    `values` is the length-2^k truth table indexed by the integer whose binary
    digits are the variable assignment (variable 0 is the least significant
    bit). Standard recursion: a constant function has depth 0; otherwise depth =
    1 + min over query variables of max(depth of the two cofactors). Memoized on
    the (frozenset of live indices, active-mask) so repeated subproblems are
    not recomputed. Exponential in k, so only for small k (k <= 8 here).
    """
    from functools import lru_cache

    full = list(values)

    @lru_cache(maxsize=None)
    def rec(active_vars: Tuple[int, ...], fixed_bits: int, fixed_mask: int) -> int:
        # Collect the outputs consistent with the current partial assignment.
        outs = set()
        for idx in range(1 << k):
            if (idx & fixed_mask) == fixed_bits:
                outs.add(full[idx])
                if len(outs) == 2:
                    break
        if len(outs) <= 1:
            return 0
        best = None
        for v in active_vars:
            bit = 1 << v
            rest = tuple(u for u in active_vars if u != v)
            d0 = rec(rest, fixed_bits, fixed_mask | bit)
            d1 = rec(rest, fixed_bits | bit, fixed_mask | bit)
            d = 1 + max(d0, d1)
            if best is None or d < best:
                best = d
        return best

    return rec(tuple(range(k)), 0, 0)


def build_values(func, k: int) -> List[int]:
    """Tabulate `func` over all 2^k assignments, returning a flat list.

    Index i encodes the assignment whose bit j (LSB-first) is variable j.
    """
    out = []
    for i in range(1 << k):
        assign = tuple((i >> j) & 1 for j in range(k))
        out.append(func(assign))
    return out


def random_restriction(n: int, p: float, rng: random.Random) -> Tuple[List[int], Dict[int, int]]:
    """A Hastad-style random restriction.

    Each of n variables is left free with probability p; otherwise it is fixed
    to a uniformly random bit. Returns (free_vars, fixed) where fixed maps a
    fixed variable index to its value.
    """
    free = []
    fixed = {}
    for i in range(n):
        if rng.random() < p:
            free.append(i)
        else:
            fixed[i] = 1 if rng.random() < 0.5 else 0
    return free, fixed


def restrict_parity(free: List[int], fixed: Dict[int, int]):
    """The restriction of n-bit parity to the free variables.

    Parity is linear, so restricting it just XORs in the fixed bits as a
    constant offset. The result depends on ALL free variables.
    """
    offset = sum(fixed.values()) & 1

    def f(assign_free: Tuple[int, ...]) -> int:
        return (sum(assign_free) + offset) & 1

    return f


def restrict_term(term: Dict[int, int], free: List[int], fixed: Dict[int, int]):
    """Restrict a single AND-term (a width-w conjunction of literals).

    `term` maps variable index -> required bit. The term outputs 1 iff every
    listed variable matches its required bit. After fixing some variables the
    term is either: killed (a fixed variable contradicts the term -> constant 0),
    forced satisfied on the fixed part, or still depending on the free part.
    Returns (kind, residual_func) where kind in {"const0","const1","live"}.
    """
    for v, b in term.items():
        if v in fixed and fixed[v] != b:
            return "const0", (lambda a: 0)
    live_vars = [v for v in term if v in free]
    if not live_vars:
        return "const1", (lambda a: 1)

    free_index = {v: free.index(v) for v in live_vars}

    def f(assign_free: Tuple[int, ...]) -> int:
        return 1 if all(assign_free[free_index[v]] == term[v] for v in live_vars) else 0

    return "live", f


def run(n: int = 12, p: float = 0.5, width: int = 3, trials: int = 2000, seed: int = 7):
    rng = random.Random(seed)

    # Part 1: parity is restriction-robust. Its decision-tree depth equals the
    # number of surviving free variables, every time.
    depths_match = 0
    free_counts = []
    counted = 0
    cap = 8  # exact DT-depth is exponential in #free vars; cap for tractability
    for _ in range(trials):
        free, fixed = random_restriction(n, p, rng)
        free_counts.append(len(free))
        if len(free) > cap:
            continue
        f = restrict_parity(free, fixed)
        values = build_values(f, len(free))
        depth = min_decision_tree_depth(values, len(free))
        counted += 1
        if depth == len(free):
            depths_match += 1

    # Part 2: a width-w AND-term is fragile. Measure collapse probability.
    collapses = 0
    for _ in range(trials):
        term_vars = rng.sample(range(n), width)
        term = {v: (1 if rng.random() < 0.5 else 0) for v in term_vars}
        free, fixed = random_restriction(n, p, rng)
        kind, _ = restrict_term(term, free, fixed)
        if kind in ("const0", "const1"):
            collapses += 1
    collapse_prob = collapses / trials

    # Exact expectation for one width-w term under the restriction. Per variable:
    #   free                w.p. p
    #   fixed and matching  w.p. (1-p)/2
    #   fixed contradicting w.p. (1-p)/2
    # The term stays "live" (non-constant) iff no variable contradicts AND not
    # all variables are fixed. So
    #   P(live) = ((1+p)/2)^w - ((1-p)/2)^w
    #   P(collapse to a constant) = 1 - P(live).
    p_live = ((1 + p) / 2) ** width - ((1 - p) / 2) ** width
    pred_collapse = 1 - p_live

    return {
        "n": n,
        "p": p,
        "width": width,
        "trials": trials,
        "parity_depth_match": depths_match,
        "parity_counted": counted,
        "mean_free": sum(free_counts) / len(free_counts),
        "term_collapse_prob": collapse_prob,
        "term_collapse_predicted": pred_collapse,
    }


def main():
    n, p, width, trials = 12, 0.5, 3, 2000
    print(f"Hastad switching-lemma demo: n={n}, restriction keeps each var free w.p. p={p}")
    print(f"Width-w term experiment uses w={width}, {trials} trials.\n")
    r = run(n=n, p=p, width=width, trials=trials)

    print("Part 1: PARITY is restriction-robust (it has nowhere to hide).")
    print(f"  mean surviving free variables: {r['mean_free']:.2f} (expected {n*p:.2f})")
    print(f"  trials with restricted-parity DT-depth == #free vars: "
          f"{r['parity_depth_match']}/{r['parity_counted']}")
    assert r["parity_depth_match"] == r["parity_counted"], "parity should never collapse"
    print("  -> restricted parity ALWAYS depends on every surviving variable. "
          "Min decision-tree depth never drops below #free vars.\n")

    print("Part 2: a width-w AND-term (a DNF building block) is fragile.")
    print(f"  empirical collapse probability: {r['term_collapse_prob']:.3f}")
    print(f"  exact predicted collapse prob 1 - (((1+p)/2)^w - ((1-p)/2)^w) = "
          f"{r['term_collapse_predicted']:.3f}")
    assert abs(r["term_collapse_prob"] - r["term_collapse_predicted"]) < 0.05
    print("  -> terms become constant with high probability under restriction "
          "(empirical matches the exact prediction).\n")

    print("Conclusion (the lower bound in miniature):")
    print("  A DNF small enough to be AC0 has all its terms collapse under a random")
    print("  restriction, so the whole circuit becomes a shallow decision tree. But")
    print("  parity's decision-tree depth does NOT drop: it still depends on every")
    print("  surviving variable. That gap is why constant-depth circuits need")
    print("  super-polynomial size for parity (Hastad 1986). This technique does not")
    print("  relativize, which is exactly why it proves a real separation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
