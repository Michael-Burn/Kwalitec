# KWP-009 — Learning Difficulty & Cognitive Load Engine

**Programme:** KWP-009 · Learning Difficulty & Cognitive Load Engine  
**Phase:** Educational Intelligence Phase 3  
**Date:** 2026-07-30  
**Nature:** Application-layer educational demand modelling — **no runtime authority redesign**  
**Authority:** KWP-008 · KWP-007 · KWP-006 · SR-001A · `PRODUCT_BLUEPRINT.md`

---

## 1. Executive Summary

KWP-009 introduces the deterministic **Learning Difficulty Engine**: a composing application authority that answers *how educationally demanding this topic is for this learner* from evidence the platform already holds — practice outcomes, authored/CKG difficulty, session duration, reinforcement history, reflection, partial completion, recovery, cadence, and retention/weak-topic signals.

The engine differentiates **objective topic complexity** (normally moderate) from **observed learner difficulty** (very demanding for this student), estimates educational load without psychological labels, and recommends pacing actions such as Continue, Reduce Session Length, Increase/Decrease Spacing, Take Consolidation Session, Split Topic, Increase Challenge, and Maintain Pace.

Learning Strategy (KWP-007) continues to answer **WHAT** should happen next. Diagnostics (KWP-008) supply cause-level **WHY**. Difficulty supplies **Pace** — how demanding the journey currently is.

**Verdict:** Educational demand is now modelled deterministically and composed onto Sitting Report recommendations without duplicating Evidence validation, Strategy decision rules, Diagnostics cause rules, Twin math, Progress writing, or Runtime redesign.

---

## 2. Implementation Audit

| # | Capability | Verdict | Classification | Notes |
|---|---|---|---|---|
| 1 | Practice outcomes | Available | **EXISTING** | EV-RT-07/08/40; `StrategyEvidenceInput` practice counts |
| 2 | Learning Strategy (WHAT) | Available | **EXISTING** · composed | Not redesigned; Sitting Report keeps strategy titles |
| 3 | Learning Diagnostics (WHY) | Available | **EXISTING** · composed | Not redesigned; Focus guidance retained |
| 4 | History / cadence | Available | **EXISTING** | Streak, recent session count, consecutive partials |
| 5 | Reflection | Available | **EXISTING** | EV-RT-10 / `has_reflection` + reflection_count |
| 6 | Confidence | Available | **EXISTING** | Consumed via StrategyEvidenceInput lift only |
| 7 | Session duration | Partial in runtime | **EXISTING** signal · **NEW** load use | `actual_duration_minutes` / opaque duration |
| 8 | Repeated attempts / reinforcement | Thin | **NEW** enrichments | `topic_attempt_count`, `reinforcement_session_count` |
| 9 | Recovery rate | Partial (diagnostics recovered_after_misses) | **EXISTING** shape · **NEW** load use | Softens observed difficulty / load points |
| 10 | Topic history / authored difficulty | CKG `DifficultyBand` exists | **EXISTING** vocabulary · **NEW** mapping | Maps foundational→light … capstone→intensive |
| 11 | Objective topic complexity | Absent as EI model | **NEW** | Authored prefer; heuristic fallback |
| 12 | Learner-specific (observed) difficulty | Absent | **NEW** | Outcomes + reinforcement + weak-topic |
| 13 | Learning effort | ERE effort minutes catalogue elsewhere | **NEW** sitting effort band | Does not rewrite ERE thresholds |
| 14 | Educational pacing | Strategy momentum / spacing exist | **NEW** pacing posture | Hold / Slow / Maintain / Accelerate |
| 15 | Session intensity | Adaptive intensity notes elsewhere | **NEW** sitting intensity | Light → Overloaded (internal) |
| 16 | Revision pressure | Strategy spacing / Adaptive urgency | **NEW** pressure band | Composes; does not re-rank Strategy |
| 17 | Load recommendations | Strategy has overlapping titles | **NEW** load vocabulary | Continue / Reduce length / Spacing / Split / … |
| 18 | Student experience (natural Pace) | Strategy + Diagnostics on Complete | **MODIFIED** | Pace · guidance line |
| 19 | Founder load analytics | Strategy + Diagnostics metrics only | **NEW** | Highest load topics, reinforcement, pacing, recovery |
| 20 | LearningSessionRuntime / Evidence / Twin / Progress / Mission / FSM | Must not redesign | **EXISTING** unchanged | Consumed as inputs only |

### EXISTING (reused)

- Session Evidence Packages + observation type ids (EV-001A / EV-001B)  
- `StrategyEvidenceInput.from_opaque` field vocabulary (KWP-007)  
- CKG / authored difficulty string vocabulary (`DifficultyBand` conceptual map)  
- Sitting Report projector + Complete surface (KWP-005 / KWP-007 / KWP-008)  
- Founder Platform Intelligence pattern (yield / Strategy / Diagnostics)  
- Product Language Guide + forbidden-term scrub  

### NEW

- `app/application/learning_difficulty/` — DTOs, complexity, load, rules, guidance, engine  
- `app/services/learning_difficulty_metrics.py` — founder difficulty / load trends  
- `tests/test_kwp009_learning_difficulty.py`  
- `KWP009_IMPLEMENTATION_REPORT.md`  

### MODIFIED

- Sitting Report VM + projector — difficulty Pace guidance composed  
- Completion / StudySession presentation DTOs and Complete template  
- Founder Platform Intelligence — Learning Difficulty metrics section  
- Product language approved term: `Learning Difficulty`  

---

## 3. Learning Difficulty Architecture

```
Sitting opaque facts / Progress flags / optional Twin + cadence
        │
        ├──────────────────┬──────────────────────┐
        ▼                  ▼                      ▼
 LearningStrategyEngine   LearningDiagnosticsEngine   LearningDifficultyEngine
   → WHAT (action)          → WHY (cause) + Focus       → Pace (demand / load)
        │                  │                      │
        └──────────────────┴──────────────────────┘
                           ▼
                 Sitting Report / Complete
                   Recommended next step (WHAT)
                   Why · cause explanation
                   Focus · diagnostic guidance
                   Pace · difficulty guidance
                           │
                           ▼
                 Founder LearningDifficultyMetrics
```

**Non-goals / hard boundaries**

| Authority | Relationship |
|---|---|
| Learning Strategy Engine | Not redesigned; composed for WHAT |
| Learning Diagnostics Engine | Not redesigned; composed for WHY / Focus |
| EducationalEvidenceAuthority | Not called; disposition flags consumed if present |
| StudentTwinEngine | Optional read-only enrichments only (difficulty, attempts, recovery) |
| ProgressEngine | Consumes advance flags; never writes coverage |
| LearningSessionRuntime / Session FSM | Unchanged |
| Mission Runtime / Commercial Loop | Unchanged |
| ERE `effort_for_difficulty` | Left intact; sitting engine does not rewrite ERE catalogues |

---

## 4. Difficulty Modelling

### Objective vs observed

| Layer | Source | Example |
|---|---|---|
| **Objective complexity** | Authored / CKG difficulty (preferred) or LO / practice-volume heuristic | Chapter 15 · normally moderate |
| **Observed difficulty** | Practice outcomes, reinforcement, weak-topic, recovery | Observed as very demanding for this learner |
| **Gap** | `observed_rank − objective_rank` | Positive gap → different pacing (consolidation / split) |

Objective bands (internal): Light / Moderate / Demanding / Intensive / Unknown.  
Observed bands (internal): Light / Moderate / Demanding / Very demanding / Unknown.

Students never see these band names — only natural Pace copy.

### Cognitive / educational load

Deterministic 0–100 load points from:

| Signal | Effect |
|---|---|
| Repeated mistakes | Increases load |
| Reflection with weak practice | Increases load |
| High session frequency | Increases load |
| Partial completion / abandoned | Increases load |
| Long study duration | Increases intensity / load |
| Repeated reinforcement | Increases load + revision pressure |
| Recovery after misses | Softens load and observed band |
| Clean strong sitting | Softens load |

**Never** uses psychological labels (cognitive load, burnout, anxiety, fatigue) in student copy.

### Derived postures

| Posture | Values (internal) |
|---|---|
| Learning effort | Low / Steady / High / Very high |
| Educational pacing | Hold / Slow / Maintain / Accelerate |
| Session intensity | Light / Standard / Heavy / Overloaded |
| Revision pressure | None / Light / Elevated / Urgent |

---

## 5. Decision Rules

Priority-ordered deterministic rules (`app/application/learning_difficulty/rules.py`):

| Priority | Evidence pattern | Recommendation |
|---|---|---|
| 1 | Very demanding + heavy reinforcement + repeated misses | Split Topic |
| 2 | Overloaded intensity / very long dense sitting | Reduce Session Length |
| 3 | Observed ≫ objective, urgent revision pressure, or demanding + ≥2 misses | Take Consolidation Session |
| 4 | Elevated/light pressure with misses or retention risk | Decrease Spacing |
| 5 | Heavy intensity + high effort | Reduce Session Length |
| 6 | Light observed + strong / advanced sitting | Increase Challenge |
| 7 | Stable light topic, no revision pressure | Increase Spacing |
| 8 | Recovered after difficult / misses | Continue |
| 9 | Light / moderate / unknown observed | Maintain Pace |
| 10 | Fallback | Continue |

No AI. Same inputs → same `rule_id`, recommendation, postures, and explanation.

---

## 6. Student Experience

### Sitting Report (primary)

After Finish Review → Sitting Report **Recommended next step**:

- Strategy title + body (**WHAT**)  
- Why · cause explanation (**WHY** from Diagnostics, Strategy fallback)  
- Focus · diagnostic guidance  
- **Pace · difficulty guidance** (KWP-009)  
- Spacing / confidence guidance retained from Strategy  

Example:

> **Take Consolidation Session**  
> Pace · This topic has required more practice than recent topics. A shorter reinforcement session is recommended before progressing from Annuities.  
> Why · Annuities is normally a moderately demanding topic, but today's practice made it feel harder — more practice than usual was needed.

Forbidden fragments (Twin, Evidence Authority, Educational+, band names, cognitive load, overloaded, psychological labels, FSM, Runtime) are scrubbed from student copy.

### Home

No Home redesign in KWP-009 — Pace surfaces on Sitting Report / Complete. Exam Week Briefing remains Strategy/Diagnostics composition from KWP-007/008.

---

## 7. Founder Analytics

Extended Platform Intelligence (`/founder/alpha-observability`) with **Learning Difficulty**:

- Sittings evaluated  
- Average load points  
- Consolidation rate  
- Reduce session length rate  
- Recovery after difficult topics  
- Pacing trends (slow / maintain / accelerate)  
- Topics generating highest average load  
- Average reinforcement by topic  
- Recommendation distribution  

Computed by replaying packages through `LearningDifficultyEngine` — does not mutate authorities. Internal band / load labels appear on the founder surface only.

---

## 8. Architecture Compliance

| Constraint | Status |
|---|---|
| Learning Strategy redesign | **No** — composed only |
| Learning Diagnostics redesign | **No** — composed only |
| LearningSessionRuntime redesign | **No** |
| EducationalEvidenceAuthority | **Unchanged** |
| StudentTwinEngine | **Unchanged** |
| ProgressEngine | **Unchanged** |
| Mission Runtime / Commercial Loop / Session FSM | **Unchanged** |
| No AI / opaque scores as product | **Met** — deterministic rules + guidance |
| Students never see band / psych labels | **Met** |
| Layering | Application engine → presentation projectors → founder metrics |
| Curriculum V1/V2 | **N/A** — no curriculum engine changes |
| Educational reasoning duplication | Composes Strategy input lift + sitting signals; does not fork Evidence / Progress / Twin / Strategy / Diagnostics math |

---

## 9. Files Modified

### Created

- `app/application/learning_difficulty/__init__.py`  
- `app/application/learning_difficulty/dto.py`  
- `app/application/learning_difficulty/complexity.py`  
- `app/application/learning_difficulty/load.py`  
- `app/application/learning_difficulty/rules.py`  
- `app/application/learning_difficulty/guidance.py`  
- `app/application/learning_difficulty/engine.py`  
- `app/services/learning_difficulty_metrics.py`  
- `tests/test_kwp009_learning_difficulty.py`  
- `KWP009_IMPLEMENTATION_REPORT.md`  

### Modified

- `app/presentation/session/sitting_report.py`  
- `app/presentation/session/view_models.py`  
- `app/presentation/session/dto/study_session.py`  
- `app/presentation/session/services/study_session_service.py`  
- `app/templates/session/partials/session_body.html`  
- `app/presentation/product_language.py`  
- `app/founder/dashboard/routes.py`  
- `app/founder/dashboard/templates/founder_dashboard/alpha_observability.html`  

### Migration Impact

**None.**

---

## 10. Tests Executed

```bash
python3 -m pytest tests/test_kwp009_learning_difficulty.py \
  tests/test_kwp008_learning_diagnostics.py \
  tests/test_kwp007_learning_strategy.py \
  tests/test_kwp005_sitting_reports.py \
  tests/test_kwp006_home_exam_briefing.py -q
```

**Outcome:** 71 passed.

Coverage includes objective vs observed gap, consolidation / reduce length / split / increase challenge, spacing recommendations, recovery continue, student-copy safety (no psych / band labels), Sitting Report Pace composition, founder highest-load + reinforcement metrics, template markers, approved term, and determinism.

Ruff clean on new / touched modules.

---

## 11. Known Limitations

1. Authored difficulty depends on Twin / opaque enrichment (`difficulty` / `difficulty_band`); without it, objective complexity falls back to LO / practice-volume heuristics.  
2. Reinforcement and topic-attempt counts require optional cadence / Twin enrichments — thin packages lawfully under-estimate repeated-topic load.  
3. Session duration intensifies load only when `session_duration_minutes` / `actual_duration_minutes` is present on the opaque package.  
4. Difficulty advice is not persisted onto sitting metadata for History drill-down (same deferred continuity as KWP-007/008).  
5. Runtime A Decision / Mission selection unchanged — difficulty explains demand and pacing; it does not select Today's Mission.  
6. ERE effort catalogues and Adaptive intensity envelopes are not rewritten — sitting load is a parallel Educational Intelligence model.

---

## 12. Recommendation for KWP-010

**Working title:** KWP-010 — Educational Intelligence Continuity & Authority Matrix

**Mandate:** Close the Educational Intelligence loop after Phase 1–3:

1. Persist last Strategy advice + Diagnostics report + Difficulty profile onto sitting metadata for History drill-down.  
2. Authority matrix: document when Learning Strategy vs Diagnostics vs Difficulty vs Runtime A Decision vs Adaptive Revision each win (no silent re-ranking).  
3. Optional richer Twin snapshot enrichments (authored difficulty, reinforcement counts, duration) into EI inputs (still no Twin math rewrite).  
4. Dogfood: verify students trust Sitting Report WHAT + WHY + Focus + Pace across reinforce / consolidate / split / challenge paths.  
5. Decide whether Version 2 authored misconception / difficulty tags should feed objective complexity more richly.

**Non-goals:** Evidence grade redesign, Progress Engine rewrite, Mission Runtime redesign, LLM load scoring, notification infrastructure, psychological profiling.

---

## Success Criteria Check

> Kwalitec should understand not only what students know, or why they struggle, but how educationally demanding the journey currently is for them.

**Status:** Met for the commercial Sitting Report path. Strategy supplies WHAT; Diagnostics supply cause-level WHY and Focus; Difficulty supplies Pace — objective vs observed demand, effort, intensity, revision pressure, and natural load recommendations. Thin sittings lawfully fall through to Maintain Pace / Continue. Band and psychological labels never reach students.

---

**Document status:** Complete — KWP-009 implementation deliverable  
**Next programme:** KWP-010 Educational Intelligence Continuity & Authority Matrix (recommended)  
**Architecture stance:** SR-001A authorities unchanged; Learning Difficulty composes outputs only
