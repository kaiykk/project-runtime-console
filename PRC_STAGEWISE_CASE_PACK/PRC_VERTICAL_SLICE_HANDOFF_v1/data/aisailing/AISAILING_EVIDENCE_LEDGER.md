# AISailings Agent Project Evolution Case V0 Evidence Ledger

This ledger is the review surface for
`AISAILING_EVOLUTION_OVERVIEW.md` and
`AISAILING_EVOLUTION_GRAPH.json`.

Evidence IDs are stable within this V0 packet. A source receipt or report is
the authority for the underlying fact; this ledger is only a compact pointer
and interpretation boundary.

## Reading rules

- `OBSERVED` means the cited artifact directly contains the fact or result.
- `HUMAN_RATIFIED` means the cited control-plane document records an explicit
  product decision or acceptance.
- `INFERRED` means the packet combines multiple observations; it is not a new
  decision.
- `UNKNOWN` means the available evidence is insufficient.

The cited paths are absolute paths in the inspected worktree unless stated
otherwise. Secrets, authorization headers, provider keys, and private user
data are intentionally omitted.

## Evidence index

### E-001: Initial product goal and workflow framing

- Status: `HUMAN_RATIFIED`
- Source type: Document
- Source:
  `/opt/github_repo/worktrees/recruitment-demo-v01-semantic-turn-projection-v01/prototypes/chatbot/pi-ai/docs/01_Product_Constitution.md`
  and `docs/00_Project_Knowledge_Map.md`
- Relevant content: the product is a maritime AI work entry; recruitment is the
  first deep workflow; chat is the interaction surface; user language comes
  before internal object names.
- Supports: the original project goal and initial product framing.
- Does not support: a complete original PRD, production scope, or current
  implementation readiness.
- Human confirmation still needed: whether these documents capture every
  original product motivation.

### E-002: Natural language and real-path product boundary

- Status: `HUMAN_RATIFIED`
- Source type: Document
- Source:
  `/opt/github_repo/worktrees/recruitment-demo-v01-semantic-turn-projection-v01/prototypes/chatbot/recruitment-demo-v01/docs/control_plane/AISAILINGS_V01_PRODUCT_NORTH_STAR.md`
- Relevant content: users describe needs in natural language, receive useful
  results or clarification, and the real Backend-to-Frontend path is the
  acceptance surface; continuity is a product invariant.
- Supports: the current North Star and Experience Star boundary.
- Does not support: a claim that the current runtime already satisfies it
  globally.
- Human confirmation still needed: the final release-level acceptance bar.

### E-003: Existing business and retrieval assets should be reused safely

- Status: `OBSERVED` / `HUMAN_RATIFIED`
- Source type: Document
- Source:
  `/opt/github_repo/worktrees/recruitment-demo-v01-semantic-turn-projection-v01/prototypes/chatbot/pi-ai/docs/02_System_Architecture_Map.md`
  and `docs/06_Decision_Log.md`
- Relevant content: intended layering puts provider, workflow, validation,
  controlled tools, Backend, and Frontend in separate responsibilities; the
  existing recommendation API remains outside the provider layer.
- Supports: the initial architectural direction and reuse boundary.
- Does not support: a final shared Runtime or a complete tool architecture.
- Human confirmation still needed: whether historical S02/S04 slice decisions
  should remain current for future product work.

### E-004: Core Architecture Gate versus Human Experience Gate

- Status: `HUMAN_RATIFIED`
- Source type: Document
- Source:
  `/opt/github_repo/worktrees/recruitment-demo-v01-semantic-turn-projection-v01/prototypes/chatbot/recruitment-demo-v01/docs/control_plane/README.md`
  and `ACTIVE_WORK_CARD.md`
- Relevant content: Frame, Responsibility, and Product Progress Guards are
  separate; machine gates do not imply Human Experience PASS.
- Supports: the control rule used in the current evolution case.
- Does not support: Human Experience PASS for any current candidate.
- Human confirmation still needed: none for the rule itself; future product
  acceptance remains human-owned.

### E-005: Current runtime baseline and evidence boundary

- Status: `OBSERVED`
- Source type: Document
- Source:
  `/opt/github_repo/worktrees/recruitment-demo-v01-semantic-turn-projection-v01/prototypes/chatbot/recruitment-demo-v01/docs/control_plane/CURRENT_RUNTIME_BASELINE.md`
- Relevant content: the current baseline records a two-call working path,
  evidence versus runtime assets, external Frontend/provider dependencies, and
  claims that remain not validated.
- Supports: the distinction between current implementation, evidence, and
  unknowns.
- Does not support: a global performance or production claim.
- Human confirmation still needed: whether the current baseline should be
  updated after future work.

### E-006: Early bounded slices and no automatic filter inference

- Status: `OBSERVED`
- Source type: Document
- Source:
  `/opt/github_repo/worktrees/recruitment-demo-v01-semantic-turn-projection-v01/prototypes/chatbot/recruitment-demo-v01/experiments/rapid_vertical_runtime_v01/PACKAGE_1_SLICE_2_SEMANTIC_AUTHORITY_CUTOVER_REPORT.md`
  and `PACKAGE_1_SLICE_3_VESSEL_SEMANTICS_AND_FALLBACK_REPORT.md`
- Relevant content: S1/S2 use a validated delta before retrieval; unsupported
  facts remain evidence; no silent predicate is created.
- Supports: the transition from provider output to controlled workflow state.
- Does not support: complete retirement of all legacy callers or global query
  support.
- Human confirmation still needed: final global query policy.

### E-007: Semantic Delta mutation authority

- Status: `OBSERVED`
- Source type: Document, test, and real trace pointers
- Source:
  `PACKAGE_1_SLICE_2_SEMANTIC_AUTHORITY_CUTOVER_REPORT.md`, especially the
  validated delta and legacy shadow sections; related tests under
  `experiments/rapid_vertical_runtime_v01/test_work_bridge.py` and
  `test_rvr03.py`.
- Relevant content: Clean business fields change only when the validated
  Semantic Delta is applied; legacy processing uses an independent shadow
  state and cannot write Clean state.
- Supports: the bounded mutation-authority transition.
- Does not support: physical deletion or retirement of every legacy path.
- Human confirmation still needed: none for the tested clean path; complete
  retirement remains open.

### E-008: Explicit migration and retirement limits

- Status: `OBSERVED`
- Source type: Document
- Source:
  `experiments/rapid_vertical_runtime_v01/ROUND_2_2_CLEAN_RUNTIME_CODE_RESPONSIBILITY_AUDIT.md`
- Relevant content: legacy action selection and direct writers are marked for
  migration/split/retirement after evidence; the report explicitly defers
  physical retirement and identifies loaded-but-unused assets.
- Supports: the claim that old responsibilities were narrowed/quarantined,
  not universally removed.
- Does not support: a clean Runtime with no compatibility code.
- Human confirmation still needed: future retirement decisions.

### E-009: Early product acceptance context

- Status: `OBSERVED` / `HUMAN_RATIFIED` within slice scope
- Source type: Document
- Source:
  `/opt/github_repo/worktrees/recruitment-demo-v01-semantic-turn-projection-v01/prototypes/chatbot/pi-ai/docs/00_Project_Knowledge_Map.md`
  and `docs/06_Decision_Log.md`
- Relevant content: S02 and S04 were accepted for bounded slices, while the
  project-level 100-request acceptance target and global policies remained
  open.
- Supports: the claim that the project grew by bounded slices rather than one
  complete architecture.
- Does not support: complete product acceptance.
- Human confirmation still needed: whether the historical slice acceptance is
  still a current baseline.

### E-010: Vessel semantic state and explicit fallback rule

- Status: `OBSERVED` / `HUMAN_RATIFIED` for bounded behavior
- Source type: Document and test
- Source:
  `PACKAGE_1_SLICE_3_VESSEL_SEMANTICS_AND_FALLBACK_REPORT.md`
- Relevant content: `KNOWN`, `ANY`, `MISSING`, and `UNKNOWN` are distinct;
  unknown plus explicit fallback can permit position-only retrieval; unknown
  alone cannot.
- Supports: the vessel authority/fallback workstream and rejection of silent
  fallback.
- Does not support: a complete vessel ontology or policy for every phrase.
- Human confirmation still needed: compound phrase and alternative-set policy.

### E-011: Multi-context ownership for fallback and clarification

- Status: `OBSERVED`
- Source type: Document and bounded evidence
- Source:
  `PACKAGE_1_SLICE_3_VESSEL_SEMANTICS_AND_FALLBACK_REPORT.md`, especially the
  R13/F2 and retrieval eligibility sections.
- Relevant content: fallback authorization and pending vessel clarification
  are scoped to the owning Context; a sibling Context does not inherit them.
- Supports: the bounded multi-context safety claim.
- Does not support: full Work/Lead referent resolution in arbitrary language.
- Human confirmation still needed: broader cross-Work continuity policy.

### E-012: Historical semantic and vessel coverage gaps

- Status: `OBSERVED`
- Source type: Document
- Source:
  `AISAILINGS_LEGACY_EVIDENCE_HANDOFF.md` and
  `PACKAGE_1_SLICE_3_VESSEL_SEMANTICS_AND_FALLBACK_REPORT.md`
- Relevant content: missing, unknown, unrestricted, shorthand, and ambiguous
  expressions require different handling; unsupported facts cannot be silently
  executed.
- Supports: the reason the authority boundary became a major workstream.
- Does not support: the claim that all historical language is now covered.
- Human confirmation still needed: final domain authority coverage.

### E-013: Control plane activates responsiveness as bounded P0

- Status: `HUMAN_RATIFIED`
- Source type: Commit and document
- Source: commit `2a830173a34d3dbb17b1b771c3b39aeff4c12939` and
  `docs/control_plane/AISAILINGS_V01_PRODUCT_NORTH_STAR.md`.
- Relevant content: real interaction responsiveness becomes the active P0;
  natural-language continuity and Frontend truth mapping remain invariants.
- Supports: the existence and scope of the responsiveness workstream.
- Does not support: the claim that responsiveness replaced the original goal.
- Human confirmation still needed: final latency budgets for complex turns.

### E-014: Two-call path and provider telemetry

- Status: `OBSERVED`
- Source type: Commit and receipt
- Source: commits `6d76d026ffe1085f949439f02c6530d3e2862558`,
  `170475c`, and `50d24db`; report
  `experiments/rapid_vertical_runtime_v01/P0_001_REAL_INTERACTION_RESPONSIVENESS_REPORT.md`.
- Relevant content: two serial calls became the tested default; timing and
  provider reasoning telemetry were recorded; the path was not permanently
  frozen as architecture.
- Supports: the bounded responsiveness outcome.
- Does not support: a global 2-second SLA or universal model validity.
- Human confirmation still needed: production performance target.

### E-015: Frontend and browser path continuity

- Status: `OBSERVED`
- Source type: Commit, test, and experiment receipt
- Source: `PHASE2_2_MINIMUM_SEMANTIC_MECHANISM_RECEIPT.md`,
  `PHASE2_EXPERIMENT_RECEIPT.md`, and commits `34e3153`, `c5557ee`, and
  `9141073`.
- Relevant content: candidate HTTP output reached the existing Frontend route;
  candidate cards were visible in bounded smokes; scroll ownership and pending
  clarification focus were repaired in earlier paths.
- Supports: a real tested Backend-to-Frontend continuity path.
- Does not support: a full Human Experience PASS or complete Frontend behavior.
- Human confirmation still needed: browser acceptance across broader cases.

### E-016: Fresh multi-context clarification evidence

- Status: `OBSERVED`
- Source type: Report and tests
- Source: `experiments/rapid_vertical_runtime_v01/FRESH_MULTICONTEXT_CLARIFICATION_EVIDENCE_REPORT_20260926.md`
  and commit `2ab7812`.
- Relevant content: pending clarification focus and multi-context ownership
  were exercised through the demo adapter.
- Supports: the workstream's focus on context ownership and clarification.
- Does not support: general Lead Continuity.
- Human confirmation still needed: broader natural-language referent behavior.

### E-017: Phase 2.1 bundled Treatment signal

- Status: `OBSERVED`
- Source type: Experiment receipt
- Source:
  `experiments/phase2_architecture_experiment/PHASE2_EXPERIMENT_RECEIPT.md`
  and `PHASE2_1_GPT_REVIEW_PACKET.md`.
- Relevant content: Treatment improved the tested multi-act and target
  ownership outcomes, cost materially more, and shared the A09 hard-gate
  violation with Control. The receipt says the package did not isolate loop
  control from authority access and extra budget.
- Supports: a cost-bearing Treatment-package signal and the need for ablation.
- Does not support: Agent Loop superiority, causal loop value, or a promotion
  decision.
- Human confirmation still needed: none for the recorded experiment result;
  generalization remains open.

### E-018: Phase 2.2 preregistered mechanism comparison

- Status: `OBSERVED`
- Source type: Experiment receipt
- Source:
  `experiments/phase2_architecture_experiment/PHASE2_2_MECHANISM_ABLATION_GPT_REVIEW_PACKET.md`
  and `PHASE2_2_MINIMUM_SEMANTIC_MECHANISM_RECEIPT.md`.
- Relevant content: candidates isolated authority access, budget, refinement,
  authority plus refinement, and a bundled Agent Loop reference; decision order
  and target/sentinel rules were frozen before new results.
- Supports: causal comparison design and the simplicity prior.
- Does not support: provider-independent causal generalization.
- Human confirmation still needed: whether the bounded semantic candidate
  should remain current after future fresh evidence.

### E-019: Phase 2.2 result

- Status: `OBSERVED`
- Source type: Experiment result
- Source: final rerun under
  `experiments/phase2_architecture_experiment/phase2_2_evidence_20261007_rerun01/`.
- Relevant content: authority-assisted and authority-refinement improved target
  cases; budget-matched and refinement-only did not; authority-only regressed
  an ambiguity sentinel; authority plus one refinement met target and sentinel
  requirements; the full Agent Loop reference was not shown necessary.
- Supports: `authority_refinement` as the provisional minimum tested safe
  semantic mechanism.
- Does not support: a complete product architecture, global H1, or the claim
  that loops never add value.
- Human confirmation still needed: broader independent validation.

### E-020: DSH Evaluation v0 discovery model

- Status: `OBSERVED` / `HUMAN_RATIFIED` as scope boundary
- Source type: Document, code, and receipt
- Source:
  `experiments/dsh_evaluation_v0/README.md`,
  `experiments/dsh_evaluation_v0/contract.py`, and the Iteration 1 receipt.
- Relevant content: DSH generated natural-language scenarios against a frozen
  candidate, preserved seed/scenario/conversation/trace, and checked
  deterministic invariants outside product Runtime.
- Supports: DSH as an external bounded evaluation workstream.
- Does not support: autonomous product evolution or a product Runtime Agent.
- Human confirmation still needed: future DSH scope and promotion policy.

### E-021: Terminal Work mutation discovery and repair

- Status: `OBSERVED`
- Source type: Experiment receipt, trace, test, and commit
- Source: core-gate receipt at
  `experiments/dsh_evaluation_v0/evidence/core_gate_closure/AISAILINGS_V1_CORE_GATE_CLOSURE_RECEIPT.md`,
  seed 67 T003/T005 traces, commit `4e204d1`, and terminal ownership receipt
  under `evidence/terminal_ownership_repair/`.
- Relevant content: seed 67 showed a cancelled Work was later mutated; the
  failure was assigned to Workflow/ownership; the repair added a terminal
  guard; seed 71 and seed 73 then passed the bounded terminal invariants.
- Supports: the causal local repair story and terminal ownership gate closure.
- Does not support: full Lead Continuity, arbitrary Work reference resolution,
  or a general new-Work policy.
- Human confirmation still needed: future ambiguous cancellation/new-demand
  interactions.

### E-022: DSH fresh sibling failures and evaluator correction

- Status: `OBSERVED`
- Source type: Receipt and commit
- Source: DSH Iteration 1/2 receipts and commits `442c8d4`, `4574d8d`,
  `d1fda3f`, and `1d8d041`.
- Relevant content: fresh sessions found correction/retrieval/ownership issues;
  evaluator coverage itself was repaired when it missed a valid correction
  precondition; a current-result Workflow dispatch gap was repaired separately.
- Supports: the project learned to separate product failures from evaluator
  failures and transport failures.
- Does not support: the evaluator is universally complete.
- Human confirmation still needed: broader evaluator validation.

### E-023: Evidence versus filter boundary

- Status: `OBSERVED` / `HUMAN_RATIFIED`
- Source type: Product and slice reports
- Source:
  `AISAILINGS_LEGACY_EVIDENCE_HANDOFF.md`,
  `PACKAGE_1_SLICE_2_SEMANTIC_AUTHORITY_CUTOVER_REPORT.md`, and the North
  Star document.
- Relevant content: user facts are retained as evidence unless an executable
  field is authorized by the current contract.
- Supports: the trust boundary and safe retrieval claim.
- Does not support: support for age/salary/experience filtering.
- Human confirmation still needed: future business policy for unsupported facts.

### E-024: Core gate closure after targeted repairs

- Status: `OBSERVED`
- Source type: Core-gate receipt
- Source:
  `experiments/dsh_evaluation_v0/evidence/core_gate_closure/AISAILINGS_V1_CORE_GATE_CLOSURE_RECEIPT.md`.
- Relevant content: Confirmation seeds 59/61 passed current result,
  correction coverage, and ownership; Discovery 67 failed terminal immutability;
  Human Experience remained not passed.
- Supports: the important distinction between repaired gates and a remaining
  lifecycle blocker at that point in the evolution.
- Does not support: the final terminal repair by itself; that is E-021.
- Human confirmation still needed: whether the current head should continue to
  treat the terminal gate as closed after any later source change.

### E-025: Human UAT Round 1 experience gaps

- Status: `OBSERVED`
- Source type: Human UAT failure analysis
- Source:
  `experiments/phase2_architecture_experiment/HUMAN_UAT_ROUND_1_FAILURE_ANALYSIS_PACKET.md`
  and the core-gate reconciliation table.
- Relevant content: compound vessel expression did not produce the expected
  usable canonical type; generic state re-query did not explain the unresolved
  condition; alternative vessel policy and unsupported authority coverage
  remained open.
- Supports: current Human Experience limitations and open policy questions.
- Does not support: the claim that those gaps were solved or that they should
  be ignored because core automation passed.
- Human confirmation still needed: desired product behavior for each gap.

### E-026: Separate terminal immutability from Lead Continuity

- Status: `HUMAN_RATIFIED`
- Source type: User direction and Design Guard receipt
- Source: current control-plane Design Guard material and terminal ownership
  repair receipt.
- Relevant content: “cancelled Work cannot be modified” is a Workflow hard
  invariant; “cancel old task and create/select a new Work” is a separate Lead
  Continuity capability and may require clarification.
- Supports: the correct boundary for interpreting the terminal repair.
- Does not support: complete Lead Continuity.
- Human confirmation still needed: exact business policy for ambiguous
  references and “重新找” semantics.

### E-027: Current branch and control-plane identity

- Status: `OBSERVED`
- Source type: Git and control-plane files
- Source: branch
  `feature/semantic-turn-projection-v01`, HEAD
  `6f37eba0ba07d1b4d4a02e0c2946c3b475cebeea`, clean worktree at inspection,
  `docs/control_plane/README.md`, and `AGENTS.md`.
- Relevant content: current Design & Evolution Guard is persisted as part of
  the four-layer control plane; the worktree is the accepted product baseline
  for this case.
- Supports: the current-state identity and the document authority order.
- Does not support: any claim about uncommitted external worktrees or PR state.
- Human confirmation still needed: whether a later branch has superseded this
  head.

## Important relationships and their evidence

### L-001: Original goal -> bounded semantic/workflow slices

- Claim type: `INFERRED` from `E-001`, `E-002`, `E-006`.
- Supports: the project implemented the original goal through bounded workflow
  slices rather than treating the provider call as the product.
- Cannot prove: that every later implementation choice was directly caused by
  the original documents.
- Alternative explanation: the slices may have been driven partly by available
  demo assets and time constraints, which are not fully recorded.

### L-002: Mixed mutation risk -> validated Semantic Delta decision

- Claim type: `OBSERVED` for the report's stated rationale and implementation;
  causal project-level synthesis is `INFERRED`.
- Supports: the clean path was designed around a single validated mutation
  input and shadow legacy comparison.
- Cannot prove: this was the only reason for the change or that all callers now
  use it.
- Alternative explanation: the Delta boundary may also have been chosen for
  auditability and migration convenience.

### L-003: Phase 2.1 bundled signal -> Phase 2.2 ablation

- Claim type: `OBSERVED` / `HUMAN_RATIFIED` within the experiment receipt.
- Supports: Phase 2.1 explicitly says the treatment bundled mechanisms and the
  next question was causal ablation.
- Cannot prove: that no other internal motivation contributed.
- Alternative explanation: cost control or desire to avoid Phase 3 may also
  have influenced timing, but is not separately quantified.

### L-004: Seed 67 failure -> terminal Workflow repair

- Claim type: `OBSERVED`.
- Supports: the core-gate receipt names the first divergence and the next-step
  repair, commit `4e204d1` implements the guard, and later receipt reports the
  bounded gate pass.
- Cannot prove: that the repair handles every future reference ambiguity.
- Alternative explanation: a different lifecycle routing policy could also
  have avoided this exact trace.

### L-005: Human UAT gaps -> unresolved product work

- Claim type: `OBSERVED` / `INFERRED`.
- Supports: the gaps are directly recorded and remain in the limitation table.
- Cannot prove: their priority relative to future product work without a human
  product decision.
- Alternative explanation: a future controlled policy could make some current
  gaps intentionally unsupported rather than defects.

## Evidence gaps for future versions

1. Preserve a stable Session-to-workstream link when delegating work. Current
   Session logs show activity, but not a complete semantic label for each
   workstream.
2. Record explicit decision events separately from agent summaries and commit
   messages, including who accepted/rejected a hypothesis and why.
3. Record experiment lineage in machine-readable form: candidate hash, shared
   downstream hash, corpus hash, decision rule hash, and final disposition.
4. Record rejected alternatives and the evidence threshold that rejected them;
   commit messages alone are too terse.
5. Record product policy decisions separately from technical fixes, especially
   for Work creation, vessel alternatives, and unsupported knowledge.
6. Preserve an immutable human UAT observation schema with expected behavior,
   actual behavior, severity, and whether it blocks Core or Experience gates.
7. Preserve PR review disagreement and approval context in a project-accessible
   artifact; it is not recoverable from Git alone.
8. Record whether a result was selected, merged, quarantined, or merely tested,
   rather than inferring lifecycle from directory names.
