# UI Convergence Reference Observations

本文件只记录本轮实际观察到的交互事实和证据边界，不把外部产品的模型或 ontology 带入 PRC。

## THOUGHTDAG_INTERACTION_FACTS

- 官方 demo：`https://app.thoughtdag.workers.dev/`。
- 在 overview 画布可以同时看到节点和分支边；加载 example 后仍保留 root/branch 的整体结构。
- 选择节点后，局部信息增加，但周围图结构没有被清空。
- timeline 可以按创建时间跳转到节点。
- zoom in、zoom out、fit view 和 minimap 是独立的导航操作。
- overview、example、selected、interaction 的截图、snapshot 和短视频位于 `reference-corpus/thoughtdag/`。
- 官方产品语义包含可编辑的 context edges；这只是观察到的外部事实，不能作为 PRC Runtime Model 或可编辑关系的授权。

证据边界：这些文件证明交互行为曾经在官方 demo 中可见，不证明 ThoughtDAG 的 ontology、context semantics 或任何 PRC runtime capability。

## AGENT_MONITOR_RUNTIME_FACTS

- Web demo 明确标记为 `DEMO MODE`，展示 sample data；不能当作 PRC 的真实 runtime evidence。
- Electron native app 读取到本机历史 run inventory，侧栏显示约 81 个 runs，来源包括 Codex、Claude Code 和多个 Home Project / PRC runs。
- 真实选择的 run 是 `Codex 14 agents / Home Project`，截图见 `reference-corpus/agent-monitor/native-14-agent-overview.png`。
- native run header 显示 `14 agents` 和 `13 spawn relationships`，与侧栏的 run 计数一致。
- run 画布显示 root 到 child 的连接、Agent 名称、模型、reasoning level、`Finished` 状态、input/output token 和 tool 数；可选择单个 Agent 查看其 trace。
- 选择单个 Agent 后，native detail 区域显示该 Agent 的模型、状态、token、`TOOLS` 数量、角色 `subagent` 和时间信息；截图见 `native-14-agent-selected.png`，可访问性快照见 `native-14-agent-selected.snapshot.txt`。
- native run inventory 与外部参考产品的实现行为相关，但不证明 PRC Observer 已经正确重建这些关系。PRC 必须继续以真实 app-server evidence 为准。
- Agent Monitor 仓库没有发现 LICENSE 或 SPDX license metadata；本仓库只采用 clean-room 交互参考，不复制代码或 assets。

## PRC_C0_FAILURES

- C0 的真实 browser capture 使用 PRC Runtime Observer / app-server data，不使用 synthetic nodes 或 edges。
- C0 仍是三列结构：Run list、Agent topology、selected Agent trace。它作为 `UI_BASELINE_C0`，不作为新变体的默认架构。
- C0 可以加载历史 runs，并显示 14-agent、27-agent 等较大 run；大 run 会造成超长 trace snapshot，整体方向和关系不容易快速读取。
- C0 的 trace 记录仍显示 `RECONCILIATION_UNRESOLVED`；这必须作为 runtime evidence boundary 展示，不能被 UI 解释成已完成对齐。
- C0 初始状态会显示“正在读取运行记录”，数据加载后才出现真实 run；加载状态属于可观察行为，不是 runtime completion 证据。
- C0 的截图、snapshot 和视频位于 `reference-corpus/prc-c0/`。

## EVIDENCE BOUNDARIES

- 截图和视频证明可见的 UI 状态与交互路径，不单独证明 runtime truth。
- 外部参考产品的视觉或交互事实不得改变 PRC 的 North Star、Runtime Identity Contract、Judgment Sidecar 或 Observer Independence boundary。
- 本轮所有 PRC 变体必须使用现有 Runtime Observer 的真实数据；禁止为了展示效果新增 fake node、fake edge 或 synthetic runtime event。
- `SHOW_JUDGMENTS=false`、`read_only=true`、`runtime_effect=NONE` 在本轮保持不变。
