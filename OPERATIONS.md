# Operations Guide: AI-augmented (and AI-only) execution of the P vs NP proof program

> How to run this repo as the operational substrate for the proof program. The
> current mode is AI-augmented (human owner in the critical path). The AI-only
> variant requires infrastructure not yet built (see §7).
>
> **Scope**: how to launch sessions, deploy agents, maintain state, escalate to
> human review. Not the mathematical content (that lives in `experiments/`,
> `docs/03_research/`, `lean/`).

## 1. The repo as substrate

| Component | Path | Role |
|---|---|---|
| Agent role specifications | [`.claude/agents/`](.claude/agents/) | Six specialized agents: surveyor, builder, verifier, adversary, synthesizer, orchestrator. |
| Phase state | [`PHASE_STATE.md`](PHASE_STATE.md) | Current phase, sub-task, last verification, next steps. Read by ORCHESTRATOR at start of every session. |
| Project narrative | [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md) | Cross-architecture findings. Updated by SYNTHESIZER. |
| Status table | [`experiments/PLAN.md`](experiments/PLAN.md) | Per-experiment status. |
| Strategic snapshot | [`STATE_OF_THE_PROGRAM.md`](STATE_OF_THE_PROGRAM.md) | One-page repo-wide strategic state. |
| Research directions | [`docs/03_research/research_directions/`](docs/03_research/research_directions/) | Per-direction execution roadmaps. |
| Formal verification | [`lean/`](lean/) | Lean 4 / Mathlib project. Structural claims verified here are canonical. |
| Persistent memory | [`memory/MEMORY.md`](memory/MEMORY.md) | Cross-session context. Read at session start. |

## 2. The session loop

### 2.1 Session start

1. ORCHESTRATOR reads [`PHASE_STATE.md`](PHASE_STATE.md) and
   [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md).
2. ORCHESTRATOR decides the session goal from the prior session's recommended
   next steps.
3. ORCHESTRATOR deploys agents via the `Agent` tool with `subagent_type` matching
   the role (e.g. `subagent_type: surveyor`).

### 2.2 Agent deployment (parallel where possible)

For mapping work:
- Deploy 1-3 SURVEYORs on the relevant sub-corpus.
- Deploy 3-5 BUILDERs on the same research direction with different attack angles.
- Deploy 1-2 VERIFIERs to formalize BUILDER outputs.
- Deploy 1-2 ADVERSARYs to run the three-barrier discipline.

### 2.3 Synthesis

After agent outputs land, deploy SYNTHESIZER to integrate them and update
[`experiments/LEARNINGS.md`](experiments/LEARNINGS.md),
[`experiments/PLAN.md`](experiments/PLAN.md), and
[`PHASE_STATE.md`](PHASE_STATE.md).

### 2.4 Session end

ORCHESTRATOR writes to [`PHASE_STATE.md`](PHASE_STATE.md): current phase +
sub-task, sessions used / budgeted, pending agent outputs, recommended next
deployments, and any falsifiability triggers approaching or hit.

### 2.5 Commit

The session's work is committed with a clear message, for example
"Phase X.Y: BUILDER outputs + VERIFIER results + ADVERSARY barrier findings".

## 3. The barrier discipline gate

Every candidate technique passes through the three-barrier checker
([`experiments/_shared/barriers.py`](experiments/_shared/barriers.py)) BEFORE any
deeper investment. A technique that hits a barrier is not pursued unless the
BUILDER's writeup explains exactly how it evades that barrier (as Williams's ACC0
technique does). This is the operational form of the wrong-approach discipline.

## 4. Verification stack

Every claim should pass through layers before becoming canonical:

1. **Mechanical computation**: at least two independent code paths, agreement
   required.
2. **Symbolic verification**: `sympy` where applicable.
3. **Formal proof in Lean 4**: structural claims formalized in
   [`lean/PvsNP/`](lean/PvsNP/) and proved via Mathlib.
4. **Multi-agent consensus**: independent VERIFIER runs produce the same
   conclusion.

A claim is canonical when all applicable layers agree. Until then it is
provisional and marked as such.

## 5. Escalation to human review

Certain decisions warrant human review:
- **A claimed proof that $\mathsf{P} = \mathsf{NP}$ or $\mathsf{P} \ne \mathsf{NP}$**:
  submit to human peer review before any public claim. The Clay problem has a
  long history of false proofs; the bar is extreme.
- **A claimed technique that evades all three barriers**: this is the rare and
  valuable case. Verify the barrier-evasion claims against multiple independent
  arguments before celebrating.
- **A discovery that the architectural picture is wrong**.

ORCHESTRATOR flags such situations and pauses pending human input.

## 6. Falsifiability triggers

The program is restructured if:
- A candidate circuit-lower-bound technique is shown to be natural (so it falls
  to Razborov-Rudich) after being claimed non-natural.
- A claimed separation is shown to relativize or algebrize.
- A direction makes no progress for N sessions.

ORCHESTRATOR tracks these in [`PHASE_STATE.md`](PHASE_STATE.md).

## 7. Costs and prerequisites for AI-only execution

To run a serious autonomous program would require multi-agent orchestration
software, a large Lean 4 / Mathlib expansion (complexity theory is thinly
formalized as of 2026), scheduled execution, and a substantial compute budget.
As of 2026 this is a target design, not an operating program. The current mode is
AI-augmented with the human owner in the critical path.

## 8. For someone picking up this repo

1. **Read** [`PHASE_STATE.md`](PHASE_STATE.md) for current state.
2. **Read** [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md) for the
   cumulative narrative.
3. **Read** [`.claude/agents/orchestrator.md`](.claude/agents/orchestrator.md) for
   how to drive sessions.
4. **Run** one ORCHESTRATOR session to plan the next phase.
5. **Deploy** the agents ORCHESTRATOR recommends.
6. **Commit** the session's work with a clear message.
7. **Update** PHASE_STATE.md for the next session.

This is iterative. The compounding effect across many sessions is what produces
the program output.
