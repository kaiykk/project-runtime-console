# Human Review Packet

**Round:** `PRC-V0-STEP-1-SHADOW-TOOL-OUTPUT-20261005`  
**Project:** Project Runtime Console  
**Status:** `PRINCIPAL_REVIEW`

## 1. Agent Monitor License And Shell Decision

`donvito/agent-monitor` was checked on 2026-10-05. Repository metadata did not
expose an SPDX license, and the local study checkout had no `LICENSE` or
`COPYING` file.

Decision: **clean-room behavioral reference only**. No Agent Monitor
implementation code or source assets were copied. The current console uses an
independently implemented Project / Run / Agent Topology / Trace surface.

## 2. Three Hypotheses

- **H1 — Transcript-first:** watch Codex JSONL sessions and normalize observed
  tool results.
- **H2 — Hook-first:** use a Codex lifecycle hook as the authoritative source.
  The hook framework was observed, but no real `PostToolUse` payload was
  delivered.
- **H3 — Dual-channel:** reconcile hook and transcript observations using
  stable identifiers. The reconciliation rules were tested only with
  sanitized fixtures.

## 3. Evidence Matrix And Commitment

The independent comparison is recorded in:

`experiments/hypothesis-frontier/STEP1_EVIDENCE_MATRIX.md`

Commitment:

```text
COMMIT_H1
```

Reason: H1 is the only strategy with observed runtime transcript evidence,
demonstrated tool-call/result correlation, replay behavior, and a bounded
implementation surface. H2 and H3 remain useful future probes, but neither
has live source evidence sufficient for Step 1 commitment.

## 4. What Was Implemented

The bounded vertical slice is:

```text
Codex transcript
  -> canonical tool.output.value event
  -> SHADOW judgment sidecar
  -> local JSONL Judgment Ledger
  -> Agent Monitor-style trace surface
```

Implemented boundaries:

- transcript JSONL replay with `session_id`, `turn_id`, `call_id`, source
  ordinal, and deterministic event identity;
- explicit `CORRELATED`, `PARTIAL`, and `UNKNOWN` identity states;
- deterministic fake judge and DeepSeek HTTP provider adapter;
- `SHADOW` judgment records with provider, model, latency, timestamp, and
  source reference;
- local JSONL ledger;
- local console showing Project, Run, Agent Topology, Trace, Shadow Judgment,
  selected event details, and Judgment Ledger;
- privacy-preserving demo output that retains explicit `PRC_DEMO_*` markers and
  redacts other tool output.

No H2 hook integration, H3 reconciliation integration, active intervention,
Control Plane, Delegatus integration, DSH/Claude adapter, ThoughtDAG, or
Hypothesis Frontier product UI was implemented.

## 5. How To Run

From the repository root:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/run_step1_demo.py \
  --transcript /path/to/a/codex/session.jsonl \
  --output output/demo-state.json
python3 apps/console/server.py \
  --data output/demo-state.json \
  --port 8765
```

Open:

```text
http://127.0.0.1:8765
```

The demo command writes only derived state and a local ledger under
`output/`. Raw transcripts are never copied into the repository.

## 6. Reproduce The Real Codex Demo

A disposable probe used for this packet ran a Codex task in
`/tmp/prc-step1-demo` that emitted three explicit safe markers:

```text
PRC_DEMO_TOOL_1
PRC_DEMO_TOOL_2
PRC_DEMO_TOOL_3
```

Its persisted transcript was replayed into the demo state. The resulting
state contained:

- 3 observed `function_call_output` events;
- 3 shadow judgments;
- 3 matching `canonical_event_id` pairs;
- `run.status = OBSERVED`;
- `shadow_invariant.runtime_effect = NONE`.

The exact transcript path is intentionally local-only and is not committed.

## 7. Screenshots

- [Initial console](output/playwright/step1-console.png)
- [Second event selected](output/playwright/step1-console-selected-event.png)

The screenshots show the Agent topology, run trace, shadow verdicts, selected
event identity, and Judgment Ledger.

## 8. DeepSeek Status

No real DeepSeek call was used in this run. `DEEPSEEK_API_KEY` was absent, so
the implementation returned:

```text
judge_setup: HUMAN_SETUP_REQUIRED
judge_provider: fake
judge_model: step1-deterministic
```

This is an explicit setup boundary, not a fabricated DeepSeek success.

## 9. Known Limitations

- Transcript append latency, rotation, truncation, and file locking are not
  measured.
- Parent/child Agent topology is not reconstructed from the transcript;
  the demo displays one session-bound Agent with
  `OBSERVED_SESSION_ONLY`.
- Duplicate output semantics remain unresolved.
- H2 hook delivery and `tool.output.value` coverage remain unknown.
- H3 reconciliation is fixture-only and is not in the runtime path.
- The fake provider is not evidence of judgment quality.
- The console is a local vertical slice, not production packaging.
- Demo tool output is redacted unless it is an explicit safe marker.

## 10. Local Audit Result

**`PASS_WITH_BOUNDARY`**

Validation completed:

- Step 1 vertical-slice tests: `5/5` passed;
- H1 spike tests: `6/6` passed;
- H2 spike tests: `4/4` passed;
- H3 spike tests: `5/5` passed;
- Python compilation passed;
- `git diff --check` passed;
- tracked-source secret scan passed;
- local `/api/state` returned the expected v0 state;
- browser interaction switched the selected event and matching judgment;
- event identity remained equal from transcript event to judgment to ledger;
- shadow runtime effect remained `NONE`.

The audit confirms implementation behavior within the tested scope. It does
not validate the unresolved runtime model beyond that scope.

## 11. Semantic Smoke-Test Result

Fresh reviewer result: **`PARTIAL`**

The reviewer identified the product as a Project Runtime Console for
inspecting a Codex run, Agent topology, runtime trace, and attached shadow
judgments. It did not read the implementation and did not frame the product
as orchestration, a task board, governance, or hypothesis management.

The result is `PARTIAL`, rather than `MATCH`, because the screenshot visibly
uses `fake / step1-deterministic`; it cannot prove a real independent
DeepSeek judge. Redacted tool output also limits inspection of the underlying
run.

## 12. Recommended Step 2

One bounded follow-up probe is recommended, but not authorized automatically:

> Configure a disposable `PostToolUse` hook outside the active product
> configuration, capture one redacted real payload, and compare its stable
> identity and coverage with the H1 transcript event.

Do not begin a broad H2/H3 campaign. Stop at `PRINCIPAL_REVIEW`.
