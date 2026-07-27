# AP-002 — Implementation Plan

**Programme:** AP-002 — Educational Assessment Engine  
**Status:** Design — future implementation roadmap  
**Constraint:** Each milestone independently releasable; no big-bang cutover  

---

## 1. Sequencing principle

Build along the authority chain:

```
Domain → Delivery → Evidence → Twin wiring → Adaptive triggers → Founder analytics
```

Preserve AP-001 as observation ingress. Prefer additive schema and opt-in mission activity types.

---

## 2. Milestones

### AP-002A — Assessment domain

**Goal:** Establish Assessment Engine bounded context (domain + application skeletons) without student UX.

**Deliver:**

- Domain types: AssessmentSession, AssessmentItemRef, Response, Intent, EvidenceDimensions
- Application service interfaces (create session, commit response) behind ports
- Persistence model additive tables (sessions/items/responses) — no Twin duplication
- Founder diagnostic read endpoints (optional, thin)
- Architecture doc + tests for domain invariants

**Does not:** Deliver questions to students, change missions UX, call Reasoning bypassing AP-001.

**Exit:** Domain compile/tests green; AP-001/SDT/AME/Tutor unchanged in behaviour.

---

### AP-002B — Question delivery

**Goal:** Deliver curriculum-aligned items in a minimal student surface.

**Deliver:**

- Instrument catalogue (seeded / founder-authored subset)
- Session construction + one-item-at-a-time delivery UI
- Response capture (MC/numeric/confidence first)
- Mapping to AP-001 `question_attempt` / `quiz_submission` events
- UX copy aligned with `UX_PRINCIPLES.md`

**Does not:** Full taxonomy (all item types), adaptive triggering, Tutor deep integration.

**Exit:** Student can complete a short check; observations appear via AP-001.

---

### AP-002C — Evidence collection

**Goal:** Rich, deterministic evidence dimensions on every committed response.

**Deliver:**

- Full evaluation rules for initial item types
- Misconception tags, hint/retry/time metadata
- PerformanceSummary enrichment (evidence-only)
- Evidence strength banding contract
- Validation that soft signals remain non-authoritative alone

**Does not:** New Reasoning policies beyond consuming richer metadata; no LLM scoring.

**Exit:** Founder diagnostics show evidence dimension completeness; integrity tests pass.

---

### AP-002D — Twin integration

**Goal:** Ensure richer observations improve Twin usefulness through Reasoning.

**Deliver:**

- Observation metadata contract freeze
- Reasoning rule updates *only as needed* to consume new evidence dimensions (separate careful change)
- Traceability: session → event → observation → reasoning run
- Thin-evidence / cold-start honesty checks
- Regression: no direct mastery writes from Engine

**Does not:** Redesign Twin aggregate; does not add LLM inference.

**Exit:** Same inputs → same Twin inferences; audit chain complete; architecture tests green.

---

### AP-002E — Adaptive triggering

**Goal:** Mission Engine can schedule assessment intents lawfully.

**Deliver:**

- Trigger policies: diagnostic, revision, checkpoint, adaptive, recovery, mastery verification
- Eligibility gates (workload, density, prerequisites)
- Mission activity mapping + explainable reasons on mission card
- Opt-in generation; Learning Mode authority preserved
- Tutor “explain this check” hookup to recent session feedback

**Does not:** Exam simulation product; forced passwalls.

**Exit:** Missions optionally include framed checks; Twin updates influence next missions only via Reasoning.

---

### AP-002F — Founder analytics

**Goal:** Operator visibility into assessment system health — not student league tables.

**Deliver:**

- Evidence density dashboards
- Instrument quality (misconception yield, abandonment, over-assessment rate)
- Pipeline health (events without reasoning, failed emission)
- Export for research / EIP evidence programmes

**Does not:** Student-facing rankings; marketing score vanity.

**Exit:** Founders can answer “is assessment reducing Twin uncertainty?” with evidence.

---

## 3. Dependency graph

```
AP-002A
   ↓
AP-002B
   ↓
AP-002C
   ↓
AP-002D  ← may coordinate with Educational Reasoning rule milestone
   ↓
AP-002E  ← depends on AME-001 stability
   ↓
AP-002F
```

TUTOR-001 remains consumable from AP-002B onward for light explanation; deeper interpret patterns land with AP-002E.

---

## 4. Release rules

1. Each milestone ships behind feature flags where student-visible.
2. Each milestone includes architecture compliance notes (V1/V2 curriculum untouched unless Retrieval contracts need additive profiles).
3. No milestone may introduce LLM into Reasoning.
4. Migrations are additive and reversible in intent (no Twin table drops).
5. Completion reports required per programme reporting rules when executed.

---

## 5. Suggested first implementation slice

Start with **AP-002A + narrow AP-002B**: one subject, multiple-choice + confidence, manual Founder-triggered session — prove observation yield before adaptive triggering.

---

## 6. Explicit non-milestones (defer)

- Full free-text LLM rubric scoring
- High-stakes mock exam product
- Replacement of LXP practice capture on day one
- Public question marketplace
- Peer comparative analytics
