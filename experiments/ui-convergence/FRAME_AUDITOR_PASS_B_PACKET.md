# PRC UI Convergence — Frame Auditor Pass B

```yaml
round_id: PRC-UI-CONVERGENCE-R1-20261006
review_id: prc-ui-convergence-frame-pass-b-20261006
review_mode: FRAME_COMPARISON
model_shaping: YES
human_facing_artifact: YES
```

## Auditor Boundary

Read only the frozen Reference Precommit, the Frame Proposal, and the same
Human references used in Pass A. Do not inspect source code, screenshots,
browser recordings, implementation rationale, tests, commit messages, or
unlisted evidence. Do not modify files. Do not design variants or approve
implementation.

## Allowlisted Evidence

- `experiments/ui-convergence/REFERENCE_FIRST_PRECOMMIT.md`
- `experiments/ui-convergence/FRAME_PROPOSAL.md`
- `docs/NORTH_STAR.md`
- `docs/SHELL_FREEZE_V0.md`
- `docs/ui-frame-change-v1.md`
- `docs/governance/GLOBAL_GOVERNANCE_BOOTSTRAP.md`
- `docs/governance/THREE_ROLE_BOOTSTRAP.md`
- `docs/capability-imports/AGENT_MONITOR.md`
- `docs/capability-imports/THOUGHTDAG.md`
- `/Users/kai/.codex/attachments/7f30e918-c149-4bb7-ba5d-b4ef6e2eac94/已粘贴的文本.txt`

## Required Output

Return exactly:

```text
FRAME_DECISION: FRAME_OK | FRAME_REOPEN | PRINCIPAL_REVIEW
BLOCKING_FRAME_QUESTION: <one question or NONE>
EVIDENCE_GAP: YES | NO
REVIEW_SCOPE:
  reviewed: <paths>
  not_reviewed: <paths>
  cannot_conclude: <paths or NONE>
RATIONALE: <short evidence-bounded rationale>
ADVISORY_ONLY: YES
```

`FRAME_OK` means only that the bounded proposal is supported enough to enter
the next execution step. It does not approve the UI, prove utility, or ratify
the product model.
