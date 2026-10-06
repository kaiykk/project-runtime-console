# Project Runtime Console Session Protocol

This is a new repository. Do not use the archived
`project-evolution-state` repository, its research artifacts, its old
prototype, or any PES terminology as startup context.

## Startup

1. Read `README.md` and `docs/NORTH_STAR.md`.
2. Read `docs/SHELL_FREEZE_V0.md`.
3. Read `docs/governance/GLOBAL_GOVERNANCE_BOOTSTRAP.md`.
4. Read `docs/governance/THREE_ROLE_BOOTSTRAP.md` and resolve the pinned
   canonical Home Project SOP files before any bounded governance round.
5. Read the capability-import contracts under
   `docs/capability-imports/`.
6. Read the current Step 1 contract under
   `experiments/hypothesis-frontier/STEP1_CONTRACT.md`.
7. Run `git status --short --branch`.
8. Confirm the active bounded question before editing.

Before any non-trivial, Human-facing, or model-shaping governance round:

1. Run the DSH preflight from the local governance bootstrap.
2. Confirm the Global Reviewer route before Manager execution.
3. Use the canonical Home Project packet and receipt contract.
4. Do not claim DSH review without a `governance_audit_receipt`.
5. If the canonical SOP or DSH review route is unavailable, return
   `REVIEW_ROUTE_UNAVAILABLE` and `STOP_AND_REPORT`.

Before implementing Codex runtime semantics, use this authority order:
OpenAI Codex current protocol/source, the pinned MIT Delegatus implementation
where relevant, local compatibility evidence, then a new hypothesis only for
an unresolved gap. Do not create a probe to re-prove semantics already defined
by an upstream surface. Record the checked Codex version, protocol surface,
and any unavailable method in the execution receipt. Do not infer a native
runtime field from transcript shape when the upstream surface defines it;
unresolved compatibility remains `UNKNOWN`.

## Non-Negotiable Boundaries

- Step 1 is limited to runtime event ingestion into the Shadow Judgment
  Sidecar.
- All judgments are `SHADOW`; they cannot block, mutate, stop, trigger, or
  otherwise alter Codex execution.
- `tool.output.value` must be attached to a stable canonical event identity.
  Timestamp-only matching is not sufficient.
- A product Judge call may be claimed only when a real product provider receipt
  exists. A product provider receipt is not a governance audit receipt.
- A DSH governance review may be claimed only when a canonical packet was
  reviewed and a `governance_audit_receipt` exists.
- No secrets, API keys, raw private transcripts, or hidden reasoning may be
  committed.
- H1, H2, and H3 experiments must use distinct branches/worktrees from one
  clean baseline. A session fork alone is not Git isolation.
- Do not add Task Board, Orchestrator, Pipeline, Project Evolution, Workline,
  Control Plane, Memory, Hive, ThoughtDAG product ontology, editable runtime
  lineage, context-edge semantics, or active-intervention UI. A
  ThoughtDAG-inspired graph-first Runtime Canvas is authorized only as the
  read-only Presentation / Interaction Layer under
  `docs/ui-frame-change-v1.md`.
- Do not treat `FRAME_OK`, a passing test, or a plausible screenshot as proof
  of model validity.

## Change Classification

Routine implementation can use local review. Changes to product information
architecture, event identity, judgment authority, runtime topology, or
shadow-mode semantics are model-shaping and require the global governance
bootstrap route.

## Governance Invariants

Freeze protects against premature drift; evolution protects against frozen
mistakes. Classify evaluation failures as follows:

```text
IMPLEMENTATION_FAILURE
  -> repair the current frame
MODEL_ASSUMPTION_FAILURE
  -> bounded model repair
FRAME_CONTRADICTION
  -> FRAME_REOPEN_CANDIDATE
```

Only the Human Principal may `AMEND` or `SUPERSEDE` a frozen frame. Reviewer
verdicts and passing tests do not silently change a frozen boundary.

For semantics owned by an external system, use this authority order:

```text
official upstream contract/source
  -> mature prior art
  -> local compatibility validation
  -> hypothesis search only for unresolved gaps
```

Do not create a new large governance framework to compensate for an unverified
upstream fact.

## Reporting

Human-facing HTML reports must be in Chinese. Reports must distinguish
confirmed evidence, observed behavior, hypothesis, and unknown. Never
fabricate a provider result, runtime event, or outcome.
