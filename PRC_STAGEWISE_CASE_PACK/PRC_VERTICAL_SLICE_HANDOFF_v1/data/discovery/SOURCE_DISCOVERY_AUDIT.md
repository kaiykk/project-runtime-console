# AISailing Source Discovery Audit

Round: 0  
Date: 2026-10-08  
Scope: source discovery only; no Project Evolution Map or evolution summary produced  
Audit output: `/opt/aisailing-source-discovery-round0/`

## Isolation and Method

This audit used a separate output directory and a path/filename exclusion list for the three named blind-test reference files:

- `AISAILING_EVOLUTION_OVERVIEW.md`
- `AISAILING_EVOLUTION_GRAPH.json`
- `AISAILING_EVIDENCE_LEDGER.md`

The excluded directory was not opened, copied, parsed, or used as evidence. No PRC B2 prototype data or reference answer was read. The audit only inspected source names, Git metadata, non-secret documentation, bounded evidence metadata, and the Codex Session index/listing surfaces.

No AISailing business repository, branch, worktree, configuration, or existing document was modified. Credential-bearing `.env` files were identified where relevant but not opened or exported.

## 1. Found Sources and Versions

The local environment contains several source families rather than one directory with the exact name `AISailing`:

1. `/opt/github_repo/ai` is a Git repository whose configured remote is the Codeup repository `aisailings/ai.git`. It has local and remote refs covering the legacy recommendation/data work and the newer recruitment-agent work. The earliest visible local commit is dated July 22, 2026; the recent visible history reaches October 8, 2026.
2. `/opt/github_repo/worktrees/` contains 12 related worktrees for recruitment-demo, semantic projection, P0 responsiveness, pipeline, and pi-ai reconciliation branches. Most are clean; one semantic-loop worktree and some older chatbot worktrees are dirty. Their status was observed without cleanup.
3. `/opt/chatbot/recruitment_demo_v01` is a separate Git repository with a short but explicit September 21-26 history. It contains I1/I2 lanes, rapid-runtime and stabilization branches, E2E evidence, tests, and worktrees. Its project brief calls the product a Recruitment Agent Harness, so its mapping to the AISailing product is probable but not proven by the repository name alone.
4. `/opt/chatbot/pi-ai` is a non-Git project snapshot with a `BRIEF.md`, architecture and handoff documents, OpenSpec material, tests, evidence, and runtime traces. It is highly relevant to the recruitment-agent work, but its lack of local `.git` metadata prevents direct commit-level reconstruction.
5. `/opt/zhy_web/job_rec` contains readable C-end job-recommendation handoffs, trace SQL, data-quality SQL, and readable SQL views. These are analysis and handoff artifacts, not a complete upstream repository.
6. `/opt/zhy_web/recommended-crew-codex-handoff-20260803` contains an extracted recommended-crew source snapshot, frontend/backend files, handoff documents, screenshots, a package index, and `SHA256SUMS`. The matching ZIP under `/opt/zhy_web` is an archive duplicate, not a second development history.
7. `/opt/zhy_shipowner_vessel/zhy_uat` and `/opt/zhy_shipowner_vessel/zhy_prod` contain bridge SQL, validation SQL, runner scripts, production/UAT logs, and explicitly versioned directories such as `rec_pool_v1_20260801` and `rec_pool_v2_20260909`. These are operational snapshots with useful dates and artifacts, but their files alone do not prove database state or production outcomes.
8. `/opt/ai_uat_rec_v1_0604_handover_20260804` is an older recommendation-pipeline handover with full/incremental SQL, production scripts, harness material, and a handover document. It is historical and partly superseded by later pipeline directories.
9. `/opt/aisailings-evidence/human-uat-round2` contains a frozen candidate identity, phase manifests, UAT receipt, per-turn JSON evidence, smoke results, screenshots, and a preserved browser assertion failure. The receipt records `FROZEN_BEFORE_HUMAN_UAT`; it explicitly says Human UAT was not executed and the Human Experience Gate was not passed.
10. `/opt/aisailings-shared/CODEX_DSH_SERVER_BOOTSTRAP_PROTOCOL_V1.md` is a readable protocol document for the Codex/DSH execution environment. It is a control/procedure source, not proof that every historical Session followed it.

The most complete local Git source is `/opt/github_repo/ai`. The most useful older product-context sources are the August 3 extracted handoff package and the August 4 recommendation handover. The most recent evidence sources are the September 26-October 8 Git/worktree records and the October 8 UAT evidence freeze.

## 2. Session Readability: Full Content or Index/Summary?

The answer is mixed:

- The local Codex Session index `/root/.codex/session_index.jsonl` is readable as an index. It contained 181 rows at audit time, including repeated IDs under renamed titles. It provides IDs, titles, and timestamps, not complete turns.
- The Codex app thread listing exposed recent thread IDs, project IDs, host, cwd, status, title, and concise summaries. It confirmed AISailing-related threads such as data/recommendation investigations, C-end recommendation work, recruitment-agent work, DSH work, and the current source audit.
- The complete body of the relevant AISailing Sessions was not established from the listing alone. In particular, many important Sessions point to `/Users/kai/Documents/AiSailing` or other local paths that are not mounted in the current remote workspace.
- `/root/.codex/archived_sessions` exposes at least one archived rollout file, but there is not yet a complete archive-to-project inventory proving that all AISailing Sessions are present there.
- `/opt/chatbot/pi-ai/logs/runtime_trace` is genuinely readable as JSONL trace content. There are 799 trace files from September 15-22, with structural fields such as `trace_id`, `stage_name`, `component`, `code_revision`, timing, status, input/output references, and payload references. Only structure and counts were sampled; raw payloads were not broadly extracted.

Therefore, Session content is mostly available as index/summary and runtime-structural evidence, not as a complete, trustworthy transcript corpus.

## 3. Reliability of Human Decision Records

There are useful decision-like records, but no single reliable complete human decision ledger was found.

Readable records include:

- repository `BRIEF.md`, handoff documents, OpenSpec artifacts, decision logs, and principal-review documents in the recruitment-agent snapshot;
- Git commit messages and branch names;
- UAT freeze identity, candidate hashes, startup checks, and explicit readiness/known-boundary statements;
- handoff documents that distinguish confirmed code facts from items requiring runtime or database validation;
- local reports and receipts that record test outcomes, closeouts, or preserved failures.

These records are strong for what a file or test explicitly records. They are not sufficient to infer why a decision was made, who approved it, whether an informal discussion changed it, or whether a commit was accepted through a PR. The Codeup remote is configured, but no local PR/MR body, review comments, approval, or requested-change record was found. A commit was not treated as a decision rationale.

## 4. Important History Likely Trapped in Inaccessible Sessions

The following history may exist only in unavailable or incomplete Session sources:

- the original product goal and early prioritization behind the AISailing recommendation and recruitment-agent work;
- the transition between the older recommendation/data pipeline and the newer recruitment-agent/runtime work;
- why particular branches, candidates, fallback policies, or authority boundaries were selected;
- informal human review, rejection, approval, and handoff conversations;
- external chat or voice discussion that was pasted into Sessions but is not present as a standalone local record;
- complete evidence-to-decision links for the September 15-October 8 DSH and agent-runtime work;
- PR-level discussion and review comments for Codeup branches;
- the full local workstation repository at `/Users/kai/Documents/AiSailing`, including any branches or worktrees not mirrored under `/opt`.

The current evidence can locate many of these gaps, but it cannot fill them without the original Session exports, local workstation mount, or Codeup review access.

## 5. Is the Material Sufficient for a Limited Reconstruction?

`LIMITED_SCOPE_ONLY`

Reason:

- There is enough local material to begin a bounded reconstruction of observable implementation and evidence lineage for selected slices, especially:
  - the August 3-4 recommendation/web handoff snapshot;
  - the August 13 onward UAT/production bridge and recommendation-pool artifacts;
  - the September 21-October 8 recruitment-agent Git branches, worktrees, runtime traces, test evidence, and UAT freeze.
- There is not enough source access for a complete project-wide reconstruction with reliable decision causality. The exact project boundary is also split between the AISailing recommendation/data line and the Recruitment Agent line, with names that are related but not identical.
- The human UAT receipt is a freeze/readiness record, not evidence that Human UAT or the Human Experience Gate actually completed.
- PR/review records, complete Session bodies, unmounted local project files, and full human decision records are missing or only summarized.

This status means a finite, explicitly bounded reconstruction could start after human review of the manifest. It does not authorize or claim a full evolution map.

## Minimum Additional Inputs Needed

To move beyond limited scope, the smallest useful supplement is:

1. A read-only export or mount of `/Users/kai/Documents/AiSailing`, including its Git refs, worktrees, and project-local documents.
2. Complete exports for the AISailing-related Codex/DSH Sessions from August 12-October 8, including tool outputs and attachment references, with secrets redacted.
3. Codeup PR/MR exports for the relevant branches, including review comments, approvals, requested changes, and linked issue/decision references.
4. The original human decision records or meeting/chat excerpts that explain the major product and runtime decisions, rather than only the resulting commits or handoffs.
5. A human-confirmed mapping of which sources belong to the same AISailing product boundary: recommendation/data pipeline, web snapshot, Recruitment Agent, pi-ai, and DSH evaluation assets.

## Final Status

`LIMITED_SCOPE_ONLY`

The local source surface is substantial and auditable for selected slices, but source gaps prevent a complete, project-wide, decision-causal reconstruction.
