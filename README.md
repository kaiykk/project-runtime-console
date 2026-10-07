# Project Runtime Console

Project Runtime Console inspects real Codex multi-agent runs while preserving native runtime truth, native parent-child lineage, and read-only behavior.

## North Star

A Human can inspect a real run, understand which Agents participated, open native runtime evidence, and see any independent shadow judgment attached to that evidence without confusing observation with intervention or engineering outcome.

## Experience Star

```text
Project -> Run -> Agent topology -> selected Agent -> runtime evidence
                                      \\-> shadow judgment (if present)
```

The experience must make global structure and local evidence reachable without inventing task meaning, outcomes, or lineage.

## V1 Scope

- Preserve the Codex-native Runtime Observer and runtime substrate.
- Keep the transcript event parser, shadow provider boundary, judgment sidecar, and replayable ledger as the minimal foundation.
- Evaluate mature upstream observability and work-segmentation capabilities against one real 27-Agent run before implementing new product primitives.
- Use the frozen V2.5 interaction contract as a replaceable presentation shell for the first real-run vertical slice.
- Treat `experiments/v1-reuse-compatibility/` as evidence, not production ontology or a WorkStage classifier.

The current compatibility result is `INCONCLUSIVE`: the local Trajectory probe produced real session/turn/deliverable data but no task boundaries, and the remaining upstream interaction findings require adaptation rather than direct semantic import. See `docs/current-state.md` and the V1 evidence files.

## V2.5 Real-Run Slice

`apps/console/` serves the frozen V2.5 spatial map from a read-only Codex
native observer. The current target is the historical run
`01a0eca4-7029-7f92-b5a9-2006edb08721`. WorkStage labels are a bounded
projection from explicit user-message anchors; every displayed native record
keeps its observer identity and can be opened through
`Outcome -> Evidence -> Raw Trace`.

This slice is intentionally `PARTIAL`: runtime facts and raw evidence are
real, while completion, contribution, outcome, and causality remain
`UNKNOWN / NOT ESTABLISHED` unless native evidence proves them.

## Explicitly Out Of Scope

No new graph/layout system, WorkStage classifier, Diagnostic White-box,
control plane, orchestration, or active intervention is included. The V2.5
page is a frozen interaction baseline, not a commitment to a final product
architecture.
