# Current State

**Date:** 2026-10-09
**Project:** Project Runtime Console
**Active round:** `PRC V1 repair planning and publication candidate review`

**Product status:** `NOT_ACCEPTED / RETURN_TO_REPAIR`. This tree is a clean
publication candidate, not a product-acceptance verdict.

## Repository State

The active tree was reduced to the Codex-native runtime substrate, the transcript/shadow judgment foundation, minimal tests, and the current PRC shell. Compatibility research evidence is maintained as a separate evidence bundle rather than as product runtime content. Git history remains the archive.

## Runtime Foundation

Retained runtime capabilities are:

- `packages/codex_runtime/`: read-only Codex app-server observation, native Thread identity, root-run grouping through `parentThreadId`, and native event projection.
- `packages/runtime_events/`: transcript tool-result parsing and stable event identity.
- `packages/judge_deepseek/`, `packages/judgment_sidecar/`, and `packages/judgment_ledger/`: bounded shadow judgment provider, receipt, sidecar, and replayable JSONL persistence.

No runtime, identity, lineage, or judgment semantics were changed by the cleanup.

## V1 Reuse Probe

Target: real Codex Run `01a0eca4-7029-7f92-b5a9-2006edb08721`.

Observed native shape from the read-only app-server observer: `1 root / 26 children`, `4,251` native events, and `69` turns. The sanitized fixture is retained in the separately classified evidence bundle and is not loaded by the runtime.

Trajectory local-only probe:

- Binary: Trajectory `0.6.0`, commit `f03a74b21d31e9d95e491f35cc4646d5262e3f76`.
- Local backfill/indexing completed against the Codex rollout corpus in an isolated temporary home; no remote MCP, OAuth, or Datadog publishing was used.
- `patterns session <ID> --json` produced real structured output: `codex`, `42` turns, `26` subagent invocations, `task_count: 0`, `19` commits, `124` Markdown files, and `9` test files in deliverable evidence.
- `patterns estimate --since 2026-09-29 --json` produced a no-inference cost estimate for `14` unclassified sessions. `patterns analyze --yes` was not run.

The session report did not produce human work/task boundaries. Therefore the probe is `PARTIAL`: it confirms local Codex recognition, backfill, indexing, turn/subagent/deliverable extraction, but not the required Planning, Research, Validation, Correction, Prototype, or Review segmentation.

Evidence is recorded in the separate PRC evidence-bundle manifest and the
direction-review receipts. The product tree does not claim that this probe
establishes WorkStage support.

## Verdict

Overall V1 reuse verdict remains `INCONCLUSIVE`. The Trajectory probe is stronger than the earlier command-not-found observation, but it still does not establish WorkStage compatibility.

## V1 Product Boundary

The approved Work B2 spatial map and Agents/Trace C v0.2 reading structure are
served from `apps/console/`. Work uses the original B2 `caseData` positions,
relations, translations, and evidence index. Agents and Trace keep the C-style
Run rail, spatial field, Focus Inspector, Turn groups, and native record modal.

```text
local Codex rollout JSONL
  -> read-only Session adapter
  -> shared Work / Agents / Trace shell
  -> B2 curated case or C native records
  -> source path + line + byte offset
```

The default real source is AISailing recruitment-related Session
`019faced-f11a-75e1-ac20-8b95e24d4628`: 5 turns, 313 native records, 35 tool
calls, and no confirmed native child-agent lineage. Work remains explicitly
`CURATED_CASE / REFERENCE_CASE`; it is not a claim that this Session produced
the AISailing evolution map.

Earlier browser verification covered the current shell at 1366x900 and
1600x900, but it does not establish product acceptance. The current repair
frontier remains native lineage/Turn ownership, Work activity evidence mapping,
B2 interaction parity, and C v0.2 Agents/Trace parity.

Remaining product boundary: the current native source does not expose confirmed
child-Agent identity, so the Agents surface intentionally remains an explicit
empty/unknown state. Work is still a curated reference surface rather than an
automatically reconstructed project history.

Review screenshots and DSH receipts are kept outside this clean product tree in
the separate local review bundle.

## Repair boundary

The internal planning graph is `Ticket 01 -> Ticket 02 -> {Ticket 03, Ticket
04}`. Ticket 04 owns the C v0.2 Agents topology/selection/focus surface and
Trace reading. This tree does not authorize implementation, ticket publication,
or remote mutation. The compatibility research bundle is separate from the
runtime and the old remote `main` remains the historical baseline.

## Validation

The retained Python smoke suite covers native observer projection, stable transcript event identity, shadow judgment, DSH receipt handling, and JSONL ledger replay.
