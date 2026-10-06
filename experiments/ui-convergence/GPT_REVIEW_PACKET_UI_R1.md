# GPT Review Packet — PRC UI Convergence R1

```yaml
packet_type: GPT_REVIEW_PACKET
round_id: PRC-UI-CONVERGENCE-R1-EXECUTION-20261006
project: project-runtime-console
review_target: previous_ui_convergence_result
status: HUMAN_EXPECTATION_MISMATCH__PRINCIPAL_REVIEW
prepared_by: Codex Manager
product_ui_approval: NOT_GRANTED
winner_ratification: NOT_GRANTED
refinement_authorized: false
merge_authorized: false
```

## 0. Review Request

Human Principal 的反馈是：上一轮输出结果与预期依旧差别很大。这个反馈优先于
本地 comparator 的相对排序。本 packet 的目的不是为 `V1-A` 胜出辩护，而是请
GPT 独立判断本轮失败的性质和下一步边界。

请重点判断：

1. 我们是否把一个尚未充分确认的 Human-facing 目标错误翻译成了
   graph-first runtime dashboard；
2. 本轮是否主要优化了 Agent topology、trace navigation 和 runtime evidence，
   却没有交付 Human 真正需要的工作体验；
3. 这属于 `IMPLEMENTATION_FAILURE`、`MODEL_ASSUMPTION_FAILURE`、
   `FRAME_CONTRADICTION`，还是 `INSUFFICIENT_REVIEW_EVIDENCE`；
4. 在没有补充 Human 对理想体验的明确描述之前，是否根本不应继续做 UI refinement。

不要擅自补写 Human 的理想 UI，也不要因为某个候选在相对比较中排名第一，
就把它解释成产品方向正确。

## 1. Principal Authorization and Frozen Boundaries

本轮基于 Human Principal 已授权的 Frame Change：

- ThoughtDAG-inspired graph-first Runtime Canvas 可以作为 v0 的只读
  Presentation / Interaction Layer；
- 可以在 bounded、attributed 条件下复用 ThoughtDAG MIT 代码；
- graph 只能表达既有 Project / Run / Codex Runtime Observer facts；
- graph 不是新的 runtime model、ontology 或 authority surface。

以下边界没有被修改：

- PRC North Star；
- Codex Runtime Model；
- Runtime Identity Contract；
- Step 1 `canonical_event_id` semantics；
- Judgment Sidecar boundary；
- `SHOW_JUDGMENTS=false`、`read_only=true`、`runtime_effect=NONE`；
- Runtime Observer Independence；
- 不允许 editable runtime lineage、context-edge semantics、
  memory/model-context semantics 或任意用户创建的 runtime relationship；
- 不允许 Control Plane、Task Board、Orchestrator 或 active intervention；
- Product UI approval、winner ratification 和 frame supersession 仍由 Human Principal
  单独决定。

原始 frame amendment：
`docs/ui-frame-change-v1.md`

治理不变量：

```text
Freeze protects against premature drift;
Evolution protects against frozen mistakes.

IMPLEMENTATION_FAILURE
  -> repair inside the current frame

MODEL_ASSUMPTION_FAILURE
  -> bounded model repair

FRAME_CONTRADICTION
  -> FRAME_REOPEN_CANDIDATE
```

本 review 必须遵守：reviewer 可以提出 reopen，但 Manager 不得静默重解释
frozen frame；没有 Human Principal 授权，不得修改 frame。

## 2. What Was Actually Executed

本轮是一个 bounded UI comparison，不是产品 UI 发布，也不是 runtime model 变更。

执行内容：

- 在三个隔离 worktree 中构建三个结构不同的 Presentation / Interaction Layer；
- 三个变体共享同一个 Runtime Observer backend；
- 三个变体都读取真实 Codex app-server / Runtime Observer 数据；
- 使用 small multi-Agent run 和 large Home Project run；
- 捕获 overview、root、child、event、large run、history reopen 和 interaction video；
- 进行了本地 browser/image/runtime-truth evidence review；
- 没有修改 Runtime Identity、Judgment Sidecar、`canonical_event_id`、Observer
  semantics 或 active intervention；
- 没有 merge 任意变体；
- 没有执行 winner refinement；
- 没有获得独立 Visual / UX / Runtime Truth reviewer receipts。

执行 packet：

- `experiments/ui-convergence/EXECUTION_PACKET.md`
- `experiments/ui-convergence/REFERENCE_OBSERVATIONS.md`
- `experiments/ui-convergence/HUMAN_REVIEW_PACKET_UI_R1.md`

## 3. Baseline and Reference Facts

### 3.1 C0 baseline

`C0` 是真实数据驱动的三列 baseline：

- Run list；
- Agent topology；
- selected Agent trace。

它的已知问题包括：large run 的 trace 很长，整体关系不易快速读取，部分历史
状态仍然显示 `RECONCILIATION_UNRESOLVED`。这些是 runtime evidence boundary，
不是 UI 可以自行推断或修复的事实。

C0 被记录为 `UI_BASELINE_C0`，本轮没有把它视为已经满足产品目标。

### 3.2 外部交互参考

ThoughtDAG 观察到的交互事实：overview graph、branch edge、selected node 的局部
disclosure、timeline、zoom、fit view、minimap。它只证明这些交互在外部 demo 中
可见，不证明 PRC 应采用 ThoughtDAG ontology、context semantics 或 editable
relationship。

Agent Monitor native capture 观察到：真实 run inventory、parent-child graph、
Agent status/model/token/tool 数、单 Agent trace。其仓库没有发现 LICENSE / SPDX
metadata，因此本项目只采用 clean-room interaction reference，没有复制其代码
或 assets。该 capture 也不证明 PRC Observer 已经正确恢复全部 runtime semantics。

参考材料：

- `experiments/ui-convergence/reference-corpus/thoughtdag/`
- `experiments/ui-convergence/reference-corpus/agent-monitor/`
- `experiments/ui-convergence/reference-corpus/prc-c0/`

## 4. Three Variants and Evidence

### V1-A — Spatial Agent Graph + Trajectory Rail

结构：中心空间 Agent graph，底部 selected Agent trajectory rail，右侧 inspector；
支持 root、fit、zoom、run 切换。

worktree / commit：

- `/tmp/prc-ui-v1-a`
- `6c171c9`

证据：

- `experiments/ui-convergence/variants/v1-a/small.png`
- `experiments/ui-convergence/variants/v1-a/large.png`
- `experiments/ui-convergence/variants/v1-a/child.png`
- `experiments/ui-convergence/variants/v1-a/event.png`
- `experiments/ui-convergence/variants/v1-a/history-reopen.png`
- `experiments/ui-convergence/variants/v1-a/large.snapshot.txt`
- `experiments/ui-convergence/variants/v1-a/child.snapshot.txt`
- `experiments/ui-convergence/variants/v1-a/event.snapshot.txt`
- `experiments/ui-convergence/variants/v1-a/interaction.webm`

### V1-B — Timeline Lanes + Relationship Navigation

结构：每个 Agent 一条 timeline lane，事件沿 lane 展开；parent/child 关系通过
真实 Agent metadata 表达，支持 compact / expanded disclosure。

worktree / commit：

- `/tmp/prc-ui-v1-b`
- `6c71300`

证据：

- `experiments/ui-convergence/variants/v1-b/small.png`
- `experiments/ui-convergence/variants/v1-b/large.png`
- `experiments/ui-convergence/variants/v1-b/child.png`
- `experiments/ui-convergence/variants/v1-b/event.png`
- `experiments/ui-convergence/variants/v1-b/history-reopen.png`
- `experiments/ui-convergence/variants/v1-b/large.snapshot.txt`
- `experiments/ui-convergence/variants/v1-b/child.snapshot.txt`
- `experiments/ui-convergence/variants/v1-b/event.snapshot.txt`
- `experiments/ui-convergence/variants/v1-b/interaction.webm`

### V1-C — Focused Relationship Map + Inspect Drawer

结构：关系聚焦图、parent/root/child 导航、当前 Agent event strip，以及显示 identity、
trace、tool item 和原始归一化 event 的 inspect drawer。

worktree / commit：

- `/tmp/prc-ui-v1-c`
- `846b228`

证据：

- `experiments/ui-convergence/variants/v1-c/small.png`
- `experiments/ui-convergence/variants/v1-c/large.png`
- `experiments/ui-convergence/variants/v1-c/child.png`
- `experiments/ui-convergence/variants/v1-c/event.png`
- `experiments/ui-convergence/variants/v1-c/history-reopen.png`
- `experiments/ui-convergence/variants/v1-c/large.snapshot.txt`
- `experiments/ui-convergence/variants/v1-c/child.snapshot.txt`
- `experiments/ui-convergence/variants/v1-c/interaction.webm`

## 5. Observed Results

### 5.1 Local relative comparison

```text
WINNER: V1-A
RUNNER_UP: V1-C
THIRD: V1-B
```

本结果的含义仅是：在本地比较标准下，V1-A 比 V1-B / V1-C 更容易先看懂
当前真实 Agent topology，再进入 selected Agent trace。

本结果不证明：

- V1-A 满足 North Star；
- graph-first 是正确的产品信息架构；
- Human 需要 Agent topology 作为首页主组织方式；
- V1-A 可以进入 Product v0 baseline；
- V1-A 可以进入 refinement 或 merge；
- 当前模型已经表达了 Human 想理解的工作对象。

### 5.2 本地 review 中的正向观察

- V1-A 的 root、child、边和 selected disclosure 同时可见；
- V1-B 的事件顺序和 Agent 间对照最清晰；
- V1-C 的单 Agent evidence inspection 和关系导航最完整；
- 三个变体均使用同一个真实 Observer API；
- 没有发现 hard-coded runtime IDs、fake nodes 或 synthetic runtime events；
- `notLoaded` 和 `RECONCILIATION_UNRESOLVED` 没有被 UI 静默推断为 completed 或
  已对齐。

### 5.3 本地 review 中的限制

- V1-A 的 14-agent 横向 graph 需要滚动，底部 rail 和右侧 inspector 争夺注意力；
- V1-B 更像时间分析器，关系全局被 lane 结构弱化；
- V1-C 的 large-run 全局方向感弱于 V1-A；
- large run 仍可能出现很长的 trace；
- 尚未做移动端和极小窗口 review；
- 没有独立 Visual / UX / Runtime Truth reviewer receipt；
- runtime history / event reconciliation 仍有 `notLoaded` 与
  `RECONCILIATION_UNRESOLVED` boundary。

## 6. DSH Boundary Result

DSH 读取了上一轮 Human Review Packet 的治理边界，并返回 advisory boundary：

```yaml
global_decision: PRINCIPAL_REVIEW
advisory_only: true
winner_ratified: false
refinement_authorized: false
product_ui_approved: false
governance_audit_receipt_issued: false
dsh_review_claim: false
```

Receipt：
`experiments/ui-convergence/receipts/final-global-review.json`

该结果不能被解释为 DSH 已经独立审查了每个变体的截图、source 或运行中的 browser。
Receipt 明确列出了未审查项，因此本 packet 不把 DSH 结果包装成 Product UI approval。

## 7. Central Mismatch

Human 的最新判断是：结果与预期依旧差别很大。当前仓库没有一份足够具体的
Human Experience Reference 可以在本 packet 中替 Human 解释“预期到底是什么”；
因此不应自行填充缺失目标。

本轮最需要审查的可能偏差是：

```text
Human wanted a durable, understandable way to re-enter and work with the
runtime/project experience.

The round optimized a graph-first runtime observability surface:
agent topology -> selected agent -> trace/event inspection.
```

这只是待审的 failure hypothesis，不是已经确认的结论。请判断：

- graph 是否把 research/runtime variables 错误提升成了产品 IA；
- Agent tree / trace / event 是否成为了产品中心，而不是支撑 Human 任务的 evidence；
- 本轮是否在解决“如何看见 runtime”而不是“Human 需要如何理解和重新进入工作”；
- Frame Change 允许 graph-first presentation，是否被误读成了 graph-first product
  requirement；
- 现有 review 任务是否只验证了“能否操作和观察”，没有验证“是否符合 Human
  experience reference”。

不要因为这些问题看起来合理就自动判定为 `FRAME_CONTRADICTION`。请以 packet、
North Star、实际截图/视频和 Human feedback 为依据，并明确事实与假设的边界。

## 8. Questions for GPT Reviewer

请按以下顺序回答：

### A. Goal

基于 `docs/NORTH_STAR.md`、现有 frame amendment 和 Human 的“差别很大”反馈，
本轮实际验证的 Goal 是什么？本轮是否把 Goal 缩窄或替换成了另一个 Goal？

### B. Existing Capability

本轮实际证明了哪些能力？仅列有证据支持的能力，例如：

- 真实 runtime data 是否可呈现；
- parent-child topology 是否可导航；
- selected Agent trace 是否可查看；
- history reopen 是否可操作；
- evidence boundary 是否可见。

不要把截图合理、相对排名第一或测试通过提升为 Product / North Star 价值证据。

### C. Missing Capability

当前结果距离 Human 预期还缺哪些能力？请区分：

- implementation gap；
- model / representation gap；
- missing Human Experience Reference；
- missing review evidence。

### D. Failure Classification

只选择并论证一个主分类，必要时列出次级因素：

```text
IMPLEMENTATION_FAILURE
MODEL_ASSUMPTION_FAILURE
FRAME_CONTRADICTION
INSUFFICIENT_REVIEW_EVIDENCE
```

如果选择 `FRAME_CONTRADICTION`，必须指出被哪条新 Human intent、upstream/prior-art
evidence，或 North Star blocking evidence 触发；不能仅因为结果不好看就 reopen frame。

如果选择 `MODEL_ASSUMPTION_FAILURE`，必须指出是哪一个 representation assumption
需要做 bounded model repair。

如果选择 `INSUFFICIENT_REVIEW_EVIDENCE`，必须明确缺什么独立证据，以及在没有该证据
时哪些结论不能下。

### E. Continue / Stop Decision

在不重新设计 UI 的前提下回答：

- 当前是否应停留在 Principal Review；
- 是否需要先补 Human Experience Reference / intent-fidelity evidence；
- 是否允许任何变体进入 refinement；
- 是否允许 merge 或 promote。

如建议继续研究，只能提出一个 bounded question，不能开启 broad UI research。

## 9. Required Reviewer Output

请返回一个明确的 review verdict，包含：

```yaml
REVIEW_SCOPE:
  reviewed:
  not_reviewed:
  cannot_conclude:

PRIMARY_CLASSIFICATION:
  one_of:
    - IMPLEMENTATION_FAILURE
    - MODEL_ASSUMPTION_FAILURE
    - FRAME_CONTRADICTION
    - INSUFFICIENT_REVIEW_EVIDENCE
  evidence:

CURRENT_CAPABILITY:
MISSING_CAPABILITY:
OPEN_HUMAN_INTENT:
RECOMMENDED_STOP_OR_NEXT_STEP:
```

并明确回答：

```text
MERGE: FORBIDDEN unless separately authorized by Human Principal
REFINEMENT: FORBIDDEN unless separately authorized by Human Principal
PRODUCT_UI_APPROVAL: NOT_GRANTED
FRAME_STATUS: unchanged unless Human Principal amends it
```

## 10. Explicit Non-Authorization

在 GPT review 和 Human Principal 后续决定之前，本 packet 不授权：

- 继续 polish 或 refine V1-A、V1-B、V1-C；
- 合并任意 variant worktree commit；
- 把 V1-A 作为 Product v0 baseline；
- 重做 graph、canvas、timeline 或 drawer 设计；
- 引入新的 ontology、schema、Control Plane、Task Board 或治理框架；
- 修改 Runtime Identity、Observer semantics、Judgment Sidecar 或 event identity；
- 用本地 comparator 或 passing tests 代替 Human ratification；
- 把上一轮的 advisory DSH output 说成独立 UI approval。

本轮保持 `PRINCIPAL_REVIEW`，直到 Human Principal 对 review 结论和下一步作出单独决定。

## 11. Evidence Index

核心 packet：

- `experiments/ui-convergence/HUMAN_REVIEW_PACKET_UI_R1.md`
- `experiments/ui-convergence/EXECUTION_PACKET.md`
- `experiments/ui-convergence/REFERENCE_OBSERVATIONS.md`
- `experiments/ui-convergence/receipts/final-global-review.json`
- `docs/ui-frame-change-v1.md`
- `docs/NORTH_STAR.md`
- `docs/SHELL_FREEZE_V0.md`

Variant evidence：

- `experiments/ui-convergence/variants/v1-a/`
- `experiments/ui-convergence/variants/v1-b/`
- `experiments/ui-convergence/variants/v1-c/`

Running local indexes for human inspection：

- V1-A：`http://127.0.0.1:8877/`
- V1-B：`http://127.0.0.1:8878/`
- V1-C：`http://127.0.0.1:8879/`

主仓库 C0 当前未运行：`http://127.0.0.1:8765/`。如需查看 C0，必须单独启动
`python3 apps/console/server.py --port 8765`；这不是本 packet 的执行步骤，也不改变
本轮停止条件。

