# H2 Hook-First Hypothesis

## CLAIM

The local Codex installation exposes a hook framework and contains a
`PostToolUse` event type, but this worktree cannot claim H2 support because the
active local configuration only wires an `Interrupt` command hook. Live
`tool.output.value` delivery and hook payload coverage remain `UNKNOWN`.

## WHY_PLAUSIBLE

The installed Codex binary contains hook event names for `post_tool_use`,
`pre_tool_use`, session lifecycle, and subagent lifecycle events. It also
contains stable-identity candidates including `session_id`, `turn_id`,
`tool_call_id`/`call_id`, `tool_name`, and `tool_output`. The local configuration
has a `hooks` namespace and the CLI exposes hook-trust handling, so a command
hook route is present in principle.

## PREDICTION

If H2 is viable for Step 1, a configured `PostToolUse` hook should receive one
tool-result payload per disposable tool call with enough stable identity to
correlate the result to a canonical event without timestamp-only matching.

## CHEAP_PROBE

Run only read-only checks:

1. Inspect the active Codex `config.toml` with structured TOML parsing and
   report hook event names and handler types, without printing command values or
   reading authentication files.
2. Run `codex --version` and `codex --help` and record whether the installed
   CLI exposes hook-trust handling.
3. Inspect bounded strings from the installed Codex binary for hook event names
   and candidate payload fields.
4. Do not start a Codex task, invoke a hook, read sessions, read transcripts,
   or write a runtime configuration.

The reproducible probe is
`experiments/hypothesis-frontier/h2-hook-first/probe_hook_surface.py`.

## OBSERVED_EVIDENCE

Observed on October 5, 2026:

- The local CLI reports `codex-cli 0.153.4`.
- The active config contains a `hooks` namespace with one configured event:
  `Interrupt`, using a `command` handler with a three-second timeout.
- No active `PostToolUse` hook is configured in that file.
- CLI help exposes `--dangerously-bypass-hook-trust`, confirming that the
  installed CLI has a hook trust path.
- The installed binary contains `post_tool_use` and related hook event names,
  plus candidate fields `hook_event_name`, `session_id`, `turn_id`,
  `tool_call_id`, `call_id`, `tool_name`, `tool_output`, `agent_id`, and
  `thread_id`.
- No real `PostToolUse` stdin payload was observed. No Codex task was started
  for this spike, and no session or transcript payload entered the evidence
  artifact.

The bounded code spike includes a strict normalizer for a future observed
`PostToolUse` payload. It derives `event_id` from
`session_id + turn_id + tool_call_id`, preserves the result as `value`, and
returns `UNKNOWN` or `UNSUPPORTED` when the required evidence is absent. It is
not connected to a configured runtime hook.

## FALSIFIER_RESULT

H2's prediction of sufficient live tool-result coverage is not supported by
this probe. The hook framework is `OBSERVED`, and the `PostToolUse` symbol is
`OBSERVED` in the installed binary, but actual event delivery, ordering,
latency, duplicate behavior, agent attribution, and replayability are
unproven. The Step 1 H2 verdict is therefore `UNKNOWN`, not `KEEP`.

## KNOWN_GAPS

- The actual `PostToolUse` payload schema is not confirmed from a delivered
  event; binary strings are capability evidence, not runtime evidence.
- `tool.output.value` has not been observed on the hook path.
- Event coverage, latency, ordering, duplicate rate, agent attribution,
  replayability, future intervention potential, and provider coupling are
  `UNKNOWN`.
- No disposable main-agent/subagent scenario was run.
- No hook was added to the user's active Codex configuration.
- The final bounded evidence collection is limited to configuration, CLI help,
  and installed-binary metadata; no raw session or transcript output is
  retained.
- The normalizer does not execute a hook, send data to a sidecar, persist a
  judgment, or affect Codex execution.

## IMPLEMENTATION_COST

Low for the bounded spike: two standard-library scripts and focused unit tests.
The probe is read-only, and the adapter has no provider, sidecar, UI, or
orchestration dependency.

## EXIT_COST

Low if H2 is archived: retain the probe and normalizer as explicit evidence
that the route was not proven. If H2 is later reconsidered, the next bounded
probe must configure a disposable `PostToolUse` hook, capture one redacted
payload, measure the common scenario against the Step 1 observation criteria,
and verify stable correlation before any runtime integration is attempted.
