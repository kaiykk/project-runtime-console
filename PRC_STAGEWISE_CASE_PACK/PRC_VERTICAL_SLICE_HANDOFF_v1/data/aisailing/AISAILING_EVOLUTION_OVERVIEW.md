# AISailings Agent Project Evolution Case V0

Status: `V0_REPRESENTATIVE_EVIDENCE_CASE`

Generated: `2026-10-08`

Scope: AISailings Recruitment Agent development evidence available in the
current repository/worktree and selected Codex/DSH records. This is an
evolution case for an external Project Runtime Console experiment. It is not
a product architecture specification, a release approval, or a claim that an
agent has autonomously understood the project.

## Evidence discipline

This case uses four labels:

- `OBSERVED`: directly present in a source file, commit, test, trace, or
  receipt.
- `HUMAN_RATIFIED`: explicitly accepted, rejected, or bounded by the Product
  Owner/Principal in a project control document or recorded user direction.
- `INFERRED`: a conservative synthesis from multiple observations; it is not
  itself a project decision.
- `UNKNOWN`: the accessible records do not establish the claim.

The case deliberately does not turn chronological adjacency into causality.
Where a receipt explicitly says that an observation caused a repair or a
decision, that relation is recorded. Elsewhere, the text says only that two
workstreams coexisted or that a later state is visible.

## 1. Thirty-second view

### Why the project started

The project began as a maritime AI work entry, with recruitment as the first
deep workflow. The intended user experience was natural-language description
of a crewing need, followed by clarification when information was missing and
useful candidate retrieval through existing business capabilities. Chat was
the interaction surface, not the product object; the early constitution
described the recruitment task/workflow as the primary subject.

This initial goal is `HUMAN_RATIFIED` in the 2026-08 project constitution and
knowledge map. The earliest accessible records also show a deliberate split
between a Python provider layer, workflow/validation, controlled business
tools, Backend, and Frontend. At that stage the project had not yet settled
the final Work model or a global acceptance corpus.

### What changed most

The work moved through four connected but distinguishable directions:

1. **Recruitment semantics and bounded workflow slices.** The team converted
   raw language into evidence-preserving semantic proposals, clarification
   state, canonical vessel/position resolution, validated state changes, and
   bounded retrieval. Missing, explicit unknown, and explicit unrestricted
   vessel scope were separated; unsupported user facts were preserved rather
   than silently made into filters.
2. **Real runtime and Frontend continuity.** The prototype was connected to
   real HTTP and browser paths, while the team investigated latency, pending
   clarification ownership, state projection, and candidate ownership. A
   two-call provider path became the bounded V0.1 default for the tested scope,
   but not a permanent architecture decision.
3. **Mechanism comparison.** Phase 2 compared a single structured semantic
   call with a bounded Agent Loop and then ablated authority observations,
   refinement, and extra budget. The Agent Loop was not accepted by assumption.
   The bounded evidence favored read-only maritime authority observations plus
   one proposal refinement as the smallest tested safe semantic mechanism,
   while leaving global H1 and production readiness unestablished.
4. **Evidence-driven lifecycle safety.** DSH was kept outside the product
   Runtime and used to generate constrained natural-language sessions. It
   found that a cancelled Work could still be mutated by a later turn. That
   finding led to a Workflow terminal-ownership guard and a Design & Evolution
   Guard. The resulting evidence closed the tested terminal immutability and
   terminal-to-new-intent gates, but did not establish full Lead Continuity or
   Human Experience success.

### Current state in one sentence

As of the current branch HEAD `6f37eba0ba07d1b4d4a02e0c2946c3b475cebeea`,
AISailings has a bounded, evidence-instrumented recruitment prototype with
stronger ownership and terminal-state invariants than its earlier slices, and
an accepted provisional semantic candidate, but it remains a constrained demo:
compound vessel normalization, state explanation, alternative-set policy,
full Lead Continuity, Maritime Knowledge Service coverage, and a complete
Human Experience Gate are not established.

The sentence above is a synthesis: its individual parts are separately
supported by the current control plane and receipts; it is not a new product
ratification.

## 2. Main work directions

### Direction A: From provider call to recruitment workflow

**Why it started.** The original project needed to move from a text-only
provider call toward a useful recruitment workflow without inventing business
facts or rebuilding the existing recommendation algorithm. The early project
documents explicitly placed the provider layer before workflow, validation,
controlled business tools, Backend, and Frontend.

**What actually happened.** The earlier `pi-ai` work established bounded
retrieval and clarification slices, including S02 direct supported retrieval
and S04 conditional partial execution. The later demo work added a runtime
with Work/Context/Position distinctions, source evidence, clarification
ownership, and a validated semantic delta as the clean mutation input. Existing
legacy mutation paths were retained as shadow/compatibility evidence in the
bounded clean path instead of being allowed to override validated state.

**Status.** `PARTIALLY_COMPLETE_FOR_BOUNDED_SLICES` (`OBSERVED`). The slices
demonstrate useful local behavior and reusable boundaries, but they do not
prove the final global Work model, full user task continuity, or all business
policies.

### Direction B: Semantic authority, vessel scope, and safe fallback

**Why it started.** Real recruitment language showed that canonical vessel
terms, shorthand, missing vessel information, explicit unknowns, and
position-only fallback have different meanings. A null field could not safely
mean both “not mentioned” and “search any vessel”.

**What actually happened.** The runtime published bounded vessel authority and
coverage, separated `KNOWN`, `ANY`, `MISSING`, and `UNKNOWN`, and required
explicit fallback authorization for an unknown vessel before position-only
retrieval. Multi-context evidence showed that fallback authorization must stay
with its owning Context. The clean path kept unsupported facts as evidence and
did not silently compile them into SQL predicates.

**Status.** `SUPPORTED_FOR_TESTED_SUPPORTED_PATHS` (`OBSERVED`). The evidence
does not establish complete maritime authority coverage. Human UAT later showed
that compound phrases such as `21万吨散货船` and unsupported/alternative
vessel requests still have product-facing gaps.

### Direction C: Real interaction responsiveness and Frontend truth mapping

**Why it started.** After the bounded runtime existed, the product needed to
work through the real Backend-to-Frontend surface and respond within a useful
interaction budget. The control plane made responsiveness the active P0 while
preserving natural-language continuity and Frontend truth mapping as product
invariants.

**What actually happened.** Real provider behavior and call timing were
measured. Provider thinking was disabled for the tested latency comparison,
and a two-call path was made the bounded V0.1 default. The work also restored
Frontend scrolling, connected the candidate-aware HTTP path, and ran browser
smokes. These changes were accompanied by explicit warnings that a passing
latency sample was not a global SLA and that browser/Backend continuity was an
acceptance surface.

**Status.** `BOUNDED_EVIDENCE_ONLY` (`OBSERVED`). The runtime path is usable for
the tested cases, but the global latency target, all current Frontend behavior,
and complete Human Experience quality remain unvalidated.

### Direction D: Architecture hypothesis and mechanism ablation

**Why it started.** A testable H1 compared a single structured semantic call
with a bounded Agent Loop while preserving shared Workflow, Authority,
Retrieval, Backend, and Frontend boundaries. The comparison was intended to
falsify the assumption that an Agent Loop must be better.

**What actually happened.** Phase 2.1 found a narrow Treatment-package value
signal for multi-act interpretation and context/target ownership, at materially
higher cost, while both candidates shared a downstream hard-gate problem.
After the shared repair, Phase 2.2 compared authority access, additional
budget, refinement, authority plus refinement, and the bundled Agent Loop
reference. Extra budget alone and refinement alone did not reproduce the target
gain. Authority alone improved target cases but regressed an ambiguity
sentinel. Authority plus one refinement met the bounded target and sentinel
rule. The full Agent Loop was not shown necessary.

**Status.** `PROVISIONAL_SEMANTIC_MECHANISM_RESULT` (`OBSERVED`, with the
claim boundary stated in the receipt). `authority_refinement` is an accepted
provisional semantic candidate for the bounded evidence path, not a global
product architecture promotion.

### Direction E: DSH as an external failure-discovery loop

**Why it started.** The project needed fresh natural-language combinations,
not only hand-authored query fixes. DSH was introduced as an external,
bounded black-box evaluator that could create latent scenarios, converse with
the frozen candidate, save traces, and check deterministic business
invariants. The product Runtime was explicitly kept separate.

**What actually happened.** DSH generated fresh sibling sessions that found
correction/retrieval and result-ownership issues, then later found a terminal
Work mutation after cancellation. The evaluator itself also needed repair when
its correction coverage logic failed to recognize a valid action-ready state.
The project preserved transport failures, invalid attempts, and old evidence
instead of silently converting them into product results.

**Status.** `BOUNDED_EVALUATION_CAPABILITY` (`OBSERVED`). DSH can discover
some capability-level failures in the tested environment. It does not prove
the product is autonomous, globally reliable, or ready for Phase 3.

## 3. Key turns in the evolution

### Turn 1: The project stopped treating parsed language as an executable filter

The early constitution and later runtime reports repeatedly separated what the
user said from what the existing data and recommendation path could execute.
Age, salary, experience, schedule, location, tonnage, and other facts could be
preserved as evidence without becoming SQL predicates. This became a durable
product boundary, not just a parser detail.

`OBSERVED`: the rule is stated in the product documents and exercised in the
bounded slices. `HUMAN_RATIFIED`: the control-plane product boundaries retain
this as a ratified expectation. `INFERRED`: this rule is one of the project's
most important trust-preserving changes because it prevents a visible answer
from claiming more business truth than retrieval actually used.

### Turn 2: Mutation authority moved toward validated semantic deltas

The clean runtime work identified a mixed-authority problem: interpretation,
action selection, direct mutation, and retrieval could be interleaved. The
bounded cutover made a validated Semantic Delta the only clean business-field
mutation input, while keeping old action paths as shadow evidence during
transition. This reduced the chance that a legacy branch could silently write
or override validated state.

`OBSERVED`: the Slice 2 report, source, tests, and real S1/S2 traces establish
this for the clean path. `UNKNOWN`: the evidence does not establish that all
historical direct callers have been retired; the report explicitly says some
standalone legacy callers remain compatible paths.

### Turn 3: The active product priority became real interaction responsiveness

The 2026-09-27 control-plane ratification explicitly made real interaction
responsiveness the active P0, while preserving semantic continuity and
Frontend truth mapping as invariants. The runtime then measured call timing,
changed the tested default path, and recorded the limits of that evidence.

This is a `HUMAN_RATIFIED` priority change within V0.1, not evidence that
latency work replaced the product goal. The available records do not prove that
every latency change was solely caused by one experiment; the evolution graph
therefore represents this as a ratified workstream and a bounded implementation
outcome, not an overconfident causal claim.

### Turn 4: The Agent Loop was treated as a hypothesis, not a destination

Phase 2.1 showed a cost-bearing Treatment package signal. The receipt itself
states that the signal bundled loop behavior, authority observations, and extra
inference budget, so it did not justify retaining the Agent Loop as a whole.
Phase 2.2 then preregistered an ablation comparison. The final bounded result
favored read-only authority observations plus one explicit proposal refinement,
while weakening budget-only, refinement-only, authority-only-as-promotion, and
full Agent Loop necessity claims.

This is one of the clearest examples of evidence changing the strength of an
architecture hypothesis. It does **not** prove that a loop can never be useful;
it limits the current claim to the tested semantic capability families and
corpus.

### Turn 5: A safe cancellation response was not enough

The first core-gate closure receipt recorded that Confirmation seeds 59 and 61
passed current-result, correction, and cross-Work ownership checks. Discovery
seed 67 then showed a more serious mismatch: the system said a Work was
cancelled, but a later mutation changed the cancelled Work's business content.
The trace identified a Workflow/ownership divergence rather than a provider or
evaluator problem. This caused a local Workflow repair and focused the Design
Guard on distinguishing terminal immutability from the separate Lead
Continuity question of creating or selecting a new Work.

The subsequent terminal-ownership receipt reports fresh Confirmation seed 71
and Discovery seed 73 passing the bounded terminal invariants. That closes the
tested lifecycle boundary, not all possible referent and new-Work ambiguity.

### Turn 6: Human experience remained a separate gate

Human UAT Round 1 exposed at least two user-facing gaps: compound vessel
language did not yield the expected usable vessel type, and the system could
not explain which condition remained unconfirmed. The project classified these
as future capability/experience gaps for the bounded core gate, while retaining
them as explicit limitations. That separation is important: the machine core
gate could proceed for a local invariant without declaring the Human Experience
Gate passed.

## 4. What was retained, withdrawn, or redirected

### Retained

- The maritime recruitment assistant remains the product mainline.
- Natural language remains the product input; clarification is a valid outcome.
- Work, Context, Position, ownership, source evidence, and authoritative
  business state remain separate concepts.
- Existing maritime/recruitment services and retrieval paths are reused rather
  than replaced by a new recommendation algorithm.
- Validated business mutation and fail-closed retrieval gates remain the core
  safety direction.
- Candidate freeze, identity attribution, node-level trace, raw versus
  normalized evidence separation, and immutable historical receipts remain the
  experiment discipline.
- `authority_refinement` remains the provisional semantic candidate within the
  bounded mechanism result, without silently becoming a permanent product
  architecture.

### Withdrawn, weakened, or quarantined

- The claim that a bounded Agent Loop is automatically superior was weakened;
  no Agent Loop winner was promoted from the shared-hard-gate result.
- Extra inference budget as an explanation was weakened by the Phase 2.2
  budget-matched candidate.
- Refinement without authority observations was weakened by the refinement-only
  candidate.
- Authority-only promotion was withheld because of the ambiguity sentinel
  regression.
- Legacy semantic mutation branches were moved behind a shadow/compatibility
  boundary in the clean path; physical retirement was explicitly deferred,
  not falsely declared complete.
- Full Lead Continuity, Skills/Experts, dynamic routing, Maritime Knowledge
  Service, and Phase 3 autonomous R&D were not admitted as consequences of the
  bounded results.

### Changed direction

The project direction became more evidence- and boundary-driven. The work
shifted from “build an intelligent agent architecture” toward:

```text
preserve user meaning
-> validate attribution and authority
-> commit authoritative state safely
-> retrieve only from allowed state
-> verify the visible Frontend result
-> use bounded experiments to challenge the architecture hypothesis
```

This is `INFERRED` as a cross-record characterization. The underlying
responsibility boundaries and accepted decisions are directly documented.

## 5. Current state

### Established for bounded scope

- A real recruitment Backend/Frontend path exists for the tested candidate
  entrypoint and can expose candidate results with identity checks.
- Known, missing, unknown, and explicit unrestricted/fallback vessel semantics
  have bounded tested behavior.
- Validated mutation and current-result ownership gates exist in the tested
  clean workflow.
- Terminal Work immutability and terminal-to-new-intent re-owning passed the
  latest bounded Confirmation/Discovery gate.
- The `authority_refinement` mechanism result is supported for the tested
  Phase 2.2 target and sentinel corpus.
- The project has retained failure evidence, not only passing snapshots.

### Partially complete

- Natural-language multi-turn recruitment continuity works for selected cases,
  but broad Lead Continuity and referent resolution are not established.
- Vessel authority coverage is useful but not complete. Compound phrases,
  alternatives, and unsupported vessel types still need product decisions and
  evidence.
- State mutation and retrieval ownership are safer, but legacy compatibility
  paths remain and need explicit lifecycle treatment before any claim of total
  retirement.
- The Frontend continuity path is real for tested smoke/candidate paths, but
  Human UAT quality remains a separate open gate.

### Still unresolved

- Full Lead/Task Continuity: when a user cancels an old Work and says “find
  another chief officer”, when should the system create a new Work, select an
  existing Work, or ask a clarification?
- Compound vessel normalization and alternative-set policy, including whether
  “bulk or container” means a choice, a multi-scope search, or another policy.
- State explanation: how the assistant should explain the exact missing or
  unresolved business condition for a specific Work/Context.
- Maritime Knowledge Service scope and authoritative coverage beyond the current
  domain packs/services.
- Candidate details and broader retrieval usefulness.
- Global Agent Lead/mode routing and whether any loop is needed beyond the
  current semantic mechanism.
- The global acceptance corpus, provider-independent generalization, and
  production readiness.

## 6. Relationship to the original goal

The accessible evidence supports **alignment in direction**, not completion.
The project is still working on the original problem: a user should be able
to describe maritime recruitment needs naturally, receive safe clarification,
and obtain useful results through the real product path. The strongest changes
have made business state and visible results more trustworthy.

At the same time, the project has narrowed several claims. It no longer treats
an Agent Loop, a complete ontology, a generic Skill/Expert layer, or a passing
machine benchmark as automatic progress toward the product goal. That is
consistent with the original trust and authority constraints, but it leaves
important user-facing work unfinished.

The precise claim is therefore:

```text
GOAL_ALIGNMENT: SUPPORTED_FOR_DIRECTION
GOAL_COMPLETION: NOT_ESTABLISHED
HUMAN_EXPERIENCE_GATE: NOT_PASSED
GLOBAL_H1: NOT_ESTABLISHED
```

## 7. Evidence gaps and access limits

This V0 did not attempt to scan every historical Session, every branch, every
PR discussion, or every provider trace. The following gaps remain:

- No complete PR/Code Review API or PR discussion archive was inspected. PR
  intent, review disagreement, and merge rationale are therefore `UNKNOWN`
  unless preserved in repository documents or commits.
- Only selected Codex Session records were consulted. The available Session
  identifiers include `01a0c6d5-825b-7fd3-bb2b-4697bba9a9dd` and
  `01a110c6-629c-72c2-a919-9fe798b51b13`; they provide supporting context but
  are not a complete project history.
- Provider raw responses and browser artifacts exist in referenced evidence
  directories, but this V0 uses only targeted representative artifacts rather
  than reproducing every turn.
- The earliest business goal is reconstructed from project documents and
  recorded human direction; a complete original PRD or product-roadmap
  conversation was not available in the inspected scope.
- The relation between every individual commit and a human decision is not
  recoverable from commit messages alone. The Ledger marks such claims as
  `INFERRED` or `UNKNOWN` rather than assigning motives.

## 8. Interpretation boundary for PRC

PRC may use this case to display:

- goal to workstream to evidence to decision relationships;
- supported and weakened hypotheses;
- retained versus quarantined responsibilities;
- open questions and evidence gaps;
- confidence and evidence status.

PRC must not display this V0 as proof that AISailings has autonomous project
understanding, complete product readiness, or a globally valid architecture.

