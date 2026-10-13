# Project Runtime Console

PRC 是本地只读的 Agent 工作可视化阅读器。当前是尚未通过产品验收的工作基线，不是完成产品。

## North Star / Experience Star

让非底层调试使用者通过统一可视化理解项目如何推进、执行者如何行动、一次请求怎样变成结果，并能随时核对依据。

- Work：工作内容演变；B2 人工案例是明确标注的参考，不冒充自动重建。
- Agents：执行结构和过程；没有子 Agent 仍应有请求、动作、结果的有用执行图。
- Trace：所选工作的具体执行；原始记录列表不是最终体验。
- 侧栏：任务、这一步带来的变化、实际结果；身份与原文是展开依据。

B2/C 是批准的体验基础，Langfuse/ThoughtDAG 仅在明确补充层级后使用。当前任务摘要与完整 Trace 仍未完成，不能将保留的预览实现当作目标已经达成。

## Run

```bash
python3 apps/console/server.py 4173
```

打开 http://127.0.0.1:4173 。读取本机 `~/.codex/sessions` 和 `~/.codex/archived_sessions`，源文件只读。可以在 URL 指定 `session_id`；没有对应本机记录就报告缺失，不使用 mock 数据回退。当前保留的默认样本在其他机器上可能不存在。

前端：共享 `prc-core.js`、单 Session `prc-execution.js`、C 预览 `prc-agents.js`、父侧适配 `prc-c-data.js`。只初始化一次。Work 仍读 B2 caseData；当前 Trace/历史返回和可读摘要有已知缺口，详见 [当前状态](docs/current-state.md)。

## Checks

```bash
python3 -m unittest discover -s tests -v
node tests/test_c_data.cjs
python3 -m compileall -q apps packages tests
git diff --check
```

默认测试仅使用合成/公开结构。固定私人样本诊断须显式设置 `PRC_LOCAL_DIAGNOSTICS=1` 且有相应数据访问许可；文件存在不等于样本 hash 和规则通过。`/acceptance.html` 只做历史案例诊断，其 PASS 不是产品认可，也不代表当前代码获得 DSH/global review。

## Boundaries

不上传原始 Session、凭证、隐藏推理或私人截图。常见凭证替换不是完整隐私保证。所有派发/步骤/顺序关系与摘要必须有来源；通知、助手自述与已验证结果分开。隐藏推理不作为说明来源。

不迁移 Rust，不构建自动干预平台，不宣称完整自动跨 Session 重建。新实施前需要方案和独立、有界的 global review。项目 Issue 入口：https://github.com/kaiykk/project-runtime-console/issues/2
