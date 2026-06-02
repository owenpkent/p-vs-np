import Lake
open Lake DSL

package PvsNP where
  -- Add package configuration options here

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.13.0"

@[default_target]
lean_lib PvsNP where
  -- Library configuration
