# 当前状态

更新：2026-10-13。产品状态：**NOT_ACCEPTED**。

## 已批准方向
让非底层调试使用者通过统一可视化理解项目推进、执行者行动、请求变成结果，并核对依据。
Work 讲工作内容演变；Agents 讲执行结构与过程；Trace 讲具体执行；侧栏讲任务、变化和实际结果。
B2/C 是批准体验基础；Langfuse/ThoughtDAG 的补充层级尚在决策，不得将不同关系合成未证明的因果线。

## 本轮：历史工作树清理，不是新产品实现
- 保留 Python 读取/服务、来源定位、稳定 occurrence、证据和既有测试。
- 去重仅跳过重复调用，不丢弃同 call ID 的工具结果；血缘仅由有明确 sender 的 spawn 证据建立。
- 删除已覆盖的身份墙/样本专用旧渲染器，提取共享核心、执行图和 C 页面；一个入口初始化。
- 保留单 Session 步骤图和地图/证据交互；移除活跃样本专用摘要与硬编码 404。角色线索明确是待整理内容，不代表通用理解能力。
- 固定样本检查仅为诊断，不读取历史 DSH 回执作为当前审核；默认测试不读取私人 Session。

## 仍未完成
可读任务/变化/结果摘要、完整可视化 Trace、child 内部记录读取、Work 转折/关系交互和完整导航恢复。保留的旧界面不代表已经符合 Experience Star。

## 下一步
先出新实现方案，再独立 global review；reviewer 先看用户目标、批准参考和失败反例，再看有界提案，不继承作者的完整推理上下文。通过后才实施。
Issue 入口：
- https://github.com/kaiykk/project-runtime-console/issues/2
- https://github.com/kaiykk/project-runtime-console/issues/3
- https://github.com/kaiykk/project-runtime-console/issues/4

## 历史与权限
Git 历史保留；本机原文、旧未提交状态说明及过程证据保留在本机忽略目录，不上传私人内容。
用户授权本轮清理后的 commit/push；未授权合并、强推或重写历史。Claude Code 是 PRC 唯一产品写入者。
