# H1 Transcript-first

## CLAIM

Transcript watching is a plausible Step 1 input path for offline and replay
oriented observation of Codex tool results. It can normalize a
`function_call_output` record into the target `tool.output.value` event without
changing Codex execution, but this spike does not establish live coverage or
production readiness.

## WHY_PLAUSIBLE

The local Codex session store contains ordered JSONL records. The inspected
records expose:

- top-level `ordinal` and `timestamp`;
- `session_meta.payload.session_id`;
- `turn_context.payload.turn_id`;
- `response_item.payload.type`;
- `response_item.payload.call_id`;
- string `response_item.payload.output` on tool-result records.

The `call_id` is a better correlation anchor than a timestamp. A preceding
call record can also provide the tool name without copying the private
transcript into this repository.

## PREDICTION

Given an available transcript file, H1 should be able to:

1. observe appended complete JSONL records through a polling watcher;
2. recognize `function_call_output` and `custom_tool_call_output` records;
3. correlate a result to `session_id`, `turn_id`, and `call_id`;
4. emit a deterministic event ID when the stable identity fields are present;
5. preserve `PARTIAL` or `UNKNOWN` when the transcript does not support that
   identity.

## CHEAP_PROBE

Inspect local session-file metadata only, then run the parser against a
sanitized fixture and an incremental partial-line scenario. Do not persist or
commit raw transcript output, private paths, credentials, or hidden reasoning.

## OBSERVED_EVIDENCE

On 2026-10-05, a local session JSONL file was inspected read-only. It
contained 113 ordinal-bearing records with no descending or duplicate ordinal
transitions in the inspected sequence. It contained 25 distinct call IDs and
23 distinct tool-output call IDs; all 23 output IDs matched a prior call ID.
The parser observed 35 output records in that file, so repeated output records
for an existing call ID are possible and duplicate semantics remain
`UNKNOWN`. The output records used `function_call_output` with string output
values.

The sanitized fixture and focused tests confirm that:

- the normalized event is `tool.output.value` in `SHADOW` mode;
- `session_id`, `turn_id`, `call_id`, tool name, source ordinal, and a
  deterministic event ID are retained;
- identical input produces the same event ID;
- identical timestamps do not determine event identity;
- an incomplete final JSONL line is held until its newline arrives.

These observations support the parser shape only. Live latency, transcript
flush behavior, rotation, multi-agent attribution, and complete event coverage
remain `UNKNOWN`.

## FALSIFIER_RESULT

The cheap probe did not falsify the narrow prediction for a sanitized,
single-session tool result. It did falsify any stronger claim that timestamps
alone are sufficient: the implementation leaves identity unresolved when the
stable session/call fields are missing.

## KNOWN_GAPS

- `PARTIAL` and `UNKNOWN` are explicit boundaries, not inferred identities.
- Transcript availability, append latency, rotation, truncation, and file
  locking were not measured.
- Agent or parent/child attribution is `UNKNOWN` from this bounded parser.
- Coverage for non-tool response items and future transcript schema changes is
  `UNKNOWN`.
- No hook comparison, sidecar, provider call, ledger, UI, or intervention was
  implemented.
- The inspected local files do not prove that every Codex runtime or future
  version emits the same shape.

## IMPLEMENTATION_COST

Low for the spike: one standard-library parser, one polling watcher, one
sanitized fixture, and focused unit tests. No dependency installation or
runtime modification is required.

## EXIT_COST

Low for this spike: remove the experiment directory if H1 is not selected.
If H1 is selected, a later implementation would need an explicit policy for
file discovery, rotation, live latency, privacy filtering, agent attribution,
deduplication, and source-version compatibility before it could be considered
ready for a broader Step 1 slice.
