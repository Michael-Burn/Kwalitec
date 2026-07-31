# KWP-007 — Learning Strategy Engine

**Programme:** KWP-007 · Learning Strategy Engine  
**Phase:** Educational Intelligence Phase 1  
**Date:** 2026-07-30  
**Nature:** Application-layer educational strategy composition — **no runtime authority redesign**  
**Authority:** KWP-006 · KWP-005 · KWP-004 · KWP-003 · SR-001A · EV-001A · EV-001B · SDT-004 · `PRODUCT_BLUEPRINT.md`

---

## 1. Executive Summary

KWP-007 introduces the deterministic **Learning Strategy Engine**: a composing application authority that answers *what educational strategy should come next* from evidence the platform already holds — sitting practice outcomes, Finish Review honesty, Progress advance flags, optional confidence reports, retention/weak-topic signals, and study cadence.

The engine produces **recommendations, not scores** — Advance Topic, Consolidate Understanding, Immediate Reinforcement, Scheduled Revision, Increase Challenge, Recover Prior Knowledge, Maintain Current Pace, Slow Progression, Repeat Practice, and Practice to Build Certainty — each with a student-readable **WHY**. Internal confidence calibration (healthy / over-confident / under-confident) is translated into natural guidance and **never** shown as labels.

**Verdict:** Fragmented strategy signals across Twin RecommendationPolicy, Adaptive revision urgency, Progress advance gates, Sitting Report heuristics, and the shadow MS-005 StrategyEngine are now **composed** into one Educational Intelligence Phase 1 vocabulary without duplicating evidence validation, Twin math, Progress writing, or Runtime A re-ranking.

---

## 2. Implementation Audit

| # | Capability | Verdict | Classification | Notes |
|---|---|---|---|---|
| 1 | Strategy decisions (advance / revise / consolidate / …) | Fragmented → unified vocabulary | **NEW** engine · **EXISTING** signal sources | Composes sitting + Progress + optional Twin/cadence; does not replace DecisionEngine / ProgressEngine |
| 2 | Recommendation generation (not scores) | Partial (Twin / Journey / Adaptive / Runtime A) | **NEW** strategy titles · reuses explain patterns | Student titles match product brief |
| 3 | Confidence calibration → guidance | Partial (shadow StrategyEngine divergence) | **NEW** calibration module | Labels internal only |
| 4 | Spaced revision timing | Partial (`RevisionUrgency` 4-band) | **NEW** SpacingDecision (+ **No review**) | Evidence-derived; no fixed calendar invent |
| 5 | Learning momentum | Partial (velocity / consistency / narrative) | **NEW** momentum projector | No new persistence |
| 6 | Explainability (WHY) | Existing chains elsewhere | **NEW** strategy explainability · **MODIFIED** Sitting Report | Every advice has WHY |
| 7 | Student-facing strategy | Thin (tomorrow preview heuristics) | **MODIFIED** Sitting Report + Home briefing detail | Strategy block on Complete |
| 8 | Founder strategy metrics | Educational+ yield only | **NEW** LearningStrategyMetrics | Platform Intelligence section |
| 9 | LearningSessionRuntime / Evidence / Twin / Progress / Mission / FSM | Must not redesign | **EXISTING** unchanged | Consumed as inputs only |

### EXISTING (reused)

- Session Evidence Packages + observation type ids (EV-001A / EV-001B)  
- Progress advance / mission-completed flags (SR-003 ProgressEngine outputs)  
- Twin `ConfidenceBand` vocabulary for numeric → band mapping  
- Adaptive `RevisionUrgency` conceptual bands (Immediate / Today / This week / Deferred) as design reference  
- Sitting Report opaque projector (KWP-005)  
- Exam Week Briefing / Home Insights (KWP-006)  
- Educational+ yield founder surface (KWP-004 / KWP-005)  
- Product Language Guide + forbidden-term scrub  

### NEW

- `app/application/learning_strategy/` — DTOs, rules, calibration, spacing, momentum, explainability, engine  
- `app/services/learning_strategy_metrics.py` — founder strategy distribution  
- `tests/test_kwp007_learning_strategy.py`  
- `KWP007_IMPLEMENTATION_REPORT.md`  

### MODIFIED

- Sitting Report VM + projector — strategy recommendation + WHY  
- Completion / StudySession presentation DTOs and Complete template  
- Exam Week Briefing focus detail — strategy WHY when Revision is primary  
- Founder Platform Intelligence — Learning Strategy metrics section  
- Product language approved term: `Learning Strategy`  

---

## 3. Learning Strategy Architecture

```
Sitting opaque facts / Progress flags / optional Twin + cadence
        │
        ▼
 StrategyEvidenceInput.from_opaque(...)
        │
        ▼
 LearningStrategyEngine.evaluate(...)
   ├─ rules.select_strategy          → StrategyAction + rule_id
   ├─ calibration.calibrate          → internal ConfidenceCalibration
   ├─ spacing.decide_spacing         → SpacingDecision
   ├─ momentum.derive_momentum       → MomentumPosture
   └─ explainability.*               → title, body, WHY, natural guidance
        │
        ▼
 LearningStrategyAdvice (student_projection omits calibration labels)
        │
        ├─ Sitting Report / Complete surface
        ├─ Home Exam Week Briefing focus detail (Revision path)
        └─ Founder LearningStrategyMetrics (batch over packages)
```

**Non-goals / hard boundaries**

| Authority | Relationship |
|---|---|
| EducationalEvidenceAuthority | Not called; disposition flags consumed if present |
| StudentTwinEngine | Optional read-only enrichments only |
| ProgressEngine | Consumes advance flags; never writes coverage |
| LearningSessionRuntime / Session FSM | Unchanged |
| Mission Runtime / Commercial Loop | Unchanged |
| Runtime A DecisionEngine | Not re-ranked; strategy is educational posture, not mission selection |
| MS-005 StrategyEngine (shadow) | Left shadow; KWP-007 does not enable the flag |

---

## 4. Decision Rules

Priority-ordered deterministic rules (`app/application/learning_strategy/rules.py`):

| Priority | Evidence pattern | Strategy |
|---|---|---|
| 1 | Abandoned / retention risk + weakness / long gap + weak | Recover Prior Knowledge |
| 2 | Incorrect + over-confident calibration | Consolidate Understanding |
| 3 | Repeated incorrect (all wrong / incorrect dominates) | Immediate Reinforcement / Consolidate |
| 4 | Correct + under-confident calibration | Practice to Build Certainty |
| 5 | Repeated partial finishes / partial + mixed | Slow Progression |
| 6 | Incorrect cluster | Repeat Practice / Immediate Reinforcement |
| 7 | Long gap / retention risk without weak crash | Scheduled Revision |
| 8 | Sustained strong (+ healthy/unknown calibration) | Increase Challenge |
| 9 | Strong + accepted / honest finish | Advance Topic |
| 10 | Default | Maintain Current Pace |

No AI. Same inputs → same `rule_id`, action, spacing, and explanation.

---

## 5. Explainability

Every `LearningStrategyAdvice` includes:

- `recommendation_title` — product vocabulary  
- `recommendation_body` — what to do  
- `explanation` — **WHY** in learner language  

Example (reinforcement):

> Today's Session revisits Apply discount factors because repeated practice misses show they need reinforcement before introducing new material.

Forbidden fragments (Twin, Evidence Authority, Educational+, over/under-confident labels, FSM, Runtime) are scrubbed from student copy.

---

## 6. Confidence Calibration

| Internal label | When | Student sees |
|---|---|---|
| Healthy | Confidence and practice align | Natural “aligned” guidance (no “Healthy” word) |
| Over-confident | High confidence + weak/mixed practice | Check-assumptions guidance |
| Under-confident | Low confidence + strong practice | Certainty-catch-up practice guidance |
| Unknown | No confidence signal | Empty confidence guidance |

Students never see the internal enum names.

---

## 7. Spacing Strategy

| Decision | Typical triggers |
|---|---|
| Immediate | Reinforce / consolidate / recover / repeat |
| Tomorrow | Practice for certainty / slow progression / maintain with gaps |
| This week | Scheduled revision / advance with residual risk |
| Later | Long gap reinforcement |
| No review | Strong advance / increase challenge without weakness |

Timing is evidence-derived. The engine does **not** invent calendar dates or write `next_review_date`.

---

## 8. Learning Momentum

Derived from existing sitting + cadence flags (no new tables):

| Posture | Signal sketch |
|---|---|
| Recovery | Abandoned, finish=no, retention+weak |
| Plateau | Repeated partial / mixed flat practice |
| Acceleration | Progress advanced + strong practice |
| Consistency | Streak / recent session cadence |
| Topic stability | Accurate practice without misses |
| Quiet | Insufficient practice signal |

---

## 9. Student Experience

### Sitting Report (primary)

After Finish Review → Sitting Report includes **Recommended next step**:

- Strategy title + body  
- Why · explanation  
- Spacing guidance  
- Confidence guidance (natural language only)  

Tomorrow preview prefers strategy posture; Advance still names the next topic when known.

### Home (secondary)

Exam Week Briefing recommended-focus detail uses a strategy WHY when Revision is the primary weak-topic source — still presentation-only.

---

## 10. Founder Analytics

Extended Platform Intelligence (`/founder/alpha-observability`) with **Learning Strategy**:

- Strategy distribution counts  
- Advance / reinforcement / recovery / revision rates  
- Immediate spacing rate  
- Internal over/under confidence rates (founder-only)  

Computed by replaying packages through `LearningStrategyEngine` — does not mutate authorities.

---

## 11. Architecture Compliance

| Constraint | Status |
|---|---|
| LearningSessionRuntime redesign | **No** |
| EducationalEvidenceAuthority | **Unchanged** |
| StudentTwinEngine | **Unchanged** |
| ProgressEngine | **Unchanged** |
| Mission Runtime / Commercial Loop / Session FSM | **Unchanged** |
| No AI / opaque scores as product | **Met** — deterministic rules + recommendations |
| Layering | Application engine → presentation projectors → founder metrics |
| Curriculum V1/V2 | **N/A** — no curriculum engine changes |
| Recommendation duplication | Composes existing signals; does not fork Evidence / Progress / Twin math |

---

## 12. Files Modified

### Created

- `app/application/learning_strategy/__init__.py`  
- `app/application/learning_strategy/dto.py`  
- `app/application/learning_strategy/calibration.py`  
- `app/application/learning_strategy/spacing.py`  
- `app/application/learning_strategy/momentum.py`  
- `app/application/learning_strategy/rules.py`  
- `app/application/learning_strategy/explainability.py`  
- `app/application/learning_strategy/engine.py`  
- `app/services/learning_strategy_metrics.py`  
- `tests/test_kwp007_learning_strategy.py`  
- `KWP007_IMPLEMENTATION_REPORT.md`  

### Modified

- `app/presentation/session/sitting_report.py`  
- `app/presentation/session/view_models.py`  
- `app/presentation/session/dto/study_session.py`  
- `app/presentation/session/services/study_session_service.py`  
- `app/templates/session/partials/session_body.html`  
- `app/presentation/student/exam_week_briefing.py`  
- `app/presentation/product_language.py`  
- `app/founder/dashboard/routes.py`  
- `app/founder/dashboard/templates/founder_dashboard/alpha_observability.html`  

### Migration Impact

**None.**

---

## 13. Tests Added

```bash
python3 -m pytest tests/test_kwp007_learning_strategy.py tests/test_kwp005_sitting_reports.py tests/test_kwp006_home_exam_briefing.py -q
```

**Outcome:** 35 passed.

Coverage includes decision rules (reinforce / consolidate / advance / recover / spacing / challenge / slow), calibration label concealment, Sitting Report strategy projection, founder metrics distribution, template markers, approved term, and determinism.

---

## 14. Known Limitations

1. Strategy is composed from sitting-local + optional enrichments — full Twin snapshot / AdaptiveDecision pipeline is not required for Phase 1 and may remain unused when signals are thin.  
2. MS-005 shadow `StrategyEngine` remains OFF and is not unified into KWP-007 (future promotion / authority matrix).  
3. Runtime A Decision / Mission selection is unchanged — Learning Strategy advises educational posture; it does not replace Today's Mission selection.  
4. Spacing does not write review schedules into TopicProgress / Memory Engine.  
5. Home surfaces strategy WHY mainly via Revision-led briefing detail — richer History → stored Sitting Report drill-down remains deferred.  
6. Founder calibration rates are internal analytics; students never see those labels.

---

## 15. Recommendation for KWP-008

**Working title:** KWP-008 — Strategy Continuity & Authority Alignment

**Mandate:** Close the Educational Intelligence loop after Phase 1 strategy composition:

1. Persist last Learning Strategy advice onto sitting metadata for History drill-down continuity.  
2. Authority matrix: document when Learning Strategy vs Runtime A Decision vs Adaptive Revision each win (no silent re-ranking).  
3. Optional read-path from Twin snapshot / AdaptiveDecision into `StrategyEvidenceInput` enrichments (still no Twin math rewrite).  
4. Dogfood: verify students trust Sitting Report WHY across reinforce / advance / recover paths.  
5. Decide whether to retire or promote MS-005 shadow StrategyEngine planners behind the same vocabulary.

**Non-goals:** Evidence grade redesign, Progress Engine rewrite, Mission Runtime redesign, LLM recommendations, notification infrastructure.

---

## Success Criteria Check

> A student should trust that every recommendation is educationally justified, clearly explained, and personalised using their own learning evidence. No AI. No opaque decisions. Deterministic educational reasoning only.

**Status:** Met for the commercial Sitting Report path when practice / finish / Progress signals exist. Thin sittings lawfully fall through to Maintain Current Pace with honest WHY. Calibration labels never reach students.

---

**Document status:** Complete — KWP-007 implementation deliverable  
**Next programme:** KWP-008 Strategy Continuity & Authority Alignment (recommended)  
**Architecture stance:** SR-001A authorities unchanged; Learning Strategy composes outputs only  
