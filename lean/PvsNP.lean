-- Main module for the PvsNP project. Imports all sub-modules.
-- See lean/README.md for project status and structure.
--
-- This is a SKELETON. It states the central objects and theorems of the P-vs-NP
-- landscape as typed Lean declarations with documented `sorry` markers. It is
-- not expected to build against Mathlib without further work: Mathlib's
-- complexity-theory coverage is thin, so most statements use lightweight
-- self-contained models rather than canonical Mathlib definitions.

import PvsNP.Basic
import PvsNP.SAT
import PvsNP.CookLevin
import PvsNP.Relativization
import PvsNP.CircuitLowerBounds
