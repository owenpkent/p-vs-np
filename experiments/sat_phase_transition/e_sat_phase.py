"""Random 3-SAT phase transition and the hardness peak (experiment b).

Why this experiment exists. P vs NP asks whether SAT (the canonical
NP-complete problem, Cook 1971) is in P. The random k-SAT model gives the
sharpest empirical picture of *where* SAT is hard. For random 3-SAT with n
variables and m clauses, the satisfiable fraction undergoes a sharp threshold
as the ratio alpha = m/n crosses a critical value. The threshold is
conjectured (and for large k proved, Ding-Sly-Sun 2015) to be a sharp constant;
for k=3 the best numerical estimate is alpha_c ~ 4.267 (Mertens-Mezard-Zecchina
2006; Crawford-Auton 1996 located the empirical crossing near 4.2-4.3).

The structurally important fact for complexity theory is the coincidence of two
curves:

  - the satisfiability probability drops from ~1 to ~0 across alpha_c;
  - the running time of complete solvers (DPLL and descendants) peaks right at
    alpha_c.

The easy-hard-easy pattern is why "most" SAT instances are not hard: hardness
concentrates at the threshold. This is a worst-case-vs-average-case lesson that
the P vs NP program must respect. A proof that NP-complete problems are hard
must explain the worst case, which the threshold instances approach but random
sampling alone never pins.

What this script does. It implements a small, self-contained DPLL solver with
unit propagation and a simple branching heuristic, generates random 3-SAT at a
grid of ratios, and measures (1) the satisfiable fraction and (2) the median
DPLL decision count. It prints the curves and the location of the empirical
hardness peak, and saves a plot if matplotlib is available.

Dependencies: numpy + standard library only (matplotlib optional for the plot).
"""

from __future__ import annotations

import random
import statistics
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Random 3-SAT instance generation
# ---------------------------------------------------------------------------

def random_3sat(n: int, m: int, rng: random.Random) -> List[Tuple[int, int, int]]:
    """Generate m random 3-clauses over n variables.

    A literal is a nonzero integer: +v means variable v true, -v means false.
    Each clause is three distinct variables with random signs (the standard
    uniform random 3-SAT model used in the threshold literature).
    """
    clauses = []
    for _ in range(m):
        vars_ = rng.sample(range(1, n + 1), 3)
        clause = tuple(v if rng.random() < 0.5 else -v for v in vars_)
        clauses.append(clause)
    return clauses


# ---------------------------------------------------------------------------
# DPLL with unit propagation
# ---------------------------------------------------------------------------

@dataclass
class DPLLStats:
    decisions: int = 0


def _simplify(clauses, lit):
    """Return (clauses', ok) after asserting literal `lit`.

    Clauses satisfied by `lit` are dropped; the negation of `lit` is removed
    from the remaining clauses. ok is False if that produces an empty clause
    (a conflict).
    """
    out = []
    for clause in clauses:
        if lit in clause:
            continue  # clause satisfied
        if -lit in clause:
            reduced = tuple(x for x in clause if x != -lit)
            if not reduced:
                return None, False  # empty clause -> conflict
            out.append(reduced)
        else:
            out.append(clause)
    return out, True


def _unit_propagate(clauses, stats):
    """Assign all forced (unit) literals. Returns (clauses, ok).

    Pure simplification on the clause set: each unit clause forces its literal,
    which simplifies the rest, possibly creating new units. ok is False on
    conflict.
    """
    while True:
        unit = None
        for clause in clauses:
            if len(clause) == 1:
                unit = clause[0]
                break
        if unit is None:
            return clauses, True
        clauses, ok = _simplify(clauses, unit)
        if not ok:
            return None, False


def dpll(clauses, n, rng) -> Tuple[bool, DPLLStats]:
    """Decide satisfiability via DPLL. Returns (sat, stats).

    Standard recursive DPLL: unit-propagate to fixpoint, then branch on the
    first remaining literal, trying both truth values. `stats.decisions` counts
    branch points, the standard proxy for instance hardness.
    """
    stats = DPLLStats()

    def solve(clauses):
        clauses, ok = _unit_propagate(clauses, stats)
        if not ok:
            return False
        if len(clauses) == 0:
            return True  # all clauses satisfied
        branch_lit = clauses[0][0]
        stats.decisions += 1
        for lit in (branch_lit, -branch_lit):
            child, ok = _simplify(clauses, lit)
            if ok and solve(child):
                return True
        return False

    sat = solve(clauses)
    return sat, stats


# ---------------------------------------------------------------------------
# Experiment driver
# ---------------------------------------------------------------------------

def run(n: int = 60, trials: int = 60, alphas=None, seed: int = 12345):
    """Sweep clause/variable ratio, measure SAT fraction and DPLL hardness."""
    if alphas is None:
        alphas = [round(a, 2) for a in _frange(3.0, 6.0, 0.25)]
    rng = random.Random(seed)
    rows = []
    for alpha in alphas:
        m = int(round(alpha * n))
        sats = 0
        decision_counts = []
        for _ in range(trials):
            clauses = random_3sat(n, m, rng)
            sat, stats = dpll(clauses, n, rng)
            sats += 1 if sat else 0
            decision_counts.append(stats.decisions)
        frac = sats / trials
        med = statistics.median(decision_counts)
        rows.append((alpha, frac, med))
    return rows


def _frange(lo, hi, step):
    x = lo
    out = []
    while x <= hi + 1e-9:
        out.append(x)
        x += step
    return out


def main():
    n = 60
    trials = 60
    print(f"Random 3-SAT phase transition: n={n} variables, {trials} trials per ratio")
    print(f"{'alpha=m/n':>10} {'P(SAT)':>9} {'median DPLL decisions':>22}")
    rows = run(n=n, trials=trials)
    peak_alpha, peak_med = None, -1
    for alpha, frac, med in rows:
        marker = ""
        if med > peak_med:
            peak_med = med
            peak_alpha = alpha
        print(f"{alpha:>10.2f} {frac:>9.2f} {med:>22.1f}")
    print()
    # Find the ratio where P(SAT) crosses 0.5 (empirical threshold)
    crossing = None
    for i in range(1, len(rows)):
        a0, f0, _ = rows[i - 1]
        a1, f1, _ = rows[i]
        if f0 >= 0.5 >= f1:
            # linear interpolation
            if f0 != f1:
                crossing = a0 + (f0 - 0.5) * (a1 - a0) / (f0 - f1)
            else:
                crossing = (a0 + a1) / 2
            break
    print(f"Empirical SAT/UNSAT crossing (P=0.5): alpha ~ {crossing:.2f}" if crossing else "crossing not bracketed in range")
    print(f"Empirical hardness peak (max median decisions): alpha = {peak_alpha:.2f}")
    print("Reference: rigorous/numerical 3-SAT threshold alpha_c ~ 4.267 "
          "(Mertens-Mezard-Zecchina 2006); finite-n crossing drifts toward it from above.")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import os

        alphas = [r[0] for r in rows]
        fracs = [r[1] for r in rows]
        meds = [r[2] for r in rows]
        fig, ax1 = plt.subplots(figsize=(8, 5))
        ax1.plot(alphas, fracs, "o-", color="tab:blue", label="P(satisfiable)")
        ax1.axvline(4.267, color="gray", ls="--", lw=1, label="alpha_c ~ 4.267")
        ax1.set_xlabel("clause/variable ratio alpha = m/n")
        ax1.set_ylabel("P(satisfiable)", color="tab:blue")
        ax2 = ax1.twinx()
        ax2.plot(alphas, meds, "s-", color="tab:red", label="median DPLL decisions")
        ax2.set_ylabel("median DPLL decisions (hardness)", color="tab:red")
        ax1.set_title(f"Random 3-SAT phase transition (n={n})")
        fig.tight_layout()
        out = os.path.join(os.path.dirname(__file__), "sat_phase_transition.png")
        fig.savefig(out, dpi=120)
        print(f"Saved plot to {out}")
    except Exception as e:  # pragma: no cover - plotting is optional
        print(f"(plot skipped: {e})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
