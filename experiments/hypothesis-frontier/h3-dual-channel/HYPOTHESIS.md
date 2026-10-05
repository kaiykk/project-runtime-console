# H3 Dual-Channel Hypothesis

## CLAIM

Sanitized hook and transcript observations can be reconciled into a small,
traceable event record when a stable event or provider identifier is present,
while unilateral observations and cross-channel disagreement remain visible.

## WHY_PLAUSIBLE

Hooks are positioned to expose live runtime semantics, while transcripts can
provide replayable history. A shared stable identifier gives both channels a
bounded join key without treating capture time as event identity.

## PREDICTION

The probe should:

- correlate matching `event_id` or `provider_event_id` values;
- collapse repeated same-channel observations with the same stable identity and
  semantic payload;
- preserve `HOOK_ONLY` and `TRANSCRIPT_ONLY` when one channel has no stable
  match;
- preserve `CONFLICT` when a stable match has disagreeing payload or identity
  fields; and
- refuse timestamp-only correlation.

## CHEAP_PROBE

Run a standard-library fixture probe with sanitized `tool.output.value`
observations covering duplicate hook delivery, provider-identifier
correlation, payload conflict, timestamp-only input, and an unmatched
transcript.

Command:

```text
python3 -m unittest discover -s experiments/hypothesis-frontier/h3-dual-channel -p 'test_*.py'
```

## OBSERVED_EVIDENCE

The focused local tests passed with five cases:

- duplicate hook observations collapsed to one `HOOK_ONLY` record;
- matching provider event identifiers produced `CORRELATED`;
- matching identity with changed sanitized payload produced `CONFLICT`;
- equal timestamps without stable identifiers remained separate as
  `HOOK_ONLY` and `TRANSCRIPT_ONLY`;
- an unmatched transcript remained `TRANSCRIPT_ONLY`.

This is fixture-level implementation evidence only. It does not establish
coverage or latency for live Codex hooks or transcript files.

## FALSIFIER_RESULT

The bounded fixture probe did not falsify the hypothesis. The implementation
does not claim the hypothesis is validated for live runtime input.

## KNOWN_GAPS

- No live hook surface or transcript watcher was exercised.
- No buffering, retry, out-of-order delivery, or late-arrival policy is
  implemented.
- Divergent duplicate payloads within one channel are not given a separate
  resolution policy.
- No provider, sidecar, ledger, UI, orchestration, or intervention behavior is
  included.
- Stable identifiers must be supplied by an upstream sanitized adapter; this
  probe does not invent them.

## IMPLEMENTATION_COST

Low. The spike is a small standard-library module with an allowlisted event
normalizer, deterministic reconciliation records, and focused unit tests. It
adds no runtime dependency and touches no product surface.

## EXIT_COST

Low. The spike is isolated to the H3 experiment directory and can be archived
without migration or compatibility work. Any future production adapter would
need a separate review of identity ownership, event ordering, and live-source
evidence.
