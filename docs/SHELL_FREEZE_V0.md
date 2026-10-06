# Shell Freeze v0

**Status:** Human-amended for UI Convergence R1; runtime and authority
boundaries remain frozen

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
- ThoughtDAG-inspired graph-first Runtime Canvas as a bounded Presentation /
  Interaction Layer, subject to `docs/ui-frame-change-v1.md`
- Hive UI
- Active interventions

Sandcastle hypothesis branches are development tooling only. They must not
appear in the product information architecture.

The following remain forbidden in the authorized Runtime Canvas presentation:

- ThoughtDAG product ontology;
- editable runtime lineage or user-created runtime relationships;
- ThoughtDAG context-edge semantics;
- memory or model-context semantics;
- arbitrary user-created nodes or edges;
- any Control Plane, intervention, orchestration, or workflow surface.

## Boundary

This document still does not authorize implementation of every allowed
surface. The UI Convergence R1 amendment authorizes a presentation/interaction
exploration only. It does not modify the PRC North Star, Codex Runtime Model,
Runtime Identity Contract, Judgment Sidecar boundary, or Runtime Observer
Independence requirement. Runtime edges remain observed facts.
