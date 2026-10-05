# Step 1 Frame Proposal

**Round:** `PRC-V0-STEP-1-SHADOW-TOOL-OUTPUT-20261005`  
**Status:** bounded execution frame; Human product direction is frozen

## Problem

The console needs a reliable, evidence-backed way to receive a real Codex
tool-result event and attach an independent shadow judgment to the same trace
event.

## Frozen Frame

The product shell is Agent Monitor-style runtime observability:

```text
Project -> Run -> Agent Topology -> Trace -> Shadow Judgment
```

The judgment is a local sidecar observation. It does not control Codex.

## Operational Assumptions to Test

- Transcript watching may provide sufficient v0 event coverage.
- Codex hooks may provide a better live event source, but their actual
  coverage is unverified.
- Hooks and transcripts may need reconciliation, but dual-channel complexity
  must be measured rather than assumed.
- A canonical event must have a stable identity or an explicit unresolved
  correlation state.
- A DeepSeek provider is a boundary adapter, not a source of runtime truth.

## Corrections Applied Before Execution

1. H1/H2/H3 start from one clean repository baseline with distinct
   branch/worktree identities.
2. H2 cannot claim support until the actual local Codex hook surface and
   event coverage are observed.
3. `tool.output.value` is a target decision point, not proof that every input
   source exposes that field.
4. Timestamp-only deduplication and correlation are prohibited.
5. Real provider use requires a bounded, redacted input and a persisted
   response receipt. A fake provider is the only valid fallback.
6. A disposable test task must avoid unrelated repositories and must not
   modify the product repository except within the designated experiment
   branch/worktree.

## Exact Output

The round may produce:

- three bounded hypothesis spikes;
- one evidence matrix;
- one commitment decision;
- one winning Step 1 vertical slice;
- local correctness evidence;
- one Chinese human-facing semantic smoke-test artifact;
- one compact `HUMAN_REVIEW_PACKET.md`.

It may not produce a Control Plane, active intervention, later judgment points,
Delegatus integration, DSH/Claude adapters, ThoughtDAG UI, or a Hypothesis
Frontier product surface.
