# PRC V1 Integration Vertical Slice 执行回执

## 范围

本回次只接入一个本地 Codex rollout JSONL，保留 Work B2、Agents C v0.2、Trace C v0.2 的主要交互意图，未接入远程 Codex，也未改写原始 Session。

## 真实来源

- 默认 Session ID：`019faced-f11a-75e1-ac20-8b95e24d4628`
- 来源：`vscode`
- 工作目录：`/Users/kai/Documents/ZHY_Project_from_Scratch`
- 原始路径：`/Users/kai/.codex/sessions/2026/07/29/rollout-2026-07-29T16-11-42-019faced-f11a-75e1-ac20-8b95e24d4628.jsonl`
- 实际规模：5 Turns、380 行、313 条 Human-facing native records、35 次 tool call、35 次 tool result
- Agents 边界：该文件内没有观察到可确认的 native child-agent identity 或 dispatch lineage，因此页面显示 `NO_NATIVE_LINEAGE` / `UNKNOWN`。

页面只读读取上述路径，展示层排除 reasoning records，并对常见凭证模式做显示脱敏；原文件不会被修改或复制进仓库。

## 数据流

```text
本地 Codex rollout JSONL
  -> packages/session_sources/codex_jsonl.py
  -> apps/console/server.py (/api/session, /api/case)
  -> 一个产品 shell 的 Work / Agents / Trace
  -> event_id -> session_id + line + byte_offset + native item id
```

Work 中的 AISailing evolution map 是 `CURATED_CASE / REFERENCE_CASE`，不声称由当前 Session 自动恢复。DSH 复核确认当前提交没有可用的 `REAL_SESSION` Work 活动入口，因此也没有可验证的 Work -> native Trace 下钻；这一项仍待修复。

## 浏览器证据

- `output/playwright/final-work-1600.png`
- `output/playwright/final-work-1366.png`
- `output/playwright/final-agents-1600.png`
- `output/playwright/final-agents-1366.png`
- `output/playwright/final-trace-1600.png`
- `output/playwright/final-trace-1366.png`
- `output/playwright/final-trace-raw-1600.png`

已实际验证：

1. Work 使用冻结 B2 的原始空间地图、节点关系、宽 Inspector 和证据索引。
2. Trace 的真实记录可进入同一 shell；Work 的真实 Session 入口和 Work -> Trace 定位尚未通过 DSH 复核。
3. Agents 显示当前 Session 的 native identity 与 lineage 缺口，不造子 Agent。
4. Trace 按 Turn 展开真实 records；打开 raw modal 可看到脱敏 native envelope、原始路径、JSONL 行号和 byte offset。
5. URL 会保存部分选择状态，但 DSH 复核发现 `popstate` 未同步渲染状态，浏览器前进/后退恢复仍未通过。
6. 1366 与 1600 宽度均完成截图；无远程 provider 请求；浏览器 console 无 error/warning。

## 结论

当前 slice 对“冻结 Mock 结构 + 真实 Session -> 三个共享 surface -> 证据定位”的目标为 `PARTIAL`：Agents 的原生子 Agent lineage 受源文件能力限制保持 UNKNOWN；Trace/Raw Record 链路真实且可回溯；但 Work 的 B2 关系/证据交互、真实 Session 活动入口与跨 Tab 历史恢复仍不满足契约。工程与浏览器验证通过不等于产品验收 PASS。DSH formal verdict 为 `PARTIAL / RETURN_TO_REPAIR`。
