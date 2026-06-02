"""Phase 0 smoke test: does the three-barrier wrong-approach detector work?

This is the P-vs-NP analog of the Riemann repo's Davenport-Heilbronn smoke
test. There the control is a single L-function; here it is the trio of barrier
theorems. The smoke test pins the barrier profile of four canonical techniques
against the published record:

  1. Pure diagonalization relativizes (and algebrizes), so it is disqualified.
  2. Razborov's monotone method is a natural proof (large + constructive).
  3. Arithmetization is non-relativizing but algebrizes (the AW 2008 example).
  4. Williams's NEXP-not-in-ACC0 evades all three barriers.

If any of these regress, the checker logic has drifted from the mathematics.
"""

from __future__ import annotations

from experiments._shared import BarrierChecker, BARRIERS


def check(label, ok, info=""):
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}{(' - ' + info) if info else ''}")
    return ok


def test_diagonalization_disqualified():
    print("Test 1: pure diagonalization is disqualified (relativizes)")
    v = BarrierChecker().check(BARRIERS["diagonalization"])
    return (
        check("hits relativization barrier", v.hits_relativization)
        and check("hits algebrization barrier", v.hits_algebrization)
        and check("does not evade all three", not v.evades_all)
    )


def test_monotone_is_natural():
    print("Test 2: Razborov monotone method is a natural proof")
    v = BarrierChecker().check(BARRIERS["razborov_monotone"])
    ok_nat = check("hits natural-proofs barrier (large + constructive)", v.hits_natural_proofs)
    ok_rel = check("does NOT relativize (opens the circuit)", not v.hits_relativization)
    return ok_nat and ok_rel


def test_arithmetization_algebrizes():
    print("Test 3: arithmetization is non-relativizing but algebrizes")
    v = BarrierChecker().check(BARRIERS["arithmetization_ip"])
    ok_rel = check("does NOT relativize", not v.hits_relativization)
    ok_alg = check("DOES algebrize (Aaronson-Wigderson 2008)", v.hits_algebrization)
    ok_dq = check("disqualified by the algebrization barrier", not v.evades_all)
    return ok_rel and ok_alg and ok_dq


def test_williams_evades_all():
    print("Test 4: Williams NEXP-not-in-ACC0 evades all three barriers")
    v = BarrierChecker().check(BARRIERS["williams_acc0"])
    return (
        check("evades relativization", not v.hits_relativization)
        and check("evades natural proofs", not v.hits_natural_proofs)
        and check("evades algebrization", not v.hits_algebrization)
        and check("evades all three (necessary, not sufficient)", v.evades_all)
    )


def test_report_renders():
    print("Test 5: verdict report renders for each canonical technique")
    ok = True
    for key in BARRIERS:
        v = BarrierChecker().check(BARRIERS[key])
        text = v.report()
        ok = ok and check(f"{key} report non-empty", isinstance(text, str) and len(text) > 0)
    return ok


def main():
    results = [
        test_diagonalization_disqualified(),
        test_monotone_is_natural(),
        test_arithmetization_algebrizes(),
        test_williams_evades_all(),
        test_report_renders(),
    ]
    print()
    n_pass = sum(results)
    print(f"Smoke test: {n_pass}/{len(results)} passed")
    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
