# Project Runtime Console

PRC V1 是一个本地只读产品闭环：从本机 Codex rollout JSONL 读取真实运行记录，在一个共享 shell 中提供 Work、Agents、Trace 三个入口，并让每条可读证据回到原始 Session 的路径、行号和 byte offset。

## North Star

让 Human 能从项目参考地图进入真实 Agent 执行记录，理解发生过什么，并在证据不足时看到明确的 `UNKNOWN / UNAVAILABLE`，而不是被推断的工作意义、结果或 lineage 误导。

## Experience Star

```text
Work reference / real activity
        -> Agent identity boundary
        -> Turn / tool records
        -> sanitized native envelope
        -> source path + line + byte offset
        -> return through browser history
```

## V1 Scope

- 本地 Codex Session only；不读取远程 Codex App，不上传 Session。
- Work 使用 AISailing B2 作为明确标注的 `CURATED_CASE / REFERENCE_CASE`，同时展示当前真实 Session 的独立活动入口。
- Agents 只展示本地源能证明的 native identity 和 lineage；没有 child identity 时保持 `NO_NATIVE_LINEAGE / UNKNOWN`。
- Trace 按 Turn 展示真实 JSONL records；reasoning 不进入 Human-facing records；raw modal 展示常见凭证脱敏后的 native envelope。
- 三个 Surface 共用 `session_id`、`turn_id`、`event_id` 和 URL history，不使用 iframe 或静态截图拼接。

## Run

```bash
python3 apps/console/server.py 4173
```

打开 <http://127.0.0.1:4173>。默认目标 Session 为：

```text
019faced-f11a-75e1-ac20-8b95e24d4628
```

本地 adapter 会从 `~/.codex/sessions` 和 `~/.codex/archived_sessions` 读取 JSONL，原始文件保持只读。页面中的 Session 列表可以切换本地 AISailing Session，URL 会保留 `session_id`。

默认 Session 是 AISailing 招聘相关对话：5 个 Turn、313 条 native records；它没有可确认的原生 child-Agent lineage，因此 Agents 页面明确显示 `UNKNOWN / UNAVAILABLE`，不会从工具调用推断 Agent。

## Verification

```bash
python3 -m unittest discover -s tests -v
```

浏览器截图和本轮执行回执位于 `output/playwright/` 与 `docs/PRC_V1_VERTICAL_SLICE_RECEIPT.md`。`output/` 默认被 Git 忽略，截图保留在本机作为验收 artifact。

## Explicit boundaries

本轮没有实现自动 Project Evolution reconstruction、WorkStage classifier、远程 provider、完整 multi-agent lineage 恢复或 Diagnostic White-box。Work 的 curated case 不是当前 Session 的自动结论；运行记录的数量不能证明贡献、因果、完成或 outcome。
