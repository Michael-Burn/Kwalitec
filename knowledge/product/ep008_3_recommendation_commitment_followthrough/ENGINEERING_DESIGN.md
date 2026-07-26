# EP-008.3 — Engineering Design

**Programme:** EP-008.3 — Recommendation Commitment & Follow-through  
**Date:** 2026-07-26  
**Status:** Design authority for successor implementation  
**Starting board:** Validated KSI **64** (K2 = **68**, K7 = **58**, K8 = **72**) — EP-008.1B  
**Primary lever:** K2 Recommendation usefulness (behavioural commitment / follow-through)  
**Secondary:** K7 Revision / continuity narrative; K8 hold (no regression)  
**Maps to:** P-004.1 **IMP-02**; EP-008.1B residual `TRUST-PERC-06`; GAP-06 acceptance KPI  

---

## 1. Problem statement

EP-008.1 / EP-008.1A shipped Recommendation Trust presentation. EP-008.1B validated that students **understand** and **state willingness** to follow schema-complete tips (K2 **55 → 68**). Runtime A educational reasoning was unchanged and remains authoritative.

The remaining gap is **behavioural**:

| Student need (success criterion) | Status after EP-008.1B |
|---|---|
| I understand why this is today’s priority | **Validated** (trust speech) |
| I **chose** to do it | **Unproven** — no conscious commitment affordance |
| I know what changed afterwards | **Partial** — review_point echo exists; no commitment→completion→reflection narrative |
| Plans feel continuous, not isolated tips | **Weak** — coherence label exists; no commitment history |
| Honest “not today” without shame | **Missing** — alternatives are informational only; no deferred commitment |

**Root cause:** RC-05 measurement half + IMP-02 — trust precedes acceptance; acceptance / follow-through still uninstrumented and unexperienced. Stated willingness ≠ commitment KPI (`LESSONS_LEARNED.md` EP-008.1B).

**This programme improves recommendation execution, not recommendation intelligence.**

---

## 2. Design thesis

> Close the educational loop from inspectable tip → conscious commitment → study session → completion → brief reflection → plan continuity → next tip, using preference/intent surfaces and authored Runtime A speech — without changing ranking, Decision Framework, or educational reasoning.

Trust made tips *worth accepting*. Commitment makes acceptance *real, honest, and measurable*.

---

## 3. Non-negotiable constraints

| Constraint | Source |
|---|---|
| Do **not** change Runtime A educational reasoning | Programme brief; Architecture Art. IV |
| Do **not** change `RecommendationService` ranking / Decision Framework / quality ladder | EP-003.1; REM-06; IMP-01 boundary |
| Do **not** change `PlanningService` / `ReadinessService` optimisation or weights | Programme brief |
| Runtime A remains sole educational authority | DR-002 |
| Presentation / commitment layer must **not** re-decide or re-rank | EP-008.1 mapper doctrine |
| No LLM / conversational AI / Learning Twin authority | Product Constitution; P-001.2 P9 |
| No speculative personalisation; personalisation flags stay OFF by default | EP-009.x boundary |
| No gamification, streaks, shame, or conversion theatre | Programme brief; K5 integrity |
| Preference / intent ≠ mastery ≠ Educational Evidence of understanding | EIP-002; Constitution Art. V §2; `record_decision` docstring |
| Single primary CTA retained (DR-050) | Decision Register |
| Behaviour metrics are **observational research only** — never feed ranking | Programme brief; EP-003.4 claim boundary |
| Effectiveness marketing freeze (DR-036) remains until separate Stage 1 evidence | EP-001 / EP-007.3 |

---

## 4. System context (authority map)

```
RecommendationService (+ quality contract)     ← READ / CALL existing preference APIs only
        │  schema-complete tip (unchanged authorship)
        ▼
Educational runtime bridge / Home trust VM     ← EP-008.1 permanent (T1–T11)
        ▼
RecommendationCommitmentService (NEW)          ← student_experience application layer
        │  commit / defer / complete-link / reflection compose / history narrative
        │  preference-journal emit (fail-open; EP-003.4)
        │  optional call: RecommendationService.record_decision(...)  [existing]
        ▼
Home / Coach / Mission / Session outcome / History surfaces
```

**Services reviewed; educational cores not modified:**

| Service | Role | EP-008.3 action |
|---|---|---|
| `RecommendationService` | Tip authorship + existing Decision Journal `record_decision` | **Call only** — no ranking / schema / Decision Framework edits |
| `ReadinessService` | Readiness MES | **Read-only** |
| `PlanningService` | Mission / plan | **Read-only** — continuity copy narrates relationship |
| Mission / unified journey | Session lifecycle | **Bind** commitment state; do not invent new educational maths |
| Learning Feedback (EP-003.4) | Observational preference events | **Emit** commitment/defer/complete/reflection-viewed (research) |
| Analytics dashboards | Operator views | Optional research read of aggregates — **no student gamification** |

---

## 5. Student journey (educational loop)

```
Recommendation (Runtime A + Trust Contract T1–T11)
        ↓
Student commitment  ("I'm doing this next.")
        ↓
Study session       (existing Mission / unified journey)
        ↓
Completion          (existing session complete)
        ↓
Reflection          (brief: what changed / why it mattered / what was learned / what next)
        ↓
Plan update         (Runtime A regenerates tip from updated state — unchanged)
        ↓
Next recommendation (continuity line: "part of one continuous study plan")
```

Tone: **educational commitment**, not gamified quest completion.

---

## 6. Commitment contract (student-visible)

### 6.1 States

| State ID | Name | Student meaning | Preference claim |
|---|---|---|---|
| **C0** | Offered | Tip visible; no commitment yet | None |
| **C1** | Committed | “I’m doing this next.” | Intent / preference |
| **C2** | In session | Session started from committed tip | Intent + engagement observation |
| **C3** | Completed | Session completed for that commitment | Preference journal + existing completion |
| **C4** | Reflected | Student viewed (or briefly confirmed) completion reflection | Observational |
| **D1** | Deferred | Honest “not today” with reason | Preference / intent only |
| **R0** | Refusal night | `honest_refusal` — commitment CTA hidden; restorative Start Session only | N/A |

State machine (happy path): `C0 → C1 → C2 → C3 → C4 → C0(next tip)`.  
Defer path: `C0 → D1` (no punishment; tip may remain available or regenerate per Runtime A as today).

### 6.2 Commitment affordance (C1)

| Rule | Detail |
|---|---|
| Label | **“I’m doing this next.”** — never “Accept AI”, “Trust the model”, or “Confirm recommendation quality” |
| Effect | Records conscious intent; enables committed chrome on Home/Mission; does **not** grant mastery |
| Relationship to Start Session | Commitment may precede or coincide with Start Session; DR-050 keeps **one** primary educational CTA. Preferred UX: primary button remains **Start Session**; commitment is an explicit adjacent confirm (“I’m doing this next”) that can be combined into one POST when starting, or a lightweight confirm before start |
| Alternatives | Remain informational (EP-008.1 T10) — selecting an alternative does **not** re-rank Runtime A; optional “Commit to this option instead” is **out of scope** (would imply selection authority) |

### 6.3 Deferred commitment (D1)

If the student cannot follow today’s tip, allow **honest reasons** from a fixed catalogue:

| Code | Student label |
|---|---|
| `not_enough_time` | Not enough time |
| `need_prerequisite` | Need a prerequisite first |
| `studying_elsewhere` | Already studying elsewhere |
| `not_today` | Not today |
| `other` | Something else (optional free-text ≤140 chars; preference only) |

Rules:

- Never punish, score-shame, streak-break, or reduce “trust score.”  
- Never manipulate (“Are you sure you want to fall behind?”).  
- Defer is **not** dismissal of educational authority — Runtime A tip remains lawful advice.  
- Copy: calm acknowledgement + optional plan-continuity line (“Your study plan continues; we’ll meet you when you’re ready.”).  
- Do **not** invent a different tip client-side.

### 6.4 Completion reflection (C3→C4)

After lawful session completion, briefly explain using **authored + preference** fields only:

| Reflection element | Source | Rule |
|---|---|---|
| What you did | Commitment title + session topic | Fact of completion |
| What changed | Authored `review_point` / Study Progress / mission completion labels already available | Pass-through; no new Twin claim |
| Why this mattered | Authored `expected_benefit` / why | Pass-through |
| What Runtime A learned | Honest static framing: practice and completion update the educational state that tips draw from — **never** “the AI learned you prefer X” unless authored preference-journal speech exists | Prefer humble; ban personal-model theatre |
| What happens next | Authored next / mission continuity / regenerated tip on return Home | Plan continuity |

Optional one-tap “Got it” advances C3→C4 (observational `reflection_viewed`).

### 6.5 Recommendation history (educational narrative)

Lightweight history — **not** an audit log:

| Entry type | Student sees |
|---|---|
| Completed | Tip title · when · short “why it mattered” (benefit) · continuity |
| Deferred | Tip title · reason label · calm note that plan continues |
| Committed incomplete (optional) | “You committed but didn’t finish” — restorative, not shaming |

Surface: extend Student History (or a compact “Recent study choices” section on Home L2 / History page). Cap recent narrative to ~7–14 days / ≤10 entries.

### 6.6 Plan continuity

Every commitment, defer, and reflection surface reinforces:

> This is part of **one continuous study plan**.

Mechanisms:

- Echo `plan_coherence_label` when authored.  
- Continuity sentence on defer and reflection.  
- History narrative ties choices to the same plan — avoid “random tip of the day” framing.

---

## 7. Data model (application / preference layer)

### 7.1 New frozen DTOs (student_experience)

**`RecommendationCommitmentSnapshot`**

| Field | Type | Notes |
|---|---|---|
| `state` | `str` | `offered` / `committed` / `in_session` / `completed` / `reflected` / `deferred` / `refusal` |
| `recommendation_key` | `str` | Stable key from authored tip (title+generated_at or bridge id) — not a new ranking id |
| `title` | `str` | Pass-through |
| `committed_at` | `str` | ISO or empty |
| `deferred_reason_code` | `str` | Catalogue code or empty |
| `deferred_reason_label` | `str` | Student-safe label |
| `continuity_line` | `str` | Presentation composition |
| `reflection` | `CommitmentReflectionSnapshot \| None` | Post-complete |

**`CommitmentReflectionSnapshot`**

| Field | Type |
|---|---|
| `what_you_did` | `str` |
| `what_changed` | `str` |
| `why_it_mattered` | `str` |
| `what_was_learned` | `str` |
| `what_happens_next` | `str` |

**`RecommendationNarrativeEntrySnapshot`** (history)

| Field | Type |
|---|---|
| `kind` | `str` | `completed` / `deferred` / `committed_incomplete` |
| `title` | `str` |
| `occurred_at` | `str` |
| `summary_line` | `str` |
| `reason_label` | `str` | Defer only |

### 7.2 Persistence options (successor chooses one; prefer minimal)

| Option | Description | Migration? |
|---|---|---|
| **A (preferred)** | New `recommendation_commitments` table owned by experience layer (preference/intent claim) + call existing `RecommendationService.record_decision` for Decision Journal continuity | Yes (additive) |
| **B** | Encode defer codes in existing `Decision.outcome_summary` + `accepted`/`completed` flags only | Possibly none; weaker narrative query |
| **C** | Learning-feedback events only (no durable student history UX) | No — **insufficient** for Design Area 4 |

**Forbidden:** treating commitment rows as mastery, readiness writes, or ranking features.

### 7.3 Explicit non-changes

- No changes to recommendation ranking / `recommendation_quality` ladder.  
- No new Twin / Adaptive educational authority.  
- No LLM-authored reflection text.  
- Behaviour metrics do not become Runtime A inputs.

---

## 8. Behaviour metrics (research-only)

Measure for research; **do not** change Runtime A.

| Metric | Definition | Claim use |
|---|---|---|
| Commitment rate | Commit events / schema-complete tip impressions (day) | K2 Strong-band evidence (with Tier B) |
| Completion rate | Completions linked to commitments / commitments | Follow-through |
| Deferred rate | Defers / tip impressions | Honesty / load |
| Reflection viewed | C4 / completions | Loop closure |
| Recommendation revisit | Return-to-Home tip views after defer | Continuity |

Privacy: scoped to authenticated user; aggregate operator views under approved PRD / analytics pilot gates (IMP-02 / EFF-06). Prefer under-claim; metrics alone ≠ educational effectiveness (DR-021 / DR-036).

---

## 9. Traceability to K2 / K7 / K8

| Design area | KSI link | Mechanism |
|---|---|---|
| Conscious commitment | **K2** | Acceptance / follow-through (PSF quantitative path) |
| Deferred honesty | **K2** + K8 hold | Agency without fake compliance; no overclaim |
| Completion reflection | **K2** + K8 hold | Closes “what changed afterwards” |
| Recommendation history | **K2** + **K7** | Narrative continuity; revision/plan story |
| Plan continuity | **K2** + K1 side-effect (prefer 0 claim) | Non-isolated actions |
| Observational metrics | K2 claimability | Unlocks Strong-band scoring discipline |

**Out of scope for claims here:** ranking precision, exam outcomes, DR-036 freeze lift, Gate G1.9.

---

## 10. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Commitment becomes conversion dark pattern | Fixed calm copy; no shame; defer first-class |
| Cognitive load / second CTA fight | Preserve DR-050; combine commit+start where possible; keep defer in disclosure |
| Metrics drive ranking temptation | Hard non-goal; STOP check |
| Reflection invents Twin learning | Authored + humble static frames only |
| History becomes audit log clutter | Cap entries; educational summary lines only |
| Touching RecommendationService “just for flags” | Call `record_decision` only; no ranking edits |
| Strong-band K2 claimed from UI without behaviour | Validation Plan prefer-lower + KPI floors |

---

## 11. Success definition (design)

Design succeeds when a successor can implement commitment / defer / reflection / history / continuity such that students consistently experience:

> “I understand why this is today’s priority.” → “I chose to do it.” → “I know what changed afterwards.”

…without any change to Runtime A educational reasoning.

Validated K2 ≥ 75 requires the Validation Plan (Tier A + behavioural observables + Tier B) — not this document alone.

---

## References

- `../ep008_1_recommendation_trust/` (Trust Contract T1–T11; permanent)  
- `../ep008_1b_recommendation_trust_validation/` (K2 68; EP-008.3 justified)  
- `../p004_1_ksi_gap_analysis/HIGH_LEVERAGE_IMPROVEMENTS.md` (IMP-02)  
- `../p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md` (explainable acceptance)  
- `../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md` (K2 measurement)  
- `../p003_5_evidence_hierarchy/EVIDENCE_HIERARCHY.md`  
- `app/services/recommendation_service.py` (`record_decision` preference journal)  
- `app/domain/recommendation/affordances.py` (accept / dismiss / defer structural hooks)  
- `app/application/student_experience/recommendation_trust.py`  

---

**End of ENGINEERING_DESIGN**
