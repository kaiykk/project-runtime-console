# PRC — Codex One-shot Vertical Slice (Integration-First)

## North Star
Produce a running, local-first PRC which ingests at least one **actual on-disk Codex Session** (not a fixture) and displays Work / Agents / Trace in **one product shell** matching the approved mocks. Prefer adapting mature OSS/Skills over building own Session parser, memory engine, tracing platform or agent runtime. Complete one self-managed design→implement→test→fix loop and hand back verifiable artifacts.

## Binding product decisions
- Work = cross-session **Project Evolution Map**; UX reference `mock/work/PRC_AISAILING_WORK_B2.html` (most recent). Spatial zones, readable decision stories, narrow drill-down, 480px-ish inspector, back/history, upstream/downstream highlighting, provenance.
- Agents = native provider Agent identities, delegation and work/result structure; UX reference exact `mock/agents_trace/prc_agents_surface_C_v02_interactive.html`. Never promote raw tool events to Agents. Partial data must look partial.
- Trace = native provider turns/events, user/agent/tool distinction, readable by turn with exact source access; same C v0.2 reference. Never replace with a fabricated replay.
- Work B2 replaces the old Work iframe in C v0.2. Product freeze is interaction/semantics, **not** existing runtime implementation.

## Prerequisite / clean context
1. Locate both exact HTML references and inspect them in a browser. If C v0.2 is missing, ask for the original file and STOP implementation; do not invent a substitute.
2. Start a fresh branch/worktree and fresh implementation session in the existing PRC codebase or an isolated new `prc-vslice` module. Record where. Do not destroy/overwrite prior work or ignore actual runtime/file safety rules. Historical documentation is read-only background; this file supersedes conflicting older product design decisions.
3. Inventory local Codex session **readability** (e.g. ~/.codex/sessions, archived_sessions, rollout JSONL). Use one redacted actual local session for acceptance; the source remains read-only. Do not assume remote Codex App session bodies are available.

## Agent loop and bounded OSS selection
Use Matt Pocock's Sandcastle `@ai-hero/sandcastle` if container tools and credentials are available, with an isolated branch/worktree, limited iterations, and run/test/repair gates. It is an **agent sandbox orchestrator**, not a library quality oracle. Do not install Sandcastle into the PRC application as a product dependency merely to evaluate a candidate. If Sandcastle is unavailable or disproportionate, use an isolated worktree/container and the same fast checks.

Screen ONLY local-session parsers likely to offer the required records: 
- `https://github.com/Ax-For/session-observer`
- `https://github.com/QJ-Chen/agentlen`
- `https://github.com/RobertTLange/agentlens`
Compare README/API quickly (no full repo audit). Test a tiny adapter/fixture inside sandbox for 1–2 top choices; favor stable local Session → Turn/Event/Agent and raw source pointer, streaming additions if easy. Choose one or implement minimal compatibility adapter if necessary. Reuse selectively; never transplant an entire competing front end or add huge dependencies to PRC. Memory/Skill options (`claude-mem`, `keep-the-why`, `langmem`) are OPTIONAL only if low-friction and clearly support the first slice. No Graphiti deployment, no daily scheduler yet.

## Minimal implementation slice
1. Local source selector: choose one allowed local Codex sessions directory / project, index one or more real sessions, show source/coverage/read errors transparently. Never read or upload secrets; no remote source.
2. Backend source adapter: preserve provider-native `session_id`, run/turn/event/agent/thread references where present; stable provenance `{source_type,file_path,offset_or_event_id,span}`; incremental read optional. Missing fields remain unknown, not synthesized as facts.
3. Unified project/run selection and deep-link state across Work / Agents / Trace; browser back and return-to-position work.
4. Trace C: select an actual local session; render real grouped turns/tools with expandable original records, not screenshot-only or mocked data.
5. Agents C: render real native agent identity and delegation only where source supports it; single-agent/unknown structure is acceptable with explicit note. Don't render 27 fake agents for an unrelated session.
6. Work B2: preserve approved mock as a visible **curated reference case** (label `CURATED_CASE`, never call it live). For the real local session, add a minimal evidence-backed project activity/episode projection associated with its source, not a falsely complete Evolution Graph. Even one authentic session-linked event is acceptable. If no important decision can be reliably established, show `No confirmed decision yet` and allow trace drill-down.
7. All three tabs within a single real app shell, not iframe placeholders. Shared selection and navigation should carry stable IDs and correct source evidence. Prior C v0.2's old Work fixture must not reappear.
8. Store only minimal local index/cache as needed. No task scheduling, auto-evolving memory or graph database in V0.

## Non-negotiable acceptance
Use `02_ACCEPTANCE.md`. Browser automation with screenshot comparison for each tab and interaction, API integration tests on sample local redacted Session, and recorded positive/negative paths. If an acceptance point fails, repair in-loop before final report. Do not claim PASS on a static mock.

## Handoff
Deliver running local URL/launch command; branch/commit and changed files; selected OSS with reasons; actual source ID / file pointer used, and explicit redaction; screenshots for Work/Agents/Trace and evidence drill-down; test commands/results, blocking gaps, known limitations. Prefer working increment over report volume.

## Stop rules
Only stop without implementation for genuine missing required mock C, missing local Session access, or unsafe write/security conflict. Do not pretend a missing source is implemented; don't ask for arbitrary additional sign-offs at intermediate non-blocking steps. Complete the vertical slice if prerequisites are met.
