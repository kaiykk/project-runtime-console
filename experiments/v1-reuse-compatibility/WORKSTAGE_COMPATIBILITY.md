# WORKSTAGE_COMPATIBILITY

Round: `V1 Reuse & Compatibility`

## Q1 — What did Trajectory segment?

The local-only Trajectory probe recognized and indexed the real Run
`01a0eca4-7029-7f92-b5a9-2006edb08721`, but it did not produce Human work
boundaries.

The requested command was executed against the real Run
`01a0eca4-7029-7f92-b5a9-2006edb08721`:

```text
trajectory patterns session 01a0eca4-7029-7f92-b5a9-2006edb08721 --json
```

The saved structured output reports:

```text
client_source: codex
turn_count: 42
subagent_invocations: 26
task_count: 0
tasks: null
commits: 19
markdown_files_written: 124
test_files_written: 9
file_changing_turns: 21
```

The local binary was Trajectory `0.6.0`, commit
`f03a74b21d31e9d95e491f35cc4646d5262e3f76`. Backfill/indexing ran against an
isolated temporary home: `86` Codex rollout files were seen and `64` sessions
were indexed in the bounded batch. No Datadog remote MCP, OAuth, or publishing
was used.

The earlier command-not-found attempt and the remote MCP `401 Unauthorized`
remain historical attempts recorded in
`evidence/datadog-capability-probe.json`; they are not the final local probe
result. `patterns estimate --since 2026-09-29 --json` also ran and reported
`14` unclassified sessions, `135` turns to analyze, and an estimated cost of
`0.0840568` USD. `patterns analyze --yes` was not run.

The real local PRC evidence confirms the input shape only:

```text
1 root / 26 children
4,186 native events
67 turns
64 completed turns / 3 interrupted turns
```

The output contains session activity and deliverable evidence, not Trajectory
task/work boundaries. The native event mix
(`commandExecution`, `fileChange`, `collabAgentToolCall`, and others) is not a
human work taxonomy. Therefore no claim can be made that the run was segmented
into Planning, Research, Validation, Correction, Prototype, or Review.

**Q1 result: PARTIAL / NO_HUMAN_WORK_BOUNDARIES_OBSERVED.**

## Q2 — Can a thin WorkStage projection stay evidence-grounded?

The temporary strict projection was run as a contract check against the
available evidence. It received no Trajectory task/work records. It therefore
emitted zero WorkStages and rejected the projection:

```text
title: BLACK_BOX
outcome: BLACK_BOX
reason: no source task refs or Trajectory evidence refs
```

Using event counts or tool names to invent stages would create an LLM summary
black box. The projection cannot be called compatible because this probe did
not supply Trajectory task references and evidence references for derived
title/outcome fields. The successful session report is evidence of recognition
and deliverables, not sufficient input for WorkStage projection.

**Q2 result: NOT ESTABLISHED.**

## Q3 — Reuse findings

The source-backed findings are in `V1_REUSE_MATRIX.md`:

- Langfuse graph mechanics are `ADAPT`, not `DIRECT_REUSE`, because its
  observation model, timing-derived edge rules, layout worker, and selection
  state are coupled to Langfuse contracts.
- AgentProvenance's bounded lens, local focus, side detail, raw evidence, and
  derived-edge labeling are useful `PATTERN_ONLY` or `ADAPT` references. Its
  Apache-2.0 code has a clearer attribution boundary, but its security
  provenance ontology is not a PRC WorkStage ontology.
- Trailblaze is unverified because no unique source/license/revision was found.

No interaction implementation was copied or added to production PRC.

## Q4 — Can upstreams share one PRC selection/view state?

Only a neutral adapter boundary is supported by the evidence:

```text
selected native Agent / runtime event
    -> bounded focus / expansion state
    -> upstream renderer or local evidence view
```

The evidence does not support importing either upstream ontology, timing
inference, security lens, or task taxonomy as PRC semantics. A shared PRC
selection/view state is therefore plausible as an adapter concern, but it was
not implemented or integration-tested in this round.

## Minimum WorkStage Contract Assessment

The proposed fields are sufficient as an output boundary only if every
non-native `title` and `outcome` carries source/evidence references:

```text
id
title
outcome
status
parent_stage_id
source_task_refs
evidence_refs
```

The contract is not sufficient to manufacture segmentation. It depends on an
upstream structured task/work evidence producer and on a projection that does
not hide its derivation. With the current evidence, the correct output is
`BLACK_BOX`, not a guessed WorkStage.

## Verdict

```text
INCONCLUSIVE
```

Reason: the primary real-world local Trajectory probe executed and produced
structured session activity, cost, and deliverable evidence, but no task/work
segmentation. Q1 is therefore only partial and Q2 remains unestablished. The
interaction reuse study does show a credible hybrid reuse path for
graph/layout/focus mechanics, but it cannot determine whether PRC can be
mostly assembled from mature capabilities while owning only a minimal
WorkStage contract. No production implementation is authorized by this
result.

## Evidence Index

- `evidence/datadog-capability-probe.json`
- `evidence/real-run-observation-summary.json`
- `evidence/workstage-projection.json`
- Existing sanitized input fixture:
  `evidence/prc-27-agent-sanitized-v2.json`
- Langfuse disposable clone:
  `8b587645cf144b7bdf27883f59cd2c2e39552471`
- AgentProvenance disposable clone:
  `24765384a83047693b849b1be6b0c17116be558a`
