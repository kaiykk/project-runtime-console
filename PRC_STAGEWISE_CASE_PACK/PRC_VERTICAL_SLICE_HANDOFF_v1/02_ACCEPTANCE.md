# Acceptance — PRC Integration Vertical Slice

## P0 (required for DONE)
- [ ] Both approved source HTML mocks loaded and distinguished correctly; C old Work iframe ignored.
- [ ] App starts locally from a documented command (no remote provider required for read-only viewer).
- [ ] Local Codex real source imported, file remains unchanged; session ID and original provenance path visible.
- [ ] Work / Agents / Trace all clickable in ONE shell and stay navigable without iframe placeholders.
- [ ] Trace shows real session grouped by turn, real tool calls, source-grounded raw-detail affordance; bad/incomplete events handled.
- [ ] Agents uses native identity/parent-child only if found; explicit single-agent/no-lineage empty state otherwise.
- [ ] Work B2 reference case readable with goal→current, decision pivots, evidence; reference flagged curated. Local session adds ≥1 authentic evidence-linked activity entry, or explicitly ‘no reliable significant change’, never fake an architecture decision.
- [ ] Work node inspector readable and spacious, back button functions, upstream/downstream selection reflects real registered relations, evidence drilldown works.
- [ ] Cross-tab source identity preserved: select a real local Session, drill from its Work activity → native Agent/Trace record and back where source mapping exists; missing mapping has explicit unavailable state.
- [ ] Project/run switching does not mix two sessions' identities, source locations or curated case.
- [ ] Browser screenshot checks at desktop sizes (e.g. 1366 and 1600 width), interactions and browser console error check run.
- [ ] No success claim based only on copied screenshot or fabricated fixture; no exposure of secrets or remote uploads; no mutation of original sessions.

## P1 only if cheap
- [ ] Incremental ingestion/polling without duplicate events.
- [ ] Search/filter in source sessions; minimal decision capturing Skill integration with provenance.

## Explicitly out of scope
- Remote Codex App ingestion; full project-history reconstruction; daily scheduled recap; auto-human-ratified causal graph; multiple provider universal parsers; production auth/cloud hosting; complete Sandcastle adoption.

## Evaluation status discipline
- PASS: actually demonstrated on real local records with browser/API tests and screenshots.
- PARTIAL: working authentic path with documented missing mapping/interactions.
- BLOCKED: no required C prototype or no readable local session; never substitute invented data.
