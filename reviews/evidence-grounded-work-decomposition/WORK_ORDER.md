# Work Order: Evidence-Grounded Work Decomposition

## Project

Project Runtime Console

## Objective

Upgrade the real-run vertical slice from explicit user-message anchors to a
generic, evidence-grounded WorkStage projection for the real target run:

`01a0eca4-7029-7f92-b5a9-2006edb08721`

The product must let a Human inspect the major work that actually happened
without first reading the raw trace.

## Frozen boundaries

- Keep the V2.5 frontend interaction contract frozen.
- Do not hard-code a target-run stage list.
- Do not reuse the old static fixture narrative as ground truth.
- Do not force a Research stage when the run does not support one.
- Do not infer causality, contribution, completion, or outcome without evidence.
- Do not build Diagnostic White-box, add providers, or build a generalized platform.
- Preserve reversible navigation to native runtime records.

Derived semantics are allowed. Unsupported semantics must remain `UNKNOWN` or
`NOT ESTABLISHED`.

## Acceptance questions

Independently determine whether:

A. A Human can explain the main pieces of work that happened.
B. Meaningful branches or sub-stages are represented when the trajectory supports them.
C. Representative WorkStage title, outcome, and grouping trace to concrete runtime evidence.
D. The projection is independent of manually enumerated target-run stages.
E. Evidence drill-down terminates in real native records.

Do not optimize the implementation specifically for the wording of these
questions.

## Review subject

- Commit: `93e246fdefdf9d734d2858fc0024a4c4a9528ae3`
- Repository: `/Users/kai/Documents/project-runtime-console`
- Launch: `PYTHONPATH=. python apps/console/server.py 4174`
- URL: `http://127.0.0.1:4174/`
- Native source: Codex app-server observer
- Review permission: read-only; do not modify files or create commits

## Allowlisted evidence

- `apps/console/index.html`
- `apps/console/server.py`
- `packages/codex_runtime/observer.py`
- `packages/workstage_projection.py`
- `tests/test_workstage_projection.py`
- `experiments/v1-reuse-compatibility/evidence/prc-27-agent-sanitized-v2.json`
- `output/playwright/01-overview-real-run.png`
- `output/playwright/02-stage-with-branches.png`
- `output/playwright/03-selected-branch.png`
- `output/playwright/04-branch-raw-trace.png`
- `output/playwright/05-returned-overview-zoomed.png`

The browser is the primary acceptance surface. Treat implementation claims as
untrusted until verified in the running product and against native evidence.

## Stop and classification rule

Return one of `PASS`, `PARTIAL`, or `FAIL`. Classify each material failure as
`IMPLEMENTATION_FAILURE` or `MODEL_ASSUMPTION_FAILURE`.

`MODEL_ASSUMPTION_FAILURE` means the native trajectory cannot reliably support
the WorkStage abstraction or its required human meaning. Do not propose a new
architecture in that case; stop for Principal / Model Track review.
