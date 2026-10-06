# PRC UI Convergence — Frame Auditor Pass A

```yaml
round_id: PRC-UI-CONVERGENCE-R1-20261006
review_id: prc-ui-convergence-frame-pass-a-20261006
review_mode: REFERENCE_PRECOMMIT
model_shaping: YES
human_facing_artifact: YES
builder_context: EXCLUDED
manager_rationale: EXCLUDED
```

## Auditor Boundary

You are the independent Frame / Experience Auditor for Pass A. Read only the
Human references listed below. Do not inspect source code, existing UI
screenshots, existing experiment packets, implementation plans, variant
ideas, commit messages, tests, or Manager explanations. Do not modify files.

Do not choose a product frame. Do not ratify the ThoughtDAG-inspired
direction. Freeze a reference-derived precommit that a later Frame Comparison
can use to challenge proposed frames.

## Allowlisted Human References

- `/Users/kai/Documents/project-runtime-console/docs/NORTH_STAR.md`
- `/Users/kai/Documents/project-runtime-console/docs/SHELL_FREEZE_V0.md`
- `/Users/kai/Documents/project-runtime-console/docs/governance/GLOBAL_GOVERNANCE_BOOTSTRAP.md`
- `/Users/kai/Documents/project-runtime-console/docs/governance/THREE_ROLE_BOOTSTRAP.md`
- `/Users/kai/Documents/project-runtime-console/docs/capability-imports/AGENT_MONITOR.md`
- `/Users/kai/Documents/project-runtime-console/docs/capability-imports/THOUGHTDAG.md`
- `/Users/kai/.codex/attachments/7f30e918-c149-4bb7-ba5d-b4ef6e2eac94/已粘贴的文本.txt`

## Required Output

Return a concise `REFERENCE_FIRST_PRECOMMIT` containing only:

1. `HUMAN_PROBLEM` — what the Human needs to understand or accomplish;
2. `EXPERIENCE_INVARIANTS` — what must remain true in a Human-facing artifact;
3. `HUMAN_CONFIRMED_DECISIONS` — only decisions explicitly present in the
   allowlisted references;
4. `SUPPORTED_CONCEPTS` — concepts the references support considering, without
   treating them as approved architecture;
5. `UNAUTHORIZED_OR_FORBIDDEN_CONCEPTS` — concepts the references exclude;
6. `LIKELY_FRAMING_FAILURES` — ways a proposed frame could drift from Human
   intent or runtime truth;
7. `QUESTIONS_EVERY_FRAME_MUST_ANSWER` — falsifiable questions for Pass B;
8. `AUTHORITY_CONFLICTS` — unresolved conflicts between allowlisted Human
   references, especially the Shell Freeze / ThoughtDAG boundary.

Use evidence-bounded language. Keep the result independent of any proposed
implementation. The output is advisory and is not a product approval.
