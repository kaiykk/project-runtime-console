# V1_REUSE_MATRIX

Round: `V1 Reuse & Compatibility`

This matrix records source-backed compatibility evidence only. It does not
authorize production integration and does not define a PRC UI or upstream
ontology.

## Datadog Trajectory Probe

| PRC need | Upstream | Classification | Exact source / revision | License | Dependencies | Semantic assumptions | Integration cost | Evidence |
|---|---|---|---|---|---|---|---|---|
| Codex history backfill, task segmentation, Work Insights, outcomes, `patterns session --json` | Datadog Trajectory | `ADAPT` for recognition/activity evidence; `REJECT` for WorkStage import in this round | Trajectory `0.6.0`, commit `f03a74b21d31e9d95e491f35cc4646d5262e3f76`; local probe artifacts in `evidence/trajectory-patterns-session-01a0eca4-7029-7f92-b5a9-2006edb08721.json` and `evidence/trajectory-patterns-estimate-2026-09-29.json` | Not independently established in this probe | Local CLI with isolated Codex rollout corpus; no remote MCP or OAuth used | Session/turn/subagent/deliverable evidence is available, but `task_count: 0` and `tasks: null`; cannot treat activity or deliverable fields as Human work taxonomy | Low for reading evidence; unestablished for WorkStage compatibility | `evidence/datadog-capability-probe.json`: local backfill/indexing completed, target session recognized, `patterns session --json` returned structured data, but no task/work boundaries; `patterns analyze --yes` was not run |

The local DSH Trajectory package was inspected and deliberately excluded from
this row. It is `@deepseek-ai/dsh-client-ui-trajectory`, a browser view plugin
for DSH conversation events. It is not evidence of Datadog Codex backfill,
task segmentation, or `patterns session`.

## Interaction / Implementation Reuse

| PRC need | Upstream | Classification | Exact source | License | Dependencies | Semantic assumptions | Estimated integration cost | Evidence |
|---|---|---|---|---|---|---|---|---|
| Aggregated vs expanded complexity management | Langfuse `trace-graph-view` | `ADAPT` | `web/src/features/trace-graph-view/buildGraphCanvasData.ts`, `buildExpandedGraph.ts`, `types.ts` at `8b587645cf144b7bdf27883f59cd2c2e39552471` | MIT (`package.json`, repository `LICENSE`) | React, `elkjs`, `d3-selection`, `d3-zoom`, Langfuse observation types and app components | Nodes are Langfuse observations; aggregation uses step/name and expansion uses observation hierarchy plus timing-derived sibling order. PRC Agent/Runtime Event semantics cannot be imported directly | Medium-high: isolate renderer/builders and replace data contracts, selection plumbing, and labels | README lines 11-31; `buildExpandedGraph.ts` lines 11-20 and 84-92; source inspected in disposable clone |
| Deterministic graph layout and viewport | Langfuse `trace-graph-view` | `ADAPT` | `web/src/features/trace-graph-view/layout/elkLayout.ts`, `layout/graphLayoutWorkerClient.ts`, `components/ElkGraphRenderer.tsx` at the same revision | MIT | `elkjs`, Web Worker, `d3-zoom`, React | Layout input is a trace observation graph; viewport owns a user override over fit; PRC can reuse mechanics only after translating native graph facts | Medium: renderer can be isolated, but worker/build integration is coupled to Langfuse app conventions | README lines 35-54; `ElkGraphRenderer.tsx` lines 82-91 and 113-120; layout worker source inspected |
| Local focus and bounded expansion | Langfuse `trace-graph-view` | `ADAPT` | `web/src/features/trace-graph-view/components/TraceGraphView.tsx`, `graphNodeMatching.ts`, `buildExpandedGraph.ts` at the same revision | MIT | React, URL query state, Langfuse observation schema | Focus resolves observation IDs and can walk to a retained parent; expanded edges include timing-derived happened-before relations. PRC must keep native parent lineage separate from derived display edges | Medium: selection adapter plus explicit native/derived edge boundary required | `TraceGraphView.tsx` lines 66-70 and 104-123; README lines 44-47 |
| Persistent detail / raw evidence drill-down | AgentProvenance | `ADAPT` | `internal/dashboard/index.html` lines 356-369, 888-1015, 1180-1230 at `24765384a83047693b849b1be6b0c17116be558a` | Apache-2.0 (`LICENSE`) | Go embedded server, local JSON endpoints, inline HTML/JS/CSS; no PRC-compatible package boundary | Detail is AgentProvenance evidence/provenance, with its own kinds, lenses, and derived-edge model. PRC may reuse the interaction shape, not the evidence ontology | Medium-high: interaction can be re-expressed, data/lens APIs cannot be copied into PRC semantics | README lines 782-846; source shows selected node detail, local expansion controls, paged focused evidence, and bounded preview |
| Large-graph readability / summary to local graph | AgentProvenance | `PATTERN_ONLY` | `internal/dashboard/index.html` lines 652-724 and `1518-1529`; README lines 800-835 at the same revision | Apache-2.0 | Inline SVG, custom Sugiyama layout, local lens endpoints | Summary groups, `lineage/upstream/downstream/children`, and derived edges are security-provenance-specific; PRC cannot treat their groups as WorkStages | Low-medium for interaction pattern; high for implementation due semantic mismatch | Source shows bounded `localScope`, summary/expanded/raw detail, and focused evidence refs; not a drop-in module |
| Shared selection / view continuity | Langfuse `trace-graph-view` | `ADAPT` | `TraceGraphView.tsx` and `graphNodeMatching.ts` at `8b587645cf144b7bdf27883f59cd2c2e39552471` | MIT | React query params and Langfuse host view state | Selection identity is observation ID and repeated nodes cycle observations; PRC needs Agent/Event identity and must preserve its existing identity contract | Medium | README lines 44-47; source inspected in disposable clone |
| Focal + depth + dock interaction | Trailblaze | `INCONCLUSIVE` / `REJECT_FOR_NOW` | Unique public repository/package/source was not located from the supplied name; GitHub repository search and npm search produced no matching implementation | Unavailable | Unavailable | Cannot infer behavior, license, or semantic assumptions from a name or screenshot | Unknown; no integration estimate is admissible | Search results and source/license checks recorded as unavailable; no exact source path exists in this round |

## Q4 Compatibility Boundary

The interaction mechanics are not one uniform drop-in substrate:

- Langfuse offers the closest reusable graph renderer mechanics, but its
  observation identity, timing-derived edges, and graph modes require an
  adapter before PRC can use them.
- AgentProvenance offers a mature overview -> focused local graph -> raw
  evidence interaction, with explicit derived-edge treatment. Its security
  provenance graph and lens vocabulary must remain outside PRC semantics.
- The two can converge on a PRC-owned selection/view-state adapter only at the
  level of neutral references such as selected agent/event, view mode, focus,
  and evidence refs. Their upstream ontologies cannot be unified by direct
  reuse.
- Datadog Work segmentation remains unverified, so no upstream task model is
  admitted into the WorkStage contract.

The overall allowed verdict for this round is recorded in
`WORKSTAGE_COMPATIBILITY.md`: `INCONCLUSIVE`. Local Trajectory recognition and
structured activity extraction are partially confirmed, but WorkStage
segmentation compatibility is not established. No direct WorkStage import is
authorized by this evidence.
