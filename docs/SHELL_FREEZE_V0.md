# Shell Freeze v0

**Status:** Human-frozen for Step 1

## Primary Information Architecture

```text
Project
  -> Run
    -> Agent Topology
      -> Trace
        -> Shadow Judgment
```

The primary object shown to a Human is a runtime Project/Run, not a research
workflow or a hypothesis-management surface.

## Allowed in v0

- Project and Run navigation
- Parent/child Agent topology
- Agent trace and tool call/result details
- Runtime status
- Existing usage/token information when the source provides it
- Compact Shadow Judgment badge and detail
- Judgment Ledger view
- Judge provider and runtime-adapter status

## Forbidden in v0

- Task Board
- Orchestrator UI
- Pipeline UI
- Project Evolution
- Workline
- Hypothesis graph in the product UI
- Control Plane
- Skill UI
- Memory UI
- ThoughtDAG canvas
- Hive UI
- Active interventions

Sandcastle hypothesis branches are development tooling only. They must not
appear in the product information architecture.

## Boundary

This freeze does not authorize implementation of every allowed surface. Step 1
only needs enough Agent Monitor-style shell to show one real tool-result trace
event and its attached shadow judgment.
