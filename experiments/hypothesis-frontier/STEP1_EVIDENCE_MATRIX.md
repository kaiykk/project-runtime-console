# Step 1 Evidence Matrix

**Round:** `PRC-V0-STEP-1-SHADOW-TOOL-OUTPUT-20261005`  
**Comparison date:** 2026-10-05  
**Scope:** independent comparison of the completed H1, H2, and H3 spikes only.

## Commitment

`COMMIT_H1`

The committed scope is transcript-first ingestion for the bounded Step 1
observation path:

- watch an available Codex session JSONL file;
- normalize only observed `function_call_output` and
  `custom_tool_call_output` records;
- require stable `session_id` and `call_id` evidence, with source ordinal
  retained for deterministic event identity;
- preserve `PARTIAL` or `UNKNOWN` when identity is incomplete;
- keep live latency, rotation, multi-agent attribution, deduplication policy,
  hook delivery, and intervention behavior explicitly unresolved.

This is a commitment to the input-path direction, not authorization to build
the sidecar, provider, ledger, UI, orchestration, or intervention behavior.

## Rating Rule

- `SUPPORTED`: direct evidence demonstrates the criterion within the stated
  bounded scenario.
- `PARTIAL`: direct evidence covers a material subset, but an important
  scenario or operational dimension remains unresolved.
- `WEAK`: only fixture behavior, implementation shape, or indirect capability
  evidence exists; the criterion is not demonstrated on the live source.
- `UNKNOWN`: the criterion was not measured or the available evidence cannot
  support a bounded claim.

## Evidence Sources

The three directories below were read as external, read-only evidence. No file
in them was modified.

- **H1:** `/Users/kai/Documents/project-runtime-console-worktrees/h1/experiments/hypothesis-frontier/h1-transcript-first/`
- **H2:** `/Users/kai/Documents/project-runtime-console-worktrees/h2/experiments/hypothesis-frontier/h2-hook-first/`
- **H3:** `/Users/kai/Documents/project-runtime-console-worktrees/h3/experiments/hypothesis-frontier/h3-dual-channel/`

Line references below are relative to the named hypothesis directory.

## Matrix

| Criterion | H1: transcript-first | H2: hook-first | H3: dual-channel |
|---|---|---|---|
| `EVENT_COVERAGE` | **PARTIAL**. `HYPOTHESIS.md:44-66` reports 35 output records in one inspected session and 23 distinct output call IDs; `transcript_watcher.py:11-15` recognizes both observed output record types. Boundary: one session only; non-tool, multi-agent, rotation, and future-schema coverage remain `UNKNOWN`. | **UNKNOWN**. `HYPOTHESIS.md:44-58` records config, CLI, and binary-symbol evidence but no delivered `PostToolUse` stdin payload. Boundary: capability names do not establish runtime delivery or coverage. | **UNKNOWN**. `HYPOTHESIS.md:41-53` explicitly limits the result to sanitized fixtures and says no live hook or transcript source was exercised. Boundary: source coverage is unmeasured. |
| `LATENCY` | **UNKNOWN**. `HYPOTHESIS.md:64-66,75-80` says append latency and flush behavior were not measured; `transcript_watcher.py:160-195` implements polling but does not measure timing. Boundary: no live latency claim. | **UNKNOWN**. `HYPOTHESIS.md:68-81` lists latency as unproven because no hook event was delivered. Boundary: hook positioning is not a latency measurement. | **UNKNOWN**. `HYPOTHESIS.md:52-64` reports no live source, buffering, retry, or late-arrival probe. Boundary: reconciliation fixtures contain no timing evidence. |
| `ORDERING` | **PARTIAL**. `HYPOTHESIS.md:46-53` reports 113 ordinal-bearing records with no descending or duplicate ordinal transitions; `transcript_watcher.py:124-157,169-195` consumes records sequentially. Boundary: out-of-order arrival, flush boundaries, rotation, and late records were not tested. | **UNKNOWN**. `HYPOTHESIS.md:68-81` explicitly leaves ordering unproven. Boundary: binary strings and hook configuration provide no delivered sequence. | **UNKNOWN**. `reconcile.py:119-207` has no buffering or out-of-order policy, and `HYPOTHESIS.md:60-66` names ordering as a gap. Boundary: fixture input order is not runtime ordering evidence. |
| `DUPLICATE_RATE` | **WEAK**. `HYPOTHESIS.md:49-52` observes 35 output records versus 23 distinct output call IDs, showing repeats are possible but not measuring a rate or defining deduplication. Boundary: repeated records may be retries, duplicates, or valid repeated observations. | **UNKNOWN**. `HYPOTHESIS.md:68-81` reports duplicate behavior as unproven, and no hook payload was observed. Boundary: no delivery sample exists. | **WEAK**. `HYPOTHESIS.md:43-50` and `reconcile.py:210-224` demonstrate same-channel collapse for identical stable identity plus semantic payload. Boundary: no live duplicate rate and no divergent-duplicate resolution policy. |
| `AGENT_ATTRIBUTION` | **UNKNOWN**. `HYPOTHESIS.md:64-66,75-82` explicitly marks agent or parent/child attribution as unknown. Boundary: session and turn identifiers are not agent topology. | **WEAK**. `HYPOTHESIS.md:52-55` finds candidate `agent_id` and `thread_id` strings; `hook_adapter.py:93-110` can retain one when present. Boundary: the fields came from binary strings or synthetic tests, not a delivered hook payload. | **WEAK**. `reconcile.py:37-40,105-115` carries `agent_id`, and `test_reconcile.py:6-19` uses it in fixtures. Boundary: the reconciler does not establish how upstream runtime events obtain trustworthy attribution. |
| `TOOL_CALL_RESULT_CORRELATION` | **SUPPORTED** within the observed transcript shape. `HYPOTHESIS.md:46-62` reports all 23 output IDs matched a prior call ID; `transcript_watcher.py:73-99,130-157` carries session, turn, call, tool, ordinal, and explicit unresolved states; `test_transcript_watcher.py:24-44` verifies deterministic correlation. Boundary: one inspected source shape and no sidecar delivery. | **WEAK**. `hook_adapter.py:70-112` and `test_hook_first.py:29-50` normalize a synthetic `PostToolUse` payload using stable IDs. Boundary: `HYPOTHESIS.md:56-64` confirms no real hook payload, so source-to-result correlation is unproven. | **WEAK**. `HYPOTHESIS.md:17-26` and `reconcile.py:125-128,227-233` correlate stable event/provider identifiers. Boundary: this is cross-channel reconciliation of already-sanitized events, not observation of a tool call/result pair. |
| `REPLAYABILITY` | **SUPPORTED** for available transcript files. `HYPOTHESIS.md:3-9,29-36` frames offline/replay observation; `transcript_watcher.py:103-195` parses deterministic ordered JSONL and holds incomplete lines; `test_transcript_watcher.py:137-146` verifies replay from a fixture. Boundary: file discovery, rotation, truncation, locking, and retention were not measured. | **UNKNOWN**. `HYPOTHESIS.md:74-86` says no session or transcript payload entered the evidence and replayability is unproven. Boundary: a hook delivery path alone does not supply replay history. | **WEAK**. `HYPOTHESIS.md:43-50` verifies deterministic retention of `TRANSCRIPT_ONLY` fixtures, but `HYPOTHESIS.md:60-70` confirms no transcript watcher or live replay path. Boundary: reconciliation is not a replay source. |
| `FUTURE_INTERVENTION_POTENTIAL` | **WEAK**. `transcript_watcher.py:160-195` can observe appended complete records, but `HYPOTHESIS.md:64-66,83-84` provides no live-latency or downstream-action evidence. Boundary: the route remains observation-only and cannot justify intervention timing. | **WEAK**. `HYPOTHESIS.md:12-17,44-58` shows a hook framework and trust path, but no delivered event or configured target hook. Boundary: lifecycle symbols are not an executable intervention channel. | **PARTIAL**. `reconcile.py:20-27,149-205` preserves unilateral and conflict states that could inform later shadow decisions. Boundary: no live source, dispatch, timing, or intervention behavior is implemented or proven. |
| `IMPLEMENTATION_COMPLEXITY` | **PARTIAL**. `HYPOTHESIS.md:88-100` reports a low-cost standard-library spike but lists production policies for discovery, rotation, privacy, attribution, deduplication, and compatibility. Boundary: low spike cost is not a full integration estimate. | **PARTIAL**. `HYPOTHESIS.md:90-101` reports a low-cost read-only spike, while the next step still requires disposable hook configuration, payload capture, and coverage measurement. Boundary: actual hook integration cost is unmeasured. | **PARTIAL**. `HYPOTHESIS.md:72-83` reports a small standard-library probe, but a usable dual route would add two live-source adapters, identity ownership, ordering, and reconciliation policies. Boundary: only fixture reconciliation cost is observed. |
| `PROVIDER_COUPLING` | **SUPPORTED**. `HYPOTHESIS.md:83-84` and the source-only parser/watcher contain no provider, sidecar, ledger, or UI dependency. Boundary: provider integration was intentionally not attempted. | **SUPPORTED**. `HYPOTHESIS.md:60-64,90-94` and `hook_adapter.py:1-7` keep normalization separate from provider and sidecar behavior. Boundary: only the input adapter is evidenced. | **SUPPORTED**. `HYPOTHESIS.md:67-76` and `reconcile.py:83-116` use an allowlisted sanitized event model without provider execution. Boundary: the `provider` field is metadata, not a provider call or coupling test. |

## Decision Basis

H1 is the only hypothesis with both observed runtime transcript evidence and a
working bounded parser/watcher that demonstrates stable tool-call/result
correlation and replay from ordered JSONL. Its unresolved live-latency and
coverage boundaries are explicit, and its spike has the smallest evidenced
integration surface.

H2 has a plausible local hook framework, but the decisive event-delivery
evidence is absent. H3 provides useful reconciliation semantics, including
duplicate collapse and conflict preservation, but its inputs are sanitized
fixtures and it depends on two upstream channels that were not exercised.
Those results do not justify selecting either path as the Step 1 source of
runtime truth.

## Validation

Focused external validations completed read-only:

- H1: `python3 -m unittest discover -s . -p 'test_*.py'` -> `6/6` passed.
- H2: `python3 -m unittest discover -s . -p 'test_*.py'` -> `4/4` passed.
- H3: `python3 -m unittest discover -s . -p 'test_*.py'` -> `5/5` passed.

The tests validate the three bounded spikes and fixtures only. They do not
promote the unresolved runtime boundaries into confirmed capability.

