# UI Convergence R1 Execution Packet

```yaml
round_id: PRC-UI-CONVERGENCE-R1-EXECUTION-20261006
status: AUTHORIZED_EXECUTION
frame_status: FRAME_OK__ADVISORY_ONLY
baseline: UI_BASELINE_C0
stop_condition: PRINCIPAL_REVIEW
initial_variant_limit: 3
refinement_limit: 2
```

## 执行目标

在不改变 PRC Runtime Observer、Runtime Identity Contract、Judgment Sidecar 或
runtime authority 的前提下，比较三种真正结构不同的 graph-first Presentation /
Interaction Layer。目标是获得可审计的 UI/交互证据，不是批准产品 UI baseline。

## 冻结边界

- ThoughtDAG-inspired graph-first Runtime Canvas 仅是只读 Presentation / Interaction Layer。
- runtime lineage 是 observed fact；用户不能创建或编辑 runtime relationship。
- 不引入 ThoughtDAG ontology、context-edge semantics、memory/model-context semantics、Control Plane、Task Board、Orchestrator 或 active intervention。
- 不修改 Codex Runtime Model、Runtime Identity Contract、Step 1 `canonical_event_id`、Judgment Sidecar 或 Observer Independence。
- 所有变体使用真实 Runtime Observer 数据；不得创建 fake topology。
- `SHOW_JUDGMENTS=false`、`read_only=true`、`runtime_effect=NONE`。
- Visual Review、UX Review、Runtime Truth Review 必须相互隔离；各自 verdict 不是 Human ratification。
- 不自动 merge winner；最终只把 Top 1 / Top 2 交给 Human Principal Review。

## 参考证据

- ThoughtDAG 交互证据：`reference-corpus/thoughtdag/`。
- Agent Monitor Web / native 证据：`reference-corpus/agent-monitor/`。
- C0 基线证据：`reference-corpus/prc-c0/`。
- 事实与限制汇总：`REFERENCE_OBSERVATIONS.md`。

## 变体实验设计

三个变体必须来自独立 worktree、同一 Runtime Observer backend 和同一真实数据集：

| 变体 | 主结构 | 与其他变体的关键差异 |
|---|---|---|
| V1-A | 空间 Agent graph + 侧边 trajectory rail | graph layout、Agent/trajectory 关系、selected disclosure、event detail |
| V1-B | 时间轨迹主视图 + parent/child lanes | graph layout、semantic zoom、run navigation、trace representation |
| V1-C | 关系网络主视图 + focus/inspect drawer | graph layout、selected disclosure、event detail、trace representation |

这些差异至少覆盖四个结构维度，不以颜色、字体或间距作为变体差异。

## 统一真实测试集

- 小型可理解 multi-Agent Run：真实的约 3-agent PRC run。
- 大型 orientation Run：真实的约 14-agent Home Project run，或当前 Observer 能稳定读取的同等历史 run。
- 每个变体都必须捕获：overview、root selected、child selected、zoomed-out graph、trajectory、event detail、large run、history/reopen、interaction video。

## 审查顺序

1. Visual Reviewer：只读 Product Brief、参考截图/视频和变体截图/视频。
2. UX Reviewer：只操作运行中的 browser，不看 source 或 builder rationale。
3. Runtime Truth Reviewer：对照 Observer / Agent Monitor evidence 检查 topology、status 和 trace ownership。
4. Comparator：综合人类任务表现、可读性、runtime truth、大 run 可用性和冻结边界。

阻断条件：仍以三列 dashboard 为主、graph 不可读、root/child 不清楚、trace leakage、large run 不可用、或出现 fake topology。

## Refinement / rollback

winner 最多 refinement 两轮。每轮只处理前三个观察到的 UX/visual failure，并重新截图、复审；若 task success、graph readability、runtime correctness 或 large-run usability 出现实质 regression，自动回滚并记录证据。

## 当前完成度

- Frame A / Pass A / Pass B：已完成，`FRAME_OK`，advisory only。
- Upstream-first 与失败分类 invariant：已在 `fcdbdc1` 冻结。
- ThoughtDAG / Agent Monitor / C0 reference capture：已完成；native Agent Monitor 真实 14-agent capture 已补充。
- 三个独立 UI worktree、三变体实现与 review：尚未完成。
- 最终状态：必须停止在 `PRINCIPAL_REVIEW`，不得自动 merge 或 promote。
