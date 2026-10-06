# Current State

**Date:** 2026-10-06
**Project:** Project Runtime Console
**Active bounded round:** `PRC-V0-STEP-3-LIVE-RUNTIME-CONSOLE-20261006`

## UI Convergence Checkpoint

The Principal input `PRC-UI-CONVERGENCE-R1-20261006` was reviewed as a new
Human-facing/model-shaping round request. The Principal subsequently issued a
versioned `FRAME_EVOLUTION` amendment, recorded at
`docs/ui-frame-change-v1.md`, which updates the presentation boundary in
`docs/SHELL_FREEZE_V0.md` and `docs/capability-imports/THOUGHTDAG.md`.
Runtime, identity, judgment, and observer-independence boundaries remain
unchanged.

The DSH round-start Global Review returned `GO_LOCAL` for exactly one action:
`RUN_PASS_A_REFERENCE_PRECOMMIT_ONLY`. Pass A completed and produced
`experiments/ui-convergence/REFERENCE_FIRST_PRECOMMIT.md`. After the Principal
amendment, Pass B Frame Comparison reviewed the proposal and returned
`FRAME_OK / EVIDENCE_GAP=NO / ADVISORY_ONLY=YES`. This permits preparation of
the next bounded execution packet; it does not approve the UI or authorize
unbounded implementation.

Current status: `PASS_B_COMPLETE__EXECUTION_PACKET_REQUIRED`.

Do not start ThoughtDAG/Agent Monitor reference capture, the convergence
harness, UI variants, refinement, or code changes until the next bounded
execution packet is prepared and authorized. Receipts:

- `experiments/ui-convergence/receipts/round-start-global.json`
- `experiments/ui-convergence/receipts/frame-pass-a.json`
- `experiments/ui-convergence/receipts/frame-pass-b.json`
- `experiments/ui-convergence/REFERENCE_FIRST_PRECOMMIT.md`

## Current Outcome

Step 3 implemented one read-only Codex-native Runtime Observer and one
minimal Console surface. It remains a bounded implementation result, not a
Human Principal ratification and not Product v0 completion.

The observer now:

- connects to the local Codex app-server through JSON-RPC;
- requests all current Codex thread source kinds, including subagents;
- follows `parentThreadId` to group descendants under the root Run while
  preserving each Thread's native `sessionId`;
- uses native Thread IDs for Agent identity and native Turn/item IDs for live
  trace ownership;
- reads history through `thread/read` with turns;
- preserves native `notLoaded` instead of inferring `completed`;
- exposes explicit `RECONCILIATION_UNRESOLVED` when no persisted
  `canonical_event_id` relation has been established;
- keeps `read_only=true`, `runtime_effect=NONE`, and
  `SHOW_JUDGMENTS=false`.

## Evidence Result

Confirmed or directly observed:

- Codex CLI `0.153.4` exposes the checked app-server surface:
  `initialize`, `thread/list`, `thread/read`, thread status, turn lifecycle,
  and item lifecycle notifications.
- A real app-server history Run with one root and two children was opened.
  The Console displayed three Agents, correct root/child edges, and separate
  trace rows for the selected child.
- A larger real historical Run with 14 native Agents was also discovered;
  this shows the source-kind and pagination repair reaches actual subagent
  records beyond the three-Agent Gold Run.
- Native `Thread.sessionId` values for child threads are distinct from the
  root in the observed data. The logical Run grouping therefore uses the root
  Thread session reached through `parentThreadId`; Agent identity is never
  derived from `sessionId`.
- The historical read path is available for the observed Runs. Live native
  items remain explicitly unresolved against Step 1 persisted event IDs.
- Focused and full test suite: `11/11` passed. Python compilation and
  `git diff --check` passed.

## Partial / Not Proven

- The Console can poll the app-server and consume native notification buffers,
  but a controlled active Gold Run with a witnessed working-to-finished
  transition was not completed in this round.
- The Gold Run topology and history reopen are confirmed; the same run was
  not captured end-to-end as live UI plus post-completion reopen evidence.
- No DSH product Judge invocation was performed. No product provider receipt
  exists, and no Shadow Judgment capability is claimed for Step 3.
- No Agent Monitor behavioral comparison was completed.
- Live native observation has no established relation to Step 1
  `canonical_event_id`; the boundary remains
  `RECONCILIATION_UNRESOLVED`.

## Governance Boundary

The round-start DSH receipt is retained at
`experiments/runtime-observer/receipts/step3-round-start-global.json`.
It authorizes this bounded observer implementation only. It does not review
the final implementation, ratify the runtime model, authorize DSH Judge
integration, or declare Product v0 success.

## Next Action

Stop at `PRINCIPAL_REVIEW`. The Human Principal must decide whether the
remaining controlled live-transition probe and the separately sequenced DSH
Judge probe should receive a new bounded authorization. Do not enter a new
phase automatically.

## Evidence Pointers

- `experiments/runtime-observer/STEP3_EXECUTION_PACKET.md`
- `experiments/runtime-observer/receipts/step3-execution.json`
- `HUMAN_REVIEW_PACKET_STEP3.md`
- `experiments/runtime-observer/receipts/gold-run-evidence.json`
- `output/playwright/step3-gold-run-root.png`
- `output/playwright/step3-gold-run-child.png`
- `output/playwright/step3-child-trace.png`

No raw private transcript, secret, credential, or hidden reasoning is
committed.
