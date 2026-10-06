# PRC UI Convergence R1 — Human Review Packet

```yaml
round_id: PRC-UI-CONVERGENCE-R1-EXECUTION-20261006
status: PRINCIPAL_REVIEW
decision_authority: HUMAN_PRINCIPAL
product_ui_approval: NOT_GRANTED
automatic_merge: FORBIDDEN
```

## 1. 本轮边界

本轮只比较 Project Runtime Console 的 Presentation / Interaction Layer。
ThoughtDAG-inspired graph-first Runtime Canvas 已经由 Principal 正式授权，但
仍然只是只读展示层，不是新的 runtime model、ontology 或 authority surface。

保持不变：PRC North Star、Codex Runtime Model、Runtime Identity Contract、
Step 1 `canonical_event_id`、Judgment Sidecar、`SHOW_JUDGMENTS=false`、
`read_only=true`、`runtime_effect=NONE` 和 Runtime Observer Independence。

仍然禁止：ThoughtDAG product ontology、editable runtime lineage、context-edge
semantics、memory/model-context semantics、user-created runtime relationships、
Control Plane、Task Board、Orchestrator 和 active intervention。

## 2. 已冻结治理不变量

- `IMPLEMENTATION_FAILURE -> repair current frame`
- `MODEL_ASSUMPTION_FAILURE -> bounded model repair`
- `FRAME_CONTRADICTION -> FRAME_REOPEN_CANDIDATE`
- 只有 Human Principal 可以 `AMEND` 或 `SUPERSEDE` frozen frame。
- 外部系统语义遵循：official upstream contract/source -> mature prior art ->
  local compatibility validation -> unresolved gaps only。
- `FRAME_OK` 是进入本轮执行的 advisory checkpoint，不是 UI approval 或 model
  validity。

相关 checkpoint：`fcdbdc1`、`experiments/ui-convergence/receipts/frame-pass-b.json`。

## 3. Reference Corpus

### ThoughtDAG

官方 demo `https://app.thoughtdag.workers.dev/` 的实际观察结果：overview 中可见
分支边；选择节点会增加局部详情但保留周围图；timeline、zoom、fit view 和
minimap 是独立导航操作。截图、snapshot 和视频在
`experiments/ui-convergence/reference-corpus/thoughtdag/`。

这只证明交互事实，不授权 ThoughtDAG ontology 或 context-edge semantics。

### Agent Monitor

Web demo 明确是 `DEMO MODE`，只能作为 sample-data 交互参考。Electron native
app 读取到本机约 81 个历史 runs；本轮实际选择的 run 是 `Codex 14 agents / Home
Project`，native evidence 显示 `14 agents`、`13 spawn relationships`，并能看到
Agent 状态、模型、token、tool 数和单 Agent trace。证据位于
`experiments/ui-convergence/reference-corpus/agent-monitor/`，包括：

- `native-14-agent-overview.png`
- `native-14-agent-selected.png`
- `native-14-agent-selected.snapshot.txt`

Agent Monitor 未发现 LICENSE / SPDX metadata；本仓库只采用 clean-room 交互参考，
没有复制其代码或 assets。

### C0

C0 是真实 app-server data 驱动的三列 baseline：Run list、Agent topology、selected
Agent trace。它保留为 `UI_BASELINE_C0`，不作为新变体默认结构。大 run 会出现超长
trace，且当前真实数据仍明确显示 `RECONCILIATION_UNRESOLVED`；这些都是 evidence
boundary，不由本轮 UI 改写。

## 4. Test Data

- Small run：`01a10d11-94f6-7af2-b7e2-455929f127bb`，3 agents，真实 Codex
  app-server data。
- Large run：`01a0f0b2-1bd3-7501-87a2-681d45cdd051`，14 agents，真实 Codex
  app-server data；Observer 返回 13 条 parent-child spawn relationship。
- 三个变体都通过同一组 read-only API：`/api/health`、`/api/runs`、
  `/api/runs/<run_id>`。

## 5. 三个结构变体

### V1-A — Spatial Agent Graph + Trajectory Rail

结构：中心是按真实 parent-child id 排布的空间 Agent graph，底部是选中 Agent 的
事件轨迹 rail，右侧是选中 Agent inspector；支持 root、fit、zoom、run 切换。

证据：

- `/experiments/ui-convergence/variants/v1-a/small.png`
- `/experiments/ui-convergence/variants/v1-a/large.png`
- `/experiments/ui-convergence/variants/v1-a/child.png`
- `/experiments/ui-convergence/variants/v1-a/event.png`
- `/experiments/ui-convergence/variants/v1-a/history-reopen.png`
- `/experiments/ui-convergence/variants/v1-a/large.snapshot.txt`
- `/experiments/ui-convergence/variants/v1-a/child.snapshot.txt`
- `/experiments/ui-convergence/variants/v1-a/event.snapshot.txt`
- `/experiments/ui-convergence/variants/v1-a/interaction.webm`

### V1-B — Timeline Lanes + Relationship Navigation

结构：中心是每个真实 Agent 一条 lane 的时间轨迹，事件沿 lane 顺序展开；左侧
保留 run/history，右侧显示选中 Agent；紧凑/展开控制改变每个 lane 的 disclosure。
parent/child 关系通过真实 Agent metadata 在 lane label 中显示。

证据：

- `/experiments/ui-convergence/variants/v1-b/small.png`
- `/experiments/ui-convergence/variants/v1-b/large.png`
- `/experiments/ui-convergence/variants/v1-b/child.png`
- `/experiments/ui-convergence/variants/v1-b/event.png`
- `/experiments/ui-convergence/variants/v1-b/history-reopen.png`
- `/experiments/ui-convergence/variants/v1-b/large.snapshot.txt`
- `/experiments/ui-convergence/variants/v1-b/child.snapshot.txt`
- `/experiments/ui-convergence/variants/v1-b/event.snapshot.txt`
- `/experiments/ui-convergence/variants/v1-b/interaction.webm`

### V1-C — Focused Relationship Map + Inspect Drawer

结构：中心是关系聚焦图，顶部提供 parent/root/child 导航，图下方是当前 Agent 的
事件带，右侧 drawer 显示 Agent identity、trace、tool item 和原始归一化 event。
它把“从当前节点沿关系检查证据”作为主要交互。

证据：

- `/experiments/ui-convergence/variants/v1-c/small.png`
- `/experiments/ui-convergence/variants/v1-c/large.png`
- `/experiments/ui-convergence/variants/v1-c/child.png`
- `/experiments/ui-convergence/variants/v1-c/event.png`
- `/experiments/ui-convergence/variants/v1-c/history-reopen.png`
- `/experiments/ui-convergence/variants/v1-c/large.snapshot.txt`
- `/experiments/ui-convergence/variants/v1-c/child.snapshot.txt`
- `/experiments/ui-convergence/variants/v1-c/event.snapshot.txt`
- `/experiments/ui-convergence/variants/v1-c/interaction.webm`

## 6. Review Results

以下是本轮 browser/image evidence 的 advisory review，不是 Product UI approval。

### Visual / Information Hierarchy

| Variant | Observed strengths | Observed risks | Result |
|---|---|---|---|
| V1-A | root、child、边和 selected disclosure 同时可见；空间关系最直观；大 run 仍可通过 canvas scroll/zoom 定位 | 14-agent 横向图需要水平滚动；底部 rail 与右侧 inspector 同时争夺注意力 | PASS_WITH_LIMITS |
| V1-B | 14-agent run 的事件顺序和 Agent 间对照最清晰；紧凑/展开是明确的 semantic disclosure | 关系图被 lane 结构弱化；更像时间分析器；大 run 纵向滚动负担较大 | PARTIAL |
| V1-C | focus path、parent/root/child 导航、drawer evidence 关系清楚；单 Agent 检查最完整 | 大 run 的全局 branch orientation 不如 A；右侧 trace 仍可能很长 | PASS_WITH_LIMITS |

### UX Task Check

任务：识别 root、数 direct children、打开 Child A、切换 Child B、找到 tool
call/result、从 overview 到 Agent 到 event、返回 overview、打开 14-agent run、
reload 后 reopen history。

- V1-A：root/children、child trace、event detail、14-agent orientation、reload
  reopen 均可操作；点击路径短，主要负担是横向 canvas 定位。
- V1-B：root/lane、child lane、event detail、14-agent history 均可操作；事件顺序
  最容易比较，主要负担是从 lane 回到关系全局。
- V1-C：root/parent/child path 和 drawer evidence 最直接；14-agent 全局方向需要
  更多滚动，主要负担是 focus view 与全局 view 的切换。

### Runtime Truth Check

- 三个变体都直接读取同一 Runtime Observer API，没有写入或启动 Codex turn。
- parent-child 展示均来自返回的 `parent_runtime_agent_instance_id`；代码中没有
  hard-coded runtime IDs、fake nodes 或 synthetic events。
- 14-agent run 的实际 evidence 是 14 agents / 13 relationships；截图中显示的
  Agent names、models、statuses、event types 来自 API response。
- 三个变体都保留 `notLoaded` 和 `RECONCILIATION_UNRESOLVED`，没有把它们推断为
  completed 或已对齐。
- 现有事件的 `canonical_event_id` 仍为 unresolved；本轮没有修改 identity 或
  reconciliation semantics。

## 7. Comparator

### WINNER — V1-A

选择依据不是算术总分，而是本轮主要产品问题：Human 是否能先看懂真实 Agent
topology，再进入具体 trace。V1-A 的空间关系、root/child 边和 selected Agent
disclosure 最直接，且保留了从 graph 到 trajectory 到 event 的连续路径。

### RUNNER_UP — V1-C

V1-C 的单 Agent evidence inspection 和 parent/root/child 导航最完整，适合核查单条
关系与 trace；但在 14-agent 大 run 的整体方向感上弱于 V1-A。

### Third — V1-B

V1-B 对事件顺序的比较最强，但 parent-child topology 被 lane 结构吸收，不能作为
当前 round 的首选 graph-first presentation。

## 8. Refinement / Rollback

本轮没有执行 winner refinement，也没有 rollback：

```yaml
winner_refinement_rounds: 0
rollback_count: 0
reason: initial_variants_produced_sufficient_comparative_evidence_for_principal_review
```

这不表示 winner 已被批准，也不表示可自动合并。

## 9. Commands

三个 worktree 已隔离并各自有 implementation commit：

- V1-A：`/tmp/prc-ui-v1-a`，commit `6c171c9`，运行 `python3 apps/console/server.py --port 8877`
- V1-B：`/tmp/prc-ui-v1-b`，commit `6c71300`，运行 `python3 apps/console/server.py --port 8878`
- V1-C：`/tmp/prc-ui-v1-c`，commit `846b228`，运行 `python3 apps/console/server.py --port 8879`

三个服务都只读访问本机 Codex app-server；不要把 worktree commit 自动 merge 到
`main`。

## 10. Known Limitations / Uncertainty

- 本轮完成了本地 browser/image/runtime-truth evidence review，但没有把三条 reviewer
  角色伪装成已经产生独立 DSH receipt；独立 Visual Reviewer、UX Reviewer 和
  Runtime Truth Reviewer 的正式 receipt 仍是缺口。
- 现有 Observer 的历史线程状态和 event reconciliation 仍有 `notLoaded` /
  `RECONCILIATION_UNRESOLVED`。UI 只显示边界，没有修复它们。
- Agent Monitor 的 native capture 是外部行为参考，不是 PRC correctness evidence。
- 尚未做移动端和极小窗口的 usability review。
- 本轮没有测试 provider Judge、Shadow Judgment 展示或任何 active intervention；
  `SHOW_JUDGMENTS=false` 保持不变。

## 11. Principal Decision Required

请 Principal 只对以下 bounded decision 作裁决：

1. 是否接受 V1-A 作为下一轮可继续 refine 的 presentation candidate；
2. 是否接受 V1-C 作为 runner-up reference；
3. 是否保持当前 `PRINCIPAL_REVIEW`，不 merge、不 promote、不进入 Product v0 baseline。

本 packet 不替 Principal 做 UI ratification，也不授权下一轮 refinement。
