# PRC — Agents Surface C / 独立交互原型

状态：`EXPLORATION_ONLY` — 未冻结 / 不替代 OpenDesign A/B / 不进入 production。

## 开始

双击 `prc_agents_surface_C_interactive.html` 即可。它内嵌了已脱敏的 fixture，无需本地服务、数据库或外部请求。建议桌面浏览器宽度 ≥ 1280px，最初用「适配」使空间进入视口。

## C 的产品假设

这不是 27 个等大 Agent 节点，也不是把 event count 画成圆点。

- 第一层：从原生派发内容识别**目前有证据支持的任务类别**。四个子 Agent 可以展示在三块**DERIVED、可回溯**的区域中；其余 22 个**只有身份，不编造任务**。
- 第二层：选择 Agent 后，详情优先呈现它为何被派发、真实 Agent 执行消息、最后一条原生 Agent 消息，再到原始记录。
- 第三层：Trace 读取与所选 Agent 关联的、包内保留的执行样本；可从 Trace 回到 Spatial Canvas，保持 selection/viewport。
- 原生血缘另有 27 项可核对的列表；工作区域本身不等于 native parent/child 或 WorkStage。

## 建议用同样的 3 个用户任务对比 A、B、C

1. **30 秒概览**：不看文件名/ID，你能说出目前哪些 Agent 的任务已知、哪些未知吗？是否误认为看到的三类任务覆盖全部 27 个？
2. **子 Agent 意图与交付**：先选 `Schrodinger`（浅层系统侦察），再选 `Kierkegaard`（已授权写入）；能否找到完整 native dispatch prompt、实际 agentMessage、最后 native message？你能区分「最后说了什么」与「已经验证什么」吗？
3. **证据与回退**：选择 `Gibbs`，查看执行证据 → 点一条真实记录 → 返回地图；选中 Agent 是否保持？手动缩放后的视口是否保持？

可测试第四题：点开任何一个内容未知的 Agent，例如 `Kuhn`，验证是否诚实显示 `UNAVAILABLE` 而非从 event count 编出任务。

## 必须保留的边界

- 数据：全部 27 个 native Agent 身份，26 条 parent/child；其中仅 5 个（含 Root）有脱敏原生输入和消息正文。
- 4 个子 Agent 在地图上的 3 个组，**仅依据原生派发信息制作的 `DERIVED` 演示性分组**，不是自动分类系统，也不是 WorkStage，更不是 27 Agent 的工作结构全覆盖。
- Evidence 浏览器显示 `representative-agents.json` 的**选录记录**，而非全部 4,251 条执行内容。原始 native ID 保留于取证记录。
- 所有显示的输出都是 **last native agentMessage**，不是单独的 provider return，也不等于已验证任务完成。
- Root 的首个 userMessage 与最终 last native message 相隔多轮，不能把两者拼为一个端到端任务的因果故事。
- 这份数据不支持完善的跨 WorkStage 关联、全部 Agent 的任务叙事、hidden reasoning、逐结论支持关系。

## C 的已知弱点（不隐瞒）

1. 大屏上地图整体需要缩放，节点微文案可能偏小；真正的详细内容在不缩放的右侧 Inspector。
2. 工作区域的角色标签是人工从 4 个代表性派发 prompt 提取的**设计假设**。尚未测试可泛化的自动分组，也没有验证真正的 Run-level WorkStage。
3. UI 使用的是被摘录的 native agentMessage，没有完整涵盖所选 Agent 的全部执行历史或工具输出。
4. Timeline 未做成可用视图；Work Surface 未连入。这是 `Agents Surface` 设计探索，不是完整的 PRC。
5. 这是一次单设计者独立实现的 C 候选；用户理解度还未经独立盲评。不能用实现完成替代产品 PASS。

## Design Guard

`FRAME_MISMATCH`：如果人否决 C 的整个空间与信息架构，不能先把任务降级为「调一下右侧栏、换配色」；必须回到 Whole Surface 方向判断。允许修复经人批准框架内的局部缺陷，但不允许用局部 patch 冒充整体产品验证。
