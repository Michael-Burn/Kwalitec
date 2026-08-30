# ADR-027 Phase 3 — V1 Adaptive Policy Design

**Status:** Proposal for empirical verification against current code. Not yet accepted; does **not** authorize implementation.  
**Governing ADR:** [`docs/adr/ADR-027-student-knowledge-state-and-adaptive-decision-architecture.md`](../adr/ADR-027-student-knowledge-state-and-adaptive-decision-architecture.md)  
**Nature:** Implementation design under ADR-027 (not a new ADR)  
**Date:** 2026-08-30  
**Verified against:** current working tree (Runtime A `PlanningService` Learning Mode consolidation; Runtime C / M0 `SittingDecisionOrchestrator` + Policy V0; `LearnerTwinQueryPort` + `DailyLoopLearnerTwinQueryAdapter`; `DECISION_RECORDED` audit)  
**Predecessors:** [`ADR027_M0_DECISION_BOUNDARY_DESIGN.md`](ADR027_M0_DECISION_BOUNDARY_DESIGN.md), [`ADR027_PHASE2_CANONICAL_TWIN_DESIGN.md`](ADR027_PHASE2_CANONICAL_TWIN_DESIGN.md)

---

## Document purpose

Phase 3 proposes the first genuinely adaptive Decision Engine policy (Policy V1): when a Consolidation moment is due, select the revisit topic from Learner Twin Estimated Knowledge under an evidence floor, with honest SAFE_FALLBACK when evidence is insufficient, and with exam-proximity weighting of Consolidation vs new material.

This document records that design and the empirical verification of its open questions against current code. It does **not** authorize application changes.

---

## Placement rationale

This file lives under `docs/architecture/` beside the M0 and Phase 2 ADR-027 design documents. ADR-027 itself remains in `docs/adr/`. This document is a **design proposal under that ADR**, not a competing architectural decision.

---

## Context

Phase 2 made the Learner Twin the genuine, unconditional, canonical source of Estimated Knowledge for this product. Policy V0, introduced in Phase 1 (M0), was a deliberate behavioral wrap of the existing linear selection logic, designed specifically to prove the Decision Engine boundary was correct without yet introducing any adaptive intelligence. Its own governing design was explicit that policy sophistication should be earned by real evidence rather than anticipated in advance.

Before scoping this phase, it was raised as a genuine concern that no real students yet exist, and that building a more sophisticated policy now might mean designing its actual logic from assumptions rather than evidence, the exact pattern this project has deliberately avoided everywhere else. This concern was corrected on reflection: it had conflated the absence of a large body of real usage with the absence of any legitimate basis for a first policy at all. The person building this product intends to use it themselves as a real student preparing for real, consequential professional exams before anyone else does, which is itself a genuine, if initially small, evidence loop, and the product's own existing teaching-strategy documentation already establishes real, defensible principles this policy can be built from rather than invented. The standing development philosophy adopted for this project going forward is to build the best-reasoned version of a given piece of the system now, grounded in realistic assumptions and whatever the product has already established as sound, and to refine it once real use exists, rather than either guessing without grounding or refusing to build anything until a large population of real users has accumulated.

## What V1 changes, and what it deliberately does not

Learning Mode's day to day selection of new material remains exactly as Policy V0 left it: syllabus order, no interleaving of topics before a student has covered them for the first time. This boundary is deliberately preserved because this product's own teaching-strategy law already names introducing mixed-topic practice before single-topic competence as a real cognitive-overload risk, and nothing about this phase's own evidence changes that judgement.

The genuine, well-grounded gap this phase closes is narrower and more specific: this project's own investigation earlier in this effort found that Consolidation Missions, the product's existing mechanism for revisiting previously covered material, currently choose which topic to revisit using a fixed calendar cadence rather than any real signal about what the student is actually weak on. Now that Estimated Knowledge is genuinely canonical, this is the natural and well-founded first place to introduce real adaptivity, because it corrects an existing mechanism's honesty rather than inventing a new one.

## The V1 policy

When a Consolidation moment is due, using the existing cadence trigger already present in the product, the topic selected for that consolidation is determined as follows.

First, restrict consideration to topics the student has already covered, for which the Learner Twin has admitted genuine evidence, meaning the topic has been practised enough to produce a real Estimated Knowledge value rather than merely being marked complete with no evidence yet recorded. A topic that is covered but has no Twin evidence is treated as not yet assessed, never as a candidate for being called weak.

Second, restrict this candidate set further to only those topics with at least three independent evidenced observations recorded by the Twin. A single observation is not a reliable enough signal to act on: a student can answer one question correctly by chance or incorrectly through a momentary slip, and treating either as settled evidence of genuine strength or weakness would be an unsound basis for a real decision, not merely an early one. Three is the customary minimum floor used in educational measurement for an estimate that is no longer pure noise, while still being realistically achievable quickly by an actual student working through the platform.

Third, if there are at least two or three topics meeting that bar, select the one with the lowest Estimated Knowledge among them as the consolidation target, breaking ties by whichever has gone longest since it was last practised. If fewer than that minimum number of topics meet the evidence bar, the policy falls back to the existing Consolidation selection logic exactly as it behaves today. This fallback is not an unhandled failure; it is the correct, expected, honestly recorded outcome for a student, including the product's own creator in his own early personal use, who has not yet generated enough evidence for a genuinely reliable comparison, and should be recorded as a safe fallback outcome rather than silently presented as if it were an adaptive choice.

Fourth, as a student's exam date approaches, Consolidation is weighted more heavily relative to the introduction of new material, tapering how much new content is introduced as the exam nears rather than switching abruptly at a single point in time. This should begin as a gradual, continuously increasing effect starting around six weeks before the exam date, becoming strongly weighted toward review in the final two to three weeks. A smooth ramp rather than a single hard cutoff is deliberately preferred, both because an abrupt, single-point behaviour change would be a noticeable and somewhat arbitrary discontinuity for a real student to experience, and because this shape is consistent with the broader spacing-effect literature on how review density should relate to time remaining before a point where retention is being tested, and mirrors how experienced candidates already tend to treat the final weeks before a professional exam sitting as a distinct, more review-heavy phase in their own self-directed study.

## Relationship to the existing architecture

This is Policy V1 behind the Decision Engine boundary already established in Phase 1. It does not change that boundary, the Learning Orchestrator, or Runtime C's role as a pure executor. It reads Estimated Knowledge exclusively through the canonical Learner Twin query interface established in Phase 2, and it must never read from any of the retired legacy mastery representations. It must produce the same three recorded outcomes already established for every decision: a genuinely adaptive, evidence-driven consolidation selection is recorded as adaptive; falling back to the existing cadence-based selection because too little evidence yet exists is recorded as a safe fallback, honestly, not as if it were adaptive; and any case where no valid selection can be made at all remains a blocked outcome, consistent with existing handling.

## Open questions for verification, not for guessing

This design is written from principle and from what this project already knows about its own architecture, but the following must be verified against the actual current code before being treated as accepted, rather than assumed:

1. Where exactly does the existing Consolidation cadence trigger live in code today, and what does it currently receive as input?
2. Whether a student's exam date is already available as context at the point this decision would be made, and in what form.
3. Whether the Learner Twin's query interface, as it exists after Phase 2, can already answer both an Estimated Knowledge value and an evidence count for a given topic, or whether the evidence count specifically would need to be added to that interface.
4. Whether the existing three recorded decision outcomes can be extended to this new policy without modification, or whether anything about how they are currently recorded assumes there is only ever one policy in play.

## Consequences

This is expected to be the first decision this product makes about a real student that is genuinely adaptive in the sense the entire architecture leading up to this phase exists to make possible: a decision that follows from what the system has actually observed about that specific student, rather than a fixed rule applied identically to everyone. It is deliberately narrow in scope, touching only which topic is chosen at an existing review moment, and deliberately conservative in what it is willing to trust as evidence, so that its first real exercise, including by the product's own creator using it as a genuine student, is a meaningful and honest test of whether this specific, well-reasoned starting policy is actually good, rather than a test of something invented without any grounding at all.

---

## Verification findings

Empirical re-check against the current working tree (2026-08-30). Findings only — no implementation approach.

### 1. Consolidation cadence trigger — where it lives and what it receives

**Two spines; only one has Consolidation today.**

| Spine | Live for sole-runtime CS1 Home? | Consolidation? |
|-------|----------------------------------|----------------|
| **Runtime C** + M0 Decision Engine / Policy V0 | Yes — Home/Journey via `SittingDecisionOrchestrator.ensure_todays_sitting` → Runtime C materialisation (`app/application/adaptive_decision/orchestrator.py`, `policy_v0.py`) | **None.** `EducationalRuntimeEngineService` has no consolidation/watermark/checkpoint selection. M0 explicitly left Runtime A Consolidation **out of scope** (`ADR027_M0_DECISION_BOUNDARY_DESIGN.md` §8.1 row 2). |
| **Runtime A Learning Mode** | Only students **without** Runtime C enrolment (TEMPORARY RI-002 path); not Home for Runtime C CS1 | **Yes** — watermark + topic selection inside `PlanningService._select_topic_for_today` (`app/services/planning_service.py` ~1457–1588) |

**Runtime A trigger (exact):**

- Inputs: `user_id`, `active_plan: StudyPlan`, `target_date: date`.
- Reads `active_plan.new_topics_since_consolidation_checkpoint` (integer watermark) and `active_plan.exam_date`.
- Cadence: `_consolidation_cadence(days_remaining)` where `days_remaining = (exam_date - target_date).days` — stepped bands: `>60` → every **4** new CLT topics; `30–60` → every **3**; `<30` → every **2** (`planning_service.py` ~1300–1310).
- When `watermark >= cadence`, calls `_select_consolidation_topic(user_id, active_plan, curriculum)`.

**Runtime A topic selection today (complicates the design narrative):**

- `_select_consolidation_topic` → `_weak_covered_topics_for_consolidation` already ranks **covered** leaf topics by Twin EK via `topic_ek_by_orm_id` / `ek_display_0_100`, keeps those whose stage from Twin EK is Learning or Not Started, sorts ascending EK, avoids immediate repeat via `last_consolidation_topic_id` (~1388–1454).
- Covered topics with **no** Twin evidence are currently forced to `mastery_value = 0.0` and therefore **can be selected as weak** — opposite of the Phase 3 rule that no-EK covered topics must never be called weak.

**Contradiction with design prose:** The draft says Consolidation currently chooses the revisit topic by a “fixed calendar cadence rather than any real signal about weakness.” Empirically: (a) the **when** trigger is a **topic-count watermark** whose threshold steps with exam proximity (not a calendar “pick this day”); (b) the **which topic** choice on Runtime A is already Twin-EK-ordered among “weak” covered topics; (c) the sole-runtime Decision Engine path has **no** Consolidation mechanism at all. Clause 4’s smooth 6-week continuous ramp does not exist; Runtime A uses discrete 4/3/2 bands at 60/30-day boundaries only, and only on that spine.

**Additional empirical complication (watermark increment wiring):** The designed increment of `new_topics_since_consolidation_checkpoint` lives in `_apply_mission_topic_progress` in `app/mission/routes.py` (~212–244), on first-time CLT Study Progress completion only. Repo-wide, that helper is only defined in that module and is not called from other `app/` production paths (legacy `complete_mission` now delegates to Study Session). Selection/reset logic still runs when the watermark is already high enough, but live watermark growth on the current completion path is not evidenced by an `app/` caller outside tests.

### 2. Exam date availability at the decision point

- **StudyPlan:** `exam_date` is a required `Date` column (`app/models/study_plan.py`); `get_weeks_remaining()` and Learning Mode selection both use it.
- **Runtime A consolidation decision point:** yes — `active_plan.exam_date` is in hand inside `_select_topic_for_today`.
- **M0 Decision Engine / Policy V0:** `DailySittingRequest` carries only `user_id`, `subject_code`, `mission_date`, optional `curriculum_identity` (`app/application/adaptive_decision/types.py`). **No exam_date / days_remaining / proximity.** The adaptive decision package has zero references to exam_date.
- **Nearby but unused by the engine:** Runtime C `EnrolmentSnapshot.exam_date` exists on the enrolment DTO (`app/application/educational_runtime_engine/dto.py`); the orchestrator loads enrolment for `curriculum_identity` only and does not pass `exam_date` into `DailySittingRequest`.
- **Learner Twin query surface:** no exam-date / exam-proximity fields on `LearnerTwinQueryPort` / `TopicKnowledgeFact`.
- **Elsewhere:** `ExamTimeline.get_timeline` and related readiness/dashboard paths load active plan `exam_date` and compute `days_remaining` (`app/services/exam_timeline.py`) — presentation/KPI use, not Decision Engine input.

### 3. Learner Twin query interface — EK and evidence count

`LearnerTwinQueryPort` (`app/application/student_twin/query.py`) already exposes both via `TopicKnowledgeFact`:

- `has_estimated_knowledge: bool`
- `estimated_knowledge: float | None`
- `estimated_mastery: float | None`
- **`evidence_count: int`**
- **`last_practised_at: datetime | None`**
- plus coverage via `topic_covered(...)`

Methods: `knowledge_snapshot`, `topic_knowledge`, `topics_with_estimated_knowledge`, `topic_covered`.

Adapter `DailyLoopLearnerTwinQueryAdapter._fact_from_twin` (`app/infrastructure/adapters/student_twin/query_adapter.py`) sets `evidence_count=len(events)` from Twin history and `last_practised_at` from max event time. **Evidence count does not need to be added** for the Phase 3 filters as written; the port already answers EK + evidence count + last practised. There is no precomputed `days_since_practice` on the port (callers would derive it from `last_practised_at`).

Note: Runtime A consolidation today does **not** call this port; it uses `twin_cutover_service.topic_ek_by_orm_id` / `ek_display_0_100` and does not apply an evidence-count floor.

### 4. Three outcomes / DECISION_RECORDED and a second policy intent

**Outcome enum itself is policy-agnostic:** `DecisionOutcome` = `ADAPTIVE | SAFE_FALLBACK | BLOCKED` (`app/application/adaptive_decision/types.py`).

**Recording already carries multi-policy fields:** each `SittingDecision` and each `DECISION_RECORDED` payload includes `intent`, `policy_id`, `outcome`, `reason_codes`, `selection_trace` (`app/application/adaptive_decision/audit.py`). Constants today: `INTENT_DAILY_SITTING`, `POLICY_V0_ID`.

**What assumes a single daily-sitting seam (report only — not a proposed fix):**

- Protocol is a single method `decide_daily_sitting` (`app/application/adaptive_decision/protocol.py`).
- Result type is `SittingDecision` shaped for daily sitting (package/LO/campaign fields).
- Audit hardcodes `"seam": "runtime_c.generate_daily_mission"`.
- Orchestrator only drives Runtime C daily sitting and **forbids** `ADAPTIVE` under M0 Policy V0 (`orchestrator.py`).
- Nothing in the outcome enum or audit schema **forbids** a second `intent` / `policy_id` string; the **types, protocol method, and seam hardcoding** are what currently assume one intent (daily sitting) on one seam (Runtime C).

Extending to Consolidation therefore is not “outcomes must change,” but the current M0 surface is daily-sitting-specific and Runtime-C-seamed; Consolidation still lives only on Runtime A, which M0 never wrapped.

### Consequences of these findings for the design as written (findings only)

The Phase 3 design’s premise that the first adaptive act is “honest Consolidation topic pick at an existing cadence moment” is **architecturally mismatched with the sole-runtime path**: that path has no Consolidation trigger. On the path that *does* have Consolidation (Runtime A), topic pick is already Twin-EK-ordered, and no-EK covered topics are already treated as weak — so the “first adaptive honesty” claim overlaps existing Runtime A behaviour in part, while the evidence-count floor and no-EK exclusion would be **behaviour changes** relative to that path, not greenfield.

---

## Document control

| Field | Value |
|-------|-------|
| Authoring mode | Proposal + verification — **do not implement from this file alone** |
| Commit | Design document only; does not accept Phase 3 or authorize implementation |
| Supersedes | Nothing |
| Does not supersede | M0 decision boundary design; Phase 2 canonical Twin design |
| Next step after acceptance | Scoped implementation brief with Goal + Touch List (separate from this file) |
