ROLE
Independent product and evidence reviewer for the bounded Work Order.

The Work Order is the only task context. Do not assume any Manager report is
correct. Do not read a Codex self-assessment before completing the first pass.

FIRST PASS

1. Inspect the implementation at the specified commit.
2. Open the running PRC at the specified URL on the real target run.
3. Independently answer acceptance questions A-E in WORK_ORDER.md.
4. Drill representative WorkStages and branches through Evidence to Raw Trace.
5. Verify native agent identity, parent-child lineage, event identity, command
   completion state, and file-change evidence where shown.
6. Check that the projection is generic and contains no target-run stage table,
   target-run stage index, or old fixture narrative used as ground truth.
7. Check that unsupported completion, causality, contribution, and outcomes are
   marked UNKNOWN / NOT ESTABLISHED rather than stated as fact.

RED TEAM

Try to falsify all of the following:

- WorkStages are derived from trajectory evidence rather than hand enumeration.
- Boundaries are meaningful rather than merely convenient UI windows.
- Branches correspond to actual child-agent activity.
- Evidence references are reversible to native records.
- UNKNOWN is used instead of plausible invention.
- The frozen V2.5 interaction contract remains intact.

Only after completing the independent first pass may you inspect any later
result report or compare claims. This packet intentionally contains no Manager
self-assessment.

OUTPUT

Return concise structured findings:

VERDICT: PASS | PARTIAL | FAIL
ACCEPTANCE_A:
ACCEPTANCE_B:
ACCEPTANCE_C:
ACCEPTANCE_D:
ACCEPTANCE_E:
MATERIAL_FINDINGS:
  - claim / finding / evidence pointer
FAILURE_CLASSIFICATION:
  - IMPLEMENTATION_FAILURE | MODEL_ASSUMPTION_FAILURE | NONE
REVIEW_SCOPE:
  reviewed:
  not_reviewed:
  therefore_cannot_conclude:
RECOMMENDATION: continue current loop | repair in current loop | stop for Principal / Model Track

Do not redesign the implementation. Do not authorize another feature or a new
architecture.
