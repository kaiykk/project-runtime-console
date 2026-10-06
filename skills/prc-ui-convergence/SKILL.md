---
name: prc-ui-convergence
description: Bounded browser-in-the-loop convergence for Project Runtime Console UI variants.
---

# PRC UI Convergence

This skill is a research harness for one Human-facing UI convergence round. It
does not implement a runtime observer, a product Judge, a Control Plane, or a
new Project Runtime Console model.

## Required Order

1. Read `docs/ui-frame-change-v1.md`, `experiments/ui-convergence/REFERENCE_FIRST_PRECOMMIT.md`, and the current execution packet.
2. Capture reference behavior and the frozen C0 baseline before changing PRC presentation code.
3. Build exactly three structurally distinct variants from one runtime/backend baseline.
4. Exercise every variant with the same real small and large multi-Agent Runs.
5. Separate screen-only Visual Review, browser-only UX Review, and Runtime Truth Review.
6. Compare evidence without Builder advocacy.
7. Refine the winner at most twice; rollback on material regression.
8. Stop at `PRINCIPAL_REVIEW`; never merge or promote automatically.

## Method Sources

This skill adapts methodology, not source code or product ontology:

| Method | Use in this skill | License / provenance |
|---|---|---|
| Anthropic frontend-design skill | design brief, deliberate visual direction, screenshot critique | methodology reference; no files vendored |
| OpenAI curated Playwright skill | real browser interaction, snapshots, screenshots, traces | local skill at `~/.codex/skills/playwright/SKILL.md`; no files copied |
| Vercel agent-browser dogfood methodology | user-perspective task validation and repro-first evidence | methodology reference; no files vendored |
| `chenxiachan/thoughtdag` | bounded canvas interaction reference; MIT implementation only if provenance is recorded | MIT, commit recorded per reused component |
| `donvito/agent-monitor` | clean-room runtime interaction reference only | license not exposed in local study; no code/assets reuse |

## Evidence Rules

- Real runtime data only. Never add synthetic nodes or edges for visual effect.
- Runtime lineage is read-only observed fact.
- `SHOW_JUDGMENTS=false`, `read_only=true`, and `runtime_effect=NONE` remain
  the default during this round.
- A screenshot is evidence of appearance, not evidence of runtime correctness.
- `FRAME_OK`, `PASS`, and a comparator result are advisory checkpoints, not
  Human ratification or product utility proof.
- Human-facing HTML and reports are Chinese.

## Variant Diversity Gate

Each variant plan must differ materially across at least four of:

- graph layout;
- Agent/trajectory relationship;
- selected-node disclosure;
- event-detail disclosure;
- semantic zoom;
- run navigation;
- trace representation.

Color, typography, spacing, and border changes alone fail the gate as
`VARIANT_SET_REJECTED`.

## Review Firewalls

- Visual Reviewer: product brief + reference captures + variant captures only.
- UX Reviewer: running browser only; no source or Builder rationale.
- Runtime Truth Reviewer: runtime evidence + rendered evidence; no aesthetic
  advocacy.
- Comparator: all review evidence; no Builder advocacy.

## Reusable Scripts

The scripts in `scripts/` are intentionally small wrappers around the real
browser and process commands. They write only under the round's
`experiments/ui-convergence/` corpus and never mutate runtime state.
