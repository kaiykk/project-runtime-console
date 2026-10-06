# PRC UI Convergence — Frame Proposal

```yaml
round_id: PRC-UI-CONVERGENCE-R1-20261006
proposal_id: PRC-FRAME-GRAPH-FIRST-RUNTIME-CANVAS-V1
review_stage: PASS_B_FRAME_COMPARISON
product_frame_status: PROPOSAL_ONLY
implementation_status: NOT_STARTED
```

## Proposed Frame

Present the existing Project/Run as a graph-first Runtime Canvas. The canvas
shows only observed Codex runtime topology and trace facts:

```text
Project / Run context
  -> observed Agent topology
    -> selected Agent trajectory
      -> selected runtime event
        -> optional shadow Judgment annotation
```

The graph is a presentation and interaction layer. It does not become a new
runtime identity model or product ontology. Project/Run remains the primary
runtime object; graph-first describes how the Human sees and navigates that
object.

## Interaction Commitments

- Parent/child Agent relationships are visible in the overview without
  opening a detail panel.
- Selecting an Agent focuses its observed trajectory without changing runtime
  lineage or mixing sibling traces.
- Selecting an event reveals its tool call/result detail while preserving the
  surrounding Run and Agent context.
- Overview, trajectory, and event detail are navigable through the same canvas
  context with progressive disclosure.
- Zoom, focus, pan, minimap, or related navigation may be evaluated as
  interaction mechanisms, but they cannot create or edit runtime edges.
- Raw JSON is evidence detail, not the primary interaction.

## Runtime Truth Boundary

The frame must render the existing Runtime Observer projection and the same
real historical multi-Agent Run used for all variants. It must preserve:

- native Agent identity and parent identity;
- observed status without inferring completion from missing data;
- Agent-specific trace ownership;
- explicit `RECONCILIATION_UNRESOLVED` where live/history relation is not
  established;
- `read_only=true`, `runtime_effect=NONE`, and hidden judgments by default.

No fake nodes, synthetic edges, fabricated status, or presentation-only Agent
grouping is permitted.

## Bounded ThoughtDAG Reference Use

The proposal may evaluate ThoughtDAG-inspired canvas mechanics such as
semantic zoom, viewport navigation, minimap, node focus, edge routing, and
incremental graph append behavior. It must not import ThoughtDAG conversation
ontology, context-edge semantics, memory/model context, Q/A, model
invocation, or editable relationships. Any copied MIT code requires the
provenance fields specified by `docs/ui-frame-change-v1.md`.

## Acceptance Questions For Pass B

1. Is this a presentation-layer evolution of the existing Project/Run rather
   than a new runtime model?
2. Does it preserve all Human experience invariants in
   `REFERENCE_FIRST_PRECOMMIT.md`?
3. Does it keep runtime lineage read-only and evidence-backed?
4. Does it prevent a graph aesthetic from fabricating topology or hiding
   trace ownership errors?
5. Is the proposal specific enough to support later structural variant
   comparison without deciding a final UI or implementation?
6. Does it remain within the Principal amendment and unchanged boundaries?

## Stop Boundary

This document does not authorize ThoughtDAG capture, harness creation, UI
implementation, variant generation, or refinement. Those actions require a
`FRAME_OK` result from the independent Pass B review and the next bounded
execution action.
