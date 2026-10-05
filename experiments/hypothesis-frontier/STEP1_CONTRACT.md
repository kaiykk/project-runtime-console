# Step 1 Hypothesis Frontier Contract

**Round:** `PRC-V0-STEP-1-SHADOW-TOOL-OUTPUT-20261005`

## Single Question

How should real Codex runtime events reliably enter the Shadow Judgment
Sidecar?

## Bounded Vertical Slice

```text
real Codex tool result
  -> runtime event ingestion
  -> normalized event
  -> DeepSeek shadow judgment
  -> local Judgment Ledger
  -> judgment visible on the matching trace event
```

Decision point: `tool.output.value`

Allowed verdicts:

```text
KEEP
ARCHIVE
DUPLICATE
IMPORTANT_PROGRESS
UNKNOWN
```

Mode: `SHADOW`

## Three Independent Hypotheses

### H1 — Transcript-first

Watch and parse `~/.codex/sessions`. Prediction: v0 can operate without hooks.

### H2 — Hook-first

Use a Codex lifecycle hook as the authoritative runtime source. Prediction:
hooks provide sufficient coverage and better realtime semantics. The hook
surface and coverage must be observed before this hypothesis can be marked
supported.

### H3 — Dual-channel

Reconcile hook and transcript observations. Prediction: hooks add live
semantics, transcripts add replay/history, and reconciliation produces a more
stable event. `HOOK_ONLY`, `TRANSCRIPT_ONLY`, `CORRELATED`, and `CONFLICT` must
remain distinguishable.

## Common Scenario

Where practical, all branches use the same disposable scenario:

- one main Agent;
- one subagent;
- at least three tool calls;
- corresponding results;
- task stop;
- no modification to unrelated repositories.

The scenario is evidence collection, not a product feature.

## Observation Criteria

Record only what can be observed:

- `EVENT_COVERAGE`
- `LATENCY`
- `ORDERING`
- `DUPLICATE_RATE`
- `AGENT_ATTRIBUTION`
- `TOOL_CALL_RESULT_CORRELATION`
- `REPLAYABILITY`
- `FUTURE_INTERVENTION_POTENTIAL`
- `IMPLEMENTATION_COMPLEXITY`
- `PROVIDER_COUPLING`

Do not invent numerical precision when a boundary is not measurable.

## Branch Output

Every branch must provide `HYPOTHESIS.md` with:

```text
CLAIM
WHY_PLAUSIBLE
PREDICTION
CHEAP_PROBE
OBSERVED_EVIDENCE
FALSIFIER_RESULT
KNOWN_GAPS
IMPLEMENTATION_COST
EXIT_COST
```

It must also provide a working code spike limited to the Step 1 question.
No full UI, full sidecar, orchestration, or active intervention is allowed.

## Isolation

Each branch must have a distinct Git branch and worktree from the same clean
baseline. No branch may inspect another branch's implementation before the
comparison step. The main integration branch remains untouched until the
commitment gate.

## Commitment Gate

The comparison must return exactly one of:

```text
COMMIT_H1
COMMIT_H2
COMMIT_H3
COMBINE_WITH_EXACT_SCOPE
INSUFFICIENT_EVIDENCE
```

If `INSUFFICIENT_EVIDENCE`, run exactly one additional cheap probe against the
unresolved discriminator. Do not open a broad new research campaign.

## Stop

After the winning slice, local audit, semantic smoke test, and final Global
Review, stop at `PRINCIPAL_REVIEW`. Do not start `task.frame`, completion
judgment, active intervention, Delegatus integration, DSH/Claude adapters,
Project Evolution, ThoughtDAG, or Hypothesis Frontier product UI.
