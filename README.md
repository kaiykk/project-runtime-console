# Project Runtime Console

Project Runtime Console is a new product for inspecting a real Agent run,
following its runtime topology and trace, and viewing independent shadow
judgments attached to runtime events.

## North Star

When a Human opens the console, they should be able to inspect a real Codex
run, understand the parent/child Agent topology, open the runtime trace, and
see an independent Judge's shadow judgment attached to the corresponding
event. The judgment is observable, replayable, and has no effect on Codex
execution.

## V0 Product Shape

```text
Project
  -> Run
    -> Agent Topology
      -> Trace
        -> Shadow Judgment
```

V0 is runtime observability plus shadow evaluation. It is not a Control Plane,
Task Board, Orchestrator, Project Evolution system, Memory UI, Skill UI,
ThoughtDAG canvas, or active intervention system.

## Step 1

Step 1 answers one question:

> How should real Codex runtime events reliably enter the Shadow Judgment
> Sidecar?

The first bounded vertical slice observes one real `tool.output.value`, turns
it into a canonical runtime event, sends a bounded copy to a local DeepSeek
judge provider or deterministic fake provider, persists the shadow judgment,
and displays it on the matching trace event.

The Step 1 implementation is not authorized to alter Codex behavior.

## Repository Boundaries

```text
apps/console/
packages/runtime-events/
packages/providers/codex/
packages/judgment-sidecar/
packages/judge-deepseek/
packages/judgment-ledger/
plugins/codex-judgment-adapter/
experiments/hypothesis-frontier/
```

These boundaries are intentional. The console, event sensor, sidecar,
provider, ledger, and future Codex adapter must not collapse into one module.

## Status

Step 1 is in setup and hypothesis-frontier evaluation. No winner is committed
until the three independent input strategies have been compared and the
commitment gate has returned a bounded decision.

Human-facing HTML reports are produced in Chinese. Code identifiers and
protocol field names remain English.
