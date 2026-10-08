# PRC V1 Integration Vertical Slice 执行回执

## 范围

本回次只接入一个本地 Codex rollout JSONL，保留 Work B2、Agents C v0.2、Trace C v0.2 的主要交互意图，未接入远程 Codex，也未改写原始 Session。

## 真实来源

- Session ID：`019f12a7-b9b1-72d3-92a4-6894c5d34a86`
- 来源：`vscode`
- 工作目录：`/Users/kai/Documents/AiSailing`
- 原始路径：`/Users/kai/.codex/sessions/2026/06/29/rollout-2026-06-29T17-13-29-019f12a7-b9b1-72d3-92a4-6894c5d34a86.jsonl`
- 实际规模：68 Turns、4851 行、4297 条 Human-facing native records、812 次 tool call、814 次 tool result
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

Work 中的 AISailing evolution map 是 `CURATED_CASE / REFERENCE_CASE`，不声称由当前 Session 自动恢复。真实 Session 只在 Work 的 `REAL_SESSION` 活动入口出现，并可进入同一 Session 的 Trace/Agents。

## 浏览器证据

- `output/playwright/work-1600.png`
- `output/playwright/work-1366.png`
- `output/playwright/agents-1600.png`
- `output/playwright/trace-1600.png`
- `output/playwright/trace-raw-1600.png`

已实际验证：

1. Work 显示 curated AISailing map、宽 Inspector 和真实 Session 入口。
2. Work 的真实 Session 入口进入 Trace，并定位到真实 tool call 的 Turn/event。
3. Agents 显示当前 Session 的 native identity 与 lineage 缺口，不造子 Agent。
4. Trace 按 Turn 展开真实 records；打开 raw modal 可看到脱敏 native envelope、原始路径、JSONL 行号和 byte offset。
5. URL 保存 `tab`、`turn`、`event`、`session_id`，浏览器前进/后退可以恢复同一选择状态。
6. 1366 与 1600 宽度均完成截图；无远程 provider 请求。

## 结论

当前 slice 对“真实 Session -> 三个共享 surface -> 证据定位”的目标为 `PARTIAL`：Trace 和跨 surface 证据链已是真实可用；Agents 的原生子 Agent lineage 受源文件能力限制保持 UNKNOWN；Work 仍是 curated reference + authentic activity，不是自动 Project Evolution reconstruction。
