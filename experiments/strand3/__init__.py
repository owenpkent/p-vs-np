"""Strand-3 search: candidate non-algebrizing invariants for the dossier's missing object.

The 2050 dossier's braided path needs a quantity that is both strand-1 (cheaply
computable by a faster-than-brute-force #SAT-style algorithm) and strand-3 (provably
not reconstructible from a low-degree oracle extension). This package runs candidate
invariants through the algebrization probe plus a strand-1 computability judgment and
a circularity check, logging each as a coordinate. See docs/03_research/strand3_ledger.md.
"""
