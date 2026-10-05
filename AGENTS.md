# Project Runtime Console Session Protocol

This is a new repository. Do not use the archived
`project-evolution-state` repository, its research artifacts, its old
prototype, or any PES terminology as startup context.

## Startup

1. Read `README.md` and `docs/NORTH_STAR.md`.
2. Read `docs/SHELL_FREEZE_V0.md`.
3. Read `docs/governance/GLOBAL_GOVERNANCE_BOOTSTRAP.md`.
4. Read the four capability-import contracts under
   `docs/capability-imports/`.
5. Read the current Step 1 contract under
   `experiments/hypothesis-frontier/STEP1_CONTRACT.md`.
6. Run `git status --short --branch`.
7. Confirm the active bounded question before editing.

## Non-Negotiable Boundaries

- Step 1 is limited to runtime event ingestion into the Shadow Judgment
  Sidecar.
- All judgments are `SHADOW`; they cannot block, mutate, stop, trigger, or
  otherwise alter Codex execution.
- `tool.output.value` must be attached to a stable canonical event identity.
  Timestamp-only matching is not sufficient.
- A real DeepSeek call may be claimed only when a real response receipt exists.
  Without `DEEPSEEK_API_KEY`, use a deterministic fake provider and record
  `HUMAN_SETUP_REQUIRED`.
- No secrets, API keys, raw private transcripts, or hidden reasoning may be
  committed.
- H1, H2, and H3 experiments must use distinct branches/worktrees from one
  clean baseline. A session fork alone is not Git isolation.
- Do not add Task Board, Orchestrator, Pipeline, Project Evolution, Workline,
  Control Plane, Skill, Memory, Hive, ThoughtDAG, or active-intervention UI.
- Do not treat `FRAME_OK`, a passing test, or a plausible screenshot as proof
  of model validity.

## Change Classification

Routine implementation can use local review. Changes to product information
architecture, event identity, judgment authority, runtime topology, or
shadow-mode semantics are model-shaping and require the global governance
bootstrap route.

## Reporting

Human-facing HTML reports must be in Chinese. Reports must distinguish
confirmed evidence, observed behavior, hypothesis, and unknown. Never
fabricate a provider result, runtime event, or outcome.
