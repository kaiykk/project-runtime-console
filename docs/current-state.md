# Current State

**Date:** 2026-10-07
**Project:** Project Runtime Console
**Active round:** `V2.5 real-run vertical slice`

## Repository State

The active tree was reduced to the Codex-native runtime substrate, the transcript/shadow judgment foundation, minimal tests, and the V1 compatibility evidence. Former console, graph prototypes, OpenDesign studies, identity experiments, governance packets, and other superseded temporary work are not part of the active tree. Git history remains the archive; no archive folder was created.

## Runtime Foundation

Retained runtime capabilities are:

- `packages/codex_runtime/`: read-only Codex app-server observation, native Thread identity, root-run grouping through `parentThreadId`, and native event projection.
- `packages/runtime_events/`: transcript tool-result parsing and stable event identity.
- `packages/judge_deepseek/`, `packages/judgment_sidecar/`, and `packages/judgment_ledger/`: bounded shadow judgment provider, receipt, sidecar, and replayable JSONL persistence.

No runtime, identity, lineage, or judgment semantics were changed by the cleanup.

## V1 Reuse Probe

Target: real Codex Run `01a0eca4-7029-7f92-b5a9-2006edb08721`.

Observed native shape from the read-only app-server observer: `1 root / 26 children`, `4,251` native events, and `69` turns. The sanitized fixture is retained at `experiments/v1-reuse-compatibility/evidence/prc-27-agent-sanitized-v2.json`.

Trajectory local-only probe:

- Binary: Trajectory `0.6.0`, commit `f03a74b21d31e9d95e491f35cc4646d5262e3f76`.
- Local backfill/indexing completed against the Codex rollout corpus in an isolated temporary home; no remote MCP, OAuth, or Datadog publishing was used.
- `patterns session <ID> --json` produced real structured output: `codex`, `42` turns, `26` subagent invocations, `task_count: 0`, `19` commits, `124` Markdown files, and `9` test files in deliverable evidence.
- `patterns estimate --since 2026-09-29 --json` produced a no-inference cost estimate for `14` unclassified sessions. `patterns analyze --yes` was not run.

The session report did not produce human work/task boundaries. Therefore the probe is `PARTIAL`: it confirms local Codex recognition, backfill, indexing, turn/subagent/deliverable extraction, but not the required Planning, Research, Validation, Correction, Prototype, or Review segmentation.

Evidence:

- `experiments/v1-reuse-compatibility/evidence/trajectory-patterns-session-01a0eca4-7029-7f92-b5a9-2006edb08721.json`
- `experiments/v1-reuse-compatibility/evidence/trajectory-patterns-estimate-2026-09-29.json`
- `experiments/v1-reuse-compatibility/evidence/datadog-capability-probe.json`
- `experiments/v1-reuse-compatibility/V1_REUSE_MATRIX.md`
- `experiments/v1-reuse-compatibility/WORKSTAGE_COMPATIBILITY.md`

## Verdict

Overall V1 reuse verdict remains `INCONCLUSIVE`. The Trajectory probe is stronger than the earlier command-not-found observation, but it still does not establish WorkStage compatibility.

## V2.5 Real-Run Vertical Slice

The frozen V2.5 interaction shell is now served at `apps/console/` and reads
the target run through `CodexRuntimeObserver` at request time. The actual path
is:

```text
Codex app-server (read-only)
  -> native agents / turns / events
  -> bounded user-anchor projection
  -> V2.5 WorkStage spatial map
  -> drawer Evidence
  -> native Raw Trace records
```

The browser probe verified the overview, stage selection, Evidence navigation,
Raw Trace navigation, return navigation, and zoom using the real run. The
overview displayed `27` agents, `26` children, `4251` native events, `69` turns,
and available history. Raw Trace displayed real `userMessage`, `agentMessage`,
and `commandExecution` records with native IDs and command completion state.

The projection remains `PARTIAL`: WorkStage titles are derived navigation
labels from explicit user-message anchors; native runtime does not establish
the displayed work outcomes, complete causality, or contribution semantics.
The five acceptance questions therefore cannot all be answered from this
slice without unsupported interpretation.

Checkpoint: `frontend-v1-baseline-v2.5`.

## Validation

The retained Python smoke suite covers native observer projection, stable transcript event identity, shadow judgment, DSH receipt handling, and JSONL ledger replay.
