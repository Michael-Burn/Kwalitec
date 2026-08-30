# ADR-027 M0 — Decision Boundary Design (Policy V0)

**Status:** Accepted design for M0 implementation — authorizes the **design only**; does **not** authorize code changes (implementation requires a separate scoped brief)  
**Governing ADR:** [`docs/adr/ADR-027-student-knowledge-state-and-adaptive-decision-architecture.md`](../adr/ADR-027-student-knowledge-state-and-adaptive-decision-architecture.md)  
**Nature:** Implementation design under ADR-027 (not a new ADR)  
**Date:** 2026-08-30  
**Verified against:** current working tree (Runtime C `EducationalRuntimeEngineService.generate_daily_mission`, Runtime A `PlanningService._select_topic_for_today`, PB-002 package selection, educational experience Home path)  
**Predecessor evidence:** ADR-027 empirical investigation (2026-08-30) — re-checked in code for this proposal

---

## Document purpose

M0 is the first migration step under ADR-027. Its only job is to prove that **decision-making authority** can sit behind the correct architectural boundary, with **identical student-facing decisions** to today, and with **trustworthy instrumentation** of every decision outcome.

M0 does **not**:

- Introduce genuinely adaptive (knowledge-driven) selection  
- Build or wire a Learner Twin as Decision Engine input  
- Change what Kwalitec decides for any student  
- Migrate every selection spine in the product  

**Success criterion (binding):**  
*Can we move the existing decision-making behaviour behind the correct boundary, prove that behaviour has not changed, and establish trustworthy instrumentation for what happens next?*

V1 (later, explicitly out of scope here) is where an adaptive policy that consumes Learner Twin state may be introduced.

---

## Placement rationale

This file lives under `docs/architecture/` because that directory already holds implementation plans and technical designs that sit under accepted architecture decisions (e.g. `CAPABILITY_2_*_IMPLEMENTATION_PLAN.md`). ADR-027 itself remains in `docs/adr/`. This document is a **design proposal under that ADR**, not a competing architectural decision.

Suggested filename if accepted without rename: keep  
`docs/architecture/ADR027_M0_DECISION_BOUNDARY_DESIGN.md`.

---

## 1. Selector choice

### 1.1 Candidates (verified)

| Candidate | Seam | Live student trigger today | What it decides |
|-----------|------|----------------------------|-----------------|
| **A — Runtime C** | Immediately before the topic/package/LO selection block inside `EducationalRuntimeEngineService.generate_daily_mission` (`app/application/educational_runtime_engine/service.py` ~448–777; selection core ~589–701) | `EducationalExperienceService.load_for_user(ensure_mission=True)` on Home/Journey (`educational_experience/service.py` ~209–215); Runtime C enrolled students never fall back to Runtime A (`presentation/student/views.py` V1S-007) | Syllabus topic (`derive_progress` → `current_topic_id`), post-tip Memory/Publication fronts, PB-002 package/day, certified LO overlay |
| **B — Runtime A Learning Mode** | `PlanningService._select_topic_for_today` (`planning_service.py` ~1452–1583) before mission persist in `_generate_mission_for_date` (~774) | Students **without** Runtime C enrolment (TEMPORARY RI-002 path); not Home for Runtime C CS1 | Consolidation checkpoint **or** `CurriculumService.get_next_incomplete_topic` |

### 1.2 Recommendation: **Candidate A (Runtime C `generate_daily_mission`)**

**Choose Runtime C as the first M0 seam.**

Reasoning (grounded in current code, not only the prior investigation summary):

1. **Matches ADR-027’s target loop.** The ADR ends at Orchestrator → **Runtime C**. Establishing the boundary on Runtime A Learning Mode would prove a seam on a spine the ADR treats as demoted for published-curriculum students, and would leave the live CS1 Home path still deciding inside Runtime C.
2. **Actively exercised on the sole-runtime student path.** With a Runtime C enrolment, Home/Journey ensure today’s mission exclusively via `generate_daily_mission`. Learning Mode is explicitly routed away for those students.
3. **Composition already sits downstream of a durable mission snapshot.** `StudentRuntimeCoordinator.accept_and_start_session` and session substance planning consume a materialised mission (`topic_id`, `educational_package_id`, objectives, tasks). They do not need to know how those fields were chosen — so M0 can demote selection without rewriting composition.
4. **Regression risk is concentrated but testable.** Runtime C selection is more complex than Learning Mode’s leaf walk, but behaviour-preservation tests can pin topic + package + LO identity. Preferring “simpler code” (Runtime A) would migrate the wrong authority for the product’s published-curriculum spine.

**Caveat (honest):** Candidate A is **not** the simpler first cut. Candidate B has fewer branches and a cleaner function boundary (`_select_topic_for_today` already returns `Topic | None`). It is a better *engineering* sandbox and a worse *architectural* first step under ADR-027.

### 1.3 Alternate for a later, separate M0-style migration

**Candidate B remains available** as a subsequent, separately scoped migration (suggested label: **M0-A**): wrap Runtime A Learning Mode (`_select_topic_for_today` / `get_next_incomplete_topic`, including the consolidation watermark branch) behind the same Decision Engine contract for non–Runtime-C students until RI-002 retirement. Do **not** fold M0-A into this M0.

---

## 2. Adaptive Decision Engine contract (M0-minimal)

### 2.1 Design rules for M0

- One **intent-specific** method for daily sitting selection (ADR left one-vs-many open; M0 settles **intent-specific for the first seam only**).  
- Do **not** require Learner Twin / Curriculum State / Context objects as meaningful inputs yet (those are V1+).  
- Do **not** reuse Cap 2.8 `app/domain/decision/engine.py` `DecisionEngine.evaluate(twin, readiness, …)` as the live M0 path — that engine is a separate structural Epic-2 ship, Twin-coupled, and is **not** wired to Runtime C Home today. Naming in code must avoid implying that Cap 2.8 engine is M0 authority.  
- Do **not** overload the Epic-2 `app/application/learning_orchestrator/LearningOrchestrator` pipeline facade (Evidence→Twin→Mission event coordination). ADR-027’s Learning Orchestrator for M0 is a **thin sitting coordinator** (proposed name below).

### 2.2 Proposed types (illustrative; implementation may adjust names)

```python
from enum import StrEnum
from dataclasses import dataclass
from typing import Protocol
from datetime import date

class DecisionOutcome(StrEnum):
    ADAPTIVE = "adaptive"
    SAFE_FALLBACK = "safe_fallback"
    BLOCKED = "blocked"

@dataclass(frozen=True)
class DailySittingRequest:
    """M0 inputs — enough to run Policy V0; not Twin state."""
    user_id: int
    subject_code: str
    mission_date: date
    # Optional opaque handles Policy V0 needs to call existing helpers
    # (enrolment/curriculum identity). Prefer passing ids, not Flask objects.
    curriculum_identity: str | None = None

@dataclass(frozen=True)
class SittingDecision:
    outcome: DecisionOutcome
    intent: str  # fixed "daily_sitting" for M0
    policy_id: str  # "policy_v0" for M0
    decision_id: str
    # Executable payload Runtime C needs to materialise a sitting
    topic_id: str | None
    topic_code: str | None
    educational_package_id: str | None
    educational_package_mode: str | None
    certified_mission_id: str | None
    objective_ids: tuple[str, ...]
    # Honest instrumentation
    reason_codes: tuple[str, ...]
    block_reason: str | None  # set iff BLOCKED
    # Provenance for audit (not student-facing)
    selection_trace: dict  # e.g. preferred_topic, memory_pack_id, pack_id

class AdaptiveDecisionEngine(Protocol):
    def decide_daily_sitting(
        self, request: DailySittingRequest
    ) -> SittingDecision:
        """Always returns exactly one of ADAPTIVE | SAFE_FALLBACK | BLOCKED."""
        ...
```

### 2.3 What Runtime C receives

Runtime C’s materialisation API accepts a **`SittingDecision` executable subset** (or a dedicated `SittingExecutionSpec` stripped of outcome/policy metadata). It must **not** import the Decision Engine protocol, Policy V0, or outcome enums for control flow — only execute topic/package/LO/title/task assembly it already performs after selection today.

---

## 3. Orchestration boundary

### 3.1 Proposed thin orchestrator

**Name (proposed):** `SittingDecisionOrchestrator`  
**Package (proposed):** `app/application/adaptive_decision/` (new), *not* inside `educational_runtime_engine/` and *not* an extension of Epic-2 `learning_orchestrator`.

**Call site:** replace the direct

`EducationalExperienceService.load_for_user` → `EducationalRuntimeEngineService.generate_daily_mission(...)`

with:

```
EducationalExperienceService.load_for_user
  └─ SittingDecisionOrchestrator.ensure_todays_sitting(user_id, subject, day)
        ├─ AdaptiveDecisionEngine.decide_daily_sitting(...)   # Policy V0
        ├─ record decision audit / telemetry
        └─ EducationalRuntimeEngineService.materialise_daily_mission_from_spec(spec)
```

Idempotency, enrolment guards that are **operational** (existing mission same-day, oversized retirement, tip-complete reopen) may remain in Runtime C **before** calling the orchestrator, *or* stay as pre-checks inside `generate_daily_mission` that short-circuit without consulting the engine. M0 preference: **keep today’s idempotent short-circuit inside Runtime C** so Policy V0 is only invoked when a new sitting identity must be chosen — matching “composition/ops unchanged; selection authority moves.”

### 3.2 How Runtime C stays unaware of the Decision Engine

| Layer | May know Decision Engine? | Role |
|-------|---------------------------|------|
| `SittingDecisionOrchestrator` | Yes | Calls engine; records outcome; hands execution spec to Runtime C |
| `AdaptiveDecisionEngine` / Policy V0 | Yes | Decides |
| `EducationalRuntimeEngineService` | **No** | Materialises mission from execution spec; templates, chunking, events, persist |
| `StudentRuntimeCoordinator` / session | **No** | Unchanged composition |

Dependency direction: **Orchestrator → Decision Engine** and **Orchestrator → Runtime C**. Runtime C never imports Decision Engine.

### 3.3 Flag gate during cutover

Introduce env flag (proposed): `KWALITEC_ADR027_M0_DECISION_BOUNDARY`  
- **Default OFF** in code and in production until explicitly enabled  
- OFF → today’s `generate_daily_mission` path unchanged (no behaviour risk while deploy is paused)  
- ON → orchestrator path above  

Document the flag in `docs/production/VERSION_1_FLAG_MATRIX.md` when implementation is accepted (out of scope for this proposal file’s acceptance).

---

## 4. Policy V0 — verbatim behavioural wrap

### 4.1 What Policy V0 is

Policy V0 is the **existing Runtime C selection logic** currently embedded in `generate_daily_mission`, extracted behind `AdaptiveDecisionEngine.decide_daily_sitting`, with **no intentional change** to inputs→outputs.

It is a **move**, not a rewrite. Prefer calling the same helpers in the same order:

1. Derive progress → `current_topic_id` / `syllabus_complete` / `completed_topic_ids`  
2. `pending_post_tip_front_package` → `memory_pack`  
3. Resolve `preferred_topic` (progress current, or package topic when post-tip + tip-complete)  
4. `_select_certified_mission(...)` with that preferred topic  
5. Finalize `topic_id` under MISSION-002 rules (certified topic only when it matches progress current and no memory pack)  
6. When `certified_guidance_enforced(subject)`: `resolve_active_educational_package(...)` (or use `memory_pack`)  
7. Produce objective id list using the same certified/template/mastered/chunking **selection** inputs Policy V0 owns for decision identity; **chunking against session budget** may remain Runtime C composition if that keeps the wrap smaller — but then comparison tests must assert the pre-chunk decision fields Policy V0 owns. **Recommendation:** for M0, treat **topic_id + educational_package_id + certified_mission_id + pre-chunk objective_ids** as the decision identity; leave session-budget chunking in Runtime C exactly as today.

### 4.2 Edge cases Policy V0 must reproduce exactly

Verified current behaviours:

| Condition | Today’s behaviour | Policy V0 must |
|-----------|-------------------|----------------|
| Syllabus complete **and** no post-tip front package | `SyllabusAlreadyComplete` raised; experience catches → `mission=None` | `BLOCKED` with stable `block_reason` (e.g. `syllabus_complete`) — student still sees no mission |
| Enrolment not ACTIVE and no memory pack | `IllegalRuntimeState` | `BLOCKED` (`enrolment_inactive`) |
| Tip-complete but CP/CR front remains | Re-open enrolment to ACTIVE; select memory pack topic/package | Same sitting identity as today |
| Existing GENERATED/ACCEPTED mission for day, package matches owed | Idempotent return of existing mission (**before** selection) | Unchanged Runtime C short-circuit; Policy V0 not consulted |
| Existing mission wrong package (PX-B-006) or completed learning blocking revision (PX-B-005) | Delete/regenerate | Unchanged Runtime C ops; then Policy V0 runs for regeneration |
| `certified_guidance_enforced` and no resolvable package | `CertifiedGuidanceUnavailable`; experience → `coverage_gap`, no mission | `BLOCKED` (`certified_guidance_unavailable`) |
| No mission template for topic | `IllegalRuntimeState` | `BLOCKED` (`no_mission_template`) |
| Unsatisfied `prerequisite_ids` on template/topic | `IllegalRuntimeState` with missing ids | `BLOCKED` (`unsatisfied_prerequisites`) — live CS1 artefacts typically have empty prereqs (inert), but code path must remain |
| Certified/template objectives all mastered | Fall back to remaining topic LOs or first template objective | Same objective identity |
| Preferred certified topic ≠ progress current (and not memory pack) | Keep progress/`preferred_topic` as mission topic (MISSION-002) | Same |

Policy V0 does **not** invent new recovery behaviour for these cases.

### 4.3 Explicit non-goals inside Policy V0

- No reading of Stage A `TopicProgress.mastery_score`, Twin daily-loop EK, or Cap 2.8 DecisionEngine candidates  
- No Runtime A consolidation watermark logic  
- No change to PB-002 successor rules themselves — only **who calls them**

---

## 5. Three-outcome semantics for M0 specifically

ADR-027’s abstract definitions assume a future adaptive policy. M0 has **no** such policy. An honest framing is required so telemetry is not a lie from day one.

### 5.1 Proposal (binding for M0)

Treat every Decision Engine invocation as a **two-stage evaluation**, even when stage one is a no-op:

1. **Adaptive attempt** — In M0, there is no adaptive policy. This stage **always declines** (records `adaptive_attempted=false` / reason `no_adaptive_policy_m0`). It never emits `ADAPTIVE`.  
2. **Deterministic Policy V0** — If V0 can produce a valid sitting identity, emit **`SAFE_FALLBACK`**. If it cannot (the BLOCKED table in §4.2), emit **`BLOCKED`**.

| Outcome | M0 meaning | Expected frequency at M0 soak |
|---------|------------|-------------------------------|
| `ADAPTIVE` | A knowledge-driven policy produced the sitting | **Always 0** until V1 |
| `SAFE_FALLBACK` | Adaptive declined; Policy V0 produced today’s linear/campaign sitting | Nearly all successful Home mission generations |
| `BLOCKED` | Neither adaptive nor Policy V0 can lawfully produce a sitting | Syllabus complete without fronts; guidance withheld; illegal state |

### 5.2 Why not label Policy V0 as `ADAPTIVE`?

Because ADR-027 forbids presenting a safe fallback as adaptive, and Policy V0 is explicitly **deterministic curriculum/campaign progression**, not a decision that follows from what the system believes the student knows. Labelling it `ADAPTIVE` would poison the very metric M0 is meant to create (“how often are we actually adaptive?”).

### 5.3 Why not collapse to a single outcome until V1?

Because the instrumentation contract must exist **before** V1 ships. Recording `ADAPTIVE=0` / `SAFE_FALLBACK=n` / `BLOCKED=m` from M0 onward is the point. Collapsing outcomes would force a second instrumentation migration later.

### 5.4 Student-facing speech

M0 must not introduce any student-visible claim that today’s mission was “adaptive.” Existing MES / explanation surfaces stay as they are. Outcome enums are **operator/audit**, not Home chrome.

---

## 6. Telemetry / audit requirements

### 6.1 What to record on every Decision Engine call

| Field | Purpose |
|-------|---------|
| `decision_id` | Stable id for this evaluation |
| `occurred_at` (UTC) | Timestamp |
| `user_id` | Student |
| `subject_code` / `curriculum_identity` | Scope |
| `intent` | `daily_sitting` |
| `seam` | `runtime_c.generate_daily_mission` |
| `outcome` | `adaptive` \| `safe_fallback` \| `blocked` |
| `policy_id` | `policy_v0` (or `none` when adaptive declined) |
| `block_reason` | Present iff blocked |
| `topic_id` / `topic_code` | Decision identity |
| `educational_package_id` / mode / campaign_day | Decision identity |
| `certified_mission_id` | When present |
| `objective_ids` (pre-chunk) | Decision identity |
| `reason_codes` | Stable machine codes (e.g. `policy_v0_campaign_order`, `no_adaptive_policy_m0`) |
| `mission_instance_id` | Filled after materialisation when a mission is created/returned |
| `flag_enabled` | Whether M0 path was active |
| `selection_trace` (compact JSON) | preferred_topic, memory_pack present, owed pack, etc. |

### 6.2 Where to persist (consistent with this codebase)

**Primary (durable, queryable):** append a row to Runtime C’s existing event spine — `runtime_educational_events` (`RuntimeEducationalEvent`) — with a new `EducationalEventType` such as `DECISION_RECORDED`. This matches how `MISSION_GENERATED` / `MISSION_COMPLETED` are already audited via `_append_event` in `EducationalRuntimeEngineService`.

- Orchestrator (or a small audit helper it owns) writes the decision event.  
- Prefer **not** overloading `MISSION_GENERATED` payload alone — selection outcome must be queryable even when materialisation is skipped (`BLOCKED`) or idempotently short-circuited.

**Secondary (operational logs):** structured log line via existing `StructuredLogger` / module logger with the same fields (correlation id when present), analogous to adaptive-shadow observational logging — logs are not the system of record.

**Do not use for M0 primary audit:**

- Decision Journal (`DecisionJournalEntry`) — product accept/dismiss of recommendations; different semantics  
- Cap 2.8 / Adaptive Shadow `ADAPTIVE_SHADOW_*` integration events — observational shadow pipeline, wrong claim class  
- Presentation telemetry — engagement chrome, not educational decision authority

### 6.3 Query posture M0 must enable

From day one of flag-ON soak, an operator must be able to answer:

- Count / rate of `ADAPTIVE` vs `SAFE_FALLBACK` vs `BLOCKED`  
- Top `block_reason` values  
- Whether any `ADAPTIVE` rows appear (M0 invariant: **zero**)

---

## 7. Behaviour-preservation test strategy

### 7.1 Goal

Prove Policy V0 behind the new boundary produces **identical sitting decisions** to the current live selector for a representative matrix of real student/topic/package states — not only the happy path.

### 7.2 Approach: dual-path characterization (table-driven)

1. **Freeze a reference function** `legacy_select_daily_sitting(...)` that is either:
   - the current inlined selection block extracted **without behaviour change** into a test-visible helper used by today’s `generate_daily_mission`, **or**
   - a characterization oracle that runs pre-M0 `generate_daily_mission` in a transaction and reads back topic/package/objectives from the mission/event payload, then rolls back.  
   Prefer extract-and-share: one implementation called by both legacy path (flag OFF) and Policy V0 (flag ON) initially is acceptable **only if** tests still compare Policy V0 against a pinned snapshot of expected identities from fixtures; do not let “single implementation” silently delete the comparison.

2. **Policy V0 path:** `AdaptiveDecisionEngine.decide_daily_sitting` → compare fields in §6 decision identity.

3. **Table-driven fixtures** (minimum set — expand if soak finds gaps):

| Case | State sketch |
|------|----------------|
| Cold start | No completed packs; first syllabus topic |
| Mid-campaign | Completed packs on a leaf; successor via `tomorrow_preview` / campaign_day |
| Same-leaf multi-day | Package chain still owed; topic must not advance |
| Post-tip Memory Front (CP) | Syllabus tip-complete; CP pending |
| Post-tip Publication Front (CR) | After CP; CR pending |
| Syllabus complete, no fronts | Expect BLOCKED / no mission |
| Guidance enforced, missing package | Expect BLOCKED + coverage gap behaviour |
| Certified LO overlay | Preferred topic matches progress; certified mission id present |
| Certified mismatch MISSION-002 | Certified topic ≠ current → keep progress topic |
| Idempotent same-day | Existing GENERATED mission returned; Policy V0 not required to re-decide |
| Oversized / wrong-package regeneration | Ops delete then new decision matches legacy |

4. **Assertions:** equality on `topic_id`, `educational_package_id`, `certified_mission_id`, ordered pre-chunk `objective_ids`, and block/no-block. Do not assert new `decision_id` equality.

5. **Property / soak gate (pre-merge confidence):** run the dual comparison across **all CS1 publication_approved package chain positions** represented in inventory fixtures (or a generated walk of campaign days for at least one subject), plus **N ≥ 50** randomized but deterministic seeded progress/pack completion subsets. Fail the suite on any divergence.

6. **Flag-OFF regression:** existing Runtime C mission generation tests (`tests/application/educational_runtime_engine/`, certification CS06, experience tests) remain green with flag OFF without modification beyond any shared helper extract.

7. **Flag-ON smoke:** subset of the same tests with flag ON; Home `load_for_user` still yields equivalent mission snapshots.

### 7.3 What “identical” does not require

- Identical `mission_instance_id` / event ids  
- Identical log text  
- Presence of decision audit rows on the legacy path (legacy has none)

---

## 8. Explicit out-of-scope list

### 8.1 Inventory of six selection authorities (investigation framing)

Used for scope bounding in this proposal:

| # | Authority | Location (anchor) | M0? |
|---|-----------|-------------------|-----|
| 1 | Runtime A Learning Mode | `PlanningService._select_topic_for_today` → `get_next_incomplete_topic` | **No** |
| 2 | Runtime A Consolidation checkpoint | watermark / `_select_consolidation_topic` inside Learning Mode | **No** |
| 3 | Runtime A Revision Mode | `_generate_revision_mission_for_date` | **No** |
| 4 | Runtime C daily sitting selection | `generate_daily_mission` topic + package + certified LO block | **Yes — sole M0 target** |
| 5 | Twin `build_daily_study_plan` | gated; cutover OFF in production | **No** |
| 6 | Epic-2 Cap 2.8 `DecisionEngine` / EducationalOrchestrator dashboard path | `app/domain/decision/engine.py`; dashboard composer — not Runtime C Home | **No** |

### 8.2 Also untouched (not in the six, but easy to imply)

- RecommendationService advisory tips  
- MissionOptimizer (deprecated)  
- Baseline position seed (one-time enrolment)  
- Session substance re-resolve of package when unbound (same PB-002 policy; composition, not new authority)  
- Knowledge Engine / Learner Twin unification  
- `SR_TWIN_DAILY_LOOP` / Estimated Knowledge readers  
- Student-facing copy claiming adaptivity  
- Cap 2.8 numeric ranking / candidate sets as live Home authority  

M0 must not be described as “all selection now goes through the Decision Engine.”

---

## 9. Rollback strategy

Context: production deploy is **manual and currently paused** (`VERSION_1_FLAG_MATRIX` deploy note). That is an advantage: code can merge with the boundary **dark**.

| Layer | Action |
|-------|--------|
| **Instant kill-switch** | Set `KWALITEC_ADR027_M0_DECISION_BOUNDARY=0` (or unset) and redeploy when deploys resume — returns to today’s `generate_daily_mission` selection-in-Runtime-C path |
| **Default-safe merge** | Ship flag **OFF** by default; enabling is a separate, deliberate operator step |
| **Schema** | Prefer additive event type / nullable columns only. Rollback must not require a blocking downgrade to serve students |
| **Code revert** | Revert the M0 commit(s) if the flag path is wrong; Runtime C composition APIs should remain backward compatible with the legacy generator |
| **Data** | Decision audit rows are observational; leaving them in place after rollback is safe |
| **Do not** | Rely on unflagged cutover; do not delete the legacy selection path in the same PR that introduces the boundary |

---

## 10. Acceptance criteria (checkable)

M0 is **done and safe to merge** only when all of the following are true:

1. **Boundary exists:** Daily sitting decisions for Runtime C (flag ON) are produced only by `AdaptiveDecisionEngine.decide_daily_sitting` via `SittingDecisionOrchestrator`; Runtime C materialisation modules do not import the Decision Engine.  
2. **Behaviour preserved:** Dual-path / table-driven suite (§7) passes with zero divergences on decision identity fields for the agreed fixture matrix and CS1 chain walk.  
3. **Flag OFF parity:** With the flag OFF, existing Runtime C generation/experience/certification tests pass; production default remains OFF.  
4. **Policy V0 fidelity:** Policy V0 is a behavioural wrap of the pre-M0 selection helpers/order; no Twin/EK-driven branches.  
5. **Three outcomes instrumented:** Every engine invocation persists `ADAPTIVE` | `SAFE_FALLBACK` | `BLOCKED` per §5–§6; M0 soak shows `ADAPTIVE == 0`.  
6. **Blocked paths honest:** Syllabus-complete / guidance-unavailable / illegal-state cases still yield no unlawful mission and record `BLOCKED` with stable reasons.  
7. **Composition untouched in responsibility:** Session start (`StudentRuntimeCoordinator.accept_and_start_session` and below) requires no Decision Engine awareness.  
8. **Scope honesty:** Mechanisms #1–#3, #5–#6 (§8) are unmodified in behaviour and ownership.  
9. **Rollback documented:** Flag kill-switch + default-OFF posture recorded for operators (flag matrix update in the implementation PR).  
10. **Success criterion met:** The team can answer yes to: *existing decision-making behaviour moved behind the correct boundary; proven unchanged; instrumentation trustworthy for what happens next (V1).*

---

## 11. Suggested implementation touch list (for a future Agent brief — not authorized yet)

When (and only when) this proposal is accepted, a subsequent implementation brief should limit edits to approximately:

| Create | Modify |
|--------|--------|
| `app/application/adaptive_decision/` (protocol, Policy V0, orchestrator, audit helper) | `app/application/educational_experience/service.py` (call orchestrator when flag ON) |
| Tests under `tests/application/adaptive_decision/` | `app/application/educational_runtime_engine/service.py` (extract materialise-from-spec; keep legacy path) |
| Flag resolver entry + `.env.example` comment | `docs/production/VERSION_1_FLAG_MATRIX.md` |
| Optional Alembic if new event type needs enum constraints | Domain `EducationalEventType` if extended |

**Must not touch** without a new brief: PlanningService Learning Mode, Twin daily loop, Cap 2.8 DecisionEngine live wiring, student templates claiming adaptivity.

---

## 12. Open points for reviewer / chief architect

These are settled enough to implement once answered; M0 should not invent answers silently:

1. Confirm **Candidate A** over the simpler Runtime A sandbox for the first seam.  
2. Confirm M0 three-outcome framing: **`ADAPTIVE` always declines; Policy V0 → `SAFE_FALLBACK`**.  
3. Confirm audit primary store: **`runtime_educational_events` + `DECISION_RECORDED`**.  
4. Confirm naming: `SittingDecisionOrchestrator` vs reusing the string “Learning Orchestrator” in code (ADR language vs Epic-2 package collision).  
5. Confirm whether pre-chunk `objective_ids` are inside Policy V0 identity or remain composition-only (§4.1 recommendation: include pre-chunk in identity).

### Resolution (chief architect review — accepted)

Reviewed and accepted. The five open points are resolved as follows:

1. **Seam:** Candidate A (Runtime C `generate_daily_mission`) confirmed. Candidate B (Runtime A Learning Mode) remains available as a later, separately scoped M0-A migration, not folded into this one.
2. **Three-outcome framing confirmed:** in M0, the adaptive stage always declines and is never recorded as `ADAPTIVE` (stays at 0 until V1); Policy V0 success is `SAFE_FALLBACK`; Policy V0 inability is `BLOCKED`.
3. **Audit primary store confirmed:** `runtime_educational_events` with a new `DECISION_RECORDED` event type.
4. **Naming confirmed:** `SittingDecisionOrchestrator`, to avoid colliding with the existing but semantically different Epic-2 `LearningOrchestrator` and Cap 2.8 `DecisionEngine` already present in the codebase.
5. **Pre-chunk `objective_ids` confirmed** as part of Policy V0's decision identity; session-budget chunking against those objectives remains Runtime C composition, unchanged.

---

## Document control

| Field | Value |
|-------|-------|
| Authoring mode | Proposal only — **do not implement from this file alone** |
| Commit | Committed as accepted M0 design under ADR-027 (design authorization only; implementation not yet authorized) |
| Supersedes | Nothing; implements a slice of ADR-027 intent |
| Next step after acceptance | Scoped implementation brief with Goal + Touch List + mandated tests |
