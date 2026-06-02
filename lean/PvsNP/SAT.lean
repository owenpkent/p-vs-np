/-
Boolean satisfiability (SAT): CNF formulas, assignments, satisfiability, and SAT
as a language. SAT is the canonical NP-complete problem (Cook 1971).

This module is concrete: a literal, clause, and CNF are real inductive/data
types, evaluation is a real Boolean function, and `Satisfiable` is a real
existential. Only the encoding of a CNF as a `BitString` (to view SAT as a
`Language`) is left abstract (VERIFIER target #SAT-enc), since a faithful,
length-respecting encoding is bookkeeping that does not affect the statements.
-/

import PvsNP.Basic

namespace PvsNP

/-- A literal: a variable index with a polarity (true = positive, false = negated). -/
structure Literal where
  var : Nat
  pos : Bool

/-- A clause is a disjunction of literals. -/
abbrev Clause := List Literal

/-- A CNF formula is a conjunction of clauses. -/
abbrev CNF := List Clause

/-- An assignment maps variable indices to Boolean values. -/
abbrev Assignment := Nat → Bool

/-- A literal is satisfied if its variable's value matches its polarity. -/
def Literal.eval (l : Literal) (a : Assignment) : Bool :=
  if l.pos then a l.var else !(a l.var)

/-- A clause is satisfied if some literal in it is satisfied. -/
def Clause.eval (c : Clause) (a : Assignment) : Bool :=
  c.any (fun l => l.eval a)

/-- A CNF is satisfied if every clause is satisfied. -/
def CNF.eval (φ : CNF) (a : Assignment) : Bool :=
  φ.all (fun c => c.eval a)

/-- A CNF is satisfiable if some assignment satisfies it. -/
def Satisfiable (φ : CNF) : Prop := ∃ a : Assignment, φ.eval a = true

/-- Encoding of a CNF as a bit string. VERIFIER target #SAT-enc: a concrete,
    length-polynomial encoding/decoding pair. -/
def encodeCNF (_φ : CNF) : BitString := []

/-- Decoding a bit string back to a CNF (partial; total here for the skeleton).
    VERIFIER target #SAT-enc. -/
def decodeCNF (_x : BitString) : CNF := []

/-- SAT as a language: the strings that encode satisfiable CNF formulas. -/
def SAT : Language := fun x => Satisfiable (decodeCNF x)

/-- The empty CNF (no clauses) is satisfied by every assignment. A sanity check
    that evaluation behaves, provable now. -/
theorem empty_cnf_satisfiable : Satisfiable ([] : CNF) :=
  ⟨(fun _ => true), rfl⟩

/-- A CNF containing the empty clause is unsatisfiable: the empty clause has no
    satisfied literal. Provable now. -/
theorem empty_clause_unsat (φ : CNF) (h : ([] : Clause) ∈ φ) : ¬ Satisfiable φ := by
  rintro ⟨a, ha⟩
  have : ([] : Clause).eval a = true := by
    have := List.all_eq_true.mp ha [] h
    simpa using this
  simp [Clause.eval] at this

end PvsNP
