# KWP-008 — Learning Diagnostics Engine

**Programme:** KWP-008 · Learning Diagnostics Engine  
**Phase:** Educational Intelligence Phase 2  
**Date:** 2026-07-30  
**Nature:** Application-layer educational cause diagnosis — **no runtime authority redesign**  
**Authority:** KWP-007 · KWP-006 · KWP-005 · SR-001A · `PRODUCT_BLUEPRINT.md`

---

## 1. Executive Summary

KWP-008 introduces the deterministic **Learning Diagnostics Engine**: a composing application authority that answers *why this learner is struggling or succeeding* from evidence the platform already holds — practice outcomes, confidence, retention/weak-topic signals, reading completion, practice-shape (numeric / MCQ), optional prerequisite titles, cadence, and Finish Review honesty.

Learning Strategy (KWP-007) continues to answer **WHAT** should happen next. Diagnostics supply cause-level **WHY** and actionable **Focus** guidance. Students never receive internal category labels (e.g. “Prerequisite weakness”); they see guidance such as “Review discount factors before continuing with annuities.”

**Verdict:** Probable learning causes are now diagnosed deterministically and composed onto Sitting Report recommendations without duplicating Evidence validation, Strategy decision rules, Twin math, Progress writing, or Runtime redesign.

---

## 2. Implementation Audit

| # | Capability | Verdict | Classification | Notes |
|---|---|---|---|---|
| 1 | Practice outcomes | Available | **EXISTING** | EV-RT-07/08/40; `StrategyEvidenceInput` practice counts |
| 2 | Confidence | Available | **EXISTING** | KWP-007 `calibrate()` / `ConfidenceCalibration` reused |
| 3 | History / cadence | Available | **EXISTING** | Streak, consecutive partials, recent session count |
| 4 | Revision / retention | Available | **EXISTING** | `retention_risk`, `days_since_topic_practice` |
| 5 | Reflection | Available | **EXISTING** | EV-RT-10 / `has_reflection` (input only) |
| 6 | Learning Strategy (WHAT) | Available | **EXISTING** · composed | Not redesigned; Sitting Report keeps strategy titles |
| 7 | Progress flags | Available | **EXISTING** | `progress_advanced`, `mission_completed` |
| 8 | Topic relationships | Partial | **EXISTING** Twin gap path · **NEW** sitting enrichments | Optional `prerequisite_title` / `strong_prerequisite` from twin_signals; no KnowledgeGapService rewrite |
| 9 | Conceptual misunderstanding | Partial reason codes in Strategy | **NEW** category | Formal diagnosis + guidance |
| 10 | Prerequisite weakness | Twin KnowledgeGap elsewhere | **NEW** sitting diagnosis | Guidance names prerequisite topic when known |
| 11 | Formula recall weakness | Absent as EI diagnosis | **NEW** | Numeric + formula hint / token heuristics |
| 12 | Calculation accuracy | Absent | **NEW** | Numeric miss with method-present pattern |
| 13 | Reading interpretation | Sitting stages exist | **NEW** | Reading skipped / completed + weak practice |
| 14 | Exam technique | Partial finishes exist | **NEW** | Partial / incomplete finish + mixed practice |
| 15 | Confidence mismatch | Exists as calibration | **EXISTING** signal · **NEW** category packaging | Labels stay internal; student guidance only |
| 16 | Retention decay | Exists as strategy recover/revise | **EXISTING** signal · **NEW** category | Cause-level WHY |
| 17 | Inconsistent practice | Momentum / partials | **NEW** | Cadence + repeated partials |
| 18 | Improving / strong (success causes) | Outcomes only | **NEW** | Correct-after-misses; strong accepted practice |
| 19 | Student guidance (no labels) | Strategy has natural copy | **NEW** diagnostics guidance module | Forbidden label scrub |
| 20 | Founder diagnostic trends | Strategy metrics only | **NEW** | Platform Intelligence section |
| 21 | Sitting Report WHAT + WHY | Strategy WHY only | **MODIFIED** | Cause WHY + Focus guidance composed |
| 22 | LearningSessionRuntime / Evidence / Twin / Progress / Mission / FSM | Must not redesign | **EXISTING** unchanged | Consumed as inputs only |

### EXISTING (reused)

- Session Evidence Packages + observation type ids (EV-001A / EV-001B)  
- `StrategyEvidenceInput.from_opaque` field vocabulary (KWP-007)  
- `calibrate()` / `performance_band()` confidence helpers (KWP-007)  
- Sitting Report projector + Complete surface (KWP-005 / KWP-007)  
- Exam Week Briefing focus detail hook (KWP-006 / KWP-007)  
- Founder Platform Intelligence pattern (Educational+ yield / Learning Strategy)  
- Product Language Guide + forbidden-term scrub  

### NEW

- `app/application/learning_diagnostics/` — DTOs, rules, guidance, engine  
- `app/services/learning_diagnostics_metrics.py` — founder diagnostic trends  
- `tests/test_kwp008_learning_diagnostics.py`  
- `KWP008_IMPLEMENTATION_REPORT.md`  

### MODIFIED

- Sitting Report VM + projector — diagnostic guidance + composed cause WHY  
- Completion / StudySession presentation DTOs and Complete template  
- Exam Week Briefing focus detail — diagnostic WHY when Revision is primary  
- Founder Platform Intelligence — Learning Diagnostics metrics section  
- Product language approved term: `Learning Diagnostics`  

---

## 3. Learning Diagnostics Architecture

```
Sitting opaque facts / Progress flags / optional Twin + cadence
        │
        ├──────────────────────────────┐
        ▼                              ▼
 LearningStrategyEngine          LearningDiagnosticsEngine
   → WHAT (action + title)         → WHY (cause) + Focus guidance
        │                              │
        └──────────┬───────────────────┘
                   ▼
         Sitting Report / Complete
           Recommended next step (WHAT)
           Why · cause explanation
           Focus · actionable guidance
                   │
                   ▼
         Founder LearningDiagnosticsMetrics
```

**Non-goals / hard boundaries**

| Authority | Relationship |
|---|---|
| Learning Strategy Engine | Not redesigned; composed for WHAT |
| EducationalEvidenceAuthority | Not called; disposition flags consumed if present |
| StudentTwinEngine | Optional read-only enrichments only (prerequisite title, retention) |
| ProgressEngine | Consumes advance flags; never writes coverage |
| LearningSessionRuntime / Session FSM | Unchanged |
| Mission Runtime / Commercial Loop | Unchanged |
| KnowledgeGapService / ERE | Left intact; sitting diagnostics do not replace Twin gap retrieval |

---

## 4. Diagnostic Categories

Internal categories (founder / audit only — **never** student-facing labels):

| Category | Typical evidence pattern | Student guidance example |
|---|---|---|
| Conceptual misunderstanding | Incorrect + over-confident, or repeated incorrect without formula/calc shape | “Revisit the core idea behind …” |
| Prerequisite weakness | Weak topic / repeated misses + prerequisite title; or strong prior + weak dependent | “Review discount factors before continuing with annuities.” |
| Formula recall weakness | Numeric/short misses + formula tokens in hints/objectives | “Refresh the key formula for …” |
| Calculation accuracy | Numeric misses with method present (some numeric correct) | “Slow down on the arithmetic …” |
| Reading interpretation | Reading skipped/incomplete or reading + MCQ misses | “Re-read the material … carefully …” |
| Exam technique | Partial/no finish + mixed practice / repeated partials | “Practise completing … under clearer steps …” |
| Confidence mismatch | Reuses KWP-007 over/under calibration | Knowledge stronger than perceived / check assumptions |
| Retention decay | Retention risk or ≥14-day gap with weakness | “Return briefly to … soon …” |
| Inconsistent practice | Repeated partials / broken cadence | “Keep a steadier study rhythm …” |
| Improving understanding | Correct after misses in the sitting | “Correct answers after earlier misses …” |
| Strong performance | All correct + accepted / advanced sitting | “Continue from a strong base …” |
| Insufficient signal | Thin evidence | Honest continue-while-evidence-accumulates |

Priority-ordered rules live in `app/application/learning_diagnostics/rules.py`. Same inputs → same `rule_id`, category, and guidance. No AI.

---

## 5. Explainability (WHAT + WHY)

Every commercial Sitting Report recommendation now carries:

| Layer | Source | Student sees |
|---|---|---|
| **WHAT** | Learning Strategy | Recommendation title + body |
| **WHY** | Diagnostics (preferred) or Strategy fallback | Cause explanation (`Why · …`) |
| **Focus** | Diagnostics guidance | Actionable next focus (`Focus · …`) — never category labels |

Example (prerequisite pattern):

> **Immediate Reinforcement**  
> Reinforce Annuities in the next Session — today's practice needs another pass.  
> Why · Misses on Annuities often trace back to gaps in Discount factors, so rebuilding that foundation comes first.  
> Focus · Review discount factors before continuing with Annuities.

Forbidden fragments (Twin, Evidence Authority, Educational+, category label names, calibration enum names, FSM, Runtime) are scrubbed from student copy.

---

## 6. Student Experience

### Sitting Report (primary)

After Finish Review → Sitting Report **Recommended next step**:

- Strategy title + body (**WHAT**)  
- Why · cause explanation (**WHY**)  
- Focus · diagnostic guidance (when a concrete cause exists)  
- Spacing / confidence guidance retained from Strategy  

### Home (secondary)

Exam Week Briefing recommended-focus detail uses diagnostic cause WHY when Revision is the primary weak-topic source — still presentation-only.

---

## 7. Founder Analytics

Extended Platform Intelligence (`/founder/alpha-observability`) with **Learning Diagnostics**:

- Primary category distribution  
- Confidence mismatch rate  
- Retention decay rate  
- Prerequisite weakness rate  
- Conceptual misunderstanding rate  
- Formula recall / calculation rates  
- Reading / exam technique rates  
- Inconsistent practice rate  

Computed by replaying packages through `LearningDiagnosticsEngine` — does not mutate authorities. Category names appear on the founder surface only.

---

## 8. Architecture Compliance

| Constraint | Status |
|---|---|
| Learning Strategy redesign | **No** — composed only |
| LearningSessionRuntime redesign | **No** |
| EducationalEvidenceAuthority | **Unchanged** |
| StudentTwinEngine | **Unchanged** |
| ProgressEngine | **Unchanged** |
| Mission Runtime / Commercial Loop / Session FSM | **Unchanged** |
| No AI / opaque scores as product | **Met** — deterministic rules + guidance |
| Students never see diagnostic labels | **Met** |
| Layering | Application engine → presentation projectors → founder metrics |
| Curriculum V1/V2 | **N/A** — no curriculum engine changes |
| Educational reasoning duplication | Composes Strategy calibration + sitting signals; does not fork Evidence / Progress / Twin math |

---

## 9. Files Modified

### Created

- `app/application/learning_diagnostics/__init__.py`  
- `app/application/learning_diagnostics/dto.py`  
- `app/application/learning_diagnostics/rules.py`  
- `app/application/learning_diagnostics/guidance.py`  
- `app/application/learning_diagnostics/engine.py`  
- `app/services/learning_diagnostics_metrics.py`  
- `tests/test_kwp008_learning_diagnostics.py`  
- `KWP008_IMPLEMENTATION_REPORT.md`  

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

## 10. Tests Executed

```bash
python3 -m pytest tests/test_kwp008_learning_diagnostics.py tests/test_kwp007_learning_strategy.py tests/test_kwp005_sitting_reports.py tests/test_kwp006_home_exam_briefing.py -q
```

**Outcome:** 53 passed.

Coverage includes prerequisite guidance (no labels), confidence mismatch, conceptual + mismatch co-findings, retention decay, improving understanding, formula / calculation / reading / exam technique, strong performance, Sitting Report WHAT+WHY+Focus composition, founder metrics distribution, template markers, approved term, and determinism.

Ruff clean on new / touched modules.

---

## 11. Known Limitations

1. Formula / calculation / reading diagnoses depend on practice-shape enrichments (response_type, hints, reading stages) — thin packages lawfully fall through to coarser causes or insufficient signal.  
2. Prerequisite titles require optional Twin / opaque enrichment; without them, weak-topic + repeated incorrect still diagnose prerequisite weakness with generic “building blocks” guidance.  
3. KnowledgeGapService / Learning Graph prerequisite traversal is not invoked from the commercial sitting path (by design: no Twin redesign).  
4. Diagnostics do not persist onto sitting metadata for History drill-down (same deferred continuity as KWP-007 strategy advice).  
5. Runtime A Decision / Mission selection unchanged — diagnostics explain causes; they do not select Today's Mission.  
6. Authored misconception banks (Version 2 education models) are not required for Phase 2; heuristics operate on existing sitting evidence only.

---

## 12. Recommendation for KWP-009

**Working title:** KWP-009 — Educational Intelligence Continuity & Authority Matrix

**Mandate:** Close the Educational Intelligence loop after Phase 1 strategy + Phase 2 diagnostics:

1. Persist last Strategy advice + Diagnostics report onto sitting metadata for History drill-down.  
2. Authority matrix: document when Learning Strategy vs Learning Diagnostics vs Runtime A Decision vs Adaptive Revision each win (no silent re-ranking).  
3. Optional richer Twin snapshot / AdaptiveDecision enrichments into diagnostic inputs (still no Twin math rewrite).  
4. Dogfood: verify students trust Sitting Report WHAT + WHY + Focus across reinforce / advance / recover / prerequisite paths.  
5. Decide whether authored misconception tags should feed diagnostic categories in a later content programme.

**Non-goals:** Evidence grade redesign, Progress Engine rewrite, Mission Runtime redesign, LLM diagnosis, notification infrastructure.

---

## Success Criteria Check

> Every educational recommendation should now have both WHAT and WHY supported by deterministic educational reasoning.

**Status:** Met for the commercial Sitting Report path. Strategy supplies WHAT; Diagnostics supply cause-level WHY and Focus guidance. Thin sittings lawfully fall through to Strategy WHY and/or insufficient-signal diagnostics. Category labels never reach students.

---

**Document status:** Complete — KWP-008 implementation deliverable  
**Next programme:** KWP-009 Educational Intelligence Continuity & Authority Matrix (recommended)  
**Architecture stance:** SR-001A authorities unchanged; Learning Diagnostics composes outputs only
