# PRC UI Convergence Round-Start Packet

```yaml
round_id: PRC-UI-CONVERGENCE-R1-20261006
project: Project Runtime Console
principal_input: /Users/kai/.codex/attachments/7f30e918-c149-4bb7-ba5d-b4ef6e2eac94/已粘贴的文本.txt
  principal_input_status: AMENDED_BY_PRINCIPAL_FRAME_EVOLUTION_DECISION
  round_status: PASS_B_COMPLETE__EXECUTION_PACKET_REQUIRED
model_shaping: YES
human_facing_artifact: YES
global_review_required: YES
intent_fidelity_required: YES
```

## Execution Correction

The supplied Principal input requests a new graph-first UI convergence round
and explicitly freezes the current three-column console as `UI_BASELINE_C0`.
It conflicts with the current repository boundary in two places:

- `docs/SHELL_FREEZE_V0.md` currently forbids a ThoughtDAG canvas.
- `docs/capability-imports/THOUGHTDAG.md` currently marks ThoughtDAG as
  `NOT_AUTHORIZED_FOR_V0`.

The Principal has now formally amended the presentation boundary. The
versioned amendment is `docs/ui-frame-change-v1.md`; the two affected files
are `docs/SHELL_FREEZE_V0.md` and `docs/capability-imports/THOUGHTDAG.md`.
The amendment authorizes ThoughtDAG-inspired graph-first Runtime Canvas work
as a Presentation / Interaction Layer only. It does not alter the runtime
model, identity contract, judgment sidecar, or observer-independence boundary.

The attached plan is also corrected in these ways:

1. Pass A blind Reference Precommit precedes any Manager frame proposal.
2. Pass B Frame Comparison must return `FRAME_OK` before variant
   implementation or a convergence harness is used for product changes.
3. The existing Runtime Observer backend and real historical runs remain the
   only data source; no fake topology is permitted.
4. Visual, UX, and Runtime Truth reviews are independent evidence paths.
5. A comparator may select `WINNER` and `RUNNER_UP` for Principal review, but
   neither result approves a product baseline or changes `main`.
6. The three-variant and two-refinement limits are hard stop rules, not a
   commitment to spend all iterations.

## Goal / Observation / Solution Hypothesis

**Goal:** determine, through bounded browser evidence, whether a graph-first
runtime presentation can make the real Project Runtime Console topology and
trace easier for a Human to understand than `UI_BASELINE_C0`, without changing
runtime truth, lineage, judgment authority, or execution behavior.

**Observation:** the current C0 implementation has confirmed Codex-native
root/child discovery and selected-agent history traces, but its presentation
is a three-column shell. The supplied Principal input reports that topology,
progressive disclosure, orientation, and trace continuity are not yet
immediately legible. That feedback is a Human-facing observation, not a
validated replacement information architecture.

**Solution Hypothesis:** a bounded, graph-first presentation with semantic
zoom and progressive disclosure may improve Human task performance while
preserving the existing `Project -> Run -> Agent topology -> Agent trajectory
-> runtime event -> optional shadow judgment` boundary. This remains a
hypothesis until independently reviewed and exercised in a browser.

## Current Phase Anchor

This is a UI-frame discovery and evidence round for Project Runtime Console.
It is not Product v0 approval, a runtime identity round, a DSH product Judge
round, or a phase transition.

## Non-Goals / Forbidden Growth

- no ThoughtDAG ontology, memory model, editable context edges, or model
  invocation logic;
- no Agent Monitor code or assets, because the local contract permits only a
  clean-room behavior reference;
- no DSH product Judge, active intervention, Control Plane, Task Board,
  Orchestrator, Project Evolution, or new runtime identity model;
- no fake nodes, fake events, or fabricated parent/child edges;
- no changes to Step 1 `canonical_event_id` semantics;
- no merging, promotion, or automatic change to the Product UI baseline;
- no claim that screenshots, `FRAME_OK`, local `PASS`, or a comparator result
  proves model validity or product utility.

## Required Review Route

```text
Principal input
  -> Global round-start review
  -> Pass A blind Reference Precommit
  -> Frame Proposal / Pass B Frame Comparison
  -> bounded harness and reference capture
  -> three isolated variants
  -> independent Visual / UX / Runtime Truth reviews
  -> comparator
  -> at most two winner refinements with regression rollback
  -> Intent Fidelity Review
  -> Global Review
  -> PRINCIPAL_REVIEW
```

The first local objective was intentionally narrower than the supplied full
round:

```text
RUN_PASS_A_REFERENCE_PRECOMMIT_ONLY
```

It produced the blind Reference Precommit. Following the Principal amendment,
Pass B has now returned `FRAME_OK`; the next action must still be separately
bounded and may not be inferred from this result.

Current checkpoint artifacts:

- `docs/ui-frame-change-v1.md`
- `experiments/ui-convergence/REFERENCE_FIRST_PRECOMMIT.md`
- `experiments/ui-convergence/FRAME_PROPOSAL.md`
- `experiments/ui-convergence/receipts/frame-pass-b.json`

## Human References

The Pass A reviewer may read only:

- `docs/NORTH_STAR.md`
- `docs/SHELL_FREEZE_V0.md`
- `docs/governance/GLOBAL_GOVERNANCE_BOOTSTRAP.md`
- `docs/governance/THREE_ROLE_BOOTSTRAP.md`
- `docs/capability-imports/AGENT_MONITOR.md`
- `docs/capability-imports/THOUGHTDAG.md`
- the supplied Principal input at
  `/Users/kai/.codex/attachments/7f30e918-c149-4bb7-ba5d-b4ef6e2eac94/已粘贴的文本.txt`

The reviewer must not receive Manager rationale, source code, implementation
plans, existing variant ideas, or a proposed winner.

## Decision Authority

```yaml
decision_authority:
  global_reviewer_can:
    - classify alignment and evidence sufficiency for this round-start gate
    - allow the single Pass A objective or stop/reopen it
    - identify one blocking frame question
  global_reviewer_cannot:
    - ratify the ThoughtDAG-inspired frame
    - modify North Star, Shell Freeze, or capability contracts
    - authorize Product v0 promotion or a phase transition
    - select a UI winner
    - authorize DSH product judgment or active intervention
  manager_can:
    - prepare the bounded packet and preserve source boundaries
    - execute only the explicitly allowed local objective
  manager_cannot:
    - treat the attachment as proof that the new frame is valid
    - skip Pass A / Pass B / Intent Fidelity review
    - silently resolve the Shell Freeze conflict
```

## Required Global Review Output

Return:

```text
GLOBAL_DECISION: GO_LOCAL | STOP_REFRAME | PRINCIPAL_REVIEW
LOCAL_OBJECTIVE: <one bounded objective or null>
WHY: <short evidence-bounded rationale>
DO_NOT_DO: [<explicit boundaries>]
REVIEW_SCOPE:
  reviewed: []
  not_reviewed: []
  cannot_conclude: []
ADVISORY_ONLY: YES
```
