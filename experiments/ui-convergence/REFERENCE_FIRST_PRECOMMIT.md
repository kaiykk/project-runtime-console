# Reference-First Precommit

```yaml
round_id: PRC-UI-CONVERGENCE-R1-20261006
review_id: prc-ui-convergence-frame-pass-a-20261006
executor: dsh-headless
source: FRAME_AUDITOR_PASS_A_PACKET.md and its allowlisted Human references
artifact_status: SANITIZED_REVIEWER_OUTPUT
raw_reasoning: OMITTED
product_frame_selected: NO
advisory_only: YES
```

## HUMAN_PROBLEM

- A Human needs to inspect a real Agent run during and after execution and
  understand it from runtime evidence, not from an untraceable summary.
- The Human needs to identify participating Agents, runtime events, and
  shadow judgments without mistaking a judgment for intervention or outcome.
- Parent/child topology, Agent trajectory, and event detail must be discoverable
  without excessive scrolling or a separate research workflow.
- The Human must orient within a large multi-Agent Run and return from detail
  to the whole Run.

## EXPERIENCE_INVARIANTS

- Preserve `Project -> Run -> Agent topology -> Agent trajectory -> runtime
  event -> optional Judgment annotation`.
- Parent/child relationships must be legible without opening a details panel.
- Topology and Trace remain one coherent experience with progressive
  disclosure; raw JSON is not the primary interaction.
- Runtime nodes, edges, status, events, and trace ownership come from real
  evidence. Fake topology and user-editable runtime lineage are prohibited.
- Judgments remain shadow annotations and cannot affect Codex execution.
- Human-facing reports distinguish confirmed evidence, observed behavior,
  hypothesis, and unknown; HTML reports are Chinese.
- Review verdicts are advisory and never substitute for Human ratification.

## HUMAN_CONFIRMED_DECISIONS

- The primary object is a runtime Project/Run, not a research workflow or
  hypothesis-management surface.
- `UI_BASELINE_C0` is frozen as a functional/runtime baseline for this round;
  its visual architecture is not assumed to be the target.
- The supplied Principal input authorizes a bounded UI convergence round with
  reference capture, exactly three structurally distinct variants, browser
  evidence, independent Visual/UX/Runtime reviews, at most two refinements,
  rollback on material regression, and a final stop at `PRINCIPAL_REVIEW`.
- Agent Monitor is a clean-room behavior reference; its implementation and
  assets are not reusable under the current license boundary.
- ThoughtDAG may be run as a bounded interaction reference and any future
  narrow code reuse must record repository, commit, path, license, local path,
  and modification, with MIT attribution.
- ThoughtDAG ontology, editable context edges, memory/Q&A model, model
  invocation logic, and unrelated product features are not imported.
- All variants must use the existing Runtime Observer backend and the same
  real historical multi-Agent Run; fake nodes are prohibited.
- A winner is not automatically merged or approved as the Product UI
  baseline; the Human Principal reviews Top 1 and Top 2.

## SUPPORTED_CONCEPTS

- A graph-first live runtime presentation is the explicit target direction in
  the supplied Principal input, pending the unresolved frozen-document
  conflict below.
- Reference behaviors worth evaluating include spatial hierarchy, branch
  readability, semantic zoom, node selection, focus, minimap/navigation,
  detail disclosure, large-Run orientation, and materially useful motion.
- Runtime-observer concepts worth evaluating include topology truth,
  parent/child readability, Agent state, Agent-to-Trace navigation, and trace
  richness.
- A repo-local convergence harness may coordinate browser capture, task replay,
  evidence comparison, targeted refinement, and rollback, but it must remain
  small and must not become a product runtime.

## UNAUTHORIZED_OR_FORBIDDEN_CONCEPTS

- Task Board, Orchestrator, Pipeline, Project Evolution, Workline, hypothesis
  graph, Control Plane, Skill UI, Memory UI, Hive UI, and active intervention.
- Agent Monitor code/assets or any claim that license uncertainty grants reuse
  permission.
- ThoughtDAG conversation/context ontology, editable lineage/context edges,
  memory model, Q/A model, model invocation logic, and unrelated features.
- Fake nodes/edges/events, trace leakage, presentation-caused missing Agents,
  raw JSON as primary interaction, or a builder self-certifying from source.
- Automatic winner merge, more than three initial variants, more than two
  refinements, or final Product UI approval claims.
- Using `FRAME_OK`, `INTENT_PASS`, `PASS`, screenshots, or tests as Human
  ratification or proof of model validity.

## LIKELY_FRAMING_FAILURES

- Leaving the experience as a decorated three-column dashboard rather than a
  materially different graph-first presentation.
- Using attractive but fabricated grouping, edges, hierarchy, or status.
- Importing ThoughtDAG's editable context model into a runtime-observation
  product whose edges are observed facts.
- Separating topology and trace so the Human loses context when moving from
  overview to Agent to event detail.
- Hiding basic answers such as root and direct-child count behind panels,
  scroll, or raw JSON.
- Treating visual quality as compensation for runtime identity or trace-owner
  errors.
- Presenting shadow judgment as an intervention or engineering outcome.
- Calling styling changes structural variants, validating against fake data,
  or leaking builder rationale into independent reviewers.
- Treating the Principal input as silently rewriting every existing boundary,
  or treating the old freeze as permanently blocking an explicit Principal
  request without routing the conflict back to Principal review.

## QUESTIONS_EVERY_FRAME_MUST_ANSWER

- Can a Human identify the root Agent and direct-child count from the overview?
- Are every rendered node and edge backed by runtime-observed evidence?
- Is each sibling Agent's trajectory isolated from the other sibling's trace?
- Does one canvas preserve context across overview, trajectory, and event detail?
- Can a Human locate a tool call and result without using raw JSON?
- Are active/finished/unknown statuses faithful to runtime evidence?
- Can a Human orient in the large Run with measurable click and zoom/pan
  burden?
- Does the frame preserve the Project/Run primary object while remaining
  graph-first?
- Does it remain within authorized product boundaries, with unresolved
  additions explicitly marked?
- Are the three variants structurally different across at least four declared
  dimensions and tested on the same real Run?
- Are evidence states and review verdicts visibly kept separate from approval?
- Is all third-party reference material provenance-complete?

## AUTHORITY_CONFLICTS

- `SHELL_FREEZE_V0.md` lists `ThoughtDAG canvas` as forbidden in v0, and
  `docs/capability-imports/THOUGHTDAG.md` says `NOT_AUTHORIZED_FOR_V0`. The
  supplied Principal input sets a ThoughtDAG-inspired live runtime canvas as
  the target and authorizes bounded reference/use exploration. Whether this
  explicitly amends the frozen documents is unresolved.
- The old freeze names `Agent Topology -> Trace`, while the new input adds
  `Agent trajectory -> runtime event`; their relationship is unresolved.
- The old freeze makes Project/Run the primary object; the new input requires
  graph-first presentation. Whether graph-first is a presentation of the same
  Project/Run object or a new primary object is unresolved.
- The old freeze is Step 1-specific and minimal; the new input authorizes a
  broader convergence round. Whether this is a new bounded round or a Step 1
  scope expansion is unresolved.
- The exact interleaving of autonomous convergence and mandatory Frame,
  Intent Fidelity, Local Auditor, and Global Reviewer checkpoints is unresolved.
- This artifact is not a frame selection, governance receipt, product
  approval, or evidence that the C0 complaints are independently confirmed.
